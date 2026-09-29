"""Content engine: drafts per bucket and account voice, each joining an everyday scene to ONE cited teaching.

Pipeline for every draft: pick (scene, teaching) → draft (rules template, or the model: Sonnet, medium) → check
(rules checks always; plus the model check: Opus, high, when the model engine is on) → review queue (pending).
The app never posts anywhere. Posts never use personal data. Design: ENGINE_SPEC.md §14 and rules/content/.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import time
from functools import lru_cache
from typing import Optional

from . import claims, config, ontology
from .llm import LLMError, Ledger, ModelClient

DEFAULT_FORMATS = {
    "x_post": {"parts": [1, 1], "max_chars_per_part": 280},
    "x_thread": {"parts": [4, 7], "max_chars_per_part": 280},
    "ig_carousel": {"parts": [6, 9], "max_words_per_part": 30, "caption_max_words": 120},
    "short_video": {"parts": [4, 10], "total_words": [110, 160]},
    "long_video": {"parts": [5, 7]},
}
PERSONAL_DATA = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d[\d\s-]{8,}\d|https?://", re.I)
CLOSINGS = ["Where does this show up in your week?", "What would it look like to notice this once, today?",
            "Which part of this is true for you?", "What changes if you read your day this way?",
            "Sit with that for a moment."]


@lru_cache(maxsize=1)
def buckets() -> dict:
    p = config.RULES / "content" / "buckets.json"
    if not p.exists():
        return {}
    return {b["id"]: b for b in json.loads(p.read_text(encoding="utf-8"))["buckets"]}


@lru_cache(maxsize=1)
def formats() -> dict:
    p = config.RULES / "content" / "formats.json"
    if not p.exists():
        return DEFAULT_FORMATS
    d = json.loads(p.read_text(encoding="utf-8"))
    return d.get("formats", d)


@lru_cache(maxsize=None)
def voice(bucket_id: str) -> str:
    p = config.RULES / "voices" / f"{bucket_id}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _limits(fmt: str) -> dict:
    f = dict(DEFAULT_FORMATS.get(fmt, {}))
    spec = formats().get(fmt) or {}
    for k in ("parts", "max_chars_per_part", "max_words_per_part", "caption_max_words", "total_words"):
        if k in spec:
            f[k] = spec[k]
    return f


def source_line(tid: str) -> str:
    c = ontology.citation(tid)
    return f"{c['title']} {c['ref']}".strip()


# --- selection ---------------------------------------------------------------------------------
def _used_pairs(store, bucket_id: str, days: int = 30) -> tuple[set, set]:
    cutoff = time.time() - 86400 * days
    pairs, tids = set(), set()
    for p in store.list_posts():
        if p["bucket"] != bucket_id or p["created"] < cutoff or p["status"] == "rejected":
            continue
        b = p["body"]
        pairs.add((b.get("scene_idx"), b.get("tid")))
        tids.add(b.get("tid"))
    return pairs, tids


def pick(store, bucket_id: str, fmt: str, seed: int = 0) -> Optional[tuple[int, dict]]:
    """A (scene, pool item) pair not used by this account in 30 days; each teaching at most once per 30 days."""
    b = buckets()[bucket_id]
    pairs, tids = _used_pairs(store, bucket_id)
    pool = [it for it in b["teaching_pool"] if ontology.citable(it["tid"]) and it["tid"] not in tids]
    rng = random.Random(f"{bucket_id}:{fmt}:{seed}:{len(pairs)}")
    rng.shuffle(pool)
    scenes = list(range(len(b["scenes"])))
    rng.shuffle(scenes)
    for it in pool:
        for s in scenes:
            if (s, it["tid"]) not in pairs:
                return s, it
    return None


# --- drafting ----------------------------------------------------------------------------------
def _sentence(s: str) -> str:
    s = (s or "").strip()
    return s if not s or s[-1] in ".?!…”\"" else s + "."


def rules_draft(bucket_id: str, fmt: str, scene_idx: int, item: dict) -> dict:
    b = buckets()[bucket_id]
    scene = _sentence(b["scenes"][scene_idx])
    point, angle, src = _sentence(item["point"]), _sentence(item.get("angle", "")), source_line(item["tid"])
    close = CLOSINGS[int(hashlib.sha1(f"{bucket_id}{scene_idx}{item['tid']}".encode()).hexdigest(), 16) % len(CLOSINGS)]
    if fmt == "x_post":
        parts = [f"{scene} {point} ({src})"]
        if len(parts[0]) + len(angle) + 1 <= 280 and angle:
            parts = [f"{scene} {point} {angle} ({src})"]
    elif fmt == "x_thread":
        parts = [scene, f"An old text puts it this way: {point} ({src})", angle, close]
        c = ontology.citation(item["tid"])
        if c.get("paraphrase") and len(c["paraphrase"]) <= 270:
            parts.insert(2, _sentence(c["paraphrase"]))
    elif fmt == "ig_carousel":
        parts = [scene, "An old text has a word for this.", point, f"Source: {src}", angle, close]
    elif fmt == "short_video":
        parts = _short_video_parts(scene, point, angle, src, close, item["tid"])
    elif fmt == "long_video":
        c = ontology.citation(item["tid"])
        parts = [f"1. The scene: {scene}", f"2. The teaching: {point} ({src})",
                 f"3. What the text says, read closely: {_sentence(c.get('paraphrase', ''))}",
                 f"4. The link: {angle}", f"5. Where the text stops: it describes; it does not promise results.",
                 f"6. Close: {close}"]
    else:
        raise ValueError(f"unknown format {fmt}")
    body = {"bucket": bucket_id, "format": fmt, "scene_idx": scene_idx, "tid": item["tid"], "source": src,
            "parts": [p for p in parts if p.strip()], "engine": "rules", "ai_label": _ai_label(fmt)}
    if fmt == "ig_carousel":
        body["caption"] = f"{scene} {point} {angle} Source: {src}."
    return body


BRIDGES = ["Notice what the text does and does not say. It describes what happens in the mind; it promises nothing.",
           "Read it slowly. It is not advice from outside you. It is a description you can check against your own day.",
           "The old texts are often this plain. They name the thing, and leave the seeing to the reader."]


def _words(t: str) -> int:
    return len(re.sub(r"\[on screen:[^\]]*\]", "", t).split())


def _short_video_parts(scene, point, angle, src, close, tid) -> list[str]:
    """45–60 s script: 110–160 spoken words (on-screen cues excluded), built only from the pool item and the
    ontology's own paraphrase, plus one fixed bridge sentence that makes no claim."""
    c = ontology.citation(tid)
    head = [f"[on screen: {scene}] {scene}", f"[on screen: {src}] There is an old text that says it plainly. {point}"]
    tail = [angle, f"[on screen: {close}] {close}"]
    body, n = [], _words(" ".join(head + tail))
    for sent in re.split(r"(?<=[.!?])\s+", c.get("paraphrase") or ""):
        if sent and n + len(sent.split()) <= 150:
            body.append(sent)
            n += len(sent.split())
        if n >= 115:
            break
    parts = head + ([f"Here is what the passage says, closely: {' '.join(body)}"] if body else []) + tail
    b = int(hashlib.sha1(tid.encode()).hexdigest(), 16) % len(BRIDGES)
    while _words(" ".join(parts)) < 110 and b < len(BRIDGES) * 2:
        parts.insert(-1, BRIDGES[b % len(BRIDGES)])
        b += 1
    return parts


def _ai_label(fmt: str) -> str:
    spec = formats().get(fmt) or {}
    return spec.get("ai_label_reminder") or "Label AI-assisted media where the platform requires it."


DRAFT_SYSTEM = """You draft one social post for a human editor to review. You never publish anything.
Join the everyday scene to the ONE teaching given, using only the teaching's own point as given; never stretch it.
Follow the account's voice guide and the tone guide. Plain, warm, exact. Cite the source line exactly as given.
Never: health, cure, therapy, sleep or stress-relief claims; diagnosis or clinical words; predictions or astrology;
modern research or psychology; promises ('you will'); personal data; hashtags beyond two; emojis as content.
Return JSON only."""
DRAFT_SCHEMA = {"type": "object", "properties": {"parts": {"type": "array", "items": {"type": "string"}},
                "caption": {"type": "string"}}, "required": ["parts", "caption"], "additionalProperties": False}
CHECK_SYSTEM = """You are the strict content checker. Given a teaching (its original text and the ontology's paraphrase)
and a draft post, answer: does the post represent the teaching faithfully (no added doctrine, no reversed sense)? Does
it make any health, cure, diagnosis, prediction or astrology claim, or cite modern research? Is the idea specific: does
it name a concrete scene AND this teaching's own point, with a link that is the teaching's point rather than a stretch?
Be strict: when unsure, fail. Return JSON only."""
CHECK_SCHEMA = {"type": "object", "properties": {"faithful": {"type": "boolean"}, "claims": {"type": "array", "items": {"type": "string"}},
                "idea_specific": {"type": "boolean"}, "stretch": {"type": "boolean"}, "reason": {"type": "string"}},
                "required": ["faithful", "claims", "idea_specific", "stretch", "reason"], "additionalProperties": False}


def model_draft(client: ModelClient, ledger: Ledger, bucket_id: str, fmt: str, scene_idx: int, item: dict) -> dict:
    b = buckets()[bucket_id]
    c = ontology.citation(item["tid"])
    lim = _limits(fmt)
    user = json.dumps({"format": fmt, "limits": lim, "format_spec": formats().get(fmt, {}),
                       "voice_guide": voice(bucket_id), "tone_guide": (config.RULES / "tone.md").read_text(encoding="utf-8"),
                       "scene": b["scenes"][scene_idx], "teaching": {"source_line": source_line(item["tid"]),
                       "point": item["point"], "angle": item.get("angle", ""), "paraphrase": c["paraphrase"],
                       "original": (c.get("original") or "")[:600]}}, ensure_ascii=False)
    out = client.call_json("content_draft", DRAFT_SYSTEM, user, DRAFT_SCHEMA, ledger).data
    return {"bucket": bucket_id, "format": fmt, "scene_idx": scene_idx, "tid": item["tid"], "source": source_line(item["tid"]),
            "parts": [p for p in out.get("parts") or [] if isinstance(p, str) and p.strip()], "caption": out.get("caption", ""),
            "engine": "model", "ai_label": _ai_label(fmt)}


# --- checks --------------------------------------------------------------------------------------
def shingles(text: str, n: int = 5) -> set:
    t = re.sub(r"\s+", " ", (text or "").lower()).strip()
    return {t[i:i + n] for i in range(max(0, len(t) - n + 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def post_text(body: dict) -> str:
    return "\n".join(body.get("parts") or []) + ("\n" + body["caption"] if body.get("caption") else "")


def rules_check(store, body: dict) -> dict:
    fmt, lim, text = body["format"], _limits(body["format"]), post_text(body)
    problems = []
    lo, hi = lim.get("parts", [1, 99])
    if not (lo <= len(body.get("parts") or []) <= hi):
        problems.append(f"parts {len(body.get('parts') or [])} not in {lo}–{hi}")
    if lim.get("max_chars_per_part") and any(len(p) > lim["max_chars_per_part"] for p in body["parts"]):
        problems.append("a part is over the character limit")
    if lim.get("max_words_per_part") and any(len(p.split()) > lim["max_words_per_part"] for p in body["parts"]):
        problems.append("a slide is over the word limit")
    if lim.get("caption_max_words") and len((body.get("caption") or "").split()) > lim["caption_max_words"]:
        problems.append("caption over the word limit")
    if lim.get("total_words"):
        w = len(re.sub(r"\[on screen:[^\]]*\]", "", " ".join(body["parts"])).split())
        if not (lim["total_words"][0] <= w <= lim["total_words"][1]):
            problems.append(f"script is {w} words, outside {lim['total_words']}")
    if not ontology.citable(body["tid"]):
        problems.append("teaching not citable")
    if body["source"] not in text:
        problems.append("source line missing")
    hits = claims.scan(text)
    if hits:
        problems.append(f"forbidden claim: {hits[0]['match']!r}")
    if PERSONAL_DATA.search(text):
        problems.append("personal data or link")
    sh = shingles(text)
    worst = 0.0
    for p in store.list_posts():
        if p["status"] == "rejected":
            continue
        worst = max(worst, jaccard(sh, shingles(post_text(p["body"]))))
    if worst >= 0.5:
        problems.append(f"near-duplicate (5-gram Jaccard {worst:.2f})")
    return {"passed": not problems, "problems": problems, "max_similarity": round(worst, 3)}


def model_check(client: ModelClient, ledger: Ledger, body: dict) -> dict:
    c = ontology.citation(body["tid"])
    user = json.dumps({"teaching": {"source_line": body["source"], "original": (c.get("original") or "")[:800],
                                    "paraphrase": c["paraphrase"]}, "post": post_text(body)}, ensure_ascii=False)
    out = client.call_json("content_check", CHECK_SYSTEM, user, CHECK_SCHEMA, ledger).data
    ok = bool(out.get("faithful")) and not out.get("claims") and bool(out.get("idea_specific")) and not out.get("stretch")
    return {"passed": ok, **out}


# --- batch ---------------------------------------------------------------------------------------
def draft_batch(store, bucket_id: str, fmt: str, n: int = 1, engine: Optional[str] = None,
                client: Optional[ModelClient] = None) -> dict:
    if bucket_id not in buckets():
        raise ValueError(f"unknown bucket {bucket_id}")
    engine = engine or config.engine_mode()
    if engine == "model":
        client = client or ModelClient()
        if not client.available():
            engine = "rules"
    ledger = Ledger()
    queued, failed = [], []
    attempts = 0
    while len(queued) < n and attempts < n * 3:
        attempts += 1
        picked = pick(store, bucket_id, fmt, seed=attempts)
        if not picked:
            failed.append({"reason": "no unused (scene, teaching) pair left in the pool for 30 days"})
            break
        s, it = picked
        try:
            body = model_draft(client, ledger, bucket_id, fmt, s, it) if engine == "model" else rules_draft(bucket_id, fmt, s, it)
        except LLMError as e:
            failed.append({"tid": it["tid"], "reason": f"draft step failed ({e.kind})"})
            body = rules_draft(bucket_id, fmt, s, it)
        chk = {"rules": rules_check(store, body)}
        if engine == "model" and chk["rules"]["passed"]:
            try:
                chk["model"] = model_check(client, ledger, body)
            except LLMError as e:
                chk["model"] = {"passed": False, "reason": f"check step failed ({e.kind})"}
        passed = chk["rules"]["passed"] and chk.get("model", {"passed": True})["passed"]
        chk["passed"] = passed
        chk["engine"] = engine
        if passed:
            pid = store.add_post(bucket_id, bucket_id, fmt, body, chk, status="pending")
            queued.append(pid)
        else:
            failed.append({"tid": it["tid"], "scene_idx": s, "problems": chk["rules"].get("problems") or [chk.get("model", {}).get("reason")]})
    tot = ledger.totals()
    if tot.get("calls"):
        store.add_cost("content", f"{bucket_id}:{fmt}", tot)
    return {"queued": queued, "failed": failed, "engine": engine, "cost": tot}


def calendar(store, bucket_id: str, days: int = 30) -> list[dict]:
    """A 30-day plan drawn from this account's approved/edited and pending posts. A plan only: the app posts nothing."""
    posts = [p for p in store.list_posts() if p["bucket"] == bucket_id and p["status"] in ("approved", "edited", "pending")]
    posts.sort(key=lambda p: ({"approved": 0, "edited": 0, "pending": 1}[p["status"]], p["created"]))
    by_fmt: dict = {}
    for p in posts:
        by_fmt.setdefault(p["format"], []).append(p)
    rotation = ["x_post", "ig_carousel", "x_thread", "short_video", "x_post", "ig_carousel", "long_video"]
    plan, used = [], set()
    for d in range(1, days + 1):
        want = rotation[(d - 1) % len(rotation)]
        cand = [p for p in by_fmt.get(want, []) if p["id"] not in used] or [p for p in posts if p["id"] not in used]
        if cand:
            p = cand[0]
            used.add(p["id"])
            plan.append({"day": d, "format": p["format"], "post_id": p["id"], "status": p["status"],
                         "source": p["body"].get("source"), "first_line": (p["body"].get("parts") or [""])[0][:120]})
        else:
            plan.append({"day": d, "format": want, "post_id": None, "status": "to draft"})
    return plan
