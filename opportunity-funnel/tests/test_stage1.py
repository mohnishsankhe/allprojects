import json

import pytest

import common
import stage1

LENSES = ["life_stage", "profession", "transition", "obligation", "business_type", "identity_community"]


def make_room(slug, lens, origin="generated", name=None, where_url=None, ladder_steps=3, ventures=(),
              duplicate_of=None, geography=("IN",), confidence="moderate"):
    where_url = where_url or f"https://forum.test/{slug}/"
    return {
        "slug": slug,
        "name": name or f"Crowd {slug.replace('-', '')}",
        "lens": lens,
        "origin": origin,
        "who": "who they are",
        "where": [{"name": f"forum for {slug}", "url": where_url}],
        "who_pays": "they pay themselves",
        "size": {"value": 1000, "unit": "people", "tag": "estimate", "reasoning": "a guess"},
        "ladder": [{"step": i, "problem": f"problem {i}", "price_text": "$10", "url": "https://p.test/x"} for i in range(1, ladder_steps + 1)],
        "geography": list(geography),
        "venture_overlap": list(ventures),
        "duplicate_of": duplicate_of,
        "reasoning": "same situation, gather in one place",
        "confidence": confidence,
    }


def write_part(run, name, rooms, wrap=True):
    p = run / "01_rooms.parts" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    common.write_json(p, {"rooms": rooms} if wrap else rooms)
    return p


def full_set(per_lens=14):
    rooms = []
    for lens in LENSES:
        for i in range(1, per_lens + 1):
            rooms.append(make_room(f"{lens.replace('_', '-')}-{i}", lens))
    return rooms


def write_full_set(run, per_lens=14):
    rooms = full_set(per_lens)
    for lens in LENSES:
        write_part(run, f"{lens}.json", [r for r in rooms if r["lens"] == lens])
    return rooms


def test_merge_counts_render_and_determinism(run, cli):
    write_full_set(run)
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Rooms: 84 in, 84 kept, 0 removed." in r.stdout
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    assert data["status"] == "ok" and data["counts"]["kept"] == 84
    assert data["counts"]["by_lens"] == {lens: 14 for lens in LENSES}
    assert data["parts"] == [f"{lens}.json" for lens in LENSES]
    assert all(room["status"] == "kept" for room in data["rooms"])
    assert data["rooms"][0]["lens"] == "life_stage" and data["rooms"][-1]["lens"] == "identity_community"
    md = (run / "01_rooms.md").read_text(encoding="utf-8")
    assert md.startswith("# Stage 1: rooms") and "| life_stage | 14 | 8 | yes |" in md
    assert "Geography is written down but never used as a filter." in md
    first_json = (run / "01_rooms.json").read_bytes()
    first_md = (run / "01_rooms.md").read_bytes()
    r2 = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r2.returncode == 0
    assert (run / "01_rooms.json").read_bytes() == first_json and (run / "01_rooms.md").read_bytes() == first_md
    # without --merge-parts the file is re-checked and stays identical
    r3 = cli("rooms", "--run", "2026-09-26")
    assert r3.returncode == 0 and (run / "01_rooms.json").read_bytes() == first_json
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "count" and e["command"] == "rooms" and e["rooms_kept"] == 84 for e in events)


def test_validation_lists_every_problem_and_never_checks_geography(run, cli):
    rooms = write_full_set(run)
    bad = make_room("bad-room", "profession")
    bad["slug"] = "Bad Room"
    bad["where"] = []
    bad["venture_overlap"] = ["v9"]
    bad["confidence"] = "sure"
    bad["ladder"] = [{"step": 2, "problem": "x"}, {"step": 1, "problem": ""}]
    bad["size"] = {"value": 10, "tag": "measured"}
    bad["origin"] = "dreamed"
    bad["geography"] = "anything at all, even nonsense"  # never checked
    ok_geo = make_room("geo-room", "profession", geography=("Mars", "GLOBAL", "not-a-code"))
    write_part(run, "gap_profession.json", [bad, ok_geo])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1, r.stdout
    err = r.stderr
    for needle in ("'slug' 'Bad Room' must use lowercase", "'where' must be a non-empty list",
                   "venture_overlap id 'v9' is not in config/ledger.yaml", "'confidence' must be high, moderate or low",
                   "ladder step 1: 'step' must be 1", "ladder step 2: 'problem' is missing",
                   "a measured number needs a 'url' or 'record_ids'", "size: 'unit' is missing",
                   "'origin' must be generated, gap_pass or external"):
        assert needle in err, needle
    assert "gap_profession.json: room 1 (Bad Room)" in err
    assert "geography" not in err.lower()
    assert not (run / "01_rooms.json").exists()
    # the odd geography values pass once the rest is fixed
    write_part(run, "gap_profession.json", [ok_geo])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    geo = next(x for x in data["rooms"] if x["slug"] == "geo-room")
    assert geo["geography"] == ["Mars", "GLOBAL", "not-a-code"] and len(data["rooms"]) == len(rooms) + 1


def test_graveyard_removes_dead_rooms_unless_revived(froot, run, cli):
    write_full_set(run)
    common.append_graveyard("2026-09-01", 2, "room:profession-3", "no reach entry matches")
    common.append_graveyard("2026-09-01", 2, "room:transition-2", "dead once")
    common.append_graveyard("2026-09-01", 2, "room:crowd-obligation5", "matched by normalized name")
    gy = froot / "graveyard.md"
    gy.write_text(gy.read_text(encoding="utf-8").replace(
        "- 2026-09-01 | stage 2 | room:transition-2 | dead once",
        "- 2026-09-01 | stage 2 | room:transition-2 | dead once\n  - new evidence 2026-09-20: a thread with 40 buyers https://x.test/t"),
        encoding="utf-8")
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    kept = {x["slug"] for x in data["rooms"]}
    assert "profession-3" not in kept and "obligation-5" not in kept and "transition-2" in kept
    removed = {x["slug"]: x for x in data["removed"]}
    assert removed["profession-3"]["status"] == "graveyard" and "no reach entry matches" in removed["profession-3"]["reason"]
    assert removed["obligation-5"]["status"] == "graveyard"
    assert "removed profession-3: graveyard" in r.stdout
    assert "## Removed rooms (2)" in (run / "01_rooms.md").read_text(encoding="utf-8")


def test_exact_duplicates_keep_first_by_lens_then_origin(run, cli):
    write_full_set(run)
    # same slug in a later lens's generated file and an earlier lens's gap file: lens order wins
    write_part(run, "gap_life_stage.json", [make_room("shared-slug", "life_stage", origin="gap_pass", name="Gap copy")])
    write_part(run, "profession.json", [make_room("shared-slug", "profession", name="Generated copy")]
               + [r for r in full_set() if r["lens"] == "profession"])
    # same normalized name, different slugs, same lens: generated beats gap_pass
    write_part(run, "gap_obligation.json", [make_room("obligation-99", "obligation", origin="gap_pass", name="CROWD   Obligation1!")])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    kept = {x["slug"]: x for x in data["rooms"]}
    assert kept["shared-slug"]["lens"] == "life_stage" and kept["shared-slug"]["origin"] == "gap_pass"
    assert "obligation-99" not in kept and "obligation-1" in kept
    removed = {(x["slug"], x["status"]): x for x in data["removed"]}
    assert removed[("shared-slug", "duplicate")]["of"] == "shared-slug" and removed[("shared-slug", "duplicate")]["lens"] == "profession"
    assert removed[("obligation-99", "duplicate")]["of"] == "obligation-1"
    assert data["counts"]["kept"] == 85


def test_duplicate_of_removes_room_and_bad_target_is_an_error(run, cli):
    write_full_set(run)
    write_part(run, "gap_transition.json", [make_room("transition-dup", "transition", origin="gap_pass", duplicate_of="transition-1")])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    assert "transition-dup" not in {x["slug"] for x in data["rooms"]}
    rem = next(x for x in data["removed"] if x["slug"] == "transition-dup")
    assert rem["status"] == "duplicate_of" and rem["of"] == "transition-1"
    write_part(run, "gap_transition.json", [make_room("transition-dup", "transition", origin="gap_pass", duplicate_of="no-such-room")])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "duplicate_of 'no-such-room' is not a slug in the parts" in r.stderr


def test_near_duplicates_are_listed_not_removed(run, cli):
    write_full_set(run)
    write_part(run, "gap_profession.json", [
        make_room("ib-analyst-recruiting-students", "profession", origin="gap_pass",
                  name="Students recruiting for investment banking analyst roles"),
        make_room("ib-summer-analyst-recruits", "profession", origin="gap_pass",
                  name="Students recruiting for investment banking summer analyst roles"),
        make_room("shares-a-place", "profession", origin="gap_pass", name="A totally different crowd",
                  where_url="https://www.forum.test/profession-2"),
    ])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    pairs = {(n["a"], n["b"]): n["why"] for n in data["near_duplicates"]}
    assert ("ib-analyst-recruiting-students", "ib-summer-analyst-recruits") in pairs
    assert "names share" in pairs[("ib-analyst-recruiting-students", "ib-summer-analyst-recruits")]
    assert pairs[("profession-2", "shares-a-place")] == "same place: forum.test/profession-2"
    assert len(data["near_duplicates"]) == 2 and data["counts"]["kept"] == 87
    assert "2 near-duplicate pair(s) to review" in r.stdout
    assert "set `duplicate_of` on the weaker one" in (run / "01_rooms.md").read_text(encoding="utf-8")
    assert stage1.jaccard({"a", "b", "c"}, {"a", "b", "d"}) == pytest.approx(0.5)
    assert stage1.name_tokens("The engineers in India, for the GRE") == {"engineers", "india", "gre"}


def test_count_ranges_fail_unless_dry_run(run, cli, h, froot):
    write_full_set(run, per_lens=10)  # 60 rooms: below 80
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1
    assert "60 rooms kept; the run needs at least 80" in r.stderr
    assert (run / "01_rooms.json").exists()  # written anyway so the gap pass can read it
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    assert data["status"] == "counts_out_of_range" and len(data["count_problems"]) == 1
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26", "--dry-run")
    assert r.returncode == 0 and "warning (dry run): 01_rooms.json: 60 rooms kept" in r.stdout
    # a lens below its minimum, and too many rooms
    h.set_rule(froot, "stage1", "min_rooms_per_lens", 12)
    write_full_set(run, per_lens=14)
    write_part(run, "profession.json", [r for r in full_set(14) if r["lens"] == "profession"][:11])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "lens profession has 11 rooms; it needs at least 12" in r.stderr
    h.set_rule(froot, "stage1", "rooms_max", 70)
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "the maximum is 70" in r.stderr


def test_part_order_and_missing_inputs(run, cli):
    lenses = stage1.lens_order()
    names = ["gap_transition.json", "external.json", "zzz_other.json", "transition.json", "life_stage.json", "gap_life_stage.json"]
    ordered = sorted(names, key=lambda n: stage1.part_order_key(n, lenses))
    assert ordered == ["life_stage.json", "transition.json", "gap_life_stage.json", "gap_transition.json", "external.json", "zzz_other.json"]
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 2 and "No part files in runs/2026-09-26/01_rooms.parts/" in r.stderr
    r = cli("rooms", "--run", "2026-09-26")
    assert r.returncode == 2 and "01_rooms.json is missing" in r.stderr
    write_part(run, "life_stage.json", {"not": "a list"}, wrap=False)
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "needs a 'rooms' list" in r.stderr


def test_lens_mismatch_is_a_warning_and_external_origin_is_accepted(run, cli):
    rooms = write_full_set(run)
    write_part(run, "external.json", [make_room("from-founder", "obligation", origin="external")])
    write_part(run, "gap_profession.json", [make_room("odd-lens", "transition", origin="gap_pass")])
    r = cli("rooms", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "warning: gap_profession.json: room 1 (odd-lens): lens is transition but the file is for profession" in r.stdout
    data = json.loads((run / "01_rooms.json").read_text(encoding="utf-8"))
    assert data["counts"]["by_origin"] == {"generated": len(rooms), "gap_pass": 1, "external": 1}
    assert data["counts"]["by_lens"]["transition"] == 15
