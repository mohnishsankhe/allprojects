# U03-principal-upanisads — skeleton sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Owner of **lin:upanisadic** and **ult:upanisadic**. The generator scripts are in `_gen/` (part1–part10, `common.py`). `_gen/check_refs.py` checks cross-references, and `_lookup.py` and `_locate.py` look up refs in the local e-texts.

**Method note.** Everything was written from model knowledge, then refs were spot-checked against local e-texts in `sources_raw`:
- the Advaita-Śāradā root texts (`raw_etexts/vedAntam/advaitam/advaita-shAradA/mUla/`)
- the ebhāratī copies of the Kena, Aitareya, Chāndogya and Maitrāyaṇī
- the Jaiminīya Upaniṣad Brāhmaṇa e-text

345 of 446 teachings carry the note "Ref spot-checked … not a fidelity check". All entries remain at level `skeleton`.

Ref conventions:
- **BĀU:** Kāṇva recension, adhyāya.brāhmaṇa.kaṇḍikā.
- **ChU:** prapāṭhaka.khaṇḍa.verse.
- **KU:** adhyāya.vallī.verse; the continuous vallī number 1–6 is given in notes.
- **AU:** three-level numbering (3.1.3 = 3.3).
- **MuU:** the common numbering 2.2.8–11. The Śaṅkara e-text numbers these verses 2.2.9–12.
- **KauU:** Cowell / Advaita-Śāradā numbering.
- **MaiU:** Cowell numbering.

## 1. Coverage checklist (A2 and related D/E/F/G items → ids)

### The thirteen texts
All have a source entry with Veda/śākhā, structure, two dating accounts, summary and editions:
- src:isa-upanisad, src:kena-upanisad, src:katha-upanisad, src:prasna-upanisad, src:mundaka-upanisad
- src:mandukya-upanisad, src:taittiriya-upanisad, src:aitareya-upanisad, src:chandogya-upanisad
- src:brhadaranyaka-upanisad, src:svetasvatara-upanisad, src:kausitaki-upanisad, src:maitri-upanisad

Four minor old Upaniṣads outside the Muktikā list were also added: src:baskala-upanisad, src:chagaleya-upanisad, src:arseya-upanisad, src:saunaka-upanisad.

### Four mahāvākyas (cpt:mahavakyas, trm:mahavakya)
- prajñānaṃ brahma — tea:aitareya-upanisad:3.1.3
- ahaṃ brahmāsmi — tea:brhadaranyaka-upanisad:1.4.10
- tat tvam asi — tea:chandogya-upanisad:6.8.7, with the refrain in 6.9.1-4 to 6.16.1-3
- ayam ātmā brahma — tea:mandukya-upanisad:2 and tea:brhadaranyaka-upanisad:2.5.16-19

### Neti neti
- tea:brhadaranyaka-upanisad:2.3.6, 3.9.26, 4.2.4, 4.4.22, 4.5.13-15
- cpt:neti-neti, prc:neti-neti, trm:neti-neti

### Five sheaths
- tea:taittiriya-upanisad:2.1.1, 2.2-5, 3.2.1-3.6.1
- cpt:five-sheaths, trm:kosa, trm:annamaya … trm:anandamaya
- pth:bhrguvalli-five-realizations

### Three states and the fourth
- tea:mandukya-upanisad:1–12
- tea:brhadaranyaka-upanisad:4.3.9-14 and 4.3.19-21
- tea:chandogya-upanisad:8.9–8.12
- tea:maitri-upanisad:7.11
- cpt:four-states-and-turya, cpt:turiya, cpt:deep-sleep, cpt:self-luminosity

### Kaṭha
- Naciketas and Yama: tea:katha-upanisad:1.1.1-4 … 1.1.21-29
- The three boons: 1.1.10-11, 1.1.12-19, 1.1.20
- Śreyas and preyas: 1.2.1-2 (cpt:sreyas-preyas)
- The chariot: 1.3.3-4 and 1.3.5-9 (cpt:chariot-image)
- Ladder of principles: 1.3.10-11 (cpt:hierarchy-of-principles-katha)
- Senses turned outward: 2.1.1
- Yoga as firm holding of the senses: 2.3.10-11 (prc:adhyatma-yoga)
- Inward withdrawal: pth:katha-inward-withdrawal

### Muṇḍaka
- Two birds: tea:mundaka-upanisad:3.1.1-2 and tea:svetasvatara-upanisad:4.6-7 (cpt:two-birds)
- Higher and lower knowledge: tea:mundaka-upanisad:1.1.4-5 (cpt:para-apara-jnana)
- Bow and arrow: 2.2.3-4

### Dialogues
- Yājñavalkya–Maitreyī: BĀU 2.4.1-3, 2.4.5, 2.4.12, 2.4.13-14, 4.5.1, 4.5.6, 4.5.13-15
- Yājñavalkya–Janaka: BĀU 4.1.2-7, 4.2.4, 4.3.2-6 … 4.3.35-38, 4.4.1-2 … 4.4.25; "as one acts so one becomes" is 4.4.5
- Janaka's court: BĀU 3.1–3.9, including Gārgī (3.6.1, 3.8.2-8, 3.8.9, 3.8.10, 3.8.11-12) and Uddālaka and the inner controller (3.7.1-2, 3.7.3-23); dsp:janaka-court-brahmodya
- Uddālaka–Śvetaketu: ChU 6.1–6.16 (clay 6.1.4-6, honey 6.9, rivers 6.10, banyan 6.12, salt 6.13); prc:sad-vidya
- Prajāpati–Indra–Virocana: ChU 8.7.1-3 … 8.12.3-6; pth:indra-prajapati-four-instructions; dsp:virocana-body-as-self
- Satyakāma Jābāla: ChU 4.4.1-5 and 4.5.1-4.9.3
- Nārada–Sanatkumāra and bhūman: ChU 7.1–7.26; pth:bhuma-vidya-ladder; cpt:bhuman
- Dahara-vidyā: ChU 8.1–8.2 (prc:dahara-vidya)
- Śāṇḍilya-vidyā: ChU 3.14.1-4 (prc:sandilya-vidya)
- Raikva: ChU 4.1.1-4.2.5 and 4.3.1-8 (prc:samvarga-vidya)
- Aśvapati Kaikeya: ChU 5.11–5.18; dsp:vaisvanara-six-views
- Ajātaśatru–Gārgya: BĀU 2.1 and KauU 4; dsp:gargya-ajatasatru-debate
- Ghora Āṅgirasa–Kṛṣṇa Devakīputra: ChU 3.17.6
- Indra–Pratardana: KauU 3.1, 3.2, 3.3-8, 3.9
- Kena yakṣa and Umā Haimavatī: Kena 3.1-12 and 4.1-3

### Other named teachings
- Contest of the prāṇas: BĀU 6.1.1-14, ChU 5.1.1-15, PrU 2.1-4, KauU 2.14, BĀU 1.3.1-7 and 1.5.21-23; cpt:contest-of-the-pranas
- Five fires and the two paths: BĀU 6.2, ChU 5.3–5.10, PrU 1.9-10, KauU 1.2-1.3; cpt:pancagni-vidya, cpt:devayana-pitryana
- Maitrī: sixfold yoga 6.18, plus 6.19–6.24 including the two brahmans at 6.22; prc:sadanga-yoga-maitri, referencing pth:maitri-six-limbs
- Śvetāśvatara: yoga chapter ŚU 2.1–2.17 (prc:svetasvatara-yoga); Rudra-Śiva ŚU 3–4 (cpt:rudra-siva); devotion ŚU 6.23
- Īśa 1 and 9-11 (also 12-14 and 15-18)
- Taittirīya: TU 1.11.1-4, 2.4.1, 2.7.1, 2.8.1-5
- Oṃ: PrU 5.1-7
- Udgītha: ChU 1.1.1-3
- BĀU 1.3.28 (asato mā), 5.2.1-3 (da da da), and creation from the self (1.4.1-3, 1.4.7-17)

### Teachers
All requested teachers are present; historicity is marked on each. Ids of note:
- tch:ajatasatru-kasi (disambiguated from the Magadhan king)
- tch:saunaka-mahasala
- tch:krsna-devakiputra (kept separate from tch:krsna)
- tch:svetasvatara (historicity unknown)

Also added:
- tch:kausitaki, tch:paingya
- the six Praśna questioners
- the four teachers in BĀU 4.1 (Jitvan Śailini, Udaṅka Śaulbāyana, Barku Vārṣṇa, Gardabhīvipīta Bhāradvāja)
- the five householders of ChU 5.11
- Mahidāsa Aitareya, Vāmadeva, Triśaṅku, Māhācamasya, and others

### Concepts
cpt:atman, cpt:brahman, cpt:atman-brahman-identity, cpt:prana, cpt:five-pranas, cpt:four-states-and-turya, cpt:five-sheaths, cpt:karma, cpt:rebirth, cpt:devayana-pitryana, cpt:moksa, cpt:jivanmukti, cpt:vidya-avidya, cpt:antaryamin, cpt:bhuman, cpt:ananda, cpt:ananda-mimamsa, plus about 55 more.

Where another unit already has the id, I contributed this lineage's definition instead of creating a new one (e.g., cpt:saksin, cpt:isvara, cpt:grace).

### Ultimate view
ult:upanisadic. It records the texts' statements and points to the disputes where later schools diverge (dsp:tat-tvam-asi, dsp:souls-one-or-distinct, dsp:world-real-or-appearance, dsp:saguna-nirguna, dsp:being-or-non-being-first) without resolving them.

### Corrections to the task's MUST COVER list
1. "prāṇo brahma kaṃ brahma khaṃ brahma" is ChU 4.10.4, not 4.10.5.
2. KauU 1 gives the moon's questioning and the path to the brahma-world, not the five-fires doctrine itself.
3. TU 2 speaks of selves "made of" (-maya) food, breath and so on. The word kośa does not occur in TU 2 (checked). "Five sheaths" is later Vedānta usage.
4. In BĀU 3.2.11 and 4.5.3 the words "neti neti" are an ordinary "no, no". The apophatic formula occurs only at the five places listed above.
5. Muṇḍaka 2.2 numbering differs by one between editions.
6. KauU section numbering varies between editions:
   - Pratardana's inner agnihotra is 2.5 (2.4 in the raw_etexts copy).
   - The father–son transfer is 2.15 (2.10 in the raw_etexts copy).
   - "He makes him do good action" is 3.9 in the Advaita-Śāradā text (3.8 elsewhere).
7. The Kena is Jaiminīya Upaniṣad Brāhmaṇa 4.18–21 (Oertel's numbering), which is anuvāka 10 of book 4 in the e-text.
8. The MaiU verses "mana eva manuṣyāṇām …" are 6.34 in the common numbering. The e-text also places them in chapter 4.
9. The other listed refs are correct as given.

## 2. Least sure (check these first for hallucination)
- **Kauṣītaki brahma-world landmark names** (1.3–1.5). Readings vary: Vijarā/Virajā, Ilya/Tilya, Sālajya/Sāyujya.
- **Tables and mappings from memory:**
  - the BĀU 4.3.33 bliss levels
  - the ChU 3.13 pairings of breath, sense and deity
  - the names of the four quarters in ChU 4.5–9
  - the MaiU 3.5 lists of tamas/rajas marks (low)
  - MaiU 6.1-2 (low)
  - MaiU 6.29 secrecy wording and section number (low)
- **Maitrī numbering** generally. Only 5.2, 6.18–6.24, 6.34 and 7.8–7.11 were checked locally.
- **Teacher identities:**
  - tch:vajasravasa as the Uddālaka line
  - Uṣasti (ChU) = Uṣasta (BĀU)
  - tch:ayasya-angirasa (low)
  - tch:kapila, where the reading of ŚU 5.2 is disputed (low)
- **Minor old Upaniṣads** (src:baskala-upanisad, src:chagaleya-upanisad, src:saunaka-upanisad; low): their contents, and the attribution of the edition to Belvalkar (1925).
- **Other single claims:**
  - that the Muktikā places the Maitrī under the Sāmaveda
  - TB 3.11.8 as the older Naciketas story
  - ŚU 2.1-5 as VS 11.1-5
  - Madhva's school treating the Āgama-prakaraṇa kārikās as śruti
  - TU 1.10 (obscure words)
  - Kena 4.6 (tadvana)
  - MuU 3.2.10 (śirovrata)
- **Scholarly dates.** All are rough estimates at low confidence.
- **brw:mandukya-madhyamaka-prapancopasama** (low). The shared phrase itself is secure; any direction of borrowing is not asserted.

## 3. Gaps (belong here but not created responsibly)
- Individual names in the vaṃśa lists (BĀU 2.6, 4.6, 6.5). Only the endpoints and a few named teachers are recorded.
- Detailed coverage of:
  - the sāman meditations (ChU 1.3–1.7, 2.1–2.22)
  - BĀU 1.5 (seven foods), 1.6 and 5.4–5.14
  - KauU 2.3–2.10 (rites, summarized only)
  - MaiU 2.3–4.6 and 6.1–6.17 and 6.25–6.38
- The contents of the Bāṣkala, Chāgaleya and Śaunaka Upaniṣads. The Ārṣeya is covered only by its opening.
- The lost Paiṅgi Upaniṣad cited by Śaṅkara.
- The Mahānārāyaṇa (TĀ 10); the entry exists in U02.
- Commentators' readings of individual verses (Śaṅkara, Rāmānuja, Madhva). These belong to U13–U16; only pointers are given in notes.
- Śākhā affiliation of the Śvetāśvatara and Māṇḍūkya (uncertain).
- dsp ids referenced but owned by U50: dsp:works-knowledge-grace, dsp:souls-one-or-distinct, dsp:status-of-veda, dsp:women-caste-liberation, dsp:is-there-a-self, dsp:causation, dsp:isvara, dsp:saguna-nirguna, dsp:world-real-or-appearance.
- pth:maitri-six-limbs and pth:yoga-sutra-eight-limbs (owned by U51).

## 4. Out of reach
- The oral svara (accent) recitation traditions of each śākhā.
- Manuscript variants of the Maitrāyaṇīya and Kauṣītaki. Critical editions (Cowell, van Buitenen, Frenz) are not available locally.
- Belvalkar's 1925 edition of the four minor texts.
- **Restricted:** BĀU 6.4 (procreation rites) is recorded as a summary only (tea:brhadaranyaka-upanisad:6.4.1-28, prc:garbhadhana with restricted: true). The palate practices of MaiU 6.20–21 are given only in the text's own words, and khecarī is not described.
