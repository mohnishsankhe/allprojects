# U11-nyaya-vaisesika — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

Owned lineages: lin:nyaya, lin:vaisesika, lin:navya-nyaya (parent lin:nyaya). The generators are _gen/part1…part9. To re-run, delete the *.jsonl files and run all parts in order, because save() appends interpretation-log lines instead of replacing them. _gen/dcs_text.py holds the verbatim DCS sūtra texts (CC BY 4.0).

## Checking method (no web)
- Wording and numbering were checked against local e-texts in sources_raw; every entry stays at skeleton level.
- Nyāya Sūtra: the DCS text and raw_etexts nyayasutra.md agree, and teaching ids use their numbering.
  - The Taranatha edition (GRETIL Nyāyabhāṣya) numbers differently from 2.1.20, 2.2.43, 3.1.15, 3.2.34 and 5.1.4 onward.
  - Each affected teaching notes the Taranatha number (mapping table in _gen/common.py).
- Vaiśeṣika Sūtra: the DCS text is Candrānanda's recension, and ids use its numbering. The Upaskāra-only sūtra is tea:vaisesika-sutra:upaskara-1.1.4.
- `original` text is given only for passages confirmed locally. Two exceptions whose wording is certain and partly confirmed: NK 5.1 and the Nyāyavārttika's opening verse.

## Corrections to the MUST-COVER list
1. VS 1.1.2 is correct. But the sūtra that lists the six categories exists only in the Upaskāra recension (1.1.4); Candrānanda's recension lacks it, and its 1.1.4 lists the nine substances.
2. VS 1.1.5 names 17 qualities; Praśastapāda reaches 24 by adding 7 through the word "ca".
3. Absence as a seventh category is explicit in Udayana's Lakṣaṇāvalī and Śivāditya's Saptapadārthī. The Kiraṇāvalī explains why Praśastapāda did not list it. Candramati's Daśapadārthī counts ten categories.
4. Four pramāṇas is the Nyāya count. Vaiśeṣika accepts two (VS 9.19 C treats verbal knowledge as inference), and Bhāsarvajña three.
5. NK 5.1 gives 8 or 9 proofs, depending on whether "ādi" (destruction) is counted separately.
6. The Kiraṇāvalī is one work: Udayana's commentary on Praśastapāda. It is listed once, not twice.
7. Nyāya Sūtra numbering depends on the edition: the mantra–Āyurveda sūtra is 2.1.69 in DCS and 2.1.68 in Taranatha.
8. Reading "avyapadeśya / vyavasāyātmaka" in NS 1.1.4 as indeterminate and determinate perception is Vācaspati's, following his teacher Trilocana. It is not in the sūtra or in Vātsyāyana.
9. "Pariśuddhi" is the Nyāyavārttikatātparyapariśuddhi.

## 1. Checklist (item → id)
**Texts**
- Root texts and old commentaries: NS src:nyaya-sutra; NBh; NV; TṬ; nyayasucinibandha.
- Udayana: Pariśuddhi, nyaya-kusumanjali, atmatattvaviveka, laksanavali, kiranavali-udayana, nyaya-parisista.
- Jayanta: nyayamanjari, nyayakalika, agamadambara.
- Bhāsarvajña: nyayasara and nyayabhusana; the bliss view is tea:nyayasara:moksa.
- Manuals: tarkabhasa-kesava-misra, tarkikaraksa, tarkasangraha with its dipika.
- Viśvanātha: bhasapariccheda, nyayasiddhantamuktavali, nyayasutravrtti-visvanatha.
- Tattvacintāmaṇi (4 khaṇḍas) and its commentaries: aloka, didhiti, rahasya, jagadisi, gadadhari.
- Raghunātha's other works: padarthatattvanirupana, akhyatavada-raghunatha, nanvada.
- Jagadīśa: sabdasaktiprakasika, tarkamrta. Gadādhara: vyutpattivada, saktivada. Also muktivada-raghudeva.
- Vaiśeṣika: vaisesika-sutra, vaisesika-sutra-vrtti-candrananda, upaskara, padarthadharmasangraha, vyomavati, nyayakandali, kiranavali-udayana, saptapadarthi, nyayalilavati, dasapadarthasastra.

**Teachers**
- All registry ids are used (Gautama, Vātsyāyana, Uddyotakara, Vācaspati, Udayana, Gaṅgeśa, Kaṇāda, Praśastapāda).
- About 32 others, including Jayanta, Bhāsarvajña, Raghunātha, Jagadīśa, Gadādhara, Mathurānātha, Viśvanātha and Annambhaṭṭa.

**Concepts**
- Categories and method: cpt:sixteen-padarthas-nyaya, cpt:four-pramanas-nyaya / cpt:two-pramanas-vaisesika, cpt:twelve-prameyas.
- NS 1.1.2: cpt:nyaya-chain-of-liberation.
- Inference and debate: cpt:five-membered-inference, cpt:hetvabhasa-nyaya, cpt:three-kinds-of-debate (plus chala, jāti, nigrahasthāna, siddhānta concepts).
- Self and mind: cpt:self-nyaya-vaisesika, cpt:marks-of-the-self, cpt:plurality-of-selves, cpt:manas-atomic.
- Liberation: cpt:apavarga-nyaya, with the bliss question in dsp:bliss-in-liberation.
- Vaiśeṣika ontology: cpt:seven-padarthas-vaisesika, cpt:nine-dravyas, cpt:twenty-four-gunas, cpt:atomism-vaisesika, cpt:adrsta, cpt:dharma-vaisesika (VS 1.1.2).
- Īśvara: cpt:udayana-proofs-of-isvara.
- Navya-Nyāya: cpt:vyapti, cpt:vyaptipancaka, cpt:paramarsa, cpt:paksata, cpt:avacchedaka, cpt:navya-nyaya-cognition-analysis, cpt:alaukika-pratyaksa.
- Section D items: states, body, ethics, rebirth, powers, cosmology, sound/language, and the two path maps (pth:nyaya-path-to-apavarga, pth:vaisesika-path-to-moksa).

**Teachings**: NS 107; VS 58 plus Upaskāra 1.1.4; Praśastapāda 10; NBh 23; NK 9; Tattvacintāmaṇi 10; Tarkasaṅgraha 20; others 22.

**Disputes**
- Registry disputes referenced from teachings: is-there-a-self, isvara, status-of-veda, number-of-pramanas, causation, souls-one-or-distinct, works-knowledge-grace.
- 19 new, all queued with candidate readings:
  - svatah-paratah-pramanya, members-of-inference, whole-and-parts, reality-of-universals, momentariness, external-objects, bliss-in-liberation.
  - eternality-of-sound, theory-of-error, sakti-causal-power, self-awareness-of-cognition, pramana-samplava, establishment-of-pramanas.
  - own-nature-of-things, atomism, validity-of-inference, pilupaka-pitharapaka, definability-of-categories, debate-without-thesis.

**Ultimate views**: ult:nyaya, ult:vaisesika, ult:navya-nyaya. They describe Īśvara plus many eternal selves. The caveats cover the rejection of monism, Udayana's "one Lord, many names" passage, and the rejection of level-of-truth readings.

**Tagging decision**: `level` is "unmarked" for almost all Nyāya-Vaiśeṣika teachings, because the tradition has no two-truth scheme. "conventional" is used only for Vaiśeṣika ritual and ethical injunctions.

## 2. Least sure (check first)
- Nyāyakusumāñjali verse numbers (1.2, 1.3, 3.8, 4.5, closing verse) and the opening-prose list of names.
- All Praśastapāda teachings, especially the common-duty list, the liberation passage and the seers' knowledge.
- Gaṅgeśa's siddhānta definition of vyāpti.
- Āhnika numbers for the Nyāyamañjarī; section summaries for the Ātmatattvaviveka; the Nyāyavārttika on the self.
- Teacher legends and relations: Vāsudeva Sārvabhauma, the Raghunātha–Pakṣadhara debate, Harirāma as Gadādhara's teacher, Raghudeva, Udayana at Puri.
- Minor manuals and commentaries.
- Pīlupāka vs piṭharapāka; the purītat account of deep sleep.
- Borrowings with Āyurveda (Caraka), the Pāśupata affiliation, and Prābhākara categories.
- NS 4.1.59–62 and 3.2.66–72.

## 3. Gaps
- Lost Vaiśeṣika commentaries (Rāvaṇabhāṣya, Kaṭandī, Ātreyabhāṣya).
- Further works of Śaṅkara Miśra and Śrīvallabha; Jagadīśa's Sūkti; Padmanābha's Setu; Rucidatta; Vācaspati II; Bhāvivikta; Śaṅkarasvāmin.
- Raghunātha's specific revisions of the categories, deliberately not asserted.
- The sub-lists of the faults, and the member list of the 21 kinds of pain (the number itself is confirmed).
- External ids referenced by the slug rule and not yet defined by other units:
  - cpt:anatta, cpt:apurva, cpt:four-noble-truths, cpt:non-duality-of-self-advaita, cpt:pramana-vyavastha-buddhist, cpt:satkaryavada, cpt:self-luminous-consciousness, cpt:ten-courses-of-action.
  - obs:three-poisons, prc:asubha-bhavana, prc:sravana-manana-nididhyasana.
  - trm:apurva, trm:pudgala-paramanu, trm:satkaryavada.
  - src:sarvadarsanasangraha, src:naisadhiyacarita, src:tattvopaplavasimha, tch:xuanzang.

## 4. Out of reach
- No local e-texts exist for these, which are the priority targets for Phase C/D:
  - Praśastapāda (PDS), the Nyāyavārttika, Nyāyakusumāñjali and Ātmatattvaviveka.
  - The Nyāyamañjarī, Nyāyasāra and Upaskāra.
  - Praśastapāda's three commentaries: Vyomavatī, Nyāyakandalī, Kiraṇāvalī.
  - The Pratyakṣa, Anumāna and Upamāna khaṇḍas of the Tattvacintāmaṇi.
- The oral pedagogy of the traditional Nyāya schools is not recorded.
- The Daśapadārthī survives only in Chinese.
- No restricted practices occur in this unit.
