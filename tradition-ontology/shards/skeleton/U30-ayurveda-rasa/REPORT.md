# U30-ayurveda-rasa — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent, which cannot write report files in this harness; saved verbatim by the orchestrator.)_

**Method.** All entries come from model knowledge and stay at level `skeleton`. Verse numbers and wording were checked read-only against local e-texts in `sources_raw/`:
- **DCS corpus** (verse = the e-text's sentence counter):
  - Caraka Saṃhitā: Sū 1–30, Ni, Vi, Śā, In; Ci 1–5.
  - Suśruta Saṃhitā.
  - Aṣṭāṅgahṛdaya.
  - Rasārṇava, Rasahṛdayatantra, Rasaratnasamuccaya, Rasaratnākara.
  - Sarvadarśanasaṃgraha, Raseśvara chapter.
  - The opening of the Āyurvedadīpikā.
- **Devanāgarī e-texts in raw_etexts:** only the passages cited were looked up:
  - Caraka Ci 15.
  - Mādhava Nidāna 1.
  - Śārṅgadhara Pūrva 3 and 5.
  - Bhāvaprakāśa Pūrva 1.
  - Bhela Ci 8.

`original` wording is given only for verses read in those files (71 teachings). Teaching refs use sthāna + chapter.verse, e.g. `tea:caraka-samhita:su.1.41` and `sa.1.137-139`. For Caraka Ci 1 the form is `ci.1.4.30-35` (chapter.pāda.verse).

**Restricted content.** Nothing restricted is recorded beyond summary and the texts' own warnings (`restricted: true`, 68 entries). This covers:
- mercury and its processing;
- metal and mineral calxes;
- the eighteen saṃskāras, named only by count;
- dehavedha and lohavedha;
- breath-holding in the Rasārṇava;
- bloodletting;
- the hut-entering rasāyana, flagged because its regimen includes seclusion, purgation and metal or gem formulations;
- the making of the rasaliṅga.

The quantities and procedures that follow the warning verses (e.g. Rasaratnākara 1.31ff, RRS 11.26ff, RRS 6.17) were deliberately omitted.

## Corrections to the task's list
1. **Kapha subtypes.** Suśruta (Sū 21.14) gives only the functions of the five kaphas. The names (avalambaka, kledaka, bodhaka, tarpaka, śleṣaka) come from Vāgbhaṭa (AHS Sū 12.15-18).
2. **Rañjaka pitta.** Suśruta places it in the liver and spleen (Sū 21.10); Vāgbhaṭa places it in the stomach (AHS Sū 12.13).
3. **Para and apara ojas.** Caraka says only "the seat of the supreme (para) ojas" (Sū 30.7). "Apara ojas" is the commentators' gloss (Cakrapāṇi, recalled), and is marked as such.
4. **"Ojas, tejas and prāṇa".** These are not a doctrinal triad in the classical texts I checked. Ca Ci 15.3 lists ojas, tejas, the fires and the prāṇas among the things that depend on agni.
5. **The three supports.** Caraka's words are āhāra, svapna and brahmacarya (Sū 11.35); Vāgbhaṭa has śayana (AHS Sū 7.52).
6. **"Ācāra-rasāyana".** This is the later name. The texts say "nitya-rasāyana" (Ca Ci 1.4.34; AHS Utt 39.179).
7. **"The tenfold examination".** Caraka has two different lists of ten:
   - the ten things to be examined before acting (Vi 8.84);
   - the tenfold examination of the patient (Vi 8.94).
8. **Thirteen agnis.** The count is later. Ca Ci 15.13-15 gives the parts: the belly-fire, five element-fires and seven tissue-fires.
9. **Caraka's structure** is confirmed by Sū 30.33: 120 chapters (Sū 30, Ni 8, Vi 8, Śā 8, In 12, Ci 30, Ka 12, Si 12).
   - Dṛḍhabala supplied 17 Cikitsā chapters plus the Kalpa and Siddhi sections (Si 12.38-40).
   - The DCS e-text reads "ṣaḍviṃśatā" (26) for the tantrayuktis, but lists 36; standard editions read 36.
10. **Suśruta's structure:** 120 chapters in five sthānas plus a 66-chapter Uttaratantra (186 in all, Su Sū 1.39-40). He counts 32 tantrayuktis (Utt 65.3).
11. **Suśruta's health definition** is Su Sū 15.41 in the DCS e-text (15.48 in some printed editions).
12. **Two further sources on the self.** Caraka also treats self and liberation in Śā 5, besides Śā 1: loka-puruṣa, the path at 5.12, and nirvāṇa. Suśruta Śā 1.16 says the selves are eternal but not all-pervading — a real difference from Caraka.
13. **Ātreya's other name.** Caraka's colophon verse Sū 11.65 names him "Kṛṣṇātreya".
14. **Transmission variants** are recorded side by side:
    - Caraka: Bharadvāja goes to Indra.
    - AHS: Indra teaches Atri's son.
    - Bhāvaprakāśa: Ātreya goes to Indra himself, and the Bharadvāja story is also told.
    - Suśruta: Indra teaches Dhanvantari.
15. **Rasaratnasamuccaya authorship.** Its author calls himself "son of Siṃhagupta" (1.9), as the Aṣṭāṅgahṛdaya's author does. The attribution to Vāgbhaṭa is kept as doubtful.
16. **The Sarvadarśanasaṃgraha** names eighteen processings of mercury (Raseśvara 19-21); the names are not reproduced here.

## Decisions (for DECISIONS.md)
- **Family "shared"** for lin:ayurveda and lin:rasa-sastra:
  - Āyurveda calls itself an upāṅga of the Atharvaveda, but Buddhist authors (the Aṣṭāṅgahṛdaya, Ravigupta, the Bower MS) and Jain authors (Ugrāditya) wrote within it.
  - Rasa is mainly Śaiva, but works are ascribed to Nāgārjuna, and the Jain Merutuṅga commented on the Rasādhyāya.
- **Sub-lineages added:** lin:atreya-sampradaya, lin:dhanvantari-sampradaya and lin:kerala-astavaidya (low confidence).
- **Separate teacher ids kept:**
  - tch:nagarjuna-siddha, apart from tch:nagarjuna;
  - tch:govinda-rasahrdaya, apart from tch:govinda-bhagavatpada;
  - tch:vyadi-rasasiddha, apart from tch:vyadi;
  - tch:kumarasiras-bharadvaja, apart from tch:bharadvaja;
  - tch:sarngadhara-vaidya, apart from tch:sarngadhara-anthologist.
- **Registry and shared ids reused:** tch:caraka, tch:susruta, tch:vagbhata (RRS attribution "doubtful"), tch:hemadri, tch:dhanvantari, tch:bharadvaja, tch:brahma, tch:indra, tch:nityanatha, tch:carpatanatha.
- **Homonyms given an Āyurveda/Rasa definition, not a new id:** trm:dosa, trm:srotas, trm:mala, trm:rasa, trm:kancuka, trm:bhasma, trm:graha, trm:vada, trm:visarga-kala.
- **Id collision avoided.** Śamana was filed as trm:samsamana (saṃśamana) because its slug would collide with samāna (trm:samana).

## 1. Coverage checklist (A11 Āyurveda, Rasa Śāstra; parts of D, E, F, G, C)

**Lineages**
- lin:ayurveda
- lin:rasa-sastra
- sub-lineages: lin:atreya-sampradaya, lin:dhanvantari-sampradaya, lin:kerala-astavaidya
- ult:ayurveda, noting that Āyurveda is a science of life and not a soteriology
- ult:rasa-sastra

**Texts**
- **Caraka:** src:caraka-samhita
  - 160 teachings, across all eight sthānas.
  - Tradition's transmission account: tea:caraka-samhita:su.1.3-5, su.1.17-23, su.1.30-33; cpt:descent-of-ayurveda.
- **Suśruta:** src:susruta-samhita, 23 teachings: su.1.3-5 through utt.65.3.
- **Vāgbhaṭa:** src:astanga-hrdaya (25 teachings), src:astanga-sangraha.
- **Other compendia:**
  - src:madhava-nidana (tea: 1.1-3, 1.4, 1.5-10)
  - src:sarngadhara-samhita (tea: purva.3.1-5, purva.5.49-52)
  - src:bhavaprakasa (4 teachings)
  - src:kasyapa-samhita, src:bhela-samhita (tea:bhela-samhita:ci.8), src:harita-samhita
- **Lost tantras:** src:agnivesa-tantra, src:jatukarna-samhita, src:parasara-samhita-ayurveda, src:ksarapani-samhita.
- **Commentaries:**
  - on Caraka: src:ayurveda-dipika (Cakrapāṇi), src:nirantarapadavyakhya, src:carakanyasa, src:carakatattvapradipika, src:jalpakalpataru (recent)
  - on Suśruta: src:nibandha-sangraha (Ḍalhaṇa), src:bhanumati, src:nyayacandrika-gayadasa
  - on Vāgbhaṭa: src:sarvangasundara (Aruṇadatta), src:ayurveda-rasayana (Hemādri), src:sasilekha
  - on the others: src:madhukosa, src:dipika-adhamalla, src:gudharthadipika-kasirama
- **Later works:** src:cakradatta, src:siddhayoga-vrnda, src:vangasena, src:gadanigraha, src:cikitsakalika, src:yogaratnakara, src:bhaisajyaratnavali, src:vaidyajivana, src:ayurveda-prakasa.
- **Nighaṇṭus:** src:dhanvantari-nighantu, src:raja-nighantu, src:madanapala-nighantu, src:kaiyadeva-nighantu, src:astanga-nighantu.
- **Specialist and other works:**
  - src:nadi-pariksa, src:tantrayuktivicara
  - src:navanitaka, src:siddhasara, src:kalyanakaraka
  - veterinary and plant medicine: src:hastyayurveda, src:asvavaidyaka, src:vrksayurveda

**Teachers**
- **The divine descent:** tch:brahma, tch:daksa-prajapati, tch:asvins, tch:indra.
- **Founders:** tch:bharadvaja, tch:atreya-punarvasu.
- **Ātreya's six disciples:** tch:agnivesa, tch:bhela, tch:jatukarna, tch:parasara-ayurveda, tch:harita-ayurveda, tch:ksarapani.
- **The Caraka line:** tch:caraka, tch:drdhabala.
- **The Suśruta line:**
  - tch:dhanvantari (Divodāsa), tch:susruta
  - fellow students: tch:aupadhenava, tch:vaitarana, tch:aurabhra, tch:pauskalavata, tch:karavirya, tch:gopuraraksita
- **Children's medicine and redactors:** tch:marica-kasyapa, tch:vrddha-jivaka, tch:vatsya, tch:nagarjuna-siddha.
- **Speakers in Caraka's assemblies (18):** Kumāraśiras Bharadvāja, Kāṅkāyana, Baḍiśa, Vāyorvida, Marīci, Kāpya, Bhadrakāpya, Kuśa Sāṅkṛtyāyana, Pārīkṣi Maudgalya, Śaraloman, Hiraṇyākṣa, Bhikṣu Ātreya, Vāmaka, Maitreya, Nimi, Śākunteya, Pūrṇākṣa, Bhadraśaunaka.
- **Required commentators:** tch:cakrapanidatta, tch:dalhana, tch:arunadatta, tch:hemadri.
- **Other commentators and later authors:** tch:vagbhata, tch:madhavakara, tch:sarngadhara-vaidya, tch:bhavamisra, tch:gayadasa, tch:jejjata, tch:indu-sasilekha, tch:vijayaraksita, tch:srikanthadatta, tch:sivadasa-sena, tch:gangadhara-kaviratna (recent), and others.
- **Rasa Śāstra:**
  - tch:siva (Bhairava), tch:parvati
  - tch:govinda-rasahrdaya, tch:nityanatha, tch:carpatanatha, tch:vyadi-rasasiddha, tch:sarvajna-ramesvara
  - tch:somadeva-rasa, tch:yasodhara-rasa, tch:salinatha, tch:dhundhukanatha, tch:gopalakrsna-rasa, tch:mantharabhairava
  - tch:kankalayogin, tch:merutunga, tch:camunda-rasa, tch:cudamani-misra, tch:kakacandisvara
  - tch:sadananda-sarma (recent)

**Concepts required by the brief**
- **Doṣas:**
  - cpt:three-dosas and terms trm:vata, trm:pitta, trm:kapha
  - the five vāyus: cpt:five-vayus (lineage contribution); terms trm:prana, trm:udana, trm:samana, trm:vyana, trm:apana
  - cpt:five-pittas, with a trm: entry for each of pācaka, rañjaka, sādhaka, ālocaka, bhrājaka
  - cpt:five-kaphas, with a trm: entry for each of kledaka, avalambaka, bodhaka, tarpaka, śleṣaka
- **Tissues and wastes:** cpt:seven-dhatus with 7 dhātu terms; trm:upadhatu; cpt:malas, trm:purisa, trm:mutra, trm:sveda.
- **Fires:** cpt:agnis, trm:jatharagni, trm:bhutagni, trm:dhatvagni.
- **Āma, ojas, tejas, prāṇa:**
  - cpt:ama, trm:ama
  - cpt:ojas, trm:ojas (para/apara noted)
  - trm:tejas
  - trm:prana, cpt:prana-in-ayurveda
- **Channels:** cpt:srotas, trm:srotas.
- **Constitution:** cpt:prakrti-constitution, trm:prakrti, trm:vikrti.
- **Supports and regimen:**
  - cpt:three-upastambhas
  - cpt:dinacarya, cpt:rtucarya, cpt:adana-visarga
  - cpt:sadvrtta, cpt:ten-sinful-acts
- **Rejuvenation and virility:** cpt:rasayana, cpt:acara-rasayana, cpt:vajikarana.
- **Caraka's psychology:**
  - cpt:three-gunas (lineage contribution)
  - cpt:sixteen-sattvas (Ca Śā 4.36-40; Su Śā 4.81-98)
  - cpt:manasa-dosas, cpt:prajnaparadha
  - cpt:sattvavajaya, cpt:three-kinds-of-therapy (daiva-vyapāśraya)
- **The eight branches:** cpt:eight-branches; bhūtavidyā in summary only (cpt:bhutavidya-grahas).
- **Desires and rebirth:** cpt:three-esanas, cpt:rebirth-arguments-caraka (Sū 11).
- **Self, yoga and mokṣa:** cpt:self-in-caraka, cpt:yoga-in-caraka, cpt:moksa-in-caraka, cpt:naisthiki-cikitsa, cpt:vedana-and-its-cessation.
- **Treatment and pharmacology:**
  - cpt:four-pillars-of-treatment, cpt:tenfold-examination
  - cpt:six-tastes, cpt:twenty-gunas, cpt:rasa-guna-virya-vipaka-prabhava
  - diet: prc:ahara-vidhi, cpt:eight-factors-of-diet, cpt:pathya, obs:viruddha-ahara

**Section-D items for each lineage**
- **Ultimate:** ult:*.
- **Consciousness and states:** cpt:nidra-in-ayurveda, cpt:seven-kinds-of-dream, cpt:yoga-in-caraka.
- **Self:** cpt:self-in-caraka, cpt:self-in-susruta, cpt:purusa-in-ayurveda, cpt:rasi-purusa, cpt:tripod-of-life.
- **Mind:** cpt:manas-in-ayurveda, cpt:sattva-bala, cpt:eight-causes-of-smrti.
- **Body and energy:** cpt:ten-seats-of-prana, cpt:marma (reference to U58), cpt:hrdaya-in-ayurveda.
- **Matter:** cpt:five-elements (contribution), cpt:pancabhautika-dravya, cpt:six-padarthas-in-ayurveda, cpt:samanya-visesa-principle.
- **Cosmology and time:** cpt:loka-purusa-samya, cpt:yuga-decline-of-health, cpt:janapadoddhvamsa.
- **Karma:** cpt:daiva-purusakara, cpt:six-factors-of-embryo.
- **Death:** cpt:kala-akala-mrtyu, cpt:arista.
- **Powers:** cpt:eight-yogic-powers-caraka.
- **Teacher and transmission:** cpt:teacher-and-student-ayurveda, cpt:caraka-as-sesa.
- **Sound and language:** cpt:tantrayukti, cpt:sambhasa-vada, cpt:four-pramanas-caraka, cpt:eternality-of-ayurveda.

**Rasa Śāstra (restricted)**
- **Texts:** src:rasarnava (8 teachings), src:rasaratnakara (5), src:rasaratnasamuccaya (6), src:rasahrdayatantra (6), src:rasendracudamani, plus 12 further rasa texts.
- **The Raseśvara-darśana:** cpt:rasesvara-darsana, from src:sarvadarsanasangraha (10 teachings).
- **Doctrine:** cpt:jivanmukti-rasa, cpt:pinda-sthairya, cpt:mercury-as-siva-seed, cpt:divya-deha, cpt:dehavedha-lohavedha.
- **Processing and warnings:** cpt:eighteen-samskaras; cpt:rasa-dosas, obs:rasa-dosas, obs:asuddha-rasa-dravya (the texts' warnings).
- **Worship and transmission:** cpt:rasalinga, cpt:rasa-guru-and-disciple, cpt:rasa-and-pavana, cpt:twenty-seven-rasasiddhas, cpt:rasasala.
- **Practices, all restricted:** prc:rasa-samskara, prc:lohavedha, prc:dehavedha, prc:bhasma-rasayana, prc:rasalinga-puja, prc:rasa-diksa, prc:pavana-dharana-rasa.

**Practices (E)**
- **Daily and seasonal routine:** prc:dinacarya, prc:rtucarya, prc:rtu-sodhana.
- **Body care and diet:** prc:abhyanga, prc:vyayama, prc:ahara-vidhi, prc:vega-adharana, prc:three-upastambhas, prc:nidra-vidhi, prc:brahmacarya (contribution).
- **Conduct:** prc:sadvrtta, prc:acara-rasayana.
- **Rejuvenation and virility:** prc:rasayana, prc:kutipravesika-rasayana (restricted), prc:medhya-rasayana, prc:vajikarana.
- **Cleansing:** prc:pancakarma, prc:raktamoksana (restricted).
- **Daily minor practices:** prc:anjana, prc:nasya-daily, prc:gandusa.
- **Mind and ritual:** prc:sattvavajaya, prc:daivavyapasraya, prc:caraka-moksa-sadhana, prc:vaidya-diksa.

**Obstacles**
- **Doṣa imbalances (category dosa-imbalance):** obs:vata-prakopa, obs:pitta-prakopa, obs:kapha-prakopa, obs:sannipata, obs:agni-dusti.
- **Others:**
  - obs:ama, obs:ojas-ksaya, obs:srotodusti
  - obs:vega-vidharana, obs:dharaniya-vegas
  - obs:prajnaparadha, obs:asatmyendriyartha-samyoga, obs:manasa-dosas
  - obs:upadha, obs:ahankara-and-attachment-caraka
  - obs:grahabadha, obs:adharma-janapadoddhvamsa, obs:akala-mrtyu, obs:svabhavika-roga
  - obs:viruddha-ahara, obs:rasa-dosas, obs:asuddha-rasa-dravya

**Path maps (F)**
- pth:caraka-moksa-path (9 stages, B0–B7)
- pth:rasesvara-path (7 stages, B0–B8; restricted)

**Disputes (G), all internal to Āyurveda or Rasa**
- **Reconciled or partially reconciled (P2):**
  - dsp:origin-of-person-and-disease (Ca Sū 25)
  - dsp:nature-of-vayu (Sū 12)
  - dsp:number-of-tastes (Sū 26)
  - dsp:which-limb-forms-first (Śā 6.21)
  - dsp:origin-of-embryo (Śā 3)
  - dsp:is-medicine-efficacious (Sū 10; AHS Utt 40)
  - dsp:is-lifespan-fixed (Vi 3; Śā 6)
  - dsp:is-blood-a-fourth-dosa (Su Sū 21)
  - dsp:is-ayurveda-eternal (Sū 30.27)
- **Queued:**
  - dsp:is-there-rebirth-caraka (against the nāstikas; reported by an opponent)
  - dsp:is-the-self-all-pervading (Caraka against Suśruta)
  - dsp:authority-of-the-samhitas (AHS Utt 40)
  - dsp:fish-with-milk (Sū 26.83-84)
  - dsp:how-dhatus-are-nourished (low confidence)
  - dsp:is-bodily-immortality-required-for-liberation (Rasa against Advaita and Caraka)
- **Referenced only (owned by U50):** dsp:is-there-a-self, dsp:number-of-pramanas.

**Borrowings (C)**
- brw:ayurveda-to-sowa-rigpa
- brw:ayurveda-siddha-medicine
- brw:ayurveda-to-hatha-yoga
- brw:rasa-sastra-hatha-yoga
- brw:buddhist-ethics-to-ayurveda
- brw:samkhya-ayurveda-non-perception
- brw:yoga-ayurveda-caraka
- brw:kaula-to-rasa-sastra
- brw:rasa-sastra-to-ayurveda
- brw:ayurveda-jain-kalyanakaraka
- brw:natha-rasa-sastra

brw:samkhya-ayurveda, brw:vaisesika-to-ayurveda and brw:ayurveda-nyaya-vada already exist in U09 and U11 and are not duplicated.

**Phenomenology:** 15 items. Examples:
- phn:caraka-eight-yogic-powers
- phn:caraka-purified-mind-lamp
- phn:jatismara
- phn:arista-signs
- phn:rasa-conscious-light
- phn:signs-of-restored-balance

## 2. Least-sure items (check these first)
- **Teachers:**
  - tch:vatsya (the Kāśyapa redactor)
  - Indu as Vāgbhaṭa's pupil
  - tch:govinda-dasa-sena (date and authorship)
  - tch:dhundhukanatha, tch:gopalakrsna-rasa
  - tch:mantharabhairava as author of the Ānandakanda
  - tch:kankalayogin, tch:merutunga, tch:camunda-rasa, tch:cudamani-misra, tch:madhava-upadhyaya
  - tch:nilamegha, tch:jayadatta-suri, tch:surapala, tch:madanapala (date), tch:kaiyadeva
- **Sources:**
  - src:rasopanisad, src:kakacandisvarimata, src:rasendramangala
  - src:carakanyasa, src:nirantarapadavyakhya (extent)
  - src:astanga-nighantu (Vāhaṭa), src:nadi-pariksa (ascribed to Kaṇāda), src:tantrayuktivicara
  - src:bhaisajyaratnavali (date), src:siddhasara and src:navanitaka (details)
  - the chapter counts of the Aṣṭāṅgasaṅgraha
- **Recalled claims, not checked:**
  - Suśruta as a son of Viśvāmitra.
  - The Chinese Caraka–Kaniṣka story.
  - The Tibetan rendering "tsho ba'i rig pa".
  - The claim that commentators cite tantras of Aupadhenava, Aurabhra and Pauṣkalāvata.
  - Kṛṣṇātreya as a separate śālākya authority.
- **dsp:how-dhatus-are-nourished:** the three commentarial maxims are recalled only.
- **Su Śā 1.16:** the sentence on non-all-pervading selves is compressed. My reading follows Ḍalhaṇa as I recall him and needs checking against the commentary.
- **Bhāvaprakāśa and Śārṅgadhara** verse numbers follow the local e-text's numbering.
- **Bhela Ci 8** is cited at chapter level only.

## 3. Gaps (belong here but not created responsibly)
- **Kerala Aṣṭavaidya:** the names of the families, their texts (e.g. Sahasrayoga) and their commentaries on the Aṣṭāṅgahṛdaya.
- **Kāśyapa Saṃhitā:** its own teachings (the Lehādhyāya, the Revatī-kalpa), which I could not verify. Gold preparations for infants are restricted in any case.
- **Aṣṭāṅgasaṅgraha:** its teachings; the DCS has only three chapters.
- **Suśruta:** the Cikitsā chapters on rasāyana (Ci 28-30, including soma) and vājīkaraṇa (Ci 26); Utt 64; the chapters on leeches and venesection. The refs given for these are recalled.
- **Caraka chapters outside the DCS portion:** Ci 6-21 and 24-29, Kalpa, Siddhi 1-11, and Sū 22 (laṅghana and bṛṃhaṇa). No teachings were created for them.
- **Rasa texts:** the paṭalas of the Rasārṇava on initiation, the rasaśālā and dehavedha (restricted in any case, so summary only); the qualifications of the rasa physician in the Rasendracūḍāmaṇi.
- **Modern (post-1800) Āyurveda:** editors and teachers such as Gaṇanāth Sen and Yādavji Trikamji, and the institutions. Only Gaṅgādhara Kaviratna and Sadānanda Śarmā were added.
- **Content of specialist traditions:** Jain Āyurveda (Kalyāṇakāraka), Buddhist medical texts, veterinary medicine and Vṛkṣāyurveda. Sources are listed but not their teachings.
- **Siddha medicine** is left to U22 and **marma in depth** to U58; both are referenced only.

## 4. Out of reach
- **Oral and hereditary lineages:** the Aṣṭavaidya family transmissions, the paramparā vaidyas, and rasa-guru lineages. The rasa lineages are secret by the texts' own rule (Rasārṇava 1.58).
- **Undigitized manuscripts:** the lost tantras of Ātreya's other disciples; the complete Kāśyapa and Bhela manuscripts.
- **Restricted material withheld:** all procedures, quantities, apparatus and formulations of Rasa Śāstra, bhasma preparation, kuṭīprāveśika regimens and bloodletting.
