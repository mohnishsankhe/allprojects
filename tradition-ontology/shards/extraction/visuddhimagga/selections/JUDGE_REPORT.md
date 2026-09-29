# Visuddhimagga selections: Role J judge spot-check and promotion
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Files:
- /home/user/allprojects/tradition-ontology/shards/extraction/visuddhimagga/selections/fidelity.jsonl (237 lines: 183 teachings, 54 entities; each has id, verdict, status, fix, evidence with the Pali quoted, sample_role, criteria, seed)
- /home/user/allprojects/tradition-ontology/shards/extraction/visuddhimagga/selections/final/ (teachings, concepts, obstacles, phenomenology, practices, terms, skeleton_decisions)

## Step 1: original text, by code
- All 183 `original.text` spans are exact substrings of their page's IAST. None needed replacing from the segments.
- Every one of the 89 pages has at least one teaching.
- Three spans overlapped the next entry on the same page and covered text their own paraphrase does not cover: 8.p268 (710 characters), 8.p269 (69) and 8.p271 (1,128). I trimmed them by code and logged each change. They are still exact substrings.
- A final code check finds no overlapping spans.

## Step 2: sample
- Seed 20260929; n = max(18, ceil(10% of 183)) = 19, stratified: III 9, IV 2, VIII 3, IX 3, extra pages (XIV, XVII, XX, XXII) 2.
- The random 19: 3.p85, 3.p88, 3.p89/2, 3.p91/2, 3.p95/3, 3.p99/2, 3.p107/3, 3.p112/2, 3.p115, 4.p143/3, 4.p145, 8.p267, 8.p273/3, 8.p279/2, 9.p295, 9.p303/2, 9.p308, 20.p637, 22.p694.
- Also checked:
  - all 13 moderate-confidence entries (there are no low ones);
  - all 8 entries flagged restricted;
  - 14 unflagged entries that touch foulness, body parts, a charnel ground, self-harm or stopping the breath. I found these by code.
- **Result:** 15 of 19 faithful as written (78.9%), below 95%. The four failures are 3.p88, 3.p95/3, 3.p99/2 and 3.p107/3. As the protocol requires, I then checked every entry, so final fidelity mode is "individually-checked".

## Step 3: result of the full check
148 teachings pass and 35 are fixed; every fix has a `correction_log` entry.

**Paraphrase not faithful (18):**
- 3.p85/3: the six grounds of recollection were dropped from the access-only subjects.
- 3.p86: the rapture count was swapped with the happiness count.
- 3.p88: adds "pain-feeling" to the fourth jhāna.
- 3.p93: the named practices (Rathavinīta and the rest) were replaced by "few wishes".
- 3.p95/3: says "two stories"; p.96 continues with at least three.
- 3.p97: says "the elder who had learned in Dhammarakkhita's place"; the elder is Mahā-Dhammarakkhita himself.
- 3.p98/2: "bhāvanīyo" (esteemed) rendered "one who can be developed".
- 3.p99/2: "dhotamakkhitehi pādehi" (feet washed and anointed) rendered "unwashed and oiled".
- 3.p107/3 and 3.p108: "what suits" is not given as the text gives it (open platform, uneven, "turn one away").
- 3.p110: the place names Hatthikucchi Overhang and Mahinda's Cave turned into "a cave in an elephant's belly".
- 3.p114/2: three conditions merged into two.
- 4.p125: "vaṇṇaṃ amuñcitvā" (without letting go of the colour) rendered "leaving the colour aside".
- 4.p143: gives the bronze-bowl simile of p.142 instead of the potter's simile in this span.
- 8.p280: adds "connecting" to "counting and touching".
- 8.p281/2: the second line of the verse is inverted; both lines say "not the object of a single consciousness".
- 9.p306/2: whose anger subsided (the great elder's) was misstated, and the notes wrongly said the text does not say.
- 22.p683: the taints' definition (sensual lust, lust for existence, wrong view, ignorance) was dropped.

**Temperament caution missing (7):** 3.p104/2, 3.p105/2, 3.p106, 3.p106/2, 3.p106/3, 3.p106/4 and 3.p107 give the marks with no caution. I appended the text's own III p.107 caution to their notes ("kevalaṃ ācariyamatānusārena vuttaṃ, tasmā na sārato paccetabbaṃ"). 3.p105 and the six phn:vism-carita-* entities already carried it. The caution applies only to the discerning marks (pp.104–107), not to the "what suits" pages, so I did not add it there.

**Wrong-sense or unsupported links (6):**
- 3.p110/2 and 8.p266/2 linked cpt:five-hindrances, but neither passage mentions them. 8.p266/2 also glossed the Buddha's praise with the Mīmāṃsā term "arthavāda"; I removed it.
- 3.p116/2 linked trm:carita, but the passage is about disposition (ajjhāsaya), not temperament.
- 14.p468, 14.p470 and 14.p471 linked the Vism III temperament entities (phn:vism-carita-*) to the XIV definitions of greed, hate and delusion as mental factors.
- 22.p683 also carried hindrance links that p.683 does not support (checked by search); I removed them as part of its fix.

**Notes error (1):** 3.p114/3 called the four elements a restricted practice. It is not.

**Safety flag (not a fidelity fault):** 3.p116 is faithful, but I added `restricted: true` because the pupils' declarations include stopping the breath until death and grinding the body away.

**Numbers the extractor asked me to check:** all correct.
- 3.p113/2: 22 + 12 + 6 = 40; eight moving objects; 12 and 13 do not occur among devas and in the Brahma world.
- 3.p114: 19 + 1 + 1 + 1 + 18 = 40; 35 open to a beginner.
- 14.p471: 11 + 2 = 13; 12 + 1 = 13; 5; 8.
- 22.p694: all 13 pairings and all 18 principal insights are present and correctly paired.

**Restricted material:** all flagged and touching entries are summary-only; no procedures. The Jātaka mutilations (9.p302/2 and following) are narrative and the notes say so.

**Modern vocabulary scan (by code):** no psychological or clinical terms. The hits are standard renderings such as "personality view" or negations such as "no reader is diagnosed".

## Step 4: final/
- **Teachings:** `verification.level` "text-verified" and protocol "insight-p1-single+spot" on all 183. `fidelity` is {status passed/fixed, checked_by "J", date 2026-09-29, mode "individually-checked", note}.
- **Entities (54):** level unchanged ("sourced"); a J `verification.checks` record on each.
- **Entities corrected (5):**
  - trm:kalyanamitta and prc:kalyanamittata: "able to be developed" became "esteemed (bhāvanīya)".
  - prc:brahmavihara-bhavana: it stated "the fourth jhāna" as the text's plain sense, but the edition prints "catukkajjhānikā". I relabelled it as the extractor's reading.
  - cpt:ten-fetters: the first/second path division was misstated ("coarse" versus "gross").
  - obs:five-hindrances: its source for the hindrances cited p.683–684; narrowed to p.684.
- **Also confirmed:** all 9 practice warnings are verbatim Pali from the cited pages (checked by code with whitespace normalised), and every linked id resolves.
- **skeleton_decisions:** all 19 original `replaced_by` ids exist. I added 5 upgrades, each marked "Added by J", for skeletons inside the selected pages that had no decision:
  - 14/3 → 14.p468
  - 20/2 → 20.p633
  - 20/3 → 20.p637
  - 20/4 → 20.p638
  - 22/3 → 22.p694

  I checked each skeleton against the Pali; all five are accurate. Total now 24.

## Step 5: validation
`validate_shard.py` on final/ gives 0 errors and 1 warning (REPORT.md missing; this text is it).

## Open points for the orchestrator
- **Extractor's report inaccuracies:**
  - Its moderate ids 4.p144/1, 8.p273/3, 8.p277/1 and 9.p308/3 do not exist; the data has 4.p144, 8.p273/2, 8.p277 and 9.p308/2.
  - It says trm:viveka is unlinked, but 4.p143/2 links it; the sense fits.
  - Its list of undecided skeletons omitted the 5 in-range ones above.
- **Skeleton 3/11** is filed under chapter III but is p.118, the opening of chapter IV. It needs an orchestrator correction.
- **No chapter entries:** there are no `tea:visuddhimagga:ch<N>` teachings, although the Role S brief asks for them. I did not add any.
- **E-text readings kept literally** (the printed edition and the PTS variant notes were not compared):
  - 3.p111/2 "catukkajjhānikā", probably catuttha-;
  - 9.p308/2 "purimaṃ disaṃ", probably uparimaṃ;
  - 14.p471 "ekatta-", probably ekanta-;
  - 3.p105 "mānam pi", probably ṭhānam.
- **Merge conflicts to expect:**
  - cpt:first-jhana has category "stages-maps" in the shard but "consciousness-states" in data.
  - trm:vicara and trm:sukha are headed "Sanskrit" in data and "Pali" in the shard. trm:vicara also holds the Advaita "inquiry" sense under the same id as the Pali "sustained thought"; the homonym policy should be decided.
- **Restricted-flag policy:** the 12 unflagged entries that only name foulness or body parts in passing are summary-only, so I left them unflagged. A stricter flag policy is the orchestrator's decision.
- **Minor looseness:** several passing entries carry small wording notes in their fidelity.jsonl evidence, for example 4.p140/2 and obs:kamacchanda ("lust for sense objects" for saṅkapparāga). They do not change the sense and I left them as written.
- **What I could not check:** the printed PTS edition and its variant footnotes; pages outside the selection that entries point to as "continued" (only adjacent pages were read where needed).
- **Process:** the session scratchpad is shared with other agents. A parallel Dhammapada judge overwrote my sample file mid-run. I regenerated it from the seed (the sample was identical) and confirmed my verdict file was intact before building final/.
