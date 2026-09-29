#!/usr/bin/env python3
"""Run the evaluation sets through the product and prepare the judge packets.

  python3 scripts/run_eval.py --engine rules [--sets personas,safety,adversarial] [--content]

- Sets: eval/personas.jsonl (30 synthetic personas), eval/safety.jsonl (12), eval/adversarial.jsonl (10). They are
  written by the evaluation analyst only; builders never read them.
- Every case runs through insight.service.Service (consent, safety first, reading) with a throw-away encrypted store,
  so no synthetic text is kept outside eval/results/.
- Writes eval/results/<engine>/<set>/<id>.json|.md, eval/results/<engine>/summary.json (automated gate checks) and
  eval/judge/<engine>/*.jsonl (packets for the judge: citation sample 30%, swap pairs, claims and injection review,
  content review). Live-model gates are 'not run' when the engine is rules or no API key is set.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from insight import config, gates, ontology  # noqa: E402
from insight.service import Service  # noqa: E402
from insight.store import Store  # noqa: E402

EVAL = ROOT / "eval"


def load(name: str) -> list[dict]:
    p = EVAL / f"{name}.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def insights_of(rep: dict) -> list[dict]:
    out = []
    for m in rep.get("mappings") or []:
        out.append({"where": f"mapping {m['dx_id']}", "text": m.get("why", ""), "cites": m.get("cites", [])})
    for k, lens in (rep.get("lenses") or {}).items():
        for p in lens.get("points") or []:
            out.append({"where": f"lens {k}", "text": p["text"], "cites": p.get("cites", [])})
    rec = rep.get("reconciliation") or {}
    for p in rec.get("points") or []:
        out.append({"where": f"reconciliation ({p.get('basis')})", "text": p["text"], "cites": p.get("cites", [])})
    for p in rec.get("differences") or []:
        out.append({"where": "difference", "text": p["text"], "cites": p.get("cites", [])})
    for p in (rep.get("pathway") or {}).get("practices") or []:
        out.append({"where": f"pathway {p['px_id']}", "text": p.get("why", ""), "cites": p.get("cites", [])})
    return out


def run_case(svc: Service, case: dict, engine: str) -> tuple[dict, str]:
    inputs = case["inputs"]
    start = svc.start(inputs.get("age", 30), True)
    if "declined" in start:
        rep = {"engine": engine, "created": time.time(), "safety": {"route": "decline_minor"}, "stopped": start["declined"]}
        from insight.report import to_markdown
        return rep, to_markdown(rep)
    out = svc.reading(start["person_id"], inputs, engine=engine)
    return out["report"], out["markdown"]


def check_case(rep: dict, md: str, case: dict) -> dict:
    exp = case.get("expected") or {}
    r = {
        "route": gates.route(rep, exp.get("route")),
        "evidence": gates.evidence(rep, case["inputs"]),
        "claims": gates.forbidden_claims(rep, md),
        "practice_safety": gates.practice_safety(rep),
        "two_lenses": gates.two_lenses(rep),
        "schema": gates.schema(rep) if not rep.get("stopped") else [],
        "citations_resolve": gates.citations_resolve(rep),
        "must_show": gates.must_show(md, exp.get("must_show")),
        "must_not": gates.must_not(md, exp.get("must_not")),
    }
    return {k: v for k, v in r.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="rules", choices=["rules", "model"])
    ap.add_argument("--sets", default="personas,safety,adversarial")
    ap.add_argument("--content", action="store_true", help="export the review queue for the content gates")
    ap.add_argument("--queue-dir", help="ONTO_DATA_DIR of the queue to export (default: the configured data dir)")
    ap.add_argument("--seed", default="20260929")
    a = ap.parse_args()
    os.environ["ONTO_ENGINE"] = a.engine        # an evaluation run is an explicit operator choice of engine (config.reading_engine)
    if a.engine == "model" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("model engine needs ANTHROPIC_API_KEY: live gates are NOT RUN", file=sys.stderr)
        return 3
    res_dir = EVAL / "results" / a.engine
    judge_dir = EVAL / "judge" / a.engine
    res_dir.mkdir(parents=True, exist_ok=True)
    judge_dir.mkdir(parents=True, exist_ok=True)
    summary = {"engine": a.engine, "ontology_snapshot": {"diagnosis_usable": len(ontology.diagnosis()),
               "practices_usable": len(ontology.practices()), "gentle": len(ontology.gentle_practices())},
               "sets": {}, "run_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    reports = {}
    with tempfile.TemporaryDirectory() as td:
        os.environ["ONTO_DATA_DIR"] = td          # throw-away key and database for synthetic cases
        os.environ.pop("ONTO_DATA_KEY", None)
        svc = Service(store=Store(Path(td) / "eval.sqlite3"))
        for name in [s for s in a.sets.split(",") if s]:
            cases = load(name)
            out_dir = res_dir / name
            out_dir.mkdir(parents=True, exist_ok=True)
            rows = []
            for c in cases:
                t0 = time.time()
                try:
                    rep, md = run_case(svc, c, a.engine)
                    err = None
                except Exception as e:   # noqa: BLE001 — record, never stop the run
                    rep, md, err = {}, "", f"{type(e).__name__}: {e}"
                (out_dir / f"{c['id']}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
                (out_dir / f"{c['id']}.md").write_text(md, encoding="utf-8")
                chk = check_case(rep, md, c) if not err else {"error": [err]}
                rows.append({"id": c["id"], "route": (rep.get("safety") or {}).get("route"),
                             "status": "stopped" if rep.get("stopped") else ("insufficient" if rep.get("insufficient") else ("ok" if rep else "error")),
                             "n_mappings": len(rep.get("mappings") or []), "n_practices": len((rep.get("pathway") or {}).get("practices") or []),
                             "seconds": round(time.time() - t0, 2), "failures": {k: v for k, v in chk.items() if v}})
                reports[(name, c["id"])] = (c, rep, md)
            summary["sets"][name] = {"n": len(cases), "cases": rows,
                                     "failing": [r["id"] for r in rows if r["failures"]]}
    rng = random.Random(a.seed)
    # judge packet 1: citation integrity — 30% of (statement, cite) pairs from the persona reports
    pairs = []
    for (name, cid), (c, rep, md) in reports.items():
        if name != "personas":
            continue
        for ins in insights_of(rep):
            for t in ins["cites"]:
                if ontology.citable(t):
                    pairs.append({"case": cid, "where": ins["where"], "statement": ins["text"], "cite": ontology.citation(t)})
    k = -(-len(pairs) * 3 // 10) if pairs else 0
    sample = rng.sample(pairs, k) if k else []
    ran = {n for n, _ in reports}
    if "personas" in ran:      # never overwrite a packet for a set that was not run
        (judge_dir / "citation_sample.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in sample), encoding="utf-8")
    # judge packet 2: swap test — each persona's insights against the next persona's own words
    per = [(cid, c, rep) for (name, cid), (c, rep, md) in reports.items() if name == "personas" and rep.get("mappings")]
    swaps = []
    for i, (cid, c, rep) in enumerate(per):
        if len(per) < 2:
            break
        ocid, oc, _ = per[(i + 1) % len(per)]
        swaps.append({"report_of": cid, "other_person": ocid,
                      "other_words": "\n".join(gates.own_words(oc["inputs"])),
                      "insights": [{"where": x["where"], "text": x["text"]} for x in insights_of(rep)],
                      "quote_overlap": __import__("insight.specificity", fromlist=["x"]).swap_overlap(rep, "\n".join(gates.own_words(oc["inputs"])))})
    if "personas" in ran:
        (judge_dir / "swap_pairs.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in swaps), encoding="utf-8")
    # judge packet 3: safety + adversarial review (whole rendered outputs)
    rev = [{"set": n, "case": cid, "expected": c.get("expected"), "attack": c.get("attack"), "markdown": md}
           for (n, cid), (c, rep, md) in reports.items() if n in ("safety", "adversarial")]
    if ran & {"safety", "adversarial"}:
        (judge_dir / "safety_adversarial_review.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rev), encoding="utf-8")
    # judge packet 4: claims review — every persona report, rendered
    cl = [{"case": cid, "markdown": md} for (n, cid), (c, rep, md) in reports.items() if n == "personas"]
    if "personas" in ran:
        (judge_dir / "claims_review.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in cl), encoding="utf-8")
    if a.content:
        store = Store(Path(a.queue_dir) / "insight.sqlite3") if a.queue_dir else Store()
        from insight import content
        posts = [p for p in store.list_posts() if p["status"] != "rejected"]   # rejected drafts are not part of the queue
        sims = []
        for i, p in enumerate(posts):
            best = 0.0
            for q in posts[:i] + posts[i + 1:]:
                best = max(best, content.jaccard(content.shingles(content.post_text(p["body"])), content.shingles(content.post_text(q["body"]))))
            sims.append(best)
        rows = [{"post_id": p["id"], "bucket": p["bucket"], "format": p["format"], "status": p["status"],
                 "text": content.post_text(p["body"]), "cite": ontology.citation(p["body"]["tid"]) if ontology.citable(p["body"]["tid"]) else None,
                 "claim_hits": [h["match"] for h in __import__("insight.claims", fromlist=["x"]).scan(content.post_text(p["body"]))],
                 "max_similarity": round(s, 3)} for p, s in zip(posts, sims)]
        (judge_dir / "content_review.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows), encoding="utf-8")
        summary["content"] = {"n": len(rows), "claim_hits": sum(1 for r in rows if r["claim_hits"]),
                              "near_duplicates": sum(1 for r in rows if r["max_similarity"] >= 0.5),
                              "uncitable": sum(1 for r in rows if not r["cite"])}
    summary["judge_packets"] = {"citation_sample": len(sample), "citation_pairs_total": len(pairs), "swap_pairs": len(swaps),
                                "safety_adversarial": len(rev), "claims_review": len(cl)}
    prev_p = res_dir / "summary.json"
    if prev_p.exists():          # keep the results of sets (or content) not run this time
        prev = json.loads(prev_p.read_text(encoding="utf-8"))
        summary["sets"] = {**prev.get("sets", {}), **summary["sets"]}
        if "content" not in summary and "content" in prev:
            summary["content"] = prev["content"]
        pk = dict(prev.get("judge_packets") or {})
        for k, v in (summary.get("judge_packets") or {}).items():
            if k in ("safety_adversarial",) and not (ran & {"safety", "adversarial"}):
                continue
            if k != "safety_adversarial" and "personas" not in ran:
                continue
            pk[k] = v
        summary["judge_packets"] = pk
    prev_p.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: (v if k != "sets" else {n: {"n": s["n"], "failing": s["failing"]} for n, s in v.items()})
                      for k, v in summary.items()}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
