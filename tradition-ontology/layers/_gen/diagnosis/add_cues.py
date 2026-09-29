#!/usr/bin/env python3
"""Apply cues_new.NEW to layers/diagnosis.json (idempotent). Run after build.py, which rewrites the file without them.

    python3 layers/_gen/diagnosis/add_cues.py

For every (entry, marker) in NEW: the marker must be found by the start of its text, and must be a user-facing marker
of a mappable, non-denylisted entry (the mapper's own catalog decides); otherwise it is skipped and reported. Earlier
additions are stripped first, then each new cue is appended to "cues" and listed in "cues_added" (same strings), unless
it is already a cue of that marker or is listed in cues_removed.json (removed by cue_check.py: too generic on the bland
baseline). Original cues listed in cues_removed.json are removed from "cues" too. Nothing else in the file changes.
"""
import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from insight import mapper, ontology  # noqa: E402
from cues_new import NEW  # noqa: E402

DIAG = ROOT / "layers" / "diagnosis.json"
REMOVED = HERE / "cues_removed.json"


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")


def main() -> int:
    text_before = DIAG.read_text(encoding="utf-8")
    raw = json.loads(text_before)
    by_id = {e["id"]: e for e in raw}
    removed = json.loads(REMOVED.read_text(encoding="utf-8")) if REMOVED.exists() else []
    gone = {(r["id"], r["marker"], r["cue"]) for r in removed}

    # the user-facing layer and the mapper's own catalog decide which markers can be matched at all
    usable = {}
    for e in raw:
        c = ontology._clean_entry(json.loads(json.dumps(e)))
        if c and c.get("definitions"):
            usable[c["id"]] = c
    cat = mapper.build_catalog(usable)
    live = {(eid, mk.text) for eid in cat.mappable for mk in cat.markers[eid]}

    # 1. strip earlier additions (idempotent re-run)
    for e in raw:
        for m in e.get("markers") or []:
            add = set(m.pop("cues_added", None) or [])
            m["cues"] = [c for c in m.get("cues") or [] if c not in add]

    # 2. remove original cues that cue_check.py found generic
    orig_removed = []
    for e in raw:
        for m in e.get("markers") or []:
            for c in list(m["cues"]):
                if (e["id"], m["marker"], c) in gone:
                    m["cues"].remove(c)
                    orig_removed.append(f"{e['id']} | {c}")

    # 3. add
    errors, skipped, n_added, n_markers = [], [], 0, 0
    for eid, specs in NEW.items():
        e = by_id.get(eid)
        if e is None:
            errors.append(f"{eid}: entry not in diagnosis.json")
            continue
        for prefix, cues in specs:
            idx = [i for i, m in enumerate(e["markers"]) if nfc(m["marker"]).startswith(nfc(prefix))]
            if len(idx) != 1:
                errors.append(f"{eid}: marker prefix {prefix!r} matches {len(idx)} markers")
                continue
            m = e["markers"][idx[0]]
            if (eid, m["marker"]) not in live:
                skipped.append(f"{eid} | {m['marker'][:60]} (not a user-facing mappable marker now)")
                continue
            if len(set(cues)) != len(cues):
                errors.append(f"{eid}: duplicate new cues under {prefix!r}")
            add = [c for c in dict.fromkeys(cues) if c not in m["cues"] and (eid, m["marker"], c) not in gone]
            if not add:
                continue
            new_m = {"marker": m["marker"], "cues": m["cues"] + add, "cues_added": add}
            for k, v in m.items():
                if k not in new_m:
                    new_m[k] = v
            e["markers"][idx[0]] = new_m
            n_added += len(add)
            n_markers += 1

    if errors:
        for x in errors:
            print("ERR", x)
        return 1
    out = json.dumps(raw, ensure_ascii=False, indent=1) + "\n"
    # re-validate: same entries, same fields except cues / cues_added, cues_added a sub-list of cues
    back = json.loads(out)
    before = json.loads(text_before)
    assert [e["id"] for e in back] == [e["id"] for e in before]
    for a, b in zip(back, before):
        assert {k: v for k, v in a.items() if k != "markers"} == {k: v for k, v in b.items() if k != "markers"}
        assert len(a["markers"]) == len(b["markers"])
        for ma, mb in zip(a["markers"], b["markers"]):
            assert ma["marker"] == mb["marker"] and ma["cites"] == mb["cites"]
            assert set(ma) - {"cues_added"} == set(mb) - {"cues_added"}
            assert all(c in ma["cues"] for c in ma.get("cues_added") or [])
            assert len(set(ma["cues"])) == len(ma["cues"])
    DIAG.write_text(out, encoding="utf-8")
    print(f"added {n_added} cues to {n_markers} markers; original cues removed as generic: {len(orig_removed)}")
    for x in orig_removed:
        print("  removed original:", x)
    for x in skipped:
        print("  skipped:", x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
