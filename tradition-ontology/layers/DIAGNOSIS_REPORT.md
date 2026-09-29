_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Files** (all under layers/)
- `/home/user/allprojects/tradition-ontology/layers/diagnosis.json`: JSON list, UTF-8, indent 1.
- `/home/user/allprojects/tradition-ontology/layers/_gen/diagnosis/`:
  - `build.py` validates and writes the layer; run it with `python3 layers/_gen/diagnosis/build.py`.
  - The content scripts are `common.py`, `entries_yoga.py`, `entries_gita_upa.py`, `entries_buddhist.py` and `entries_jain.py`.
  - `idx.py` fetches segments and teachings.
  - `vism.py` reads the Devanagari PTS e-text as IAST, page by page (it uses the e-text's page markers).
  - `build_report.json` holds the full machine report.
- The earlier cut-off run had left `_gen/diagnosis/` empty, so there was nothing to reuse.

**Coverage**
- **Yoga Sūtra with Vyāsa:**
  - The 5 kleśas, each with the four states of YS 2.4 plus Vyāsa's fifth, the burnt seed.
  - The 5 vṛttis, each afflicted or unafflicted.
  - The 9 obstacles and the 4 companions of distraction.
  - One entry for Vyāsa's five grounds of mind (YB 1.1), and the vitarkas of YS 2.33–34.
  - Powers as obstacles (YS 3.37, 3.51).
- **Gītā:**
  - The 3 guṇas, one gone beyond the guṇas, and one of steady wisdom.
  - The anger chain (2.62–63), desire-anger as the enemy (3.36–43, 16.21), and the demonic endowment (16.4).
  - Arjuna's dejection, and the restless mind.
- **Taittirīya, Māṇḍūkya, Gauḍapāda, Kaṭha:**
  - The 5 sheaths.
  - The 5 vital currents, from TU 1.7.1, TU 2.2.1, KU 2.2.3 and Vyāsa on YS 3.39.
  - The 4 states of MāU 2–7.
  - Gauḍapāda's laya, vikṣepa, kaṣāya and rasāsvāda, plus fear of the no-contact yoga (3.39) and the no-mind state.
  - From the Kaṭha: the unrestrained senses (the chariot), the outward-turned senses, choosing the pleasant, and yoga as firm holding of the senses.
- **Buddhist:**
  - The 5 hindrances and the 10 fetters.
  - The 3 unwholesome roots, craving, heedlessness (Dhp 21), and muddled mindfulness (MN 118).
  - The contracted and scattered mind of MN 10.
  - The 6 temperaments, with posture, work, eating, seeing and mental states from Vism III pp. 104–107.
  - Three more from the Visuddhimagga: the ten impediments, the ten imperfections of insight, and the near and far enemies of the divine abidings.
- **Jain:**
  - The 4 kaṣāyas, each with the four intensities of TS 8.9, and the nine quasi-passions.
  - Wrong view, non-abstention and heedlessness (TS 8.1).
  - Sorrowful and cruel dwelling (TS 9.28–35).

**Checked by code (build.py)**
- Unique `dx:` ids and all required fields.
- `kind`, `lens` and `grade` values are from the allowed sets.
- Every definition, marker, state, equivalence and pairing has at least one citation, and the citations are well-formed.
- Every equivalence target exists and has a matching reverse link with the same grade.
- Missing ontology_refs are dropped: none remain dropped, and every entry now has refs.
- A scan for clinical and modern-psychology words. "diagnos" is allowed only as a negation inside `not_to_be_read_as`. The scan caught 11 hits, all fixed.
- Every cited ref exists in the prepared segments. Every Visuddhimagga page exists in the e-text.
- The written file is re-read and re-checked.

**Checked by reading**
- Every definition and marker was written from the source text itself: YS and Vyāsa, the Gītā, TU, MāU, GK, KU, MN 10, DN 22, MN 118, the Dhammapada, TS, and the Visuddhimagga pages cited.
- For DN 2 I read the local copy of the Pali (bilara, dn2:68–74).

**Citations not yet in data/ (82)**
- **Visuddhimagga (27):** 3.p90, 3.p101, 3.p102, 3.p104, 3.p105, 3.p106, 3.p107, 3.p114; 4.p125, 4.p140, 4.p141, 4.p146; 9.p318, 9.p319; 14.p468, 14.p469, 14.p470, 14.p471; 17.p569, 17.p570; 20.p633, 20.p637, 20.p638; 22.p682, 22.p683, 22.p684, 22.p694.
- **Kaṭha (14):** 1.2.1, 1.2.2, 1.2.5, 1.2.6, 1.3.3–1.3.9 (each verse), 2.2.3, 2.3.10, 2.3.11.
- **Gauḍapāda (9):** 1.14, 1.15, 3.31, 3.35, 3.40, 3.42, 3.43, 3.46, 3.47.
- **Gītā (8):** 16.21, 18.26, 18.27, 18.28, 18.35, 18.37, 18.38, 18.39.
- **Dhammapada (8):** 3, 4, 202, 221, 251, 334, 335, 338.
- **Taittirīya (8):** 2.2.1, 2.3.1, 2.5.1, 3.2.1, 3.3.1, 3.4.1, 3.5.1, 3.6.1.
- **Tattvārtha (4):** 9.30, 9.31, 9.32, 9.33.
- **Vyāsa bhāṣya (3):** 1.9, 2.7, 2.8.
- **Māṇḍūkya (1):** 8.
- Many of these are already covered by existing range ids, for example gita 18.26-28 and 18.36-39, katha 1.3.5-9, tattvartha 9.30-33, taittiriya 3.2.1-3.6.1 and mandukya 8-11. `build_report.json` lists them all.

**Practice ids used (54)**
- **Yoga Sūtra (9):**
  - px:viveka-khyati-ys-2-26, px:pratipaksa-bhavana-ys-2-33, px:kriya-yoga-ys-2-1, px:dhyana-ys-2-11
  - px:abhyasa-vairagya-ys-1-12, px:ekatattva-abhyasa-ys-1-32, px:maitri-bhavana-ys-1-33, px:sanga-smaya-akarana-ys-3-51
  - px:approach-a-teacher-bg-4-34 (a Gītā practice, also paired with YS doubt)
- **Gītā (7):** px:guna-witnessing-bg-14-19-23, px:bhakti-yoga-bg-14-26, px:indriya-samyama-bg-2-58-61, px:bearing-the-surge-bg-5-23, px:atma-anatma-viveka-bg-2-11-30, px:abhyasa-vairagya-bg-6-35, px:returning-the-mind-bg-6-26
- **Upaniṣads and Gauḍapāda (7):** px:bhrgu-inquiry-tu-3, px:omkara-upasana-mau-8-12, px:manonigraha-gk-3-40-46, px:recollecting-suffering-and-the-unborn-gk-3-43, px:katha-inward-withdrawal-1-3-13, px:inward-turned-gaze-ku-2-1-1, px:sreyas-preyas-viveka-ku-1-2-2
- **Suttas (8):**
  - From MN 10: px:satipatthana-nivarana-contemplation-mn10-36, px:khandha-contemplation-mn10-38, px:satipatthana-ayatana-contemplation-mn10-40, px:satipatthana-citta-contemplation-mn10-34, px:four-truths-contemplation-mn10-44, px:sati-sampajanna-mn10-8.
  - px:aloka-sanna-dn2-68 (DN 2).
  - px:anapanasati-first-tetrad (MN 118).
- **Visuddhimagga (15):** px:pathavi-kasina-vism-4, px:metta-bhavana-vism-9, px:paccaya-pariggaha-vism-19, px:namarupa-pariccheda-vism-18, px:asubha-bhavana-vism-6, px:kayagatasati-32-parts-vism-8, px:brahmavihara-bhavana-vism-9, px:colour-kasina-vism-5, px:six-recollections-vism-7, px:maranasati-vism-8, px:upasamanussati-vism-8, px:catudhatuvavatthana-vism-11, px:ahare-patikulasanna-vism-11, px:maggamagga-vavatthana-vism-20
- **Tattvārtha (9):** px:uttama-ksama-ts-9-6, px:uttama-mardava-ts-9-6, px:uttama-arjava-ts-9-6, px:uttama-sauca-ts-9-6, px:anupreksa-ts-9-7, px:tattvartha-sraddhana-ts-1-2, px:vrata-ts-7-1, px:dharmya-dhyana-ts-9-36, px:maitri-pramoda-karunya-madhyastha-ts-7-11

**Practices that need a safety-tier review.** These pairings are as the texts give them; the practice layer should decide the tier.
- Two include tapas: kriya-yoga-ys-2-1, and bhrgu-inquiry-tu-3 (Varuṇa tells Bhṛgu to seek through tapas).
- asubha-bhavana-vism-6 is contemplation of decay, which the schema says is never gentle.
- maranasati-vism-8 is contemplation of death.
- ahare-patikulasanna-vism-11 concerns food.
- vrata-ts-7-1 includes the vow of celibacy.
- pathavi-kasina-vism-4 and colour-kasina-vism-5 are kasiṇa (disk) practices.

**Judgement calls (worth a DECISIONS entry; I did not edit DECISIONS.md)**
1. **Hindrance similes.** DN 2 applies debt, disease, prison, slavery and desert road to the five hindrances as a set, listed in the same order as the hindrances. Pairing one image to each hindrance is the commentators' reading, and each marker says so. Separately, Vism XIV p.470 itself says remorse is "to be regarded as slavery". For DN 2 I cited the existing id tea:samannaphala-sutta:67-74, which is skeleton.
2. **Temperaments.** Vism III p.107 says its own method of reading temperament from behaviour is only the teachers' opinion and not authoritative, that others can adopt the same behaviour, and that the marks blur when temperaments are mixed. I added this caution as a cited definition in all six temperament entries and in their `not_to_be_read_as`.
3. **Jain passions.** The Tattvārtha only names the passions and their four grades, so the markers are thin and stay close to the plain meaning of each word. The commentators' account of what each grade blocks is not cited, because it is not in data/. The pairing of forbearance, softness, straightness and purity (TS 9.6) against anger, pride, deceit and greed is by the meaning of the words; each entry says the sūtra itself does not state it.
4. **Empty cues.** 13 markers deliberately have no cues, so that nobody gets matched to them:
   - the five vital currents;
   - the fourth state (turīya), one beyond the guṇas, one of steady wisdom, the no-mind state, and the Kaṭha's highest state;
   - lust for form and lust for the formless (the text gives no description of how they show);
   - the one-pointed ground in the grounds-of-mind entry.

   The vital currents also have no paired practices, and the powers that YS 3.39–40 attach to them stay summary-only.
5. **Words that look alike but differ are kept separate**, and each entry says so:
   - Gauḍapāda's kaṣāya is not the Jain kaṣāya.
   - avirati means greed for objects in the Yoga, but not having taken the vows in the Jain text.
   - pramāda in the Yoga, the Jain text and the Dhammapada are three different uses.
   - The Yoga's smṛti (memory) is not the Buddhist sati (mindfulness).
   - Jain māyā (deceit) is not the Vedānta māyā (illusion).
   - I left the Advaita ids cpt:mithyatva and trm:mithyatva out of the Jain wrong-view entry.
6. **Left out on purpose:**
   - The Jain "activity" (yoga) cause of bondage, which is not something to recognise in a person.
   - The leśyās, which TS 2.6 names only.
   - The 22 hardships (parīṣaha), because of the fasting risk.
   - YS 1.34 and Gītā 4.29 and 5.27, which are breath control.
7. **Numbering:** the Yoga Sūtra follows the Āgāśe/GRETIL edition, so powers-as-obstacles is 3.37 and the five vital currents are defined in Vyāsa on 3.39. The Tattvārtha follows the Digambara recension. The prepared Tattvārtha segment file has a ref "8.116" that is probably 8.16; I did not use it.

**Not checked or open**
- My English renderings were not compared against a second translation.
- Equivalences across traditions pull in citations from the other tradition's text, so an entry can be held back by the verification level of another text.
- The Vyāsa segment for 1.31 also contains the lead-in to 1.32; I cite that sentence as YB 1.31.

**Rules followed:** I did not run git, and wrote nothing outside `layers/`.
