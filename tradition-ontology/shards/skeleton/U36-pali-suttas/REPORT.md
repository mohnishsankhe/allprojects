# U36-pali-suttas — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent; subagents cannot write report files in this harness, so the orchestrator saves it.)_

**Scope.** Coverage map B3: the Pali Vinaya and Sutta Piṭaka, the key suttas, and the core concepts of early Buddhism. U36 owns `lin:early-buddhism` and `lin:theravada`, `ult:early-buddhism` and `ult:theravada`. The Abhidhamma, commentaries, manuals and modern lineages belong to U37.

**Method.**
- Everything is skeleton level, written from model knowledge.
- Every teaching is anchored to the local SuttaCentral bilara-data (Mahāsaṅgīti root text, CC0), read alongside Sujato's CC0 English.
- `_gen/canon.py` resolves each teaching's segment range. A range that does not resolve blocks the save (`done()`), so no teaching carries an unchecked locator.
- `original` is filled only by reading the exact segments from the local edition. It keeps the edition's ṁ. There are 96 such quotes.
- Paraphrases are by U36. Fidelity has not been checked.
- Generators live in `_gen/` (part1–part12). `rebuild.sh` regenerates the whole shard from scratch.

**Teaching id convention** (documented in `_gen/common.py`):
- A sutta with its own source uses `tea:<sutta-slug>:<SC section/segment range>`, e.g. `tea:dhammacakkappavattana-sutta:4.1-4.10`. `location.section` gives the canonical number and `location.segments` the full SC segment ids.
- Collections: `tea:dhammapada:277-279`, `tea:udana:8.1`, `tea:itivuttaka:44`, `tea:sutta-nipata:4.11`, `tea:therigatha:5.10`.
- Untitled SN/AN suttas sit under their saṃyutta or nikāya source, e.g. `tea:nidana-samyutta:12.21`, `tea:anguttara-nikaya:3.47`.
- Vinaya uses the traditional numbering: `tea:mahavagga-vinaya:1.23.5`, `tea:cullavagga:10.1.6`, `tea:mahavibhanga:pj3.1.1`.

## 1. Checklist (coverage map B3 and the unit brief's MUST-COVER)

### Canon structure
| item | id(s) |
|---|---|
| Tipiṭaka | src:pali-tipitaka |
| Vinaya Piṭaka | src:vinaya-pitaka |
| Suttavibhaṅga | src:suttavibhanga, src:mahavibhanga, src:bhikkhunivibhanga |
| Pātimokkha (227 / 311, rule classes and counts) | src:patimokkha, src:bhikkhuni-patimokkha |
| Khandhaka: Mahāvagga 1–10, Cullavagga 1–12 | src:khandhaka, src:mahavagga-vinaya, src:cullavagga |
| Parivāra | src:parivara |
| Sutta Piṭaka and the four Nikāyas (counts, organisation) | src:sutta-pitaka, src:digha-nikaya, src:majjhima-nikaya, src:samyutta-nikaya, src:anguttara-nikaya |
| Khuddaka Nikāya in full (18 books of the Burmese canon; Niddesa split into its two parts) | src:khuddaka-nikaya; src:khuddakapatha, src:dhammapada, src:udana, src:itivuttaka, src:sutta-nipata (+ src:atthakavagga, src:parayanavagga), src:vimanavatthu, src:petavatthu, src:theragatha, src:therigatha, src:apadana, src:buddhavamsa, src:cariyapitaka, src:jataka, src:mahaniddesa, src:culaniddesa, src:patisambhidamagga, src:nettippakarana, src:petakopadesa, src:milindapanha |
| 17 main saṃyuttas as sources | src:mara-, bhikkhuni-, nidana-, anamatagga-, khandha-, salayatana-, vedana-, asankhata-, abyakata-, magga-, bojjhanga-, satipatthana-, indriya-, iddhipada-, anapana-, sotapatti-, sacca-samyutta |
| Abhidhamma books | U37 (referenced only) |

### Key suttas

**Registry ids — all have a source entry and teachings:**
- dhammacakkappavattana, anattalakkhana, adittapariyaya, satipatthana (MN 10, section by section), mahasatipatthana, anapanasati, kayagatasati
- samannaphala, brahmajala, mahanidana, mahaparinibbana, kalama
- metta (Snp 1.8), aggivacchagotta, madhupindika, mulapariyaya, vitakkasanthana, sallatha, bahiya

**Brief's additional list — all present:**
- MN 2, 4, 9, 19, 21, 22, 26, 36, 38, 39, 43, 44, 62, 63, 64, 111, 121, 122, 131, 135, 136, 137, 140, 148
- DN 9, 11, 27, 31
- SN 12.15, 12.61, 22.95, 35.23, 45.2, 46.51, 47.19, 56.31
- AN 3.33 (plus 3.34), 4.41, 6.63, 8.6, 10.60
- Ud 8.1–3 (plus 8.4); Snp 1.1, 1.3; Aṭṭhakavagga 4.3, 4.8, 4.9, 4.11, 4.14, 4.15; Pārāyana 5.2, 5.7, 5.16; Iti 43 (plus 1, 27, 44, 49)
- Thig 1.1, 1.12, 3.5, 3.8, 5.9, 5.10, 6.3, 6.6, 10.1, 11.1, 13.1; Thag 16.8, 18.1
- Dhp 1–2, 5, 21, 35, 103, 153–154, 160, 165, 183, 197, 203–204, 223, 276, 277–279, 282, 372, 396

**Also added:**
- DN 3, 4, 5, 8, 13, 14, 23, 26, 32, 33, 34
- MN 1, 7, 8, 11, 12, 13, 18, 20, 24, 27, 28, 41, 47, 49, 56, 58, 61, 70, 75, 86, 93, 95, 98, 101, 107, 115, 117, 118, 119, 125, 128, 129, 130, 141, 143, 145, 146, 149, 152
- Around 40 more SN and AN suttas, including SN 2.26, 5.2, 5.10, 12.1, 12.2, 12.20, 12.21, 12.23, 12.63, 12.65, 12.67, 12.68, 22.22, 22.59, 22.85–89, 35.85, 35.95, 38.1, 43, 44.10, 46.53, 46.55, 47.6, 47.13, 54.9, 55.5 and AN 1.51–52, 1.279, 3.47, 3.61, 3.89, 3.100–101, 3.136, 4.36, 4.49, 4.77, 4.170, 4.232–233, 5.57, 5.177, 6.10, 6.19, 6.55, 7.61, 8.30, 8.39, 8.41, 8.51, 8.53–54, 9.36, 10.25, 10.176, 11.1, 11.15
- Khp 1–4, 7; Ud 1.1, 1.3, 3.10, 4.1, 5.1, 5.5, 6.4; Snp 1.4, 1.7, 2.1, 2.4, 3.2
- Bv 2 (Sumedha, the ten perfections); Mil 3.1.1 (the chariot)
- Vinaya: Mv 1.1, 1.5, 1.6, 1.11, 1.12, 1.21, 1.23–24, 1.54, 2.1–3, 5.1, 8.26, 10.2; Cv 5.8, 5.33, 7.3.14, 10.1, 11, 12; Pār 1, 3, 4

### Concepts
| item | id(s) |
|---|---|
| four noble truths | cpt:four-noble-truths, cpt:three-turnings-twelve-aspects, trm:dukkha/samudaya/nirodha/magga/ariya-sacca |
| three marks | cpt:three-marks, trm:anicca/dukkha/anatta/tilakkhana |
| five aggregates | cpt:five-aggregates, trm:khandha, trm:upadanakkhandha, trm:rupa/vedana/sanna/sankhara/vinnana |
| six sense bases | cpt:twelve-ayatanas, cpt:eighteen-dhatus, trm:ayatana, trm:salayatana, trm:sabba |
| twelve links | cpt:twelve-links, cpt:dependent-origination, trm:paticcasamuppada, trm:idappaccayata, one term per link |
| thirty-seven wings | cpt:thirty-seven-wings, the seven group concepts (cpt:four-satipatthanas, four-right-efforts, four-iddhipadas, five-indriyas, seven-bojjhangas, noble-eightfold-path; the powers are covered by cpt:five-indriyas), and **one term entry for each of the 37 members** (trm:kayanupassana … trm:samma-samadhi, incl. trm:saddhabala … trm:pannabala) |
| jhānas | cpt:four-jhanas, cpt:first-jhana … cpt:fourth-jhana, factor terms |
| formless attainments | cpt:formless-attainments, four sphere terms |
| cessation | cpt:nirodha-samapatti, trm:sannavedayitanirodha, cpt:death-and-cessation |
| hindrances | obs:five-hindrances and each member, with antidotes (SN 46.51) and similes (DN 2, SN 46.55); cpt:five-hindrances |
| factors of awakening | cpt:seven-bojjhangas |
| ten fetters and stages | obs:ten-fetters, obs:five-lower-fetters, obs:five-higher-fetters, each fetter; cpt:four-stages-of-awakening, cpt:eight-noble-persons, cpt:seven-noble-persons |
| papañca | cpt:papanca, obs:papanca, trm:papanca, cpt:conceiving |
| two arrows | cpt:two-arrows, phn:two-darts |
| Bāhiya teaching | cpt:bahiya-teaching |
| three trainings | cpt:three-trainings (+ U51's pth:three-trainings) |
| kamma | cpt:kamma, cpt:four-kinds-of-kamma, cpt:complexity-of-kamma, trm:kamma/cetana/vipaka |
| rebirth and realms | cpt:rebirth, cpt:rebirth-realms (→ U37's cpt:thirty-one-planes), cpt:five-gati, cpt:niraya, cpt:peta |
| ten pāramīs (Theravāda list) | cpt:ten-paramis, trm:parami |
| three knowledges / six abhiññā | cpt:three-vijjas, cpt:six-abhinnas |
| unanswered questions | cpt:undeclared-questions, dsp:avyakata |
| nibbāna and its synonyms | cpt:nibbana, cpt:synonyms-of-nibbana (SN 43 uddāna quoted), cpt:two-nibbana-dhatus |
| anattā | cpt:anatta |
| middle way | cpt:middle-way |
| brahmavihāras | cpt:four-brahmaviharas |
| recollections | cpt:six-anussati |
| foulness and nine charnel stages | prc:asubha-bhavana, prc:navasivathika, prc:patikulamanasikara |
| four elements | cpt:four-elements, cpt:six-dhatus |
| mindfulness of death | prc:maranassati |

**Additional concepts:** luminous mind, emptiness in the suttas, convention and the ultimate, the gradual training, upanisā, seven purifications (MN 24), councils, ordination, garudhamma, the own-language rule (Cv 5.33).

### Practices
- Mindfulness of breathing: prc:anapanasati plus **prc:anapanasati-step-01 … step-16**, and pth:anapanasati-sixteen-steps.
- Satipaṭṭhāna: prc:satipatthana and the four contemplations.
- Divine abidings: prc:brahmavihara-bhavana and the four individual abidings.
- Recollections: six recollection entries.
- Foulness: prc:asubha-bhavana, with the SN 54.9 / Pār 3 warning.
- Removing distracting thoughts: prc:vitakkasanthana (the five methods, MN 20).
- Sense restraint: prc:indriya-samvara.
- Precepts: prc:panca-sila, prc:attha-sila, prc:dasa-sila.
- Uposatha: prc:uposatha, prc:patimokkha-uddesa.
- Also added: kāyagatāsati, suññatā-vihāra, kasiṇa, perception of light, ten perceptions, the five reflections, paritta, act of truth, dāna, going for refuge, pilgrimage, dhutaṅga, care of the sick, offerings to the departed.
- Restricted, summary only, with the text's own rejection: prc:appanaka-jhana and prc:ahara-upaccheda.

### Teachers
- The Buddha: tch:gotama-buddha, with the tradition's dating (623–543 BCE) and the scholarly dating (c. 480–400 BCE) kept apart.
- Named in the brief: Sāriputta, Moggallāna, Ānanda, Mahākassapa, Upāli, Anuruddha, Mahākaccāna, two Puṇṇas (tch:punna-mantaniputta, tch:punna-sunaparantaka), Khemā, Uppalavaṇṇā, Paṭācārā, Dhammadinnā, Kisāgotamī, Mahāpajāpatī, Aṅgulimāla, Bāhiya, Citta, Anāthapiṇḍika, Visākhā (tch:visakha-migaramata; the Visākha of MN 44 is tch:visakha-upasaka).
- Councils: Yasa Kākaṇḍakaputta, Revata, Sabbakāmī, Moggaliputta Tissa.
- Laṅkā and Asoka: Asoka, Mahinda, Saṅghamittā, Devānampiya Tissa, Vaṭṭagāmaṇī.
- Seven past Buddhas, Dīpaṅkara and Metteyya.
- About 60 further disciples, lay followers and interlocutors.

### Disputes
- dsp:is-there-a-self and dsp:women-caste-liberation (U50) are referenced; the Buddhist side is supplied as teachings.
- New disputes:
  - dsp:caste-and-purity
  - dsp:tevijja-union-with-brahma
  - dsp:animal-sacrifice
  - dsp:kiriyavada-akiriyavada (six teachers, reported by opponent)
  - dsp:austerity-and-past-kamma (Jains, MN 101/56)
  - dsp:bhikkhuni-order (Cv 10; recent revival)
  - dsp:avyakata (partially reconciled under P6-upaya and P1-level, with tradition objections)
  - dsp:consciousness-transmigrates
  - dsp:is-there-another-world
  - dsp:devadatta-five-points (partially reconciled under P3-path)
  - dsp:ten-points-vesali
- All others are queued with candidate readings; none is called a contradiction.

### Path maps
- U51's registry maps are referenced: pth:three-trainings, pth:jhana-formless-cessation, pth:four-stages-of-awakening, pth:seven-purifications.
- New maps: pth:gradual-training (DN 2), pth:transcendental-dependent-origination (SN 12.23 / AN 11.1), pth:anapanasati-sixteen-steps. Their bands are logged as interpretation.

### Ultimate views
- ult:early-buddhism and ult:theravada. Caveat: nibbāna is one unconditioned element but not a self, creator or ground (MN 1, DN 1, Dhp 279).

### Corrections to the brief's list (checked against the local texts)
- **AN 3.33 in SuttaCentral numbering** is the Sāriputta Sutta ('no I-making, mine-making'). The Nidāna Sutta (the three roots of kamma), AN 3.33 in the PTS count, is SC **AN 3.34**. Both are included.
- **The three trainings** (adhisīla, adhicitta, adhipaññā): SC AN 3.89.
- **Mahāsaṅgīti titles differ from the common names:**
  - MN 26 is titled Pāsarāsi (id kept as ariyapariyesana-sutta).
  - DN 11 Kevaṭṭa (id kevaddha-sutta); DN 26 Cakkavatti (id cakkavattisihanada-sutta).
  - DN 31 Siṅgāla (id sigalovada-sutta); DN 8 Mahāsīhanāda (id kassapasihanada-sutta).
  - SN 56.31 Sīsapāvana (id simsapa-sutta); AN 3.65 Kesamutti (id kalama-sutta); MN 63/64 Mālukya.
  - Alt titles are recorded.
- **SC and PTS numbers differ:** the Āsīvisa Sutta is SN 35.238 (PTS 35.197) and the Chappāṇa Sutta SN 35.247 (PTS 35.206). Pacalāyamāna is SC AN 7.61, and the Mettā benefits are SC AN 11.15.
- **Snp 5 numbering:** SC numbers the Pārāyana introduction as 5.1, so Ajita is 5.2 and Mogharāja 5.16.
- **The Buddha–Cunda passage:** the 'two meals of equal fruit' statement is DN 16 4.42, a separate teaching from the meal and illness (4.13–4.20).

## 2. Least-sure items (check first)
- **Teachings at moderate confidence (71).** These are paraphrased from memory and checked at section level only:
  - Vinaya narratives: Mv 1.5, 1.6, 1.12.4, 1.21, 1.23–24, 1.54, 2.1–3, 5.1; Cv 5.8, 5.33, 7.3.14, 11.1.x, 12; Pār 3, Pār 4. No English was available locally for the Vinaya.
  - Poem summaries: Thag 16.8, 18.1 and the Therīgāthā summaries; Snp 3.2, 4.3–4.15, 5.2, 5.7; Snp 1.7 (Mātaṅga detail); Snp 2.1.
  - Ud 3.10, 5.5, 6.4; Iti 1; Khp 7.
  - Bv 2.116–165: the similes for the ten perfections are from memory. The names and order were confirmed locally.
  - DN 11 (4–7), DN 33 (1.6–1.7), MN 7 (18–20), MN 56, MN 95, MN 125, MN 130, MN 146, MN 152, SN 22.87 (8–11), SN 51.20, AN 3.61 (9–13), AN 3.65 (17–20), AN 5.28, AN 6.63 (33–38), AN 8.30, AN 4.233.
- **Teachers (31 at moderate confidence).** The commentary- and chronicle-based entries (Mahinda, Saṅghamittā, Moggaliputta Tissa, Devānampiya Tissa, Vaṭṭagāmaṇī, Nāgasena, Milinda) carry dates from memory. So do the 'foremost' (etadagga) attributions, which were not checked item by item against AN 1.188–267. Also Khujjuttarā, Tapussa-Bhallika, Yasodharā (a commentarial name), Revata and Sabbakāmī.
- **Metadata.** Canon counts (SN 7,762 and AN 9,557 by the commentarial count), Parivāra section counts, and the KN book lists of the Thai and Sri Lankan editions. Scholarly dates for KN books are approximate.
- **Snp 1.8 as 'Karaṇīyamettā Sutta'.** This title is traditional; the Mahāsaṅgīti title is 'Mettasutta'.
- **Cross-unit relation targets are guesses** where the other unit had not yet written: cpt:buddha-nature, cpt:emptiness, cpt:bodhicitta, cpt:six-paramitas, obs:three-poisons, trm:sunyata/samvrti and the other Sanskrit-side trm ids. Where U10, U37 and U38 already had ids, the targets were aligned to them.

## 3. Gaps (belong here but not created responsibly in this pass)
- Individual suttas not yet given teachings: most of SN 1–11 (the Sagāthāvagga, apart from 1.1, 2.26, 5.2, 5.10 and 6.1), SN 41 (Citta), SN 36 beyond 36.6, most AN fours to elevens, and MN 3, 5, 6, 14–17, 23, 25, 29–35, 37, 40, 42, 45–46, 48, 50–55, 57, 59–60, 65–69, 71, 73–74, 76–85, 87–92, 94, 96–97, 99–100, 102–106, 108–110, 112–114, 116, 120, 123–124, 126–127, 132–134, 138–139, 142, 144, 147, 150–151.
- The Jātaka, Vimānavatthu, Petavatthu, Apadāna, Cariyāpiṭaka, Niddesa, Paṭisambhidāmagga, Netti and Peṭakopadesa have source entries only. They have no teachings, except Khp 7 (which recurs as Pv 1.5), Bv 2 and Mil 3.1.1.
- The etadagga lists (AN 1.188–267) are not extracted as teachings.
- The Pātimokkha rules themselves are not extracted beyond Pār 1, 3 and 4.
- Energy anatomy (channels, centres) has no counterpart in the Pali suttas; this is noted, not filled.
- Snp 2.7 (Brāhmaṇadhammika) is cited in dsp:animal-sacrifice from memory but has no teaching.

## 4. Out of reach
- The oral chanting traditions (paritta books, Mahāparitta ordering) and the living ordination lineages. Only textual anchors are recorded.
- The modern bhikkhunī revival is summarised from general knowledge and flagged `recent`.
- The Chinese Āgama parallels are U38's.
- No restricted method details are recorded. Breathless meditation and fasting are summary plus the text's own verdict only (MN 12, MN 36).

## 5. Notes for the merge
- **Ids shared with U37/U38** (same doctrine, merged by id): prc:anapanasati, prc:metta-bhavana, prc:buddhanussati, prc:maranassati, prc:kayagatasati, prc:dhutanga, prc:paritta, prc:pattidana; obs:four-oghas, obs:four-upadanas, obs:seven-anusayas, obs:ten-fetters, obs:five-hindrances; cpt:five-aggregates, cpt:four-noble-truths, cpt:dependent-origination, cpt:luminous-mind, cpt:six-abhinnas, cpt:kalyanamittata, cpt:world-cycles, cpt:nirodha-samapatti.
- **Two ids renamed to match U37:** obs:four-vipallasas and obs:four-asavas. The texts usually give three āsavas; this is noted in the entry.
- **Cross-unit relations to U37/U38 concepts are logged as correspondences:** cpt:thirty-seven-bodhipaksya-dharmas, cpt:sasana-decline, cpt:seven-purifications-concept, cpt:four-paths-and-fruits, cpt:karma-as-volition, cpt:councils, cpt:luminous-mind-bhavanga, cpt:two-truths-theravada, cpt:magadhi-root-language, cpt:pudgala-doctrine.
- **dsp:bhikkhuni-order** (Theravāda) is distinct from U38's dsp:bhiksuni-ordination-revival (Mūlasarvāstivāda/Tibet). **dsp:ten-points-vesali** complements U38's dsp:cause-of-the-first-schism.
- **Pali-id terms** carry equivalence links to Sanskrit ids, each logged: trm:nirvana, karma, dhyana, prajna, smrti, maitri, upeksa, avidya, trsna, atman (contested), anatman, skandha, pratityasamutpada, arhat and others. The ones not found in any current shard are trm:anatman, trm:anitya, trm:bodhyanga, trm:marga, trm:samvrti, trm:sunyata and trm:vipasyana.
- **Shared-slug terms** (same word in Pali and Sanskrit) contribute an early-Buddhist definition to the existing id: nirodha, samadhi, citta, sila, karuna, mudita, bhavana, vedana.
