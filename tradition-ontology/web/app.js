"use strict";
/* Plain JS, no frameworks. Every string from the server or the user is put into the page with textContent
   (never innerHTML), so nothing typed by a person or written by a model can become markup or script. */

const $ = (id) => document.getElementById(id);
const PID_KEY = "onto_person_id";
const RID_KEY = "onto_reading_id";
const MAX_BYTES = 24 * 1024;
let adminToken = "";
let lastMarkdown = "";
let age = null;

function el(tag, attrs, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "class") n.className = v;
    else if (k === "text") n.textContent = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else if (v === true) n.setAttribute(k, "");
    else if (v !== false && v != null) n.setAttribute(k, String(v));
  }
  for (const k of kids.flat()) {
    if (k == null || k === false) continue;
    n.append(k instanceof Node ? k : document.createTextNode(String(k)));
  }
  return n;
}
const clear = (n) => { while (n.firstChild) n.removeChild(n.firstChild); return n; };
const pid = () => sessionStorage.getItem(PID_KEY) || "";
const say = (t) => { $("status").textContent = t || ""; };

async function api(path, opts = {}) {
  const headers = { "Accept": "application/json" };
  if (opts.body !== undefined) headers["Content-Type"] = "application/json";
  if (pid()) headers["X-Person-Id"] = pid();
  if (opts.admin) headers["X-Admin-Token"] = adminToken;
  let res;
  try {
    res = await fetch(path, { method: opts.method || "GET", headers,
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined, credentials: "same-origin" });
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Could not reach the server. Please try again." } };
  }
  const type = res.headers.get("content-type") || "";
  let data = null;
  if (type.includes("json")) { try { data = await res.json(); } catch (e) { data = null; } }
  else { data = await res.text(); }
  return { ok: res.ok, status: res.status, data };
}
const errText = (r) => (r.data && r.data.message) || "Something went wrong. Please try again.";

/* ---------- views ---------- */
function show(view) {
  for (const v of ["reading", "data", "admin"]) $("view-" + v).hidden = v !== view;
  document.querySelectorAll(".tab").forEach((t) => {
    if (t.dataset.view === view) t.setAttribute("aria-current", "page"); else t.removeAttribute("aria-current");
  });
  say("");
  if (view === "data") { $("data-empty").hidden = !!pid(); }
}
function step(name) {
  for (const s of ["consent", "intake", "report"]) $("step-" + s).hidden = s !== name;
}
document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => show(t.dataset.view)));

/* ---------- consent ---------- */
async function loadConsent() {
  const r = await api("/api/consent");
  if (!r.ok) { say(errText(r)); return; }
  const box = clear($("consent-text"));
  for (const p of r.data.text || []) box.append(el("p", { text: p }));
  $("consent-label").textContent = r.data.checkbox || "";
}
function renderStop(container, msg) {
  clear(container);
  container.append(el("h3", { text: msg.title || "Let's pause here" }));
  if (msg.body) container.append(el("p", { text: msg.body }));
  for (const x of msg.extra || []) container.append(el("p", { text: x }));
  if ((msg.resources || []).length) {
    const ul = el("ul", { "aria-label": "Where to find help" });
    for (const r of msg.resources) ul.append(el("li", {}, el("strong", { text: r.region + ": " }), r.name + " — " + r.contact));
    container.append(ul);
  }
  container.hidden = false;
}
$("consent-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const err = $("consent-error");
  err.textContent = "";
  const a = parseInt($("age").value, 10);
  if (!Number.isInteger(a) || a < 1 || a > 129) { err.textContent = "Please give your age as a number."; $("age").focus(); return; }
  if (!$("consent-box").checked && a >= 18) { err.textContent = "Please tick the box to agree."; $("consent-box").focus(); return; }
  const r = await api("/api/start", { method: "POST", body: { age: a, consent: $("consent-box").checked } });
  if (!r.ok) { err.textContent = errText(r); return; }
  if (r.data.declined) {
    step("report");
    $("report").replaceChildren();
    renderStop($("stop-box"), r.data.declined);
    $("h-report").focus();
    return;
  }
  age = a;
  sessionStorage.setItem(PID_KEY, r.data.person_id);
  sessionStorage.removeItem(RID_KEY);
  step("intake");
  $("h-intake").scrollIntoView();
});

/* ---------- intake ---------- */
async function loadQuestions() {
  const r = await api("/api/questions");
  if (!r.ok) { say(errText(r)); return; }
  const box = clear($("questions"));
  for (const q of r.data) {
    if (q.type !== "free_text") continue;   // age is asked on the first screen; scale or option picks are never evidence
    const id = "q-" + q.id;
    box.append(el("div", { class: "field" },
      el("label", { for: id, text: q.text }),
      el("textarea", { id, rows: 3, maxlength: 2000, "data-qid": q.id })));
  }
}
function gatherInputs() {
  const answers = {};
  document.querySelectorAll("#questions textarea").forEach((t) => { if (t.value.trim()) answers[t.dataset.qid] = t.value.trim(); });
  const inputs = { answers, free_text: $("free-text").value.trim(), dialogue: $("dialogue").value.trim(),
    dialogue_speaker: $("speaker").value.trim() };
  if (age !== null) inputs.age = age;
  return inputs;
}
$("intake-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const err = $("intake-error");
  err.textContent = "";
  const body = { person_id: pid(), inputs: gatherInputs() };
  if ($("engine").value) body.engine = $("engine").value;
  if (new TextEncoder().encode(JSON.stringify(body)).length > MAX_BYTES) {
    err.textContent = "That is too much text for one reading. Please shorten some answers."; return;
  }
  const btn = $("intake-submit");
  btn.disabled = true;
  say("Reading what you wrote. This can take a little while.");
  const r = await api("/api/reading", { method: "POST", body });
  btn.disabled = false;
  say("");
  if (!r.ok) {
    err.textContent = errText(r);
    if (r.status === 403) { sessionStorage.removeItem(PID_KEY); }
    return;
  }
  if (r.data.reading_id) sessionStorage.setItem(RID_KEY, r.data.reading_id);
  showReport(r.data.report, r.data.markdown);
  // the person's words are not kept in the page once the reading is made
  document.querySelectorAll("#questions textarea").forEach((t) => { t.value = ""; });
  $("free-text").value = ""; $("dialogue").value = "";
});

/* ---------- report ---------- */
function citeLine(ids, cites) {
  const out = [];
  for (const id of ids || []) { const c = (cites || {})[id]; if (c) out.push((c.title || "") + " " + (c.ref || "")); }
  return out.join("; ");
}
function pointItem(p, cites, prefix) {
  const li = el("li", {}, prefix ? el("strong", { text: prefix }) : null, p.text + " ");
  const c = citeLine(p.cites, cites);
  const meta = [p.basis, c].filter(Boolean).join("; ");
  if (meta) li.append(el("span", { class: "cite", text: "(" + meta + ")" }));
  return li;
}
function showReport(rep, md) {
  lastMarkdown = md || "";
  step("report");
  const box = clear($("report"));
  const stop = $("stop-box");
  stop.hidden = true;
  $("checkin-box").hidden = true;
  $("report-actions").hidden = false;
  $("dl-md").hidden = !md;
  const stopMsg = rep.stopped;
  for (const n of rep.notices || []) box.append(el("p", { class: "notice", text: n }));
  if (stopMsg) {
    renderStop(stop, stopMsg);
    $("dl-md").hidden = true;
    $("h-report").focus();
    return;
  }
  box.prepend(el("p", { class: "standing", text: "This reading reflects what you wrote through the lens of traditional texts. It is not a diagnosis, not medical or psychological advice, and it does not predict anything." }));
  const cites = rep.citations || {};
  if (rep.insufficient) {
    box.append(el("div", { class: "card" }, el("p", { text: rep.insufficient })));
    box.append(el("p", {}, el("button", { type: "button", onclick: () => step("intake") }, "Add more and try again")));
    $("dl-md").hidden = true;
    $("h-report").focus();
    return;
  }
  if (rep.summary) box.append(el("h3", { text: "What you shared, in brief" }), el("p", { text: rep.summary }));
  if ((rep.mappings || []).length) {
    box.append(el("h3", { text: "Patterns the texts describe" }));
    for (const m of rep.mappings) {
      const card = el("div", { class: "card" }, el("h4", { text: m.name + " (" + m.lens_label + ")" }));
      for (const e of m.evidence || []) card.append(el("p", { class: "quote", text: "“" + e.quote + "”" }));
      card.append(el("p", { text: "Why this fits: " + (m.why || "") }));
      card.append(el("p", { text: "How sure: " + m.confidence }));
      const c = citeLine(m.cites, cites);
      if (c) card.append(el("p", { class: "cite", text: "Texts: " + c }));
      box.append(card);
    }
  }
  for (const [key, title] of [["vedic", "The Vedic and yogic reading"], ["ascetic", "The ascetic reading (Buddhist and Jain)"]]) {
    const lens = (rep.lenses || {})[key];
    if (!lens) continue;
    box.append(el("h3", { text: title }));
    if ((lens.points || []).length) box.append(el("ul", {}, lens.points.map((p) => pointItem(p, cites))));
    else if (lens.note) box.append(el("p", { text: lens.note }));
  }
  const rec = rep.reconciliation || {};
  if ((rec.points || []).length || (rec.differences || []).length) {
    box.append(el("h3", { text: "How the two readings fit together" }));
    const ul = el("ul");
    for (const p of rec.points || []) ul.append(pointItem(p, cites));
    for (const d of rec.differences || []) ul.append(pointItem(d, cites, "Where they differ: "));
    box.append(ul);
  }
  const pw = rep.pathway || {};
  if ((pw.practices || []).length) {
    box.append(el("h3", { text: "A gentle practice pathway" }));
    for (const p of pw.practices) {
      const card = el("div", { class: "card" }, el("h4", { text: p.name }), el("p", { text: p.why || "" }));
      card.append(el("ol", {}, (p.steps || []).map((s) => el("li", { text: s }))));
      const d = p.duration || {};
      if (d.minutes_per_session) {
        const m = d.minutes_per_session;
        card.append(el("p", { text: "Length: " + m[0] + "–" + m[m.length - 1] + " minutes, " + (d.sessions_per_day || 1) + " time(s) a day (" + (d.basis || "") + ")." }));
      }
      for (const w of p.warnings || []) {
        card.append(el("p", {}, el("strong", { text: "The texts' caution: " }), w.text + " ",
          el("span", { class: "cite", text: "(" + citeLine(w.cites, cites) + ")" })));
      }
      const c = citeLine(p.cites, cites);
      if (c) card.append(el("p", { class: "cite", text: "Texts: " + c }));
      box.append(card);
    }
    if ((pw.sequence || []).length) {
      box.append(el("h3", { text: "Your 14 days" }), el("ul", {}, pw.sequence.map((s) => el("li", { text: "Day " + s.day + ": " + s.plan }))));
    }
    if (pw.checkin_prompt) box.append(el("h3", { text: "Daily check-in" }), el("p", { text: pw.checkin_prompt }));
  }
  const cl = Object.values(cites);
  if (cl.length) {
    box.append(el("h3", { text: "Sources" }));
    box.append(el("ul", {}, cl.map((c) => el("li", {}, el("strong", { text: (c.title || "") + " " + (c.ref || "") }),
      " (" + c.level + ")" + (c.original ? " — “" + c.original.slice(0, 160) + "”" : "")))));
  }
  if (sessionStorage.getItem(RID_KEY)) $("checkin-box").hidden = false;
  $("h-report").focus();
}
$("dl-md").addEventListener("click", () => download("my-reading.md", lastMarkdown, "text/markdown"));
$("print").addEventListener("click", () => window.print());
$("again").addEventListener("click", () => { step("intake"); $("stop-box").hidden = true; });

function download(name, text, type) {
  const url = URL.createObjectURL(new Blob([text], { type: type + ";charset=utf-8" }));
  const a = el("a", { href: url, download: name });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/* ---------- check-in ---------- */
$("checkin-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const out = clear($("ck-result"));
  $("ck-stop").hidden = true;
  const text = $("ck-text").value.trim();
  if (!text) { out.textContent = "Write a line or two first."; $("ck-text").focus(); return; }
  const r = await api("/api/checkin", { method: "POST", body: { person_id: pid(), reading_id: sessionStorage.getItem(RID_KEY) || null,
    day: parseInt($("ck-day").value, 10), text } });
  if (!r.ok) { out.textContent = errText(r); return; }
  if (r.data.stopped) { renderStop($("ck-stop"), r.data.stopped); $("ck-text").value = ""; return; }
  out.textContent = "Saved.";
  for (const n of r.data.notes || []) out.append(el("p", { class: "notice", text: n }));
  $("ck-text").value = "";
});

/* ---------- my data ---------- */
$("data-view-btn").addEventListener("click", async () => {
  const out = clear($("data-out"));
  if (!pid()) { $("data-empty").hidden = false; return; }
  const r = await api("/api/me");
  if (!r.ok) { out.textContent = errText(r); return; }
  out.append(el("pre", { text: JSON.stringify(r.data, null, 2) }));
});
$("data-export").addEventListener("click", async () => {
  if (!pid()) { $("data-empty").hidden = false; return; }
  const r = await api("/api/me");
  if (!r.ok) { say(errText(r)); return; }
  download("my-data.json", JSON.stringify(r.data, null, 2), "application/json");
  say("Your data was downloaded.");
});
$("data-delete").addEventListener("click", () => {
  if (!pid()) { $("data-empty").hidden = false; return; }
  $("data-confirm").hidden = false; $("data-confirm-no").focus();
});
$("data-confirm-no").addEventListener("click", () => { $("data-confirm").hidden = true; $("data-delete").focus(); });
$("data-confirm-yes").addEventListener("click", async () => {
  const r = await api("/api/me", { method: "DELETE" });
  $("data-confirm").hidden = true;
  if (!r.ok) { say(errText(r)); return; }
  sessionStorage.removeItem(PID_KEY); sessionStorage.removeItem(RID_KEY);
  clear($("data-out")); clear($("report")); lastMarkdown = ""; age = null;
  $("stop-box").hidden = true; $("checkin-box").hidden = true;
  step("consent");
  say("Everything held about you was deleted.");
});

/* ---------- admin ---------- */
$("admin-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  adminToken = $("admin-token").value;
  $("admin-token").value = "";
  const r = await api("/api/admin/buckets", { admin: true });
  if (!r.ok) { $("admin-body").hidden = true; say(r.status === 403 ? "That token was not accepted." : errText(r)); return; }
  const b = clear($("draft-bucket")), f = clear($("draft-format"));
  for (const x of r.data.buckets) b.append(el("option", { value: x.id, text: x.name }));
  for (const x of r.data.formats) f.append(el("option", { value: x, text: x }));
  $("admin-body").hidden = false;
  say("");
  await Promise.all([loadPosts(), loadCosts()]);
});
$("post-status").addEventListener("change", loadPosts);

async function loadPosts() {
  const st = $("post-status").value;
  const r = await api("/api/admin/posts" + (st ? "?status=" + encodeURIComponent(st) : ""), { admin: true });
  const box = clear($("posts"));
  if (!r.ok) { box.textContent = errText(r); return; }
  if (!r.data.length) { box.append(el("p", { text: "Nothing here." })); return; }
  for (const p of r.data) box.append(postCard(p));
}
function postCard(p) {
  const b = p.body || {};
  const ta = el("textarea", { rows: 6, "aria-label": "Post text; separate parts with a line of three dashes" }, );
  ta.value = (b.parts || []).join("\n---\n");
  const note = el("input", { type: "text", maxlength: 300, "aria-label": "Reviewer note" });
  const chk = p.check || {};
  const probs = ((chk.rules || {}).problems || []).join("; ");
  const done = async (action) => {
    const body = { action, note: note.value };
    if (action === "edit") body.body = Object.assign({}, b, { parts: ta.value.split(/\n-{3}\n/).map((s) => s.trim()).filter(Boolean) });
    const r = await api("/api/admin/posts/" + encodeURIComponent(p.id) + "/review", { method: "POST", admin: true, body });
    say(r.ok ? "Saved." : errText(r));
    if (r.ok) loadPosts();
  };
  return el("div", { class: "card" },
    el("h4", { text: p.bucket + " · " + p.format + " · " + p.status }),
    el("p", { class: "cite", text: "Source: " + (b.source || "") + (probs ? " · Check: " + probs : "") }),
    el("p", { class: "cite", text: "Reminder: " + (b.ai_label || "") }),
    ta,
    el("div", { class: "field" }, el("label", { text: "Note" }), note),
    el("button", { type: "button", class: "primary", onclick: () => done("approve") }, "Approve"),
    el("button", { type: "button", onclick: () => done("edit") }, "Save edit"),
    el("button", { type: "button", class: "danger", onclick: () => done("reject") }, "Reject"));
}
async function loadCosts() {
  const r = await api("/api/admin/costs", { admin: true });
  const box = clear($("costs"));
  if (!r.ok) { box.textContent = errText(r); return; }
  const rows = Object.entries(r.data);
  if (!rows.length) { box.append(el("p", { text: "No model calls recorded yet." })); return; }
  const t = el("table", {}, el("thead", {}, el("tr", {}, ["Kind", "Count", "Cost (USD)", "Average", "Input tokens", "Output tokens"].map((h) => el("th", { scope: "col", text: h })))));
  const tb = el("tbody");
  for (const [k, v] of rows) tb.append(el("tr", {}, [k, v.count, v.cost_usd, v.avg_cost_usd, v.input_tokens, v.output_tokens].map((x) => el("td", { text: String(x) }))));
  t.append(tb); box.append(t);
}
$("draft-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  say("Drafting.");
  const r = await api("/api/admin/drafts", { method: "POST", admin: true,
    body: { bucket: $("draft-bucket").value, format: $("draft-format").value, n: parseInt($("draft-n").value, 10) || 1 } });
  say(r.ok ? "Queued " + r.data.queued.length + ", not passed " + r.data.failed.length + "." : errText(r));
  if (r.ok) { $("post-status").value = "pending"; loadPosts(); loadCosts(); }
});
$("cal-btn").addEventListener("click", async () => {
  const r = await api("/api/admin/calendar?bucket=" + encodeURIComponent($("draft-bucket").value), { admin: true });
  const box = clear($("calendar"));
  if (!r.ok) { box.textContent = errText(r); return; }
  const tb = el("tbody");
  for (const d of r.data) tb.append(el("tr", {}, [d.day, d.format, d.status, d.first_line || ""].map((x) => el("td", { text: String(x) }))));
  box.append(el("table", {}, el("thead", {}, el("tr", {}, ["Day", "Format", "Status", "First line"].map((h) => el("th", { scope: "col", text: h })))), tb));
});

/* ---------- start ---------- */
(async function init() {
  await Promise.all([loadConsent(), loadQuestions()]);
  if (pid()) step("intake"); else step("consent");
})();
