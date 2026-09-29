#!/usr/bin/env python3
"""Dev recall of the offline rules engine on tests/fixtures/dev_personas.jsonl (P6). Mechanical; no judgement.

    python3 layers/_gen/diagnosis/dev_recall.py              # after (layer as it is) and before (P6 cues stripped)
    python3 layers/_gen/diagnosis/dev_recall.py --detail     # also print, per target, the best evidence of the
                                                             # target entries that did not map

For each synthetic dev persona: map_person(inputs, safety.rule_screen(text), engine="rules") -> mapped entries and
confidence. A target pattern is "hit" when any entry listed for it in TARGETS maps. For target entries that did not map,
the script reports (by code) the floor reason and the best evidence per unit (match type, strength, caps, cue, quote),
aggregated exactly as mapper.aggregate does, before the cross-group overlap step.
The dev personas are development data written for this round; they are NOT evaluation data (eval/ is never read here).
Writes dev_recall_report.json next to this file.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from insight import mapper, safety  # noqa: E402
import cue_check as cc  # noqa: E402
from cues_new import NEW_P6  # noqa: E402

DEV = ROOT / "tests" / "fixtures" / "dev_personas.jsonl"
REPORT = HERE / "dev_recall_report.json"

# pattern label -> entries whose markers describe that pattern (any of them counts as a hit)
TARGETS = {
    "attachment": ["dx:klesa-raga", "dx:nivarana-kamacchanda", "dx:root-lobha", "dx:tanha", "dx:kasaya-lobha",
                   "dx:fetter-kamaraga", "dx:katha-outward-senses", "dx:guna-rajas", "dx:jain-arta-dhyana",
                   "dx:gita-anger-chain", "dx:antaraya-avirati"],
    "clinging/fear of loss": ["dx:root-lobha", "dx:fetter-kamaraga", "dx:kasaya-lobha", "dx:klesa-raga", "dx:tanha",
                              "dx:jain-arta-dhyana", "dx:jain-raudra-dhyana", "dx:guna-tamas"],
    "lasting anger/resentment": ["dx:kasaya-krodha", "dx:klesa-dvesa", "dx:root-dosa", "dx:fetter-patigha",
                                 "dx:nivarana-byapada", "dx:gita-kama-krodha", "dx:gita-anger-chain", "dx:carita-dosa",
                                 "dx:gita-asuri-sampad", "dx:jain-raudra-dhyana", "dx:vitarka-himsadi"],
    "restless/wandering mind": ["dx:gita-restless-mind", "dx:citta-vikkhitta", "dx:gk-viksepa",
                                "dx:nivarana-uddhacca-kukkucca", "dx:fetter-uddhacca", "dx:nivarana-kamacchanda",
                                "dx:katha-unrestrained-senses", "dx:mutthassati"],
    "regret/going over the past": ["dx:nivarana-uddhacca-kukkucca"],
    "doubt": ["dx:nivarana-vicikiccha", "dx:fetter-vicikiccha", "dx:antaraya-samsaya", "dx:gita-visada",
              "dx:carita-moha"],
    "pride/conceit": ["dx:kasaya-mana", "dx:fetter-mana", "dx:gita-asuri-sampad", "dx:katha-preyas", "dx:carita-raga",
                      "dx:carita-dosa", "dx:klesa-asmita"],
    "envy": ["dx:carita-dosa"],
    "concealment": ["dx:kasaya-maya", "dx:gita-asuri-sampad", "dx:carita-raga", "dx:guna-tamas"],
    "putting things off": ["dx:antaraya-pramada", "dx:antaraya-alasya", "dx:pamada", "dx:guna-tamas",
                           "dx:antaraya-styana", "dx:nivarana-thina-middha"],
    "dullness": ["dx:nivarana-thina-middha", "dx:gk-laya", "dx:antaraya-styana", "dx:antaraya-alasya",
                 "dx:guna-tamas"],
    "greed": ["dx:kasaya-lobha", "dx:root-lobha", "dx:guna-rajas", "dx:tanha", "dx:antaraya-avirati",
              "dx:gita-kama-krodha", "dx:katha-outward-senses", "dx:katha-preyas", "dx:carita-dosa"],
}
LEVELS = ["none", "low", "moderate", "high"]


def load_dev() -> list:
    return [json.loads(l) for l in DEV.read_text(encoding="utf-8").splitlines() if l.strip()]


def text_of(inputs: dict) -> str:
    parts = [v for v in (inputs.get("answers") or {}).values() if isinstance(v, str)]
    if (inputs.get("free_text") or "").strip():
        parts.append(inputs["free_text"])
    return " ".join(parts)


def p6_set() -> set:
    return {(eid, prefix, c) for eid, specs in NEW_P6.items() for prefix, cues in specs for c in cues}


def strip_p6(raw: list) -> list:
    """The layer without this round's cues (the 'before' state)."""
    p6 = p6_set()
    out = json.loads(json.dumps(raw))
    for e in out:
        for m in e.get("markers") or []:
            drop = {c for (eid, pre, c) in p6 if eid == e["id"] and mapper.normalise(m["marker"]).startswith(
                mapper.normalise(pre))}
            if drop:
                m["cues"] = [c for c in m.get("cues") or [] if c not in drop]
                if "cues_added" in m:
                    m["cues_added"] = [c for c in m["cues_added"] if c not in drop]
    return out


def diagnose(inputs: dict, scr, layer: dict, eids: list) -> dict:
    """Per target entry: floor code, E, E_net, units and the best item per unit (pre-overlap)."""
    R = mapper.Reading(inputs, scr, layer, None, None)
    if getattr(scr, "route", "continue") in safety.STOP_ROUTES:
        return {}
    mapper.rules_engine(R)
    out = {}
    for eid in eids:
        if eid not in R.cat.mappable:
            continue
        its = [i for i in R.items if i.eid == eid]
        cs = [c for c in R.counters if c.eid == eid]
        rej = collections.Counter(r["code"] for r in R.rejected if r["entry_id"] == eid)
        if not its and not cs and not rej:
            continue
        A = mapper.aggregate(eid, its, cs, R.cat.entries[eid])
        kept = []
        for it in A.kept:
            m = layer[eid]["markers"][it.marker_index]
            cue = m["cues"][it.cue_index] if it.cue_index is not None else None
            kept.append({"unit": it.unit, "match": it.match, "strength": it.strength, "caps": it.caps,
                         "spec": it.spec, "cue": cue, "quote": it.quote})
        out[eid] = {"code": A.code, "level": A.level, "E": round(A.E, 2), "E_net": round(A.E_net, 2),
                    "n_units": A.n_units, "n_direct_units": A.n_direct_units, "kept": kept,
                    "counters": [(c.reason, c.weight, c.quote) for c in cs], "rejected_codes": dict(rej)}
    return out


def run(layer: dict, people: list, detail: bool) -> dict:
    res = []
    for p in people:
        inp = p["inputs"]
        scr = safety.rule_screen(text_of(inp))
        out = mapper.map_person(inp, scr, engine="rules", layer=layer)
        maps = [(m["dx_id"], m["confidence"]) for m in out["mappings"]]
        per_target = {}
        for t in p["target"]:
            hits = [(e, c) for e, c in maps if e in TARGETS[t]]
            best = max((c for _, c in hits), key=LEVELS.index, default="none")
            per_target[t] = {"hit": bool(hits), "best": best, "entries": hits}
        rec = {"id": p["id"], "route": scr.route, "unmapped_reason": out["audit"]["unmapped_reason"],
               "mappings": maps, "targets": per_target,
               "off_target": [(e, c) for e, c in maps if not any(e in TARGETS[t] for t in p["target"])]}
        if detail:
            eids = sorted({e for t in p["target"] for e in TARGETS[t]})
            rec["target_evidence"] = diagnose(inp, scr, layer, eids)
        res.append(rec)
    n_t = sum(len(r["targets"]) for r in res)
    summary = {
        "personas": len(res),
        "personas_with_any_mapping": sum(1 for r in res if r["mappings"]),
        "personas_with_target_hit": sum(1 for r in res if any(v["hit"] for v in r["targets"].values())),
        "targets_hit": f"{sum(1 for r in res for v in r['targets'].values() if v['hit'])}/{n_t}",
        "target_confidence": dict(collections.Counter(v["best"] for r in res for v in r["targets"].values())),
        "mapping_confidence": dict(collections.Counter(c for r in res for _, c in r["mappings"])),
        "off_target_mappings": sum(len(r["off_target"]) for r in res),
        "by_pattern": {},
    }
    for t in TARGETS:
        vs = [r["targets"][t] for r in res if t in r["targets"]]
        summary["by_pattern"][t] = f"{sum(1 for v in vs if v['hit'])}/{len(vs)}"
    return {"summary": summary, "personas": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()
    people = load_dev()
    raw = cc.load_raw()
    after = run(cc.usable_layer(raw), people, args.detail)
    before = run(cc.usable_layer(strip_p6(raw)), people, False)
    rep = {"p6_cues": len(p6_set()), "before": before["summary"], "after": after["summary"],
           "personas_after": after["personas"],
           "personas_before": [{k: r[k] for k in ("id", "mappings", "targets")} for r in before["personas"]]}
    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("P6 cues:", rep["p6_cues"])
    for k in ("before", "after"):
        s = rep[k]
        print(k.upper(), json.dumps({x: s[x] for x in s if x != "by_pattern"}, ensure_ascii=False))
        print("   by pattern:", json.dumps(s["by_pattern"], ensure_ascii=False))
    for r, b in zip(after["personas"], before["personas"]):
        tg = "; ".join(f"{t}:{v['best']}" for t, v in r["targets"].items())
        print(f"{r['id']} [{r['route']}] {tg} | maps {r['mappings']} | before {b['mappings']}")
        if args.detail:
            for t, v in r["targets"].items():
                if v["hit"]:
                    continue
                ev = r.get("target_evidence", {})
                cands = [(e, d) for e, d in ev.items() if e in TARGETS[t]]
                cands.sort(key=lambda x: -x[1]["E_net"])
                if not cands:
                    print(f"    - {t}: no target entry has any evidence item")
                for e, d in cands[:3]:
                    print(f"    - {t}: {e} {d['code']} E={d['E']} Enet={d['E_net']} units={d['n_units']} "
                          f"direct={d['n_direct_units']} rej={d['rejected_codes']}")
                    for k in d["kept"]:
                        print(f"        {k['unit']} {k['match']}/{k['strength']} caps={k['caps']} spec={k['spec']} "
                              f"cue={k['cue']!r} q={k['quote'][:90]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
