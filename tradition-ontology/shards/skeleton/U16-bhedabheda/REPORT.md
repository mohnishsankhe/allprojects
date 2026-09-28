# U16-bhedabheda — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Validator: 0 errors. The only warning is that REPORT.md is missing, which saving this file resolves.
Counts: sources 121 · teachers 80 · teachings 155 · terms 128 · concepts 75 · practices 25 · obstacles 19 · disputes 14 · paths 4 · phenomenology 10 · borrowings 10 · lineages 5 · ultimate 5 · interpretation_log 16.
Generators are in `_gen/` (h.py, then p01–p21), and every part can be re-run.

## 1. Coverage checklist (A6 and related D/E/F/G items)

### Lineages and ult views
- Bhedābheda: lin:bhedabheda, ult:bhedabheda
- Nimbārka: lin:dvaitadvaita, ult:dvaitadvaita
- Vallabha: lin:pustimarga, ult:pustimarga
- Gauḍīya: lin:gaudiya-vaisnava, ult:gaudiya-vaisnava
- Śrīkaṇṭha: lin:siva-visistadvaita, ult:siva-visistadvaita

### Bhāskara and the early bhedābheda teachers
- Texts: src:brahma-sutra-bhasya-bhaskara; src:gita-bhasya-bhaskara (low).
- Teachings: tea:brahma-sutra-bhasya-bhaskara:1.1.1, 1.4.25, 1.4.26, 2.1.14, 2.3.43, 4.1.
- Aupādhika bhedābheda: cpt:aupadhika-bhedabheda, trm:aupadhika-bhedabheda, trm:upadhi, obs:upadhi-bondage.
- Jñāna-karma-samuccaya: cpt:, trm:, prc: and dsp:jnana-karma-samuccaya.
- The charge that māyāvāda is Buddhist: tea:…:1.4.25, which references dsp:advaita-crypto-buddhism (owned by U50).
- Denial of jīvanmukti: dsp:jivanmukti.
- Yādavaprakāśa: tch:yadavaprakasa, src:brahma-sutra-bhasya-yadavaprakasa (lost), src:yatidharmasamuccaya, src:vaijayanti.
- Bhartṛprapañca: tch:bhartrprapanca, src:brhadaranyaka-bhasya-bhartrprapanca (lost), plus 2 teachings flagged reported_by_opponent.
- Also added: tch:asmarathya, tch:audulomi, and Vijñānabhikṣu's src:vijnanamrta-bhasya (avibhāga).

### Nimbārka school
- Nimbārka: tch:nimbarka; src:vedanta-parijata-saurabha; src:dasasloki (all 10 verses as teachings); src:krsnastavaraja.
- Śrīnivāsa: tch:srinivasa-nimbarka, src:vedanta-kaustubha.
- Keśava Kāśmīrin: tch:kesava-kasmirin, src:kaustubha-prabha, src:tattvaprakasika-kesava-kasmirin, src:kramadipika.
- Also added: Śrī Bhaṭṭa, Harivyāsadeva, Puruṣottamācārya, Devācārya, Paraśurāma Devācārya and Mādhava Mukunda, with their texts.
- Svābhāvika bhedābheda: cpt:svabhavika-bhedabheda; tea:vedanta-parijata-saurabha:3.2.27.
- Rādhā–Kṛṣṇa: tea:dasasloki:4 and 5, prc:yugala-upasana, trm:yugala.
- The five means: cpt:five-means-nimbarka, prc:prapatti, prc:gurupasatti.
- Arthapañcaka: cpt:arthapancaka-nimbarka.
- The three realities: cpt:three-realities-nimbarka.

### Vallabha and the Puṣṭimārga
- Main works: src:anubhasya, src:tattvarthadipanibandha, src:subodhini-vallabha.
- Ṣoḍaśagrantha: src:sodasagrantha plus all 16 works as separate sources.
- Other works: src:madhurastaka, src:patravalambana, src:purusottama-sahasranama.
- Viṭṭhalanātha: tch:vitthalanatha, src:vidvanmandana, src:srngararasamandana.
- The aṣṭachāp: trm:astachap and all eight poets (tch:surdas created; its id is fixed in the registry). src:sursagar is contributed and gives both the tradition's and the scholarly account.
- Vārtā literature: src:caurasi-vaisnavan-ki-varta, src:do-sau-bavan-vaisnavan-ki-varta.
- Avikṛta-pariṇāma: cpt:avikrta-parinama, tea:anubhasya:1.4.26.
- Puṣṭi and maryādā: cpt:pusti-and-maryada, tea:bhagavata-purana:2.10.4.
- Brahmasambandha: cpt:brahmasambandha, prc:brahmasambandha-diksa, tea:siddhantarahasya:1 and 2-3, obs:pancavidha-dosa.
- Sevā: prc:pusti-seva, prc:astayama-seva, prc:samarpana, prc:haveli-kirtan.
- The three kinds of souls: cpt:three-kinds-of-souls-vallabha.
- Other concepts: cpt:nirodha, cpt:viruddha-dharmasraya, cpt:avirbhava-tirobhava, cpt:three-forms-of-brahman-vallabha.
- Path map: pth:vallabha-bhaktivardhini-stages.

### Gauḍīya
- Caitanya: tch:caitanya; src:siksastaka, with all 8 verses as teachings.
- Nityānanda, Advaita Ācārya, Gadādhara, Śrīvāsa and Haridāsa: teacher entries for each; cpt:panca-tattva.
- The Six Gosvāmīs: tch:rupa-gosvami, sanatana-gosvami, jiva-gosvami, raghunatha-dasa-gosvami, raghunatha-bhatta-gosvami, gopala-bhatta-gosvami.
- Texts:
  - src:bhaktirasamrtasindhu (about 25 teachings), src:ujjvalanilamani, src:laghubhagavatamrta, src:brhadbhagavatamrta, src:haribhaktivilasa.
  - src:sat-sandarbha plus its six parts: tattva-, bhagavat-, paramatma-, krsna-, bhakti- and priti-sandarbha. Also src:sarvasamvadini.
  - src:caitanya-caritamrta (about 24 teachings), src:caitanya-bhagavata.
  - src:govinda-bhasya; Baladeva's src:prameyaratnavali and src:gita-bhusana.
  - Viśvanātha Cakravartin's works: src:madhurya-kadambini, src:raga-vartma-candrika, src:sarartha-darsini and others.
  - Also src:upadesamrta (7 teachings), src:brahma-samhita (6 teachings), Kavikarṇapūra's works, Narottama's works and src:bhakti-ratnakara.
- Acintya-bhedābheda: cpt:acintya-bhedabheda, tea:sarvasamvadini:on-paramatma-sandarbha, tea:caitanya-caritamrta:2.20.108.
- Brahman–Paramātman–Bhagavān (BhP 1.2.11): contributions to cpt:brahman-paramatman-bhagavan (owned by U07). References U07's tea:bhagavata-purana:1.2.11 and 1.3.28.
- The three śaktis: cpt:three-saktis-of-visnu (contribution), cpt:hladini-sandhini-samvit, tea:visnu-purana:1.12.69.
- Rasas:
  - five primary: cpt:five-devotional-rasas
  - seven secondary: cpt:seven-secondary-rasas
  - components of rasa and sthāyibhāva: cpt:bhakti-rasa-components, trm:sthayibhava
  - cpt:eight-sattvika-bhavas, cpt:thirty-three-vyabhicari-bhavas
- Vaidhī and rāgānugā bhakti: cpt:vaidhi-bhakti, cpt:raganuga-bhakti, prc:vaidhi-sadhana, prc:raganuga-sadhana.
- The 64 limbs: prc:sixty-four-limbs-of-sadhana-bhakti, prc:five-potent-limbs.
- Rūpa's stages (BRS 1.4.15–16): tea:bhaktirasamrtasindhu:1.4.15-16, which references pth:rupa-gosvami-bhakti-stages (owned by U51). Contributed terms for each of the nine stages. Also pth:madhurya-kadambini-stages.
- The mahāmantra and nāma-japa: prc:hare-krsna-mahamantra, prc:nama-japa, prc:nama-sankirtana, tea:kalisantarana-upanisad:text.
- The name: cpt:name-and-named-non-different, cpt:namabhasa.
- The ten offences: contribution to obs:nama-aparadha (owned by U07); obs:seva-aparadha.
- Mañjarī-bhāva (summary only): cpt:manjari-bhava, cpt:siddha-deha, prc:asta-kaliya-lila-smarana, trm:siddha-pranali.
- Other path maps: pth:ramananda-samvada-ladder, pth:ujjvalanilamani-prema-ladder.

### Śrīkaṇṭha
- tch:srikantha; src:srikantha-bhasya, with 4 teachings (1.1.2, 1.3.14, 2.2.38, 4.4.17).
- Appayya's works: src:sivarkamanidipika, src:sivadvaitanirnaya, src:ratnatrayapariksa, src:sivatattvaviveka.
- Concepts: cpt:siva-visistadvaita, cpt:dahara-siva, cpt:siva-samya, cpt:veda-agama-equality; practice prc:dahara-vidya.

### Vīraśaiva philosophy only (lin:virasaiva is owned by U20)
- src:srikarabhasya; src:siddhantasikhamani (contributed).
- cpt:sakti-visistadvaita; trm:sakti-visistadvaita and trm:linganga-samarasya (contributed).
- tch:sripati, using U20's id, which differs from the "tch:sripati-pandita" slug.

### Disputes
- With Advaita: dsp:gaudiya-critique-of-advaita (records the Sārvabhauma and Prakāśānanda debates), dsp:brahma-parinama-vada, dsp:jivanmukti, dsp:atomic-or-pervasive-self, dsp:prema-beyond-moksa, dsp:is-bhakti-a-rasa.
- Among the schools themselves: dsp:aupadhika-vs-svabhavika-bhedabheda, dsp:jnana-karma-samuccaya.
- Status of Rādhā: dsp:status-of-radha.
- Svakīyā vs parakīyā: dsp:svakiya-parakiya. This is recorded as a debate inside the Gauḍīya tradition (Rūpa and Viśvanātha vs Jīva), plus the Nimbārka view.
- Others: dsp:gaudiya-sampradaya-affiliation, dsp:srikantha-advaita-or-visistadvaita, dsp:authority-of-the-agamas, dsp:siddha-pranali-eligibility (recent).
- Reconciliation status:
  - Partially reconciled, with principle and objections recorded (5): jnana-karma-samuccaya, status-of-radha, is-bhakti-a-rasa, srikantha-advaita-or-visistadvaita, prema-beyond-moksa.
  - Queued, with RQ-U16-1 to RQ-U16-9 in `queue_ref` (9): aupadhika-vs-svabhavika-bhedabheda, brahma-parinama-vada, jivanmukti, svakiya-parakiya, gaudiya-critique-of-advaita, gaudiya-sampradaya-affiliation, atomic-or-pervasive-self, authority-of-the-agamas, siddha-pranali-eligibility.
  - The orchestrator should copy RQ-U16-1 to RQ-U16-9 into RECONCILE_QUEUE.md.

### Contributions to the D checklist
cpt:moksa, cpt:jivanmukti, cpt:last-thought, cpt:antahkarana, cpt:bhakti-by-gunas, cpt:tattva-counts-reconciled-bhagavata, cpt:kali-yuga-dharma, cpt:viraha-bhakti, cpt:avatara-doctrine, cpt:pati-pasu-pasa, cpt:linganga-samarasya; prc:puja, prc:kirtana, prc:ekadasi-vrata, prc:bhuta-suddhi.

### Corrections to the task list
- The Kalisantaraṇa gives the Hare Rāma half first; Gauḍīya practice usually begins with Hare Kṛṣṇa.
- The phrase "acintya-bhedābheda" comes from Jīva's Sarvasaṃvādinī (and the CC), not from the six Sandarbhas proper.
- Haribhaktivilāsa authorship is disputed: Gopāla Bhaṭṭa is named in the text and Sanātana wrote the commentary.
- The Aṇubhāṣya was completed by Viṭṭhalanātha.
- The svakīyā–parakīyā debate is chiefly inside the Gauḍīya tradition, not between schools.
- Viśvanātha is a teacher, not a text.
- Bhāskara's crypto-Buddhism phrase is well attested, but its commonly cited place (ad BS 1.4.25) is unconfirmed.

## 2. Least sure — check these first
- **Section-level references:** the Sandarbha "sections" (anuccheda numbers not given), Bhakti-sandarbha 273, the Mādhuryakādambinī showers, UN 1.21, and BRS 1.2.8, 1.2.187, 1.2.270-273, 1.2.292, 1.3/2.
- **Vallabha's short works:** approximate verse ranges for Siddhāntarahasya 4-8, Siddhāntamuktāvalī 3-6, Bhaktivardhinī 1-5, Sevāphala 1-3, and the "1ff" references for Puṣṭipravāhamaryādābheda, Nirodhalakṣaṇa and Sannyāsanirṇaya. Also the five-jointed avidyā and the 28 tattvas (both low confidence).
- **Bhāskara references:** 1.1.1, 2.1.14 and 4.1 are position-level recollections, not verified loci.
- **Bhartṛprapañca:** loci "bau-5.1.1" and "bau-intro".
- **Minor authors:** Nimbārka-school authors and works (Devācārya, Puruṣottamācārya, Mādhava Mukunda, Paraśurāma Devācārya, Kramadīpikā authorship, Śrutyantasuradruma). Later Śuddhādvaita authors (Giridhara, Bālakṛṣṇa Bhaṭṭa, Puruṣottama, Harirāy dates).
- **Doubtful titles:** Bhāskara's Gītā commentary, the Vaijayantī attribution, Ratnatrayaparīkṣā and Śivatattvaviveka.
- **Events and dates:** the Bengal (Murshidabad c. 1717) and Jaipur svakīyā/parakīyā hearings; Śrīpati's date; Śrīkaṇṭha's date.
- **Other uncertain items:** Kṛṣṇakarṇāmṛta 1.1 wording, CC 1.4.68, the full list of 64 limbs (only partly enumerated), the sevāparādha list, and Siddha Kṛṣṇadāsa Bābā.
- **Quoted Sanskrit:** `original` text is given only for verses recalled with high certainty (Śikṣāṣṭaka, BRS 1.1.11/1.1.17/1.4.15-16, Upadeśāmṛta 1-3/8, Brahma Saṃhitā 5.1, CC 2.19.151 and 2.20.108, TDN 1.7, SR 1, SM 2, Catuḥślokī 1, Madhurāṣṭaka 1, Daśaślokī 4, BRS 1.2.22/1.2.295/1.3.1/1.4.1, CC 1.17.21, Śikṣāṣṭaka 7). All still need checking against editions.
- **Invented or cross-unit ids that do not exist yet:** cpt:aprthak-siddhi (U14), cpt:nine-rasas-natyasastra (U31), src:kavyaprakasa (U31). Also tch:brahma, used as the "revealer" of the Brahma Saṃhitā.

## 3. Gaps (not created, to fill later)
- The full verse-by-verse list of the 64 limbs (BRS 1.2).
- Bhartṛprapañca's eight avasthās of Brahman.
- Yādavaprakāśa's doctrine as a teaching: the Vedārthasaṅgraha section numbers are unknown.
- Sundara Bhaṭṭa's Setukā and other Nimbārka sub-commentaries; the Nimbārka paramparā list beyond the main names.
- Most of Harirāy's works and the Śikṣāpatra; Nanddās's Bhaṃvargīt; Paramānandsāgar.
- The seven houses of Viṭṭhalanātha's sons, and their deities (nidhi), as entities.
- Vallabha's Pūrvamīmāṃsā-bhāṣya fragment and the Śikṣāślokī.
- Gauḍīya works not yet created: Jīva's Gopālatāpanī and Brahma Saṃhitā commentaries, Rūpa's Mathurāmāhātmya, Raghunātha Dāsa's Muktācarita and Dānakelicintāmaṇi, Viśvanātha's Gurvaṣṭaka and Camatkāracandrikā, Baladeva's Vedāntasyamantaka.
- The Nityānanda- and Advaita-vaṃśa guru lineages.
- Manipuri and Assamese Gauḍīya branches.
- The Kheturi festival as an event entry.
- Madhusūdana Sarasvatī's Bhaktirasāyana side of dsp:is-bhakti-a-rasa, which is only summarised.
- The Śrīkarabhāṣya and Siddhāntaśikhāmaṇi have no U16 teachings; U20 holds the Siddhāntaśikhāmaṇi teachings.
- No energy-anatomy teachings exist in these lineages beyond Haribhaktivilāsa's nyāsa and bhūta-śuddhi. This is recorded as an absence, not a gap to invent.

## 4. Out of reach, restricted or confidential
- Initiation mantras are summarised only and never reproduced: the gopāla-mantra, the kāma-gāyatrī and the brahmasambandha formula.
- Siddha-praṇālī identity details are transmitted orally and kept confidential.
- The Vārtā and havelī-saṅgīt repertoire lives largely in manuscripts and sect archives (Nathdwara, Kankroli).
- Gauḍīya manuscript collections are held in Vṛndāvana and Bengal.
- Lost texts: Bhartṛprapañca's and Yādavaprakāśa's commentaries.
- There are no restricted practices in this unit.
