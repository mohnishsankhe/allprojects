# Content gate (P5): judge report

Judge: onto-judge (claude-opus-5-5). Packet: `eval/judge/rules/content_review.jsonl` (50 rules-engine drafts, 10 per bucket, 5 formats). Per-post scores, evidence and exact fixes: `eval/judge/content_verdicts.jsonl`. "Lnn" means packet line nn.
Checked by code: claims.scan re-run (0 hits); pairwise 5-gram Jaccard recomputed (max 0.256); `source_line(tid)` exact match; format limits; fix lengths. Checked by reading: all 50 texts against the cited original and paraphrase, and the neighbouring verses in `data/`.
Not run: the AI-label reminder (not exported to the packet; the code sets `body.ai_label`); on-screen timing; the model check (rules engine only).

| criterion | pass | fail |
|---|---|---|
| (a) cites faithfully | 42 | 8 |
| (b) no claims | 49 | 1 |
| (c) no near-duplicates | 48 | 2 |
| (d) idea-specific | 10 | 40 |
| **all of a–d** | **8** | **42** |
| (e) format/voice, note only | 30 | 20 |

Passing posts (8): L3, L8, L15, L16, L19, L20, L35, L40. Passes per bucket: work 2, overthinking 4, sleep 0, loneliness 2, meaning 0.

## Failures and fixes (the full fix text for each post is in the verdicts file)
Posts failing (a), (b) or (c); each also fails (d) unless marked:
- L1 43b7a496 (a,d): the pool tid 17.14-16 resolves to BhG 17.14 (austerity of the body), but the post states 17.15 (speech) under "17.14-16"; the scene is unrelated. Fix: tid → `tea:bhagavad-gita:17.15`; redraft on work scene 12 with a link and a closing.
- L5 8d8fd04e (a,d): "not only the others'" is not in TS 6.10; the link is about handover notes, not the drafts-folder scene. Fix: delete the phrase; scene → work 14.
- L9 ce0be2ff (a,d): "Intensity is not on its list, so a few quiet minutes kept daily fit it well" adds advice, and YS 1.21 speaks of intense ardour. Fix: retire YS 1.14 from the work pool, or rewrite its angle.
- L10 6e62a2ff (c,d): the same idea as L4 (staying even toward praise and blame at work); the link belongs to another scene. Fix: work scene 2, with a link on "enemy and friend".
- L13 f76647f4 (a,d): "fruit is its being experienced" is TS 8.21 but is cited as 8.23; the post implies the replayed worry falls away. Fix: remove TS 8.23 from the overthinking pool.
- L14 3262dfaf (b,d): part 3 says "you will not again come to birth and ageing" with no attribution, so it reads as a promise; the link lists other worries. Fix: delete part 3; rewrite the link for the choice scene.
- L21 d5bbaf87 (c,d): DN22:13 is the same passage as MN10:36 (L15), in the same template sentence; the scene treats bedtime drowsiness as a hindrance. Fix: drop DN22:13 from the sleep pool.
- L30 91a2726f (a,d): "The morning call" reads "arise, awake" literally; the pairing with the night bus rests on a pun. Fix: sleep scene 13, and a link saying it is "not about the alarm ... a call to understanding".
- L34 bbb84031 (a,d): the link secularises the devotees' company in BhG 10.9 and nudges toward faith. Fix: mark it as devotional; closing "Sit with that for a moment."; delete the repeated part 3.
- L47 1ac8dcde (a only): "Not a new identity to build, the sutra says" is not in YS 1.3. Fix: a new link naming "then" and the Buddhist difference.
- L49 95dac2fc (a only): "the teacher does not give orders" is contradicted by BhG 18.65-66. Fix: "Near the end ... Kṛṣṇa hands the choice back".
Posts failing (d) only:
- x_post with no link or closing, so the scene and the teaching just sit side by side: L2, L11, L12, L22, L23, L31 (also praises unchosen solitude, against the BhG 13.11 never-list), L32, L33, L41, L42 (svadharma unexplained), L43. Fix: the exact redrafts in the verdicts file (all 280 characters or fewer, length and claims checked by code).
- Link written for another scene, fixed by a scene swap: L4→work 4; L6→work 11; L17→overthinking 3; L25→sleep 11; L26→sleep 14; L27→sleep 2; L28→sleep 2 (or add a dream scene); L29→sleep 5; L44→meaning 12; L45→meaning 6; L48→meaning 8; L50→meaning 14. Link rewritten for its own scene: L18, L38.
- Stretch or never-list breach: L7 (the lotus leaf recast as workload running off; restore "by sin (pāpa)", scene → work 13); L24 (posture vs a sound; rewrite the link); L36 (the scene has no fear; → loneliness 12); L37 (invites the devotional view; neutral link and closing); L39 (casts missing a friend as the near enemy of compassion; retire the pairing); L46 (a rebirth verse set on a job choice; → meaning 9, plus a Buddhist-difference slide).

## Gate verdict: FAIL
8 of 50 posts pass a–d; the gate needs 50 of 50. Claims (b) is nearly clean and similarity (c) is clean by code, but (d) fails in 40 posts and (a) in 8. Most of the causes are in the templates, so redrafting posts alone will not hold.

## Fixes the drafting templates need (`insight/content.py`, `rules/content/buckets.json`)
1. x_post: never drop the link. Emit scene + short point + citation + link + closing, and add a short point to each pool item instead of cutting the angle. `rules_check` should reject a post with no link or closing (15 of 15 x_posts lack both).
2. Scene binding: each angle is written for one scene, but `pick()` shuffles scenes independently. Add allowed `scenes` to each pool item and draw only from them (17 links name another scene).
3. Citation exactness: a range tid resolves to its first verse (`17.14-16` → 17.14). Reject pool items whose ref differs from the resolved ref, and match the source line exactly rather than as a substring.
4. x_thread part 3 pastes the raw paraphrase: it repeats part 2 in 5 of 10 threads and brought in a "you will" promise (L14). Drop it or rewrite it in the third person, and add a `\byou will\b` check for posts.
5. short_video: the close-reading beat is cut from the start of the paraphrase (L39 read the wrong sentences), and the "where the text stops" beat appears in 1 of 10. long_video: no minutes and no 2–4 points per section (5 of 5).
6. Pool text to correct: the BhG 17.14-16 tid; the YS 1.14 angle; the TS 8.23 point; the BhG 18.63, YS 1.3, BhG 10.9 and TS 6.10 angles; the BhG 5.10 point ("by sin"). Parallel passages sit in different pools: DN22:13 = MN10:36 and DN22:4 = MN10:8.
7. Closings: choose per teaching, not from one generic list ("read your day this way" was put on a devotional verse in L37). `_sentence()` should not produce "'.'." or "—." (6 posts).

(e) note: 20 fail (15 x_posts missing the link and closing; 5 long videos without minutes or points). The 10 carousels and 10 short videos are within limits. The 10 threads are within limits, but 5 repeat part 2.


## Re-run (P6)

Judge: onto-judge (claude-opus-5-5), 2026-09-29. Packet: `eval/judge/rules/content_review.jsonl`: 50 rules-engine posts redrafted from `buckets.json` 2.0, 10 per bucket (3 x_post, 2 x_thread, 2 ig_carousel, 2 short_video, 1 long_video). Per-post scores, evidence and fixes are in `eval/judge/content_verdicts_rerun.jsonl`. "Lnn" means line nn of the new packet; the P5 line numbers above refer to other posts.
Checked by code:
- claims.scan re-run: 0 hits in 50.
- Keyword scan for health, clinical, research, promise and prediction words: the only hits are scene words or the verses' own attributed words.
- Pairwise 5-gram Jaccard recomputed: max 0.316 (L8/L38), same as the packet.
- `source_line(tid)` is printed exactly in all 50, never as a prefix of a longer ref. For every tid, `teaching(tid).id == tid` and the teaching is citable. No tid appears twice.
- Format limits: x_post and thread parts ≤ 280 characters, slides ≤ 30 words, captions ≤ 120 words, short videos 113–127 words, long videos 6 sections / 10 minutes.
- Every fix below was re-checked for length, pool-field word limits, claims.scan and similarity.

Checked by reading: all 50 posts against the cited original and paraphrase, and against neighbouring entries in `data/`: BhG 12.19, 13.12; TS 6.4-6.5; Vism 9.p299-300; MN 10:2, 10:8, 10:46; DN 22:3; MN 118:7; TU 2.1.1, 2.2-5.
Not run: the AI-label reminder (not in the packet); on-screen timing; the model check (rules engine only).

| criterion | pass | fail |
|---|---|---|
| (a) cites faithfully | 45 | 5 |
| (b) no claims | 50 | 0 |
| (c) no near-duplicates | 46 | 4 |
| (d) idea-specific | 48 | 2 |
| **all of a–d** | **40** | **10** |
| (e) format/voice, note only | 30 | 20 |

Passes per bucket: work 9, overthinking 7, sleep 8, loneliness 8, meaning 8 (P5: 8 of 50 in total). The P5 template faults are fixed in this packet:
- Every x_post has a link and a closing.
- Scenes are bound to their items.
- Every tid is exact.
- No "you will" remains.

The P5 (a) items in this packet (TS 6.10, BhG 5.10 "by sin") now pass. The other P5 (a) items are not in this packet and were not checked here.

### Failures and exact fixes (full text and lengths in the verdicts file)
- L3 d4daac3e work x_post, BhG 2.47 (a): "never to its fruits, and not to inaction either" puts inaction under the right (adhikāra). The verse says not to let attachment (saṅga) be to inaction. Fix: point → "The right is to the action alone, Kṛṣṇa says, never to its fruits; nor should one cling to inaction." (redraft 263 chars).
- L11 d7a1f95b overthinking x_post, YS 1.32 (c): the link "one principle, returned to" restates L17's BhG 6.26 "the instruction is the return", on the same many-at-once scene. Fix: link → "Twelve pulls; the sūtra's counsel is one, not twelve." (259 chars).
- L14 5f5befb9 overthinking x_thread, MN 10:36 (c): same idea and closing as L13 (MN 10:34): know the state rather than stop it, then "What is here now?". Fix: link → "Beyond knowing it is there, the sutta asks one to know how it arose."; closing → "Which line in the meeting started it?".
- L20 abac28ed overthinking long_video, Dhp 348 (a): section 5 says the verse "does not promise a result", but its last line states one (no more birth and ageing). Fix: section 5 points → "The verse ends on its own goal: with the mind freed everywhere, the Dhammapada says, one does not come again to birth and ageing. That is the text's goal in its own words; this video promises nothing."
- L23 0ccc23c5 sleep x_post, BAU 4.3.9-14 (c): the point and the closing "Whose light was it?" repeat L22's thesis from BAU 4.3.2-6 (the self as its own light; "What is still lit?"). Fix: x_link "Waking life gave the pieces; the dreamer built."; closing → "What did the dream borrow from the day?" (276 chars).
- L28 85450832 sleep short_video, MN 10:6 (a, c):
  - (a) "No technique, no target" is contradicted by MN 10:2 (goals) and MN 10:46 (stated result).
  - (c) Same instruction and closing as L21: DN 22:4 = MN 10:8, the next section, which also lists lying down and sleeping.
  - Fix: remove MN 10:6 from the sleep pool, treat DN 22:3-4 / MN 10:6-8 as one passage family in the overlap check, and redraft from another sleep item.
- L39 22f9b21c loneliness short_video, Dhp 76 (a):
  - "the friend": the verse speaks of a wise one to keep company with.
  - The bridge "It is not advice from outside you": the verse is advice (bhaje).
  - The STOPS line "does not promise a result": the verse says "better, not worse".
  - Fix: close_reading → "The verse describes the wise one twice: one who points out faults (vajjadassī), and a reprover (niggayhavādī). It likens that person to someone who shows where treasure lies hidden."; link → "The verse counts such a person's words as treasure."; bridge → "The old texts are often this plain. They name the thing, and leave the seeing to the reader."; STOPS → "Where the text stops: it says only that keeping such company is better, not worse." (121 words).
- L40 25521c0d loneliness long_video, MN 118:8 (a): the STOPS line is contradicted by "a little given to such an assembly becomes much". Fix: section 5 points → "The passage also calls this assembly worthy of gifts, where a little given becomes much: its own teaching on giving, stated as the text's. It praises one assembly; it promises no company."
- L42 a4051cdb meaning x_post, TU ch2 (d): the link maps "name and job" onto the first self (the body made of food), and the closing "And the fifth answer?" steers the reader to the bliss-self as who they are (meaning never-list). Fix: link → "Its list has no name or job; it starts at the body."; closing → "What comes after the job?" (270 chars).
- L49 365de4f8 meaning short_video, BhG 3.35 (d): the link is a gloss and joins nothing. By the gloss's own terms (svadharma is station duty, not a calling), a friend's life path is not what the verse is about, and "measure" is not in the verse. The faithful use (keep to one's station) is barred by the meaning never-list. Fix: retire BhG 3.35 from the meaning pool, redraft from another item, and drop the svadharma line in `rules/voices/meaning.md`.

### Template and pool fixes (`insight/content.py`, `rules/content/buckets.json`)
1. The fixed STOPS line "it describes what happens; it does not promise a result" is false when the cited text states a fruit (Dhp 348, Dhp 76, MN 118:8). Add an optional `stops` field per pool item and use it in short and long videos. Check every video-eligible item for a stated fruit before the next draft.
2. BRIDGES[1] "It is not advice from outside you" is false for injunctive verses; change it to "Read it slowly, and check it against your own day." Drop the bridge when STOPS follows with the same words (L18, L28).
3. The code checks passages, not ideas. Treat adjacent sutta sections with the same instruction (DN 22:3-4 / MN 10:6-8) and two passages carrying one dialogue's thesis (BAU 4.3.2-6 / 4.3.9-14) as one family per account. Have a reader compare links and closings within each pool (the pairs here: L11/L17, L13/L14, L21/L28, L22/L23).
4. Pool text to change:
   - BhG 2.47: point.
   - YS 1.32: link.
   - MN 10:36: link and closing.
   - TU ch2: link and closing.
   - BAU 4.3.9-14: x_link and closing.
   - Dhp 76: close_reading and link.
   - Retire MN 10:6 (sleep) and BhG 3.35 (meaning).

### (e) notes (not gating)
20 posts are noted: L1, L4, L5, L8, L10, L18, L19, L20, L24, L25, L26, L28, L29, L30, L31, L34, L36, L38, L40, L50.
- 7 closings use the generic "Sit with that." (L4, L5, L8, L19, L24, L36, L38).
- 5 long videos have one-line points and no other-lens section (L10, L20, L30, L40, L50). L50 should say that the Yoga Sūtra's "not-self" is not the Buddhist anattā.
- Part 3, or the close-reading beat, restates part 2 (L4, L24, L29, L34).
- The bridge and the STOPS line say the same thing back to back (L18, L28).
- A term is unglossed or bracketed twice (L1 sāttvic, L26 brahman, L19 aparikheda, L34 vijugupsate).
- L25 uses "two hours" (the sleep voice allows no numbers).
- L31's x_link repeats its point.
- In carousels, the fixed slide "An old text has a word for this." is not literally true for most scenes.
- The difference lines of L45 and L47 are nearly the same sentence.

### Gate verdict: FAIL
40 of 50 posts pass a–d; the gate needs 50 of 50.
- Claims (b) is clean. Similarity is clean by code (max 0.316).
- The 10 failures break down as:
  - 5 faithfulness failures: 2 from pool text (L3, L28) and 3 from the fixed STOPS or bridge lines (L20, L39, L40; L39 also from pool text).
  - 4 same-idea pairs within one account (L11, L14, L23, L28).
  - 2 stretched links (L42, L49).
- Every failure has an exact fix above and in the verdicts file.
- L28 and L49 are redrafted from new pool items, so those two new posts must be judged before the gate can pass.


## Re-run 2 (P6)

Judge: onto-judge (claude-opus-5-5), 2026-09-29.
- Packet: `eval/judge/rules/content_review_new10.jsonl`, the 10 replacement posts; they are lines 41-50 of the active packet `eval/judge/rules/content_review.jsonl`. Pool: `buckets.json` 2.1.
- Per-post scores, evidence and fixes: `eval/judge/content_verdicts_rerun2.jsonl`.
- "Lnn" below means line nn of the active 50-post packet.

Checked by code:
- Queue state: 60 posts in `content/queue.jsonl`, 10 rejected and 50 pending. The rejected ids are exactly the 10 failed in Re-run (P6). The 50 pending ids equal the active packet.
- Each new post's queue body text equals its packet text.
- Citations: `source_line(tid)` is printed once, exactly, in all 10. For every tid, `teaching(tid).id == tid` and the teaching is citable (9 text-verified, 1 sourced). No tid or source line appears twice among the 50.
- claims.scan: 0 hits. Keyword scan: the only hit is "promises", in the negation "this post promises nothing". No "you will".
- 5-gram Jaccard, recomputed against the 49 other active posts: max 0.242 (the two long videos' shared template lines). All 10 match the packet values. Max over all 50: 0.316 (L7/L32, unchanged).
- Format limits, rules_check and the AI-label reminder (present in each queue body): all pass.

Checked by reading:
- All 10 posts against the cited original, the paraphrase and the entry notes, and against these neighbours in `data/`: TS 6.24, 6.26, 8.12; Dhp 34-35, 329-330, 347, 349; BhG 2.60, 2.66, 2.68; MU 2, 3, 5 and MK 1.1-1.3; BAU 4.3.7, 4.3.15-18; TU 3.9.1, 3.10.2, 2.1.1, 2.2-5; YS 1.2, 1.4 and YBh 1.3-1.4.
- Each post against the 9 other active posts in its bucket, for the same idea.
- Every "where the text stops" line and bridge, for truth of this verse. Dhp 348 now carries its own `stops` line; the other videos carry the new default STOPS, which claims nothing about the text's content.

Not run: on-screen timing; the model check (rules engine only). The 40 posts that passed in Re-run (P6) were not re-judged. By code: all 40 are pending and unchanged in tid and source line, and the 100 quoted fragments in their (d) evidence all appear in the current text. The packet they were judged in has been replaced, so byte-for-byte identity could not be checked.

| criterion (10 new posts) | pass | fail |
|---|---|---|
| (a) cites faithfully | 10 | 0 |
| (b) no claims | 10 | 0 |
| (c) no near-duplicates / same idea | 9 | 1 |
| (d) idea-specific | 9 | 1 |
| **all of a–d** | **9** | **1** |
| (e) format/voice, note only | 4 | 6 |

### Failure and exact fix
- L50 c625b423, meaning short_video, YS 1.3 (c, d):
  - (d): the link "In the sūtra, 'then' means once the mind's activity is stilled: the seer rests in its own form." is a gloss and joins nothing to the scene ("'So, what do you do?' someone asks at a party."). The sūtra says nothing about occupations or answering who one is. The only join left to the reader is "the job is not who you are; the seer is", which the meaning never-list bars. This is the same fault as P6 L49.
  - (c): the same idea as L38 (BhG 13.2). Both set a request to describe oneself against a text's witness, and close on "And the knower?" / "What is the seer's own form?". The seer and the knower of the field play the same role. Its scene also repeats the new TU ch2 post (L49).
  - Fix:
    1. Retire YS 1.3 from the meaning pool (it failed (a) in P5 as well).
    2. Redraft this slot from another meaning item whose link and closing no other meaning post already carries (not a job-identity scene), and judge it.
    3. Make `_short_video_parts` render the item's `difference` line.

The 9 passing posts include the P6 fixes, applied as asked:
- Dhp 348: its own `stops` line.
- BAU 4.3.9-14: the new link and closing, now in a short video.
- TU ch2: the new link and closing.
- The retired MN 10:6 and BhG 3.35 are gone.

### (e) notes (not gating)
- Dhp 33 (L42): the link restates the point and names nothing in the scene. Suggested x_link: "The replay is the quivering; the verse straightens the mind, not the slip." (278 chars).
- BhG 2.67 (L43):
  - Part 3 restates part 2.
  - The scene is distraction rather than going over things.
  - Its "wind" closing echoes L13's.
- Long videos (L44 Dhp 348, L48 Dhp 328):
  - Each section has one line of points, and there is no other-lens section.
  - In L48, section 5 says "Where the text stops" twice. The long_video label and the default STOPS both carry it.
  - In L44, bhava is glossed two ways, and "this post" appears in a video.
- MU 4 (L45): "is dream" and "gives dream its own station" are loose, since in the verse dream is the station of the second quarter of the self. Exact wording that fits (276 chars) is in the verdicts file.
- YS 1.3 (L50): 4 of its 8 beats are fixed filler, and 3 of those say "read it into your own day". The P6 template fix 2 (drop a bridge that repeats STOPS) is not in the code.
- TS 6.25 (L41): "low-status karma" can be read as workplace status. It is the third Jain-inflow post in the work account.

### Gate verdict: FAIL
- 49 of the 50 active posts pass a–d: the 40 that stand from Re-run (P6) plus 9 of the 10 replacements.
- The gate needs 50 of 50.
- Passes per bucket: work 10, overthinking 10, sleep 10, loneliness 10, meaning 9.
- The one remaining fix: retire YS 1.3, redraft L50 from another meaning item, and judge that one post.


## Re-run 3 (P6)

Judge: onto-judge (claude-opus-5-5), 2026-09-29.
- Packet: `eval/judge/rules/content_review_new1.jsonl`, 1 replacement post. It is line 50 of the active packet `eval/judge/rules/content_review.jsonl`. Pool: `buckets.json` 2.2.
- Verdict, evidence and fix: `eval/judge/content_verdicts_rerun3.jsonl`.
- "Lnn" means line nn of the active 50-post packet.

Checked by code:
- Queue: 61 posts. The 50 pending ids equal the active packet. The 11 rejected are the 10 Re-run (P6) failures plus c625b423 (YS 1.3). Queue text equals packet text for all 50.
- YS 1.3 is in no pool. KU 1.2.1-2 is in the meaning pool only.
- The new post's queue parts equal a fresh render from its pool item.
- Citation: `source_line(tid)` is printed once and exactly. `teaching(tid).id == tid`, and the teaching is citable (sourced). The tid and source line are unique among the 50.
- claims.scan: 0 hits. Keyword scan (health, research, promise, prediction, destiny, calling, purpose, career): 0 hits. No "you will".
- 5-gram Jaccard against the 49 others: max 0.214 (L46, shared template lines), and 0.135 within the meaning bucket. Max over all 50: 0.316 (L7/L32, unchanged).
- Format: 6 beats and 123 spoken words; rules_check passes; the AI-label reminder is present.
- The other 49 are unchanged:
  - L41-49: post id, tid and text are byte-for-byte equal to the Re-run 2 packet (`content_review_new10.jsonl` lines 1-9). Only the `max_similarity` field of L46 and L47 moved (0.203 to 0.214 and 0.213), because the new L50 shares template lines with them.
  - L1-40: ids, order, tid and source line match the 40 Re-run (P6) passes. The 113 fragments quoted in their evidence are all present, 24 length counts from their (e) notes match, and 32 recorded pair similarities recompute exactly.
  - Not run: a byte-for-byte check of L1-40 against the Re-run (P6) packet, which was not kept. 38 of the 40 carry a length or similarity fingerprint; L9 and L35 carry only quoted fragments.

Checked by reading:
- The post against the paraphrase, the prepared segments KU 1.2.1-1.2.5, and these neighbours in `data/`: KU 1.1.20, 1.1.21-29, 1.2.4-6, 1.2.7-9; `cpt:sreyas-preyas`; `obs:preyas`.
- Every line, including the bridge and the STOPS line, for truth of this verse.
- The post against the 9 other meaning posts, for the same idea.

Not run: on-screen timing; the model check (rules engine only). The 49 standing posts were not re-judged.

| criterion (1 new post, L50 e9c6346a) | result |
|---|---|
| (a) cites faithfully | pass |
| (b) no claims | pass |
| (c) no near-duplicate / same idea | pass |
| (d) idea-specific | **fail** |
| (e) format/voice, note only | pass (notes) |

### Failure and exact fix
L50 e9c6346a, meaning short_video, KU 1.2.1-2 (d):
- Every line is true of the verse:
  - The point and close reading match 1.2.1-2 and the prepared text.
  - "asks that they be examined first" is the normative sense of an indicative verse. The same tolerance was given to L35.
  - The bridge and the default STOPS claim nothing false.
- The failure is the fit to the scene. The scene is "A choice between the safe offer and the one that feels right." The closing, "Which is which?", asks which offer is the good and which the pleasant. The verse does not sort two worldly offers:
  - Choosing for "getting and keeping" (yogakṣema) is the fool's reason (1.2.2), and that is what a safe offer is for.
  - The pleasant is the wealth, land and long life that Naciketas refuses (1.1.21-29). The good is knowledge (1.2.4-6).
  - The "pleasant-looking" desires are also what he cast off (1.2.3). So "the one that feels right" is not the good either.
- Read beside "The fool chooses the pleasant for getting and keeping", the post steers a job choice: the safe offer is foolish, so follow what feels right. That is close to the meaning never-list (life-path and "your calling" framing; no telling a reader to leave work). It is the fault of P5 L46 and P6 L49.
- Fix: stop pairing KU 1.2.1-2 with the offer scene. Either option below needs the new post judged.
  - Option 1: rewrite the item. Word counts are within limits and the rendered post was checked by code: 145 words, 0 claims, max Jaccard 0.156. All four lines are new:
    - scene: "A list of what the next ten years should bring, written on a quiet evening."
    - link: "The Kaṭha does not sort anyone's list; it says each of the two binds a person to its own aim."
    - closing: "What is each item on the list for?"
    - stops: "Where the text stops: it names the two and the wise one's preference; it does not say which item on a list is which."
  - Option 2: redraft the slot from an unused meaning item.

(e) notes (not gating):
- The close reading drops "with different aims" and the fruit that 1.2.1 states. An item `stops` line would be more exact than the default.
- Naciketas is named, but his refusal of Yama's offers is not told.
- The two Re-run 2 template fixes are now in the code: the difference line is rendered, and no bridge repeats STOPS.

### Gate verdict: FAIL
| criterion (50 active posts) | pass | fail |
|---|---|---|
| (a) cites faithfully | 50 | 0 |
| (b) no claims | 50 | 0 |
| (c) no near-duplicates / same idea | 50 | 0 |
| (d) idea-specific | 49 | 1 |
| **all of a–d** | **49** | **1** |
| (e) format/voice, note only | 28 | 22 |

- 49 of 50 active posts pass a–d: 40 from Re-run (P6), 9 from Re-run 2, and 0 of 1 here. The gate needs 50 of 50.
- Passes per bucket: work 10, overthinking 10, sleep 10, loneliness 10, meaning 9.
- The one remaining slot is L50 (meaning short_video). Fix KU 1.2.1-2 or redraft it from another item, then judge that one post.


## Re-run 4 (P6)

Judge: onto-judge (claude-opus-5-5), 2026-09-29.
- Packet: `eval/judge/rules/content_review_new2.jsonl`, 1 replacement post (26f34272). It is line 50 of the active packet `eval/judge/rules/content_review.jsonl`. Pool: `buckets.json` 2.3.
- Verdict and evidence: `eval/judge/content_verdicts_rerun4.jsonl`.
- "Lnn" means line nn of the active 50-post packet.

Checked by code:
- The pool item: the scene, link, closing and stops lines equal the Re-run 3 fix text, word for word. The old "safe offer" scene is off the item, and KU 1.2.1-2 is in the meaning pool only.
- Queue:
  - 62 posts. The 50 pending ids equal the active packet.
  - The 12 rejected are every post failed so far: the 10 Re-run (P6) failures, c625b423 (YS 1.3) and e9c6346a (the Re-run 3 KU post).
  - Queue text equals packet text for all 50.
  - The new post's parts equal a fresh render from its pool item.
- Citation: `source_line(tid)` is printed once and exactly. `teaching(tid).id == tid`, and the teaching is citable (sourced). The tid and source line are unique among the 50.
- claims.scan: 0 hits. Keyword scan: 0 hits. No "you will", and no personal data.
- 5-gram Jaccard:
  - Against the 49 others: max 0.156 (L47, shared template lines). Within the meaning bucket: 0.145 (L39).
  - Every packet `max_similarity` recomputes exactly. Max over all 50: 0.316 (L7/L32, unchanged).
- Format: 6 beats and 145 spoken words. rules_check passes, and the AI-label reminder is present.
- The other 49 are unchanged since Re-run 3:
  - L41-49: the raw lines are byte-for-byte equal to the Re-run 2 packet (`content_review_new10.jsonl` lines 1-9), including every field. That file predates Re-run 3. L46 and L47 `max_similarity` are back at 0.203, because e9c6346a has left the set.
  - L1-40, by code:
    - Ids, order, tid and source line match the 40 Re-run (P6) passes.
    - All 113 fragments quoted in their evidence are present. All 52 length counts in their (e) notes match. All 32 recorded pair similarities recompute exactly.
    - The Re-run 3 similarities of the rejected e9c6346a against L46 (0.214), L47 (0.213) and L39 (0.135) recompute exactly. Its max over the current 49 equals its recorded 0.214.
    - A fresh render from `buckets.json` 2.3 reproduces every pool-derived line of all 49. In the 10 L1-40 videos, only the older fixed STOPS and bridge lines differ, and each of those was read in Re-run (P6).
  - Not run: a byte-for-byte check of L1-40 against the packet judged in Re-run 3, which was not kept.

Checked by reading:
- The post against the paraphrase, the prepared segments KU 1.2.1 and 1.2.3, and these neighbours in `data/`: KU 1.1.20, 1.1.21-29, 1.2.4-6.
- Every line, including the new link and the item's own STOPS line, for truth of this passage.
- The post against the 9 other meaning posts for the same idea, with L39 (Dhp 62) read closely.

Not run: on-screen timing; the model check (rules engine only). The 49 standing posts were not re-judged.

| criterion (1 new post, L50 26f34272) | result |
|---|---|
| (a) cites faithfully | pass |
| (b) no claims | pass |
| (c) no near-duplicate / same idea | pass |
| (d) idea-specific | pass |
| (e) format/voice, note only | fail (not gating) |

L50 26f34272, meaning short_video, KU 1.2.1-2:
- (a):
  - The new link's second clause, "it says each of the two binds a person to its own aim", is 1.2.1's *te ubhe nānārthe puruṣaṃ sinītaḥ*. It also restores the "different aims" that the close reading drops.
  - "The Kaṭha does not sort anyone's list" is a true scope statement. The only list the Kaṭha treats, Yama's offers (1.1.21-29), is refused as a whole, and the good Naciketas asks for is knowledge (1.2.4-6).
  - The item's STOPS line is true of 1.2.1-2, and unlike the old default it does not deny the fruit that 1.2.1 states.
- (d):
  - The Re-run 3 fault is gone: the two worldly offers and "Which is which?" are no longer in the post.
  - The closing asks the reader to do what the verse credits to the wise (examine each thing and its aim). The close reading gives the verse's own marker ("for getting and keeping").
  - The link and STOPS say that the text does not sort the list, so no item is labelled the good and no job or life choice is steered.
- Considered, not failed:
  - "The good" is left undefined, but no line says any item is the good.
  - L39 (Dhp 62) also sets a verse against a list and carries "the fool", but its idea and closing (what is one's own) differ from this post's (what each item is for).
- The scene, link, closing and stops lines are the text this judge proposed in Re-run 3. They were judged here as new text.

(e) notes (not gating):
- The link's first clause and the STOPS line say the same thing in consecutive beats. This repeat comes from the Re-run 3 fix text. Optional edit, checked by code (139 words, 0 claims, rules_check passes): link → "The Kaṭha says each of the two binds a person to its own aim."
- The close reading still drops 1.2.1's fruit.
- Naciketas's refusal of Yama's offers and his wish for knowledge are not told. Telling them would show what the Kaṭha counts as each of the two.
- The scene is spoken twice (template).
- `stops` has no word limit in the `buckets.json` note.
- Outside the 50 posts: the meaning `scenes` list still holds "A choice between the safe offer and the one that feels right.", and `content/calendars/meaning.md` day 13 suggests it with BhG 2.22. That pairs a rebirth verse with a job choice, the P5 L46 fault. Remove the scene before anyone drafts from the calendar.

### Gate verdict: PASS
| criterion (50 active posts) | pass | fail |
|---|---|---|
| (a) cites faithfully | 50 | 0 |
| (b) no claims | 50 | 0 |
| (c) no near-duplicates / same idea | 50 | 0 |
| (d) idea-specific | 50 | 0 |
| **all of a–d** | **50** | **0** |
| (e) format/voice, note only | 27 | 23 |

- All 50 active posts pass a–d: 40 from Re-run (P6), 9 from Re-run 2 and 1 here. The gate needs 50 of 50.
- Passes per bucket: work 10, overthinking 10, sleep 10, loneliness 10, meaning 10.
- The counts were computed by code from the verdict files, taking each post's latest judging run.
- The 23 (e) notes do not gate: L1, L3, L4, L7, L9, L15, L16, L19, L20, L21, L23, L24, L25, L28, L30, L32, L40, L42-45, L48, L50.
- Limit of this verdict: L1-40 were confirmed unchanged by code fingerprints and a re-render from the pool, not byte for byte, because the Re-run 3 packet was not kept.
