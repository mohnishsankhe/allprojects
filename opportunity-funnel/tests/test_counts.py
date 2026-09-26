import json

import common
import counts
import records
from conftest import Helpers

ROOM = "gre-engineers-india"


def _ids(run, n, round=1, start=1):
    """Store n ordered records for `round`; returns their ids in collection order."""
    recs = [Helpers.make_record(f"https://a.test/r{round}/{i}", f"record {i} of round {round} some words", round=round, qi=1, rank=i)
            for i in range(start, start + n)]
    out = records.store_records(run, ROOM, "websearch", recs)
    return out["new_ids"]


def _setup(run, h, labels, keys=("fees", "quant"), n=None, batches=True):
    ids = _ids(run, n if n is not None else len(labels))
    if batches:
        records.make_batches(run, ROOM)
    h.write_taxonomy(run, ROOM, keys)
    rows = [labels[i](ids[i]) if callable(labels[i]) else h.label(ids[i], **labels[i]) for i in range(len(labels))]
    h.write_labels(run, ROOM, "batch_r1_001", rows)
    return ids


def test_count_voice_aware_totals(run, h):
    ids = _setup(run, h, [
        {"voice": "member", "keys": ["fees"], "money": True, "failed": True},
        {"voice": "member", "keys": ["fees", "quant"], "money": True},
        {"voice": "member", "keys": ["quant"]},
        {"voice": "member", "keys": [], "failed": True, "money": False},
        {"voice": "seller", "keys": ["fees"], "money": True},
        {"voice": "media", "keys": ["quant"]},
        {"voice": "other", "keys": []},
    ])
    c = counts.compute_counts(run, ROOM)
    fees, quant = c["pains"]["fees"], c["pains"]["quant"]
    assert fees["record_count"] == 2 and fees["member_record_ids"] == sorted([ids[0], ids[1]])
    assert fees["money_mentions"] == 2 and fees["failed_spend_mentions"] == 1 and fees["failed_spend_record_ids"] == [ids[0]]
    assert fees["seller_records"] == 1 and fees["seller_record_ids"] == [ids[4]] and fees["media_records"] == 0
    assert quant["record_count"] == 2 and quant["money_mentions"] == 1 and quant["media_records"] == 1
    t = c["totals"]
    assert t["by_voice"] == {"member": 4, "seller": 1, "media": 1, "other": 1}
    assert t["by_source"] == {"websearch": 7}
    assert t["member_records"] == 4 and t["member_records_with_pain"] == 3
    assert t["money_mentions"] == 3 and t["failed_spend_mentions"] == 2  # failed spend forced money on record 4
    assert c["notes"] == [f"{ids[3]}: failed_spend is true, so money was set to true."]
    out = common.room_dir(run, ROOM) / "counts.json"
    assert not out.exists()


def test_count_cli_writes_json_and_lists_every_error(run, h, cli):
    ids = _setup(run, h, [{"keys": ["fees"]}, {"keys": ["quant"]}, {"keys": []}], n=4)
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 1 and "have no label" in r.stderr and ids[3] in r.stderr
    bad = [
        h.label(ids[0], keys=["fees"]),
        h.label(ids[0], keys=["quant"]),  # conflicting duplicate
        h.label(ids[1], voice="buyer", keys=["nope", "fees", "quant"], money="yes", failed=None, reasoning="", confidence="maybe"),
        h.label("0000000000000000", keys=["fees"]),
        {"record_id": ids[2], "voice": "member", "pain_keys": "fees", "money": False, "failed_spend": False,
         "reasoning": "r", "confidence": "low"},
        h.label(ids[3], keys=[]),
    ]
    h.write_labels(run, ROOM, "batch_r1_001", bad)
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 1, r.stdout
    err = r.stderr
    for needle in ("conflicts with an earlier label", "'voice' must be member, seller, media or other",
                   "unknown pain key 'nope'", "more than 2 pain keys", "'money' must be true or false",
                   "'failed_spend' must be true or false", "missing 'reasoning'", "'confidence' must be high, moderate or low",
                   "unknown record_id '0000000000000000'", "'pain_keys' must be a list"):
        assert needle in err, needle
    lines = [ln for ln in err.splitlines() if not ln.startswith("warning:")]
    assert lines[0].startswith("Fix these:") and any(line.startswith("10. ") for line in lines)
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "error" and e["command"] == "count" for e in events)
    good = [h.label(ids[0], keys=["fees"], money=True), h.label(ids[1], keys=["quant"]), h.label(ids[2]), h.label(ids[3], voice="seller", keys=["fees"])]
    h.write_labels(run, ROOM, "batch_r1_001", good)
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "4 labeled records (member 3, seller 1, media 0, other 0)" in r.stdout
    data = json.loads((common.room_dir(run, ROOM) / "counts.json").read_text(encoding="utf-8"))
    assert data["pains"]["fees"]["seller_records"] == 1 and data["labeled"] == 4


def test_count_missing_inputs_exit_2(run, h, cli):
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 2 and "batches.json is missing" in r.stderr
    _ids(run, 2)
    records.make_batches(run, ROOM)
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 2 and "taxonomy.json is missing" in r.stderr
    h.write_taxonomy(run, ROOM, ["fees"])
    r = cli("count", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 2 and "No label files" in r.stderr


def test_competition_rank():
    ranks = counts.competition_rank({"a": (2, 5, 9), "b": (2, 5, 9), "c": (1, 9, 9), "d": (0, 0, 1)})
    assert ranks == {"a": 1, "b": 1, "c": 3, "d": 4}


# --------------------------------------------------------------------------- saturation
def _sat(run, froot, h, spec, window=4, extra_round=None):
    """spec: list of (keys, money, failed) per member record in collection order."""
    h.set_rule(froot, "stage3", "saturation_window", window)
    ids = _ids(run, len(spec))
    if extra_round:
        ids += _ids(run, len(extra_round), round=2)
        spec = list(spec) + list(extra_round)
    m = records.make_batches(run, ROOM)
    h.write_taxonomy(run, ROOM, ["a", "b", "c"])
    by_batch = {}
    for name, bids in m["batches"].items():
        for rid in bids:
            by_batch.setdefault(name, []).append(rid)
    pos = {rid: i for i, rid in enumerate(ids)}
    for name, bids in by_batch.items():
        rows = [h.label(rid, keys=spec[pos[rid]][0], money=spec[pos[rid]][1], failed=spec[pos[rid]][2]) for rid in bids]
        h.write_labels(run, ROOM, name, rows)
    return ids


def _sat_file(run):
    return common.read_json(common.room_dir(run, ROOM) / "saturation.json")


def test_saturation_not_evaluable_below_window_plus_one(run, froot, h, cli):
    _sat(run, froot, h, [(["a"], False, False)] * 4, window=4)
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Not evaluable yet: need at least 5" in r.stdout and "Saturated: no" in r.stdout
    e = _sat_file(run)["rounds"][0]
    assert e["evaluable"] is False and e["saturated"] is False and e["records"] == 4 and e["new_records"] == 4


def test_saturation_new_pain_in_last_window(run, froot, h, cli):
    spec = [(["a"], False, False)] * 4 + [(["a"], False, False), (["b"], False, False), (["a"], False, False), ([], False, False)]
    _sat(run, froot, h, spec, window=4)
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    e = _sat_file(run)["rounds"][0]
    assert e["evaluable"] and e["new_pains"] == ["b"] and e["rank_changes"] == [] and e["saturated"] is False
    assert "New pains in the last 4: b" in r.stdout


def test_saturation_rank_change(run, froot, h, cli):
    # before the window: a has 3 member records, b has 1 -> a ranks 1. The last 4 give b failed spend -> b ranks 1.
    spec = [(["a"], False, False), (["a"], False, False), (["a"], False, False), (["b"], False, False),
            (["b"], True, True), (["b"], True, False), (["a"], False, False), (["b"], False, False)]
    _sat(run, froot, h, spec, window=4)
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    e = _sat_file(run)["rounds"][0]
    assert e["new_pains"] == [] and e["saturated"] is False
    assert e["rank_changes"] == [{"key": "a", "rank_before": 1, "rank_after": 2}, {"key": "b", "rank_before": 2, "rank_after": 1}]
    assert "Rank changes: a (1 -> 2); b (2 -> 1)" in r.stdout


def test_saturation_saturated_case(run, froot, h, cli):
    spec = [(["a"], True, False), (["b"], False, False), (["a"], False, False), (["b"], False, False),
            (["a"], False, False), (["b"], False, False), ([], True, True), (["a"], False, False)]
    _sat(run, froot, h, spec, window=4)
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    e = _sat_file(run)["rounds"][0]
    assert e["saturated"] is True and e["new_pains"] == [] and e["rank_changes"] == []
    assert "Saturated: yes" in r.stdout


def test_saturation_replaces_same_round_and_appends_new_rounds(run, froot, h, cli):
    spec = [(["a"], False, False)] * 5
    _sat(run, froot, h, spec, window=4)
    assert cli("saturation", "--room", ROOM, "--run", "2026-09-26").returncode == 0
    assert cli("saturation", "--room", ROOM, "--run", "2026-09-26").returncode == 0
    data = _sat_file(run)
    assert [e["round"] for e in data["rounds"]] == [1] and data["window"] == 4
    # round 2 adds 3 records; the saturation file keeps round 1 and adds round 2
    ids2 = _ids(run, 3, round=2)
    records.make_batches(run, ROOM)
    h.write_labels(run, ROOM, "batch_r2_001", [h.label(rid, keys=["a"]) for rid in ids2])
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = _sat_file(run)
    assert [e["round"] for e in data["rounds"]] == [1, 2]
    assert data["rounds"][1]["records"] == 8 and data["rounds"][1]["new_records"] == 3 and data["rounds"][1]["saturated"] is True
    assert "Round 2: 8 records (3 new)" in r.stdout


def test_saturation_final_guard(run, froot, h, cli):
    spec = [(["a"], False, False)] * 4 + [(["b"], False, False)] * 4
    _sat(run, froot, h, spec, window=4)
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26", "--final", "--stop-reason", "saturated")
    assert r.returncode == 1 and "needs the last round to be saturated" in r.stderr
    assert _sat_file(run)["stop_reason"] is None
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26", "--final")
    assert r.returncode == 1 and "--final and --stop-reason go together" in r.stderr
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26", "--final", "--stop-reason", "exhausted")
    assert r.returncode == 0, r.stderr
    data = _sat_file(run)
    assert data["stop_reason"] == "exhausted" and data["final"] is True
    assert "Stopped: exhausted" in r.stdout
    r = cli("saturation", "--room", ROOM, "--run", "2026-09-26", "--final", "--stop-reason", "nonsense")
    assert r.returncode == 2


def test_saturation_orders_by_meta_order_not_storage_order(run, froot, h):
    h.set_rule(froot, "stage3", "saturation_window", 2)
    # stored in reverse rank order; collection order must follow meta.order
    recs = [Helpers.make_record(f"https://a.test/{i}", f"record number {i} words here", rank=i) for i in (3, 2, 1)]
    ids = records.store_records(run, ROOM, "websearch", recs)["new_ids"]
    stored = records.records_by_id(run, ROOM)
    ordered = counts.order_records(ids, stored)
    assert [stored[r]["meta"]["order"][2] for r in ordered] == [1, 2, 3]
    labels = {ids[0]: h.label(ids[0], keys=["b"]), ids[1]: h.label(ids[1], keys=["a"]), ids[2]: h.label(ids[2], keys=["a"])}
    e = counts.saturation_entry(ordered, labels, 2, 1, 3)
    assert e["new_pains"] == ["b"]  # rank 3 (stored first) is in the last window
