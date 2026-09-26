import csv

import common
import quote_check
import records

ROOM = "gre-engineers-india"
TEXT = "I paid ₹45,000 for a “premium” GRE course – it didn't help my quant score at all"
URL = "https://forum.test/t/1"


def _room(run, h):
    h.store(run, ROOM, [h.make_record(URL, TEXT, date="2025-02-03"),
                        h.make_record("https://a.test/t", "Best GRE Prep Courses in 2026 | Compared & Reviewed")])
    return records.records_by_id(run, ROOM)


def _q(rid, text, url=URL, date="2025-02-03"):
    return {"record_id": rid, "url": url, "date": date, "text": text}


def test_exact_substring_passes_and_whitespace_is_normalized(run, h):
    by_id = _room(run, h)
    rid = common.record_id(URL, TEXT)
    ok = quote_check.check_quote(_q(rid, "it didn't help my quant score"), by_id, 5)
    assert ok["status"] == "pass" and ok["reason"] == "ok" and ok["citation_corrected"] is False
    spaced = quote_check.check_quote(_q(rid, "it   didn't help\nmy quant score"), by_id, 5)
    assert spaced["status"] == "pass"
    whole = quote_check.check_quote(_q(rid, TEXT), by_id, 5)
    assert whole["status"] == "pass"


def test_whole_title_may_be_a_quote(run, h):
    by_id = _room(run, h)
    title = "Best GRE Prep Courses in 2026 | Compared & Reviewed"
    rid = common.record_id("https://a.test/t", title)
    r = quote_check.check_quote(_q(rid, title, url="https://a.test/t", date=None), by_id, 5)
    assert r["status"] == "pass"


def test_case_punctuation_and_quote_style_must_match(run, h):
    by_id = _room(run, h)
    rid = common.record_id(URL, TEXT)
    assert quote_check.check_quote(_q(rid, "It didn't help my quant score"), by_id, 5)["reason"] == "not_substring"
    assert quote_check.check_quote(_q(rid, 'a "premium" GRE course'), by_id, 5)["reason"] == "not_substring"
    assert quote_check.check_quote(_q(rid, "GRE course - it didn't help"), by_id, 5)["reason"] == "not_substring"
    assert quote_check.check_quote(_q(rid, "a “premium” GRE course – it"), by_id, 5)["reason"] == "ok"


def test_failure_reasons(run, h):
    by_id = _room(run, h)
    rid = common.record_id(URL, TEXT)
    assert quote_check.check_quote(_q(rid, "quant score at all"), by_id, 5)["reason"] == "too_short"
    assert quote_check.check_quote(_q(rid, "quant score at all"), by_id, 4)["reason"] == "ok"
    assert quote_check.check_quote(_q("0000000000000000", "it didn't help my quant score"), by_id, 5)["reason"] == "record_missing"
    assert quote_check.check_quote(_q(rid, "   "), by_id, 5)["reason"] == "empty"
    assert quote_check.check_quote({"text": "it didn't help my quant score"}, by_id, 5)["reason"] == "record_missing"
    assert quote_check.check_quote("not an object", by_id, 5)["reason"] == "empty"


def test_citation_corrected_from_stored_record(run, h):
    by_id = _room(run, h)
    rid = common.record_id(URL, TEXT)
    r = quote_check.check_quote(_q(rid, "it didn't help my quant score", url="https://wrong.test", date="2020-01-01"), by_id, 5)
    assert r["status"] == "pass" and r["citation_corrected"] is True
    assert r["url"] == URL and r["date"] == "2025-02-03"
    verified, rows = quote_check.check_quotes("gre-engineers-india--quant", [_q(rid, "it didn't help my quant score", url="x", date=None)], by_id, 5)
    assert verified == [{"record_id": rid, "url": URL, "date": "2025-02-03", "text": "it didn't help my quant score"}]
    assert rows[0]["citation_corrected"] == "yes" and rows[0]["pain_id"] == "gre-engineers-india--quant"


def test_csv_columns(run, h, tmp_path):
    by_id = _room(run, h)
    rid = common.record_id(URL, TEXT)
    _, rows = quote_check.check_quotes("r--p", [_q(rid, "it didn't help my quant score"), _q(rid, "nope not here at all")], by_id, 5)
    out = tmp_path / "quote_check.csv"
    quote_check.write_csv(out, rows)
    with open(out, newline="", encoding="utf-8") as f:
        read = list(csv.DictReader(f))
    assert list(read[0].keys()) == ["pain_id", "record_id", "status", "reason", "citation_corrected", "url", "date", "quote"]
    assert [r["reason"] for r in read] == ["ok", "not_substring"]
    assert out.read_bytes().endswith(b"\n") and b"\r\n" not in out.read_bytes()


def test_cli_self_check_changes_nothing(run, h, cli):
    _room(run, h)
    rid = common.record_id(URL, TEXT)
    draft = common.room_dir(run, ROOM) / "pains_draft.json"
    r = cli("quote-check", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 2 and "pains_draft.json is missing" in r.stderr
    common.write_json(draft, {"pains": [{"pain_key": "quant-plateau", "quotes": [
        _q(rid, "it didn't help my quant score"),
        _q(rid, "It didn't help my quant score"),
        _q(rid, "quant score"),
    ]}]})
    before = draft.read_bytes()
    r = cli("quote-check", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "quote 1: ok" in r.stdout and "quote 2: FAIL not_substring" in r.stdout and "quote 3: FAIL too_short" in r.stdout
    assert "1. " in r.stderr and "2. " in r.stderr and "funnel show --room gre-engineers-india --ids " + rid in r.stderr
    assert draft.read_bytes() == before
    assert not (common.room_dir(run, ROOM) / "quote_check.csv").exists()
    common.write_json(draft, {"pains": [{"pain_key": "quant-plateau", "quotes": [
        _q(rid, "it didn't help my quant score"), _q(rid, "I paid ₹45,000 for a “premium” GRE course", url="x", date=None)]}]})
    r = cli("quote-check", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "2 of 2 quotes verified (ok)" in r.stdout and "citation corrected" in r.stdout
