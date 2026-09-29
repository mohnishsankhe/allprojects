# Mapping rules: from a person's own words to diagnostic-layer entries
Machine-readable twin: `rules/mapping_rules.json` (every regex, threshold, reason code and 42 filter test cases).
This covers mapping only; synthesis, pathway and UI are out of scope. The thresholds are product defaults, not taken
from the texts; change them only after synthetic-persona evals. References marked "from memory" must be resolved
against `data/` before anyone sees them.

## 1. Where mapping sits
The safety screen (`rules/safety_rules.json`) runs first. On `stop_crisis` or `decline_minor` there is no mapping. On
`continue_medical_note` or `continue_no_diet` mapping runs, but flagged sentences are never evidence; under no-diet, no
sentence about food, eating, weight or diet is evidence either. If fewer than 25 of the person's own words remain
after hard exclusions, there is no mapping. The rules engine (cue matching) and the model engine (JSON candidates)
pass the same validators. **Code, never a model, decides** strength, confidence, citations (copied from the markers
used), caps and selection; any confidence or citation a model supplies is ignored. Zero mappings is a valid result,
and an unmapped entry is never reported as absent, dormant or anything else.

## 2. What counts as the person's words
**Evidence** is free-text intake answers, free text, and the person's own turns in a pasted dialogue. **Never
evidence:** question text; option or scale labels the person picked; other speakers' turns; text in double quotes
unless framed as the person's own speech or thought (`I told myself "..."`); `>` lines and anything after an
email-quote header; sentences caught by a safety or injection pattern; non-answers (`n/a`, `idk`); sentences under
70% English or ontology-term tokens (English only in v1; they are logged). **Dialogues:** the self speaker comes from
the UI or a single label such as `Me`, else the dialogue is unused (never guessed from content). A dialogue is one unit,
and each self line is conduct in one episode, so every dialogue item is capped at indirect; a self turn echoing the
other speaker is a retort. **Units:** each intake answer; each free-text paragraph (over 120 words: 60+-word chunks;
at most 3 free-text units count per entry); each dialogue. Near-identical quotes in different units count once.

## 3. The evidence unit (a quote)
One contiguous, exact substring of one sentence of one unit: 3–35 words, at most 240 characters, word-aligned, with
at least one non-stopword. Matching is case-sensitive on normalised text (NFC, zero-width characters removed,
typographic quotes to ASCII, whitespace collapsed). The only repairs are trimming end punctuation and taking the
source's casing when a case-insensitive match is unique. No ellipsis splices, changed words or translation; the shown
quote is sliced from the source by code. No email, URL or phone number. An entry takes at most one item per sentence,
and confidence uses only the quotes kept on the mapping (at most 5, the best one per unit).

## 4. When a quote is not evidence (in this order; the first failure gives the reason code)
*Span and sentence checks:* unresolved dialogue speaker, not the person's own words (`R_NOT_OWN_WORDS`) or an echo
retort; a safety or injection sentence or someone else's quotation; non-answer; non-English; bad form; personal data.
- **Clinical words** (`my anxiety`, `my OCD`): the person's clinical vocabulary is never turned into a textual category.
- **Body or health:** pain, illness, breathing difficulty or breath-holding, sex, drugs and weight are always excluded.
  Sleepiness, heaviness, tiredness and breath count only in a contemplative, devotional or study setting (japa,
  meditation, scripture). Food counts only with no disordered-eating flag and no restriction word.
- **Self-label** (`I have a lot of rajas`). **Questions:** `Am I too attached?` is excluded, `Why do I always...?` capped.
- **Sarcasm** (`oh sure`, eye-roll, `/s`, `jk`). **Hypothetical sentence** (`if` with would/could/might/'d).
*Clause checks* (clauses split at but, although, though, however, yet, ;):
- **Someone else's characterisation** (`My wife says I'm always angry`) excludes, unless endorsed (then capped).
- **Another person as subject:** the nearest subject left of the match decides. `he`, `she`, `they`, generic `you`,
  `my husband` exclude; `I`, `me`, `my mind` count; `My wife and I` counts, capped.
- **Hypothetical clause:** would, should, will, could (not couldn't), `imagine`, `what if`. Aspirational clauses
  (`I wish I didn't...`, `I'd like to stop...`) are capped instead.
- **Past and resolved** (`used to`, `no longer`, `I've stopped`, unless `now`, `still`, `these days`) and **negated**
  (negator parity differs from the cue's own: `It's not that I can't focus` against the cue `I can't focus`) items
  become counter-evidence.
*Quote check:* generic statements are always excluded (`life is just busy`, `nobody's perfect`, `like everyone`,
`I want to be happy`); `I get distracted`, or anything with `sometimes`, is excluded unless specific (§6).

## 5. Strength, caps and relevance
**Direct** (1.0) means the person states, about themself, now or as a habit, what a marker describes: an exact cue
phrase, all of a cue's content words in a small window, or a blind recheck of *explicit*. **Indirect** (0.6) is a
partial cue match, a one-word cue or a recheck of *implied*. **Suggestive** (0.3) is one shared word, corroboration
only. One cap means at most indirect; two or more mean suggestive. The caps are: hedge (`I think`, `a bit`), low
frequency (`rarely`), `we`, aspirational, weak sarcasm (`lol`, `sooo`), presupposing question, echo of the intake
question, endorsed attribution, dialogue line, one-word cue. Markers come from the texts; cues only help noticing
(SCHEMA.md), so each item names its marker. A model candidate weaker than direct, or with a negator in its clause,
goes to a **blind recheck**: a separate call that sees only the marker text and cues (no entry name), the sentence
and the one before it, and the quote. It must answer: fits (explicit or implied), speaker is self, affirmed, not
hypothetical, not joking, not true of nearly everyone, not about the body. Anything else drops the item.

## 6. Specificity: nothing that would fit anyone
There are three features: **F1** frequency, duration or intensity (`every night`, `for days`, `can't stop`); **F2** a
detail of the person's own (a content word outside the cue and the generic lexicon: `japa`, `colleague`); **F3** a
consequence or contrast (`before I finish`, `even though`). A mapping needs a kept quote whose sentence has a feature,
or evidence from 2 or more units. A cue that fires on more than 10% of bland synthetic baseline personas counts as
suggestive until it is revised.

## 7. Confidence, and when not to map
E is the sum of unit weights of 0.6 or more, plus at most 0.6 from suggestive-only units, capped at 3.0. C is the
counter-evidence (denial 1.0; weaker denial or past-resolved 0.6), and E_net = E − 0.5·C.
- **Do not map** unless E_net ≥ 1.0 AND (a direct, specific quote OR n_units ≥ 2), and the kind or entry policy
  allows it. A dialogue-only reading needs 3+ supporting self turns and tops out at low. Never enough on their own:
  suggestive items, one indirect item, one unspecific direct quote, a self-label, an entry name the person typed,
  an equivalence to another mapped entry.
- **High:** E_net ≥ 2.2, direct items in 2+ units, (3+ units OR 2+ markers), C = 0. **Moderate:** E_net ≥ 1.6,
  2+ units, 1+ direct unit. Anything else past the floor is **low**. Any counter-evidence, or model-paraphrase-only
  evidence with no lexical match, means at most moderate; §8 ceilings apply. Numbers are for audit, never shown.

## 8. Kinds and entries
- **Mappable** (maximum per reading, confidence ceiling): affliction, hindrance, fetter, passion and obstacle (2 each,
  high); mind-activity, state, guṇa and temperament (1 each, moderate). **Never mapped:** sheath, vital-current,
  state-of-consciousness and unknown kinds. These either fit everyone or are bodily.
- **Entry denylist** (on id and name; each pattern must match an entry at build time or be reported): attainments
  (samādhi, jhāna, turīya, guṇasthāna, the higher fetters); what the texts make true of all not yet free (avidyā as
  the field, YS 2.4; identity view; the five vṛttis, YS 1.5–1.6); bodily entries (illness YS 1.30, the bodily
  companions YS 1.31, vāyus, doṣas); Jain passion grades (each defined by what it obstructs).
- **Temperament** (Vism III, from memory: the text calls reading temperament from behaviour the teachers' opinion,
  not authoritative, and notes mixed types): 3+ distinct cues from 2+ markers across 3+ units, one lexical direct
  match, no counter-evidence; if a rival reaches 75% of the leader's E_net, none maps. Never "you are a ... type".
- **Guṇa** (BhG 14.10–13, from memory: all three are present; the text gives signs of one rising): 2+ cues across
  2+ units, a direct item, the 75% tie rule. Framed as signs of increase, never as a nature.

## 9. States of an affliction (YS 2.4)
States apply only to *affliction* entries with a `states` array, and are never copied to equivalents. **Udāra
(active)** may be attached only when confidence is moderate or higher, a direct, uncapped, non-dialogue quote has a
present-time marker (`now`, `these days`, `every night`) and an object (an F2 detail), and the entry lists the state.
It is stated as the text's term and nothing more. **Prasupta** never: by the text it fits every unliberated being.
**Vicchinna** never: it needs another affliction to be active, which words cannot show. **Tanu** never as a label; a
reported lessening with practice is stored as `reported_change` with the quote. The burnt seed and any other grading
are never attached.

## 10. Overlap, grouping, caps, validators
Within an equivalence group (grade exact, partial or same-under-standpoint), one quote may support every member, but
each member must match its own markers, because an equivalence never transfers evidence. Across groups, one sentence
gives full weight to the best-fit group only, suggestive weight to one other, and nothing beyond that. If two
non-equivalent entries rest on an identical quote set, keep the best fit. Groups are connected components of mapped
entries; they keep each edge's grade and note (principles rule 5), and group confidence is the maximum of the members,
never raised by their number. Per reading: at most 5 groups, 8 entries, 4 members per group, and the kind caps. Rank
by confidence, E_net, units, earliest quote, then id. Every drop is logged. **Validators** (every candidate): V1
schema; V2 entry exists, is user-facing and mappable, and its marker has cites; V3 exact substring of the claimed unit
and the person's own words; V4 form; V5 exclusions; V6 relevance; V7 rationale (at most 45 words; no clinical,
psychology or science, diagnostic, prediction, universalising or certainty words; no unsupported "you always"; every
quoted string exact; `forbidden_claims.json`); V8 cites copied by code; V9 merge duplicates; V10 confidence, floor
and kind rules; V11 overlap and grouping; V12 caps; V13 final re-check.

## 11. Worked examples (cues are illustrative; the real ones come from `layers/diagnosis.json`)
- **M1: maps, moderate** (`dx:klesa-raga`, YS 2.7). q04 "Every night I scroll reels for hours and can't stop wanting
  more" is a cue-window match ("I can't stop wanting more": {stop, want}, parity 1 = 1) with F1: direct. q09 "When a
  holiday ends I'm already planning the next one on the drive home" shares no cue words; the recheck reads it as the
  marker's longing for a remembered pleasure, *implied*: indirect. E = 1.6, two units, one direct: moderate. Udāra
  may be attached ("every night", object "reels").
- **M2: maps, low** (`dx:nivarana-thina-middha`). "When I sit for japa in the evening my head gets heavy and I nod off
  before I finish one mala": the body words are allowed by the practice setting; the recheck gives *explicit*, so it
  is direct, with F2 and F3. E = 1.0 from one unit: low, since one unit cannot reach moderate.
- **M3: maps, high** (`dx:kasaya-krodha`). q02 "I snap at my kids over small things every evening" (cue window
  {snap, small}: direct); q06 "At work I stay angry at a colleague for days after a meeting goes wrong" ("I stay angry
  for days": direct); q11 "Even a slow queue makes me want to shout at the clerk" (subject "me"; recheck *implied*:
  indirect). E = 2.6, 2 direct units out of 3: high. No state (kaṣāya entries have none); it groups with
  `dx:klesa-dvesa` only if that entry qualifies on its own markers.
- **N1: not mapped** (`dx:klesa-dvesa`). q05: "I hold grudges" is a direct match but has no F1–F3 and is a single
  unit (`R_NO_SPECIFICITY`). q12: "Life is just busy" is `R_GENERIC`. Not enough evidence: no mapping, no confidence.
- **N2: not mapped** (`dx:kasaya-krodha`). q03: "My wife says I'm always angry, but honestly I'm not an angry person".
  Clause 1 is `R_OTHER_ATTRIBUTION`; clause 2 is `R_NEGATED`, kept as counter-evidence (0.6). E = 0: `R_BELOW_FLOOR`.
- **N3: not mapped** (the ālasya obstacle, YS 1.30; id not checked). Dialogue, self speaker `Me`: "Asha: You never
  finish anything you start." / "Me: Oh sure, I'm sooo lazy 🙄" / "Me: If you'd told me earlier I would have finished
  it." Asha's line is `R_NOT_OWN_WORDS` however well it fits a cue; the second is `R_SARCASM`; the third is
  `R_HYPOTHETICAL`. No evidence remains, so nothing maps.

## 12. Text basis and limits
YS 2.4 with the Bhāṣya (states, avidyā as the field); YS 2.2 (thinning by kriyā-yoga); YS 1.5–1.6, 1.30–1.31;
BhG 14.5–13; Vism III (temperaments); TaittU 2; Māṇḍūkya 3–7; MN 44. All cited from memory, not yet checked against
`data/`. Single quotes are treated as apostrophes (a known gap). The lexical filters are English heuristics, and the
blind recheck covers paraphrase.
