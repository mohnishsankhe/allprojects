"""Stage 6: the numbers (`numbers [--check PAIN_ID]`).

For every Stage 5 survivor the script reads RUN/06_inputs/<pain-id>.json (the
walker's judged inputs), the ledger and RUN/fx_rates.json, computes every
figure in the room's currency and in US dollars for the three cases (low,
base, high), applies the six base-case kill checks, labels the evidence,
ranks the survivors, keeps at most max_survivors, and writes
06_numbers.csv, 06_numbers.md and 06_survivors.json. Every kill and cut goes
to graveyard.md. All arithmetic and currency conversion happens here (rule 2).

Cases
    low  = price.low,  conversion.low,  minutes_per_reach.high, cash_per_reach.high
    base = all base values
    high = price.high, conversion.high, minutes_per_reach.low,  cash_per_reach.low

Formulas (per case, in the room's currency c; h_c = the ledger's hour value converted to c via USD)
    price_total       = price x months (monthly) or price (one-off)
    reaches_per_sale  = 1 / conversion
    acq_hours         = reaches_per_sale x minutes_per_reach / 60
    acq_cash          = reaches_per_sale x cash_per_reach
    acquisition_cost  = acq_cash + acq_hours x h_c
    net_cash          = price_total - delivery cash cost - acq_cash
    founder_hours     = delivery hours + acq_hours
    usd_per_hour      = (net_cash / founder_hours) / fx(c)
    cash30            = price if payment_days_after_sale <= 30 else 0
Per pain
    horizon_months        = min(boredom_months, melt_months) ignoring nulls
    days_to_first_payment = days_to_first_conversation + days_to_close + build_days
    cohort_hours_per_week = first_cohort x delivery hours / delivery_weeks
                            + first_cohort x acq_hours(base) / (test.days / 7)
    guarantee_exposure    = first_cohort x refund_per_customer (room currency), also in the ledger's currency
    anchor_ratio          = base price / anchor amount (both in USD)

Public API
----------
    STAGE, CASES, CHECKS, EVIDENCE_ORDER
    load_pains(run) -> dict[pain_id -> pain]        RUN/03_listen/pains.json ({} when missing)
    kept_pains(pains) -> dict                       pains whose status is not a kill/drop/cut
    pain_counts(pain) -> dict                       {"failed_spend", "money", "records", "spend_sources", "verified_quotes"}
    load_stage5(run) -> dict[pain_id -> entry]      Stage 5 survivors from RUN/05_pairs.json
    stage5_lane(entry) -> str | None
    stage5_pair(entry) -> dict | None
    hour_value(ledger, fx) -> dict                  {"value", "currency", "usd", "assumed", "tag"}
    validate_input(data, where, fx) -> list[str]
    case_inputs(data, case) -> dict
    compute_case(data, case, h_c, fx_c) -> dict
    compute_pain(data, rules, ledger, fx) -> dict   every number for one pain (no checks)
    run_checks(numbers, data, rules, ledger, hour) -> dict[check -> {"pass", "value", "limit", "reason"}]
    evidence_strength(counts, rules) -> str         strong | moderate | weak
    rank_key(entry, rank_by) -> tuple
    money_text(amount, currency, fx) -> str         "INR 5,000.00 (USD 56.82)" or "USD 56.82"
    hypothesis(entry) / kill_rule(entry) -> str
    numbers(run) -> dict                            the 06_survivors.json content (files and graveyard written)
    check_one(run, pain_id) -> dict                 validate and compute one pain; nothing written
    render_md(result, run) -> str
    register(subparsers)                            adds `numbers [--check PAIN_ID]`

Assumed file shapes (stages 3 and 5 are written by other modules; these readers are tolerant):
    pains.json:  {"pains": [ {pain_id | room+pain_key, status, counts{record_count, money_mentions,
                 failed_spend_mentions}, spend_sources, verified_quotes | quotes[], ...} ]}  (a dict keyed by
                 pain_id is accepted too; count fields may also sit at the top level of a pain)
    05_pairs.json: {"survivors": [...]} or {"pains": [ {pain_id, status, lane, kept: PAIR} ]} or {"kept": [ids]}
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import common
import prices

STAGE = 6
CASES = ("low", "base", "high")
CHECKS = ("usd_per_hour", "cash30", "days_to_first_payment", "cohort_hours", "guarantee", "live_window")
EVIDENCE_ORDER = ("strong", "moderate", "weak")
BILLINGS = ("one_off", "monthly")
TRUST_LEVELS = ("high", "medium", "low")
REACH_KINDS = ("warm", "search")
DEFAULT_RANK_BY = ["opens_ladder", "days_to_first_payment", "usd_per_hour_base", "evidence_strength"]
DEAD_STATUSES = ("killed", "dropped", "cut", "invalid", "dead", "failed")
_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
_EPS = 1e-9

CHECK_MEANING = {
    "usd_per_hour": "in the base case an hour of the founder's time must earn at least the ledger's hour value (in USD, times the kill-rule factor)",
    "cash30": "the cash a customer pays in the first 30 days must cover what it costs to win them (cash plus founder time at the ledger's hour value)",
    "days_to_first_payment": "the first payment must arrive within the kill-rule limit (and within the ledger's runway when it has one)",
    "cohort_hours": "the first cohort's weekly hours (delivery plus acquisition) must fit the ledger's weekly hours",
    "guarantee": "the total refund exposure of the first cohort must fit the ledger's guarantee reserve",
    "live_window": "anything delivered live must fit the founder's evenings and weekends, India time",
}
CASE_MEANING = {
    "low": "low price, low conversion, slow and costly acquisition",
    "base": "the walker's base values",
    "high": "high price, high conversion, fast and cheap acquisition",
}
FORMULAS = {
    "price": "input (the walker's price for the case)",
    "price_total": "price x months (monthly) or price (one-off)",
    "reaches_per_sale": "1 / conversion",
    "acq_hours": "reaches_per_sale x minutes_per_reach / 60",
    "acq_cash": "reaches_per_sale x cash_per_reach",
    "acquisition_cost": "acq_cash + acq_hours x hour value",
    "net_cash": "price_total - delivery cash cost - acq_cash",
    "founder_hours": "delivery hours + acq_hours",
    "usd_per_hour": "(net_cash / founder_hours) / units of the currency per USD",
    "cash30": "price if payment_days_after_sale <= 30, else 0",
}
MONEY_FIELDS = ("price", "price_total", "acq_cash", "acquisition_cost", "net_cash", "cash30")
CSV_COLUMNS = [
    "pain_id", "case", "status", "rank", "currency", "price", "price_usd", "price_total", "price_total_usd",
    "reaches_per_sale", "acq_hours", "acq_cash", "acq_cash_usd", "acquisition_cost", "acquisition_cost_usd",
    "net_cash", "net_cash_usd", "founder_hours", "usd_per_hour", "cash30", "cash30_usd",
    "days_to_first_payment", "horizon_months", "cohort_hours_per_week", "guarantee_exposure",
    "guarantee_exposure_ledger", "anchor_ratio", "evidence", "opens_ladder", "failed_checks",
]


# --------------------------------------------------------------------------- small helpers
def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _text(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _r2(x):
    return None if x is None else round(float(x), 2)


def _r4(x):
    return None if x is None else round(float(x), 4)


def combine_tags(*tags) -> str:
    """A computed number is `measured` only if every input is measured; otherwise `estimate`."""
    return "measured" if tags and all(t == "measured" for t in tags) else "estimate"


def money_text(amount, currency: str, fx: dict) -> str:
    """"INR 5,000.00 (USD 56.82)"; plain "USD 56.82" for a USD room."""
    usd = common.to_usd(amount, currency, fx)
    if currency == "USD":
        return f"USD {float(amount):,.2f}"
    return f"{currency} {float(amount):,.2f} (USD {usd:,.2f})"


# --------------------------------------------------------------------------- Stage 3 pains (tolerant reader)
def load_pains(run) -> dict:
    """pain_id -> pain entry from RUN/03_listen/pains.json. {} when the file is missing."""
    p = common.listen_dir(run) / "pains.json"
    if not p.exists():
        return {}
    data = common.read_json(p)
    pains = data.get("pains") if isinstance(data, dict) else data
    items: list = []
    if isinstance(pains, dict):
        for k, v in pains.items():
            if isinstance(v, dict):
                items.append(dict(v, pain_id=v.get("pain_id") or k))
    elif isinstance(pains, list):
        items = [x for x in pains if isinstance(x, dict)]
    out: dict = {}
    for pain in items:
        pid = pain.get("pain_id")
        if not isinstance(pid, str) and pain.get("room") and pain.get("pain_key"):
            pid = f"{pain['room']}--{pain['pain_key']}"
        if isinstance(pid, str) and "--" in pid:
            out[pid] = pain
    return out


def pain_status(pain: dict) -> str:
    return str(pain.get("status") or "kept").lower()


def kept_pains(pains: dict) -> dict:
    return {pid: p for pid, p in pains.items() if pain_status(p) not in DEAD_STATUSES}


def pain_counts(pain) -> dict:
    """The evidence counts of a pain, whatever field names Stage 3 used."""
    pain = pain if isinstance(pain, dict) else {}
    scopes = [pain.get("counts") if isinstance(pain.get("counts"), dict) else {}, pain]

    def pick(*names, default=0):
        for scope in scopes:
            for n in names:
                v = scope.get(n)
                if isinstance(v, bool):
                    continue
                if _is_num(v):
                    return int(v)
                if isinstance(v, list):
                    return len(v)
        return default

    verified = pick("verified_quotes", "quotes_verified", "verified_quote_count", default=None)
    if verified is None:
        quotes = pain.get("quotes")
        verified = len(quotes) if isinstance(quotes, list) else 0
    return {
        "failed_spend": pick("failed_spend_mentions", "failed_spend"),
        "money": pick("money_mentions", "money"),
        "records": pick("record_count", "member_records", "member_record_count", "records"),
        "spend_sources": pick("spend_sources", "spend_source_count", "spend_domains"),
        "verified_quotes": int(verified),
    }


# --------------------------------------------------------------------------- Stage 5 survivors (tolerant reader)
def stage5_survivors(data, where: str = "05_pairs.json") -> dict:
    if not isinstance(data, dict):
        raise common.ValidationErrors([f"{where}: must be an object with a 'survivors' or 'pains' list."])
    items = None
    if isinstance(data.get("survivors"), list):
        items = data["survivors"]
    elif isinstance(data.get("pains"), dict):
        items = [dict(v, pain_id=v.get("pain_id") or k) if isinstance(v, dict) else k for k, v in data["pains"].items()]
    elif isinstance(data.get("pains"), list):
        items = data["pains"]
    elif isinstance(data.get("kept"), list):
        items = data["kept"]
    if items is None:
        raise common.ValidationErrors([f"{where}: needs a 'survivors', 'pains' or 'kept' list. Run `funnel pairs` again."])
    out: dict = {}
    for it in items:
        if isinstance(it, str):
            pid, entry = it, {"pain_id": it}
        elif isinstance(it, dict):
            pid, entry = it.get("pain_id"), it
        else:
            continue
        if not isinstance(pid, str) or "--" not in pid:
            continue
        if str(entry.get("status") or "kept").lower() in DEAD_STATUSES:
            continue
        out[pid] = entry
    return out


def load_stage5(run) -> dict:
    p = common.run_dir(run) / "05_pairs.json"
    common.require_file(p, "Run `funnel pairs` first.")
    return stage5_survivors(common.read_json(p), common.rel(p))


def stage5_pair(entry):
    """The kept pair of a Stage 5 entry, whatever key holds it."""
    if not isinstance(entry, dict):
        return None
    for key in ("kept", "pair", "kept_pair", "chosen", "best"):
        v = entry.get(key)
        if isinstance(v, dict) and (v.get("entry_walls") or v.get("hold_wall") or v.get("lane")):
            return v
    if entry.get("entry_walls") or entry.get("hold_wall"):
        return entry
    return None


def stage5_lane(entry):
    if not isinstance(entry, dict):
        return None
    if _text(entry.get("lane")):
        return entry["lane"]
    pair = stage5_pair(entry)
    if pair and _text(pair.get("lane")):
        return pair["lane"]
    return None


# --------------------------------------------------------------------------- ledger
def hour_value(ledger: dict, fx: dict) -> dict:
    """The founder's hour value from the ledger, in its currency and in USD."""
    cons = ledger.get("constraints") or {}
    hv = cons.get("hour_value") or {}
    value = hv.get("value")
    if not _is_num(value) or value <= 0:
        raise common.ValidationErrors(["config/ledger.yaml: constraints.hour_value.value must be a positive number."])
    cur = str(ledger.get("currency") or "INR").upper()
    return {"value": float(value), "currency": cur, "usd": common.to_usd(value, cur, fx),
            "assumed": bool(hv.get("assumed")), "tag": "ledger" + (", assumed" if hv.get("assumed") else "")}


def _ledger_limits(ledger: dict) -> dict:
    cons = ledger.get("constraints") or {}
    hpw = cons.get("hours_per_week") or {}
    use = hpw.get("use") if _is_num(hpw.get("use")) else hpw.get("low")
    runway = (cons.get("runway") or {}).get("runway_months")
    reserve = (cons.get("guarantee_reserve") or {}).get("value")
    window = ((ledger.get("practical_limits") or {}).get("live_delivery") or {}).get("window") or "evenings and weekends, IST"
    return {"hours_per_week": float(use) if _is_num(use) else None,
            "runway_months": float(runway) if _is_num(runway) else None,
            "reserve": float(reserve) if _is_num(reserve) else 0.0,
            "live_window": str(window)}


# --------------------------------------------------------------------------- validation
def _check_lbh(obj, where: str, lo=None, hi=None, exclusive_lo: bool = False) -> list:
    """A {"low", "base", "high", "reasoning"} block: numbers, ordered, within [lo, hi]."""
    if not isinstance(obj, dict):
        return [f"{where}: must be an object with low, base, high and reasoning."]
    errors = []
    vals = {}
    for k in ("low", "base", "high"):
        v = obj.get(k)
        if not _is_num(v):
            errors.append(f"{where}.{k}: must be a number (got {v!r}).")
            continue
        if lo is not None and (v < lo or (exclusive_lo and v <= lo)):
            errors.append(f"{where}.{k}: must be {'more than' if exclusive_lo else 'at least'} {lo} (got {v}).")
        if hi is not None and v > hi:
            errors.append(f"{where}.{k}: must be at most {hi} (got {v}).")
        vals[k] = v
    if len(vals) == 3 and not (vals["low"] <= vals["base"] <= vals["high"]):
        errors.append(f"{where}: low <= base <= high must hold (got {vals['low']}, {vals['base']}, {vals['high']}).")
    if not _text(obj.get("reasoning")):
        errors.append(f"{where}: missing 'reasoning'.")
    return errors


def validate_input(data, where: str, fx: dict) -> list:
    """Every problem with a 06_inputs file, in plain English. Empty when it is fine."""
    if not isinstance(data, dict):
        return [f"{where}: must be an object (see config/formats.md, Stage 6)."]
    errors: list = []
    cur = data.get("currency")
    if not isinstance(cur, str) or not _CURRENCY_RE.match(cur):
        errors.append(f"{where}: 'currency' must be a 3-letter ISO code like USD or INR (got {cur!r}).")
    elif cur not in fx:
        errors.extend(common.MissingCurrency(cur).errors)

    anchor = data.get("price_anchor")
    errors.extend(common.check_price(anchor, f"{where}: price_anchor"))
    errors.extend(common.check_judgment(anchor, f"{where}: price_anchor"))
    if isinstance(anchor, dict) and isinstance(anchor.get("currency"), str) and _CURRENCY_RE.match(anchor["currency"]) \
            and anchor["currency"] not in fx:
        errors.extend(common.MissingCurrency(anchor["currency"]).errors)
    if not _text(data.get("offer")):
        errors.append(f"{where}: 'offer' is missing (one line: what the customer gets).")

    price = data.get("price")
    errors.extend(_check_lbh(price, f"{where}: price", lo=0))
    if isinstance(price, dict):
        if price.get("billing") not in BILLINGS:
            errors.append(f"{where}: price.billing must be one_off or monthly (got {price.get('billing')!r}).")
        months = price.get("months")
        if not _is_int(months) or months < 1:
            errors.append(f"{where}: price.months must be a whole number from 1 (got {months!r}); use 1 for a one-off price.")
        pdays = price.get("payment_days_after_sale")
        if not _is_int(pdays) or pdays < 0:
            errors.append(f"{where}: price.payment_days_after_sale must be a whole number of days, 0 or more (got {pdays!r}).")
    errors.extend(_check_lbh(data.get("conversion_rate"), f"{where}: conversion_rate", lo=0, hi=1, exclusive_lo=True))
    acq = data.get("acquisition")
    if not isinstance(acq, dict):
        errors.append(f"{where}: 'acquisition' must be an object with minutes_per_reach and cash_per_reach.")
    else:
        errors.extend(_check_lbh(acq.get("minutes_per_reach"), f"{where}: acquisition.minutes_per_reach", lo=0))
        errors.extend(_check_lbh(acq.get("cash_per_reach"), f"{where}: acquisition.cash_per_reach", lo=0))

    deliv = data.get("delivery")
    if not isinstance(deliv, dict):
        errors.append(f"{where}: 'delivery' must be an object with my_hours_per_customer, cash_cost_per_customer, delivery_weeks and live.")
    else:
        for f, minimum, strict in (("my_hours_per_customer", 0, False), ("cash_cost_per_customer", 0, False), ("delivery_weeks", 0, True)):
            w = f"{where}: delivery.{f}"
            errs = common.check_number(deliv.get(f), w)
            errors.extend(errs)
            if not errs:
                v = deliv[f]["value"]
                if v < minimum or (strict and v <= minimum):
                    errors.append(f"{w}: 'value' must be {'more than' if strict else 'at least'} {minimum} (got {v}).")
        live = deliv.get("live")
        if not isinstance(live, dict):
            errors.append(f"{where}: delivery.live must be an object with value, fits_evenings_weekends_ist and reasoning.")
        else:
            for f in ("value", "fits_evenings_weekends_ist"):
                if not isinstance(live.get(f), bool):
                    errors.append(f"{where}: delivery.live.{f} must be true or false.")
            if not _text(live.get("reasoning")):
                errors.append(f"{where}: delivery.live: missing 'reasoning'.")

    chan = data.get("channel")
    if not isinstance(chan, dict):
        errors.append(f"{where}: 'channel' must be an object with name, where, reach_kind, trust, reasoning, confidence.")
    else:
        for f in ("name", "where"):
            if not _text(chan.get(f)):
                errors.append(f"{where}: channel.{f} is missing.")
        if chan.get("reach_kind") not in REACH_KINDS:
            errors.append(f"{where}: channel.reach_kind must be warm or search (got {chan.get('reach_kind')!r}).")
        if chan.get("trust") not in TRUST_LEVELS:
            errors.append(f"{where}: channel.trust must be high, medium or low (got {chan.get('trust')!r}).")
        errors.extend(common.check_judgment(chan, f"{where}: channel"))

    hz = data.get("revenue_horizon")
    if not isinstance(hz, dict):
        errors.append(f"{where}: 'revenue_horizon' must be an object with boredom_months and melt_months.")
    else:
        for f in ("boredom_months", "melt_months"):
            w = f"{where}: revenue_horizon.{f}"
            errs = common.check_number(hz.get(f), w, allow_null=True)
            errors.extend(errs)
            if not errs and hz[f].get("value") is not None and hz[f]["value"] <= 0:
                errors.append(f"{w}: 'value' must be more than 0 months, or null.")

    lt = data.get("ladder_test")
    if not isinstance(lt, dict):
        errors.append(f"{where}: 'ladder_test' must be an object with position, urgent and provable_outcome.")
    else:
        pos = lt.get("position")
        if not _is_int(pos) or pos < 1:
            errors.append(f"{where}: ladder_test.position must be a whole number from 1 (the step on the room's ladder).")
        if not isinstance(lt.get("urgent"), bool):
            errors.append(f"{where}: ladder_test.urgent must be true or false.")
        po = lt.get("provable_outcome")
        if not isinstance(po, dict):
            errors.append(f"{where}: ladder_test.provable_outcome must be an object with value, how, reasoning, confidence.")
        else:
            if not isinstance(po.get("value"), bool):
                errors.append(f"{where}: ladder_test.provable_outcome.value must be true or false.")
            if not _text(po.get("how")):
                errors.append(f"{where}: ladder_test.provable_outcome.how is missing.")
            errors.extend(common.check_judgment(po, f"{where}: ladder_test.provable_outcome"))

    ttfp = data.get("time_to_first_payment")
    if not isinstance(ttfp, dict):
        errors.append(f"{where}: 'time_to_first_payment' must be an object with days_to_first_conversation, days_to_close, build_days, reasoning.")
    else:
        for f in ("days_to_first_conversation", "days_to_close", "build_days"):
            v = ttfp.get(f)
            if not _is_int(v) or v < 0:
                errors.append(f"{where}: time_to_first_payment.{f} must be a whole number of days, 0 or more (got {v!r}).")
        if not _text(ttfp.get("reasoning")):
            errors.append(f"{where}: time_to_first_payment: missing 'reasoning'.")

    g = data.get("guarantee")
    if not isinstance(g, dict):
        errors.append(f"{where}: 'guarantee' must be an object with offered and refund_per_customer.")
    else:
        if not isinstance(g.get("offered"), bool):
            errors.append(f"{where}: guarantee.offered must be true or false.")
        r = g.get("refund_per_customer")
        if not _is_num(r) or r < 0:
            errors.append(f"{where}: guarantee.refund_per_customer must be a number, 0 or more, in the room's currency (got {r!r}).")

    t = data.get("test")
    if not isinstance(t, dict):
        errors.append(f"{where}: 'test' must be an object with n, who, how and days.")
    else:
        if not _is_int(t.get("n")) or t["n"] < 1:
            errors.append(f"{where}: test.n must be a whole number from 1 (how many people are reached).")
        for f in ("who", "how"):
            if not _text(t.get(f)):
                errors.append(f"{where}: test.{f} is missing.")
        if not _is_int(t.get("days")) or t["days"] < 1:
            errors.append(f"{where}: test.days must be a whole number from 1.")

    oq = data.get("open_questions")
    if not isinstance(oq, list) or not all(isinstance(q, str) for q in oq):
        errors.append(f"{where}: 'open_questions' must be a list of strings (use [] when there are none).")
    if data.get("confidence") not in common.CONFIDENCE_LEVELS:
        errors.append(f"{where}: 'confidence' must be high, moderate or low (got {data.get('confidence')!r}).")

    if not errors:
        hours = data["delivery"]["my_hours_per_customer"]["value"]
        minutes_low = data["acquisition"]["minutes_per_reach"]["low"]
        if hours <= 0 and minutes_low <= 0:
            errors.append(f"{where}: delivery.my_hours_per_customer and acquisition.minutes_per_reach cannot both be 0: "
                          f"the founder's time per customer must be above zero in every case.")
    return errors


# --------------------------------------------------------------------------- arithmetic
def case_inputs(data: dict, case: str) -> dict:
    price, conv, acq = data["price"], data["conversion_rate"], data["acquisition"]
    if case == "low":
        return {"price": price["low"], "conversion": conv["low"],
                "minutes_per_reach": acq["minutes_per_reach"]["high"], "cash_per_reach": acq["cash_per_reach"]["high"]}
    if case == "high":
        return {"price": price["high"], "conversion": conv["high"],
                "minutes_per_reach": acq["minutes_per_reach"]["low"], "cash_per_reach": acq["cash_per_reach"]["low"]}
    if case == "base":
        return {"price": price["base"], "conversion": conv["base"],
                "minutes_per_reach": acq["minutes_per_reach"]["base"], "cash_per_reach": acq["cash_per_reach"]["base"]}
    raise common.ValidationErrors([f"unknown case {case!r}; cases are low, base and high."])


def compute_case(data: dict, case: str, h_c: float, fx_c: float) -> dict:
    """Every per-case number in the room's currency (usd_per_hour in USD). Unrounded."""
    ci = case_inputs(data, case)
    price = data["price"]
    months = int(price["months"]) if price["billing"] == "monthly" else 1
    price_total = ci["price"] * months
    reaches_per_sale = 1.0 / ci["conversion"]
    acq_hours = reaches_per_sale * ci["minutes_per_reach"] / 60.0
    acq_cash = reaches_per_sale * ci["cash_per_reach"]
    acquisition_cost = acq_cash + acq_hours * h_c
    delivery_cash = float(data["delivery"]["cash_cost_per_customer"]["value"])
    delivery_hours = float(data["delivery"]["my_hours_per_customer"]["value"])
    net_cash = price_total - delivery_cash - acq_cash
    founder_hours = delivery_hours + acq_hours
    usd_per_hour = (net_cash / founder_hours) / fx_c
    cash30 = ci["price"] if int(price["payment_days_after_sale"]) <= 30 else 0.0
    return {
        "case": case,
        "inputs": ci,
        "price": float(ci["price"]),
        "price_total": float(price_total),
        "reaches_per_sale": reaches_per_sale,
        "acq_hours": acq_hours,
        "acq_cash": float(acq_cash),
        "acquisition_cost": float(acquisition_cost),
        "net_cash": float(net_cash),
        "founder_hours": founder_hours,
        "usd_per_hour": usd_per_hour,
        "cash30": float(cash30),
    }


def compute_pain(data: dict, rules: dict, ledger: dict, fx: dict) -> dict:
    """Every number for one validated input file: the three cases plus the per-pain figures."""
    s6 = rules.get("stage6") or {}
    hour = hour_value(ledger, fx)
    cur = data["currency"]
    fx_c = fx[cur] if cur != "USD" else 1.0
    h_c = common.from_usd(hour["usd"], cur, fx)
    cases = {c: compute_case(data, c, h_c, fx_c) for c in CASES}
    for c in cases.values():
        for f in MONEY_FIELDS:
            c[f + "_usd"] = common.to_usd(c[f], cur, fx)

    deliv = data["delivery"]
    hz = data["revenue_horizon"]
    horizon_parts = [hz[f]["value"] for f in ("boredom_months", "melt_months") if hz[f].get("value") is not None]
    horizon = min(horizon_parts) if horizon_parts else None
    ttfp = data["time_to_first_payment"]
    days = int(ttfp["days_to_first_conversation"]) + int(ttfp["days_to_close"]) + int(ttfp["build_days"])
    first_cohort = int(s6.get("first_cohort_customers", 5))
    delivery_hours = float(deliv["my_hours_per_customer"]["value"])
    delivery_weeks = float(deliv["delivery_weeks"]["value"])
    test_days = int(data["test"]["days"])
    cohort_hours = first_cohort * delivery_hours / delivery_weeks + first_cohort * cases["base"]["acq_hours"] / (test_days / 7.0)
    g = data["guarantee"]
    exposure = first_cohort * float(g["refund_per_customer"]) if g["offered"] else 0.0
    exposure_ledger = common.convert(exposure, cur, hour["currency"], fx)
    anchor = data["price_anchor"]
    anchor_usd = common.to_usd(anchor["amount"], anchor["currency"], fx)
    base_price_usd = cases["base"]["price_usd"]
    anchor_ratio = (base_price_usd / anchor_usd) if anchor_usd > 0 else None

    delivery_tags = [deliv[f]["tag"] for f in ("my_hours_per_customer", "cash_cost_per_customer", "delivery_weeks")]
    tags = {
        "price": "estimate", "price_total": "estimate", "reaches_per_sale": "estimate", "acq_hours": "estimate",
        "acq_cash": "estimate", "acquisition_cost": "estimate", "founder_hours": combine_tags(deliv["my_hours_per_customer"]["tag"], "estimate"),
        "net_cash": combine_tags("estimate", deliv["cash_cost_per_customer"]["tag"]), "usd_per_hour": "estimate", "cash30": "estimate",
        "days_to_first_payment": "estimate",
        "horizon_months": combine_tags(*[hz[f]["tag"] for f in ("boredom_months", "melt_months") if hz[f].get("value") is not None]) if horizon_parts else "estimate",
        "cohort_hours_per_week": combine_tags(*delivery_tags, "estimate"),
        "guarantee_exposure": "estimate",
        "anchor_ratio": combine_tags("estimate", "measured" if anchor.get("seen_via") == "page" else "estimate"),
    }
    return {
        "currency": cur,
        "fx_per_usd": fx_c,
        "hour_value": dict(hour, in_room_currency=h_c),
        "cases": cases,
        "horizon_months": horizon,
        "horizon_parts": {"boredom_months": hz["boredom_months"].get("value"), "melt_months": hz["melt_months"].get("value")},
        "days_to_first_payment": days,
        "days_parts": {f: int(ttfp[f]) for f in ("days_to_first_conversation", "days_to_close", "build_days")},
        "first_cohort": first_cohort,
        "cohort_hours_per_week": cohort_hours,
        "cohort_parts": {"delivery_hours": delivery_hours, "delivery_weeks": delivery_weeks, "acq_hours_base": cases["base"]["acq_hours"],
                         "test_days": test_days},
        "guarantee_exposure": exposure,
        "guarantee_exposure_usd": common.to_usd(exposure, cur, fx),
        "guarantee_exposure_ledger": exposure_ledger,
        "anchor_usd": anchor_usd,
        "anchor_ratio": anchor_ratio,
        "tags": tags,
    }


# --------------------------------------------------------------------------- checks
def run_checks(num: dict, data: dict, rules: dict, ledger: dict) -> dict:
    """The six base-case checks. Each: {"pass", "value", "limit", "reason"}."""
    s6 = rules.get("stage6") or {}
    lim = _ledger_limits(ledger)
    hour = num["hour_value"]
    base = num["cases"]["base"]
    cur = num["currency"]
    out: dict = {}

    factor = float(s6.get("min_usd_per_hour_vs_hour_value", 1.0))
    limit = hour["usd"] * factor
    v = base["usd_per_hour"]
    ok = v + _EPS >= limit
    out["usd_per_hour"] = {"pass": ok, "value": v, "limit": limit,
                           "reason": f"base case earns USD {v:,.2f} per founder hour; the ledger's hour value is USD {hour['usd']:,.2f}"
                                     + (f" x {factor:g} = USD {limit:,.2f}" if factor != 1.0 else "")}

    if bool(s6.get("cash30_must_cover_acquisition", True)):
        v, limit = base["cash30"], base["acquisition_cost"]
        ok = v + _EPS >= limit
        reason = (f"cash in the first 30 days per customer is {cur} {v:,.2f}; winning a customer costs {cur} {limit:,.2f} "
                  f"(cash {cur} {base['acq_cash']:,.2f} plus {base['acq_hours']:,.2f} founder hours at {cur} {hour['in_room_currency']:,.2f})")
        if v == 0 and int(data["price"]["payment_days_after_sale"]) > 30:
            reason += f"; nothing is paid within 30 days (payment {data['price']['payment_days_after_sale']} days after the sale)"
        out["cash30"] = {"pass": ok, "value": v, "limit": limit, "reason": reason}
    else:
        out["cash30"] = {"pass": True, "value": base["cash30"], "limit": None, "reason": "check switched off in kill_rules (cash30_must_cover_acquisition: false)"}

    max_days = float(s6.get("max_days_to_first_payment", 60))
    limit = max_days
    parts = [f"kill-rule limit {max_days:g} days"]
    if lim["runway_months"] is not None:
        runway_days = lim["runway_months"] * 30
        parts.append(f"runway {lim['runway_months']:g} months = {runway_days:g} days")
        limit = min(limit, runway_days)
    else:
        parts.append("the ledger has no runway limit")
    v = num["days_to_first_payment"]
    out["days_to_first_payment"] = {"pass": v <= limit + _EPS, "value": v, "limit": limit,
                                    "reason": f"first payment expected on day {v} (" + "; ".join(parts) + ")"}

    v = num["cohort_hours_per_week"]
    limit = lim["hours_per_week"]
    if limit is None:
        out["cohort_hours"] = {"pass": True, "value": v, "limit": None, "reason": "the ledger gives no weekly hours; not checked"}
    else:
        out["cohort_hours"] = {"pass": v <= limit + _EPS, "value": v, "limit": limit,
                               "reason": f"the first cohort of {num['first_cohort']} customers needs {v:,.2f} founder hours a week; "
                                         f"the ledger allows {limit:g}"}

    if bool(s6.get("guarantee_exposure_within_reserve", True)):
        v, limit = num["guarantee_exposure_ledger"], lim["reserve"]
        out["guarantee"] = {"pass": v <= limit + _EPS, "value": v, "limit": limit,
                            "reason": (f"refund exposure of the first cohort is {hour['currency']} {v:,.2f}; the reserve is "
                                       f"{hour['currency']} {limit:,.2f}") if data["guarantee"]["offered"] else "no guarantee is offered"}
    else:
        out["guarantee"] = {"pass": True, "value": num["guarantee_exposure_ledger"], "limit": None,
                            "reason": "check switched off in kill_rules (guarantee_exposure_within_reserve: false)"}

    live = data["delivery"]["live"]
    if bool(s6.get("live_delivery_must_fit_window", True)):
        if not live["value"]:
            out["live_window"] = {"pass": True, "value": False, "limit": None, "reason": "nothing is delivered live"}
        elif live["fits_evenings_weekends_ist"]:
            out["live_window"] = {"pass": True, "value": True, "limit": None, "reason": f"live delivery fits {lim['live_window']}"}
        else:
            out["live_window"] = {"pass": False, "value": True, "limit": None,
                                  "reason": f"live delivery does not fit {lim['live_window']} (the walker says so)"}
    else:
        out["live_window"] = {"pass": True, "value": bool(live["value"]), "limit": None,
                              "reason": "check switched off in kill_rules (live_delivery_must_fit_window: false)"}
    return out


# --------------------------------------------------------------------------- evidence and ranking
def evidence_strength(counts: dict, rules: dict) -> str:
    labels = ((rules.get("stage6") or {}).get("evidence_labels") or {})
    strong = labels.get("strong") or {}
    moderate = labels.get("moderate") or {}
    fs, rc = counts.get("failed_spend", 0), counts.get("records", 0)
    ss, money = counts.get("spend_sources", 0), counts.get("money", 0)
    if (fs >= int(strong.get("failed_spend_min", 3)) and rc >= int(strong.get("member_records_min", 30))
            and ss >= int(strong.get("spend_sources_min", 2))):
        return "strong"
    if ((fs >= int(moderate.get("failed_spend_min", 1)) or money >= int(moderate.get("or_money_min", 3)))
            and rc >= int(moderate.get("member_records_min", 15))):
        return "moderate"
    return "weak"


def rank_key(entry: dict, rank_by) -> tuple:
    key: list = []
    for name in rank_by:
        if name == "opens_ladder":
            key.append(0 if entry["opens_ladder"] else 1)
        elif name == "days_to_first_payment":
            key.append(entry["days_to_first_payment"])
        elif name == "usd_per_hour_base":
            key.append(-float(entry["cases"]["base"]["usd_per_hour"]))
        elif name == "evidence_strength":
            key.append(EVIDENCE_ORDER.index(entry["evidence"]))
    c = entry["counts"]
    key += [-c["failed_spend"], -c["money"], -c["verified_quotes"], -c["records"], entry["pain_id"]]
    return tuple(key)


# --------------------------------------------------------------------------- sentences
def price_sentence(entry: dict, fx: dict) -> str:
    text = money_text(entry["cases"]["base"]["price"], entry["currency"], fx)
    if entry["billing"] == "monthly":
        text += " a month"
    return text


def hypothesis(entry: dict) -> str:
    t = entry["test"]
    return (f"At least 1 of {t['n']} {t['who']}, reached {t['how']}, will pay {entry['price_text']} "
            f"for {entry['offer']} within {t['days']} days.")


def kill_rule(entry: dict) -> str:
    t = entry["test"]
    return (f"Kill it if fewer than 1 of the {t['n']} pays {entry['price_text']} within {t['days']} days of the first message. "
            f"Decide on day {t['days']}. No extensions.")


# --------------------------------------------------------------------------- one pain
def _rounded_case(c: dict) -> dict:
    out = {"inputs": {k: _r4(v) for k, v in c["inputs"].items()}}
    for k, v in c.items():
        if k in ("case", "inputs"):
            continue
        out[k] = _r2(v) if (k in MONEY_FIELDS or k.endswith("_usd") or k == "usd_per_hour") else _r4(v)
    return out


def evaluate(pid: str, data: dict, rules: dict, ledger: dict, fx: dict, pain=None, stage5_entry=None) -> dict:
    """Numbers, checks, evidence and sentences for one validated pain. Nothing written."""
    num = compute_pain(data, rules, ledger, fx)
    checks = run_checks(num, data, rules, ledger)
    failed = [c for c in CHECKS if not checks[c]["pass"]]
    counts = pain_counts(pain) if pain else {"failed_spend": 0, "money": 0, "records": 0, "spend_sources": 0, "verified_quotes": 0}
    s6 = rules.get("stage6") or {}
    max_pos = int(s6.get("opens_ladder_max_position", 1))
    position = int(data["ladder_test"]["position"])
    room, key = common.split_pain_id(pid)
    entry = {
        "pain_id": pid,
        "room": room,
        "pain_key": key,
        "status": "killed" if failed else "survived",
        "rank": None,
        "lane": stage5_lane(stage5_entry),
        "currency": num["currency"],
        "fx_per_usd": num["fx_per_usd"],
        "billing": data["price"]["billing"],
        "months": int(data["price"]["months"]),
        "payment_days_after_sale": int(data["price"]["payment_days_after_sale"]),
        "offer": common.normalize_ws(data["offer"]),
        "channel": {k: data["channel"].get(k) for k in ("name", "where", "reach_kind", "trust")},
        "test": {"n": int(data["test"]["n"]), "who": common.normalize_ws(data["test"]["who"]),
                 "how": common.normalize_ws(data["test"]["how"]), "days": int(data["test"]["days"])},
        "ladder_position": position,
        "opens_ladder": position <= max_pos,
        "urgent": bool(data["ladder_test"]["urgent"]),
        "provable_outcome": bool(data["ladder_test"]["provable_outcome"]["value"]),
        "live": bool(data["delivery"]["live"]["value"]),
        "guarantee_offered": bool(data["guarantee"]["offered"]),
        "evidence": evidence_strength(counts, rules) if pain else "weak",
        "evidence_counts_found": pain is not None,
        "counts": counts,
        "cases": {c: _rounded_case(num["cases"][c]) for c in CASES},
        "hour_value": {"value": num["hour_value"]["value"], "currency": num["hour_value"]["currency"],
                       "usd": _r4(num["hour_value"]["usd"]), "in_room_currency": _r4(num["hour_value"]["in_room_currency"]),
                       "assumed": num["hour_value"]["assumed"], "tag": num["hour_value"]["tag"]},
        "horizon_months": num["horizon_months"],
        "horizon_parts": num["horizon_parts"],
        "days_to_first_payment": num["days_to_first_payment"],
        "days_parts": num["days_parts"],
        "first_cohort": num["first_cohort"],
        "cohort_hours_per_week": _r4(num["cohort_hours_per_week"]),
        "cohort_parts": num["cohort_parts"],
        "guarantee_exposure": _r2(num["guarantee_exposure"]),
        "guarantee_exposure_usd": _r2(num["guarantee_exposure_usd"]),
        "guarantee_exposure_ledger": _r2(num["guarantee_exposure_ledger"]),
        "anchor": {"what": data["price_anchor"].get("what"), "price_text": data["price_anchor"].get("price_text"),
                   "amount": data["price_anchor"].get("amount"), "currency": data["price_anchor"].get("currency"),
                   "url": data["price_anchor"].get("url"), "seen_via": data["price_anchor"].get("seen_via"),
                   "amount_usd": _r2(num["anchor_usd"]), "price_status": None, "price_tag": None},
        "anchor_ratio": _r4(num["anchor_ratio"]),
        "tags": num["tags"],
        "checks": {c: {"pass": checks[c]["pass"], "value": _r4(checks[c]["value"]) if _is_num(checks[c]["value"]) else checks[c]["value"],
                       "limit": _r4(checks[c]["limit"]), "reason": checks[c]["reason"]} for c in CHECKS},
        "failed_checks": failed,
        "open_questions": [common.normalize_ws(q) for q in data.get("open_questions") or []],
        "confidence": data.get("confidence"),
        "reasoning": {
            "price": data["price"].get("reasoning"),
            "conversion_rate": data["conversion_rate"].get("reasoning"),
            "minutes_per_reach": data["acquisition"]["minutes_per_reach"].get("reasoning"),
            "cash_per_reach": data["acquisition"]["cash_per_reach"].get("reasoning"),
            "delivery_hours": data["delivery"]["my_hours_per_customer"].get("reasoning"),
            "delivery_cash": data["delivery"]["cash_cost_per_customer"].get("reasoning"),
            "delivery_weeks": data["delivery"]["delivery_weeks"].get("reasoning"),
            "live": data["delivery"]["live"].get("reasoning"),
            "channel": data["channel"].get("reasoning"),
            "time_to_first_payment": data["time_to_first_payment"].get("reasoning"),
            "provable_outcome": data["ladder_test"]["provable_outcome"].get("reasoning"),
        },
        "delivery": {"hours": float(data["delivery"]["my_hours_per_customer"]["value"]),
                     "hours_tag": data["delivery"]["my_hours_per_customer"]["tag"],
                     "cash": float(data["delivery"]["cash_cost_per_customer"]["value"]),
                     "cash_tag": data["delivery"]["cash_cost_per_customer"]["tag"],
                     "weeks": float(data["delivery"]["delivery_weeks"]["value"]),
                     "weeks_tag": data["delivery"]["delivery_weeks"]["tag"]},
    }
    entry["price_text"] = price_sentence(entry, fx)
    entry["hypothesis"] = hypothesis(entry)
    entry["kill_rule"] = kill_rule(entry)
    entry["_unrounded"] = num
    return entry


def _strip_private(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if not k.startswith("_")}


# --------------------------------------------------------------------------- the command
def inputs_dir(run) -> Path:
    return common.run_dir(run) / "06_inputs"


def check_one(run, pid: str) -> dict:
    """Validate and compute one pain from its 06_inputs file. Raises ValidationErrors; writes nothing."""
    common.split_pain_id(pid)
    p = inputs_dir(run) / f"{pid}.json"
    common.require_file(p, "The walker writes it in mode numbers (see config/formats.md, Stage 6).")
    rules = common.load_kill_rules()
    ledger = common.load_ledger()
    fx = common.load_fx(run)
    data = common.read_json(p)
    errors = validate_input(data, common.rel(p), fx)
    if not errors and data.get("pain_id") != pid:
        errors.append(f"{common.rel(p)}: 'pain_id' must be {pid} (got {data.get('pain_id')!r}).")
    if errors:
        raise common.ValidationErrors(errors)
    pains = load_pains(run)
    stage5 = {}
    if (common.run_dir(run) / "05_pairs.json").exists():
        try:
            stage5 = load_stage5(run)
        except common.FunnelError:
            stage5 = {}
    return evaluate(pid, data, rules, ledger, fx, pains.get(pid), stage5.get(pid))


def numbers(run) -> dict:
    rd = common.run_dir(run)
    rules = common.load_kill_rules()
    s6 = rules.get("stage6") or {}
    ledger = common.load_ledger()
    fx = common.load_fx(run)
    fx_file = common.read_fx_file(run)
    hour = hour_value(ledger, fx)
    pains = load_pains(run)
    survivors5 = load_stage5(run)
    idir = inputs_dir(run)

    missing: list = []
    errors: list = []
    loaded: dict = {}
    for pid in sorted(survivors5):
        p = idir / f"{pid}.json"
        if not p.exists():
            missing.append(pid)
            continue
        data = common.read_json(p)
        errs = validate_input(data, common.rel(p), fx)
        if not errs and data.get("pain_id") != pid:
            errs.append(f"{common.rel(p)}: 'pain_id' must be {pid} (got {data.get('pain_id')!r}).")
        errors.extend(errs)
        loaded[pid] = data
    if missing:
        raise common.MissingInput(f"{len(missing)} Stage 5 survivor(s) have no 06_inputs file: "
                                  + ", ".join(f"{common.rel(idir)}/{pid}.json" for pid in missing)
                                  + ". A funnel-walker in mode numbers writes each one.")
    if errors:
        raise common.ValidationErrors(errors)
    extra = sorted(p.stem for p in idir.glob("*.json")) if idir.exists() else []
    extra = [s for s in extra if s not in survivors5]

    notes: list = []
    warnings: list = []
    entries: list = []
    for pid in sorted(loaded):
        pain = pains.get(pid)
        if pain is None:
            notes.append(f"{pid}: no entry in 03_listen/pains.json, so its evidence counts are unknown; "
                         f"evidence labeled weak (conservative).")
        entries.append(evaluate(pid, loaded[pid], rules, ledger, fx, pain, survivors5.get(pid)))
    for s in extra:
        warnings.append(f"06_inputs/{s}.json is not a Stage 5 survivor; ignored.")

    # price anchors through the price checker (offline -> [measured, page not checked])
    checked = prices.check_items(run, STAGE, "numbers", [(f"{e['pain_id']} price_anchor", loaded[e["pain_id"]]["price_anchor"]) for e in entries])
    by_where = {r["where"]: r for r in checked["items"]}
    for e in entries:
        r = by_where[f"{e['pain_id']} price_anchor"]
        e["anchor"]["price_status"] = r["status"]
        e["anchor"]["price_tag"] = r["tag"]
        e["anchor"]["price_detail"] = r["detail"]

    max_keep = int(s6.get("max_survivors", 5))
    if max_keep < 1:
        raise common.ValidationErrors(["kill_rules.yaml: stage6.max_survivors must be at least 1."])
    rank_by = [str(x) for x in (s6.get("rank_by") or DEFAULT_RANK_BY)]
    survivors = sorted((e for e in entries if not e["failed_checks"]), key=lambda e: rank_key(e, rank_by))
    for i, e in enumerate(survivors, 1):
        e["rank"] = i
        e["status"] = "kept" if i <= max_keep else "cut"
    killed = sorted((e for e in entries if e["failed_checks"]), key=lambda e: e["pain_id"])
    kept = [e for e in survivors if e["status"] == "kept"]
    cut = [e for e in survivors if e["status"] == "cut"]

    date = common.run_date(run)
    for e in killed:
        reason = "numbers fail in the base case: " + "; ".join(f"{c}: {e['checks'][c]['reason']}" for c in e["failed_checks"])
        common.append_graveyard(date, STAGE, f"pain:{e['pain_id']}", reason)
    for e in cut:
        reason = (f"cut: ranked {e['rank']} of {len(survivors)} survivors and max_survivors is {max_keep}; passed every check "
                  f"(opens ladder {'yes' if e['opens_ladder'] else 'no'}, first payment day {e['days_to_first_payment']}, "
                  f"USD {e['cases']['base']['usd_per_hour']:,.2f} per hour, evidence {e['evidence']})")
        common.append_graveyard(date, STAGE, f"pain:{e['pain_id']}", reason)

    for n in notes:
        common.log_event(run, STAGE, "numbers", "note", note=n, review=True)
    for w in warnings:
        common.log_event(run, STAGE, "numbers", "note", note=w, review=False)

    result = {
        "run": common.run_name(run),
        "max_survivors": max_keep,
        "rank_by": rank_by,
        "first_cohort_customers": int(s6.get("first_cohort_customers", 5)),
        "hour_value": {"value": hour["value"], "currency": hour["currency"], "usd": _r4(hour["usd"]), "assumed": hour["assumed"]},
        "fx_as_of": fx_file.get("as_of"),
        "counts": {"in": len(entries), "survived": len(survivors), "kept": len(kept), "cut": len(cut), "killed": len(killed)},
        "kept": [e["pain_id"] for e in kept],
        "cut": [e["pain_id"] for e in cut],
        "killed": [e["pain_id"] for e in killed],
        "pains": [_strip_private(e) for e in kept + cut + killed],
        "notes": notes,
        "warnings": warnings,
        "price_check": {"counts": checked["counts"], "blocked_domains": checked["blocked_domains"]},
        "check_meaning": CHECK_MEANING,
        "case_meaning": CASE_MEANING,
        "formulas": FORMULAS,
    }
    common.write_json(rd / "06_survivors.json", result)
    write_csv(rd / "06_numbers.csv", result)
    common.write_text(rd / "06_numbers.md", render_md(result, run, fx))
    common.log_event(run, STAGE, "numbers", "count", pains_in=len(entries), survived=len(survivors), kept=len(kept),
                     cut=len(cut), killed=len(killed), max_survivors=max_keep,
                     failed_by_check={c: sum(1 for e in killed if c in e["failed_checks"]) for c in CHECKS})
    return result


# --------------------------------------------------------------------------- files
def write_csv(path, result: dict) -> None:
    rows = []
    for e in result["pains"]:
        for case in CASES:
            c = e["cases"][case]
            rows.append({
                "pain_id": e["pain_id"], "case": case, "status": e["status"], "rank": e["rank"] if e["rank"] is not None else "",
                "currency": e["currency"],
                "price": c["price"], "price_usd": c["price_usd"], "price_total": c["price_total"], "price_total_usd": c["price_total_usd"],
                "reaches_per_sale": c["reaches_per_sale"], "acq_hours": c["acq_hours"], "acq_cash": c["acq_cash"],
                "acq_cash_usd": c["acq_cash_usd"], "acquisition_cost": c["acquisition_cost"],
                "acquisition_cost_usd": c["acquisition_cost_usd"], "net_cash": c["net_cash"], "net_cash_usd": c["net_cash_usd"],
                "founder_hours": c["founder_hours"], "usd_per_hour": c["usd_per_hour"], "cash30": c["cash30"], "cash30_usd": c["cash30_usd"],
                "days_to_first_payment": e["days_to_first_payment"],
                "horizon_months": "" if e["horizon_months"] is None else e["horizon_months"],
                "cohort_hours_per_week": e["cohort_hours_per_week"], "guarantee_exposure": e["guarantee_exposure"],
                "guarantee_exposure_ledger": e["guarantee_exposure_ledger"],
                "anchor_ratio": "" if e["anchor_ratio"] is None else e["anchor_ratio"],
                "evidence": e["evidence"], "opens_ladder": "yes" if e["opens_ladder"] else "no",
                "failed_checks": ";".join(e["failed_checks"]),
            })
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def _cell(s) -> str:
    return common.normalize_ws(str(s if s is not None else "")).replace("|", "/")


def _money(amount, cur: str, fx: dict) -> str:
    return money_text(amount, cur, fx)


def _hours(x) -> str:
    return f"{float(x):,.2f} h"


def render_entry(e: dict, fx: dict, first_cohort: int) -> list:
    cur = e["currency"]
    hv = e["hour_value"]
    lines = []
    status = {"kept": f"kept, rank {e['rank']}", "cut": f"cut for rank ({e['rank']})", "killed": "killed"}[e["status"]]
    lines += [f"## {e['pain_id']} ({status})", ""]
    lines.append(f"- Room `{e['room']}`, pain `{e['pain_key']}`. Lane: {e['lane'] or 'not given'}. Currency: {cur}"
                 + (f" ({e['fx_per_usd']:,.4f} per USD)" if cur != "USD" else "") + ".")
    lines.append(f"- Offer: {_cell(e['offer'])}")
    lines.append(f"- Channel: {_cell(e['channel'].get('name'))} ({e['channel'].get('reach_kind')} reach, trust {e['channel'].get('trust')}) "
                 f"at {_cell(e['channel'].get('where'))}.")
    lines.append(f"- Hypothesis: {e['hypothesis']}")
    lines.append(f"- Kill rule: {e['kill_rule']}")
    c = e["counts"]
    ev = (f"- Evidence: **{e['evidence']}** (failed spend {c['failed_spend']}, money mentions {c['money']}, member records "
          f"{c['records']}, spend sources {c['spend_sources']}, verified quotes {c['verified_quotes']})")
    if not e.get("evidence_counts_found", True):
        ev += " [thin: counts not found in pains.json]"
    lines.append(ev + ".")
    a = e["anchor"]
    anchor_line = (f"- Price anchor: {_cell(a.get('what'))}: {_cell(a.get('price_text'))} ({a.get('currency')} {a.get('amount')}, "
                   f"USD {a['amount_usd']:,.2f}) {a.get('price_tag') or ''} <{a.get('url')}>. ")
    if e["anchor_ratio"] is None:
        anchor_line += "Anchor ratio: not computable (anchor amount is 0)."
    else:
        anchor_line += f"Our base price is {e['anchor_ratio']:.2f} x the anchor [{e['tags']['anchor_ratio']}]."
    lines.append(anchor_line)
    lines.append(f"- Founder hour value: {hv['currency']} {hv['value']:,.2f} = USD {hv['usd']:,.2f}"
                 + (f" = {cur} {hv['in_room_currency']:,.2f}" if cur != hv["currency"] else "") + f" [{hv['tag']}].")
    lines += ["", "### Inputs (the walker's judgment)", "", "| Input | Low case | Base case | High case | Tag |", "|---|---|---|---|---|"]
    cases = e["cases"]

    def ci(name):
        return [cases[k]["inputs"][name] for k in CASES]

    lines.append("| price | " + " | ".join(_money(v, cur, fx) for v in ci("price")) + f" | estimate |")
    lines.append("| conversion (share of people reached who buy) | " + " | ".join(f"{v:.4f}" for v in ci("conversion")) + " | estimate |")
    lines.append("| minutes per reach | " + " | ".join(f"{v:g}" for v in ci("minutes_per_reach")) + " | estimate |")
    lines.append("| cash per reach | " + " | ".join(_money(v, cur, fx) for v in ci("cash_per_reach")) + " | estimate |")
    d = e["delivery"]
    lines.append(f"| delivery hours per customer | {_hours(d['hours'])} | {_hours(d['hours'])} | {_hours(d['hours'])} | {d['hours_tag']} |")
    lines.append(f"| delivery cash cost per customer | {_money(d['cash'], cur, fx)} | {_money(d['cash'], cur, fx)} | {_money(d['cash'], cur, fx)} | {d['cash_tag']} |")
    lines.append(f"| delivery weeks | {d['weeks']:g} | {d['weeks']:g} | {d['weeks']:g} | {d['weeks_tag']} |")
    billing = "monthly, " + f"{e['months']} months" if e["billing"] == "monthly" else "one-off"
    lines.append(f"| billing | {billing} | {billing} | {billing} | estimate |")
    lines.append(f"| payment days after sale | {e['payment_days_after_sale']} | {e['payment_days_after_sale']} | {e['payment_days_after_sale']} | estimate |")
    lines += ["", f"### Numbers per case (in {cur}, USD in brackets)", "",
              "| Number | Formula | Low | Base | High | Tag |", "|---|---|---|---|---|---|"]
    for name in ("price", "price_total", "reaches_per_sale", "acq_hours", "acq_cash", "acquisition_cost", "net_cash", "founder_hours",
                 "usd_per_hour", "cash30"):
        vals = []
        for k in CASES:
            v = cases[k][name]
            if name in MONEY_FIELDS:
                vals.append(_money(v, cur, fx))
            elif name in ("acq_hours", "founder_hours"):
                vals.append(_hours(v))
            elif name == "usd_per_hour":
                vals.append(f"USD {v:,.2f}/h")
            else:
                vals.append(f"{v:,.2f}")
        lines.append(f"| {name} | {FORMULAS[name]} | " + " | ".join(vals) + f" | {e['tags'][name]} |")
    lines += ["", "### Numbers per pain", "", "| Number | Formula | Value | Tag |", "|---|---|---|---|"]
    dp = e["days_parts"]
    lines.append(f"| days_to_first_payment | first conversation {dp['days_to_first_conversation']} + close {dp['days_to_close']} + build "
                 f"{dp['build_days']} | {e['days_to_first_payment']} days | {e['tags']['days_to_first_payment']} |")
    hp = e["horizon_parts"]
    hz = "none" if e["horizon_months"] is None else f"{e['horizon_months']:g} months"
    lines.append(f"| horizon_months | min(boredom {hp['boredom_months'] if hp['boredom_months'] is not None else 'none'}, "
                 f"melt {hp['melt_months'] if hp['melt_months'] is not None else 'none'}) | {hz} | {e['tags']['horizon_months']} |")
    cp = e["cohort_parts"]
    lines.append(f"| cohort_hours_per_week | {first_cohort} x {cp['delivery_hours']:g} h / {cp['delivery_weeks']:g} weeks + {first_cohort} x "
                 f"{cp['acq_hours_base']:,.2f} h / ({cp['test_days']} days / 7) | {e['cohort_hours_per_week']:,.2f} h/week | "
                 f"{e['tags']['cohort_hours_per_week']} |")
    lines.append(f"| guarantee_exposure | {first_cohort} x refund per customer | {_money(e['guarantee_exposure'], cur, fx)}"
                 + (f" = {hv['currency']} {e['guarantee_exposure_ledger']:,.2f}" if cur != hv["currency"] else "")
                 + f" | {e['tags']['guarantee_exposure']} |")
    lines.append(f"| anchor_ratio | base price / anchor, both in USD | "
                 f"{'not computable' if e['anchor_ratio'] is None else f'{e['anchor_ratio']:.2f}'} | {e['tags']['anchor_ratio']} |")
    lines += ["", "### Checks (base case)", "", "| Check | Result | Why |", "|---|---|---|"]
    for name in CHECKS:
        ch = e["checks"][name]
        lines.append(f"| {name} | {'pass' if ch['pass'] else 'FAIL'} | {_cell(ch['reason'])} |")
    base = cases["base"]
    reading = (f"In the base case each customer pays {_money(base['price_total'], cur, fx)} in total. Winning one customer takes "
               f"{base['reaches_per_sale']:,.1f} people reached, {base['acq_hours']:,.2f} founder hours and {_money(base['acq_cash'], cur, fx)} in cash. "
               f"After delivery costs, {_money(base['net_cash'], cur, fx)} is left per customer for {base['founder_hours']:,.2f} founder hours: "
               f"USD {base['usd_per_hour']:,.2f} per hour against the ledger's USD {hv['usd']:,.2f}. "
               f"The low case gives USD {cases['low']['usd_per_hour']:,.2f} per hour and the high case USD {cases['high']['usd_per_hour']:,.2f}. "
               f"First payment expected on day {e['days_to_first_payment']}.")
    if e["failed_checks"]:
        reading += " Killed: " + ", ".join(e["failed_checks"]) + " failed."
    elif e["status"] == "cut":
        reading += f" Passed every check but ranked {e['rank']}; only the top {first_cohort and ''}{e.get('_max', '')}".rstrip() + " survivors are kept."
        reading = reading.replace("only the top  survivors", "only the top survivors")
    else:
        reading += " Passed every check."
    lines += ["", "### Reading", "", reading]
    if e["open_questions"]:
        lines += ["", "Open questions: " + " ".join(f"({i}) {q}" for i, q in enumerate(e["open_questions"], 1))]
    lines.append(f"Overall confidence: {e['confidence']}.")
    return lines


def render_md(result: dict, run, fx=None) -> str:
    fx = fx if fx is not None else common.load_fx(run)
    c = result["counts"]
    hv = result["hour_value"]
    lines = ["# Stage 6: numbers", "", f"Run: {result.get('run') or common.run_name(run)}.",
             f"{c['in']} Stage 5 survivor(s) priced. {c['survived']} passed every check. {c['kept']} kept (at most {result['max_survivors']}), "
             f"{c['cut']} cut for rank, {c['killed']} killed.", "",
             "Every figure is computed by the script from the walker's judged inputs, the ledger and the run's exchange rates. "
             "`[measured]` = from stored data or a cited page. `[estimate]` = reasoned; treat it as a guess with stated assumptions.",
             f"Founder hour value: {hv['currency']} {hv['value']:,.2f} = USD {hv['usd']:,.2f}"
             + (" (the ledger marks it [assumed])" if hv.get("assumed") else "") + f". Exchange rates as of {result.get('fx_as_of')}.",
             "", "Cases:", ""]
    lines += [f"- **{k}**: {v}." for k, v in CASE_MEANING.items()]
    lines += ["", "Checks (all must pass in the base case):", ""]
    lines += [f"- **{k}**: {v}." for k, v in CHECK_MEANING.items()]
    lines += ["", f"Survivors are ranked by {', '.join(result['rank_by'])}, then failed spend, money mentions, verified quotes, member records, pain id. "
              f"Evidence strength: strong = many failed-spend mentions, many member records and prices seen at two or more sources; "
              f"moderate = some money or failed-spend mentions and a fair number of records; weak = the rest.", ""]
    lines += [f"## Ranking ({c['kept']} kept, {c['cut']} cut)", ""]
    ranked = [e for e in result["pains"] if e["status"] in ("kept", "cut")]
    if ranked:
        lines += ["| Rank | Pain | Status | Opens ladder | First payment | USD/hour (low / base / high) | Evidence | Lane |",
                  "|---|---|---|---|---|---|---|---|"]
        for e in ranked:
            cs = e["cases"]
            lines.append(f"| {e['rank']} | {e['pain_id']} | {e['status']} | {'yes' if e['opens_ladder'] else 'no'} (step {e['ladder_position']}) | "
                         f"day {e['days_to_first_payment']} | {cs['low']['usd_per_hour']:,.2f} / {cs['base']['usd_per_hour']:,.2f} / "
                         f"{cs['high']['usd_per_hour']:,.2f} | {e['evidence']} | {e['lane'] or '-'} |")
    else:
        lines.append("No pain passed every check.")
    lines += ["", f"## Killed ({c['killed']})", ""]
    killed = [e for e in result["pains"] if e["status"] == "killed"]
    if killed:
        lines += ["| Pain | Failed checks | Why |", "|---|---|---|"]
        for e in killed:
            why = "; ".join(f"{k}: {e['checks'][k]['reason']}" for k in e["failed_checks"])
            lines.append(f"| {e['pain_id']} | {', '.join(e['failed_checks'])} | {_cell(why)} |")
    else:
        lines.append("None.")
    for e in result["pains"]:
        lines.append("")
        e2 = dict(e, _max=result["max_survivors"])
        lines += render_entry(e2, fx, result.get("first_cohort_customers", 5))
    if result.get("notes") or result.get("warnings"):
        lines += ["", "## Notes", ""]
        lines += [f"- {n}" for n in result.get("notes") or []]
        lines += [f"- {w}" for w in result.get("warnings") or []]
    pc = result.get("price_check") or {}
    if pc.get("blocked_domains"):
        lines += ["", "Domains to allow so the price-anchor pages can be opened: " + ", ".join(pc["blocked_domains"]) + "."]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- CLI
def _print_entry(e: dict) -> None:
    cs = e["cases"]
    print(f"{e['pain_id']}: {e['currency']}, evidence {e['evidence']}, opens ladder {'yes' if e['opens_ladder'] else 'no'}, "
          f"first payment day {e['days_to_first_payment']}.")
    print(f"  USD per hour: low {cs['low']['usd_per_hour']:,.2f}, base {cs['base']['usd_per_hour']:,.2f}, high {cs['high']['usd_per_hour']:,.2f} "
          f"(ledger hour value USD {e['hour_value']['usd']:,.2f}).")
    print(f"  Base case: price {e['price_text']}, acquisition cost {e['currency']} {cs['base']['acquisition_cost']:,.2f}, "
          f"cash in 30 days {e['currency']} {cs['base']['cash30']:,.2f}, cohort {e['cohort_hours_per_week']:,.2f} h/week.")
    for name in CHECKS:
        ch = e["checks"][name]
        print(f"  {'pass' if ch['pass'] else 'FAIL'} {name}: {ch['reason']}")
    print(f"  Hypothesis: {e['hypothesis']}")
    print(f"  Kill rule: {e['kill_rule']}")


def cmd_numbers(args) -> int:
    run = common.run_dir(args.run)
    if args.check:
        e = check_one(run, args.check)
        print(f"{common.rel(inputs_dir(run) / (args.check + '.json'))}: valid.")
        _print_entry(e)
        if e["failed_checks"]:
            print(f"Would be killed by `funnel numbers`: {', '.join(e['failed_checks'])} failed in the base case.")
        else:
            print("Passes every base-case check. Nothing was written.")
        common.log_event(run, STAGE, "numbers", "check", pain=args.check, failed_checks=e["failed_checks"],
                         usd_per_hour_base=e["cases"]["base"]["usd_per_hour"])
        return 0
    result = numbers(run)
    c = result["counts"]
    print(f"Numbers: {c['in']} pains in, {c['survived']} passed, {c['kept']} kept (max {result['max_survivors']}), "
          f"{c['cut']} cut, {c['killed']} killed.")
    for e in result["pains"]:
        if e["status"] == "kept":
            print(f"  kept #{e['rank']}: {e['pain_id']} (USD {e['cases']['base']['usd_per_hour']:,.2f}/h base, first payment day "
                  f"{e['days_to_first_payment']}, opens ladder {'yes' if e['opens_ladder'] else 'no'}, evidence {e['evidence']})")
    for e in result["pains"]:
        if e["status"] == "cut":
            print(f"  cut #{e['rank']}: {e['pain_id']}")
    for e in result["pains"]:
        if e["status"] == "killed":
            print(f"  killed: {e['pain_id']}: failed {', '.join(e['failed_checks'])}")
    for n in result["notes"]:
        print(f"review: {n}")
    for w in result["warnings"]:
        print(f"warning: {w}")
    if result["price_check"]["blocked_domains"]:
        print("Domains to allow for price-anchor pages: " + ", ".join(result["price_check"]["blocked_domains"]))
    print(f"Wrote {common.rel(run / '06_survivors.json')}, {common.rel(run / '06_numbers.csv')}, "
          f"{common.rel(run / '06_numbers.md')} and graveyard.md")
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("numbers", help="Compute every Stage 6 figure, apply the base-case checks, rank and keep survivors.")
    p.add_argument("--check", metavar="PAIN_ID", default=None, help="validate and compute one pain's 06_inputs file; write nothing")
    p.set_defaults(func=cmd_numbers)
