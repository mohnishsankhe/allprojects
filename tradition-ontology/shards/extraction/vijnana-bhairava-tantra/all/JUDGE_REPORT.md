# Vijñāna Bhairava Tantra: Role J judge spot-check and promotion (all 162 segments)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Judge: onto-judge (J), 2026-09-29 (Asia/Kolkata). Input: `single/`, which has 167 teachings (162 verse entries plus ch1, three section entries and the thesis), 112 practices, 20 terms, 9 concepts, 3 obstacles, 5 phenomenology entries and 132 skeleton decisions. I judged against the GRETIL IAST segments. I consulted no translation and no commentary.

## Outputs
- /home/user/allprojects/tradition-ontology/shards/extraction/vijnana-bhairava-tantra/all/final/ holds the same 7 files as single/.
  - Teachings: `verification.level` is "text-verified" and `protocol` is "insight-p1-single+spot".
  - Each teaching has `fidelity` {status passed|fixed, checked_by "J", date, mode "individually-checked", note = evidence}, plus a `verification.checks` record.
  - Entities keep level "sourced" and get a `verification.checks` record (phase J).
- /home/user/allprojects/tradition-ontology/shards/extraction/vijnana-bhairava-tantra/all/fidelity.jsonl has 183 lines: 167 teachings, 12 practices, 1 term and 3 skeleton decisions. Each line records:
  - id, criterion, verdict (pass/fail), status, fix, and evidence quoting the Sanskrit;
  - file and line in single/;
  - `original_matches_segment`, `in_random_sample` and stratum, `low_confidence`, `restricted_review`.
- Validation: `python3 scripts/validate_shard.py shards/extraction/vijnana-bhairava-tantra/all/final` gives 0 errors and 1 warning (REPORT.md missing).
- Scratch files, including the verdict ledger and build script, are in /tmp/claude-0/-home-user-allprojects/2c0e32b7-c920-5af7-bfe1-3ee59e322221/scratchpad/judge-vbt/.
- I wrote nothing else in the project and ran no git.

## Protocol and results
1. **Code check of originals.** All 162 verse `original.text` values equal the segment `iast` exactly. All 162 segments are covered, with no duplicate ids. All 161 linked ids exist, either in the shard or in data/.
2. **Random sample.** Seed "20260929", n = ceil(10% of 167) = 17. I split the 167 entries by verse range, with each section entry counted in its range:

   | Stratum | Entries | Sampled | Result |
   |---|---|---|---|
   | Frame (1–23) | 24 | 2 | 1 of 2 pass |
   | Dhāraṇās (24–138) | 116 | 12 | 11 of 12 pass |
   | Closing (139–162) | 25 | 3 | 3 of 3 pass |
   | ch1 and thesis | 2 | 0 | not in sample |

   - Sampled refs: 10, 11, 46, 56, 64, 66, 83, 87, 97, 102, 106, 122, 123, 126, 148, 149, 157.
   - Overall: 15 of 17 = 88.2%, below 95%.
   - Failures: 11 negated "Bhairava" itself, although pāda b 'śabdarāśir na bhairavaḥ' means "Bhairava is not the mass of sounds". 102 rendered indrajāla as "Indra's net" instead of a conjurer's magic show.
   - Because the sample failed, I checked every entry individually.
3. **Targeted sets (also covered by the full check).**
   - All 23 low-confidence entries: 5 fixed (19, 25, 48, 55, 99).
   - The 18 restricted flags: all confirmed. 28 and 36 needed paraphrase fixes.
   - 17 restricted-adjacent entries found by code (Sanskrit and English keyword scan, triaged by reading): 19, 24, 25, 26, 37, 52, 53, 62, 72, 74, 110, 115, 118, 136, 149, 154, 156. Of these, 26 is newly flagged and the other 16 are confirmed unrestricted.
   - Union of sample, low-confidence and restricted/adjacent: 59 entries, 10 of them fixed. The full check found 12 more fixes outside that set.

## Fixes (22 teachings)
**Sense errors**
- **11:** Bhairava is now the subject: "that one, Bhairava, is not the ninefold, not the mass of sounds…".
- **4, 12:** 'candrārdhanirodhikāḥ' is plural, so it names two items, "the half-moon and the nirodhikā", not "the arrester of the half-moon". 'anacka' means "vowelless", not "beyond the vowel".
- **9, 102:** śakra-/indrajāla means a magic show. Your own concepts, the practice name and v.133 already say this.
- **19:** 'jñānasattāyāṃ … praveśane' means "a beginning for entering into the being of knowledge", not "only in the presence of knowledge".
- **23:** 'parā devi' cannot be an address, because the Goddess is the speaker. It is the subject: how the supreme Goddess becomes the entrance. The earlier paraphrase left it out.
- **25:** 'bhairavyā' is instrumental, so the form of Bhairava is disclosed *through* Bhairavī, not "the form of Bhairava and Bhairavī". I also removed a supplied instruction ("attend") and an unstated gloss ("the two ends of the breath").
- **48:** the sandhi 'dhyāyann adhyeya-' fixes the compound as a-dhyeya, "what is not an object of meditation". The note's alternative is impossible.
- **99:** 'evambhāvī śivaḥ' means "one who contemplates thus is Śiva", not "Śiva is of such a nature".

**Wrong addressee**
- **47, 58:** the vocatives mṛgekṣaṇe and mahādevi address the Goddess, not the practitioner.

**Additions or imported readings**
- **1:** "heard from the god" was added; 'deva' is a vocative.
- **5:** a question was turned into an assertion.
- **28:** "(breath-)power" narrowed the verse, which says only "that power".
- **36:** "looking at a point" misread 'dṛṣṭe bindau', which means "when a point is seen". The entry stays summary-only.
- **55:** "first thick then weak" added a sequence; the verse says "thick and weak".
- **135:** "[world]" was inserted; the referent of 'idam' is unstated.

**Links and structure**
- **153:** removed the link to cpt:trika-triad. Here 'parāparaḥ' is a masculine adjective, and the entry's own note says so.
- **ch1:** "each" means ends on a result, but 103, 106, 110, 134 and 135 state none. Now "most".
- **sec-24-138:** the note's list of restricted verses now includes 26.

**Propagated to entities**
- Practices (method_summary / signs_of_progress): dhāraṇā 2, 3, 5, 13, 23, 24, 31, 34, 74, 77, 109.
- Practice names that did not match their verse:
  - dhāraṇā 21 said "above" where 'pṛṣṭha' means behind;
  - dhāraṇā 31 said "then";
  - dhāraṇā 13 added "between the brows".
- trm:maya-trika: its definition quoted v.9 with the old wording; now aligned.

**Skeleton decisions**
- 48 and 99 changed from correct to upgrade: the skeleton's readings are the grammatical ones.
- 26 has a note added about the new restricted flag.
- All 132 `replaced_by` values exist, and every skeleton teaching of this source has a decision.

In several places the fixes return to the skeleton's reading, where the extractor's departure from it was wrong: 2–6, 7–10, 47, 48, 58, 99, 102.

## Restricted policy (CLAUDE.md rule 11)
- **The 18 flagged entries are confirmed:** 27–31, 36, 64, 66–70, 77, 89, 93, 111, 113, 114.
  - All are summary-only, with no steps, counts or durations. The 'muṣṭitraya' measure at 29 is omitted.
  - At 30, "twelve" names the sequence (kramadvādaśaka); it is not a count to perform.
  - The only digits in restricted paraphrases are verse cross-references.
  - Practice flags match the teaching flags; there are now 19 restricted teachings and 19 restricted practices.
- **24:** no verb of holding. It names the two places where the breaths arise and "filling" there. Unrestricted, confirmed.
- **25:** 'anivartanāt' is an ablative noun. It describes the breath's non-return, a pause, inside or outside, with no instruction verb, count or duration. Unrestricted, confirmed.
- **26 is newly flagged restricted, as a precaution.**
  - 'na vrajen na viśec chaktir marudrūpā' uses optatives with the breath-power as subject.
  - Read descriptively, it describes the pause. The same verbs describe the natural breath at v.154, which favours this reading.
  - Read as an injunction, it says the breath should neither go out nor come in, which is an instruction to stop the breath.
  - Following "flag if the Sanskrit may instruct holding" and the conservative-option rule, I flagged it.
  - To reverse it, change `restricted` on tea:…:26 and prc:vbt-dharana-3.
- **The other adjacent entries are confirmed unrestricted:**
  - 19 and 110: fire similes.
  - 37, 52, 53, 149: imagined or inner fire.
  - 62 ('niruddhā cit') and 74 ('dhārayet'): consciousness and the mind, not the breath.
  - 72: 'pāna' is just "drinking", and no intoxicant is named.
  - 118: hunger is named only as an occasion, not fasting.
  - 136: saṃgama here means "contact".
  - 154: the breath's natural movement.
  - 156: the 21,600 figure is the text's description, not a counting instruction.
  - 115: looking down into a pit; not a restricted category, left for the practice layer.

## Open points for the orchestrator
- **Template phrases accepted as a convention.** When a verse has only a participle or statement, the extractor still writes "the practitioner is asked to…" (e.g. 38, 87, 135) or "implicitly asked…" (73, 86, 100, 110, 116–118, 124, 131). I passed these where the phrase only restates the verse. I fixed them where they added content (25, 26). A later pass could replace the phrase with "the verse describes…".
- **Mild glosses I passed.** "natural sound" (145, and in trm:nada-trika), "natural japa" (note at 156), and "natural movement as breath" (sec-139-162).
- **Text statements to keep out of user-facing material.** 140–141 (powers, "no age and no death") and 51/107 ("in days") are recorded as the text's statements. They must not reach user-facing material as claims or predictions.
- **Practice-layer safety items.** 76 (space lit by the sun), 115 (standing above a pit), 83 (moving seat).
- **Merge risk.** Skeleton prc:vbt-dharana-3 in data/ has no restricted flag. Check that the merge carries `restricted: true` and the new method_summary, as the extractor also noted for the other restricted ids.

## Not checked, or checked only partly
- My fidelity judgements rest on my own reading of the Sanskrit. I compared against no Devanāgarī text, independent edition or commentary, and GRETIL typos are kept as they are.
- Claims about KSTS numbering (163 verses) and the Kaumudī recension (in notes) are not verified here.
- The fixed entries have not had a second reader. The 11 sense-error entries listed under "Sense errors" (4, 9, 11, 12, 19, 23, 25, 48, 99, 102, plus 26) are worth a pass from the misreading hunter.
- I did not re-derive the dhāraṇā numbering (the 112 skeleton ids); I only checked that each practice matches its verse or verses.
