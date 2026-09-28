# U24-kali-kaula — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Scope.** Coverage map A8 (Kālī lineages and the ten Mahāvidyās; Kaula; sacred sites and rites; Śākta poets) and I2 (Kubjikā; Assamese and Bengali Śākta tantra).
**Lineages owned.** lin:kalikula, lin:kaula, lin:kubjika, lin:bengal-assam-sakta, each with its ult view.
**Validator.** 0 errors. The only warning is "REPORT.md missing".
**Generators.** `_gen/part1…part11`.

**Method.** Most verse locators were checked against local e-texts in sources_raw, using a parser that counts chapters and verses:
- Kulārṇava: Muktabodha M00031, 17 ullāsas confirmed.
- Kubjikāmata: GRETIL, 25 paṭalas.
- Toḍala: GRETIL, 10 paṭalas.
- Mahānirvāṇa: M00049, 14 ullāsas.
- Nirvāṇa Tantra: M00127, 14 paṭalas.
- Kālīvilāsa: eBhāratī, 35 paṭalas.
- Kaulāvalīnirṇaya: eBhāratī.
- Kāmākhyā Tantra: M00132, 9 paṭalas.
- Rudrayāmala: M00074.
- Tārā Tantra: M00094.
- Kālikā Purāṇa: M00405.
- Bṛhaddharma Purāṇa: eBhāratī.
- Kṛṣṇānanda's Bṛhattantrasāra: M00013.
- Karpūrādistotra.
- Śrītattvacintāmaṇi, prakāśa 6 (= Ṣaṭcakranirūpaṇa).
- Brahmasaṃhitā, with Jīva's commentary.
- Kaulajñānanirṇaya: M00027.

These teachings carry a note in `notes` naming the e-text. They are still skeleton entries: no fidelity check has been done.

## 1. Checklist (coverage item → ids)

### Ten Mahāvidyās
- **The group:** cpt:ten-mahavidyas.
- **Each one:** cpt:mahavidya-{kali, tara, sodasi, bhuvanesvari, bhairavi, chinnamasta, dhumavati, bagalamukhi, matangi, kamala}.
- **Terms:** trm:mahavidya, trm:kali, trm:tara, trm:sodasi, trm:tripurasundari, trm:bhuvanesvari, trm:bhairavi, trm:chinnamasta, trm:dhumavati, trm:bagalamukhi, trm:matangi, trm:kamala.
- **Consorts:** cpt:mahavidya-consorts (Toḍala 1.3-19).
- **Avatāras:** cpt:mahavidya-avatara-correspondence (Toḍala 10.9-12).
- **Texts that group them:**
  - Muṇḍamālā, as quoted in the Tantrasāra: tea:tantrasara-krsnananda:1.siddhadi-sodhana
  - Bṛhaddharma madhya 6.125-134
  - Mahābhāgavata 8
- **Satī–Śiva origin story:** cpt:mahavidya-origin-story, tea:brhaddharma-purana:madhya.6.78-87 / .98-124 / .125-134, tea:mahabhagavata-purana:8.

### Kālī tantras
src:kali-tantra, src:kalivilasa-tantra, src:mahakala-samhita, src:nirvana-tantra, src:mahanirvana-tantra (date recorded as contested attribution), src:todala-tantra, src:kamakhya-tantra, src:yoni-tantra (restricted), src:kaulavalinirnaya, src:kalikulasarvasva, src:syamarahasya, src:niruttara-tantra, src:kulacudamani-tantra, src:mundamala-tantra, src:karpuradi-stotra, src:saktisangama-tantra.

**Jayadrathayāmala:** src:jayadrathayamala — Kālīkula contribution only; U08 and U19 own it.

**Tārā tantras:** src:tara-tantra, src:brhannila-tantra, src:tararahasya, src:tarabhaktisudharnava.

**Vasiṣṭha–Cīnācāra:** tea:rudrayamala:17.105-124, tea:rudrayamala:17.125-140, tea:tara-tantra:1.2-4, cpt:cinacara, trm:cinacara, trm:mahacina.

### Kaula
- **Kaulajñānanirṇaya:** referenced (U21 owns it), plus tea:kaulajnananirnaya:6.8-14, 9.8-15, 22.10-12.
- **Kulārṇava:** src:kularnava-tantra, 17 ullāsas, 44 teachings.
  - Guru: tea:kularnava-tantra:12.49, 13.79, 13.88-94, 13.104-108, 14.*, 17.7-9, and cpt:guru-in-kaula.
  - Kula: cpt:kula-akula, tea:kularnava-tantra:17.27.
  - Inner meaning: cpt:inner-meaning-of-pancatattva.
- **Kubjikāmata and the Paścimāmnāya:** src:kubjikamata-tantra (9 teachings), src:satsahasra-samhita, src:manthanabhairava-tantra, cpt:pascimamnaya.
- **Āmnāyas:** cpt:amnayas, trm:amnaya, and the five direction terms. Only the Kulārṇava's fivefold list is verse-checked; the Kashmir–Nepal assignment of goddesses to directions is moderate confidence.
- **Kaulācāra:** trm:kulacara, cpt:seven-acaras, pth:kaula-seven-acaras.
- **Five Ms (summary only):**
  - Core entries: cpt:pancatattva, prc:pancatattva-puja (restricted).
  - Substitutes: cpt:anukalpa, prc:anukalpa-substitution.
  - Inner readings: cpt:inner-meaning-of-pancatattva.
  - The texts' warnings, in the warnings field: Kulārṇava 2.117, 2.122, 5.96-105, 9.130.

### Sacred sites and rites
- **Pīṭhas:** cpt:sakta-pithas and cpt:four-adi-pithas, from Kālikā Purāṇa 18 and KMT 11.6-7. src:pithanirnaya is recorded as a source (low confidence). The full 51/52 list was **not** reproduced; see Gaps.
- **Satī body-parts myth:** cpt:sati-body-myth, tea:kalika-purana:18.36-47 and 18.48-50.
- **Kāmākhyā:** cpt:kamakhya, trm:kamakhya.
- **Ambubachi:** cpt:ambubachi, prc:ambubachi-observance, trm:ambuvaci.
- **Sixty-four yoginīs and their temples:** cpt:sixty-four-yoginis, trm:catuhsasti-yogini. Covers Hirapur, Ranipur-Jharial, Bheraghat, Mitaoli and Khajuraho.
- **Menstruation rites:** cpt:menstruation-rites (low confidence, restricted).
- **Yoni as sacred:** cpt:yoni-as-sacred.

### Bengal and Assam
- **Kālikā Purāṇa:** src:kalika-purana (contribution), including the offering chapter (tea:kalika-purana:67.* — restricted summary with the text's own restrictions and substitutes).
- **Kṛṣṇānanda's Tantrasāra:** src:tantrasara-krsnananda, tch:krsnananda-agamavagisa, cpt:daksinakali-iconography.
- **Sarvānanda:** tch:sarvananda, src:sarvollasa-tantra.
- **Brahmānanda Giri:** tch:brahmananda-giri, src:saktanandatarangini.
- **Pūrṇānanda:** tch:purnananda, src:sritattvacintamani, src:syamarahasya, tea:sat-cakra-nirupana:50 and 51-53.
- **Rāmprasād:** tch:ramprasad-sen; src:ramprasadi-songs with 5 teachings.
- **Kamalākānta:** tch:kamalakanta; src:kamalakanta-padavali with 2 teachings; src:sadhaka-ranjana.
- **Ramakrishna:** referenced only (U52).
- **Also added:** src:yogini-tantra, src:brhaddharma-purana, src:pranatosini, src:candimangala, src:annadamangala, tch:bamakhepa, tch:bhairavi-brahmani, tch:hariharananda-bharati, tch:sivacandra-vidyarnava.

### Concepts
- **Śakti as consciousness-power:** cpt:sakti-as-consciousness-power.
- **Kuṇḍalinī, Śākta view:** contributed to cpt:kundalini and trm:kundalini; also prc:kundalini-yoga-sakta.
- **Gentle and fierce forms:** cpt:saumya-and-ugra-forms.
- **Three bhāvas:** cpt:three-bhavas, pth:three-bhavas.
- **Kālī as time:** cpt:kali-as-time.
- **Cremation-ground symbolism:** cpt:cremation-ground-symbolism.
- **Death and dying:** cpt:sakta-death-and-dying, tea:mahanirvana-tantra:10.78-80 and 10.81-83.

### Disputes (new)
1. dsp:daksina-vs-vama — partially reconciled under P4.
2. dsp:legitimacy-of-kaula-practice — partially reconciled under P4 and P1.
3. dsp:blood-sacrifice — queued as RQ-U24-blood-sacrifice.
4. dsp:bhavas-in-kali-yuga — queued as RQ-U24-bhavas-in-kali-yuga.
5. dsp:krsna-and-kali — partially reconciled under P3 and P2, with both traditions' objections recorded.
6. dsp:world-illusion-or-mansion-of-mirth — reconciled under P4; low confidence.

**Referenced, owned elsewhere:** dsp:purity-impurity-kaula, dsp:status-of-veda, dsp:women-caste-liberation, dsp:saguna-nirguna, dsp:souls-one-or-distinct, dsp:world-real-or-appearance, dsp:authority-of-sixty-four-tantras.

### Path maps
- pth:kaula-seven-acaras and pth:kaula-seven-ullasas: the Kulārṇava gives rankings, not stage content, so **no bands were assigned**. U51 should decide.
- pth:three-bhavas: only the paśu stage is banded (B1, resting on Rudrayāmala 17.125-140).

### Shared entries contributed
- **Sources:** src:jayadrathayamala, src:kalika-purana, src:agni-purana (Kubjikā chapters 143-144), src:mahabhagavata-purana.
- **Teachings under other units' sources:** src:kaulajnananirnaya (U21), src:sat-cakra-nirupana (U28), src:brahma-samhita:5.44 (U16).
- **Terms (Kaula/Śākta definitions added):** trm:kula, trm:akula, trm:sakti, trm:kundalini, trm:kali, trm:guru, trm:diksa, trm:avadhuta, trm:smasana, trm:bali, trm:mudra, trm:pasu, trm:vira, trm:bhava, trm:samaya, trm:jiva, trm:avidya, trm:linga-sarira, trm:ananda, trm:amnaya, trm:mahamaya, trm:kali-yuga, trm:hamsa, trm:pitha.
- **Concepts and practices:** cpt:kula-akula, cpt:kundalini, cpt:kinds-of-diksa, prc:antaryaga, prc:manasa-puja, prc:guru-bhakti, prc:japa, prc:purascarana, prc:diksa.

### Corrections to the MUST-COVER list
- **Mahāvidyā lists differ.** The Bṛhaddharma lists Sundarī and Ṣoḍaśī separately and omits Kamalā. The Toḍala's avatāra list pairs Mahālakṣmī (not Kamalā) with the Buddha and Durgā with Kalki. The GRETIL text reads Tārā as "nīlarūpā", where the usual reading is Matsya.
- **The Kālikā Purāṇa's body myth.** Brahmā, Viṣṇu and Śani enter the corpse; it is not Viṣṇu's discus. The text names only a handful of seats, not 51.
- **The 'rudhirādhyāya'** is ch. 67 in the Vaṅgavāsī edition; it is often cited as ch. 71.
- **The Dakṣiṇakālī meditation verse** in the Tantrasāra is quoted from the Kālī Tantra. Kṛṣṇānanda's authorship of the form is a Bengali legend.
- **The Vasiṣṭha story** is in Rudrayāmala (Uttaratantra) 17. The Tārā Tantra opens by naming Buddha and Vasiṣṭha as Kula-Bhairavas and appends the story.
- **Kulārṇava 1.110:** the e-text reads "ca jānanti"; the sense requires "na jānanti". This is noted on the teaching.
- **Mahānirvāṇa:**
  - It forbids a wife burning herself on her husband's pyre (10.79-80).
  - Its date is recorded as contested attribution metadata, not as a doctrinal dispute.
- **Kālīvilāsa:** it denies the vīra and divya dispositions in the Kali age (4.2-3).
- **Kṛṣṇānanda's own reading.** He calls the Muṇḍamālā's "no checks needed" claim praise (arthavāda). This is logged as the tradition's own use of the praise principle (P7).

## 2. Least-sure items (check these first)
- **Sources:**
  - src:mahakala-samhita (sections, editor), src:kalikulasarvasva, src:niruttara-tantra, src:kularatnoddyota, src:srimatottara-tantra, src:cincinimatasarasamuccaya.
  - src:pascimarcana-paddhati and tch:vimalaprabodha (known only from the catalogue).
  - src:pithanirnaya (attribution and date); src:sadhaka-ranjana; src:vidyasundara-ramprasad; src:kalikirtana-ramprasad; src:gandharva-tantra, src:phetkarini-tantra, src:visvasara-tantra, src:bhuvanesvari-rahasya.
- **Structure counts and editors:** Yoni Tantra 8 paṭalas; Bṛhannīla 24 paṭalas; Kaulāvalī 21 ullāsas; the Kālīvilāsa and Kulacūḍāmaṇi editors (hedged in the text).
- **Mahāvidyā iconography.** Descriptions marked "standard dhyāna, recalled" are from memory; only Kālī's is text-checked. This includes the Chinnamastā origin story ascribed to the Prāṇatoṣiṇī.
- **Pīṭha members** in cpt:sakta-pithas other than Kāmākhyā; the yoginī temple list and dates.
- **Teacher dates and legends:** Sarvānanda; Kamalākānta; Śivacandra; Kailāspati Bābā; Gauḍīya Śaṅkara; the Rāmprasād legends; Kṛṣṇānanda's Caitanya link.
- **Songs:** wording and attribution of all Rāmprasād and Kamalākānta songs (refs are first-line slugs). Āju Gosāi's reply.
- **Uncheckable references:** Mahābhāgavata ch. 8 and Bhāgavata 4.25.7-8 (not locally checked); the Nepalese āmnāya-to-goddess assignments; the KJN Siddha names (corrupt e-text).
- **Rituals:** the Ambubachi–menstruation link at Kāmākhyā (living practice, no verse anchor).

## 3. Gaps (belong here, not responsibly created)
- **Pīṭhas:** the full 51/52 list from the Pīṭhanirṇaya and the Śivacarita, with each seat's goddess and Bhairava. The text is not local.
- **Kubjikā lineage:** the teachers of the Paścimāmnāya (the Siddhas and yuganāthas of the transmission), the Manthānabhairava's contents, and the living Newar Kubjikā lineages.
- **Nepal:** the Uttarāmnāya Guhyakālī and Siddhilakṣmī cults. Local Nepalese paddhatis exist but were not read.
- **Texts not excerpted:**
  - Kulārṇava chs. 4, 6, 10, 15-16.
  - Kubjikāmata chs. 3-10, 13-22, 24-25.
  - Rudrayāmala after 17.140 (the vīra and divya stages).
  - The Kālikā Purāṇa's Tripurā worship and Durgā autumn-worship chapters.
  - Śaktisaṅgama (āmnāya and ācāra lists), Yoginī Tantra, Mātṛkābheda, Śyāmārahasya, Śāktānandataraṅgiṇī, Sarvollāsa, Prāṇatoṣiṇī.
- **Named lists:** the 64 yoginīs; the Kālī sahasranāmas and Ādyā-stotra; Kāmakalākālī.
- **Siddhis:** explicit warnings against pursuing siddhis were not found in the Kaula corpus. Only the Kulārṇava's misuse warnings, the Tantrasāra's insistence on checking mantras, and Lakṣmīdhara's critique were located.
- **Regional material:**
  - For U59: Kerala Bhadrakālī (Muḍiyēṭṭu, Koḍuṅṅallūr) and Assamese folk deodhani possession.
  - For U52: the Ramakrishna sources for the "mansion of mirth" reconciliation.

## 4. Out of reach
- Oral Kaula and Kubjikā initiations and lineage lists (secret by the tradition's own rule).
- Details of restricted rites: the five Ms, the latā-sādhana, śava-sādhana and bali. They are deliberately summary-only with the texts' warnings.
- Unedited Nepalese manuscripts.
- Oral variants of the Bengali Śākta songs.
