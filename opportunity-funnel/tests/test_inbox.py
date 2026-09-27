"""Tests for `ingest-inbox`: WhatsApp (iOS and Android), Telegram, CSV and plain-text exports are parsed,
anonymized with sender names as known names, stored once, and never printed."""
import json
import re
from pathlib import Path

import common
import funnel
import records
import sources

ROOM = "gre-engineers-india"
RUN = "2026-09-26"
NAMES = ("Rahul", "Sharma", "Priya", "Mehta", "rahul_s", "98765", "9876543210")
TEXTS = ("wasted money on coaching", "Magoosh course", "Jamboree classes", "Took four months", "coaching fee was wasted")

WHATSAPP_IOS = """‎[05/13/2024, 10:00:12] Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.
[05/13/2024, 10:01:00] Rahul Sharma: Hi Priya, has anyone here paid for the Magoosh course?
I paid ₹15,000 and I am still stuck
on quant.
[05/13/2024, 10:02:00] Priya Mehta: ‎image omitted
[05/13/2024, 10:03:00] Priya Mehta: ok
[05/13/2024, 10:04:00] +91 98765 43210: same here, wasted money on coaching, call me on 9876543210
[05/13/2024, 10:05:00] ‎Rahul Sharma added Priya Mehta
[05/13/2024, 10:06:00] Priya Mehta: This message was deleted.
[05/14/2024, 09:00:00 AM] Priya Mehta: ask Priya Mehta about the refund, she got one
"""

WHATSAPP_ANDROID = """13/05/2024, 10:01 - Rahul Sharma: Anyone tried the Jamboree classes in Pune?
Paid 40k and the faculty kept changing
13/05/2024, 10:02 - Priya Mehta: <Media omitted>
13/05/2024, 10:03 - Rahul Sharma added Priya Mehta
13/05/2024, 10:04 - Priya Mehta: yes same
14/05/2024, 08:30 - Priya Mehta: I want a refund from them
"""

WHATSAPP_AMBIGUOUS = "[05/06/2024, 10:00:00] Rahul Sharma: Which coaching is cheaper in Delhi these days\n"

TELEGRAM = {
    "name": "GRE Batch 2026", "type": "private_supergroup", "id": 1,
    "messages": [
        {"id": 1, "type": "service", "date": "2024-05-13T10:00:00", "actor": "Rahul Sharma", "actor_id": "user1",
         "action": "create_group", "title": "GRE Batch 2026", "members": ["Rahul Sharma", "Priya Mehta"], "text": "", "text_entities": []},
        {"id": 2, "type": "message", "date": "2024-05-13T10:05:00", "from": "Priya Mehta", "from_id": "user2",
         "text": ["Paid ", {"type": "bold", "text": "₹20,000"}, " for coaching, ", {"type": "mention", "text": "@rahul_s"}, " what now?"],
         "text_entities": [{"type": "plain", "text": "Paid "}, {"type": "bold", "text": "₹20,000"}]},
        {"id": 3, "type": "message", "date": "2024-05-13T10:06:00", "from": "Rahul Sharma", "from_id": "user1",
         "text": "lol", "text_entities": [{"type": "plain", "text": "lol"}]},
        {"id": 4, "type": "message", "date": "2024-05-13T10:07:00", "from": "Rahul Sharma", "from_id": "user1",
         "text": "Ask for a refund, Priya Mehta got one last week", "text_entities": []},
    ],
}

CSV = """date,sender,text
2025-01-05,Rahul Sharma,"Asked for the fee, said 15k is too much"
2025-01-06,Priya Mehta,thanks
06/02/2025,Priya Mehta,"Will pay after the mock test, promised"
"""

NOTES_MD = """# Notes from the call

Three people said the coaching fee was wasted.

ok

Two asked about refunds and one already got it.
"""


def _fill_inbox(froot, kind="closed_groups"):
    d = froot / "inbox" / kind / ROOM
    d.mkdir(parents=True, exist_ok=True)
    (d / "WhatsApp Chat with Priya Mehta.txt").write_text(WHATSAPP_IOS, encoding="utf-8")
    (d / "gre-batch.txt").write_text(WHATSAPP_ANDROID, encoding="utf-8")
    (d / "small-group.txt").write_text(WHATSAPP_AMBIGUOUS, encoding="utf-8")
    (d / "ChatExport_2024").mkdir(exist_ok=True)
    (d / "ChatExport_2024" / "result.json").write_text(json.dumps(TELEGRAM, ensure_ascii=False), encoding="utf-8")
    (d / "customer-notes.csv").write_text(CSV, encoding="utf-8")
    (d / "notes.md").write_text(NOTES_MD, encoding="utf-8")
    (d / "photo.jpg").write_bytes(b"\xff\xd8\xff\xe0 not text")
    (d / ".hidden.txt").write_text("13/05/2024, 10:01 - Rahul Sharma: hidden file must be ignored", encoding="utf-8")
    return d


def _raw_text(run, source="inbox:closed_groups"):
    return records.source_file(run, ROOM, source).read_text(encoding="utf-8")


def _assert_private(text):
    for n in NAMES:
        assert n not in text, n


# --------------------------------------------------------------------------- parsers
def test_whatsapp_parser_ios_month_first():
    r = sources.parse_whatsapp(WHATSAPP_IOS)
    assert r["date_order"] == "month-first" and "second field is over 12" in r["detected_by"]
    assert r["system_dropped"] == 4 and r["senders"] == {"Rahul Sharma", "Priya Mehta", "+91 98765 43210"}
    assert [(m["line"], m["date"]) for m in r["messages"]] == [(2, "2024-05-13"), (6, "2024-05-13"), (7, "2024-05-13"), (10, "2024-05-14")]
    assert r["messages"][0]["text"] == "Hi Priya, has anyone here paid for the Magoosh course?\nI paid ₹15,000 and I am still stuck\non quant."
    assert r["messages"][0]["sender"] == "Rahul Sharma"


def test_whatsapp_parser_android_day_first_and_default():
    r = sources.parse_whatsapp(WHATSAPP_ANDROID)
    assert r["date_order"] == "day-first" and "first field is over 12" in r["detected_by"]
    assert r["system_dropped"] == 2 and len(r["messages"]) == 3
    assert r["messages"][0]["text"] == "Anyone tried the Jamboree classes in Pune?\nPaid 40k and the faculty kept changing"
    assert r["messages"][2]["date"] == "2024-05-14" and r["messages"][2]["line"] == 6
    r2 = sources.parse_whatsapp(WHATSAPP_AMBIGUOUS)
    assert r2["date_order"] == "day-first" and "default" in r2["detected_by"] and r2["messages"][0]["date"] == "2024-06-05"
    assert sources.parse_whatsapp("[31/02/2024, 10:00:00] A B: bad date but real message here")["messages"][0]["date"] is None
    assert sources.looks_like_whatsapp(WHATSAPP_ANDROID) and not sources.looks_like_whatsapp(NOTES_MD)


def test_telegram_csv_and_paragraph_parsers():
    t = sources.parse_telegram(TELEGRAM)
    assert t["system_dropped"] == 1 and t["senders"] == {"Rahul Sharma", "Priya Mehta"}
    assert [(m["msg_id"], m["date"], m["text"]) for m in t["messages"]] == [
        (2, "2024-05-13", "Paid ₹20,000 for coaching, @rahul_s what now?"),
        (3, "2024-05-13", "lol"),
        (4, "2024-05-13", "Ask for a refund, Priya Mehta got one last week")]
    assert sources.parse_telegram({"not": "telegram"}) is None
    c = sources.parse_csv_chat(CSV)
    assert c["senders"] == {"Rahul Sharma", "Priya Mehta"} and c["date_order"] == "day-first"
    assert [(m["row"], m["date"]) for m in c["messages"]] == [(1, "2025-01-05"), (2, "2025-01-06"), (3, "2025-02-06")]
    assert sources.parse_csv_chat("when,what\n1,2\n") is None
    p = sources.parse_paragraphs(NOTES_MD)
    assert [m["paragraph"] for m in p["messages"]] == [1, 2, 3, 4] and p["messages"][2]["text"] == "ok"
    assert sources.word_count("ok") == 1 and sources.word_count("thanks a lot") == 3 and sources.word_count("# x - y") == 2


# --------------------------------------------------------------------------- ingest
def test_ingest_closed_groups_stores_anonymized_records_only(run, froot):
    _fill_inbox(froot)
    s = sources.ingest_inbox(run, ROOM)
    assert s["source"] == "inbox:closed_groups" and s["files_read"] == 6 and s["files_skipped"] == 1
    assert s["formats"] == {"csv": 1, "telegram": 1, "text": 1, "whatsapp": 3}
    assert s["messages"] == 18 and s["dropped_system"] == 7 and s["dropped_short"] == 5
    assert s["records_new"] == 13 and s["duplicates"] == 0 and s["senders_removed"] == 3
    # every file is known only by a content-free label: nothing of the file name (often a person) survives
    L = {name: sources.inbox_label(name) for name in ("ChatExport_2024/result.json", "WhatsApp Chat with Priya Mehta.txt",
                                                       "customer-notes.csv", "gre-batch.txt", "notes.md", "small-group.txt")}
    assert all(re.fullmatch(r"file_[0-9a-f]{12}", lab) for lab in L.values()) and len(set(L.values())) == 6
    by_file = {f["file"]: f for f in s["files"]}
    assert set(by_file) == set(L.values())
    WA, GB, SG, NM, TG, CSVF = (L["WhatsApp Chat with Priya Mehta.txt"], L["gre-batch.txt"], L["small-group.txt"], L["notes.md"],
                                L["ChatExport_2024/result.json"], L["customer-notes.csv"])
    assert by_file[WA]["date_order"] == "month-first"
    assert by_file[GB]["date_order"] == "day-first" and by_file[GB]["records"] == 2
    assert by_file[SG]["detected_by"].endswith("(the default)")
    assert by_file[NM]["date_order"] is None and by_file[NM]["records"] == 3
    index = json.loads(sources.inbox_index_path(run, ROOM).read_text(encoding="utf-8"))
    assert index[WA] == {"path": "WhatsApp Chat with Priya Mehta.txt", "format": "whatsapp", "kind": "closed_groups"}
    assert set(index) == set(L.values()) and "raw" in s["index"]

    raw = _raw_text(run)
    _assert_private(raw)
    for phrase in ("sender", "Rahul Sharma", "GRE Batch 2026", "WhatsApp", "gre-batch", "customer-notes", "notes.md", ".txt", ".csv"):
        assert phrase not in raw
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    assert set(json.loads(raw.splitlines()[0])) == set(records.RECORD_FIELDS)
    ios = recs[f"inbox://closed_groups/{ROOM}/{WA}#2"]
    assert ios["text"] == "Hi [name], has anyone here paid for the Magoosh course?\nI paid ₹15,000 and I am still stuck\non quant."
    assert ios["date"] == "2024-05-13" and ios["source"] == "inbox:closed_groups"
    # files are read in sorted path order: ChatExport_2024/result.json (2 records) comes first
    assert ios["meta"] == {"kind": "chat_message", "format": "whatsapp", "file": WA, "inbox": "closed_groups",
                           "line": 2, "round": 1, "order": [1, 0, 3], "date_from": "file"}
    assert recs[f"inbox://closed_groups/{ROOM}/{WA}#7"]["text"] == "same here, wasted money on coaching, call me on [phone]"
    assert recs[f"inbox://closed_groups/{ROOM}/{WA}#10"]["text"] == "ask [name] about the refund, she got one"
    assert f"inbox://closed_groups/{ROOM}/{WA}#6" not in recs  # "ok" is under 3 words
    tg = recs[f"inbox://closed_groups/{ROOM}/{TG}#2"]
    assert tg["text"] == "Paid ₹20,000 for coaching, [user] what now?" and tg["meta"]["msg_id"] == 2 and tg["date"] == "2024-05-13"
    assert recs[f"inbox://closed_groups/{ROOM}/{TG}#4"]["text"] == "Ask for a refund, [name] got one last week"
    csv1 = recs[f"inbox://closed_groups/{ROOM}/{CSVF}#r1"]
    assert csv1["text"] == "Asked for the fee, said 15k is too much" and csv1["date"] == "2025-01-05" and csv1["meta"]["row"] == 1
    assert recs[f"inbox://closed_groups/{ROOM}/{CSVF}#r3"]["date"] == "2025-02-06"
    md = recs[f"inbox://closed_groups/{ROOM}/{NM}#p2"]
    assert md["text"] == "Three people said the coaching fee was wasted." and md["date"] is None and md["meta"]["date_from"] == "none"
    assert all(r["record_id"] == common.record_id(r["url"], r["text"]) for r in recs.values())
    orders = [r["meta"]["order"] for r in records.load_records(run, ROOM)]
    assert orders == sorted(orders) and orders[0] == [1, 0, 1] and orders[-1] == [1, 0, 13]

    events = common.read_jsonl(run / "runlog.jsonl")
    _assert_private(json.dumps(events, ensure_ascii=False))
    assert "WhatsApp" not in json.dumps(events) and "gre-batch" not in json.dumps(events)
    notes = {e["file"]: e for e in events if e["kind"] == "note" and e.get("date_order")}
    assert notes[WA]["date_order"] == "month-first"
    assert notes[GB]["date_order"] == "day-first" and notes[CSVF]["date_order"] == "day-first"
    assert SG in notes and NM not in notes and TG not in notes

    # rerun: nothing new, byte-identical file
    before = records.source_file(run, ROOM, "inbox:closed_groups").read_bytes()
    s2 = sources.ingest_inbox(run, ROOM)
    assert s2["records_new"] == 0 and s2["duplicates"] == 13
    assert records.source_file(run, ROOM, "inbox:closed_groups").read_bytes() == before
    # the room's batches accept these records; the 2024 chat dates fall outside the 24-month lookback
    m = records.make_batches(run, ROOM)
    assert m["filters"]["loaded"] == 13 and m["filters"]["dropped_old"] == 8 and m["filters"]["kept"] == 5
    assert sorted(m["batches"]) == ["batch_r1_001"]


def test_cli_prints_counts_but_never_names_or_text(run, froot, cli):
    _fill_inbox(froot)
    r = cli("ingest-inbox", "--room", ROOM, "--run", RUN)
    assert r.returncode == 0, r.stderr
    out = r.stdout + r.stderr
    _assert_private(out)
    for phrase in TEXTS:
        assert phrase not in out
    assert "6 file(s) read" in out and "1 skipped" in out and "Records new: 13" in out
    wa = sources.inbox_label("WhatsApp Chat with Priya Mehta.txt")
    assert f"{wa}: whatsapp, 4 messages, 4 system lines dropped, 1 messages under 3 words dropped, 3 kept." in out
    for name in ("WhatsApp", "gre-batch", "customer-notes", "small-group", "notes.md", "ChatExport"):
        assert name not in out, name  # file names never reach the screen
    assert "label-to-file map" in out and "_inbox_index.json" in out
    assert "Dates read as month-first" in out and "Dates read as day-first" in out
    assert "Sender names removed from every message: 3 distinct (never stored or printed)." in out
    assert "inbox_closed_groups.jsonl" in out
    events = common.read_jsonl(run / "runlog.jsonl")
    src = [e for e in events if e["kind"] == "source" and e["command"] == "ingest-inbox"]
    assert len(src) == 1 and src[0]["records_new"] == 13 and src[0]["source"] == "inbox:closed_groups" and src[0]["senders_removed"] == 3
    _assert_private(json.dumps(events))


def test_customers_folder_and_source(run, froot, cli):
    d = froot / "inbox" / "customers" / ROOM
    d.mkdir(parents=True)
    (d / "messages.csv").write_text(CSV, encoding="utf-8")
    r = cli("ingest-inbox", "--room", ROOM, "--customers", "--round", "2", "--run", RUN)
    assert r.returncode == 0, r.stderr
    assert "inbox:customers" in r.stdout and "Records new: 2" in r.stdout
    _assert_private(r.stdout)
    recs = records.load_records(run, ROOM)
    assert len(recs) == 2 and all(r["source"] == "inbox:customers" for r in recs)
    assert records.source_file(run, ROOM, "inbox:customers").name == "inbox_customers.jsonl"
    assert recs[0]["url"] == f"inbox://customers/{ROOM}/{sources.inbox_label('messages.csv')}#r1" and recs[0]["meta"]["round"] == 2
    assert "messages.csv" not in r.stdout
    assert recs[0]["meta"]["order"] == [2, 0, 1]
    # closed_groups is untouched and empty: skipped, not an error
    r = cli("ingest-inbox", "--room", ROOM, "--run", RUN)
    assert r.returncode == 0 and "Nothing to ingest" in r.stdout and "closed_groups" in r.stdout
    events = common.read_jsonl(run / "runlog.jsonl")
    skip = [e for e in events if e["kind"] == "skip" and e["command"] == "ingest-inbox"]
    assert len(skip) == 1 and skip[0]["source"] == "inbox:closed_groups" and "would_add" in skip[0]


def test_missing_folder_is_skipped_and_bad_slug_refused(run, froot, capsys):
    s = sources.ingest_inbox(run, ROOM)
    assert s["records_new"] == 0 and "no chat exports" in s["skipped_reason"]
    assert not records.load_records(run, ROOM)
    rc = funnel.main(["ingest-inbox", "--room", ROOM, "--run", RUN])
    assert rc == 0 and "Nothing to ingest" in capsys.readouterr().out
    rc = funnel.main(["ingest-inbox", "--room", "../x", "--run", RUN])
    assert rc == 1


def test_known_names_reach_every_file_and_file_labels_are_safe(run, froot):
    d = froot / "inbox" / "closed_groups" / ROOM
    d.mkdir(parents=True)
    (d / "Chat with Rahul Sharma.txt").write_text("13/05/2024, 10:01 - Priya Mehta: Rahul, the Delhi fee is 40k now\n", encoding="utf-8")
    (d / "other notes.md").write_text("Priya Mehta said the Hyderabad centre refunded her fully.\n", encoding="utf-8")
    s = sources.ingest_inbox(run, ROOM)
    assert s["records_new"] == 2 and s["senders_removed"] == 2  # the sender, plus the contact named in the file name
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    chat, other = sources.inbox_label("Chat with Rahul Sharma.txt"), sources.inbox_label("other notes.md")
    assert f"inbox://closed_groups/{ROOM}/{chat}#1" in recs
    md = recs[f"inbox://closed_groups/{ROOM}/{other}#p1"]
    assert md["text"] == "[name] said the Hyderabad centre refunded her fully."  # a sender from another file
    wa = recs[f"inbox://closed_groups/{ROOM}/{chat}#1"]
    assert wa["text"] == "[name], the Delhi fee is 40k now"
    _assert_private(_raw_text(run))
    assert "Chat" not in _raw_text(run) and "other" not in _raw_text(run)


def test_file_names_that_are_people_never_reach_any_output(run, froot, cli):
    """A customers folder is where files are naturally named after the customer (rule 5)."""
    d = froot / "inbox" / "customers" / ROOM
    d.mkdir(parents=True)
    (d / "Anita Desai.txt").write_text("The coaching fee was a waste for me.\n\nI still want the refund they promised.\n", encoding="utf-8")
    (d / "priya_sharma_feedback.csv").write_text('date,sender,text\n2025-03-01,Priya Sharma,"Priya Sharma here, 15k for nothing"\n', encoding="utf-8")
    r = cli("ingest-inbox", "--room", ROOM, "--customers", "--run", RUN)
    assert r.returncode == 0, r.stderr
    stored = records.load_records(run, ROOM)
    assert len(stored) == 3
    labels = {sources.inbox_label("Anita Desai.txt"), sources.inbox_label("priya_sharma_feedback.csv")}
    assert {rec["meta"]["file"] for rec in stored} == labels
    raw = _raw_text(run, "inbox:customers")
    runlog = json.dumps(common.read_jsonl(run / "runlog.jsonl"), ensure_ascii=False)
    for needle in ("Anita", "Desai", "priya", "Priya", "sharma", "Sharma", "feedback", ".txt", ".csv"):
        assert needle not in raw, needle
        assert needle not in r.stdout + r.stderr, needle
        assert needle not in runlog, needle
    assert next(rec for rec in stored if rec["url"].endswith("#r1"))["text"] == "[name] here, 15k for nothing"
    # the map from label to file lives only under raw/, which .gitignore keeps out of git
    index = sources.inbox_index_path(run, ROOM)
    assert index.exists() and "03_listen/raw/" in common.rel(index)
    assert json.loads(index.read_text(encoding="utf-8"))[sources.inbox_label("Anita Desai.txt")]["path"] == "Anita Desai.txt"
    gitignore = (Path(__file__).resolve().parent.parent / ".gitignore").read_text(encoding="utf-8")
    assert "runs/*/03_listen/raw/" in gitignore


def test_contact_descriptors_never_strip_ordinary_words_from_other_messages(run, froot):
    """A saved contact "Rahul GRE Tutor" removes Rahul (and the whole contact name) from every message, but
    GRE, tutor, coaching and the file label stay whole: the evidence text is what the quotes must match."""
    d = froot / "inbox" / "closed_groups" / ROOM
    d.mkdir(parents=True)
    (d / "gre-batch.txt").write_text(
        "13/05/2024, 10:01 - Rahul GRE Tutor: GRE prep is expensive, my tutor charged 40k\n"
        "13/05/2024, 10:02 - Priya Mehta: my GRE tutor was worse, I paid 50k and got 300\n"
        "13/05/2024, 10:03 - Priya Mehta: Rahul GRE Tutor and rahul both said the coaching centre in Delhi is fine\n"
        "13/05/2024, 10:04 - Amit Sir Coaching: sir, the GRE coaching fee is 30k at our centre\n", encoding="utf-8")
    s = sources.ingest_inbox(run, ROOM)
    assert s["records_new"] == 4 and s["senders_removed"] == 3
    texts = [r["text"] for r in sorted(records.load_records(run, ROOM), key=lambda r: r["meta"]["order"])]
    assert texts == [
        "GRE prep is expensive, my tutor charged 40k",
        "my GRE tutor was worse, I paid 50k and got 300",
        "[name] and [name] both said the coaching centre in Delhi is fine",
        "sir, the GRE coaching fee is 30k at our centre",
    ]
    raw = _raw_text(run)
    for needle in ("Rahul", "rahul", "Priya", "Mehta", "Amit", "gre-batch"):
        assert needle not in raw, needle
    assert "[name]-batch" not in raw and sources.inbox_label("gre-batch.txt") in raw
