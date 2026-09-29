_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Covered.** I reused d3a.py and d3b.py (3.1–3.29) after reading a sample; their paraphrases were sound. I wrote 3.30–4.34 in d3c.py, d4a.py and d4b.py, with ents.py, ents2.py and build.py. Scripts and the dropped_links.json list are in `.../p3-4/_gen/S/`. I edited common.py to tolerate mixed tag strings.

**Product-note items**
- **3.37 (powers as obstacles):**
  - The sūtra entry and the bhāṣya entry are kept separate.
  - `obs:siddhis-as-upasarga` is a contribution, linked to the existing `dsp:siddhis-sign-or-obstacle`.
  - The bhāṣya's pronoun in "taddarśana" is left open in a note, and that entry is moderate.
- **3.51 (warning):**
  - Two bhāṣya entries, one for the four yogins and the invitation and one for the reflection and the warning about pride and heedlessness (pramāda), copied exactly from the segment.
  - `prc:ys-declining-invitations` and `obs:sanga-smaya-pramada` hold the verbatim Sanskrit warnings.
- **Vāsanā and saṃskāra (4.8–4.11):**
  - The vāsanā and saṃskāra concepts, terms and `prc:vasana-ksaya` are written from the text only.
  - 4.10 also records the "apare" versus "ācārya" positions on the size of the mind as `dsp:size-of-citta`.
- **The mind (4.15–4.23):**
  - Vyāsa's opponents are flagged `reported_by_opponent: true` and are unnamed as schools.
  - Two new disputes, `dsp:ys-object-independent-of-mind` and `dsp:ys-citta-self-luminous-or-seen`, are recorded with both sides (both `queued`).
- **Kaivalya:**
  - Covered at 3.50, 3.55, 4.26, 4.29–4.34; `pth:yoga-sutra-kaivalya-sequence` is a contribution with stages.
  - The sūtra 4.34 entry is high confidence.
- **Powers:** Every powers entry carries a note that they are recorded as the text states them, not promised. 3.39, 3.40 and 4.1 also say no method is given. The 4.1 herbs and elixir (rasāyana) get no practice entry.

**Judge should check.**
- The three low entries: 3.53 (sūtra, bhāṣya and its Vārṣagaṇya second entry).
- Moderate entries with disputed construals: 3.35, 3.43, 3.44–3.48, 3.51, 3.52, 4.13, 4.14, 4.20–4.23, 4.33.
- 4.33: the bhāṣya calls the finite-or-endless question "avacanīya" and then concludes "vyākaraṇīya"; I kept both words as they stand.
- The thesis entry: my reading of the six marks. I recorded no verse as arthavāda and no verse marking novelty; that is left to the interpretation layer (P7).

**Choices to note.**
- Concept ids referenced in teachings (e.g. `cpt:object-independent-of-mind`) were checked against `data/concepts.json` or my own emitted concepts.
- I dropped 91 invented or unresolvable link ids (198 links) from the `terms`, `disputes` and other link fields. Most were ad-hoc compounds such as `trm:sthairya`, `trm:vasitva`, `trm:purusa-jnana`.
- Two dispute ids I had planned (`dsp:ys-past-and-future-exist`, `dsp:ys-is-samsara-endless`) were dropped because the text gives only one side.
- 4.3 named Nandīśvara. `tch:nandisvara` in the data is the Prābhākara author, so I made a new low-confidence `tch:nandisvara-bhasya-example`.
- I remapped `obs:klesa` to the existing `obs:five-klesas`.
- Band choice in `pth:yoga-sutra-kaivalya-sequence`: dharma-megha (4.29) and the cessation of afflictions and karma (4.30–4.31) are set to B8 because the data model names dharmamegha as B8; the interpretation layer may revise this.
- Where a sūtra's tag string gave two standpoints and no path, `_tags` in common.py keeps the first standpoint and picks a default path by standpoint. The path may need review.
- Entities from earlier skeleton work are emitted as contributions under the same ids. I did not emit `dsp:siddhis-sign-or-obstacle` because the text gives one side.

**Not checked.** I could not compare against any published translation; none was consulted and none is available offline. I did not read the whole of d3a and d3b line by line (3.1–3.29). I read 3.6–3.15 and the 3.16–3.26 paraphrase openings; 3.1–3.5 and 3.27–3.29 I only ran, and read the anchors for. No skeleton decision was made by comparing the skeleton paraphrase in detail for every entry; only 3.39, 3.40 and 4.29 were flagged for wording.
