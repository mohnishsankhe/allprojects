#!/usr/bin/env python3
"""P4: draft 10 posts per bucket into the review queue, then export the queue and a 30-day calendar per bucket.

  python3 scripts/build_content_queue.py [--engine rules|model] [--data-dir ~/.onto-insight-content]

The queue database lives outside the repository (ONTO_DATA_DIR). Posts hold no personal data, so the export is
committed: content/queue.jsonl (every post, its checks and status) and content/calendars/<bucket>.md.
Nothing is ever posted: publishing is a human step after review (RUNBOOK.md).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MIX = [("x_post", 3), ("x_thread", 2), ("ig_carousel", 2), ("short_video", 2), ("long_video", 1)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="rules", choices=["rules", "model"])
    ap.add_argument("--data-dir", default=str(Path.home() / ".onto-insight-content"))
    ap.add_argument("--fresh", action="store_true", help="start from an empty queue")
    a = ap.parse_args()
    os.environ["ONTO_DATA_DIR"] = a.data_dir
    from insight import content
    from insight.store import Store
    Path(a.data_dir).mkdir(parents=True, exist_ok=True, mode=0o700)
    db = Path(a.data_dir) / "insight.sqlite3"
    if a.fresh and db.exists():
        db.unlink()
    store = Store(db)
    summary = {}
    for b in content.buckets():
        have = [p for p in store.list_posts() if p["bucket"] == b]
        if len(have) >= 10:
            summary[b] = {"queued": 0, "existing": len(have), "failed": []}
            continue
        q, f = [], []
        for fmt, n in MIX:
            r = content.draft_batch(store, b, fmt, n=n, engine=a.engine)
            q += r["queued"]
            f += r["failed"]
        summary[b] = {"queued": len(q), "failed": f}
    out = ROOT / "content"
    (out / "calendars").mkdir(parents=True, exist_ok=True)
    posts = store.list_posts()
    with open(out / "queue.jsonl", "w", encoding="utf-8") as fh:
        for p in posts:
            fh.write(json.dumps({k: p[k] for k in ("id", "bucket", "format", "status", "body", "check", "created")},
                                ensure_ascii=False) + "\n")
    for b in content.buckets():
        plan = content.calendar(store, b, 30)
        L = [f"# 30-day plan: {content.buckets()[b]['name']}", "",
             "_A plan for the human editor. The app posts nothing. Each account publishes only its own posts; "
             "label AI-assisted media where the platform requires it._", "",
             "| Day | Format | Status | Source | First line |", "|---|---|---|---|---|"]
        for d in plan:
            L.append(f"| {d['day']} | {d['format']} | {d['status']} | {d.get('source') or ''} | "
                     f"{(d.get('first_line') or '').replace('|', '/')} |")
        (out / "calendars" / f"{b}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "total_posts": len(posts)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
