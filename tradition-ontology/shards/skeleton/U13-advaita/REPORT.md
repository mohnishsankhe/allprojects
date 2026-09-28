# U13-advaita — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


All content is written from memory (`skeleton`). The `_gen/part1…part15` scripts rebuild the shard. Sūtra numbers follow Śaṅkara's recension.

## 1. Coverage checklist (coverage-map item → ids)

### A5 — Brahma Sūtras
- **The text** → `src:brahma-sutra`.
  - `structure` records 4 adhyāyas (samanvaya, avirodha, sādhana, phala) × 4 pādas, with the pāda themes in `notes`.
  - Śaṅkara's count is 555 sūtras, with pāda counts 31/32/43/28 | 37/45/53/22 | 27/41/66/52 | 19/21/16/22.
  - Other schools: Rāmānuja 545, Madhva 564; Nimbārka 549 and Vallabha 554 are low confidence. Adhikaraṇa counts are low confidence.
- **Key sūtras** (`tea:brahma-sutra:<ref>`):
  - 1.1.1–5, 1.1.12, 1.3.8
  - 1.3.31/33 (the gods' eligibility), 1.3.34/38 (Śūdras)
  - 1.4.20–23, 1.4.27
  - 2.1.1, 2.1.3, 2.1.11, 2.1.14, 2.1.24, 2.1.33–35
  - The 2.2 critiques: Sāṃkhya 2.2.1; Vaiśeṣika 2.2.11–12; Buddhist realists 2.2.18; Buddhist idealism and the void 2.2.28–29 (with Śaṅkara's comment filed under the id `…-sankara:2.2.32`); Jains 2.2.33; Pāśupatas and others 2.2.37; Pāñcarātra 2.2.42 (with Śaṅkara's comment filed under the id `…-sankara:2.2.44`)
  - 2.3.17–18, 2.3.40, 2.3.43, 2.3.50
  - 3.1.1, 3.1.8
  - 3.2.1–24 (key ones), 3.2.27, 3.2.38, 3.2.41
  - 3.3.1, 3.3.11, 3.3.33, 3.3.53–54 (against the Lokāyata)
  - 3.4.1–2, 3.4.26–27, 3.4.38, 3.4.47, 3.4.51–52
  - 4.1.1–19 (key ones), 4.2.1, 4.2.12, 4.2.17
  - 4.3.1, 4.3.7, 4.3.10, 4.3.12, 4.3.15
  - 4.4.1, 4.4.4–12, 4.4.17, 4.4.21, 4.4.22
- **Teachers named in the sūtras** → `tch:badarayana`, `tch:jaimini` (contributed), `tch:asmarathya`, `tch:audulomi`, `tch:kasakrtsna`, `tch:badari`, `tch:karsnajini`, `tch:atreya-brahma-sutra`.
- **Pre-Śaṅkara Vedāntins**
  - Teachers: `tch:bhartrprapanca`, `tch:brahmadatta`, `tch:brahmanandin` (Ṭaṅka), `tch:dramida`, `tch:sundarapandya`, `tch:upavarsa`, `tch:bodhayana-vrttikara`, `tch:guhadeva`, `tch:kapardin`, `tch:bharuci`.
  - Their lost works: `src:bodhayana-vrtti`, `src:upavarsa-vrtti`, `src:vakya-brahmanandin`, `src:dramida-bhasya`, `src:bhartrprapanca-bhasya`.
- **Lineage and ultimate view** → `lin:vedanta`, `ult:vedanta`, `pth:devayana-brahma-sutra`.

### A6 — Advaita texts and teachers
- **Lineages and ultimate views** → `lin:advaita-vedanta`, `lin:vivarana`, `lin:bhamati`; `ult:advaita-vedanta`, `ult:vivarana`, `ult:bhamati`.
- **Gauḍapāda** → `src:mandukya-karika` (4 prakaraṇas, 215 kārikās), 25 teachings `tea:mandukya-karika:*` (including 2.32, 3.39–48 and 4.22), `tch:gaudapada`, `tch:govinda-bhagavatpada`.
- **Śaṅkara's accepted works**
  - BSBh, including the adhyāsa-bhāṣya (`tea:brahma-sutra-bhasya-sankara:intro` … `intro/5`).
  - The Gītā commentary.
  - Ten Upaniṣad commentaries (BĀU, ChU, TU, Ait, Īśa, Kena, Kaṭha, Praśna, Muṇḍ, Māṇḍ+Kārikā).
  - The Upadeśasāhasrī.
- **Works attributed to Śaṅkara** (each marked traditional, disputed or doubtful)
  - Vivekacūḍāmaṇi, Ātmabodha, Aparokṣānubhūti, Bhaja Govindam, Nirvāṇaṣaṭkam, Dakṣiṇāmūrti Stotram
  - Tattvabodha, Daśaślokī, Ekaślokī, Manīṣāpañcaka, Sādhanapañcaka, Kaupīnapañcaka, Yatipañcaka, Dhanyāṣṭaka
  - Vākyavṛtti, Śataślokī, Prabodhasudhākara, Sarvavedāntasiddhāntasārasaṅgraha, Pañcīkaraṇa, Ātmānātmaviveka, Svātmanirūpaṇa, Brahmajñānāvalīmālā
  - Śivānandalaharī, Maṭhāmnāya, and the Śvetāśvatara commentary (doubtful)
- **Śaṅkara's disciples** → `tch:padmapada`, `tch:suresvara`, `tch:hastamalaka` (Hastāmalakīya), `tch:totaka` (Toṭakāṣṭaka, Śrutisārasamuddharaṇa).
- **Maṇḍana** → Brahmasiddhi, Vibhramaviveka, Vidhiviveka, Bhāvanāviveka, Sphoṭasiddhi; also `tch:ubhaya-bharati`.
- **Sureśvara** → Naiṣkarmyasiddhi, the BĀU and TU Vārttikas, Mānasollāsa and Pañcīkaraṇavārttika (the last two traditional).
- **Vivaraṇa line** → Pañcapādikā, Pañcapādikāvivaraṇa, Tattvadīpana, Vivaraṇaprameyasaṅgraha.
- **Bhāmatī line** → Bhāmatī, Tattvasamīkṣā (lost), Vedāntakalpataru, Śāstradarpaṇa, Kalpataruparimala.
- **Other dialectical and doctrinal works**
  - Saṃkṣepaśārīraka and Pañcaprakriyā (Sarvajñātman)
  - Iṣṭasiddhi (Vimuktātman)
  - Nyāyamakaranda (Ānandabodha)
  - Khaṇḍanakhaṇḍakhādya (Śrīharṣa)
  - Tattvapradīpikā (Citsukha)
  - Nyāyanirṇaya (Ānandagiri) and Ratnaprabhā (Govindānanda)
- **Vidyāraṇya and Bhāratītīrtha**
  - Pañcadaśī, Jīvanmuktiviveka, Anubhūtiprakāśa, Vaiyāsikanyāyamālā, Dṛg-Dṛśya Viveka.
  - Śaṅkaradigvijaya and Sarvadarśanasaṅgraha, with their attribution to Vidyāraṇya marked as disputed.
- **Prakāśānanda** → Vedāntasiddhāntamuktāvalī.
- **Madhusūdana** → Advaitasiddhi, Gūḍhārthadīpikā, Siddhāntabindu, Bhaktirasāyana, Vedāntakalpalatikā, Advaitaratnarakṣaṇa, Prasthānabheda.
- **Brahmānanda Sarasvatī** → Laghucandrikā.
- **Appayya** → Siddhāntaleśasaṅgraha, Parimala, Nyāyarakṣāmaṇi, Śivārkamaṇidīpikā.
- **Sadānanda** → Vedāntasāra, with the Subodhinī and Vidvanmanorañjanī commentaries.
- **Dharmarāja** → Vedāntaparibhāṣā (six pramāṇas), with the Śikhāmaṇi commentary.
- **Tripura Rahasya and later works** → Tripura Rahasya, Advaitamakaranda, Vedāntatattvaviveka, Ātmapurāṇa, Svārājyasiddhi, Ātmavidyāvilāsa, Kaivalya Navanītam (Tamil), Advaitabodhadīpikā, Bhāvārthadīpikā.
- **Recent (`recent: true`)** → Mūlāvidyānirāsa; `tch:satchidanandendra-sarasvati`, `tch:candrasekhara-bharati-iii`, `tch:candrasekharendra-sarasvati`, `tch:chinmayananda`, `tch:dayananda-saraswati-arsha`.

### A6 — Advaita concepts
- `cpt:maya`; `cpt:avidya`, `cpt:bhavarupa-avidya`, `cpt:avarana-viksepa`; `dsp:locus-of-avidya`
- `cpt:adhyasa`
- `cpt:vivarta-vada` (contrasted with `cpt:satkaryavada`)
- `cpt:three-levels-of-reality`, `cpt:mithyatva` (five definitions), `cpt:badha`
- `cpt:jivanmukti`, `cpt:videhamukti`, `cpt:krama-mukti`, `cpt:three-kinds-of-karma`, `cpt:potter-wheel`
- `cpt:sadhana-catustaya`, `cpt:sat-sampatti`, with terms for all six virtues
- `cpt:sravana-manana-nididhyasana`, `cpt:adhyaropa-apavada`, `cpt:saksin`
- `cpt:three-bodies`, `cpt:five-sheaths`, `cpt:three-states-and-turiya`
- `cpt:how-the-one-appears-as-many`, `cpt:avaccheda-vada`, `cpt:pratibimba-vada`, `cpt:abhasa-vada`
- `cpt:eka-jiva-vada`, `cpt:aneka-jiva-vada`, `cpt:drsti-srsti-vada`, `cpt:ajativada`
- `cpt:jahad-ajahal-laksana`, `cpt:mahavakya`
- Stock illustrations → `cpt:stock-illustrations` plus rope-snake, shell-silver, pot-space, reflection, dream, clay and pots, tenth man, crystal and flower, potter's wheel.
- Advaita on karma and bhakti → `cpt:karma-in-advaita`, `cpt:bhakti-in-advaita`.
- Renunciation → `cpt:sannyasa-advaita`, referencing `lin:dasanami` (owned by U57).
- The four maṭhas as the tradition's account → `cpt:four-amnaya-mathas`, `src:mathamnaya`.
- Also covered: `cpt:prakriya-principle`, `cpt:advaita-guru-parampara` and the section-D checklist items (pramāṇa, perception, antaḥkaraṇa, samādhi, creation, pralaya, death of the knower, siddhis, marks of the jīvanmukta).

### F, E and G — path maps, practices, debates
- **Path maps**
  - The teachings reference `pth:advaita-sadhana` (owned by U51) and `pth:yoga-vasistha-seven-bhumikas`.
  - New maps owned by this unit: `pth:aparoksanubhuti-fifteen-limbs`, `pth:pancadasi-seven-states`, `pth:vedantasara-samadhi-auxiliaries`, `pth:devayana-brahma-sutra`.
- **Practices (E)**
  - `prc:atma-vicara` (self-inquiry), `prc:saksi-bhava` (witness), `prc:neti-neti`, `prc:nididhyasana`
  - Also: śravaṇa, manana, seer–seen and sheath discrimination, the three states, anvaya-vyatireka, parisaṃkhyāna, prasaṅkhyāna, asparśa-yoga, Oṃ meditation, saguṇa and nirguṇa meditation, the two samādhis, vāsanā-kṣaya, mano-nāśa, the two sannyāsas, and others (29 in all).
- **Debates owned by U50** → Advaita's side is supplied as teachings referencing `dsp:world-real-or-appearance`, `dsp:souls-one-or-distinct`, `dsp:advaita-crypto-buddhism`, `dsp:saguna-nirguna`, `dsp:causation`, `dsp:is-there-a-self`, `dsp:works-knowledge-grace`, `dsp:isvara`, `dsp:status-of-veda`, `dsp:women-caste-liberation`, `dsp:number-of-pramanas`.
- **New disputes (18)**
  - The four the brief asked for: `dsp:locus-of-avidya`, `dsp:jnana-karma-samuccaya` (Bhartṛprapañca, Maṇḍana, Śaṅkara/Sureśvara, Bhāmatī and Vivaraṇa; includes the Māhiṣmatī debate as the tradition's account), `dsp:prasankhyana`, `dsp:sravana-alone-liberates`.
  - Further Advaita-internal debates: `dsp:how-the-one-appears-as-many`, `dsp:eka-jiva-aneka-jiva`, `dsp:drsti-srsti-vada`, `dsp:bhavarupa-avidya`, `dsp:maya-avidya-distinction`, `dsp:jivanmukti-possible`, `dsp:khandana-definability`.
  - Debates over the sūtras: `dsp:is-anandamaya-brahman`, `dsp:pancaratra-brahma-sutra`, `dsp:jiva-brahman-relation-brahma-sutra`, `dsp:state-of-the-liberated-brahma-sutra`, `dsp:destination-of-devayana`, `dsp:bodies-of-the-liberated`, `dsp:eligibility-of-gods`.
  - Each is either reconciled with a named principle (with the tradition's objections recorded) or queued with candidate readings.

## Corrections to the task's must-cover list
1. **Sundarapāṇḍya** is not named in the sūtras or by Śaṅkara. Later commentators attribute to him the verses quoted at the end of BSBh 1.1.4 (low confidence).
2. **Brahmanandin/Ṭaṅka** (and Dramiḍa) are known mainly from Yāmuna and Rāmānuja, not from Advaita commentaries.
3. **Bhartṛprapañca and Brahmadatta** are not named in the sūtras. They are known through Śaṅkara's and Sureśvara's refutations; Ānandagiri supplies Bhartṛprapañca's name.
4. **More teachers are named in the sūtras** than the list gave: Jaimini, Bādari, Kārṣṇājini and Ātreya as well. All are added.
5. **"2.2 … Pāñcarātra"** is Śaṅkara's reading. Rāmānuja reads 2.2.42–45 as upholding the Pāñcarātra; recorded as `dsp:pancaratra-brahma-sutra`.
6. **3.2.11** is read by Rāmānuja as affirming both marks of Brahman; noted on the teaching.
7. **Prasaṅkhyāna** (Maṇḍana, criticized in Upadeśasāhasrī metrical ch. 18) is distinct from Śaṅkara's own parisaṃkhyāna (Upadeśasāhasrī prose ch. 3). Both are recorded.
8. **Maṇḍana and Sureśvara** are one person in the tradition's account but distinct for most scholars; the karma dispute treats them as distinct voices.
9. **Tripura Rahasya** is a Śrīvidyā-milieu text whose self-aware (vimarśa) non-dualism is closer to Śākta thought; it is tagged `lin:sakta` and `lin:srividya` as well.
10. **Dṛg-Dṛśya Viveka and Pañcadaśī** have disputed or shared authorship (Bhāratītīrtha, Vidyāraṇya).
11. **The potter's wheel** image is placed at BSBh 4.1.15 (moderate confidence). The arrow image for prārabdha is in the Vivekacūḍāmaṇi and possibly ChUBh 6.14.2 (low confidence).
12. **Kāñcī Kāmakoṭi** also claims foundation by Śaṅkara, which the four āmnāya maṭhas dispute; recorded as a tradition's account.

## 2. Least sure (check these first)
- **Verse numbers**
  - Vivekacūḍāmaṇi 47, 113–115, 427, 451–453.
  - Aparokṣānubhūti 100–101, 116, 127–128, 143–144.
  - Pañcadaśī 1.15–17, the ch. 7 seven-states locator and the ch. 9 pratibandha passage.
  - Dṛg-Dṛśya Viveka 23–37.
  - Saṃkṣepaśārīraka 1.319; BĀU-Vārttika 1.4.402; Brahmasiddhi 2.1.
  - The placement of the Gūḍhārthadīpikā closing verse (ch. 15).
  - Cross-reference `tea:yoga-vasistha:3.118`.
- **Section-level references I built myself**
  - Topic ids such as `…vivarana:locus`, `…bhamati:manas`, `…vedantasara:*`.
  - BĀUBh 5.1.1 (the Bhartṛprapañca refutation locator).
- **Doctrines ascribed to specific people**
  - Maṇḍana's secondary jīvanmukti (`tea:brahmasiddhi:4/2`).
  - Brahmadatta's views.
  - The authors attached to the five definitions of mithyātva.
  - Bhāmatī vs Vivaraṇa on vividiṣā vs vedana.
  - The "two avidyās" in the Bhāmatī's opening verse.
- **Dates**
  - Prakāśātman, Sarvajñātman, Vimuktātman, Ānandabodha, Sadānanda, Prakāśānanda, Brahmānanda.
  - The Subodhinī's 1588 date.
- **Low-confidence persons and works**
  - Guhadeva, Kapardin, Bharuci, Jñānottama, Akhaṇḍānanda, Tāṇḍavarāya Svāmī.
  - Advaitabodhadīpikā, Pañcaprakriyā, Nyāyarakṣāmaṇi.
- **Tripura Rahasya** chapter structure and all its teachings.
- **Details of the Maṭhāmnāya** (which names and Vedas go with which maṭha).
- **Station order** in `pth:devayana-brahma-sutra` and the **glosses of the fifteen limbs**.

## 3. Gaps (belong here, but I could not create them responsibly)
- **Minor sub-commentaries**, known only in outline, not entered: Ānandapūrṇa, Rāmānanda Sarasvatī (Vivaraṇopanyāsa), Śaṅkhapāṇi, Anubhūtisvarūpa, Nyāyadīpāvalī, Pramāṇamālā, Advaitadīpikā, Vāsudevamanana.
- **Other Śaṅkara hagiographies** (Anantānandagiri, Cidvilāsa, Vyāsācala, Rājacūḍāmaṇi, Bṛhat-Śaṅkaravijaya) are named only in `src:sankaradigvijaya` notes.
- **The Śṛṅgeri and other maṭha guru-lists** are not entered.
- **The Nyāyāmṛta–Advaitasiddhi exchange**: I entered no separate dispute for it; Advaita's side is in the Advaitasiddhi teachings under `dsp:world-real-or-appearance`. U50 should add as historical_debates:
  - Nyāyāmṛta → Advaitasiddhi → Taraṅgiṇī → Laghucandrikā
  - Rāmānuja's seven untenabilities (saptavidha-anupapatti)
  - Deśika's Śatadūṣaṇī
  - Bhāskara's critique
- **Gauḍapāda–Madhyamaka borrowing**: left to U49, which owns coverage C. The key teachings it can rest on are GK 4.1, 4.2, 4.22, 4.47, 4.99 and 2.32.

## 4. Out of reach / coordination
- The oral teaching method (sampradāya) and the Daśanāmī initiatory transmission (mahāvākya-upadeśa at sannyāsa dīkṣā) are only documented in part; they belong to U57's GAPS.
- **Ids that need deduplication at merge** (my choices):
  - Concepts: `cpt:five-sheaths`, `cpt:three-bodies`, `cpt:three-states-and-turiya`, `cpt:pramana`, `cpt:six-marks-of-purport`, `cpt:devayana-pitryana`, `cpt:three-gunas`.
  - Terms: `trm:prarabdha-karma`, `trm:sancita-karma`, `trm:agami-karma`, `trm:annamaya-kosa` … `trm:anandamaya-kosa`, `trm:moksa`.
  - Practices: `prc:atma-vicara`, `prc:neti-neti`, `prc:saksi-bhava`.
  - Obstacles: `obs:avidya`, `obs:laya`, `obs:viksepa`.
  - Teacher: `tch:bodhayana-vrttikara` (to avoid a clash with the Dharmasūtra's Bodhāyana).
- **References to other units' ids, not defined here** (expected):
  - Teachings in U03, U05 and U06: `tea:bhagavad-gita:*`, `tea:brhadaranyaka-upanisad:*`, `tea:chandogya-upanisad:*`, `tea:katha-upanisad:2.3.16`, `tea:mundaka-upanisad:1.2.12`, `tea:yoga-vasistha:3.118`.
  - `cpt:satkaryavada` (U09).
