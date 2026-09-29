_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Role J: spot-check and promotion of MN 10, DN 22 and MN 118 (insight-p1-single+spot), 2026-09-29**

**Step 1: `original.text` checked by code.** 106 teachings carry an original. 105 equal their segment exactly. `tea:anapanasati-sutta:mn118:26/2` is an exact substring of mn118:26. The 6 ch1/thesis entries have no original. There were no mismatches, so nothing was fixed. The same code also found:
- no duplicate ids;
- every segment covered (41, 22 and 43);
- every linked id (terms, concepts, practices, obstacles, paths, teachers, cross_refs, rests_on, related) resolves in data/ or these shards.

**Step 2: sample.**
- Seed 20260929. Each text's teachings were split in file order into 5 strata, with one random pick per stratum (10% rounded up, minimum 5).
- MN 10 sample: mn10:8, 14, 30, 36, 44, plus the low entry mn10:2.
- DN 22 sample: dn22:1 (which is also its low entry), 6, 10, 17, 21.
- MN 118 sample: mn118:4, 13, 26/2, 35, 42. It has no low entries.
- No entry touches a restricted practice. No practice carries a `restricted` flag, and the charnel-ground contemplations are not in the restricted list.
- As extras, I also checked the three thesis entries, because the extractor flagged them. They do not count toward acceptance.

Each sampled entry was read against the Pali for:
- faithful paraphrase;
- no commentarial reading presented as the plain sense;
- no modern psychology;
- speaker, tags and types;
- linked ids, including homonyms. `trm:dhatu` is a multi-lineage entry whose early-Buddhist definition is the four elements, so its link from dn22:6 is the right sense.

A code scan of every entry found no modern, psychological, health or prediction wording. The few hits were in `notes` discussing renderings, which is fine. The only content problem it found was "imagines" in `trm:sivathika`.

**Step 3: acceptance.** The random sample was 15 of 15 faithful as written: 5/5 for each text, which is 100% and above the 95% bar. All three batches are accepted in sampled mode.

**Fixes**
- **`tea:anapanasati-sutta:thesis`** (extra, verdict fail, then fixed):
  - The citation "(mn118:30-38)" became "(mn118:30-39)", because the repeated factor sequence ends with the equanimity factor at mn118:39.
  - The text had called mn118:17 (place and posture) "the sutta's own condition". I reworded it so that only mn118:26 is called a condition, since mn118:17 only describes the setting.
  - A `correction_log` was added.
- **`trm:sivathika`** (MN 10 terms, an entity): "the monk imagines seeing" became "as if he saw (seyyathāpi passeyya)". "Imagines" imposed one reading of a phrase the text leaves open. A `correction_log` and a `checks` record with result "corrected" were added.

**Step 4: final/** holds the same 8 files as single/ in each folder.
- **Teachings:** all 113 are `text-verified`, keeping protocol `insight-p1-single+spot`. `fidelity.mode` is set per entry:
  - "individually-checked" for the 19 I read (7 / 6 / 6), each with status passed or fixed;
  - "sampled" for the other 94 (36 / 18 / 40), with a note saying they were not individually read and were promoted on the sample result.
- **Entities:** 142 in total. None was raised in level; each got a J `verification.checks` record:
  - 49 were sense-checked through the sampled teachings, with result partially-confirmed;
  - 92 were checked by code only, with result partially-confirmed;
  - 1 was corrected.
- **Skeleton decisions:** copied unchanged (16, 2 and 5). Every `replaced_by` and `also_replaced_by` exists in final/. Every skeleton teaching of these sources has a decision.

**Step 5: validation.** 0 errors in all three final/ folders. The one warning in each is "REPORT.md missing", which is expected.

**Open points**
1. The dn22:1 paraphrase contains two accurate editorial remarks: "As in MN 10" and "here frame and theme are one segment". Moving them to `notes` is optional; I left them.
2. The mn118:4 type "ethics" is weak but plausible, given the Pavāraṇā setting. I left it.
3. `translation_basis` contradicts itself: it says "no published translation consulted (Sujato English used only as a check)". I did not change it, and it may need rewording across all entries.
4. 94 teachings are verified only through the sample. The moderate-confidence entries the extractor listed were not individually read unless they fell in the sample; the protocol requires only the low ones. Entity content was not fidelity-checked line by line.
5. The extractor's open points still stand:
   - existing data/ entities have `rests_on` pointing to retired skeleton ids, which the merge should remap using skeleton_decisions;
   - the ids newly introduced in these shards need review at merge.
6. `location.ref` "mn118:26/2" keeps the "/2" suffix. That matches 114 existing data/ teachings, so I left it.

I did not run git, and I wrote only `fidelity.jsonl` and `final/` in the three chunk folders. My working scripts are in the session scratchpad, outside the project.

Files:
- /home/user/allprojects/tradition-ontology/shards/extraction/satipatthana-sutta/all/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/satipatthana-sutta/all/final/
- /home/user/allprojects/tradition-ontology/shards/extraction/mahasatipatthana-sutta/all/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/mahasatipatthana-sutta/all/final/
- /home/user/allprojects/tradition-ontology/shards/extraction/anapanasati-sutta/all/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/anapanasati-sutta/all/final/
