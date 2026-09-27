import json

import pytest

import common
import harvest
import records
from conftest import TRANSCRIPTS

ROOM = "gre-engineers-india"
Q1 = "GRE coaching waste of money reddit"
Q2 = '"paid" GRE course "didn\'t help"'
Q3 = "Reddit Responsible Builder Policy API access approval"
SUMMARY_PHRASES = ("Based on the search results", "REMINDER", "here's what I found", "I found several relevant results")


def _queries(run, rows):
    common.write_jsonl(harvest.queries_path(run, ROOM), rows)


def _stored(run):
    return records.load_records(run, ROOM)


def test_both_transcript_forms_are_parsed(run):
    _queries(run, [
        {"round": 1, "query": Q1, "kind": "forum"},
        {"round": 1, "query": Q2, "kind": "forum"},
        {"round": 2, "query": Q3, "kind": "official"},
    ])
    s = harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    assert s["queries_matched"] == 3 and s["queries_unmatched"] == []
    assert s["transcript_files"] == 2
    assert s["links_seen"] == 29 and s["records_new"] == 18 and s["skipped_junk"] == 10 and s["duplicates"] == 1
    recs = _stored(run)
    by_query = {}
    for r in recs:
        by_query.setdefault(r["meta"]["query"], []).append(r)
    assert len(by_query[Q3]) == 8  # toolUseResult form (main session line)
    assert len(by_query[Q1]) == 4 and len(by_query[Q2]) == 6  # tool_result string form (subagent lines)
    assert all(r["source"] == "websearch" and r["meta"]["kind"] == "search_title" for r in recs)
    assert all(r["record_id"] == common.record_id(r["url"], r["text"]) for r in recs)


def test_query_matching_is_exact_after_strip(run):
    _queries(run, [
        {"round": 1, "query": "   " + Q1 + "  ", "kind": "forum"},
        {"round": 1, "query": Q1.lower(), "kind": "forum"},
        {"round": 1, "query": "GRE coaching fees Hyderabad", "kind": "pricing"},
    ])
    s = harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    assert s["queries_matched"] == 1
    assert s["queries_unmatched"] == [Q1.lower(), "GRE coaching fees Hyderabad"]
    assert s["records_new"] == 4


@pytest.mark.parametrize("title,junk", [
    ("", True), ("   ", True), ("www.teamblind.com", True), ("buecher.de", True), ("learningcenter.unt.edu", True),
    ("https://x.com/a/b", True), ("www.careers360.com/question", True), ("Manhattan Review", True), ("Answers (2)", True),
    ("GRE – Reddit", True), ("Responsible Builder Policy – Reddit Help", False),
    ("0% found this document useful (0 votes)", False), ("How much does GRE coaching value?", False),
])
def test_junk_titles(title, junk):
    assert harvest.is_junk_title(title) is junk


def test_dates_from_url_paths(run):
    _queries(run, [{"round": 1, "query": Q1, "kind": "forum"}, {"round": 1, "query": Q2, "kind": "forum"}])
    harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    by_url = {r["url"]: r for r in _stored(run)}
    byu = by_url["https://universe.byu.edu/2002/05/13/experts-say-gre-prep-courses-a-waste"]
    assert byu["date"] == "2002-05-13" and byu["meta"]["date_from"] == "url" and byu["meta"]["date_precision"] == "day"
    dp = by_url["https://www.thedp.com/article/2016/04/studyign-for-the-graduate-record-examination"]
    assert dp["date"] == "2016-04-01" and dp["meta"]["date_precision"] == "month"
    ihe = by_url["https://www.insidehighered.com/admissions/views/2021/06/28/its-time-do-away-gre-opinion"]
    assert ihe["date"] == "2021-06-28"
    sdn = by_url["https://forums.studentdoctor.net/threads/are-gre-prep-courses-worth-it.968822/"]
    assert sdn["date"] is None and sdn["meta"]["date_from"] == "none" and "date_precision" not in sdn["meta"]
    assert sdn["meta"]["domain"] == "forums.studentdoctor.net"


def test_one_record_per_url_and_rerun_is_idempotent(run):
    _queries(run, [{"round": 1, "query": Q1, "kind": "forum"}, {"round": 1, "query": Q2, "kind": "forum"}])
    s1 = harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    urls = [r["url"] for r in _stored(run)]
    assert len(urls) == len(set(urls)) == 10
    assert urls.count("https://universe.byu.edu/2002/05/13/experts-say-gre-prep-courses-a-waste") == 1
    assert s1["duplicates"] == 1
    raw = records.source_file(run, ROOM, "websearch").read_bytes()
    s2 = harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    assert s2["records_new"] == 0 and s2["duplicates"] == 11
    assert records.source_file(run, ROOM, "websearch").read_bytes() == raw


def test_meta_order_is_round_query_index_rank(run):
    _queries(run, [
        {"round": 1, "query": "unmatched first line", "kind": "forum"},
        {"round": 1, "query": Q1, "kind": "forum"},
        {"round": 3, "query": Q3, "kind": "official"},
    ])
    harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    by_url = {r["url"]: r for r in _stored(run)}
    byu = by_url["https://universe.byu.edu/2002/05/13/experts-say-gre-prep-courses-a-waste"]
    assert byu["meta"]["order"] == [1, 2, 1] and byu["meta"]["round"] == 1 and byu["meta"]["query_kind"] == "forum"
    c360 = by_url["https://www.careers360.com/question-how-much-does-gre-coaching-value"]
    assert c360["meta"]["order"] == [1, 2, 6]  # rank counts skipped junk titles too
    reddit_help = by_url["https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy"]
    assert reddit_help["meta"]["order"] == [3, 3, 1] and reddit_help["meta"]["round"] == 3
    m = records.make_batches(run, ROOM)
    assert sorted(m["batches"]) == ["batch_r1_001", "batch_r3_001"]


def test_summary_text_is_never_stored(run):
    _queries(run, [
        {"round": 1, "query": Q1, "kind": "forum"},
        {"round": 1, "query": Q2, "kind": "forum"},
        {"round": 2, "query": Q3, "kind": "official"},
    ])
    harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    raw = records.source_file(run, ROOM, "websearch").read_text(encoding="utf-8")
    fixture_text = "".join(p.read_text(encoding="utf-8") for p in TRANSCRIPTS.rglob("*.jsonl"))
    for phrase in SUMMARY_PHRASES:
        assert phrase in fixture_text  # the fixture does carry the summaries...
        assert phrase not in raw  # ...and none of it reaches the records
    for r in _stored(run):
        assert len(r["text"]) < 200 and "\n" not in r["text"]


def test_parse_tool_result_text_handles_quotes_in_query():
    text = ('Web search results for query: ""paid" GRE course "didn\'t help""\n\n'
            'Links: [{"title":"A three word title","url":"https://a.test/x"}]\n\nBased on the search results, blah.')
    parsed = harvest.parse_tool_result_text(text)
    assert parsed == {"query": Q2, "links": [{"title": "A three word title", "url": "https://a.test/x"}]}
    assert harvest.parse_tool_result_text("Not a search result") is None
    line = json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": text}]}})
    assert harvest.parse_transcript_line(line)[0]["query"] == Q2
    assert harvest.parse_transcript_line("not json {") == []


def test_cli_harvest_reports_and_exit_codes(run, cli):
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(TRANSCRIPTS))
    assert r.returncode == 2 and "queries.jsonl is missing" in r.stderr
    _queries(run, [{"round": 1, "query": Q1, "kind": "forum"}, {"round": 1, "query": "GRE fees", "kind": "prices"}])
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(TRANSCRIPTS))
    assert r.returncode == 1 and "1. " in r.stderr and "'kind' must be one of" in r.stderr
    _queries(run, [{"round": 1, "query": Q1, "kind": "forum"}, {"round": 1, "query": "GRE fees Hyderabad", "kind": "pricing"}])
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(TRANSCRIPTS))
    assert r.returncode == 0, r.stderr
    assert "1 matched" in r.stdout and "GRE fees Hyderabad" in r.stdout
    assert "Records new: 4" in r.stdout and "Skipped junk titles: 6" in r.stdout
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["command"] == "harvest-search" and e["kind"] == "count" and e["records_new"] == 4 for e in events)
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(run / "nowhere"))
    assert r.returncode == 2 and "Transcripts folder" in r.stderr


# --------------------------------------------------------------------------- rule 1: only the search tool's own output
FABRICATED = "https://example.com/fabricated"


def test_search_shaped_output_of_another_tool_is_never_a_record(run, cli, tmp_path):
    """The fixture holds a Bash result whose stdout is shaped like a search result for Q1 (the model can type
    that). It carries the harness's Bash `toolUseResult` and a tool_use_id that belongs to a Bash tool_use, so
    it is refused and counted; the same text from a WebSearch tool_use is a result."""
    _queries(run, [{"round": 1, "query": Q1, "kind": "forum"}])
    s = harvest.harvest(run, ROOM, transcripts=TRANSCRIPTS)
    assert s["skipped_non_search_results"] == 1 and s["records_new"] == 4
    assert FABRICATED not in {r["url"] for r in _stored(run)}
    # the identity check, line by line
    decoy = f'Web search results for query: "{Q1}"\n\nLinks: [{{"title": "I paid 40k for coaching and still scored 300", "url": "{FABRICATED}"}}]'
    names = {}
    assert harvest.scan_transcript_line(json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "toolu_b", "name": "Bash", "input": {"command": "cat x"}},
        {"type": "tool_use", "id": "toolu_w", "name": "WebSearch", "input": {"query": Q1}}]}}), names) == ([], 0)
    assert names == {"toolu_b": "Bash", "toolu_w": "WebSearch"}
    bash_line = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_b", "content": decoy}]},
                 "toolUseResult": {"stdout": decoy, "stderr": "", "interrupted": False}}
    assert harvest.scan_transcript_line(json.dumps(bash_line), names) == ([], 1)
    read_line = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_w", "content": decoy}]},
                 "toolUseResult": {"type": "text", "file": {"filePath": "x.txt", "content": decoy}}}
    assert harvest.scan_transcript_line(json.dumps(read_line), names) == ([], 1)  # a WebSearch id, but a file-read shape
    unknown = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_zz", "content": decoy}]}}
    assert harvest.scan_transcript_line(json.dumps(unknown), names) == ([], 1)
    good = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_w", "content": decoy}]}}
    results, skipped = harvest.scan_transcript_line(json.dumps(good), names)
    assert skipped == 0 and results == [{"query": Q1, "links": [{"title": "I paid 40k for coaching and still scored 300", "url": FABRICATED}]}]
    # a transcript of only decoys stores nothing and the command says so
    tdir = tmp_path / "decoys"
    tdir.mkdir()
    common.write_jsonl(tdir / "s.jsonl", [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "toolu_b", "name": "Bash", "input": {}}]}},
                                          bash_line, unknown])
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(tdir))
    assert r.returncode == 0, r.stderr
    assert "Records new: 0." in r.stdout and "Skipped non-search results: 2" in r.stdout
    assert FABRICATED not in {r["url"] for r in _stored(run)}
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["command"] == "harvest-search" and e["kind"] == "count" and e["skipped_non_search_results"] == 2 for e in events)


# --------------------------------------------------------------------------- rule 5: a person's page is never a record
def test_profile_pages_are_never_stored_and_social_titles_lose_the_name(run, cli, tmp_path):
    profiles = {
        "Priya Sharma - GRE Verbal Tutor - Magoosh | LinkedIn": "https://in.linkedin.com/in/priya-sharma-1a2b3c",
        "Priya Sharma's answer to What is the best GRE coaching in Hyderabad? - Quora": "https://www.quora.com/profile/Priya-Sharma-12",
        "Priya Sharma (@priya_s) / X": "https://x.com/priya_s",
        "Rahul Verma - YouTube": "https://www.youtube.com/@rahulverma",
        "Rahul Verma | Facebook": "https://www.facebook.com/rahul.verma.9",
    }
    posts = {
        "Priya Sharma's answer to What is the best GRE coaching in Hyderabad? - Quora": "https://www.quora.com/What-is-the-best-GRE-coaching/answer/Priya-Sharma-12",
        "Priya Sharma on LinkedIn: GRE coaching fees are a scam": "https://www.linkedin.com/posts/priya-sharma_gre-activity-1",
        "Rahul Verma on X: \"paid 40k for coaching, scored 300\"": "https://x.com/rahulverma/status/123",
        "GRE quant plateau: what finally worked - YouTube": "https://www.youtube.com/watch?v=abc",
    }
    links = [{"title": t, "url": u} for t, u in list(profiles.items()) + list(posts.items())]
    tdir = tmp_path / "t"
    tdir.mkdir()
    common.write_jsonl(tdir / "s.jsonl", [{"type": "user", "message": {"content": []},
                                          "toolUseResult": {"query": "gre coaching hyderabad", "results": [{"content": links}]}}])
    _queries(run, [{"round": 1, "query": "gre coaching hyderabad", "kind": "forum"}])
    r = cli("harvest-search", "--room", ROOM, "--run", "2026-09-26", "--transcripts", str(tdir))
    assert r.returncode == 0, r.stderr
    assert "Records new: 4." in r.stdout and "Skipped profile pages: 5 (a person's page is never stored)" in r.stdout
    stored = _stored(run)
    assert {x["url"] for x in stored} == set(posts.values())
    assert [x["text"] for x in sorted(stored, key=lambda x: x["meta"]["order"])] == [
        "[name]'s answer to What is the best GRE coaching in Hyderabad? - Quora",
        "[name] on LinkedIn: GRE coaching fees are a scam",
        "[name] on X: \"paid 40k for coaching, scored 300\"",
        "GRE quant plateau: what finally worked - YouTube",
    ]
    raw = (run / "03_listen" / "raw" / ROOM / "websearch.jsonl").read_text(encoding="utf-8") + r.stdout + r.stderr
    for needle in ("Priya", "Sharma", "Rahul", "Verma", "linkedin.com/in/", "quora.com/profile", "x.com/priya_s", "youtube.com/@", "facebook.com/rahul"):
        assert needle not in raw, needle
    events = [e for e in common.read_jsonl(run / "runlog.jsonl") if e["command"] == "harvest-search" and e["kind"] == "count"]
    assert events[-1]["skipped_profile_pages"] == 5
    # the store refuses a profile URL from any adapter too
    out = records.store_records(run, ROOM, "hackernews", [{"url": "https://news.ycombinator.com/user?id=pg", "text": "a profile page with words", "date": None, "meta": {}}])
    assert out == {"new": 0, "duplicates": 0, "skipped_empty": 0, "skipped_profile": 1, "new_ids": [], "file": out["file"]}
