# Extraction report: Māṇḍūkya Upaniṣad and Gauḍapāda's Kārikā (Role S, single extraction, protocol insight-p1-single+spot)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Folders:
- /home/user/allprojects/tradition-ontology/shards/extraction/mandukya-upanisad/all/single/
- /home/user/allprojects/tradition-ontology/shards/extraction/mandukya-karika/all/single/
- Generator scripts: the matching `.../all/_gen/S/` folders, in `gen.py`, `ch1.py`, `ch2.py`, `ch3.py`, `ch4a.py`, `ch4b.py`, `ch4c.py`, `tail.py` and `lib.py`.

## What was checked, by code
- Every `original.text` equals its segment's `iast`. There are 0 mismatches and every segment has a teaching.
- Both `single/` folders validate to 0 errors.
- Every `replaced_by` in `skeleton_decisions.jsonl` exists in the teachings file.
- Every existing `data/` id linked from the output was listed with its definitions and checked (see "Homonym handling").
- No paraphrase contains the words "comment", "Śaṅkara" or "Ānandagiri". Commentators' readings appear only in `notes`, labelled as theirs.
- A non-empty paraphrase means the sense is stated in the paraphrase itself. It does not mean a judge has checked it.

## What I could not check
- Paraphrase faithfulness was not checked by code and no second reader has seen it. The judge is the check.
- No published translation or commentary was consulted, as the brief requires. Where a verse is obscure I marked it low and gave the minimal shared sense.

## Segment-level facts the judge and merger should know
- **Karika ref 2.23.** This segment holds two verses: the source marker "mandupk_2. 22" sits inside it. The first half is verse 2.22 and the second is 2.23. The edition has no segment 2.22, so I kept ref 2.23 with a note. The `original` text is the whole segment.
- **Textual corruptions in the edition**, noted in `notes`:
  - 1.5 reads "vadaitad", evidently for "vedaitad".
  - 1.21 has a corrupt first half ("mānasām anyam utkaṭam").
  - 2.16 reads "vaco".
  - 4.15 reads "kalasya" for "phalasya".
- **Duplicated verses**, cross-referenced with `cross_refs`:
  - 2.6 = 4.31 and 2.7 = 4.32.
  - 3.20–3.22 = 4.6–4.8.
  - 3.29–3.30 = 4.61–4.62.
  - 3.48 = 4.71.
- **Product-critical verses (the states layer).**
  - MU 3–5, 7 and 12 give the three states and the fourth.
  - GK 1.1–1.5 give the seats, enjoyments and satisfactions.
  - GK 1.10–1.15 compare the fourth with deep sleep:
    - 1.13 says prājña and the fourth share non-apprehension of duality, but only prājña has seed-sleep (bīja-nidrā).
    - 1.12 calls the fourth "sarvadṛk" (all-seeing), while MU 7 gives negations only. I recorded both and did not reconcile them.
  - GK 3.34–3.35 separate deep-sleep absorption (laya) from the restrained mind.
- **The obstacle counsel in GK 3.40–3.46**, recorded in the text's own terms:
  - 3.42: restrain the mind distracted in desire and enjoyment (vikṣepa) by a means (upāya), and treat laya "like desire". The construal of "suprasannaṃ laye" is moderate confidence, with commentators' readings in the note.
  - 3.43: remember that all is sorrow, and turn back from desires and enjoyments. Remembering that all is unborn is also given.
  - 3.44:
    - laya: awaken the mind (saṃbodhayet).
    - distraction: calm it again (śamayet).
    - kaṣāya: "sakaṣāyaṃ vijānīyāt", know the mind as sakaṣāya.
    - evenness (samaprāpta): do not stir it.
  - 3.45: do not relish the happiness (na āsvādayet), and be unattached through discernment.
  - 3.46: neither laya nor distraction, and that is brahman.
  - The four-fold name "rasāsvāda" comes from commentators. The Kārikā uses the verb "āsvādayet", and the note on `obs:rasasvada` says so. Other commentators' glosses of "kaṣāya" are not adopted, and the entry says its sense is discussed by commentators.
- **Buddhist-sounding vocabulary in Kārikā 4**, recorded as used with no verdict:
  - prajñapti, nimitta, paratantra, saṃkleśa, vijñāna, ābhāsa, lakṣaṇa-śūnya (called "śūnya" as an adjective);
  - kalpita and saṃvṛti, ādibuddha, kṣānti, sunirvṛta, buddha, tāyin, nāyaka, agrayāna, and "sanirvāṇa" at 3.47.
  - These are gathered in `cpt:gk-buddhist-vocabulary`, which states that no verdict is given.
- **4.1 and 4.99.** The text does not name the one saluted at 4.1, and the commentators divide on whom it means. At 4.99 "naitad buddhena bhāṣitam" is ambiguous. Both are recorded without a reading.

## Orchestrator rules applied (mid-task message)
1. **Homonym handling.**
   - I listed every existing `data/` id my output touches, with all its definition lineages (87 existing of 171 ids used).
   - I kept an id where a matching lineage sense already exists. These include trm:visva, taijasa, turiya, prajna-mandukya, prajnanaghana, jagrat, susupti, svapna, ghatakasa, amanibhava, asparsa-yoga, prapancopasama, advaita, laya, viksepa, sama, dama, cpt:ajativada, cpt:turiya, and obs:laya, viksepa, kasaya, rasasvada and four-obstacles-to-samadhi.
   - For ids whose existing definitions differ in sense, I made sense-specific ids (in `lib.py` RENAME, applied at write time). Examples:
     - trm:kasaya-gk (the existing one is Jain anger, pride, deceit and greed).
     - trm:akasa-gk (Vaiśeṣika), trm:alata-gk (Rāma-hṛdaya), trm:svabhava-gk (Madhyamaka), trm:citta-gk (Yoga), trm:paramartha-gk (Yogācāra), trm:prajna-gk (Dvaita), trm:prapanca-gk (Madhyamaka), trm:aja-gk (a she-goat in the Upaniṣadic entry), trm:vaisvanara-mu (Bhagavad Gītā 15.14).
     - cpt:maya-gk, cpt:pranava-gk, cpt:vaisvanara-mu.
     - prc:omkara-dhyana-mandukya (the existing prc:omkara-dhyana is Purāṇic, Mārkaṇḍeya Purāṇa 42).
     - phn:gk-the-fourth for the Kārikā's fourth; phn:mandukya-the-fourth is kept for the Upaniṣad.
   - Not everything was renamed. Please dedupe at merge: some terms with "-gk" or "-mu" are sense-specific duplicates of a broader entry, for example trm:jnana-gk and trm:krpana-gk.
   - `trm:moksa` and `trm:vikalpa` are kept with a lineage-specific contribution (the Kārikā's sense), as are `trm:samsara` and `trm:maya`.
2. **Commentators' glosses** are in `notes` only (labelled "commentators read..."). I removed several glosses from paraphrases during the task: "[to understanding]" at 3.15, and "residue" for kaṣāya at 3.44 (now "know it as having kaṣāya (sakaṣāya)").

## Skeleton decisions
- **Māṇḍūkya Upaniṣad, 9 existing entries** (all at level `sourced`):
  - 8 upgrade. The ids are the same and the originals are re-extracted.
  - 1 correct: `tea:mandukya-upanisad:8-11` is split into 8, 9, 10 and 11 (the segments are separate).
- **Kārikā, 33 skeleton entries** (23 upgrade, 10 correct, 0 retire). Refs were not wrong.
  - 1.10 corrects the "capable of ending" and "Lord" wording.
  - 3.44 corrects the glosses "dullness" and "latent impressions".
  - 4.42 corrects a merger of two ideas.
  - 4.73-74 splits into 4.73 and 4.74.
  - 4.87-88 splits into 4.87 and 4.88.
  - 4.90 and 4.99 correct glosses that are not in the text.
  - 4.100 corrects "pure", which is not in the verse.
  - 4.2 upgrades, with a note that "by scripture" is a gloss.

## Open points for the merger and later waves
- **Māṇḍūkya Upaniṣad 3–4.** The "seven limbs and nineteen mouths" are not enumerated in the text. The commentators' lists are in the notes only, and confidence is moderate.
- **Māṇḍūkya Upaniṣad 6.** The referent of "eṣaḥ" is unstated. The paraphrase keeps "this one", and the note gives the commentators' reading (prājña).
- **Māṇḍūkya Upaniṣad 9–11.** The fruit-promises (phala) are recorded. Whether they count as arthavāda is left to the interpretation layer, and the theses say so.
- **Disputes.**
  - The five Kārikā disputes have an unnamed opposing party because the text names none, and the lineage field is omitted for that side.
  - Please check that the merge accepts a side with `party` and no `lineage`. The validator only counts sides.
- **Thesis entries.** `tea:mandukya-upanisad:thesis` and `tea:mandukya-karika:thesis` are at moderate confidence. The six marks are cited by ref and were assessed by me, not by a second reader.
- **Obstacle members.** `obs:four-obstacles-to-samadhi` has members laya, vikṣepa, kaṣāya and rasāsvāda. The description says the fourfold name is the commentators'; the Kārikā gives its own counsel for each verse.
- **Restricted content.** The Kārikā contains no restricted practices (no body-cutting, metals, extreme retention, sexual rites or prolonged fasting). No `restricted` flags were needed.
