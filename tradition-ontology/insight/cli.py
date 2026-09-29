"""Command line that mirrors the web app. All actions go through insight/service.py.

  python -m insight.cli consent
  python -m insight.cli questions
  python -m insight.cli start --age 34 --consent
  python -m insight.cli read --person PID --answers answers.json [--free-text notes.txt] [--dialogue chat.txt --speaker Me]
                             [--engine rules|model] [--premium] [--out report.md] [--html report.html]
  python -m insight.cli report --person PID --reading RID [--format md|html|json]
  python -m insight.cli checkin --person PID [--reading RID] --day 3 --text "..."
  python -m insight.cli my-data --person PID          python -m insight.cli delete --person PID
  python -m insight.cli purge [--days 90]
  python -m insight.cli draft --bucket work --format x_post [--n 10] [--engine rules|model]
  python -m insight.cli posts [--status pending]       python -m insight.cli review --post ID --action approve|edit|reject [--note ..] [--body-file new.json]
  python -m insight.cli calendar --bucket work [--days 30]
  python -m insight.cli costs
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import config
from .service import Service, ServiceError, consent_info, intake_questions


def _read(path: str | None) -> str:
    if not path:
        return ""
    return sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")


def _print(obj) -> None:
    print(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2))


def main(argv=None) -> int:
    config.load_dotenv()
    ap = argparse.ArgumentParser(prog="insight", description="Ontology Insight Generator (CLI)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("consent")
    sub.add_parser("questions")
    s = sub.add_parser("start"); s.add_argument("--age", required=True); s.add_argument("--consent", action="store_true")
    r = sub.add_parser("read")
    r.add_argument("--person", required=True); r.add_argument("--answers"); r.add_argument("--free-text")
    r.add_argument("--dialogue"); r.add_argument("--speaker", default="")
    r.add_argument("--age"); r.add_argument("--engine", choices=["rules", "model"]); r.add_argument("--premium", action="store_true")
    r.add_argument("--out"); r.add_argument("--html")
    g = sub.add_parser("report"); g.add_argument("--person", required=True); g.add_argument("--reading", required=True)
    g.add_argument("--format", choices=["md", "html", "json"], default="md")
    c = sub.add_parser("checkin"); c.add_argument("--person", required=True); c.add_argument("--reading")
    c.add_argument("--day", type=int, required=True); c.add_argument("--text", required=True)
    c.add_argument("--engine", choices=["rules", "model"])
    m = sub.add_parser("my-data"); m.add_argument("--person", required=True)
    d = sub.add_parser("delete"); d.add_argument("--person", required=True)
    p = sub.add_parser("purge"); p.add_argument("--days", type=int)
    dr = sub.add_parser("draft"); dr.add_argument("--bucket", required=True); dr.add_argument("--format", dest="fmt", required=True)
    dr.add_argument("--n", type=int, default=1); dr.add_argument("--engine", choices=["rules", "model"])
    ps = sub.add_parser("posts"); ps.add_argument("--status")
    rv = sub.add_parser("review"); rv.add_argument("--post", required=True)
    rv.add_argument("--action", required=True, choices=["approve", "edit", "reject"]); rv.add_argument("--note", default="")
    rv.add_argument("--body-file")
    ca = sub.add_parser("calendar"); ca.add_argument("--bucket", required=True); ca.add_argument("--days", type=int, default=30)
    sub.add_parser("costs")
    a = ap.parse_args(argv)

    svc = Service()
    try:
        if a.cmd == "consent":
            ci = consent_info()
            _print("\n\n".join(ci["text"]) + f"\n\n[ ] {ci['checkbox']}  (version {ci['version']})")
        elif a.cmd == "questions":
            _print(intake_questions())
        elif a.cmd == "start":
            _print(svc.start(a.age, a.consent))
        elif a.cmd == "read":
            answers = json.loads(_read(a.answers)) if a.answers else {}
            inputs = {"answers": answers, "free_text": _read(a.free_text), "dialogue": _read(a.dialogue),
                      "dialogue_speaker": a.speaker}
            if a.age:
                inputs["age"] = a.age
            out = svc.reading(a.person, inputs, engine=a.engine, premium=a.premium)
            if a.out:
                Path(a.out).write_text(out["markdown"], encoding="utf-8")
            if a.html and out.get("reading_id"):
                Path(a.html).write_text(svc.get_report(a.person, out["reading_id"], "html"), encoding="utf-8")
            _print(f"reading_id: {out['reading_id']}\n\n{out['markdown']}")
        elif a.cmd == "report":
            _print(svc.get_report(a.person, a.reading, a.format))
        elif a.cmd == "checkin":
            _print(svc.checkin(a.person, a.reading, a.day, a.text, engine=a.engine))
        elif a.cmd == "my-data":
            _print(svc.my_data(a.person))
        elif a.cmd == "delete":
            _print(svc.delete_me(a.person))
        elif a.cmd == "purge":
            _print(svc.purge(a.days))
        elif a.cmd == "draft":
            from . import content
            _print(content.draft_batch(svc.store, a.bucket, a.fmt, n=a.n, engine=a.engine))
        elif a.cmd == "posts":
            _print(svc.posts(a.status))
        elif a.cmd == "review":
            body = json.loads(_read(a.body_file)) if a.body_file else None
            _print(svc.review(a.post, a.action, a.note, body))
        elif a.cmd == "calendar":
            from . import content
            _print(content.calendar(svc.store, a.bucket, a.days))
        elif a.cmd == "costs":
            _print(svc.costs())
    except ServiceError as e:
        print(f"error ({e.code}): {e.message}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
