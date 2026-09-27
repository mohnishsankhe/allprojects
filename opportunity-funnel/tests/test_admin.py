import json

import pytest
import yaml

import admin
import common

ROOM = "gre-engineers-india"
ASSUMED_LINES = (5, 9, 37, 39, 40, 47, 48, 49, 53, 60, 63)


def _ledger_md(froot):
    return froot / "config" / "ledger.md"


def _ledger_yaml(froot):
    return froot / "config" / "ledger.yaml"


# =========================================================================== ledger check
def test_ledger_check_passes_on_the_real_config(froot):
    r = admin.ledger_check()
    assert r["ok"] is True and r["errors"] == []
    assert r["texts_checked"] >= 30
    assert [a["line"] for a in r["assumed"]] == list(ASSUMED_LINES)
    assert r["assumed"][-1]["text"].startswith("[assumed] Ambitious students")
    assert r["not_mentioned_walls"] == ["W21", "W23", "W24", "W26", "W28"]
    assert r["counts"] == {"depth": 8, "exclusions": 2, "existing_ventures": 5, "reach.search": 1, "reach.warm": 5,
                           "supply.can_be": 4, "supply.can_rent": 3}
    assert r["warnings"] == []


def test_ledger_check_detects_text_drift(froot, run, cli):
    # `run` creates runs/2026-09-26: ledger-check logs into a run folder that exists and never creates one
    md = _ledger_md(froot)
    text = md.read_text(encoding="utf-8")
    assert "Value of one of my hours: ₹1,500." in text
    md.write_text(text.replace("Value of one of my hours: ₹1,500.", "Value of one of my hours: ₹2,000."), encoding="utf-8")
    r = admin.ledger_check()
    assert r["ok"] is False and len(r["errors"]) == 1
    assert r["errors"][0].startswith("config/ledger.yaml: constraints.hour_value.text: this text is not in config/ledger.md word for word")
    out = cli("ledger-check")
    assert out.returncode == 1
    assert "Fix these: 1 item" in out.stderr and "constraints.hour_value.text" in out.stderr
    assert "1 text fields checked" not in out.stdout and "problem(s), listed below" in out.stdout
    events = common.read_jsonl(froot / "runs" / "2026-09-26" / "runlog.jsonl")
    assert any(e["kind"] == "check" and e["command"] == "ledger-check" and e["ok"] is False for e in events)
    # whitespace differences alone are fine
    md.write_text(text.replace("Value of one of my hours: ₹1,500.", "Value  of one\tof my hours:   ₹1,500."), encoding="utf-8")
    assert admin.ledger_check()["ok"] is True


def test_ledger_check_lists_every_assumed_line(froot, cli):
    out = cli("ledger-check")
    assert out.returncode == 0, out.stderr
    assert "[assumed] items (11; they go to REVIEW.md):" in out.stdout
    for n in ASSUMED_LINES:
        assert f"  - line {n}: " in out.stdout
    assert "line 63: [assumed] Ambitious students and young professionals" in out.stdout
    assert "Human walls the ledger does not mention (treated as not supplied): W21, W23, W24, W26, W28." in out.stdout
    md = _ledger_md(froot)
    md.write_text(md.read_text(encoding="utf-8") + "\n## Extra\n- I also own a boat. [assumed: unverified]\n", encoding="utf-8")
    r = admin.ledger_check()
    assert r["ok"] is True and len(r["assumed"]) == 12 and r["assumed"][-1]["text"] == "I also own a boat. [assumed: unverified]"
    assert any("12 [assumed] line(s) but ledger.yaml marks 11" in w for w in r["warnings"])


def test_ledger_check_structural_errors(froot, cli):
    p = _ledger_yaml(froot)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    data["reach"]["warm"][1]["id"] = "w1"                      # duplicate id
    data["supply"]["can_be"][0]["wall"] = "W7"                 # machine wall in supply
    data["supply"]["can_rent"][0]["wall"] = "W99"              # unknown wall
    data["constraints"]["hours_per_week"]["use"] = 20          # outside low..high
    data["constraints"]["hour_value"]["value"] = 0
    data["depth"][0]["strength"] = "huge"
    del data["geography"]
    p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    r = admin.ledger_check()
    assert r["ok"] is False
    err = "\n".join(r["errors"])
    for needle in ("id 'w1' is also used at", "wall W7 is a machine wall", "wall 'W99' is not in config/walls.md",
                   "hours_per_week.use must lie between low and high", "hour_value.value must be a positive number",
                   "'strength' must be strong, moderate or weak", "section 'geography' is missing"):
        assert needle in err, needle
    out = cli("ledger-check")
    assert out.returncode == 1 and "7. " in out.stderr
    p.unlink()
    out = cli("ledger-check")
    assert out.returncode == 2 and "ledger.yaml is missing" in out.stderr


def test_text_fields_walks_nested_structures():
    tree = {"a": {"text": "one", "b": [{"text": "two"}, {"c": {"text": "three"}}]}, "text": "zero", "d": "text"}
    assert admin.text_fields(tree) == [("a.text", "one"), ("a.b[0].text", "two"), ("a.b[1].c.text", "three"), ("text", "zero")]


# =========================================================================== source decisions
def test_source_decision_updates_table_row_and_decision_log(froot, cli):
    p = froot / "config" / "sources.md"
    before = admin.parse_sources_table(p.read_text(encoding="utf-8"))
    r = cli("source-decision", "--source", "hackernews", "--status", "allowed", "--reason",
            "API terms read: public data, attribution asked | fine", "--url", "https://hn.algolia.com/api")
    assert r.returncode == 0, r.stderr
    assert "Table row 'Hacker News (Algolia search API)': status allowed, checked 2026-09-26 (updated)." in r.stdout
    text = p.read_text(encoding="utf-8")
    after = admin.parse_sources_table(text)
    assert len(after["rows"]) == len(before["rows"]) and after["header"] == before["header"]
    hn = next(row for row in after["rows"] if row["cells"][0].startswith("Hacker News"))
    cols = after["columns"]
    assert hn["cells"][cols["status"]] == "allowed" and hn["cells"][cols["checked"]] == "2026-09-26"
    assert hn["cells"][cols["decision and reason"]] == "API terms read: public data, attribution asked / fine"
    assert len(hn["cells"]) == len(after["header"])
    log_line = "- 2026-09-26 | hackernews | allowed | API terms read: public data, attribution asked / fine | https://hn.algolia.com/api"
    assert text.rstrip().endswith(log_line)
    # other rows untouched
    se = next(row for row in after["rows"] if row["cells"][0].startswith("Stack Exchange"))
    assert se["cells"][cols["status"]] == "blocked-by-network"
    # rerun: nothing duplicated
    r = cli("source-decision", "--source", "hackernews", "--status", "allowed", "--reason",
            "API terms read: public data, attribution asked | fine", "--url", "https://hn.algolia.com/api")
    assert r.returncode == 0 and "Already logged" in r.stdout and "already up to date" in r.stdout
    assert p.read_text(encoding="utf-8").count(log_line) == 1
    # a per-domain decision with no table row only goes to the log
    r = cli("source-decision", "--source", "forum.example.org", "--status", "skip", "--reason", "terms forbid bots")
    assert r.returncode == 0 and "No table row matches 'forum.example.org'" in r.stdout
    assert "- 2026-09-26 | forum.example.org | skip | terms forbid bots | (no URL given)" in p.read_text(encoding="utf-8")
    assert len(admin.parse_sources_table(p.read_text(encoding="utf-8"))["rows"]) == len(before["rows"])
    r = cli("source-decision", "--source", "hackernews", "--status", "maybe", "--reason", "x")
    assert r.returncode == 2  # argparse rejects an unknown status
    r = cli("source-decision", "--source", "inbox", "--status", "skip", "--reason", "x")
    assert r.returncode == 1 and "matches 2 table rows" in r.stderr
    events = common.read_jsonl(froot / "runs" / "2026-09-26" / "runlog.jsonl")
    assert sum(1 for e in events if e["kind"] == "source" and e["command"] == "source-decision") == 3


def test_sources_domains_and_keys_are_read_from_the_table(froot):
    text = (froot / "config" / "sources.md").read_text(encoding="utf-8")
    domains = admin.sources_domains(text)
    for d in ("api.stackexchange.com", "hn.algolia.com", "www.reddit.com", "oauth.reddit.com", "www.googleapis.com",
              "itunes.apple.com", "data.commoncrawl.org", "commoncrawl.s3.amazonaws.com"):
        assert d in domains
    assert "none" not in domains
    assert admin.sources_keys(text) == ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT", "STACKEXCHANGE_KEY", "YOUTUBE_API_KEY"]


# =========================================================================== init and preflight
def test_init_creates_folders_and_never_prints_keys(froot, cli):
    import shutil

    shutil.rmtree(froot / "inbox")
    r = cli("init", env={"YOUTUBE_API_KEY": "SECRET-VALUE-123"})
    assert r.returncode == 0, r.stderr
    for d in ("inbox/closed_groups", "inbox/customers", "inbox/audit_results", "runs", "cache"):
        assert (froot / d).is_dir()
    assert "created: inbox/closed_groups, inbox/customers, inbox/audit_results" in r.stdout
    assert "ledger-check passes" in r.stdout and "11 [assumed] items" in r.stdout
    assert "API keys set (names only): YOUTUBE_API_KEY." in r.stdout
    assert "SECRET-VALUE-123" not in r.stdout + r.stderr
    (froot / "config" / "ledger.md").unlink()
    r = cli("init")
    assert r.returncode == 0 and "config/ledger.md is missing" in r.stdout


def test_preflight_snapshots_config_checks_ledger_and_lists_blocked_domains(froot, run, cli):
    r = cli("preflight", "--run", "2026-09-26", env={"STACKEXCHANGE_KEY": "abc-secret"})
    assert r.returncode == 0, r.stderr
    snap = run / "config_snapshot"
    assert sorted(p.name for p in snap.iterdir()) == sorted(p.name for p in (froot / "config").iterdir())
    assert (snap / "ledger.md").read_bytes() == (froot / "config" / "ledger.md").read_bytes()
    assert "every one appears word for word" in r.stdout
    assert "API keys set (names only): STACKEXCHANGE_KEY." in r.stdout and "abc-secret" not in r.stdout
    assert "Domains to allow (exact list): " in r.stdout
    report = json.loads((run / "preflight.json").read_text(encoding="utf-8"))
    assert report["ledger_ok"] is True and report["keys"]["STACKEXCHANGE_KEY"] is True and report["keys"]["YOUTUBE_API_KEY"] is False
    assert all(d["status"] == "blocked_by_network" and d["detail"] == "FUNNEL_OFFLINE=1" for d in report["domains"])
    assert "api.stackexchange.com" in report["domains_to_allow"] and "hn.algolia.com" in report["domains_to_allow"]
    assert report["domains_to_allow"] == sorted(report["domains_to_allow"])
    events = common.read_jsonl(run / "runlog.jsonl")
    blocked = [e["domain"] for e in events if e["kind"] == "blocked" and e["command"] == "preflight"]
    assert blocked == report["domains_to_allow"]
    # --network-only: no snapshot, no ledger check
    r = cli("preflight", "--network-only", "--run", "2026-09-20")
    assert r.returncode == 0, r.stderr
    assert not (froot / "runs" / "2026-09-20" / "config_snapshot").exists()
    assert "text fields checked" not in r.stdout and "Domains probed:" in r.stdout
    # a drifted ledger makes preflight exit 1 after reporting
    md = froot / "config" / "ledger.md"
    md.write_text(md.read_text(encoding="utf-8").replace("No runway pressure", "Some runway pressure"), encoding="utf-8")
    r = cli("preflight", "--run", "2026-09-26")
    assert r.returncode == 1 and "constraints.runway.text" in r.stderr and "Domains probed:" in r.stdout


# =========================================================================== loop-init, rooms-known, graveyard
def _old_run(froot, name, room, kept=True, fx_as_of="2026-09-22"):
    rd = froot / "runs" / name
    rd.mkdir(parents=True, exist_ok=True)
    common.write_json(rd / "01_rooms.json", {"rooms": [{"slug": room, "name": f"Room {room}", "lens": "transition",
                                                        "origin": "generated", "ladder": [], "status": "kept"}]})
    common.write_json(rd / "02_mask.json", {"max_rooms": 15, "rank_by": ["ladder_steps"],
                                           "rooms": [{"slug": room, "name": f"Room {room}", "status": "kept" if kept else "killed",
                                                      "rank": 1 if kept else None, "failed_tests": [] if kept else ["reach"]}],
                                           "kept": [room] if kept else [], "killed": [] if kept else [room]})
    common.write_json(rd / "fx_rates.json", {"base": "USD", "as_of": fx_as_of, "rates": {"INR": {"per_usd": 88.0}}})
    return rd


def test_loop_init_copies_room_from_latest_run_that_kept_it(froot, cli):
    _old_run(froot, "2026-09-10", ROOM, fx_as_of="2026-09-01")
    _old_run(froot, "2026-09-20", ROOM)
    _old_run(froot, "2026-09-24", ROOM, kept=False)  # later run killed it: not a source
    _old_run(froot, "2026-09-25", "other-room")
    r = cli("loop-init", "--room", ROOM)
    assert r.returncode == 0, r.stderr
    assert f"RUN: runs/2026-09-26-loop-{ROOM}" in r.stdout and "copied from run 2026-09-20" in r.stdout
    new = froot / "runs" / f"2026-09-26-loop-{ROOM}"
    rooms = json.loads((new / "01_rooms.json").read_text(encoding="utf-8"))
    assert rooms["rooms"][0]["slug"] == ROOM and rooms["source_run"] == "2026-09-20" and rooms["loop_room"] == ROOM
    mask = json.loads((new / "02_mask.json").read_text(encoding="utf-8"))
    assert mask["kept"] == [ROOM] and mask["rooms"][0]["status"] == "kept"
    assert (new / "config_snapshot" / "ledger.yaml").exists()
    assert (new / "fx_rates.json").exists() and "copied from 2026-09-20 (4 days old)" in r.stdout
    events = common.read_jsonl(new / "runlog.jsonl")
    assert any(e["command"] == "loop-init" and e["source_run"] == "2026-09-20" for e in events)
    # rerun gives the same files
    first = (new / "01_rooms.json").read_bytes()
    assert cli("loop-init", "--room", ROOM).returncode == 0 and (new / "01_rooms.json").read_bytes() == first
    # stale fx is not copied
    r = cli("loop-init", "--room", "other-room")
    assert r.returncode == 0 and "refresh the rates" not in r.stdout  # 2026-09-25 run's fx is 4 days old: copied
    (froot / "runs" / "2026-09-25" / "fx_rates.json").write_text(
        json.dumps({"base": "USD", "as_of": "2026-08-01", "rates": {}}), encoding="utf-8")
    import shutil

    shutil.rmtree(froot / "runs" / "2026-09-26-loop-other-room")
    r = cli("loop-init", "--room", "other-room")
    assert r.returncode == 0 and "is 56 days old; refresh the rates" in r.stdout
    assert not (froot / "runs" / "2026-09-26-loop-other-room" / "fx_rates.json").exists()


def test_loop_init_refuses_dead_or_unknown_rooms(froot, cli):
    _old_run(froot, "2026-09-20", ROOM)
    r = cli("loop-init", "--room", "never-kept")
    assert r.returncode == 2 and "No run kept room never-kept" in r.stderr
    common.append_graveyard("2026-09-21", 3, f"room:{ROOM}", "no pains survived")
    r = cli("loop-init", "--room", ROOM)
    assert r.returncode == 1 and f"room {ROOM} is dead in graveyard.md (2026-09-21, stage 3: no pains survived)" in r.stderr
    gy = froot / "graveyard.md"
    gy.write_text(gy.read_text(encoding="utf-8") + "  - new evidence 2026-09-25: three customers asked, see inbox/customers\n", encoding="utf-8")
    r = cli("loop-init", "--room", ROOM)
    assert r.returncode == 0, r.stderr
    r = cli("loop-init", "--room", "../evil")
    assert r.returncode == 1 and "not a valid slug" in r.stderr


def test_rooms_known_and_graveyard_commands(froot, cli):
    r = cli("rooms-known")
    assert r.returncode == 0 and "No run has a 02_mask.json yet" in r.stdout
    _old_run(froot, "2026-09-20", ROOM)
    _old_run(froot, "2026-09-25", "other-room")
    common.append_graveyard("2026-09-21", 3, f"room:{ROOM}", "no pains survived")
    common.append_graveyard("2026-09-21", 2, "room:zzz", "dead")
    gy = froot / "graveyard.md"
    gy.write_text(gy.read_text(encoding="utf-8").replace("room:zzz | dead", "room:zzz | dead\n  - new evidence 2026-09-22: a new thread"), encoding="utf-8")
    r = cli("rooms-known")
    assert r.returncode == 0, r.stderr
    lines = [ln for ln in r.stdout.splitlines() if ln.startswith("  ")]
    assert lines[0].startswith("  other-room") and "run 2026-09-25" in lines[0]
    assert lines[1].startswith(f"  {ROOM}") and "[graveyard: dead]" in lines[1]
    r = cli("graveyard")
    assert r.returncode == 0
    assert "Graveyard: 2 entries, 1 dead, 1 revived." in r.stdout
    assert f"2026-09-21 | stage 3 | room:{ROOM} | no pains survived [dead]" in r.stdout
    assert "room:zzz | dead [revived]" in r.stdout and "new evidence 2026-09-22: a new thread" in r.stdout


# =========================================================================== log, robots, purge
def test_log_command_writes_events(run, cli):
    r = cli("log", "--stage", "3", "--note", "kept undated records", "--review", "--run", "2026-09-26")
    assert r.returncode == 0 and "marked for REVIEW.md" in r.stdout
    r = cli("log", "--stage", "6", "--cost", "about 2.50 USD for 40 calls", "--run", "2026-09-26")
    assert r.returncode == 0
    r = cli("log", "--stage", "2", "--error", "agent timed out", "--run", "2026-09-26")
    assert r.returncode == 0
    events = [e for e in common.read_jsonl(run / "runlog.jsonl") if e["command"] == "log"]
    assert [(e["kind"], e["stage"], e["text"], e["review"]) for e in events] == [
        ("note", 3, "kept undated records", True), ("cost", 6, "about 2.50 USD for 40 calls", False), ("error", 2, "agent timed out", False)]
    assert events[1]["amount"] == 2.5 and events[1]["tag"] == "estimate"
    r = cli("log", "--stage", "3", "--run", "2026-09-26")
    assert r.returncode == 2  # one of --error/--note/--cost is required
    r = cli("log", "--stage", "3", "--note", "a", "--error", "b", "--run", "2026-09-26")
    assert r.returncode == 2


def test_robots_offline_exits_3_naming_the_domain(run, cli):
    r = cli("robots", "https://forum.test/thread/1", "--run", "2026-09-26")
    assert r.returncode == 3 and "Blocked: 1 item" in r.stderr and "cannot reach forum.test" in r.stderr
    r = cli("robots", "not a url", "--run", "2026-09-26")
    assert r.returncode == 1


def test_robots_reads_cached_rules_without_the_network(froot, run, cli):
    cache = froot / "cache" / "robots" / "forum.test.txt"
    cache.parent.mkdir(parents=True)
    cache.write_text("User-agent: *\nDisallow: /private/\n", encoding="utf-8")
    r = cli("robots", "https://forum.test/private/x", "--run", "2026-09-26")
    assert r.returncode == 0 and "NOT allowed" in r.stdout and "cache/robots/forum.test.txt" in r.stdout
    r = cli("robots", "https://forum.test/public/x", "--run", "2026-09-26")
    assert r.returncode == 0 and ": allowed for user agent" in r.stdout


def test_purge_expired_by_fetched_at(run, h, cli):
    def rec(i, fetched):
        r = h.make_record(f"https://r.test/{i}", f"record number {i} with some words")
        if fetched:
            r["meta"]["fetched_at"] = fetched
        return r

    h.store(run, ROOM, [rec(1, "2026-08-01T10:00:00+00:00"), rec(2, "2026-09-20T10:00:00+00:00"), rec(3, None)], source="reddit")
    h.store(run, ROOM, [rec(4, "2026-08-01T10:00:00+00:00")], source="websearch")
    h.store(run, "other-room", [rec(5, "2026-01-01T00:00:00+00:00")], source="reddit")
    r = cli("purge-expired", "--source", "reddit", "--days", "30", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "fetched before 2026-08-27 (30 days): 2 removed." in r.stdout
    assert f"  {ROOM}: 3 before, 1 removed, 2 kept (1 without meta.fetched_at, kept)." in r.stdout
    assert "Rerun `funnel batches" in r.stdout
    import records

    left = records.load_records(run, ROOM)
    assert sorted(x["url"] for x in left) == ["https://r.test/2", "https://r.test/3", "https://r.test/4"]
    assert records.load_records(run, "other-room") == []  # the file with no rows left is removed
    assert not records.source_file(run, "other-room", "reddit").exists()
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["command"] == "purge-expired" and e["dropped"] == 2 for e in events)


# =========================================================================== show, excerpt, listen-status
TEXT = "GRE   coaching:\n\n  “worth it”?  I paid ₹30,000 and\tstill scored 305 — waste of money."


def test_show_prints_records_in_full_and_flags_missing_ids(run, h, cli):
    out = h.store(run, ROOM, [h.make_record("https://forum.test/t/1", TEXT, date="2025-03-04"),
                              h.make_record("https://forum.test/t/2", "second record with enough words")])
    rid1, rid2 = out["new_ids"]
    r = cli("show", "--room", ROOM, "--ids", f"{rid1},{rid2}", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"### {rid1} | websearch | 2025-03-04 | forum.test" in r.stdout
    assert "url: https://forum.test/t/1" in r.stdout and TEXT in r.stdout
    assert f"### {rid2} | websearch | undated | forum.test" in r.stdout
    r = cli("show", "--room", ROOM, "--ids", f"{rid1},0000000000000000", "--run", "2026-09-26")
    assert r.returncode == 1 and TEXT in r.stdout and "record 0000000000000000 is not stored for room" in r.stderr
    r = cli("show", "--run", "2026-09-26")
    assert r.returncode == 1


def test_excerpt_returns_the_exact_original_substring(run, h, cli):
    rid = h.store(run, ROOM, [h.make_record("https://forum.test/t/1", TEXT)])["new_ids"][0]
    assert admin.excerpt(TEXT, "worth it", "waste of money") == "worth it”?  I paid ₹30,000 and\tstill scored 305 — waste of money"
    assert admin.excerpt(TEXT, "“worth", "money.") == "“worth it”?  I paid ₹30,000 and\tstill scored 305 — waste of money."
    assert admin.excerpt(TEXT, "GRE coaching:", "GRE coaching:") == "GRE   coaching:"
    assert admin.excerpt(TEXT, "  I   paid  ", "305") == "I paid ₹30,000 and\tstill scored 305"
    with pytest.raises(common.ValidationErrors) as e:
        admin.excerpt(TEXT, "never there", "305")
    assert "start text was not found" in str(e.value)
    with pytest.raises(common.ValidationErrors) as e:
        admin.excerpt(TEXT, "305", "worth it")  # end before start
    assert "end text was not found after the start" in str(e.value)
    r = cli("excerpt", "--room", ROOM, "--id", rid, "--start", "I paid", "--end", "waste of money", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "I paid ₹30,000 and\tstill scored 305 — waste of money\n"
    assert "[excerpt: 11 words from record" in r.stderr and "long enough for a quote" in r.stderr
    # the excerpt passes the quote checker as an exact substring
    import quote_check
    import records

    verdict = quote_check.check_quote({"record_id": rid, "text": r.stdout.strip()}, records.records_by_id(run, ROOM), 5)
    assert verdict["status"] == "pass"
    r = cli("excerpt", "--room", ROOM, "--id", rid, "--start", "I paid", "--end", "305", "--run", "2026-09-26")
    assert "too short for a quote" not in r.stderr
    r = cli("excerpt", "--room", ROOM, "--id", rid, "--start", "305", "--end", "305", "--run", "2026-09-26")
    assert r.returncode == 0 and "too short for a quote" in r.stderr
    r = cli("excerpt", "--room", ROOM, "--id", "nope", "--start", "a", "--end", "b", "--run", "2026-09-26")
    assert r.returncode == 1


def test_show_pain_uses_pains_json_or_the_draft(run, h, cli):
    out = h.store(run, ROOM, [h.make_record(f"https://forum.test/t/{i}", f"member record {i} about fees and more words") for i in range(1, 8)])
    ids = out["new_ids"]
    pid = f"{ROOM}--fees"
    draft = {"pains": [{"pain_key": "fees", "description": "coaching fees hurt",
                        "quotes": [{"record_id": ids[0], "url": "https://forum.test/t/1", "date": None, "text": "member record 1 about fees"}]}]}
    common.write_json(common.room_dir(run, ROOM) / "pains_draft.json", draft)
    common.write_json(common.room_dir(run, ROOM) / "counts.json", {"pains": {"fees": {"member_record_ids": ids}}})
    r = cli("show", "--pain", pid, "--limit", "3", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"# Pain {pid} (from runs/2026-09-26/03_listen/rooms/{ROOM}/pains_draft.json)" in r.stdout
    assert '"description": "coaching fees hurt"' in r.stdout and "## Quotes (1)" in r.stdout
    assert "## Member records: 3 of 7 (a fixed random sample" in r.stdout
    assert r.stdout.count("### ") == 3
    assert cli("show", "--pain", pid, "--limit", "3", "--run", "2026-09-26").stdout == r.stdout  # seeded sample
    common.write_json(common.listen_dir(run) / "pains.json", {"pains": [{"pain_id": pid, "description": "from pains.json", "quotes": []}]})
    r = cli("show", "--pain", pid, "--run", "2026-09-26")
    assert r.returncode == 0 and "(from runs/2026-09-26/03_listen/pains.json)" in r.stdout and "from pains.json" in r.stdout
    assert "## Member records: 7 of 7" in r.stdout
    r = cli("show", "--pain", f"{ROOM}--nope", "--run", "2026-09-26")
    assert r.returncode == 2 and "No pain" in r.stderr


def test_listen_status_counts_sources_rounds_and_dates(run, h, cli):
    h.store(run, ROOM, [h.make_record("https://a.test/1", "first record with words", date="2025-01-02", round=1),
                        h.make_record("https://a.test/2", "second record with words", round=1),
                        h.make_record("https://b.test/3", "third record with words", round=2)])
    h.store(run, ROOM, [h.make_record("https://c.test/4", "fourth record with words", date="2025-05-06", round=2)], source="inbox")
    common.write_jsonl(common.room_dir(run, ROOM) / "queries.jsonl", [{"round": 1, "query": "a", "kind": "forum"},
                                                                       {"round": 1, "query": "b", "kind": "video"},
                                                                       {"round": 2, "query": "c", "kind": "qa"}])
    import records

    records.make_batches(run, ROOM)
    h.write_taxonomy(run, ROOM, ["fees", "quant"])
    common.write_json(common.room_dir(run, ROOM) / "saturation.json",
                      {"rounds": [{"round": 2, "records": 4, "saturated": False}], "stop_reason": None})
    s = admin.listen_status(run, ROOM)
    assert s["records"] == 4 and s["per_source"] == {"inbox": 1, "websearch": 3}
    assert s["per_round"] == {"1": 2, "2": 2} and s["dated"] == 2 and s["undated"] == 2 and s["domains"] == 3
    assert s["queries_per_round"] == {"1": 2, "2": 1}
    assert s["batches"] == ["batch_r1_001", "batch_r2_001"] and s["batch_records"] == 4
    assert s["labeled"] == 0 and s["pains_in_taxonomy"] == 2 and s["saturation"]["saturated"] is False
    r = cli("listen-status", "--room", ROOM, "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"Room {ROOM}: 4 records (2 dated, 2 undated) from 3 domain(s)." in r.stdout
    assert "Per source: inbox 1, websearch 3." in r.stdout and "Per round: round 1: 2, round 2: 2." in r.stdout
    assert "Saturation: round 2, 4 records, saturated no." in r.stdout
    r = cli("listen-status", "--room", "empty-room", "--run", "2026-09-26")
    assert r.returncode == 2 and "has no folder" in r.stderr


def test_every_documented_admin_command_and_flag_exists(cli):
    import re
    from conftest import REAL_ROOT

    parser_help = cli("--help").stdout
    mine = {"init", "preflight", "ledger-check", "loop-init", "rooms-known", "graveyard", "log", "source-decision", "robots",
            "purge-expired", "show", "excerpt", "listen-status", "price-check", "rooms", "fx", "mask"}
    for cmd in mine:
        assert re.search(rf"^\s+{re.escape(cmd)}\b", parser_help, re.M), cmd
    docs = ""
    for p in list((REAL_ROOT / ".claude").rglob("*.md")) + [REAL_ROOT / "pipeline" / "README.md"]:
        docs += p.read_text(encoding="utf-8")
    for m in re.finditer(r"funnel (%s)((?: --[a-z-]+)*)" % "|".join(sorted(mine, key=len, reverse=True)), docs):
        cmd, flags = m.group(1), m.group(2).split()
        help_text = cli(cmd, "--help").stdout
        for flag in flags:
            assert flag in help_text, f"{cmd} {flag}"


# =========================================================================== no stray run folders; dry-run folders
def test_commands_that_need_no_run_folder_never_create_one(froot, cli):
    """rooms-known, graveyard, ledger-check and init run without --run on any day (the skills call them so);
    they must not leave an empty runs/<today>/ behind, which would be listed, committed and mistaken for a run.
    A command that fails on a missing input must not create the folder either."""
    later = froot / "runs" / "2026-10-03"
    env = {"FUNNEL_TODAY": "2026-10-03"}
    for args in (("rooms-known",), ("graveyard",), ("ledger-check",), ("init",)):
        r = cli(*args, env=env)
        assert r.returncode == 0, (args, r.stderr)
        assert not later.exists(), args
    for args in (("shortlist",), ("review",), ("runlog",), ("pains",), ("status",), ("walks",), ("audit-status",), ("numbers",)):
        r = cli(*args, env=env)
        assert r.returncode == 2, (args, r.stdout, r.stderr)
        assert not later.exists(), args
    assert sorted(p.name for p in (froot / "runs").iterdir()) == []
    # once the run folder exists, the same commands log into it
    later.mkdir()
    r = cli("rooms-known", env=env)
    assert r.returncode == 0, r.stderr
    assert [(e["command"], e["kind"], e["stage"]) for e in common.read_jsonl(later / "runlog.jsonl")] == [("rooms-known", "ran", 0)]


def test_dry_run_folders_are_accepted_and_kept_apart(froot, cli):
    """A one-room dry run of Stages 3-6 lives in runs/<date>-dry-<room>/ so its files are never mistaken for
    the real run: rooms-known and audit-status skip it, `status` says (dry run) once a --dry-run command ran."""
    dry = f"2026-09-26-dry-{ROOM}"
    r = cli("log", "--stage", "3", "--note", "one-room dry run", "--run", dry)
    assert r.returncode == 0, r.stderr
    rd = froot / "runs" / dry
    assert (rd / "runlog.jsonl").exists()
    r = cli("log", "--stage", "3", "--note", "x", "--run", "2026-09-26-dry")
    assert r.returncode == 1 and "one-room dry run, `YYYY-MM-DD-dry-<room-slug>`" in r.stderr
    _old_run(froot, "2026-09-20", ROOM)
    common.write_json(rd / "02_mask.json", {"rooms": [{"slug": "dry-only-room", "name": "x", "status": "kept", "rank": 1}]})
    (rd / "SHORTLIST.md").write_text("# Shortlist\n", encoding="utf-8")
    r = cli("rooms-known")
    assert r.returncode == 0, r.stderr
    assert "dry-only-room" not in r.stdout and ROOM in r.stdout
    r = cli("audit-status")
    assert r.returncode == 2 and "No run has a SHORTLIST.md yet" in r.stderr
    r = cli("status", "--run", dry)
    assert r.returncode == 0, r.stderr
    assert f"Run runs/{dry}:" in r.stdout and "(dry run)" not in r.stdout
    r = cli("log", "--stage", "3", "--note", "y", "--run", dry, "--dry-run")
    assert r.returncode == 0, r.stderr
    r = cli("status", "--run", dry)
    assert f"Run runs/{dry} (dry run):" in r.stdout
    assert "Dry run: log ran with --dry-run in this folder. Their outputs are not a finished run" in r.stdout
