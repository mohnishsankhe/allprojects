# Originality and platform rules (content engine)

Applies to every draft from `insight/content.py` and every edit a reviewer makes. Read with `ENGINE_SPEC.md` §14,
`rules/tone.md`, `rules/forbidden_claims.json`, `rules/content/buckets.json`, `rules/content/formats.json` and
`rules/voices/<bucket>.md`.

## Design choices
1. One scene, one teaching: every post joins one bucket scene to one citable teaching; 118 of the 134 pool items are text-verified, 16 sourced.
2. Five pools (work 28, overthinking 28, sleep 26, loneliness 25, meaning 27) share no teaching, so no two accounts ever post the same verse.
3. Pools draw on Vedic/yogic, Buddhist (suttas, Dhammapada, Visuddhimagga, Heart Sūtra) and Jain texts only where the text speaks to the bucket; Jain items are few because only Tattvārtha chapters 2 and 6–8 are citable today.
4. Points and angles are our own plain words built on the ontology's paraphrase; originals are quoted briefly and always with their reference.
5. Reuse: a teaching at most once per account per 30 days, which is stricter than, and so covers, "each (scene, teaching) pair at most once".
6. Near-duplicates: a character 5-gram Jaccard of 0.5 or more against any pending, edited or approved post on any account means reject.
7. Each account publishes only its own original material; the five accounts never repost, quote, reply to or promote one another.
8. AI assistance is disclosed as each platform requires; AI-assisted media is labelled where required, and the queue shows the reminder per format.
9. No personal data ever: scenes are invented and generic, and nothing from readings, intake, check-ins or messages reaches a post.
10. Claims are blocked twice: forbidden_claims.json on every draft and edit, plus each bucket's "never" list (sleep: no sleep or health benefit; overthinking: never "anxiety" as a condition).

## 1. Reuse limits
- A teaching (tid) is used at most once per account in any 30-day window. Pending, edited and approved posts count;
  rejected posts do not. This is what `content.pick()` enforces, and it implies that each (scene, teaching) pair is used
  at most once per account per 30 days.
- Supporting teachings in a long video count as used, like the anchor teaching.
- A scene may recur with different teachings, but not on consecutive days of the same account's calendar.
- The pools are disjoint across the five accounts; a teaching moves between pools only by an edit to `buckets.json`
  that keeps them disjoint.

## 2. Near-duplicate rule
- Text compared: all parts joined by line breaks, plus the caption, lower-cased with runs of whitespace collapsed.
- Measure: Jaccard similarity of the sets of character 5-grams.
- Compared against every queued (pending), edited or approved post on all five accounts, not only the same account.
- Similarity of 0.5 or more: reject the draft. Below 0.5: the draft may go on to the other checks.
- A reviewer who edits a post must not bring it back above the threshold (for example by pasting in another post's
  lines).

## 3. Quoting and paraphrase
- Quote an original (Sanskrit, Pali, Prakrit, Chinese) only briefly: at most one verse line or 12 words, transliterated,
  and always followed by the citation line.
- Everything else is paraphrase in our own words, built on the ontology's paraphrase (the project's own wording). Never
  copy a published modern translation or commentary.
- Quotation marks around an English phrase are used only where the ontology's paraphrase gives it as the text's own
  direct speech ("I do nothing at all", "may I be happy").
- The citation line is exactly `Source Ref` as `content.source_line(tid)` returns it. It is never dropped, shortened
  or moved to a place the reader cannot see (it must appear in the post text, on a slide, or on screen).
- Say what the passage says, then stop. Never add doctrine, never reverse its sense, never attribute to one tradition
  what another teaches.

## 4. Own material per account; no cross-account amplification
- Each account publishes only drafts made from its own bucket's pool and scenes, in its own voice.
- No reposts, retweets, quote-posts, duets, stitches, shares to stories, or coordinated replies between the five
  accounts. No shared hashtag campaigns, no cross-linking in bios, no "follow our sister account".
- No engagement pods, bought followers or likes, automated replies or automated posting. The app has no posting API;
  a person posts by hand after approval.
- No reposting of other creators' material. Everything posted is our own writing on the public-domain texts.

## 5. Platform AI-content policies and labels
- Follow each platform's AI-content policy as it stands on the day of posting (X, Instagram, YouTube). The reviewer
  checks it; these rules do not claim to state the policy.
- Label AI-assisted media where the platform requires it, using the platform's own label or disclosure setting. The
  queue shows the reminder stored in `formats.json` for each format.
- Never present AI-made images, voices or faces as real people, real events or real places. No AI images of deities,
  teachers or sacred sites presented as real.
- Recommended: each profile says that posts are drafted with AI assistance and reviewed by a person.

## 6. Personal data
- No personal data from readings, intake answers, pasted dialogues, check-ins, messages or comments, ever, even with
  consent and even anonymised.
- Scenes are invented and generic. No real names, handles, @-mentions, employers, schools, places that could identify
  anyone, screenshots of messages, phone numbers or links.
- Replies to comments on a platform are written by a person and never quote a commenter's private details.

## 7. Claims and content bans
- Every draft and every edit passes `rules/forbidden_claims.json` (health or cure, diagnosis, prediction, astrology).
  A hit blocks the text.
- No modern research, psychology, neuroscience or science, even as support. No promises, no predictions.
- Only teachings for which `ontology.citable(tid)` is true: sourced or text-verified, not unverified, not retired, not
  part of a restricted practice. Skeleton entries never appear.
- Restricted practices (body-cutting, metals or mercury, extreme breath retention, sexual rites, prolonged fasting) are
  never recommended or described as something to try.
- Each bucket's "never" list in `buckets.json` applies on top of these rules.
- Tone (`rules/tone.md`): no "you are…", no flattery, no fear, no guilt, no universal filler; state differences between
  traditions plainly.

## 8. Review queue
- Every draft that passes the checks joins the queue as pending. A person approves, edits or rejects it. Nothing is
  posted by the app.
- The reviewer reads the teaching's paraphrase and original beside the draft and rejects anything that stretches the
  link, flattens a distinction, or reads as advice with a promised result.
- The calendar (30 days per account) is a plan drawn from approved and pending posts, not a schedule the app executes.

## 9. Who enforces what
- Code (`insight/content.py`): citable teaching, 30-day teaching reuse per account, part counts and length limits for
  X posts, threads, carousel slides and video word counts, citation line present, claim scan, personal-data pattern,
  near-duplicate threshold.
- Code on edit (`insight/service.py`): claim scan of the edited text.
- Model check (when the model engine runs): faithful to the teaching, no claims, idea-specific, no stretch.
- Human reviewer: platform policy and AI labels, carousel caption length, bucket "never" lists, cross-account
  amplification, quoting limits, scene repetition in the calendar, and anything the checks cannot see.
