# U02-brahmana-vedanga — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Generators are in `_gen/part1…part11`. All entries are at level `skeleton`. Where `notes` say "Phase-B spot check", the locator and wording were matched against the local e-texts in `sources_raw/`. This is not a Phase-C sourcing check.

## 0. Corrections to the task's MUST-COVER list
- **Jaiminīya Upaniṣad Brāhmaṇa.** It is a Brāhmaṇa, not an Āraṇyaka in name. It does the Āraṇyaka's job for the Jaiminīyas and contains the Kena Upaniṣad.
- **Prajāpati's "dismemberment".** The Brāhmaṇas say he fell apart (vyasraṃsata) from the exhaustion of creating (ŚB 1.6.3.35; 10.1.1.2). Nobody dismembers him; contrast RV 10.90.
- **Kalpa authors.**
  - Āśvalāyana has a Śrauta- and a Gṛhyasūtra only, with no Dharma- or Śulbasūtra.
  - Kātyāyana has Śrauta and Śulba. The White Yajurveda Gṛhyasūtra is Pāraskara's.
- **The three debts.** TS 6.3.10.5 gives three debts. ŚB 1.7.2.1–6 gives four, adding hospitality to men.
- **The āśrama debate** has three positions, not two:
  - vikalpa (free choice);
  - samuccaya (sequence);
  - bādha/aikāśramya (only the householder's order is valid): GDh 3.36 in Stenzler's numbering (GDh 3.35 is wrong), and BDh 2.6.11.27–28.
- **Puruṣārthas.** The early texts speak of three aims (trivarga). Mokṣa is added later as a fourth.
- **Pāṇinīya Śikṣā 3.** The text says the phonemes were declared by Svayambhū, not "in Śambhu's view".
- **Signs of death.** A supposed "signs of death" passage at AA 3.2.4 is not there, so it was not created. AA 3.2 was checked, and 3.2.3/5/6 were used instead.

## 1. Coverage checklist (coverage-map item → ids)

**A1 Brāhmaṇas**
- src:aitareya-brahmana, kausitaki-brahmana, taittiriya-brahmana, satapatha-brahmana, satapatha-brahmana-kanva, pancavimsa-brahmana, sadvimsa-brahmana, jaiminiya-brahmana, jaiminiya-upanisad-brahmana, gopatha-brahmana.
- Minor Sāmaveda Brāhmaṇas: samavidhana, arseya, devatadhyaya, samhitopanisad, vamsa, mantra, jaiminiya-arseya.
- Also src:kathaka-brahmana, vadhula-anvakhyana, satyayana-brahmana.

**Brāhmaṇa topics**
| Item | Ids |
|---|---|
| Ritual theory | cpt:sacrifice-as-cosmos, cpt:bandhu-correspondences, cpt:adhidaiva-adhyatma-adhiyajna, cpt:paroksa, cpt:deva-asura, cpt:brahmana-cosmogonies |
| Prajāpati | cpt:prajapati-dismemberment-restoration, cpt:year-as-prajapati; tea ŚB 1.6.3.35-36, 10.1.1.2-3, AA 3.2.6 |
| Prāṇa | cpt:prana-in-brahmanas; tea ŚB 6.1.1.1-5, KB 7.1, AA 2.2.1, ŚB 11.6.3.1-11 |
| Fire altar | cpt:agnicayana-fire-altar, prc:agnicayana; tea ŚB 10.1.1.2-3, 10.2.3.18, 10.4.3.1-10, 10.5.3.1-12 |
| Śāṇḍilya-vidyā | tea:satapatha-brahmana:10.6.3.1-2, cpt:sandilya-vidya, prc:sandilya-vidya-upasana, tch:sandilya |
| Yājñavalkya in ŚB | tch:yajnavalkya; tea ŚB 3.1.2.21, 11.3.1.2-4, 11.6.2.6-10, 11.6.3.1-11, 14.9.4.33 |
| Also | punarmṛtyu, weighing of deeds, the debts, five great sacrifices, upanayana, svādhyāya, Bhṛgu, Naciketas (TB 3.11.8), Bharadvāja (TB 3.10.11), the world-creators' session (TB 3.12.9) |

**Āraṇyakas**
- src:aitareya-aranyaka, kausitaki-aranyaka, taittiriya-aranyaka, katha-aranyaka, and the JUB.
- Internalized sacrifice: cpt:internalized-sacrifice.
- Prāṇāgnihotra: cpt:pranagnihotra, prc:pranagnihotra, trm:pranagnihotra. Teachings:
  - tea:chandogya-upanisad:5.19-23, 5.24.1-3, 5.24.4 (uses U03's source id);
  - tea:kausitaki-upanisad:2.5 (= ŚĀ 4.5), with prc:pratardana-samyamana;
  - tea:mahanarayana-upanisad:69-70 (TA 10);
  - tea:maitri-upanisad:6.9;
  - tea:pranagnihotra-upanisad:1-4 (src:pranagnihotra-upanisad and src:mahanarayana-upanisad were entered for the cross-reference; U04 owns them).

**Vedāṅgas** (lin:vedanga; cpt:six-vedangas; tea:mundaka-upanisad:1.1.4-5)
- **Śikṣā:** src:paniniya-siksa (8 teachings, all checked), rgveda-/taittiriya-/vajasaneyi-/atharvaveda-pratisakhya, rktantra, puspasutra, yajnavalkya-/naradiya-/vyasa-/manduki-siksa, vikrtivalli. Also tea:taittiriya-upanisad:1.2, 1.3, tea:chandogya-upanisad:2.22.3-5, prc:vedic-recitation-pathas, obs:reciter-faults, obs:faulty-pronunciation.
- **Chandas:** src:pingala-chandahsutra, nidana-sutra, vrttaratnakara; cpt:vedic-meters with the main metres; tea:chandogya-upanisad:1.4.2.
- **Vyākaraṇa:** src:astadhyayi, mahesvara-sutra, dhatupatha, ganapatha, unadisutra, varttika-katyayana, mahabhasya (Paspaśā ×5 and on 6.1.84), kasikavrtti, nyasa, padamanjari, mahabhasya-pradipa, siddhantakaumudi, laghusiddhantakaumudi, prakriyakaumudi, paribhasendusekhara, and the non-Pāṇinian grammars (katantra, candra, jainendra, sakatayana, siddhahema, mugdhabodha, prakrtaprakasa). Philosophy of language is left to lin:vyakarana (U31).
- **Nirukta:** src:nighantu, nirukta and its commentaries. There are 18 Nirukta teachings (1.1, 1.2, 1.12, 1.15, 1.16, 1.18, 1.20 ×2, 2.1, 2.3-4, 2.11, 2.16, 7.1, 7.4, 7.5, 7.6-7, 12.1), plus lin:nairukta and lin:aitihasika.
- **Kalpa:** src:apastamba-kalpasutra and baudhayana-kalpasutra; 16 Śrautasūtras, 18 Gṛhyasūtras (incl. kausika-sutra, karmapradipa), 5 Śulbasūtras, 7 Dharmasūtras; tea ĀpŚS 24.1.30-33, KŚS 1.1.1-8, ĀśGS 1.1.2/1.7.1/1.19.1-7/4.1-6.
- **Jyotiṣa:** src:vedanga-jyotisa (tea r.1, r.3, r.6, r.35, y.3), atharva-jyotisa; tch:lagadha. U32 is referenced via lin:jyotisa.
- **Indices and supplements:** sarvanukramani, brhaddevata, rgvidhana, caranavyuha, atharvaveda-parisistas.

**Dharmaśāstra** (lin:dharmasastra)
- **Sources:** Manu (≈70 teachings), Yājñavalkya (11), Nārada, Viṣṇu, Parāśara, Bṛhaspati, Kātyāyana, Hārīta, Śaṅkha-Likhita and minor smṛtis. The four Dharmasūtras have about 35 teachings between them. Commentaries and digests: Medhātithi, Kullūka, Viśvarūpa, Mitākṣarā, Aparārka, Ujjvalā, Maskarin, Govindasvāmin, Vaijayantī, Dāyabhāga, Kalpataru, Smṛticandrikā, Caturvargacintāmaṇi, Parāśaramādhavīya, Kālanirṇaya, Smṛtitattva, Nirṇayasindhu, Bhagavantabhāskara, Vīramitrodaya, Dharmasindhu. src:arthasastra and src:kamasutra cover the aims of life.
- **Topics:**

| Item | Ids |
|---|---|
| Āśramas | cpt:four-asramas, pth:four-asramas, dsp:asrama-vikalpa-samuccaya-badha |
| Puruṣārthas | cpt:four-purusarthas, trm:purusartha/trivarga/artha/kama/moksa, dsp:which-purusartha-is-foremost |
| Varṇa | cpt:varna-social-order, cpt:jati-mixed-classes, obs:varnasankara; tea MDh 1.31, 1.88-91, 10.4, ĀpDh 1.1.1.4-8, 2.5.11.10-11, TS 7.1.1.4-6, TB 3.12.9.2, GDh 12.4-6 |
| Saṃskāras | cpt:samskaras, cpt:forty-samskaras-eight-virtues, pth:samskara-life-cycle, 14 sacrament practices |
| Five great sacrifices | cpt:five-great-sacrifices, prc:panca-mahayajna |
| Three debts | cpt:three-debts |
| Prāyaścitta | cpt:prayascitta, prc:prayascitta-confession, prc:krcchra-penances, prc:candrayana (both restricted), obs:mahapataka, obs:upapataka |
| Śrāddha, antyeṣṭi, death | prc:sraddha-ancestral-rite, prc:antyesti, prc:udakakarma, prc:asthi-sancayana, prc:sapindikarana, prc:asauca-observance, cpt:funeral-rites, cpt:asauca, cpt:ancestors-pitrs, cpt:preta-to-pitr, cpt:yatana-body, prc:mahaprasthana (restricted), dsp:widow-anvarohana |

**Section D, per lineage**
- The ultimate: ult:vedanga, ult:dharmasastra.
- Self and mind: cpt:self-in-dharmasastra, cpt:self-as-witness, cpt:eleven-senses, cpt:gradation-of-manifest-self.
- Guṇas: cpt:three-gunas-in-dharmasastra.
- Karma: cpt:karma-of-mind-speech-body, cpt:pravrtti-nivrtti.
- Yoga: cpt:yoga-in-dharmasastra, phn:signs-of-yogic-success.
- Time and cosmology: cpt:ages-and-day-of-brahma, cpt:yuga-dharma, cpt:five-year-yuga.
- Teacher and transmission: cpt:teacher-student-rules, cpt:fitness-of-the-student, cpt:upanayana-second-birth, cpt:vamsa-lineage-lists, cpt:sista.
- Sound and language: cpt:varna-phoneme, cpt:power-of-accent, cpt:origin-of-speech-in-the-body.

**Section G:** new disputes as listed above, plus dsp:form-of-the-gods, dsp:authority-of-regional-custom, dsp:niyoga, dsp:inheritance-by-birth-or-death, dsp:vedic-ritual-killing-and-ahimsa. Teachings reference U50's dsp:status-of-veda, dsp:women-caste-liberation, dsp:works-knowledge-grace and dsp:number-of-pramanas.

**Teachers:** all those named in the task, with tradition and scholarly dating kept apart. The grammarian Patañjali is kept as a separate id, tch:patanjali-grammarian, and the tradition's identification with tch:patanjali is noted.

## 2. Least sure (check first)
- **Locators from memory (moderate or low):** ŚB 12.5.2 (kāṇḍa 12 is not in the local text), ŚB 14.1.1, ŚB 1.2.3.6-9; AB 5.33-34; TA 2.2 (anuvāka inferred); GB 1.1.16-30; JB 1.42-44; PB 17.1; Nirukta 2.16; VJ y.3; MDh 1.61-63, 2.88-92, 5.83; the 3.192-199 and 3.267-272 summaries; ĀśGS 4.1-6; MaiU 6.9; the Prāṇāgnihotra Upaniṣad (whole text).
- **Dating:** almost all scholarly dates are low confidence, especially Vedāṅga Jyotiṣa, Piṅgala, Yāska and the Prātiśākhyas.
- **Doubtful attributions:**
  - Piṅgala as Pāṇini's younger brother;
  - Vyāḍi and the Vikṛtivallī;
  - the Nandikeśvara-kāśikā;
  - Viśvarūpa = Sureśvara, and Mādhava = Vidyāraṇya;
  - Haradatta of the Dharmasūtra commentaries = Haradatta of the Padamañjarī;
  - the Kātyāyana identities (vārttikas, Prātiśākhya, Śrautasūtra, Vararuci).
- **Weak disputes:**
  - dsp:widow-anvarohana: commentators' locators are low confidence.
  - dsp:niyoga: the Bṛhaspati verse is known only through commentaries.
  - dsp:inheritance-by-birth-or-death: side locators are at chapter level.
  - The MBh 12.161 details in dsp:which-purusartha-is-foremost.
- **Minor texts with thin contents:** Vādhūla Anvākhyāna, Kaṭha Āraṇyaka, Māṇḍūkī Śikṣā, Ṛktantra, Puṣpasūtra, Nidānasūtra, Atharva Jyotiṣa, and the Atri, Saṃvarta, Uśanas and Śātātapa smṛtis.
- **New non-registry ids** for the orchestrator to confirm: lin:arthasastra, lin:kamasastra, lin:nairukta, lin:aitihasika, lin:mitaksara-school, lin:dayabhaga-school; tch:patanjali-grammarian, tch:manu-svayambhuva, tch:manu-vaivasvata. The equivalence target obs:klesas belongs to another unit and may need renaming.

## 3. Gaps (belong here but not created responsibly)
- ŚĀ 10 (the interiorized Agnihotra chapter) and BDh 2.12 (prāṇāgnihotra in the rules for eating): these locators were not verified, so no teachings were made for them.
- The Kena Upaniṣad's locator inside the JUB.
- The signs-of-death passage (it is probably in the Āraṇyaka or Pariśiṣṭa literature, but not at AA 3.2.4).
- The Kauṣītaki Āraṇyaka's chapter contents beyond adhyāyas 3–6.
- The 40 or so minor Śikṣās in `raw_etexts/shixA` (not catalogued individually).
- The individual Gṛhya and Śrauta sūtra teachings beyond Āśvalāyana.
- The Śulbasūtra verse locators.
- The later pāṭha/vikṛti treatises (Jaṭāpaṭala and others).
- The antyeṣṭi-paddhati titles.
- The sixteen-saṃskāra list's textual source (lists vary).
- The upavedas list (Caraṇavyūha, not verified).
- The Hārīta brahmavādinī quotation (known only through digests).
- The kalivarjya lists (Brahmavaivarta and Āditya Purāṇa verses, cited by digests).
- The Mīmāṃsā side of the ritual-killing debate (U12) and its Sāṃkhya and Jain anchors (U09, U34/35).

## 4. Out of reach
- The living oral recitation traditions (pāṭhas and vikṛtis as taught in the Vedic schools), and the family ritual paddhatis used in practice.
- Śrauta and Gṛhya commentaries still only in manuscript (e.g. parts of Harisvāmin and Bhaṭṭa Bhāskara).
- Lost texts known only from quotations: the Śāṭyāyana Brāhmaṇa, Bṛhaspati, Kātyāyana, Hārīta and Śaṅkha-Likhita.
- Restricted practices (the kṛcchra and cāndrāyaṇa penances, mahāprasthāna) are recorded as summary and warnings only.
