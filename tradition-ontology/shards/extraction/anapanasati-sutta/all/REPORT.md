_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Scope.** Role S single extraction of MN 10, DN 22 and MN 118. Output is in `/home/user/allprojects/tradition-ontology/shards/extraction/<slug>/all/single/`, where `<slug>` is `satipatthana-sutta`, `mahasatipatthana-sutta` or `anapanasati-sutta`. Scripts are in `…/all/_gen/S/`: `lib.py`, `t_*.py` for teachings and `e_*.py` for entities and skeleton decisions. The paraphrases were written by hand from the Pali; the Sujato English was not used to draft them.

**Checked by code**
- Every segment is covered: 41/41, 22/22 and 43/43.
- Every `original.text` equals its segment exactly. The one exception is mn118:26/2, which is an exact substring.
- No duplicate ids. All `cross_refs`, `replaced_by` and entity `rests_on` ids resolve within these shards.
- Every skeleton teaching has a decision.

**Ids and structure**
- Ids follow `tea:<slug>:<segment ref>`, for example `tea:satipatthana-sutta:mn10:36`. Each text also has `ch1` and `thesis` entries. The prepared texts have a single chapter, so `ch1` just records the structure.
- DN 22 segments that repeat MN 10 are paraphrased briefly with `cross_refs` to the MN 10 entries.
- Sentence-level extra: `tea:anapanasati-sutta:mn118:26/2` holds the text's own condition, "Nāhaṁ, bhikkhave, muṭṭhassatissa asampajānassa ānāpānassatiṁ vadāmi". It is also in `prc:anapanasati` prerequisites.

**Product points**
- **Hindrances (mn10:36, dn22:13):** the sutta only says the monk knows each hindrance as present or absent, and knows how it arises, is abandoned and does not recur. It does not state the conditions of arising or removal. This is flagged in `notes` and in the `obs:` descriptions, and no antidotes were invented. The same applies to the fetter in mn10:40.
- **Craving (dn22:19-20):** it says where craving arises and where it ceases (the "dear-looking, pleasant-looking" list). This is recorded in `trm:tanha`, `trm:piyarupa-satarupa` and `obs:tanha`.
- **Sixteen steps:** the text does not number them. They are counted from the four tetrads (mn118:18-21) and mapped to the four foundations as the text does at mn118:24-27. Path bands are copied unchanged from the existing skeleton `pth:` entries.
- **Awakening factors (mn118:30-39):** they are aroused in a dependent sequence. The seclusion/dispassion/cessation/relinquishment qualifiers belong to a separate step at mn118:42, not to the arising sequence.
- **Restricted practices:** none occur. The nine charnel-ground contemplations are recorded as the text gives them, with the comparison formula.

**Skeleton corrections**
- MN 10 `2.1`: "direct path" is a disputed rendering of ekāyana, so the new entry keeps the Pali term.
- MN 10 `6-9`: two separate sections were merged.
- MN 118 `17-22`: the place/posture, the four tetrads and the closing are separate segments.
- MN 118 `29-43`: the skeleton attached the qualifiers to the wrong step.
- The other 18 skeleton teachings are upgrades. Decisions with several replacements carry an extra `also_replaced_by` list.

**Low and moderate confidence for the judge**
- Low: mn10:2 and dn22:1, because ekāyana and ñāya are not glossed and their renderings are disputed.
- Moderate:
  - mn10:4 and dn22:2 (parimukhaṁ, sabbakāya).
  - mn10:32-34 and dn22:11-12 (sāmisa/nirāmisa, mahaggata and the other paired mind-states).
  - mn10:47-48.
  - dn22:18 and dn22:21 (long definitional segments, condensed).
  - mn118:4, 8, 14, 17, 18, 19, 21, 24-27, 38, 42.
- Commentators' readings appear only in `notes` and are stated generically, without naming a commentary.
- Also worth a look: the three thesis entries and the DN 22 definition lists.

**Not checked or open**
- The middle of the long repeated lists in dn22:19-20 and part of dn22:21 were read only in part, because they repeat.
- Entities were not fidelity-checked beyond schema validation.
- Existing skeleton entities (paths, obstacles and others) carry `rests_on` ids of the retired skeleton teachings, for example `tea:satipatthana-sutta:36-37`. The merge should remap them via `skeleton_decisions`.
- Ids that did not exist in `data/` and are newly introduced here: `tch:mahacunda`, `tch:mahakappina`, `cpt:anapanasati-fulfilment-chain`, `cpt:five-upadanakkhandha`, `obs:abhijjhadomanassa`, `obs:samyojana-arising-with-sense-base`, `obs:tanha`, `pth:noble-eightfold-path-dn22`, and 16 new `trm:` terms.
- No git was run, and nothing was written outside the three sutta folders.
