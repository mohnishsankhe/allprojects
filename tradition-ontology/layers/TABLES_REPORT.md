_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Outputs**
- `/home/user/allprojects/tradition-ontology/layers/tables/obstacle_correspondence.json`
  - Each row: `{id, title, members[{dx, lens, name, group, term, cites, user_facing}], lenses, grade, grade_basis, links, what_is_shared, what_differs, principle{id, name, reason}, cites, pending_members, user_facing, blocked_by}`.
  - `links` holds the `diagnosis.json` edges among the members.
- `/home/user/allprojects/tradition-ontology/layers/tables/one_truth.json`
  - Top level: `{first_principle{text, verse_in_full, ref, status, original, cites, user_facing}, rows[...]}`.
  - Each row: `{lineage, family, ultimate_view, name_for_the_ultimate, how_the_text_says_it, standpoint, what_it_denies, principle_relating_it, tradition_objections, cites, user_facing, blocked_by}`.
  - The provisional row also has `provisional`, `status` and `candidate_readings`.
- `/home/user/allprojects/tradition-ontology/layers/tables/path_map_correspondence.json`
  - Top level: `{bands, band_notes (B0, B8), maps[{objection_to_alignment{text, cites, user_facing}, principle, stages, user_facing_stages}], rows[{map, stage, gloss, ref, band, band_source, cites, user_facing, blocked_by, band_note, safety_note}], by_band}`.
- Scripts, all in `/home/user/allprojects/tradition-ontology/layers/_gen/tables/`:
  - `derive.py` finds the cross-lens edges and connected groups by code; its output is `derived_edges.json`.
  - `spec_obstacles.py`, `spec_one_truth.py` and `spec_paths.py` hold the reviewed text.
  - `build.py` assembles and validates, and writes `build_report.json`.
  - `validate.py` re-checks the written files on their own.
  - `idx.py` looks up teachings.

**What the code checked**
- Every dx id exists, and each member's lens matches `diagnosis.json`.
- Each row's members are connected by `diagnosis.json` equivalences and span at least two lenses.
- Each row's grade is the weakest cross-lens grade among its links.
- Every row and member has cites, and every cite exists by exact id in `data/teachings`; superseded ids are rejected.
- `user_facing` is true only if every cite is citable.
- Principle ids and names are valid, and lineage ids exist in `lineages.json`.
- Bands are valid, and `by_band` covers each stage row exactly once.
- The prose contains none of the banned words: "contradiction", and psychology or medical words such as depression, anxiety, trauma, therapy, disorder or symptom.
- The bands that objection texts rely on are asserted against `paths.json`, for example Gītā 12.11 at B1 and guṇasthāna 4 at B5 before 5–6 at B1.

**What I could not check**
- I did not re-read `sources_raw/`. The claims rest on the teachings' paraphrases in `data/`, and for the verified ones I read the full paraphrase.
- The app does not read the tables yet. `scripts/check_layers.py` covers only `diagnosis.json` and `practices.json`, not the tables.

**Main blocks on user-facing rows (need text-verification)**
- Ten remaining obstacle, one-truth and path-map rows are held back by skeleton cites:
  - TS 9.28, 9.30–33 and 9.35: the ārta and raudra rows.
  - TS 10.1–2, 5.16 and 5.30: the Jain one-truth row.
  - TS 9.45 and GJK 9–10: the guṇasthāna and TS 9.45 maps.
  - MN 24 (`tea:rathavinita-sutta:9-15`) and Vism 1/2: the seven purifications.
  - Ud 8.3, Vism 16, 16/2 and 18/2: the Theravāda one-truth row.
  - MMK 18.6: the provisional row, which stays non-user-facing anyway.

**Problems found in other files**
- **`config/data_model.md`, B8:** it lists "dharmamegha as culmination" under B8, but YS 4.29 puts dharmamegha before kaivalya (YS 4.34). I placed it at B6 and flagged it in a `band_note`.
- **`diagnosis.json`:**
  - It cites GK 3.35, 3.42 and 3.43 and TS 9.30–9.33 as separate ids, and these are missing from `data/`. Because of this, `gk-laya` and `gk-viksepa` are left out of their rows and listed under `pending_members`.
  - Several of its skeleton Visuddhimagga cites (like 20/2) have now been superseded by page ids.
- **`paths.json`:**
  - The YS eight-limbs stages lost their `rests_on` in the 17:12 merge. I cited YS 3.1–3.3 for dhāraṇā, dhyāna and samādhi, because the data ref points to YS 2.29, which is restricted.
  - In the guṇasthāna map, stages 1–2 have no band, and the band order runs against the Jain order.
  - MN 118 step 12 ("liberating the mind") is placed at B5. The sutta groups it with contemplation of mind, so I recorded this as "not yet reconciled" in the map's objection.

**For onto-deep: the hardest items, with provisional handling**
1. **Self-question (provisional row `ot:provisional-self-question`, `user_facing: false`).**
   - Is there any standpoint, accepted by at least one of the parties from its own texts, on which these can be related as more than "all deny that the body and changing cognitions are the self" (`dsp:is-there-a-self`, RQ-U50-01)?
     - the Jain jīva: TS 2.1 and 2.7; many and body-sized, TS 5.16
     - the Yoga puruṣa: YS 2.20; many, YS 2.22
     - the Upaniṣadic ātman: ChU 6.8.7, BAU 1.4.10
     - the Theravāda not-self: Dhp 279
   - If there is none, should the product only ever show them side by side?
   - The candidate readings recorded are P1, P2 (the Jain synthesis), P4 and P5/P6, each with its rejection.
2. **B7 band.** Does putting kaivalya (YS 4.34), nibbāna / arahant (MN 118:9), the Gītā's "dwelling in me" (12.8) and the Jain Jina in one band imply anything beyond "end of the course"? Each tradition denies the others' end-state. At present `about` says a shared band means only a comparable place.
3. **Negation across traditions.** Can P1-level relate the Heart Sūtra's "in emptiness no attainment" (s6–s7) to the Upaniṣads' neti neti (BAU 2.3.6) and turīya (MāU 7)? The Prajñāpāramitā denies that emptiness is an entity, and the Upaniṣadic and Advaita reading takes the negated as being-consciousness. At present each row relates to the others only through its own principle.
4. **Gītā inclusivism.** Can P3-path be used as a neutral principle when the Gītā's own statement of it is inclusivist? BhG 9.23 says other deities are worshipped "not according to the rule", and 12.5 calls the unmanifest way harder.
5. **Same word, different sense.**
   - Should `oc:avirati` (YB 1.30 greed for objects vs TS 7.1 / 8.1 absence of vows) and `oc:pramada-pamada` stay as correspondence rows at all? Or should they become "homonym" notes, since the Yoga's real counterpart to the Jain vows is the yamas (YS 2.30)?
   - Should the Jain māyā and the Vedāntic māyā (ŚU 4.9–10) be flagged product-wide?
6. **Band placements that run against each tradition's own order.**
   - Gītā 12.11 at B1 inverts BhG 12.12.
   - Guṇasthāna 4 (right view) at B5 comes before 5–6 at B1.
   - Five of the seven purifications are compressed into B4.
   - Should bands be kept for these maps, or should these maps show order only?

**Not changed:** `data/`, `DECISIONS.md`, `PROGRESS.md`, `RUNLOG.md`, `diagnosis.json`, `practices.json`. I did not run git.
