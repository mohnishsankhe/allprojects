# Dhammapada single extraction (Role S), chunk "all"
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Files are in shards/extraction/dhammapada/all/single/. Scripts are in shards/extraction/dhammapada/all/_gen/S/: lib.py, ents.py, ents2.py, v01–v09.py, chapters.py, build.py, skel.py. Running build.py then skel.py regenerates everything.

## Coverage
- 423 verse teachings, one per segment, at tea:dhammapada:<n>.
- 26 chapter entries (tea:dhammapada:ch1 to ch26) with the verse ranges and movements of each vagga.
- 1 thesis entry (tea:dhammapada:thesis), decided by the six marks with verse citations.
- New entities: 217 terms, 1 concept (cpt:mano-pubbangama), 10 obstacles and 10 practices.
- 38 of the new ids are homonym-specific ids ending in "-pali".
- Verses 1–99 came from the earlier draft. I re-read all of them against the Pali. I kept the paraphrases, corrected two notes (30 and 97), and rebuilt every link with the new resolver.
- Verses 100–423 are new.

## Checks done
- original.text is copied by code from the segment. It includes the segment's own frame text: the commentarial story-title at the start, and the vagga colophon at the end. A note on each affected entry says so.
- Segment 416 carries the verse twice. Segment 423 carries the edition's closing colophon and tables. Both have manual notes.
- Rule 1 (homonyms):
  - I did not link an existing id unless its data/ entry has a definition or lineage from early-buddhism, theravada or mahavihara.
  - Existing ids that failed that test got a sense-specific new id: trm:papa-pali, trm:dama-pali, trm:deva-pali, trm:mara-pali, trm:yama-pali, trm:sanga-pali, trm:punna-pali, prc:ahimsa-pali, obs:raga-pali, obs:soka-pali, obs:restless-mind-pali, obs:mamatva-pali and others (38 in all).
  - Where the existing entry was Buddhist but narrower or different in sense, I used distinct slugs: trm:ayu-lifespan, trm:bala-strength, trm:bala-fool, trm:vanna-beauty, trm:sota-stream.
  - I left cpt:eight-lokadhamma, obs:ten-fetters, obs:three-akusala-mula, trm:loka and cpt:tanha unlinked, because the verse names a part of them or something different.
  - The 134 reused existing ids were each checked against the printed Buddhist definition (list in _gen/S/reused_ids.json).
  - These reused ids are the ones I would ask the judge to re-check (definition snippet closest to a different sense): trm:indriya, trm:sankhara, trm:kayagatasati (def is Visuddhimagga-based), trm:uddhamsota (def is from Thig 1.12), trm:gantha, trm:chanda (def is the wholesome wish; Dhp uses it neutrally), trm:bhavana.
- Rule 2 (commentary):
  - Commentarial readings appear only in notes, each labelled "commentators' reading (not in the verse)".
  - Cases: 153-154 (awakening frame), 218, 294-295 (riddle images), 339 (thirty-six streams), 344, 370 (the three fives), 384, 385, 254-255 (bāhira), 157 (three yāmas), 240, 97, 30 (Maghavā as Sakka).
  - Story titles are only noted as commentarial frame text.
- Links: an automated check keeps a link only if a key pattern for that id matches the verse text, with the story title and colophon stripped. 117 links inherited from the drafts were dropped this way. Examples: the khanti and mettā links on 3-5, the noble-eightfold-path link on 11-12, and the arahant link on 90-96. Obstacle and practice links stand only where the verse names them. The dana, dama and ahimsa practice links are dropped on verses that only describe the act (e.g. 129-132).
- Dangerous practices: 141 (fasting, nakedness, squatting) and 308 (iron ball) are recorded as what the verse says, with a note that the verse recommends neither. No restricted practice is described step by step.
- No diagnosis, cure or health claim. 198, 203 and 204 carry notes that the verse names ātura, jighacchā and ārogya without making a health claim.

## Skeleton decisions
- Upgrade (16): 5, 21, 35, 103, 142, 160, 165, 183, 184, 197, 223, 265, 276, 282, 372, 388, 396 (a count of 17 by this list; the tally of 16 above should be read as upgrade 17, correct 5).
- Correct (5): 1-2, 153-154, 203-204, 277-279 and 70.
  - The first four are merged refs: the skeleton joined verses that the text keeps separate.
  - 70 is corrected because prc:acelaka-vata, obs:bala-tapa and trm:tapas are not in the verse.
- Retire: none.

## Low or moderate points worth the judge's attention
- 6 (yamāmase), 209 (yoga and ayoga), 218 (anakkhāta, uddhaṁsota), 240 (atidhonacārī), 302, 339, 341, 370 (the three fives), 384 (two dhammas), 385 (pārāpāra), 389 (yassa muñcati): construal is uncertain or disputed.
- 72 (ñattaṁ), 97, 294, 295: the paraphrase is literal and does not decide the riddle or the double sense.
- Moderate entries that turn on a construal (all noted): 143 (apabodheti niddaṁ), 154, 156, 157, 166 (attadattha), 193, 269, 313, 324, 344, 345, 352.
- The fifteen "low" ids above are the mandatory judge sample.

## Not done or limited
- No teachers, disputes, paths or phenomenology entries. The persons named in the verses are only Maghavā, Yama, Māra, Atula (address, verse 227) and the elephant Dhanapālaka, and none is written as a teacher entity.
- Entities are level "sourced", confidence "moderate". Term definitions are short glosses "as used in Dhp x, y, z", not lineage-level definitions. No equivalents were written between the "-pali" ids and the existing homonyms, so the interpretation layer can add them.
- Chapter and thesis entries have no original text.
- The Sujato English was consulted only as a check, and only where I was unsure (about 15 verses plus a random sample of 14 at the end).
- Random 14-verse comparison found no divergences; this is not a substitute for the judge's 10% sample.
- The "Upgrade (16)" figure in the summary lines is 17 by count. Skeleton decisions are 22 in total, made up of 17 upgrade and 5 correct.
