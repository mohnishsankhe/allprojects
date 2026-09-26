import hashlib
import json

import pytest

import common
import records

ROOM = "gre-engineers-india"


def _batch_files(run, room):
    d = records.batches_dir(run, room)
    return {p.name: p.read_bytes() for p in sorted(d.glob("*.md"))}


def test_record_id_is_stable_and_whitespace_normalized():
    a = common.record_id("https://x.test/p", "GRE  coaching\n worth it?")
    b = common.record_id("https://x.test/p", "GRE coaching worth it?")
    assert a == b and len(a) == 16
    expected = hashlib.sha256("https://x.test/p\nGRE coaching worth it?".encode("utf-8")).hexdigest()[:16]
    assert a == expected
    assert common.record_id("https://x.test/other", "GRE coaching worth it?") != a


def test_store_anonymizes_before_storage_and_keeps_only_record_fields(run, h):
    rec = h.make_record("https://forum.test/t/1", "Call Rahul on +91 98765 43210 or mail x@y.com about GRE fees $1,200")
    rec["author"] = "rahul_s"
    rec["meta"]["author_name"] = "Rahul S"
    out = h.store(run, ROOM, [rec])
    assert out["new"] == 1 and out["duplicates"] == 0
    raw = (records.source_file(run, ROOM, "websearch")).read_text(encoding="utf-8")
    assert "98765" not in raw and "x@y.com" not in raw and "rahul_s" not in raw
    stored = json.loads(raw)
    assert set(stored) == set(records.RECORD_FIELDS)
    assert stored["text"] == "Call Rahul on [phone] or mail [email] about GRE fees $1,200"
    assert stored["record_id"] == common.record_id(stored["url"], stored["text"])
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "note" and "Anonymizer limit" in e["note"] for e in events)


def test_store_dedupes_by_record_id_across_calls_and_sources(run, h):
    rec = h.make_record("https://forum.test/t/1", "GRE coaching worth it?")
    assert h.store(run, ROOM, [rec, dict(rec)])["new"] == 1
    again = h.store(run, ROOM, [rec])
    assert again["new"] == 0 and again["duplicates"] == 1
    other = h.store(run, ROOM, [rec], source="inbox:customers")
    assert other["new"] == 0 and other["duplicates"] == 1
    assert len(records.load_records(run, ROOM)) == 1
    assert not records.source_file(run, ROOM, "inbox:customers").exists()
    assert records.source_file(run, ROOM, "inbox:customers").name == "inbox_customers.jsonl"


def test_store_rejects_bad_dates_and_slugs(run, h):
    with pytest.raises(common.ValidationErrors):
        h.store(run, ROOM, [h.make_record("https://a.test/1", "some text here", date="26/09/2024")])
    with pytest.raises(common.ValidationErrors):
        h.store(run, "../escape", [h.make_record("https://a.test/1", "some text here")])
    with pytest.raises(common.ValidationErrors):
        common.check_slug("a/b")


def test_batches_by_round_never_change_earlier_batches(run, h):
    r1 = [h.make_record(f"https://a.test/{i}", f"round one record number {i}", round=1, qi=1, rank=i) for i in range(1, 4)]
    h.store(run, ROOM, r1)
    m1 = records.make_batches(run, ROOM, size=2)
    assert sorted(m1["batches"]) == ["batch_r1_001", "batch_r1_002"]
    assert len(m1["batches"]["batch_r1_001"]) == 2 and len(m1["batches"]["batch_r1_002"]) == 1
    before = _batch_files(run, ROOM)
    r2 = [h.make_record(f"https://b.test/{i}", f"round two record number {i}", round=2, qi=5, rank=i) for i in range(1, 3)]
    h.store(run, ROOM, r2)
    m2 = records.make_batches(run, ROOM, size=2)
    assert sorted(m2["batches"]) == ["batch_r1_001", "batch_r1_002", "batch_r2_001"]
    after = _batch_files(run, ROOM)
    assert after["batch_r1_001.md"] == before["batch_r1_001.md"]
    assert after["batch_r1_002.md"] == before["batch_r1_002.md"]
    assert m2["rounds"]["2"]["records"] == 2
    # a different size removes stale batch files
    m3 = records.make_batches(run, ROOM, size=10)
    assert sorted(m3["batches"]) == ["batch_r1_001", "batch_r2_001"]
    assert sorted(_batch_files(run, ROOM)) == ["batch_r1_001.md", "batch_r2_001.md"]


def test_lookback_uses_run_date_and_url_dates(run, h, froot):
    recs = [
        h.make_record("https://a.test/2024/09/25/old", "just outside the window of two years", date="2024-09-25", rank=1),
        h.make_record("https://a.test/2024/09/26/edge", "exactly on the cutoff day stays", date="2024-09-26", rank=2),
        h.make_record("https://a.test/2026/01/01/new", "a fresh record inside the window", date="2026-01-01", rank=3),
        h.make_record("https://a.test/undated", "no date anywhere in this one", date=None, rank=4),
    ]
    h.store(run, ROOM, recs)
    m = records.make_batches(run, ROOM)
    f = m["filters"]
    assert f["lookback_cutoff"] == "2024-09-26" and f["lookback_months"] == 24
    assert f["loaded"] == 4 and f["dropped_old"] == 1 and f["undated_kept"] == 1 and f["kept"] == 3
    ids = m["batches"]["batch_r1_001"]
    assert common.record_id("https://a.test/2024/09/25/old", "just outside the window of two years") not in ids
    undated_id = common.record_id("https://a.test/undated", "no date anywhere in this one")
    assert undated_id in ids and m["undated_record_ids"] == [undated_id]
    text = h.read(records.batches_dir(run, ROOM) / "batch_r1_001.md")
    assert f"### {undated_id} | websearch | undated | a.test" in text
    assert "| 2026-01-01 | a.test" in text
    # the founder can switch undated records off
    h.set_rule(froot, "stage3", "include_undated_records", False)
    m2 = records.make_batches(run, ROOM)
    assert m2["filters"]["dropped_undated"] == 1 and m2["filters"]["kept"] == 2
    assert undated_id not in m2["batches"]["batch_r1_001"]


def test_dedupe_normalized_text_keeps_first_in_collection_order(run, h):
    first = h.make_record("https://a.test/1", "GRE coaching  worth it?", rank=2)
    second = h.make_record("https://b.test/2", "GRE coaching worth it?", rank=1)
    h.store(run, ROOM, [first, second])
    m = records.make_batches(run, ROOM)
    assert m["filters"]["dropped_duplicate_text"] == 1
    assert m["batches"]["batch_r1_001"] == [common.record_id("https://a.test/1", "GRE coaching  worth it?")]


def test_order_by_meta_order_then_newest_first(run, h):
    recs = [
        h.make_record("https://a.test/3", "third by order value", round=1, qi=2, rank=1),
        h.make_record("https://a.test/1", "first by order value", round=1, qi=1, rank=1),
        h.make_record("https://a.test/2", "second by order value", round=1, qi=1, rank=2),
    ]
    h.store(run, ROOM, recs)
    unordered = [
        {"url": "https://c.test/old", "text": "unordered older text here", "date": "2025-01-01", "meta": {"round": 1}},
        {"url": "https://c.test/new", "text": "unordered newer text here", "date": "2025-06-01", "meta": {"round": 1}},
        {"url": "https://c.test/none", "text": "unordered undated text here", "date": None, "meta": {"round": 1}},
    ]
    h.store(run, ROOM, unordered, source="inbox")
    m = records.make_batches(run, ROOM)
    ids = m["batches"]["batch_r1_001"]
    expected = [common.record_id("https://a.test/1", "first by order value"),
                common.record_id("https://a.test/2", "second by order value"),
                common.record_id("https://a.test/3", "third by order value"),
                common.record_id("https://c.test/new", "unordered newer text here"),
                common.record_id("https://c.test/old", "unordered older text here"),
                common.record_id("https://c.test/none", "unordered undated text here")]
    assert ids == expected


def test_money_hint_and_cut():
    assert records.money_hint("I paid ₹15,000 for coaching") is True
    assert records.money_hint("is it worth the fee") is True
    assert records.money_hint("cost me 40k") is True
    assert records.money_hint("2 lakh gone") is True
    assert records.money_hint("USD 300 refund pending") is True
    assert records.money_hint("How to study quant for the GRE") is False


def test_batches_are_deterministic(run, h):
    recs = [h.make_record(f"https://a.test/{i}", f"record text number {i} " + "x" * 2000, rank=i) for i in range(1, 6)]
    h.store(run, ROOM, recs)
    records.make_batches(run, ROOM, size=2, chars=100)
    first = _batch_files(run, ROOM)
    manifest1 = records.manifest_path(run, ROOM).read_bytes()
    records.make_batches(run, ROOM, size=2, chars=100)
    assert _batch_files(run, ROOM) == first
    assert records.manifest_path(run, ROOM).read_bytes() == manifest1
    assert "[…cut]" in first["batch_r1_001.md"].decode("utf-8")
    assert manifest1.endswith(b"\n")
    assert json.loads(manifest1)["chars"] == 100


def test_cli_batches_and_global_flags(run, h, cli):
    r = cli("batches", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 2, r.stderr
    assert "No records for room" in r.stderr and "harvest-search" in r.stderr
    h.store(run, ROOM, [h.make_record("https://a.test/1", "one record is enough here")])
    r = cli("--run", "runs/2026-09-26", "batches", "--room", ROOM)
    assert r.returncode == 0, r.stderr
    assert "1 records loaded" in r.stdout and "batch_r1_001" in r.stdout
    r = cli("batches", "--room", ROOM, "--run", "2026-09-26", "--dry-run")
    assert r.returncode == 0, r.stderr
    r = cli("batches", "--room", "../x", "--run", "2026-09-26")
    assert r.returncode == 1 and "1. room '../x' is not a valid slug" in r.stderr
    r = cli("--help")
    assert r.returncode == 0 and "batches" in r.stdout and "harvest-search" in r.stdout
    assert "warning: pipeline/" in r.stderr or "missing" in r.stderr or r.stderr == ""
    r = cli("no-such-command")
    assert r.returncode == 2


def test_fx_helpers(run):
    fx = common.load_fx(run)
    assert fx["USD"] == 1.0 and fx["INR"] == 88.0
    assert common.to_usd(880, "INR", fx) == 10.0
    assert common.from_usd(10, "inr", fx) == 880.0
    assert round(common.convert(880, "INR", "EUR", fx), 4) == 8.6
    with pytest.raises(common.MissingCurrency) as e:
        common.to_usd(5, "JPY", fx)
    assert "JPY" in str(e.value) and e.value.code == 1


def test_graveyard_helpers(froot):
    assert common.append_graveyard("2026-09-26", 2, "room:a-room", "no reach entry matches") is True
    assert common.append_graveyard("2026-09-26", "stage 2", "room:a-room", "no reach entry matches") is False
    text = froot.joinpath("graveyard.md").read_text(encoding="utf-8")
    assert text.count("room:a-room") == 1
    assert "- 2026-09-26 | stage 2 | room:a-room | no reach entry matches" in text
    assert common.is_dead("room:a-room") and common.dead_items("room") == {"room:a-room"}
    with open(froot / "graveyard.md", "a", encoding="utf-8") as f:
        f.write("  - new evidence 2026-12-01: found a warm path, see record abc\n")
    assert not common.is_dead("room:a-room")
    assert common.parse_graveyard()[0]["status"] == "revived"
    assert common.append_graveyard("2026-09-26", 2, "room:a-room", "a different reason") is True
    assert froot.joinpath("graveyard.md").read_text(encoding="utf-8").count("room:a-room") == 1


def test_walls_ledger_and_checks(froot):
    walls = common.load_walls()
    assert walls["W1"] == {"name": "Trigger", "kind": "machine"}
    assert walls["W29"] == {"name": "Source", "kind": "human"}
    assert len(walls) == 29 and walls["W17"]["kind"] == "human" and walls["W16"]["kind"] == "machine"
    ledger = common.load_ledger()
    assert ledger["supply"]["can_be"][0]["id"] == "c1"
    assert common.load_kill_rules()["stage3"]["saturation_window"] == 300
    assert common.check_judgment({"reasoning": "x", "confidence": "high"}, "p") == []
    assert len(common.check_judgment({"confidence": "sure"}, "p")) == 2
    assert common.check_number({"value": 1, "tag": "measured", "url": "https://a"}, "n") == []
    assert common.check_number({"value": 1, "tag": "measured"}, "n")
    assert common.check_number({"value": None, "tag": "estimate", "reasoning": "r"}, "n", allow_null=True) == []
    price = {"what": "x", "price_text": "$49/month", "amount": 49, "currency": "USD", "unit": "month",
             "url": "https://a.test", "seen_via": "search"}
    assert common.check_price(price, "p") == []
    assert common.check_price(dict(price, seen_via="guess"), "p")
    assert common.check_price(dict(price, currency="usd"), "p")
