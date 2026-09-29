_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

Output folders (scripts in the matching `_gen/S/`):
- `shards/extraction/tattvartha-sutra/karma-passions/single/`
- `shards/extraction/taittiriya-upanisad/kosa/single/`
- `shards/extraction/katha-upanisad/chariot/single/`
- `shards/extraction/prajnaparamita-hrdaya/all/single/`
- `shards/extraction/prajnaparamita-hrdaya-sanskrit-short/all/single/`

Confidence spread of the teachings (high / moderate / low), for the judge's spot-check:

| Unit | High | Moderate | Low |
|---|---|---|---|
| Tattvārtha | 55 | 19 | 2 |
| Taittirīya | 24 | 12 | 1 |
| Kaṭha | 11 | 6 | 1 |
| Heart Sūtra Chinese | 5 | 5 | 2 |
| Heart Sūtra Sanskrit-short | 8 | 4 | 0 |

The judge must check every low entry:
- Tattvārtha: 6.19 (scope of "sarveṣām") and 8.24 (construal of nāma-pratyayāḥ).
- Taittirīya: 2.9.1 (the verb spṛṇute).
- Kaṭha: 1.3.2 (how the "Nāciketa" clause is construed).
- Chinese Heart Sūtra: 1.1 (the Ming imperial preface). The other low entry is the ch1 chapter summary of that same preface.

**Product-note items**
- **Five sheaths:** the Taittirīya text gives five selves "made of" (-maya) food, breath, mind, understanding and bliss, each within the last and filling it. The parts (head, wings, self, tail/support) are recorded per sheath in 2.1.1 to 2.5.1. The word kośa is not in the text; this is noted on the entries. `cpt:five-sheaths` and `cpt:bhrgu-inquiry-sequence` (Bhṛgu's five identifications of brahman, ch. 3) are written.
- **Chariot:** Kaṭha 1.3.3-9 are per verse. The concept is `cpt:katha-chariot-simile`, the unyoked mind is `obs:ayukta-manas`, and the practice is `prc:yukta-manas`. The ascending order of 1.3.10-11 is `cpt:katha-ascending-order`.
- **Kaṣāyas and binding:**
  - Tattvārtha 8.9 names the four passions, each with four varieties (anantānubandhī, apratyākhyāna, pratyākhyāna, saṃjvalana). The sūtra does not define the varieties. The commentarial (Sarvārthasiddhi) reading is kept in `notes`, labelled as the commentators' reading.
  - The binding process is written up in 6.1-6.5, 8.1-8.3 and 8.21-8.24, with `cpt:bandha`, `cpt:four-aspects-of-bandha`, `cpt:eight-karmas` and `cpt:four-kasayas-sixteen`.
- **Heart Sūtra emptiness:** `cpt:emptiness-of-the-aggregates` is emitted by both Heart Sūtra units with their own `rests_on`.

**Points for the orchestrator**
1. The Tattvārtha segment file numbers sūtra 8.16 as "8.116". My id is `tea:tattvartha-sutra:8.16`, with a note, and the original is copied from that segment.
2. The Chinese unit's chapter 1 (1.1) is an imperial Ming preface, not part of Xuanzang's text. Chapter 2 opens with an unnamed preface (2.1). Both are tagged and noted as prefaces, and the thesis covers only 2.2-2.8.
3. Both Heart Sūtra units share `src:prajnaparamita-hrdaya`. Thesis ids are `tea:prajnaparamita-hrdaya:thesis` (Chinese) and `tea:prajnaparamita-hrdaya:thesis-sanskrit-short`. Sanskrit-short chapter id is `tea:prajnaparamita-hrdaya:ch1-sanskrit-short`. Chinese chapter ids are `ch1` and `ch2`.
4. The Chinese unit has no skeleton decisions because the existing skeleton refs are `s*` and `long.*`. The `long.1` and `long.2` entries have no segment in either unit and are undecided; they need a decision from whoever handles the longer recension.
5. Split verses (e.g. Kaṭha 1.3.3-4, 1.3.5-9, Taittirīya 2.8.1-5) have `replaced_by` pointing at the first new id; the reason text lists the rest.
6. Taittirīya segments each open with the verse that closes the previous anuvāka, so an anuvāka's own verse sits in the next segment. This is noted on the affected entries. `/2` and `/3` sub-teachings carry exact-substring originals.
7. Recension issue: Tattvārtha follows the Digambara numbering per META. The Śvetāmbara text differs in numbering, in the tīrthaṅkara list (6.24) and in some wording. I noted this but did not check it against the Śvetāmbara text.
8. I did not consult commentaries for Kaṭha or Taittirīya; they are not in the local segments. Notes that say "commentators divide" are limited to Kaṭha 1.3.1, 1.3.2, 1.3.11 and 1.3.13. In Taittirīya I softened them to "the passage is obscure". The Sarvārthasiddhi reading of the four kaṣāya varieties is my recollection and is labelled as such.
9. The judge should check that the linked ids in the `terms` and `concepts` fields resolve to the right sense, especially reused existing ids (e.g. `trm:apratyakhyanavarana`, `trm:anantanubandhin`). I confirmed existence of most of these, but not their content.
10. I created `tch:sariputra` because only Pali `tch:sariputta` exists.
11. I could not check anything outside these five folders and did not run git.
