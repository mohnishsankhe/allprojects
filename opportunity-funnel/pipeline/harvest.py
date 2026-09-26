"""`harvest-search`: web-search results from session transcripts -> records.

The model never types record text. This module reads the search tool's own
output from the Claude Code transcript files and stores titles and URLs as
records (source "websearch"). The tool's written summary is never stored.

Public API
----------
    QUERY_KINDS                       allowed values of queries.jsonl "kind"
    SEARCH_PREFIX                     'Web search results for query: "'
    transcripts_dir(override=None) -> Path
        --transcripts, else env FUNNEL_TRANSCRIPTS_DIR, else ~/.claude/projects/
    load_queries(run, room) -> list[dict]
        queries.jsonl lines validated; each gets "query_index" (1-based line position)
    parse_tool_result_text(text) -> dict | None
        {"query", "links": [{"title", "url"}]} from a tool_result string, or None
    parse_transcript_line(line) -> list[dict]
        every search result on one transcript line, in either form
    iter_search_results(root) -> iterator of (path, result)   files sorted, lines in order
    is_junk_title(title) -> bool     empty, a bare domain or URL, or fewer than 3 words
    link_to_record(link, query, rank) -> dict   the record to store (before anonymizing)
    harvest(run, room, transcripts=None) -> dict   summary counts (see cmd)
    register(subparsers)             adds `harvest-search`
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import common
import records
from netfetch import url_date_info

STAGE = 3
SOURCE = "websearch"
QUERY_KINDS = ("forum", "video", "reviews", "qa", "blog", "pricing", "jobs", "official", "phrasing")
SEARCH_PREFIX = 'Web search results for query: "'
_LINKS_MARK = "Links: "
_DECODER = json.JSONDecoder()

_URL_TITLE_RE = re.compile(r"^(?:https?://|www\.)\S+$", re.I)
_DOMAIN_TITLE_RE = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/\S*)?$", re.I)
_WORD_RE = re.compile(r"[^\W_]")


# --------------------------------------------------------------------------- inputs
def transcripts_dir(override=None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("FUNNEL_TRANSCRIPTS_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".claude" / "projects"


def queries_path(run, room: str) -> Path:
    return common.room_dir(run, room) / "queries.jsonl"


def load_queries(run, room: str) -> list:
    p = queries_path(run, room)
    common.require_file(p, f"The listener writes it in mode plan (one line per search: round, query, kind).")
    rows = common.read_jsonl(p)
    errors = []
    out = []
    for n, row in enumerate(rows, 1):
        where = f"{common.rel(p)}: line {n}"
        if not isinstance(row, dict):
            errors.append(f"{where}: must be an object with round, query and kind.")
            continue
        rnd = row.get("round")
        q = row.get("query")
        kind = row.get("kind")
        if not isinstance(rnd, int) or isinstance(rnd, bool) or rnd < 1:
            errors.append(f"{where}: 'round' must be a whole number from 1 (got {rnd!r}).")
        if not isinstance(q, str) or not q.strip():
            errors.append(f"{where}: 'query' is missing or empty.")
        if kind not in QUERY_KINDS:
            errors.append(f"{where}: 'kind' must be one of {', '.join(QUERY_KINDS)} (got {kind!r}).")
        if errors and errors[-1].startswith(where):
            continue
        out.append({"round": rnd, "query": q, "kind": kind, "query_index": n})
    if errors:
        raise common.ValidationErrors(errors)
    return out


# --------------------------------------------------------------------------- transcript parsing
def _links_from_array(arr) -> list:
    links = []
    for x in arr or []:
        if isinstance(x, dict) and x.get("url"):
            links.append({"title": str(x.get("title") or ""), "url": str(x.get("url") or "").strip()})
    return links


def parse_tool_result_text(text: str):
    """Parse 'Web search results for query: "<q>"\\n\\nLinks: [...]'. The summary after the array is ignored."""
    if not isinstance(text, str) or not text.startswith(SEARCH_PREFIX):
        return None
    end = text.find("\n", len(SEARCH_PREFIX))
    if end < 0:
        end = len(text)
    query = text[len(SEARCH_PREFIX):end]
    if query.endswith('"'):
        query = query[:-1]
    idx = text.find(_LINKS_MARK + "[", end)
    if idx < 0:
        return {"query": query, "links": []}
    try:
        arr, _ = _DECODER.raw_decode(text, idx + len(_LINKS_MARK))
    except json.JSONDecodeError:
        return {"query": query, "links": []}
    return {"query": query, "links": _links_from_array(arr if isinstance(arr, list) else [])}


def parse_transcript_line(line: str) -> list:
    """Search results on one transcript line. A line with both forms is read once (the structured one)."""
    if SEARCH_PREFIX[:-1] not in line and '"toolUseResult"' not in line:
        return []
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        return []
    if not isinstance(d, dict):
        return []
    tur = d.get("toolUseResult")
    if isinstance(tur, dict) and isinstance(tur.get("query"), str) and isinstance(tur.get("results"), list):
        links = []
        for item in tur["results"]:
            if isinstance(item, dict) and isinstance(item.get("content"), list):
                links.extend(_links_from_array(item["content"]))
        return [{"query": tur["query"], "links": links}]
    out = []
    msg = d.get("message")
    content = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            inner = block.get("content")
            texts = []
            if isinstance(inner, str):
                texts.append(inner)
            elif isinstance(inner, list):
                for t in inner:
                    if isinstance(t, dict) and isinstance(t.get("text"), str):
                        texts.append(t["text"])
            for t in texts:
                parsed = parse_tool_result_text(t)
                if parsed:
                    out.append(parsed)
    return out


def iter_search_results(root: Path):
    files = sorted(p for p in Path(root).rglob("*.jsonl") if p.is_file())
    for p in files:
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                for line in f:
                    for result in parse_transcript_line(line):
                        yield p, result
        except OSError:
            continue


# --------------------------------------------------------------------------- records
def is_junk_title(title) -> bool:
    t = common.normalize_ws(title or "")
    if not t:
        return True
    if _URL_TITLE_RE.match(t) or _DOMAIN_TITLE_RE.match(t):
        return True
    words = [w for w in t.split() if _WORD_RE.search(w)]
    return len(words) < 3


def link_to_record(link: dict, query: dict, rank: int) -> dict:
    url = str(link.get("url") or "").strip()
    date, precision = url_date_info(url)
    meta = {
        "kind": "search_title",
        "query": query["query"],
        "query_kind": query["kind"],
        "round": query["round"],
        "order": [query["round"], query["query_index"], rank],
        "domain": common.domain_of(url),
        "date_from": "url" if date else "none",
    }
    if date:
        meta["date_precision"] = precision
    return {"url": url, "text": common.normalize_ws(link.get("title") or ""), "date": date, "meta": meta}


def harvest(run, room: str, transcripts=None) -> dict:
    room = common.check_slug(room, "room")
    queries = load_queries(run, room)
    by_text: dict = {}
    for q in queries:
        by_text.setdefault(q["query"].strip(), q)  # the first line wins for a repeated query
    root = transcripts_dir(transcripts)
    if not root.exists():
        raise common.MissingInput(f"Transcripts folder {root} does not exist. Pass --transcripts DIR or set "
                                  f"FUNNEL_TRANSCRIPTS_DIR.")
    existing_urls = {r.get("url") for r in records.load_records(run, room) if r.get("url")}
    seen_urls: set = set()
    matched: set = set()
    new_records: list = []
    links_seen = 0
    duplicates = 0
    skipped_junk = 0
    results_seen = 0
    files: set = set()
    for path, result in iter_search_results(root):
        q = by_text.get(result["query"].strip())
        if q is None:
            continue
        results_seen += 1
        files.add(str(path))
        matched.add(q["query"].strip())
        for rank, link in enumerate(result["links"], 1):
            links_seen += 1
            if is_junk_title(link.get("title")):
                skipped_junk += 1
                continue
            url = str(link.get("url") or "").strip()
            if not url:
                skipped_junk += 1
                continue
            if url in seen_urls or url in existing_urls:
                duplicates += 1
                continue
            seen_urls.add(url)
            new_records.append(link_to_record(link, q, rank))
    stored = records.store_records(run, room, SOURCE, new_records, command="harvest-search")
    duplicates += stored["duplicates"]
    unmatched = [q["query"] for q in queries if q["query"].strip() not in matched]
    return {
        "room": room,
        "queries": len(queries),
        "queries_matched": len(matched),
        "queries_unmatched": unmatched,
        "results_seen": results_seen,
        "transcript_files": len(files),
        "links_seen": links_seen,
        "records_new": stored["new"],
        "duplicates": duplicates,
        "skipped_junk": skipped_junk,
        "new_ids": stored["new_ids"],
    }


# --------------------------------------------------------------------------- command
def cmd_harvest(args) -> int:
    run = common.run_dir(args.run)
    s = harvest(run, args.room, transcripts=args.transcripts)
    print(f"Room {s['room']}: {s['queries']} queries in queries.jsonl; {s['queries_matched']} matched a search "
          f"result in {s['transcript_files']} transcript file(s).")
    if s["queries_unmatched"]:
        print(f"{len(s['queries_unmatched'])} queries had no transcript result yet:")
        for q in s["queries_unmatched"]:
            print(f"  - {q}")
    print(f"Links seen: {s['links_seen']}. Records new: {s['records_new']}. Duplicates: {s['duplicates']}. "
          f"Skipped junk titles: {s['skipped_junk']}.")
    common.log_event(run, STAGE, "harvest-search", "count", room=s["room"], queries=s["queries"],
                     queries_matched=s["queries_matched"], queries_unmatched=s["queries_unmatched"],
                     links_seen=s["links_seen"], records_new=s["records_new"], duplicates=s["duplicates"],
                     skipped_junk=s["skipped_junk"])
    common.log_event(run, STAGE, "harvest-search", "source", room=s["room"], source=SOURCE,
                     records_new=s["records_new"], note="titles and URLs only; the search summary is never stored")
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("harvest-search", help="Store web-search results from session transcripts as records.")
    p.add_argument("--room", required=True, help="room slug")
    p.add_argument("--transcripts", default=None, help="transcripts folder (default ~/.claude/projects or FUNNEL_TRANSCRIPTS_DIR)")
    p.set_defaults(func=cmd_harvest)
