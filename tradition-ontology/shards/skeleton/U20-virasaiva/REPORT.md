# U20-virasaiva — skeleton sweep report
_(Returned as text by the U20 subagent and saved by the orchestrator.)_

Owns lin:virasaiva; also created the sub-lineages lin:pancacarya, lin:sarana-vacana, lin:aradhya-saiva.
Counts: sources 75 · lineages 4 · teachers 78 · teachings 157 (122 SSM, 35 vacana/narrative) · terms 119 · concepts 43 · ult 4 · practices 23 · obstacles 15 · phn 12 · paths 1 · disputes 10 · borrowings 7 · interpretation_log 29. Validator: 0 errors.

## Method
- All entries are `skeleton`.
- Siddhāntaśikhāmaṇi (SSM): the 21-chapter structure, the full list of 101 sthalas and every SSM reference were checked against the local Muktabodha e-text M00207. 57 teachings carry the exact Devanāgarī verse as `original` (extracted by `_gen/extract_ssm_verses.py`). They are rated confidence high, but not yet fidelity-checked.
- Vacanas: from memory, with no `original`. Each is located by incipit, or by a descriptive `v-` key when the incipit is not recalled.
- Other Sanskrit Vīraśaiva sources: the catalogue metadata of the local e-texts.

## 1. Checklist
- **Basava / Kalyāṇa / Anubhava Maṇṭapa:** tch:basava; cpt/trm:anubhava-mantapa; trm:sunya-simhasana; tea:sunyasampadane:allama-at-kalyana; tea:basava-purana-palkuriki:episode-kalyana.
- **Allama Prabhu:** tch:allama-prabhu, tch:animisayya, src:allama-prabhu-vacanas, tea:prabhudevara-ragale:episode-animisa.
- **Akka Mahādēvi:** tch:akka-mahadevi, src:akka-mahadevi-vacanas (5 teachings), tea:sunyasampadane:akka-mahadevi, src:yoganga-trividhi.
- **Cennabasava:** tch:cennabasava, src:cennabasava-vacanas, src:karanahasuge, src:mantragopya (attribution disputed).
- **Siddharāma:** tch:siddharama, src:siddharama-caritre, dsp:allama-siddharama-works.
- **Mācayya, Cauḍayya, Candayya:** tch entries and vacana sources.
- **Women vacanakāras (all tch):** Akkamma, Muktāyakka, Satyakka, Gaṅgāmbike, Nīlāmbike, Akkanāgamma, Āydakki Lakkamma, Mōḷige Mahādēvi, Haḍapada Liṅgamma, Kētaladēvi, Sūle Saṅkavva, Duggaḷe.
- **Other vacanakāras:** Dēvara Dāsimayya, Āydakki Mārayya, Mōḷige Mārayya, Haḍapada Appaṇṇa, Haraḷayya, Madhuvarasa, Uriliṅgadēva, Uriliṅgapeddi, Ēkānta Rāmayya, Mādāra Cennayya and others.
- **Harihara:** tch:harihara-kannada, plus 3 ragaḷes and Girijākalyāṇa.
- **Cāmarasa:** tch:camarasa, src:prabhulingalile (plus Sanskrit and Tamil versions).
- **Pañcācāryas:** tch:renukacarya, tch:marularadhya, tch:ekoramaradhya, tch:panditaradhya, tch:visvaradhya, tch:daruka; cpt:pancacarya-parampara; both origin accounts in dsp:virasaiva-origins.
- **Vacana corpus:** src:vacana-sahitya plus 14 author collections; src:satsthala-jnana-saramrta.
- **Śūnyasampādane:** src:sunyasampadane, 4 redactions and 4 compilers, 7 chapter-level teachings.
- **SSM:** src:siddhantasikhamani, src:tattvapradipika-maritontadarya, 122 teachings, tch:sivayogi-sivacarya.
- **Śrīkarabhāṣya:** referenced (U16 owns it).
- **Basava Purāṇa:** src:basava-purana-palkuriki (Telugu), plus the Kannada (Bhīmakavi) and Sanskrit versions.
- **Six stages (ṣaṭsthala):** cpt:satsthala and the six stage terms; teachings are tagged pth:virasaiva-satsthala. New: pth:siddhantasikhamani-101-sthalas (101 stages; the soul-side stages are banded).
- **Guru–liṅga–jaṅgama:** cpt:guru-linga-jangama.
- **Aṣṭāvaraṇa and pañcācāra:** cpt:astavarana, cpt:pancacara, with their terms.
- **Three liṅgas:** cpt:trividha-linga; trm:istalinga, trm:pranalinga, trm:bhavalinga, trm:trptilinga.
- **The liṅga worn on the body:** prc:linga-dharana, prc:istalinga-puja.
- **Kāyaka and dāsōha:** cpt/prc:kayaka, cpt/prc:dasoha.
- **Śūnya:** cpt:sunya-allama, trm:sunya, trm:bayalu.
- **Critiques of caste, temple, Veda and pollution:** 4 cpt entries plus dsp:virasaiva-caste-and-pollution, dsp:virasaiva-sthavara-jangama, dsp:virasaiva-veda-agama-authority.
- **Women's equality:** cpt:virasaiva-women-equality.
- **Disputes (10):** the three above, plus dsp:virasaiva-origins, dsp:lingayata-hindu-identity (queued; no side taken), dsp:dasoham-soham, dsp:allama-goraksa, dsp:allama-siddharama-works, dsp:ekanta-ramayya-jainas, dsp:rv-9-83-1-pavitra.
- **Kālāmukha transition:** brw:kalamukha-to-virasaiva (scholarly hypothesis).
- **Section D:** cpt entries for self, mind, consciousness, energy anatomy, guṇas, the three malas, karma and liberation, cosmology, pañcākṣara, vacana speech, liṅgaikya and siddhis.
- **Recent (recent: true):** Hānagal Kumārasvāmi, Śivakumāra Svāmi, Halakatti, Siddappārādhya.

## Corrections to the task's list
- The second stage is māheśvara; "maheśa" is kept as an alias only.
- The SSM's third liṅga is tṛptiliṅga. Bhāvaliṅga is the vacana name; in the SSM it is a liṅga-sthala (15.37–44).
- Mantragōpya is commonly ascribed to Akka Mahādēvi; attribution to Cennabasava is doubtful.
- "Kāyakavē kailāsa" is popularly attributed to Basava, but the vacana recalled is Āydakki Mārayya's.
- The SSM is a practice and six-stage scripture, not philosophy only, so this unit created it. Reṇuka is also called Revaṇa; his emergence at Kollipāki is verified in the text.
- The Śūnyasampādane is recorded with 4 named redactions; some accounts say 5.
- The SSM has a same-jāti eating rule (9.29) and a twofold varṇāśrama ordering (10.34–36) alongside its equality statements; both are recorded.
- The Kālāmukha link is recorded as a borrowing, not a dispute.

## 2. Least sure
- All vacana incipits and paraphrases, especially the `v-` keys; the reference "Speaking of Śiva no. 820" is low confidence.
- The Śūnyasampādane's chapter-level teachings; tea:sunyasampadane:the-void is a thematic summary.
- The minor vacanakāras' signature names (aṅkita) and lives.
- The seats and emergence liṅgas of the ācāryas other than Reṇuka.
- Māyidēva's Anubhavasūtra and the Śivayogapradīpikā: existence and authorship.
- The contents of the Karaṇahasuge, Mantragōpya, Yōgāṅga Trividhi, Śivatattvasāra, Vṛṣādhipa Śataka, Siṅgirāja's work, and the Tamil Pirapuliṅkalīlai.
- Dates: Basava, Pālkuriki, the SSM (12th–15th c.), Maritoṇṭadārya, the Śūnyasampādane redactions.
- Later manual schemes: the six liṅgas, six bhaktis, six śaktis, three aṅgas, the pañcasūtaka and aṣṭamada lists.
- The Ārādhya sub-lineage (thin).
- The 2017–18 details of the identity dispute, and the Vaiṣṇava side's texts in the RV 9.83.1 dispute.
- prc:istalinga-drsti and prc:lingaikya-burial rest on general knowledge rather than a text.

## 3. Gaps
- Specific vacanas of Cennabasava, Siddharāma, Cauḍayya, Mācayya, Candayya, Satyakka, Nīlāmbike and other women; Toṇṭada Siddhaliṅga; Ṣaṇmukhasvāmi.
- Vacana-edition numbering, which is needed to fix vacana locators.
- Not created (unsure of details): the 15th-c. sthala anthologies (Mahāliṅgadēva, Jakkaṇārya) and Miśrārpaṇa.
- SSM: most of chapters 16–20 and all of chapter 21 are not extracted.
- The Tattvapradīpikā's own teachings; the Vīracūḍāmaṇi.
- Śrīkarabhāṣya teachings (U16).
- The hostile Jain account of Bijjala.
- The four states of consciousness were not found in the passages read.
- Telugu and Tamil Vīraśaiva literature beyond Pālkuriki and Śivaprakāśar.
- Child initiation, funeral rites, and the gotra/sūtra of the five pīṭhas.

## 4. Out of reach
- Palm-leaf vacana bundles and maṭha manuscripts.
- Oral initiatory instruction (the whispered mantra and nyāsa, SSM 6.21; liṅga-yoga and breath instruction deferred to the guru).
- The oral lineages of the Virakta and Pañcapīṭha maṭhas.
- Copyrighted translations (Ramanujan; Bhoosnurmath and Menezes) — referenced only.
- SSM 6.27, on the fall of the liṅga: restricted — the statement only, no original.
