"""Stage 6 (`numbers`): every formula and case by hand, each kill check, ranking, the top-5 cut,
the hypothesis and kill-rule sentences, and the `--check` errors."""
import copy
import csv
import json

import pytest

import common
import stage6

ROOM = "gre-engineers-india"
KEY = "quant-plateau"
PID = f"{ROOM}--{KEY}"
FX_INR = 88.0
HOUR_INR = 1500.0
HOUR_USD = HOUR_INR / FX_INR  # 17.0454545...


# --------------------------------------------------------------------------- builders
def base_inputs(pid=PID, currency="INR"):
    """A valid 06_inputs file. The base case passes every check with the real ledger and INR at 88 per USD."""
    return {
        "pain_id": pid, "currency": currency,
        "price_anchor": {"what": "Private GRE quant tutor, 10 hours", "price_text": "Rs 20,000 for 10 hours", "amount": 20000,
                         "currency": "INR", "unit": "package", "url": "https://tutors.test/gre-quant", "seen_via": "search",
                         "reasoning": "the human substitute is a private tutor", "confidence": "moderate"},
        "offer": "a 2-week GRE quant sprint",
        "price": {"low": 3000, "base": 5000, "high": 8000, "billing": "one_off", "months": 1, "payment_days_after_sale": 0,
                  "reasoning": "a quarter of a tutor package"},
        "conversion_rate": {"low": 0.05, "base": 0.1, "high": 0.2, "reasoning": "warm reach through the GRE product"},
        "acquisition": {"minutes_per_reach": {"low": 5, "base": 10, "high": 20, "reasoning": "one WhatsApp message and a reply"},
                        "cash_per_reach": {"low": 0, "base": 50, "high": 100, "reasoning": "a small ad spend per reach"}},
        "delivery": {"my_hours_per_customer": {"value": 1, "tag": "estimate", "reasoning": "one live review call"},
                     "cash_cost_per_customer": {"value": 200, "tag": "estimate", "reasoning": "printing and a tool licence"},
                     "delivery_weeks": {"value": 2, "tag": "estimate", "reasoning": "a two-week sprint"},
                     "live": {"value": True, "fits_evenings_weekends_ist": True, "reasoning": "calls after 8 pm IST"}},
        "channel": {"name": "WhatsApp to GRE product users", "where": "the GRE product's user list", "reach_kind": "warm",
                    "trust": "high", "reasoning": "existing users know the product", "confidence": "moderate"},
        "revenue_horizon": {"boredom_months": {"value": 6, "tag": "estimate", "reasoning": "a seasonal exam cycle"},
                            "melt_months": {"value": None, "tag": "estimate", "reasoning": "the hold wall persists"}},
        "ladder_test": {"position": 1, "urgent": True,
                        "provable_outcome": {"value": True, "how": "a score jump on a timed section", "reasoning": "scores are measurable",
                                             "confidence": "high"}},
        "time_to_first_payment": {"days_to_first_conversation": 3, "days_to_close": 7, "build_days": 2, "reasoning": "warm list, short build"},
        "guarantee": {"offered": True, "refund_per_customer": 2000},
        "test": {"n": 20, "who": "room members", "how": "by WhatsApp", "days": 14},
        "open_questions": ["Will users pay before the score jump is proven?"],
        "confidence": "moderate",
    }


def set_in(data, path, value):
    d = data
    parts = path.split(".")
    for p in parts[:-1]:
        d = d[p]
    d[parts[-1]] = value
    return data


def write_inputs(run, data):
    common.write_json(run / "06_inputs" / f"{data['pain_id']}.json", data)


def write_stage5(run, pids, lanes=None):
    lanes = lanes or {}
    pains = []
    for pid in pids:
        room = pid.split("--")[0]
        pains.append({"pain_id": pid, "room": room, "status": "kept", "lane": lanes.get(pid, "business"), "kept_index": 1,
                      "alternatives": [{"index": 1, "rank": 1, "entry_walls": ["W2", "W9", "W14"], "hold_wall": "W20",
                                        "hold_supply_id": "c1", "valid": True, "lane": lanes.get(pid, "business"),
                                        "one_liner": "For the room, a promise in two weeks.", "crux": "the crux",
                                        "credibility_question": "Will this room accept the founder as accountability?"}]})
    common.write_json(run / "05_pairs.json", {"kept": list(pids), "killed": [], "pains": pains,
                                             "counts": {"in": len(pids), "kept": len(pids), "killed": 0}})


def write_pains(run, counts_by_pid):
    """counts_by_pid: pid -> (failed_spend, money, records, spend_sources, verified_quotes)."""
    pains = []
    for pid, (fs, money, rc, ss, vq) in counts_by_pid.items():
        room, key = pid.split("--")
        pains.append({"pain_id": pid, "room": room, "pain_key": key, "status": "kept", "rank": len(pains) + 1,
                      "record_count": rc, "money_mentions": money, "failed_spend_mentions": fs, "spend_sources": ss,
                      "verified_quote_count": vq,
                      "quotes": [{"record_id": f"r{i}", "url": f"https://forum.test/{i}", "date": None, "text": f"quote {i} words words words"}
                                 for i in range(vq)]})
    common.write_json(run / "03_listen" / "pains.json", {"pains": pains, "kept": list(counts_by_pid)})


def setup_one(run, data=None, counts=(3, 5, 40, 2, 3)):
    data = data or base_inputs()
    write_stage5(run, [data["pain_id"]])
    write_pains(run, {data["pain_id"]: counts})
    write_inputs(run, data)
    return data


def survivors(run):
    return json.loads((run / "06_survivors.json").read_text(encoding="utf-8"))


def graveyard(froot):
    return (froot / "graveyard.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- formulas, by hand
def test_every_formula_in_all_three_cases_inr_one_off(run):
    data = setup_one(run)
    result = stage6.numbers(run)
    e = result["pains"][0]
    assert e["status"] == "kept" and e["rank"] == 1 and e["failed_checks"] == []
    assert e["hour_value"]["value"] == HOUR_INR and e["hour_value"]["usd"] == pytest.approx(HOUR_USD, abs=1e-4)
    assert e["hour_value"]["in_room_currency"] == pytest.approx(1500.0, abs=1e-3) and e["hour_value"]["assumed"] is True

    # base: price 5000, conv 0.1, 10 min, INR 50 per reach; delivery 1 h, INR 200, 2 weeks
    b = e["cases"]["base"]
    assert b["inputs"] == {"price": 5000, "conversion": 0.1, "minutes_per_reach": 10, "cash_per_reach": 50}
    assert b["price"] == 5000 and b["price_total"] == 5000
    assert b["reaches_per_sale"] == pytest.approx(10.0)
    assert b["acq_hours"] == pytest.approx(10 * 10 / 60, abs=1e-4)           # 1.6667 h
    assert b["acq_cash"] == pytest.approx(500.0)
    assert b["acquisition_cost"] == pytest.approx(500 + (10 * 10 / 60) * 1500, abs=1e-2)   # 3000
    assert b["net_cash"] == pytest.approx(5000 - 200 - 500)                   # 4300
    assert b["founder_hours"] == pytest.approx(1 + 10 * 10 / 60, abs=1e-4)   # 2.6667 h
    assert b["usd_per_hour"] == pytest.approx((4300 / (1 + 10 / 6)) / FX_INR, abs=1e-2)   # 18.32
    assert b["cash30"] == 5000 and b["cash30_usd"] == pytest.approx(5000 / FX_INR, abs=1e-2)
    assert b["price_usd"] == pytest.approx(56.82, abs=1e-2) and b["net_cash_usd"] == pytest.approx(4300 / FX_INR, abs=1e-2)

    # low: price 3000, conv 0.05, 20 min, INR 100 per reach
    lo = e["cases"]["low"]
    assert lo["inputs"] == {"price": 3000, "conversion": 0.05, "minutes_per_reach": 20, "cash_per_reach": 100}
    assert lo["reaches_per_sale"] == pytest.approx(20.0)
    assert lo["acq_hours"] == pytest.approx(20 * 20 / 60, abs=1e-4)          # 6.6667 h
    assert lo["acq_cash"] == pytest.approx(2000.0)
    assert lo["acquisition_cost"] == pytest.approx(2000 + (20 * 20 / 60) * 1500, abs=1e-2)  # 12000
    assert lo["net_cash"] == pytest.approx(3000 - 200 - 2000)                 # 800
    assert lo["founder_hours"] == pytest.approx(1 + 20 * 20 / 60, abs=1e-4)  # 7.6667
    assert lo["usd_per_hour"] == pytest.approx((800 / (1 + 400 / 60)) / FX_INR, abs=1e-2)  # 1.19
    assert lo["cash30"] == 3000

    # high: price 8000, conv 0.2, 5 min, INR 0 per reach
    hi = e["cases"]["high"]
    assert hi["inputs"] == {"price": 8000, "conversion": 0.2, "minutes_per_reach": 5, "cash_per_reach": 0}
    assert hi["reaches_per_sale"] == pytest.approx(5.0)
    assert hi["acq_hours"] == pytest.approx(5 * 5 / 60, abs=1e-4)            # 0.4167 h
    assert hi["acq_cash"] == 0.0
    assert hi["acquisition_cost"] == pytest.approx((5 * 5 / 60) * 1500, abs=1e-2)  # 625
    assert hi["net_cash"] == pytest.approx(8000 - 200)                        # 7800
    assert hi["founder_hours"] == pytest.approx(1 + 25 / 60, abs=1e-4)
    assert hi["usd_per_hour"] == pytest.approx((7800 / (1 + 25 / 60)) / FX_INR, abs=1e-2)  # 62.57
    assert hi["cash30"] == 8000
    assert lo["usd_per_hour"] < b["usd_per_hour"] < hi["usd_per_hour"]

    # per pain
    assert e["days_to_first_payment"] == 12 and e["days_parts"] == {"days_to_first_conversation": 3, "days_to_close": 7, "build_days": 2}
    assert e["horizon_months"] == 6 and e["horizon_parts"] == {"boredom_months": 6, "melt_months": None}
    assert e["first_cohort"] == 5
    assert e["cohort_hours_per_week"] == pytest.approx(5 * 1 / 2 + 5 * (10 / 6) / (14 / 7), abs=1e-4)  # 6.6667
    assert e["guarantee_exposure"] == 10000.0 and e["guarantee_exposure_ledger"] == pytest.approx(10000.0, abs=1e-2)
    assert e["guarantee_exposure_usd"] == pytest.approx(10000 / FX_INR, abs=1e-2)
    assert e["anchor"]["amount_usd"] == pytest.approx(20000 / FX_INR, abs=1e-2)
    assert e["anchor_ratio"] == pytest.approx(0.25, abs=1e-4)
    assert e["anchor"]["price_status"] == "seen_via_search" and e["anchor"]["price_tag"] == "[measured, page not checked]"
    assert e["evidence"] == "strong" and e["opens_ladder"] is True and e["lane"] == "business"
    # every number carries a tag
    for name in ("price", "price_total", "reaches_per_sale", "acq_hours", "acq_cash", "acquisition_cost", "net_cash", "founder_hours",
                 "usd_per_hour", "cash30", "days_to_first_payment", "horizon_months", "cohort_hours_per_week", "guarantee_exposure",
                 "anchor_ratio"):
        assert e["tags"][name] in ("measured", "estimate"), name
    assert result["counts"] == {"in": 1, "survived": 1, "kept": 1, "cut": 0, "killed": 0}


def test_monthly_billing_usd_room_and_cash30_is_one_month(run):
    data = base_inputs(pid="us-freelancers--late-invoices", currency="USD")
    data["price"] = {"low": 30, "base": 40, "high": 60, "billing": "monthly", "months": 3, "payment_days_after_sale": 0,
                     "reasoning": "a small subscription"}
    data["conversion_rate"] = {"low": 0.1, "base": 0.1, "high": 0.1, "reasoning": "flat"}
    data["acquisition"]["minutes_per_reach"] = {"low": 6, "base": 6, "high": 6, "reasoning": "flat"}
    data["acquisition"]["cash_per_reach"] = {"low": 0, "base": 0, "high": 0, "reasoning": "none"}
    data["delivery"]["my_hours_per_customer"]["value"] = 0.5
    data["delivery"]["cash_cost_per_customer"]["value"] = 0
    data["delivery"]["delivery_weeks"]["value"] = 4
    data["price_anchor"].update({"amount": 400, "currency": "USD", "price_text": "$400 per month"})
    data["guarantee"] = {"offered": False, "refund_per_customer": 0}
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    b = e["cases"]["base"]
    assert e["currency"] == "USD" and e["fx_per_usd"] == 1.0
    assert b["price"] == 40 and b["price_total"] == 120 and b["price_total_usd"] == 120
    assert b["reaches_per_sale"] == pytest.approx(10.0) and b["acq_hours"] == pytest.approx(1.0)
    assert b["acquisition_cost"] == pytest.approx(HOUR_USD, abs=1e-2)        # 1 h at the hour value, no cash
    assert b["net_cash"] == 120 and b["founder_hours"] == pytest.approx(1.5)
    assert b["usd_per_hour"] == pytest.approx(80.0)
    assert b["cash30"] == 40                                                  # the monthly price, not the total
    assert e["cases"]["low"]["price_total"] == 90 and e["cases"]["high"]["price_total"] == 180
    assert e["guarantee_exposure"] == 0.0 and e["checks"]["guarantee"]["reason"] == "no guarantee is offered"
    assert e["anchor_ratio"] == pytest.approx(0.1)
    assert e["price_text"] == "USD 40.00 a month"
    assert e["hour_value"]["in_room_currency"] == pytest.approx(HOUR_USD, abs=1e-4)


def test_horizon_ignores_nulls_and_anchor_ratio_not_computable_at_zero(run):
    data = base_inputs()
    data["revenue_horizon"]["boredom_months"] = {"value": None, "tag": "estimate", "reasoning": "unknown"}
    data["revenue_horizon"]["melt_months"] = {"value": 9, "tag": "estimate", "reasoning": "the wall melts in nine months"}
    data["price_anchor"]["amount"] = 0
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["horizon_months"] == 9 and e["anchor_ratio"] is None
    md = (run / "06_numbers.md").read_text(encoding="utf-8")
    assert "not computable" in md


# --------------------------------------------------------------------------- the six kill checks
@pytest.mark.parametrize("change, check, needle", [
    ({"price.base": 3200}, "usd_per_hour", "the ledger's hour value is USD 17.05"),
    ({"price.payment_days_after_sale": 45}, "cash30", "nothing is paid within 30 days"),
    ({"time_to_first_payment.days_to_first_conversation": 30, "time_to_first_payment.days_to_close": 30,
      "time_to_first_payment.build_days": 10}, "days_to_first_payment", "first payment expected on day 70"),
    ({"price.base": 50000, "price.high": 50000, "delivery.my_hours_per_customer.value": 4, "delivery.delivery_weeks.value": 1},
     "cohort_hours", "the ledger allows 8"),
    ({"guarantee.refund_per_customer": 30000}, "guarantee", "the reserve is INR 100,000.00"),
    ({"delivery.live.fits_evenings_weekends_ist": False}, "live_window", "does not fit evenings and weekends"),
])
def test_each_base_case_check_kills_alone_with_its_reason(froot, run, change, check, needle):
    data = base_inputs()
    for path, value in change.items():
        set_in(data, path, value)
    setup_one(run, data)
    result = stage6.numbers(run)
    e = result["pains"][0]
    assert e["status"] == "killed" and e["rank"] is None
    assert e["failed_checks"] == [check], e["checks"]
    assert needle in e["checks"][check]["reason"]
    assert result["counts"]["killed"] == 1 and result["kept"] == []
    gy = graveyard(froot)
    assert f"- 2026-09-26 | stage 6 | pain:{PID} | numbers fail in the base case: {check}:" in gy


def test_kill_check_values_by_hand(run):
    # cohort: 5 x 4 h / 1 week + 5 x 1.6667 h / 2 weeks = 20 + 4.1667 = 24.17 h/week
    data = base_inputs()
    for path, value in {"price.base": 50000, "price.high": 50000, "delivery.my_hours_per_customer.value": 4,
                        "delivery.delivery_weeks.value": 1}.items():
        set_in(data, path, value)
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["checks"]["cohort_hours"]["value"] == pytest.approx(20 + 5 * (10 / 6) / 2, abs=1e-3)
    assert e["checks"]["cohort_hours"]["limit"] == 8
    # guarantee: 5 x 30000 = 150000 INR against the 100000 reserve
    data = base_inputs()
    set_in(data, "guarantee.refund_per_customer", 30000)
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["checks"]["guarantee"]["value"] == 150000 and e["checks"]["guarantee"]["limit"] == 100000
    # usd_per_hour: net 3200 - 200 - 500 = 2500 over 2.6667 h = 937.5 INR/h = 10.65 USD/h against 17.05
    data = base_inputs()
    set_in(data, "price.base", 3200)
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["checks"]["usd_per_hour"]["value"] == pytest.approx((2500 / (1 + 10 / 6)) / FX_INR, abs=1e-2)
    assert e["checks"]["cash30"]["pass"] is True and e["checks"]["cohort_hours"]["pass"] is True
    assert e["checks"]["usd_per_hour"]["limit"] == pytest.approx(HOUR_USD, abs=1e-3)
    # cash30: 0 against the acquisition cost 3000
    data = base_inputs()
    set_in(data, "price.payment_days_after_sale", 45)
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["checks"]["cash30"]["value"] == 0 and e["checks"]["cash30"]["limit"] == pytest.approx(3000, abs=1e-2)


def test_several_failed_checks_all_land_in_the_graveyard_line(froot, run):
    data = base_inputs()
    set_in(data, "price.payment_days_after_sale", 45)
    set_in(data, "delivery.live.fits_evenings_weekends_ist", False)
    setup_one(run, data)
    e = stage6.numbers(run)["pains"][0]
    assert e["failed_checks"] == ["cash30", "live_window"]
    line = next(ln for ln in graveyard(froot).splitlines() if f"pain:{PID}" in ln)
    assert "cash30:" in line and "live_window:" in line


def test_runway_in_the_ledger_tightens_the_days_limit_and_factor_scales_hour_value(froot, run, h):
    import yaml

    p = froot / "config" / "ledger.yaml"
    ledger = yaml.safe_load(p.read_text(encoding="utf-8"))
    ledger["constraints"]["runway"]["runway_months"] = 0.3   # 9 days
    p.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")
    h.set_rule(froot, "stage6", "min_usd_per_hour_vs_hour_value", 2.0)
    setup_one(run)
    e = stage6.numbers(run)["pains"][0]
    assert e["checks"]["days_to_first_payment"]["pass"] is False
    assert e["checks"]["days_to_first_payment"]["limit"] == pytest.approx(9.0)
    assert "runway 0.3 months = 9 days" in e["checks"]["days_to_first_payment"]["reason"]
    assert e["checks"]["usd_per_hour"]["limit"] == pytest.approx(2 * HOUR_USD, abs=1e-3)
    assert e["checks"]["usd_per_hour"]["pass"] is False   # 18.32 < 34.09
    assert e["failed_checks"] == ["usd_per_hour", "days_to_first_payment"]


# --------------------------------------------------------------------------- evidence
def test_evidence_labels_follow_kill_rules():
    rules = common.load_kill_rules()

    def label(fs, money, rc, ss):
        return stage6.evidence_strength({"failed_spend": fs, "money": money, "records": rc, "spend_sources": ss, "verified_quotes": 3}, rules)

    assert label(3, 0, 30, 2) == "strong"
    assert label(2, 0, 30, 2) == "moderate"      # failed spend below 3
    assert label(3, 0, 29, 2) == "moderate"      # records below 30
    assert label(3, 0, 30, 1) == "moderate"      # one spend source
    assert label(0, 3, 15, 0) == "moderate"      # money 3, records 15
    assert label(1, 0, 15, 0) == "moderate"      # failed spend 1
    assert label(0, 2, 15, 0) == "weak"          # money below 3, no failed spend
    assert label(0, 3, 14, 0) == "weak"          # records below 15
    assert label(0, 0, 100, 5) == "weak"


def test_missing_pains_entry_labels_weak_and_notes_for_review(run):
    data = base_inputs()
    write_stage5(run, [PID])
    write_inputs(run, data)
    result = stage6.numbers(run)
    e = result["pains"][0]
    assert e["evidence"] == "weak" and e["evidence_counts_found"] is False
    assert any("evidence labeled weak" in n for n in result["notes"])
    events = [json.loads(ln) for ln in (run / "runlog.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(ev["kind"] == "note" and ev.get("review") is True and "evidence counts are unknown" in ev["note"] for ev in events)


# --------------------------------------------------------------------------- ranking and the cut
def test_ranking_order_opens_ladder_days_usd_per_hour_evidence(run):
    pids = {}
    # p1: opens ladder, day 12, 18.32 USD/h, weak evidence
    p1 = base_inputs(pid=f"{ROOM}--p1")
    # p2: step 2, day 5, high USD/h, strong evidence -> last, because it does not open the ladder
    p2 = base_inputs(pid=f"{ROOM}--p2")
    set_in(p2, "ladder_test.position", 2)
    set_in(p2, "time_to_first_payment.days_to_close", 0)
    set_in(p2, "price.base", 20000)
    set_in(p2, "price.high", 20000)
    # p3: opens ladder, day 20 -> after p1
    p3 = base_inputs(pid=f"{ROOM}--p3")
    set_in(p3, "time_to_first_payment.days_to_close", 15)
    # p4: opens ladder, day 12, higher USD/h than p1 -> before p1
    p4 = base_inputs(pid=f"{ROOM}--p4")
    set_in(p4, "price.base", 6000)
    # p5: same numbers as p1 but stronger evidence -> before p1, after p4
    p5 = base_inputs(pid=f"{ROOM}--p5")
    for d in (p1, p2, p3, p4, p5):
        pids[d["pain_id"]] = d
    write_stage5(run, sorted(pids))
    write_pains(run, {f"{ROOM}--p1": (0, 0, 5, 0, 2), f"{ROOM}--p2": (5, 9, 60, 3, 4), f"{ROOM}--p3": (0, 0, 5, 0, 2),
                      f"{ROOM}--p4": (0, 0, 5, 0, 2), f"{ROOM}--p5": (3, 4, 40, 2, 3)})
    for d in pids.values():
        write_inputs(run, d)
    result = stage6.numbers(run)
    assert result["kept"] == [f"{ROOM}--p4", f"{ROOM}--p5", f"{ROOM}--p1", f"{ROOM}--p3", f"{ROOM}--p2"]
    by = {e["pain_id"]: e for e in result["pains"]}
    assert by[f"{ROOM}--p2"]["opens_ladder"] is False and by[f"{ROOM}--p2"]["days_to_first_payment"] == 5
    assert by[f"{ROOM}--p2"]["cases"]["base"]["usd_per_hour"] > by[f"{ROOM}--p4"]["cases"]["base"]["usd_per_hour"]
    assert by[f"{ROOM}--p5"]["evidence"] == "strong" and by[f"{ROOM}--p1"]["evidence"] == "weak"
    assert [e["rank"] for e in result["pains"]] == [1, 2, 3, 4, 5]
    assert result["rank_by"] == ["opens_ladder", "days_to_first_payment", "usd_per_hour_base", "evidence_strength"]


def test_keeps_at_most_five_and_cuts_the_rest_with_a_graveyard_line(froot, run):
    datas = []
    for i in range(1, 7):
        d = base_inputs(pid=f"{ROOM}--p{i}")
        set_in(d, "time_to_first_payment.build_days", i)   # day 11 + i, so the order is p1 .. p6
        datas.append(d)
    write_stage5(run, [d["pain_id"] for d in datas])
    write_pains(run, {d["pain_id"]: (1, 1, 20, 1, 2) for d in datas})
    for d in datas:
        write_inputs(run, d)
    result = stage6.numbers(run)
    assert result["counts"] == {"in": 6, "survived": 6, "kept": 5, "cut": 1, "killed": 0}
    assert result["kept"] == [f"{ROOM}--p{i}" for i in range(1, 6)] and result["cut"] == [f"{ROOM}--p6"]
    cut = next(e for e in result["pains"] if e["status"] == "cut")
    assert cut["rank"] == 6
    gy = graveyard(froot)
    assert f"- 2026-09-26 | stage 6 | pain:{ROOM}--p6 | cut: ranked 6 of 6 survivors and max_survivors is 5" in gy
    for i in range(1, 6):
        assert f"pain:{ROOM}--p{i} |" not in gy
    md = (run / "06_numbers.md").read_text(encoding="utf-8")
    assert "only the top 5 survivors are kept" in md
    rows = list(csv.DictReader((run / "06_numbers.csv").open(encoding="utf-8")))
    assert [r["status"] for r in rows if r["pain_id"] == f"{ROOM}--p6"] == ["cut", "cut", "cut"]


# --------------------------------------------------------------------------- sentences and files
def test_hypothesis_and_kill_rule_sentences_carry_local_price_and_usd(run):
    setup_one(run)
    e = stage6.numbers(run)["pains"][0]
    assert e["price_text"] == "INR 5,000.00 (USD 56.82)"
    assert e["hypothesis"] == ("At least 1 of 20 room members, reached by WhatsApp, will pay INR 5,000.00 (USD 56.82) "
                               "for a 2-week GRE quant sprint within 14 days.")
    assert e["kill_rule"] == ("Kill it if fewer than 1 of the 20 pays INR 5,000.00 (USD 56.82) within 14 days of the first message. "
                              "Decide on day 14. No extensions.")


def test_csv_has_one_row_per_pain_and_case_and_md_shows_formulas_tags_and_cases(run):
    setup_one(run)
    stage6.numbers(run)
    rows = list(csv.DictReader((run / "06_numbers.csv").open(encoding="utf-8")))
    assert [(r["pain_id"], r["case"], r["status"]) for r in rows] == [(PID, "low", "kept"), (PID, "base", "kept"), (PID, "high", "kept")]
    assert rows[1]["price"] == "5000.0" and rows[1]["price_usd"] == "56.82" and rows[1]["net_cash"] == "4300.0"
    assert rows[0]["price"] == "3000.0" and rows[2]["price"] == "8000.0"
    assert rows[1]["days_to_first_payment"] == "12" and rows[1]["evidence"] == "strong" and rows[1]["opens_ladder"] == "yes"
    assert rows[1]["failed_checks"] == "" and rows[1]["currency"] == "INR"
    assert list(rows[0].keys()) == stage6.CSV_COLUMNS
    md = (run / "06_numbers.md").read_text(encoding="utf-8")
    assert "| Number | Formula | Low | Base | High | Tag |" in md
    assert "| net_cash | price_total - delivery cash cost - acq_cash | INR 800.00 (USD 9.09) | INR 4,300.00 (USD 48.86) | INR 7,800.00 (USD 88.64) | estimate |" in md
    assert "| usd_per_hour | (net_cash / founder_hours) / units of the currency per USD | USD 1.19/h | USD 18.32/h | USD 62.57/h | estimate |" in md
    assert "| reaches_per_sale | 1 / conversion | 20.00 | 10.00 | 5.00 | estimate |" in md
    assert "| days_to_first_payment | first conversation 3 + close 7 + build 2 | 12 days | estimate |" in md
    assert "cohort_hours_per_week | 5 x 1 h / 2 weeks + 5 x 1.67 h / (14 days / 7) | 6.67 h/week" in md
    assert "[measured, page not checked]" in md and "Founder hour value: INR 1,500.00 = USD 17.05" in md
    assert "### Reading" in md and "Passed every check." in md
    assert "- Hypothesis: At least 1 of 20" in md and "- Kill rule: Kill it if fewer than 1" in md


def test_rerun_is_byte_identical_and_never_duplicates_graveyard_lines(froot, run):
    data = base_inputs()
    set_in(data, "delivery.live.fits_evenings_weekends_ist", False)
    setup_one(run, data)
    stage6.numbers(run)
    first = {n: (run / n).read_bytes() for n in ("06_survivors.json", "06_numbers.csv", "06_numbers.md")}
    gy1 = graveyard(froot)
    stage6.numbers(run)
    assert {n: (run / n).read_bytes() for n in first} == first
    assert graveyard(froot) == gy1
    assert gy1.count(f"pain:{PID}") == 1
    text = (run / "06_survivors.json").read_text(encoding="utf-8")
    assert text.endswith("\n") and json.loads(text) == json.loads(json.dumps(json.loads(text), sort_keys=True))


def test_extra_input_files_are_ignored_with_a_warning_and_missing_ones_exit_2(run, cli):
    setup_one(run)
    write_inputs(run, base_inputs(pid=f"{ROOM}--stray"))
    r = cli("numbers", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"warning: 06_inputs/{ROOM}--stray.json is not a Stage 5 survivor; ignored." in r.stdout
    assert f"kept #1: {PID}" in r.stdout
    (run / "06_inputs" / f"{PID}.json").unlink()
    r = cli("numbers", "--run", "2026-09-26")
    assert r.returncode == 2 and f"06_inputs/{PID}.json" in r.stderr and "funnel-walker in mode numbers" in r.stderr
    (run / "05_pairs.json").unlink()
    r = cli("numbers", "--run", "2026-09-26")
    assert r.returncode == 2 and "05_pairs.json is missing" in r.stderr


def test_missing_currency_names_it(run, cli):
    data = base_inputs(currency="JPY")
    setup_one(run, data)
    r = cli("numbers", "--run", "2026-09-26")
    assert r.returncode == 1 and "no rate for currency JPY" in r.stderr


# --------------------------------------------------------------------------- --check
def test_check_valid_file_prints_numbers_writes_nothing_and_logs_a_check_event(run, cli):
    write_inputs(run, base_inputs())
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"06_inputs/{PID}.json: valid." in r.stdout
    assert "USD per hour: low 1.19, base 18.32, high 62.57 (ledger hour value USD 17.05)." in r.stdout
    assert "Passes every base-case check. Nothing was written." in r.stdout
    assert "pass usd_per_hour:" in r.stdout and "pass live_window:" in r.stdout
    assert not (run / "06_survivors.json").exists() and not (run / "06_numbers.csv").exists()
    events = [json.loads(ln) for ln in (run / "runlog.jsonl").read_text(encoding="utf-8").splitlines()]
    ev = [e for e in events if e["kind"] == "check" and e["command"] == "numbers"]
    assert ev and ev[-1]["pain"] == PID and ev[-1]["failed_checks"] == [] and ev[-1]["stage"] == 6


def test_check_reports_would_be_killed(run, cli):
    data = base_inputs()
    set_in(data, "price.payment_days_after_sale", 45)
    write_inputs(run, data)
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Would be killed by `funnel numbers`: cash30 failed in the base case." in r.stdout
    assert "FAIL cash30:" in r.stdout


def test_check_lists_every_problem_in_plain_english(run, cli):
    data = base_inputs()
    data["price"]["low"] = 9000                       # low > base
    data["price"]["billing"] = "yearly"
    data["conversion_rate"]["base"] = 0               # must be more than 0
    data["acquisition"]["minutes_per_reach"]["high"] = "ten"
    del data["delivery"]["live"]["reasoning"]
    data["channel"]["trust"] = "huge"
    data["ladder_test"]["position"] = 0
    data["time_to_first_payment"]["build_days"] = -1
    data["guarantee"]["offered"] = "yes"
    data["test"]["n"] = 0
    data["open_questions"] = "none"
    data["confidence"] = "sure"
    data["price_anchor"]["seen_via"] = "memory"
    del data["offer"]
    write_inputs(run, data)
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 1
    for needle in ("price: low <= base <= high must hold", "price.billing must be one_off or monthly",
                   "conversion_rate.base: must be more than 0", "acquisition.minutes_per_reach.high: must be a number",
                   "delivery.live: missing 'reasoning'", "channel.trust must be high, medium or low",
                   "ladder_test.position must be a whole number from 1", "time_to_first_payment.build_days must be a whole number",
                   "guarantee.offered must be true or false", "test.n must be a whole number from 1",
                   "'open_questions' must be a list of strings", "'confidence' must be high, moderate or low",
                   "price_anchor: 'seen_via' must be page or search", "'offer' is missing"):
        assert needle in r.stderr, needle
    assert "Fix these: 15 items" in r.stderr


def test_check_wrong_pain_id_zero_time_missing_file_and_missing_currency(run, cli):
    data = base_inputs()
    data["pain_id"] = f"{ROOM}--other"
    write_inputs(run, dict(data, pain_id=PID))
    common.write_json(run / "06_inputs" / f"{PID}.json", data)
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 1 and f"'pain_id' must be {PID}" in r.stderr
    data = base_inputs()
    data["delivery"]["my_hours_per_customer"]["value"] = 0
    data["acquisition"]["minutes_per_reach"] = {"low": 0, "base": 0, "high": 0, "reasoning": "none"}
    write_inputs(run, data)
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 1 and "cannot both be 0" in r.stderr
    data = base_inputs(currency="AUD")
    write_inputs(run, data)
    r = cli("numbers", "--check", PID, "--run", "2026-09-26")
    assert r.returncode == 1 and "no rate for currency AUD" in r.stderr
    r = cli("numbers", "--check", f"{ROOM}--nothing", "--run", "2026-09-26")
    assert r.returncode == 2 and f"06_inputs/{ROOM}--nothing.json is missing" in r.stderr
    r = cli("numbers", "--check", "not a pain id", "--run", "2026-09-26")
    assert r.returncode == 1 and "must look like <room-slug>--<pain-key>" in r.stderr


def test_check_one_returns_an_entry_with_lane_when_stage5_exists(run):
    data = setup_one(run)
    e = stage6.check_one(run, PID)
    assert e["status"] == "survived" and e["lane"] == "business" and e["evidence"] == "strong"
    assert e["cases"]["base"]["usd_per_hour"] == pytest.approx(18.32, abs=1e-2)
    assert copy.deepcopy(e["hypothesis"]).startswith("At least 1 of 20")


def test_price_anchor_seen_on_page_is_not_fetched_offline_and_blocked_domain_is_listed(run, cli):
    data = base_inputs()
    data["price_anchor"]["seen_via"] = "page"
    setup_one(run, data)
    r = cli("numbers", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    s = survivors(run)
    e = s["pains"][0]
    assert e["anchor"]["price_status"] == "blocked_by_network" and e["anchor"]["price_tag"] == "[measured, page not checked]"
    assert s["price_check"]["blocked_domains"] == ["tutors.test"]
    assert "Domains to allow for price-anchor pages: tutors.test" in r.stdout
