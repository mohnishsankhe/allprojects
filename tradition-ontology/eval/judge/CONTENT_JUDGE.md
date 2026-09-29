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
