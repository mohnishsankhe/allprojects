# U25-alvar-bhakti-theory — REPORT (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Validator: `python3 scripts/validate_shard.py shards/skeleton/U25-alvar-bhakti-theory` gives **0 errors**. The only warning was "REPORT.md missing".
Counts: sources 41 · teachers 28 · teachings 149 · terms 98 · concepts 40 · practices 26 · obstacles 11 · phenomenology 16 · disputes 4 · borrowings 9 · paths 2 · lineages 2 · ultimate 2 · interpretation_log 73.
Generators: `_gen/part01…part11` (`part11` rebuilds `interpretation_log.jsonl` from the shard; delete the file and re-run it after any edit).

## 0. Decisions and corrections to the MUST-COVER list
- **New sub-lineage `lin:bhakti-sastra`** ("Bhakti-śāstra: the sūtra tradition of devotional theory").
  - The Nārada and Śāṇḍilya Bhakti Sūtras belong to no institutional lineage.
  - The texts themselves name a "bhakti-śāstra" (NBS 76) and a line of "bhaktyācāryas" (NBS 83).
  - Parent is `lin:bhagavata-early`, on the tradition's account: Nārada and Śāṇḍilya as Bhāgavata/Pāñcarātra sages. This is not a claim of historical continuity; it keeps convergence counts from treating the sūtras as an independent root.
  - Vopadeva's Muktāphala (with Hemādri's Kaivalyadīpikā) and Viṣṇupurī's Bhaktiratnāvalī are grouped here.
  - It has its own `ult:bhakti-sastra`. Logged in `interpretation_log`. **Please add a DECISIONS.md line.**
- **Gīta Govinda lineages.** No owned lineage fits, so I used `lin:jagannatha` (U56, the Purī liturgical home) plus `lin:gaudiya-vaisnava` and `lin:sangita`.
  - Because Odisha/Purī *is* the home lineage, the brief's "borrowing to Odisha" became a source/practice record (`prc:astapadi-singing`, `src:gita-govinda` notes), not a borrowing edge.
  - Borrowings were made to Gauḍīya, Kerala (`lin:kerala-tantra` as the nearest lineage), `lin:sangita` and Bengal Sahajiyā (low confidence).
- **Hearing among the nine forms.** The existing `prc:sravana` (U03, U13, U15) is Vedāntic hearing of the Upaniṣads. Bhakti hearing is a new entry, `prc:sravana-bhakti`, with an "analogous" equivalence to `prc:sravana`.
  - Singing and remembering reuse `prc:kirtana` and `prc:smarana` as lineage contributions.
  - The other six are new: `prc:padasevana`, `prc:arcana`, `prc:vandana`, `prc:dasya`, `prc:sakhya`, `prc:atmanivedana`.
- **Homonyms disambiguated.**
  - `src:tiruppallantu-periyalvar`, because U18's `src:tiruppallantu` is Cēntaṉār's Śaiva hymn.
  - `src:tiruppalliyelucci-tontaratippoti`, because Māṇikkavācakar has a Śaiva Tiruppaḷḷiyeḻucci.
  - `tch:kumbhakarna-mewar` and `tch:padmavati-jayadeva`.
- **Brief corrections and precisions.**
  - The 4000 verses reach that total only with Tiruvaraṅkattu Amutaṉār's Irāmāṉuca Nūṟṟantāti (not an Āḻvār work).
  - Part totals: 947 / 1134 / 817 / 1102, counting Ciṟiya and Periya Tirumaṭal as 40 and 78.
  - Some lists count ten Āḻvārs, omitting Āṇṭāḷ and Madhurakavi.
  - Nammāḻvār's four works are equated by tradition with the Vedas: Tiruviruttam–Ṛg, Tiruvāciriyam–Yajus, Periya Tiruvantāti–Atharva, Tiruvāymoḻi–Sāman. Tirumaṅkai's six works are equated with the six aṅgas.
  - Kulacēkarar's id uses the Sanskrit slug `tch:kulasekhara-alvar`.
- **Placed with `lin:alvar` but not Āḻvār works** (flagged in their notes): Paripāṭal (Saṅgam precursor hymns to Tirumāl) and Kampaṉ's Irāmāvatāram / Caṭakōpar Antāti.
- `tch:nammalvar` had only a U14 stub reading "(U25 owns.)"; the full entry is written here.

## 1. Coverage checklist (A9 scope and brief) → ids
- **The twelve Āḻvārs.** Each has tradition and scholarly dating, works, and hagiography as `realization_account`.
  - `tch:poykai-alvar`, `tch:putattalvar`, `tch:peyalvar`, `tch:tirumalicai-alvar`, `tch:nammalvar`, `tch:madhurakavi-alvar`
  - `tch:kulasekhara-alvar`, `tch:periyalvar`, `tch:andal`, `tch:tontaratippoti-alvar`, `tch:tiruppan-alvar`, `tch:tirumankai-alvar`
  - Hagiography figures: `tch:kanikannan`, `tch:lokasaranga-muni`, `tch:kumudavalli`, `tch:kampan`.
- **Teachings per Āḻvār:**
  - Poykai: MT 1, MT 44.
  - Pūtam: IT 1.
  - Pēy: MūT 1, MūT 63.
  - Tirumaḻicai: NMT 1, NMT "cākkiyam kaṟṟōm", TCV 61.
  - Nammāḻvār (Tiruvāymoḻi): 1.1.1, 1.1.7, 1.2.1, 1.3.1, 1.4, 2.9.9, 3.3.1, 3.7.9, 4.10.1, 5.2.1, 5.8.1, 6.10.10, 7.2.1, 10.2.1, 10.9, 10.10.11, phalaśruti.
  - Nammāḻvār (other works): Tiruviruttam 1, Tiruvāciriyam, Periya Tiruvantāti 75.
  - Madhurakavi: KC 1, 2, 4.
  - Kulaśekhara: PT 4, 4.9, 5.1, 9; Mukundamālā ×2.
  - Periyāḻvār: Tiruppallāṇṭu 1, 3–5; PAT 1–3, 4.10.1, 5.4.1.
  - Āṇṭāḷ: TP 1, 2, 5, 6–15, 16–21, 28, 29, 30; NT 1, 6, 7, 12–13, 14.
  - Toṇṭaraṭippoṭi: Tirumālai 1, 2, 25, 42–43; TPE 1, 10.
  - Tiruppāṇ: AP 1, 2–9, 10.
  - Tirumaṅkai: PTM 1.1.1, 1.1.9; TNT 1–30; Ciṟiya Tirumaṭal; Tiruveḻukkūṟṟirukkai.
  - Hagiography teachings are filed under U14's `src:guruparampara-prabhavam-arayirappati` (mutal-alvars, tirumalicai, nammalvar-madhurakavi, kulasekhara, periyalvar, andal, tiruppan, tirumankai).
- **Nālāyira Divya Prabandham:** `src:nalayira-divya-prabandham` (4000; Nāthamuni; four thousands; taṉiyaṉs) plus 25 work entries (`src:tiruvaymoli` … `src:periya-tirumatal`, `src:mukundamala`).
- **Tamil Veda:** `cpt:tamil-veda`, `trm:dramidopanisad`, `dsp:tamil-prabandham-as-veda`.
- **Tiruppāvai / Mārkaḻi vow:** `src:tiruppavai`, `prc:tiruppavai-vow`, `trm:pavai-nonpu`, `trm:nonpu`, `trm:parai`, `pth:tiruppavai-approach`.
- **Nācciyār Tirumoḻi:** `src:nacciyar-tirumoli`.
- **108 Divya Deśams:** `cpt:divya-desa` and `trm:divya-desa` (contributions), `prc:divya-desa-pilgrimage` (contribution).
- **Commentaries:** referenced to U14 in the notes of `src:tiruvaymoli` (Ārāyirappaṭi … Paṉṉīrāyirappaṭi). Deśika's `src:munivahanabhoga` and `src:prabandhasaram` are added here.
- **Nārada Bhakti Sūtra:** `src:narada-bhakti-sutra` plus 40 teaching entries covering all 84 sūtras in groups (`tea:narada-bhakti-sutra:1` … `:84`).
  - Definitions: `trm:parama-prema`, `trm:amrta-svarupa`.
  - Eleven attachments: `cpt:eleven-asaktis`, `trm:ekadasa-asakti`.
  - Signs: `cpt:signs-of-the-lover-of-god`, phn ×3.
  - Superiority: `cpt:bhakti-as-its-own-fruit`.
  - Teachers: `cpt:bhaktyacaryas`.
- **Śāṇḍilya Bhakti Sūtra:** `src:sandilya-bhakti-sutra` (100 sūtras) and 10 teachings. Svapneśvara's commentary is `src:sandilya-bhakti-sutra-bhasya` / `tch:svapnesvara`; `src:bhakticandrika` is also recorded. `trm:paranurakti` covers parānurakti.
- **The nine forms (BhP 7.5.23–24):** nine practice entries, each with sources across lineages (Bhāgavata, NBS, Āḻvārs, Adhyātma Rāmāyaṇa, Rāmcaritmānas, Gītā, Śiva Purāṇa).
  - Also `tea:ramcaritmanas:3.35-36` and `cpt:nine-exemplars-of-devotion` (low).
- **Gīta Govinda:** `src:gita-govinda` and 16 teachings (1.1, 1.3, 1.4, aṣṭapadīs 1–4, cantos 2, 3, 4–6, 7–8, 9, 10 aṣṭapadī 19, 11, 12, closing).
  - Concepts: `cpt:radha-krsna-love-gita-govinda`, `cpt:dasavatara`.
  - Terms: `trm:astapadi`, `trm:nayika`, `trm:sakhi`, `trm:abhisara`, `trm:mana`, `trm:vipralambha`.
  - Practice: `prc:astapadi-singing`.
  - Sources and teachers: `tch:jayadeva`, `tch:padmavati-jayadeva`, `src:rasikapriya` / `tch:kumbhakarna-mewar`, `src:krsnagiti` / `tch:manaveda`.
  - Borrowings ×4: `brw:gita-govinda-to-gaudiya`, `-to-kerala`, `-to-sangita`, `-to-vaisnava-sahajiya`.
- **Bhakti definitions graded as equivalents:** `cpt:definitions-of-bhakti` (Nārada, Śāṇḍilya, Āḻvārs, Rāmānuja, Madhva, Rūpa, Advaita, Bhāgavata, Gītā — all with rests_on).
  - Graded equivalences are on `trm:parama-prema` ↔ `trm:paranurakti` / `trm:prema`, `trm:paranurakti` ↔ `trm:dhruvanusmrti` (contested), `trm:matinalam` ↔ `trm:bhakti`, and `trm:kanta-bhava` / `trm:nayika-bhava` ↔ `trm:madhura-rasa`.
- **Divine name:** `cpt:divine-name`, `trm:nama` (contribution), `prc:tirumantra-japa` (contribution).
- **Grace (anugraha / prasāda / aruḷ):** `cpt:grace` (contribution, with relations to `cpt:divine-grace` and `cpt:grace-anugraha`), `trm:arul`, `trm:krpa`, `trm:mahat-krpa`.
- **Surrender:** `cpt:prapatti` and `prc:saranagati` (contributions), `trm:saranagati`, `trm:akincanya`, `prc:atmanivedana`.
- **Viraha:** `cpt:viraha-bhakti` and `trm:viraha` (contributions), `trm:parama-viraha`, `trm:parama-vyakulata`.
- **Devotional moods (referencing U16):** `cpt:alvar-devotional-stances` and `cpt:eleven-asaktis`, related to `cpt:five-devotional-rasas`; `cpt:nayika-bhava`, related to `cpt:raganuga-bhakti`.
- **Devotion to the teacher:** `cpt:acarya-nistha`, `trm:acarya-nistha`, `prc:guru-bhakti` (contribution), `cpt:mahat-krpa-and-mahat-sanga`.
- **Devotee's qualities:** `cpt:qualities-of-the-devotee`, `cpt:service-to-devotees`, `prc:bhakta-caritra`.
- **Disputes:**
  - Bhakti vs jñāna: `dsp:is-knowledge-the-means-of-bhakti` (feeds `dsp:works-knowledge-grace`; partially reconciled under P3/P4).
  - Saguṇa/nirguṇa: `dsp:object-of-bhakti-sbs` (P2, the text's own reconciliation); references `dsp:saguna-nirguna`.
  - Caste: `dsp:devotee-birth-and-caste` (Tiruppāṇ; P1 partial; feeds `dsp:women-caste-liberation`).
  - Tamil Veda: `dsp:tamil-prabandham-as-veda` (queued; queue_ref `RQ-U25-tamil-veda` — **please add to RECONCILE_QUEUE.md**).
- **Ultimate:** `ult:alvar`, `ult:bhakti-sastra`.
- **Section D for lin:alvar:**
  - Consciousness and mind: `cpt:heart-and-senses-in-alvar-poetry`, phn ×11.
  - Self: `cpt:sesa-sesi-bhava` (contribution).
  - Body: `cpt:body-in-alvar-teaching` — states that no subtle-body anatomy is taught.
  - Cosmology: `cpt:creation-in-alvar-hymns`, `cpt:dravida-devotees-in-kali`.
  - Death: `cpt:antima-smrti` and `cpt:arciradi-gati` (contributions).
  - Powers: `cpt:devotee-rejects-siddhis` (contribution).
  - Śrī's mediation: `cpt:purusakara` (contribution).
  - Obstacles: `obs:aivar`, `obs:piravi-kadal`, `obs:satha-vayu`, `obs:jati-abhimana`, `obs:anyasraya`, `obs:bhagavad-vismarana`.
- **Section D for lin:bhakti-sastra:**
  - Matter and qualities: `cpt:gunas-and-bhakti`.
  - Ethics: `cpt:nirodha-in-bhakti`, `cpt:scripture-after-conviction`.
  - Path: `pth:narada-bhakti-sutra-crossing-maya`.
  - Obstacles: `obs:duhsanga`, `obs:abhimana-dambha`, `obs:vada-disputation`, `obs:worldly-talk`, `obs:jara-bhava`.
  - Practices: `prc:duhsanga-tyaga`, `prc:tadarpita-akhilacara`, `prc:bhakti-sastra-manana`, `prc:vivikta-sthana-sevana`, `prc:satsanga` (contribution).
- **Śrīvaiṣṇava practices of the hymns:** `prc:mangalasasana`, `prc:tiruppalliyelucci`, `prc:araiyar-sevai`, `prc:adhyayana-utsava`, `prc:satari`.
- **Other borrowings (section C):** `brw:alvar-nayanmar-shared-forms`, `brw:alvar-to-puranic-dravida-devotees` (BhP 11.5.38–40), `brw:puranic-to-bhakti-sastra`, `brw:epic-teaching-to-bhakti-sastra`, `brw:vedanta-to-bhakti-sastra`.
- **Teachings created under other units' sources:** `tea:bhagavata-purana:11.5.38-40`, `:7.9.10`, `:9.4.63` (U07), and `tea:ramcaritmanas:3.35-36` (U26).

## 2. Least sure — check these first (possible hallucinations)
1. **Śāṇḍilya Bhakti Sūtra sūtra numbers and wording.**
   - Numbers: 3, 4, 6, 7, 29–31 (Kāśyapa / Bādarāyaṇa / Śāṇḍilya triad), 78 ("ānindya-yony adhikriyate").
   - The refs "1.2-adhikya" and "2.1-gauni" are placement guesses.
2. **Nārada Bhakti Sūtra numbering** follows the common 84-sūtra text; editions differ by one or two. The order of vātsalya and kāntā in NBS 82 is uncertain.
3. **Āḻvār verse refs** (content confident, number not): MT 44; MūT 63 (Hari-Hara at Tirumalai — content only moderate); TCV 61; TVM 1.1.7, 2.9.9, 3.7.9, 4.10.1, 5.8.1, 10.2.1; PTA 75; KC 4; PT 4.9, 5.1, 9; PAT 4.10.1, 5.4.1; Tirumālai 1, 25, 42–43; NT 1 (verse 5), 12–13.
   - The attribution of "cākkiyam kaṟṟōm" to the Nāṉmukaṉ Tiruvantāti rather than the Tiruccanta Viruttam is moderate.
4. **Aṃśa assignments of the Āḻvārs** (`cpt:alvar-divine-origin`, teacher notes). They vary between lists; Poykai, Pūtam, Pēy, Toṇṭaraṭippoṭi and Tiruppāṇ are low.
5. **Tiruneṭuntāṇṭakam's three-voice division** (1–10 / 11–20 / 21–30) and the story that Bhaṭṭar used it to win over Nañjīyar.
6. **Tiruppāvai "order of approach" path** (`pth:tiruppavai-approach`, low): the commentators' reading and the verse ranges 16–17 / 18–20 / 21–27.
7. **Hagiographic details.**
   - Tirumaṅkai melting a golden image from a Buddhist shrine at Nāgapaṭṭinam.
   - Tirumaḻicai's writings floating back up the Kāvēri.
   - The half-risen Kumbakōṇam image.
   - Kulaśekhara's pot with the cobra.
   - The "43rd day of Kali" birth of Nammāḻvār.
8. **Texts and authors of lower confidence.**
   - `src:bhakticandrika` (Nārāyaṇa Tīrtha — which one?); `src:bhaktiratnavali` (Viṣṇupurī's date, region, arrangement); `src:muktaphala` (arranged by nine rasas?); Svapneśvara's date.
   - `src:prabandhasaram`; `src:munivahanabhoga` (entered as Maṇipravāḷa); `src:catakopar-antati` (Kampaṉ's authorship is the tradition's); Mānaveda's Kṛṣṇagīti date.
9. **Gīta Govinda.** Canto-title list; the order attributed to Pratāparudra (c. 1499) restricting Purī singers to the Gīta Govinda; the Sahajiyā rasika-couple list (`brw:gita-govinda-to-vaisnava-sahajiya`, low); closing-verse wording (mother's name Rāmādevī, with variants).
10. **Numbers:** part verse-counts of the Prabandham; the regional distribution of the 108 sites; details of the adhyayana-utsava; the explanation of the Śaṭhāri's name; Paripāṭal's number of surviving hymns (low).

## 3. Gaps — belong here but not created responsibly
- The tradition's specific Kali-year dates, birth-stars and months for each Āḻvār (in the Guruparamparā, Deśika's Prabandhasāram, Upadēśa Ratnamālai). Only a generic "early Kali age" account is given.
- Decad-by-decad coverage of the Tiruvāymoḻi (100 decads), Periya Tirumoḻi (1084 verses), Periyāḻvār Tirumoḻi (461) and Tiruccanta Viruttam. Only the famous verses are covered.
- The commentators' mapping of the akam voices (heroine / mother / friend) to spiritual states.
- The aṃśa/bound-soul question and which ācāryas stress which reading.
- Tamil originals: all omitted, because letter-exact transliteration was not certain. Sanskrit originals are given only where certain: NBS 1–4, 6, 19, 25–26, 51–52, 72–73; ŚBS 1–2; GG 1.1, 1.3; Mukundamālā ×2; BhP 9.4.63.
- Pre-modern commentaries on the Nārada Bhakti Sūtra: none recalled. Modern ones were not recorded.
- The third adhyāya of the Śāṇḍilya Sūtra (creation, jīva, Īśvara, fruits) was not recalled in detail.
- Cilappatikāram's Āycciyar Kuravai (the cowherdesses' Kṛṣṇa dance, a precursor) — no entry (Jain-authored epic; lineage placement unclear).
- The Nārada Pañcarātra definition of bhakti ("sarvopādhi-vinirmuktam …", quoted in BRS 1.1.12) and Vopadeva's Harilīlāmṛta.
- Other Gīta Govinda commentaries and imitations: Śaṅkara Miśra's Rasamañjarī, Caitanyadāsa's Bālabodhinī, Abhinava Gītagovinda (Gajapati Puruṣottama), Gītagaurīśa and others. Not created — authorship uncertain.
- The Jayadeva birthplace controversy (Bengal / Odisha / Mithilā) is recorded only in notes, not as a dispute (historical, not doctrinal).
- Tiruppāvai commentaries (Periyavāccāṉ Piḷḷai's and others) — for U14.
- The location of the nine-exemplars verse (BRS or Padyāvalī) — no teaching id created.

## 4. Out of reach (oral, undigitized, restricted)
- The araiyar cēvai (gesture, melody, hereditary families), the living adhyayana-utsava and the Kerala sopāna aṣṭapadī style. These are performance traditions documented mainly orally and in Tamil or Malayalam sources.
- The temple inscriptions (the Pratāparudra order) need epigraphic sources.
- Restricted: none in scope. The Mārkaḻi vow's abstentions are restraint, not prolonged fasting.
  - Sahajiyā readings of Jayadeva–Padmāvatī are mentioned only as a lineage claim, with no practice content. Detail belongs to U27 under the restricted-material rule.
  - The Bhāgavata's warning against imitating the Lord's love-play (BhP 10.33.30–31) is attached to the Gīta Govinda concept and practice.

## 5. Cross-unit notes
- **U14:** `tch:nammalvar` is now full. Four teachings reference `src:guruparampara-prabhavam-arayirappati` under new refs.
  - Contributions: `cpt:prapatti`, `cpt:purusakara`, `cpt:kainkarya`, `cpt:divya-desa`, `cpt:antima-smrti`, `cpt:arciradi-gati`, `cpt:sesa-sesi-bhava`, `prc:divya-desa-pilgrimage`, `prc:tirumantra-japa`, `trm:kainkarya`, `trm:mangalasasana`, `trm:divya-desa`, `trm:saulabhya`, `trm:purusakara`, `trm:akincanya`.
- **U16:** relations to `cpt:five-devotional-rasas`, `cpt:raganuga-bhakti`, `cpt:three-levels-of-bhakti`, `cpt:prema-as-fifth-goal`, `cpt:namabhasa`, `cpt:devotee-rejects-siddhis`. `cpt:nine-exemplars-of-devotion` carries a Gauḍīya definition (low) that U16 should verify.
- **U26:** `tea:ramcaritmanas:3.35-36` needs its numbering checked. `src:bhaktamal` is referenced but not created.
- **U27:** check `brw:gita-govinda-to-vaisnava-sahajiya`.
- **U50:** four new disputes feed G9, G11, G12, G13. `dsp:souls-one-or-distinct` is referenced from `dsp:object-of-bhakti-sbs`.
- **U56:** `lin:jagannatha` is the home lineage of the Gīta Govinda here. `tch:jayadeva` and `tch:padmavati-jayadeva` are written with that lineage.
- **U18:** `prc:tiruvempavai-vow` ↔ `prc:tiruppavai-vow` (analogous). `brw:alvar-nayanmar-shared-forms` cites `tea:tiruvacakam:7`, `:20` and `tea:tevaram:1.1.1`.
