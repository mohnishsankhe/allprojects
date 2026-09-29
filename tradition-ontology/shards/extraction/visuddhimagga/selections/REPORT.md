# Visuddhimagga selections, single extraction (Role S)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Paths:
- Prepared: `/home/user/allprojects/tradition-ontology/sources_raw/prepared/visuddhimagga-selections/` (`segments.jsonl`, `META.json`)
- Output: `/home/user/allprojects/tradition-ontology/shards/extraction/visuddhimagga/selections/single/`
- Scripts: `/home/user/allprojects/tradition-ontology/shards/extraction/visuddhimagga/selections/_gen/S/`

## Step 1: preparation (by code)
- Source: the GRETIL Devanāgarī annotated Visuddhimagga (PTS ed., Rhys Davids 1920–21; input by the Dhammakaya Foundation; CC BY-SA 4.0 per its header). The file was split at the `[pge NNN]` markers, giving 713 pages.
- Each page keeps its running head and the PTS variant-reading footnotes (`deva`, `iast`). Transliteration is `indic_transliteration` DEVANAGARI→IAST. The e-text's artefacts (for example `n'; `) are left as they are.
- `segments.jsonl` has fields ref, chapter, page, deva, iast (89 segments). `META.json` records edition, licence, method and the page ranges above.
- Chapter boundaries came from the running heads: III 84–117, IV 118–171, VIII 230–294, IX 295–327, XIV 438–481, XVII 518–587, XX 608–639, XXII 674–699.

## Step 2: extraction
- One teaching per page, split into /2, /3, … when a page holds several distinct teachings. Ids are `tea:visuddhimagga:<chapter>.p<page>`.
- `original.text` is an exact substring of the page IAST (anchor to anchor, copied by code). Hyphenated line breaks and footnote digits are kept because they are in the segment.
- The temperament marks (posture, work, eating, seeing, states, what suits) are recorded as the text gives them in `phn:vism-carita-*`. The text's own caution (III p. 107: not to be relied on as essential) is attached to each entry.
- Hindrance entries carry, for each hindrance, the opposed jhāna factor (IV p. 141), how it obstructs (IV p. 146), and the XIV marks (mark, function, manifestation, proximate cause).
- Practice warnings are verbatim Pali spans from the pages. Examples: counting "not below five, not above ten, no gap" (VIII p. 278); the connecting warning (p. 280); whom not to begin mettā with (IX p. 296); the earth-kasiṇa eye-opening caution (IV p. 125).
- Restricted practices (foulnesses, mindfulness occupied with the body) are summary-only and flagged `restricted`, with only the text's statement that they are not to be enlarged. No procedures are given. Teachings touching them carry `restricted: true`.
- The Jātaka narratives of patience and the leaping-rapture stories are paraphrased as told; each carries a note that they are examples and not practices.
- Nothing is diagnostic or predictive. The ten imperfections of insight (XX) are reported as the text's list.

## Skeleton decisions (`skeleton_decisions.jsonl`)
- Upgrade to page ids (17): 3→3.p84/2; 3/2→3.p85/3; 3/3→3.p90; 3/4→3.p97/2; 3/5→3.p98/2; 3/6→3.p101/2; 3/7→3.p102; 3/8→3.p110/2; 3/9→3.p111/2; 3/10→3.p114/3; 4→4.p125; 4/4→4.p143/4; 4/5→4.p144/2; 8/4→8.p278/2; 9→9.p296; 9/2→9.p307; 9/3→9.p298 (the chain runs pp. 298–306).
- Correct (2):
  - 4/3 → 3.p117/2. The quoted Pali is the nine matters to be taught, on p. 117 of ch. III. The list of the ten skills in absorption belongs to ch. IV (about p. 128), not p. 117.
  - 9/4 → 9.p319. The near and far enemies are on p. 319, with only the introduction on p. 318.
- Left undecided (outside my pages): 3/11 (p. 118 is actually the opening of ch. IV, so the skeleton is filed under the wrong chapter — worth an orchestrator correction), 4/2, 4/6, 8, 8/2, 8/3, 8/5, 8/6, 8/7, 8/8.

## Moderate-confidence entries (for the judge; there are no `low` ones)
- 3.p104/2 and 3.p105: the footprint terms ukkuṭika, anukaḍḍhita and sahasānupīḷita.
- 3.p111/2: the edition prints catukkajjhānikā for the fourth divine abiding and the four immaterial states. Context points to the fourth jhāna, but the page does not say so; kept in the notes only.
- 3.p113/2: counts of counterpart-sign, intrinsic-nature and moving objects.
- 4.p144/1: the leaping-girl story, compressed.
- 8.p273/3: the verse on four kinds at the nose-tip.
- 8.p275, 8.p276, 8.p277/1: the reciters' disagreement and the objection-and-answer passage.
- 9.p306/2: the Cittalapabbata story is very compressed in the text.
- 9.p308/3: the word-by-word glosses.
- 14.p471: dense Abhidhamma counts.
- 22.p694: dense pairings.
- Judge should check the numbers in 3.p113/2, 14.p471, 22.p694.

## Open points and things I could not check
- Only the local e-text was used, so the PTS variant footnotes in the pages were not consulted and no printed edition was compared.
- The e-text may diverge from print, as its header says.
- I did not verify some skeleton-linked homonym ids beyond reading their entries: trm:samadhi, trm:sukha, trm:vicara and trm:viveka have lin:theravada or early-Buddhist definitions in the Pali sense, so I linked to them. trm:viveka is not linked in any teaching.
- The Āghātapaṭivinaya-sutta's five ways are only referred to on IX p. 300, not listed; I did not invent them.
- ch VIII: pp. 266–281 include the first-tetrad word commentary and stop where the connecting similes are still running (p. 281 into p. 282). If the orchestrator wants a stricter "counting and connecting only", drop pp. 272–277.
- Not done by design: `REPORT.md` is not written to disk (returned here), and no git.
