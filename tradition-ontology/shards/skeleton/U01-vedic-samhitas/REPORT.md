# U01-vedic-samhitas — REPORT (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Validator: 0 errors. Counts: sources 70 · lineages 18 (lin:vedic-srauta + 16 śākhās + lin:arya-samaj) · teachers 91 · teachings 290 (RV 172; VS/TS/SV/AVŚ and tradition-accounts 118; 65 with `original`) · terms 232 · concepts 68 · practices 43 · obstacles 17 · disputes 13 · borrowings 17 · phenomenology 18 · paths 1 · ultimate 1 · interpretation_log 40.
Method: skeleton from memory. Seer, deity and metre attributions, verse numbers and every `original` were spot-checked against the local corpora: sources_raw/DharmicData (RV, VS, AVŚ with Anukramaṇī headers), raw_etexts (TS, Nāradīya and Pāṇinīya Śikṣā, Bhāgavata and Viṣṇu Purāṇa) and the DCS Nirukta (chapters 1–2 only). Entries whose notes say "checked" were read in those texts. All entries remain at level `skeleton`. Generators: _gen/part1…part10 (+ common.py).

## 1. Coverage checklist (A1 Saṃhitās + D/E/F/G items touching lin:vedic-srauta)
- **Ṛgveda (10 maṇḍalas, family books, Vālakhilya, Śākala, Padapāṭha):**
  - Sources: src:rgveda (structure note), src:valakhilya, src:pavamani (book 9), src:rgveda-padapatha, src:rgveda-khilani, src:sri-sukta, src:rgveda-pratisakhya, src:sarvanukramani, src:brhaddevata.
  - Lineages: lin:sakha-sakala/-baskala/-asvalayana/-sankhayana/-mandukayana.
- **Commentators (sources/teachers):**
  - Sāyaṇa: src:rgveda-bhasya-sayana (+ its TS and AV commentaries), tch:sayana.
  - Skandasvāmin: src:rgveda-bhasya-skandasvamin, tch:skandasvamin.
  - Veṅkaṭamādhava: src:rgarthadipika, tch:venkatamadhava.
  - Bhaṭṭa Bhāskara: src:jnanayajna, tch:bhatta-bhaskara.
  - Uvaṭa: src:mantrabhasya-uvata. Mahīdhara: src:vedadipa.
  - Madhva: src:rgbhasya-madhva.
  - Recent: Dayānanda (src:rgvedadibhasyabhumika) and Aurobindo (src:secret-of-the-veda).
- **Philosophical hymns (sources + teachings):**
  - 1.164: src:asya-vamasya-sukta; tea:rgveda:1.164.{1,2,4,6,11,20,21-22,30,31,32,37,38,39,41-42,45,46,48,50}.
  - 10.129: src:nasadiya-sukta; tea …10.129.1–7.
  - 10.90: src:purusa-sukta; tea …10.90.1, 2, 3-4, 5, 6-10, 11-12, 13-14, 16; VS 31.1, 31.18, 31.19.
  - 10.121: src:hiranyagarbha-sukta; tea …10.121.1, 2, 7-8, 10.
  - 10.125: src:vak-sukta; tea …10.125.1, 3–8.
  - 10.136: src:kesi-sukta; tea …10.136.1, 2, 3, 4-6, 7.
  - 10.71: src:jnana-sukta. 10.81–82: src:visvakarma-sukta. 10.190: src:aghamarsana-sukta.
  - 10.14–18: src:rgveda-funeral-hymns (13 teachings).
  - 3.62.10: src:gayatri-mantra. 7.59.12: src:mahamrtyunjaya-mantra.
  - 1.1: tea:rgveda:1.1.1, 1.1.2, 1.1.8-9. 1.32: tea:rgveda:1.32.1, 1.32.
  - Extras: 1.22.20, 1.50.10, 1.89, 1.115.1, 1.154, 2.12.5, 4.26.1, 4.27.1, 4.40.5, 4.58.1/3, 5.81.1, 5.85, 6.9.5–6, 6.47.18, 8.48.3, 8.58.2, 8.100, 9.113, 10.72, 10.82.7, 10.85.1/3, 10.88.15, 10.117, 10.119, 10.137, 10.151, 10.154, 10.168.4, 10.177.1, 10.191.
- **Deity hymns:**
  - Rudra (1.43.4, 1.114.8, 2.33.2/4/7/10, 7.46, AVŚ 11.2, TS 4.5) → cpt:rudra-vedic.
  - Soma (book 9) → cpt:soma-vedic, cpt:inner-soma.
  - Agni → cpt:agni-vedic.
  - Varuṇa (1.24.15, 1.25.7-11, 2.28.5, 5.85, 7.86–89, AVŚ 4.16) → cpt:varuna-mitra-guardians, cpt:sin-and-forgiveness-varuna.
- **Core concepts:**
  - ṛta, satya, tapas: cpt:rta-cosmic-order, cpt:satya-truth, cpt:tapas-vedic.
  - yajña, dharman: cpt:yajna-cosmic-sacrifice, cpt:dharman-vedic.
  - brahman (early sense): cpt:brahman-early-sense. vāc: cpt:vac-speech, cpt:four-quarters-of-speech.
  - prāṇa: cpt:prana-vedic, cpt:vedic-breaths. soma: as above. Internalization of ritual: cpt:internalization-of-ritual.
  - Gods as names of the One: cpt:gods-as-names-of-the-one, cpt:the-one-tad-ekam, ult:vedic-srauta. The caveat records Mīmāṃsā, Yāska's three deities and the Vaiṣṇava reading.
- **Sāmaveda:**
  - Sources: src:samaveda, src:jaiminiya-samhita, src:gramageya-gana, src:aranyageya-gana, src:uha-gana, src:uhya-gana, src:naradiya-siksa, src:puspa-sutra.
  - Lineages: lin:sakha-kauthuma/-ranayaniya/-jaiminiya.
  - Terms: ārcika, gāna types, stobha, the sāman parts; cpt:sama-svaras-and-musical-notes; cpt:parts-of-a-saman; prc:sama-gana.
- **Yajurveda:**
  - Black: src:taittiriya-samhita, src:maitrayani-samhita, src:kathaka-samhita, src:kapisthala-katha-samhita.
  - White: src:vajasaneyi-samhita (Mādhyandina), src:vajasaneyi-samhita-kanva. See cpt:black-and-white-yajurveda (Viṣṇu Purāṇa 3.5 account, checked).
  - Śatarudrīya / Śrī Rudram: src:satarudriya; tea TS 4.5.1, 4.5.2-9, 4.5.8, 4.5.11; VS 16.25, 16.54.
  - Camakam: src:camakam; TS 4.7.1-11, VS 18.1.
  - Also src:sivasankalpa-sukta (VS 34.1–6) and VS 1.1, 1.5, 3.60, 3.62, 11.1-5, 22.22, 23.9-12, 26.2, 32.1/3/8, 36.1/3/17/18/24, 40.15-17.
- **Atharvaveda:**
  - Sources and lineages: src:atharvaveda-saunaka, src:atharvaveda-paippalada; lin:sakha-saunaka/-paippalada.
  - Healing: tea 1.22, 1.23-24, 2.32, 3.7, 5.22; prc:bhaisajya-rites; cpt:vedic-healing-bhaisajya.
  - Vrātya: src:vratya-kanda (15.1.1-8, 15.3, 15.10-13, 15.15-17).
  - Skambha: src:skambha-sukta (10.7.1/17/32-34, 10.8.1/27-28/29/43/44).
  - Prāṇa: src:prana-sukta (11.4.1/10-11/21/22/25/26).
  - Other hymns: Pṛthivī src:prthivi-sukta; Brahmacārin src:brahmacari-sukta; Kāla src:kala-sukta; Ucchiṣṭa src:ucchista-sukta.
  - Additions: src:kena-sukta (AVŚ 10.2, the body as the city of Brahman), 3.30, 6.46, 6.108, 8.1, 8.10, 9.6, 11.8.32, 13.4, 14.1.17, 18.2–3, 19.9, 19.41, 19.52.
- **Named seers (with historicity marked):**
  - Family-book seers: Gṛtsamada, Viśvāmitra, Vāmadeva, Atri, Bharadvāja, Vasiṣṭha, Kaṇva.
  - Book 1 seers: Dīrghatamas, Agastya, Madhucchandas, Medhātithi, Śunaḥśepa, Hiraṇyastūpa, Praskaṇva, Gotama, Kutsa, Kakṣīvant, Parāśara.
  - Other seers: Nema, Kaśyapa, Jamadagni, Atharvan, Aṅgiras, Bhṛgu, Vena, Śyāvāśva, Garga, Medhya, Pragātha, Pavitra, Nārada, Bhārgava Vaidarbhi, and the book-10 seers.
  - ṛṣikās (21 teacher entries): Lopāmudrā, Ghoṣā, Apālā, Viśvavārā, Vāc Āmbhṛṇī, Śraddhā, Sūryā, Yamī, Indrāṇī, Śacī, Romaśā, Śaśvatī, Sārparājñī, Rātri Bhāradvājī, Dakṣiṇā, Godhā, Aditi, Agastya's sister, Urvaśī, Juhū. Also cpt:brahmavadinis.
  - Transmitters: Vyāsa, Paila, Vaiśampāyana, Jaimini, Sumantu, Yājñavalkya, Tittiri, Kaṭha, Śākalya, Śaunaka, Pippalāda, Kātyāyana, Yāska, Kautsa.
- **Death, afterlife, cosmology:**
  - Death and afterlife: cpt:vedic-afterlife, cpt:two-paths-fathers-gods, cpt:vedic-funeral-sequence, cpt:mrtyu-death-and-its-bonds, cpt:amrtatva-vedic-immortality, cpt:istapurta-merit, cpt:full-life-hundred-autumns.
  - Cosmology: cpt:vedic-cosmogonies, cpt:three-worlds, cpt:thirty-three-gods, cpt:vedic-cosmic-time, cpt:kala-time-as-first-cause.
- **Section D, remaining items:**
  - Self: cpt:vedic-person-components, cpt:two-birds.
  - Mind: cpt:manas-vedic, cpt:dhi-visionary-thought, cpt:kama-first-seed-of-mind.
  - States: cpt:vedic-states-waking-sleep, cpt:heart-as-seat-of-vision.
  - Body: cpt:body-as-city-of-gods.
  - Obstacles: 17 obs ids.
  - Ethics: cpt:dana-generosity, cpt:sammanasya-concord, cpt:sraddha-faith, cpt:vrata-divine-ordinance, cpt:varna-in-purusa-sukta.
  - Signs and powers: 18 phn ids, cpt:muni-and-keshin.
  - Transmission: cpt:rsi-as-seer, cpt:vedic-transmission-sakha, cpt:four-vedas-and-trayi, cpt:vedic-recitation-modes, cpt:vedic-accent-system.
- **E (practices):**
  - Mantra: prc:gayatri-japa, prc:mahamrtyunjaya-japa, prc:rudra-japa, prc:santi-patha, prc:aghamarsana.
  - Recitation (pāṭhas): prc:vedapatha, pada-, krama-, jaṭā-, ghana-pātha, prc:vikrti-pathas.
  - Śrauta rites (summary only): prc:srauta-yajna and the individual rites.
  - Funeral: prc:pitrmedha.
- **F (path maps):** pth:srauta-sequence (ritual career). Bands B0–B2; the final stage (svarga) is deliberately unbanded.
- **G / internal disputes:** dsp:rv-1-164-32-rebirth-reading, sat-or-asat-in-the-beginning, nature-of-vedic-deities, how-many-gods, atharvaveda-status, seen-or-made-hymns, visvamitra-vasistha-rivalry (queued), rv-10-18-7-widow-reading (queued), vratya-status (queued), varna-origin-purusa-sukta (queued), are-mantras-meaningful, how-to-read-the-samhitas, who-may-learn-the-veda (queued). Queue refs RQ-U01-01…05. This unit references the registry dispute dsp:status-of-veda but does not create it.
- **Borrowings:**
  - 17 brw entries: RV and AV verses into the Upaniṣads (explicit citations), the Rudram into Śaiva, Vāk into Śākta, the Puruṣa Sūkta into Pāñcarātra, speech verses into grammar, Sāman into music, the Atharvaveda into Āyurveda, and the Gāyatrī into Dharmaśāstra.
  - Two scholarly hypotheses, low confidence: Keśin/muni ↔ śramaṇa; Vrātya ↔ Pāśupata.
  - Indo-Iranian parallels are recorded only as labeled scholarly-metadata notes on 13 terms (ṛta, yajña, soma, mitra, asura, deva, hotṛ, atharvan, yama, vṛtra, druh, mantra, indra).

## Corrections to the task's MUST-COVER list and to my own recall (found while checking)
- Book 8 is mostly the Kāṇva family's (with Āṅgirasas), not a single family book like 2–7.
- 3.55 ("mahad devānām asuratvam ekam") is ascribed to Prajāpati Vaiśvāmitra/Vācya, not to Viśvāmitra.
- 6.47.18 ("Indra goes in many forms by his māyās") is by Garga Bhāradvāja, not Bharadvāja.
- The Camaka also stands at VS 18.1–27, not only TS 4.7.
- The Śatarudrīya's "namaḥ śivāya ca śivatarāya ca" is TS 4.5.8 = VS 16.41.
- AVŚ 10.8 (the jyeṣṭha-brahman hymn) is ascribed to Kutsa; 10.7 to Atharvan. AVŚ 11.4 is ascribed to Bhārgava Vaidarbhi.
- The Atharvaveda's marriage form of the Tryambaka verse (AVŚ 14.1.17) addresses Aryaman, not Tryambaka. VS 3.60 has two forms, "māmṛtāt" and "pativedanam … ito mukṣīya māmutaḥ".
- The Anukramaṇī gives the deity of 10.125 as ātman, and of 10.129/10.190 as bhāvavṛtta.
- The seven Keśin verses are ascribed one each to the seven Vātaraśana munis.
- AV 13.4.16–18 ("not second, not third…") is Whitney's numbering; in the local edition it is 13.5.16–18.

## 2. Least sure — possible hallucinations to check first
1. tea:nirukta:13.9 (the list of readings of the four quarters of speech; low).
2. tea:brhaddevata:2.82-84 (brahmavādinī list and verse numbers; low; text not available locally).
3. tea:aitareya-brahmana:2.19 (the Kavaṣa episode; low).
4. tea:rgveda-bhasya-sayana:upodghata (Sāyaṇa's definition of the Veda; low).
5. tea:nirukta:2.11, 7.5, 7.6-7: section numbers from memory. 7.4 is confirmed only via a secondary citation.
6. Minor śākhās (Bāṣkala, Māṇḍūkāyana, Rāṇāyanīya, Śāṅkhāyana regions); src:caranavyuha, src:vikrtivalli + tch:vyadi, src:puspa-sutra authorship, src:atharvaveda-parisista, src:rgvidhana.
7. Structural counts: TS 7/44/651; MS 4/54; KS 40 sthānakas; VS c. 1,975 kaṇḍikās; SV c. 1,875; AVŚ c. 730/6,000. Also that the Padapāṭha omits 10.121.10 and the Vālakhilya.
8. Commentator dates (Skandasvāmin, Veṅkaṭamādhava, Bhaṭṭa Bhāskara). Also Madhva's "several levels of meaning" doctrine, and Harisvāmin as Skandasvāmin's pupil.
9. Traditional legends: Dīrghatamas born blind; Ghoṣā's illness; Lopāmudrā as seer of a Śrīvidyā mantra; Pāṇini 4.3.102 deriving "Taittirīya" from Tittiri.
10. Dispute-side loci:
    - Śabara on devatā: chapter-level only.
    - Gopatha claim that the brahmán priest should be an Atharvavedin.
    - Pañcaviṃśa Br. 17.1–4 (vrātyastoma).
    - Which later authorities cited the "agneḥ" variant of RV 10.18.7 (not named on purpose).
    - Sāyaṇa on the Vrātya.
    - Mīmāṃsā Sūtra 1.2.31ff.
    - Suśruta Sū. 1.6 and Caraka Sū. 30.21.
    - Nāṭyaśāstra 1.17.
    - Mahābhāṣya citing 1.164.45.
11. Hymn-level paraphrases from memory: 1.32, 8.91 (Apālā details), 10.39–40 (Ghoṣā), AVŚ 2.32, 3.7, 5.22 content, 15.11–13, 15.16–17, 8.10 later paryāyas.
12. TS details: the anuvāka number of 1.8.6, TS 4.5.2-9 and 4.5.11 (passage summaries), and the placement of 1.114.8 in the Rudram.
13. The Rudra-japa multiples (11/121/1,331/14,641).

## 3. Gaps (belong here but not created responsibly)
- No verse-level teachings yet from the Paippalāda AV, the Maitrāyaṇī, Kāṭhaka or Kapiṣṭhala Saṃhitās, or the Jaiminīya SV. The TS brāhmaṇa-prose portions (e.g. kāṇḍas 5–7, dīkṣā) were not mined.
- The Sāmaveda has only SV 1 at verse level; the gāna texts' contents and the Mahānāmnī verses are missing. The Khila contents (Śrī Sūkta verses, Medhā Sūkta) are not entered as teachings.
- Full Purāṇic pupil-lines of the śākhās (Bhāgavata 12.6–7; Viṣṇu Purāṇa 3.4–6) and the Caraṇavyūha counts are not entered.
- Commentators known by name only: Udgītha, Nārāyaṇa (co-authors with Skandasvāmin), Ātmānanda (Asyavāmīya), Mudgala, Bharatasvāmin and Mādhava (Sāmaveda), Harisvāmin, Jayatīrtha and Rāghavendra on Madhva's Ṛgbhāṣya, Kapāli Śāstrī (recent).
- Many minor Ṛgveda seers were not given teacher entries (e.g. Paruchepa, Nodhas, Savya, Kumāra Ātreya, Śrutavid, Śiśu, Mūrdhanvān, Sadhri, Anila, Pataṅga, Yajña Prājāpatya, Parvata, Kūrma Gārtsamada, the Gaupāyanas, the Yāmāyanas).
- Hymns to Uṣas, the Aśvins, the Maruts, Pūṣan and others have terms only. Details of the śrauta rites belong to U02 (kalpa).
- The Mahābhāṣya grammarians' reading of RV 4.58.3 appears only as borrowing evidence; src:mahabhasya is not in the registry.
- Matter and qualities (D): the Saṃhitās have no elements or guṇa doctrine. Only the AVŚ 10.8.43 "three strands" is recorded, and its link to Sāṃkhya is marked contested.
- **External ids this unit references and expects others to create:** cpt:three-gunas, cpt:levels-of-speech, prc:antyesti, src:pancavimsa-brahmana, trm:dharma, trm:moksa, trm:avyakta, trm:sabda-brahman; Upaniṣad teachings BĀU 1.4.10, 2.5.19, 6.2.2; MuU 3.1.1; ŚU 2.1-5, 2.4, 3.8, 4.3, 4.6.
- **New lineage outside the registry:** lin:arya-samaj (recent). I created it because Dayānanda's reading of the Saṃhitās is a major one. Please flag it for inclusion or exclusion.

## 4. Out of reach
- Oral recitation lore: śākhā-specific pronunciation and hand-accent systems, living gāna performance, the secrecy of the forest (āraṇyageya) songs and the pravargya, Nambūtiri śrauta practice, and the Odisha Paippalāda reciters. None of this is captured beyond what the texts say.
- Vedic accents are not represented: `original` is unaccented IAST.
- The Bṛhaddevatā, Sarvānukramaṇī, Nirukta chapters 3–14, and the Kāṭhaka and Maitrāyaṇī texts with accents were not available locally, and GRETIL/TITUS are blocked. Check these in Phase C.
