"""The price checker (rule 8: a `[measured]` price must come from a page we can cite).

A price item looks like {"what", "price_text", "amount", "currency", "unit", "url", "seen_via"}.
The checker opens the page only when `seen_via` is "page". A price seen in a
web-search result (`seen_via: "search"`) is never fetched; it is reported as
`seen_via_search` and shown as `[measured, page not checked]`. When the network
is blocked (FUNNEL_OFFLINE=1 or the proxy refuses the domain) the status is
`blocked_by_network` and the price is kept as `[measured, page not checked]`.
Only a page that was opened and does not contain the price text gives `not_found`.

Public API
----------
    STATUSES                          every status the checker can give
    tag_for(status) -> str            "[measured]" | "[measured, page not checked]" | "[not found on page]"
    counts_as_spend(status) -> bool   every status except not_found and invalid
    check_item(item, where) -> dict   one price item -> {"where", "url", "domain", "price_text", "seen_via",
                                      "status", "tag", "detail"}
    check_items(run, stage, command, items) -> dict
        items: list of (where, item). Returns {"items": [...], "counts": {status: n}, "blocked_domains": [...]}
        and logs one `blocked` event per blocked domain plus a `check` event. Stages call this.
    collect_items(run, stage) -> list[(where, item)]
        stage 2: spend items of 02_mask_input.json (or the merged parts);
        stage 3: alternatives in every room's pains_draft.json; stage 6: price_anchor of 06_inputs/*.json
    output_path(run, stage) -> Path   RUN/price_check_stage<N>.json
    price_check(run, stage, command="price-check") -> dict   collect, check, write the file
    register(subparsers)              adds `price-check --stage 2|3|6`
"""
from __future__ import annotations

from pathlib import Path

import common
import netfetch

STATUSES = ("found", "not_found", "seen_via_search", "blocked_by_network", "robots_disallowed", "fetch_error", "invalid")
TAG_MEASURED = "[measured]"
TAG_NOT_CHECKED = "[measured, page not checked]"
TAG_NOT_FOUND = "[not found on page]"


def tag_for(status: str) -> str:
    if status == "found":
        return TAG_MEASURED
    if status == "not_found":
        return TAG_NOT_FOUND
    return TAG_NOT_CHECKED


def counts_as_spend(status: str) -> bool:
    """A price counts as spend evidence unless the page was opened and the price was not on it."""
    return status not in ("not_found", "invalid")


def _no_spaces(s: str) -> str:
    return "".join(common.normalize_ws(s).split())


def _page_contains(page_text: str, price_text: str) -> tuple:
    """(True, how) when the price text appears on the page (whitespace-normalized, then ignoring spaces)."""
    page = common.normalize_ws(page_text)
    price = common.normalize_ws(price_text)
    if not price:
        return False, "the price text is empty"
    if price in page:
        return True, "price text found on the page word for word"
    if _no_spaces(price) in _no_spaces(page):
        return True, "price text found on the page (ignoring spaces)"
    return False, "the page was opened but the price text is not on it"


def check_item(item, where: str) -> dict:
    """Check one price item. Never raises for network trouble; the status says what happened."""
    out = {
        "where": where,
        "url": item.get("url") if isinstance(item, dict) else None,
        "domain": common.domain_of(item.get("url")) if isinstance(item, dict) and item.get("url") else "",
        "price_text": item.get("price_text") if isinstance(item, dict) else None,
        "seen_via": item.get("seen_via") if isinstance(item, dict) else None,
        "status": "invalid",
        "tag": TAG_NOT_CHECKED,
        "detail": "",
    }
    errors = common.check_price(item, where)
    if errors:
        out["status"] = "invalid"
        out["detail"] = " ".join(errors)
        out["tag"] = TAG_NOT_CHECKED
        return out
    if item["seen_via"] == "search":
        out["status"] = "seen_via_search"
        out["detail"] = "price read in a web-search result; the page was not opened"
    else:
        try:
            result = netfetch.fetch(item["url"])
            text = netfetch.html_to_text(result.get("text") or "")
            ok, how = _page_contains(text, item["price_text"])
            out["status"] = "found" if ok else "not_found"
            out["detail"] = how + (" (from cache)" if result.get("from_cache") else "")
        except netfetch.NetworkBlocked as e:
            out["status"] = "blocked_by_network"
            out["detail"] = f"the network blocks {e.domain}; the page was not opened"
        except netfetch.RobotsDisallowed:
            out["status"] = "robots_disallowed"
            out["detail"] = f"robots.txt on {out['domain']} does not allow opening this page"
        except netfetch.FetchError as e:
            out["status"] = "fetch_error"
            out["detail"] = f"the page could not be opened ({e})"
    out["tag"] = tag_for(out["status"])
    return out


def check_items(run, stage: int, command: str, items) -> dict:
    """Check every (where, item) pair in order. Logs blocked domains and a check event."""
    results = [check_item(item, where) for where, item in items]
    counts = {s: 0 for s in STATUSES}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    blocked = sorted({r["domain"] for r in results if r["status"] == "blocked_by_network" and r["domain"]})
    for domain in blocked:
        common.log_event(run, stage, command, "blocked", domain=domain,
                         note=f"price page on {domain} not opened; price kept as {TAG_NOT_CHECKED}")
    common.log_event(run, stage, command, "check", what="price-check", items=len(results),
                     counts={k: v for k, v in counts.items() if v}, blocked_domains=blocked)
    return {"items": results, "counts": {k: v for k, v in counts.items() if v}, "blocked_domains": blocked}


# --------------------------------------------------------------------------- what each stage holds
def _list(obj, key):
    v = obj.get(key) if isinstance(obj, dict) else None
    return v if isinstance(v, list) else []


def _stage2_items(run) -> list:
    rd = common.run_dir(run)
    merged = rd / "02_mask_input.json"
    if merged.exists():
        data = common.read_json(merged)
    else:
        import stage2  # local import: stage2 imports this module

        parts_dir = rd / "02_mask.parts"
        if not parts_dir.exists():
            raise common.MissingInput(f"{common.rel(merged)} is missing and there are no parts in "
                                      f"{common.rel(parts_dir)}/. Write the Stage 2 parts first.")
        data = stage2.merge_parts(run)
    items = []
    for room in _list(data, "rooms"):
        slug = room.get("slug", "?") if isinstance(room, dict) else "?"
        for i, item in enumerate(_list(room, "spend"), 1):
            items.append((f"room {slug} spend item {i}", item))
    return items


def _stage3_items(run) -> list:
    ldir = common.listen_dir(run) / "rooms"
    items = []
    if not ldir.exists():
        raise common.MissingInput(f"{common.rel(ldir)}/ is missing. No room has a pains_draft.json yet.")
    for draft in sorted(ldir.glob("*/pains_draft.json")):
        room = draft.parent.name
        data = common.read_json(draft)
        for pain in _list(data, "pains"):
            key = pain.get("pain_key", "?") if isinstance(pain, dict) else "?"
            for i, item in enumerate(_list(pain, "alternatives"), 1):
                items.append((f"{room}--{key} alternative {i}", item))
    return items


def _stage6_items(run) -> list:
    d = common.run_dir(run) / "06_inputs"
    if not d.exists():
        raise common.MissingInput(f"{common.rel(d)}/ is missing. The walkers write 06_inputs/<pain-id>.json.")
    items = []
    for p in sorted(d.glob("*.json")):
        data = common.read_json(p)
        anchor = data.get("price_anchor") if isinstance(data, dict) else None
        if anchor is not None:
            items.append((f"{p.stem} price_anchor", anchor))
    return items


def collect_items(run, stage: int) -> list:
    if stage == 2:
        return _stage2_items(run)
    if stage == 3:
        return _stage3_items(run)
    if stage == 6:
        return _stage6_items(run)
    raise common.ValidationErrors([f"--stage must be 2, 3 or 6 (got {stage!r})."])


def output_path(run, stage: int) -> Path:
    return common.run_dir(run) / f"price_check_stage{stage}.json"


def price_check(run, stage: int, command: str = "price-check") -> dict:
    items = collect_items(run, stage)
    checked = check_items(run, stage, command, items)
    result = {"stage": stage, "items": checked["items"], "counts": checked["counts"],
              "blocked_domains": checked["blocked_domains"],
              "tags": {"found": TAG_MEASURED, "not_found": TAG_NOT_FOUND, "other": TAG_NOT_CHECKED}}
    common.write_json(output_path(run, stage), result)
    return result


# --------------------------------------------------------------------------- command
def cmd_price_check(args) -> int:
    run = common.run_dir(args.run)
    result = price_check(run, args.stage)
    items = result["items"]
    print(f"Stage {args.stage}: {len(items)} price item(s) checked.")
    for r in items:
        print(f"- {r['where']}: {r['price_text']!s} at {r['url']} -> {r['status']} {r['tag']}. {r['detail']}")
    if result["counts"]:
        print("Counts: " + ", ".join(f"{k} {v}" for k, v in sorted(result["counts"].items())))
    if result["blocked_domains"]:
        print("Domains to allow so these pages can be checked: " + ", ".join(result["blocked_domains"]))
    print(f"Wrote {common.rel(output_path(run, args.stage))}")
    invalid = [r for r in items if r["status"] == "invalid"]
    if invalid:
        raise common.ValidationErrors([f"{r['where']}: {r['detail']}" for r in invalid])
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("price-check", help="Check every price item of a stage against its page (seen_via page only).")
    p.add_argument("--stage", type=int, required=True, choices=(2, 3, 6), help="2 = mask spend, 3 = pain alternatives, 6 = price anchors")
    p.set_defaults(func=cmd_price_check)  # the stage for the run log is --stage itself
