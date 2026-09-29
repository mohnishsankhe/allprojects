# U35-jain-philosophy — Phase B skeleton report (Jain philosophy, yoga, practice, stages, meditation; I3 Ānandaghana, Adhyātma, Jain mantra)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent; subagents cannot write report files in this harness.)_

**Scope and ownership.** This unit owns `lin:adhyatma-jain` and `ult:adhyatma-jain`. It also writes a U35 contribution to `ult:jainism`, as the unit brief asked; U34 owns `lin:jainism` and may add to the same id, and the merge unions them. It refers to U34's lineages (`lin:jainism`, `lin:svetambara`, `lin:digambara`, `lin:yapaniya`, `lin:murtipujaka`, `lin:sthanakavasi`, `lin:terapanthi`, `lin:tapa-gaccha`, `lin:kharatara-gaccha`, `lin:terapantha-digambara`) without writing them.

**Generators.** They are in `_gen/`: `common.py`, `tsgen.py`, `termgen.py`, then `part01` … `part12`. Re-run them in order from `tradition-ontology/`. Parts 07–12 read `teachings.jsonl` to fill `rests_on` automatically.

**Counts:** lineages 1 · sources 128 · teachers 65 · teachings 427 · terms 406 · concepts 97 · practices 54 · obstacles 27 · paths 8 · phenomenology 17 · disputes 7 · borrowings 7 · ultimate 2 · interpretation_log 38.
- Teachings: Tattvārthasūtra 256; other texts 171.
- Teaching confidence: 258 high / 91 moderate / 78 low.
- Restricted: 10 teachings and 7 practices.

**Validator:** 0 errors. The only warning was that REPORT.md was missing.

**Method.** Tattvārthasūtra teachings take their sūtra number and IAST wording (`original`) from `sources_raw/prepared/tattvartha-sutra/segments.jsonl`. That is the Digambara recension, 357 sūtras: 33 / 53 / 39 / 42 / 42 / 27 / 39 / 26 / 47 / 9 by chapter. I skipped none of the doctrinally significant sūtras; descriptive runs of cosmology and lifespans are grouped as ranges. All paraphrases are mine and unchecked. All other teachings come from memory:
- `original` appears only where I am confident of the wording, and is marked "recalled".
- Verse numbers I could not confirm carry a note. Section-level refs (e.g. `tea:yogadrstisamuccaya:mitra`, `tea:jnanarnava:pindastha`) are used where I did not know the verse.
- The catalogue confirmed that about 30 Digambara titles exist (`catalog:JainDB:…`); this is recorded in the source notes. Every entry is still at level `skeleton`.

## Corrections to the MUST-COVER list
- **The Tattvārthasūtra does not list the fourteen guṇasthānas.** It gives its own ten-stage series of increasing shedding (TS 9.45), now `pth:tattvartha-ten-stages-of-nirjara`. The fourteen-stage list comes from the Ṣaṭkhaṇḍāgama, the Sarvārthasiddhi on 1.8 and the Gommaṭasāra.
- **The four objects of meditation (piṇḍastha, padastha, rūpastha, rūpātīta) are not in the TS.** They are in the Jñānārṇava and Yogaśāstra 7–10.
- **The TS names seven lay "śīlas", not twelve lay vows (7.21).** How they split into 3 guṇavratas and 4 śikṣāvratas differs between authors (Samantabhadra, Kundakunda, Hemacandra, Śvetāmbara standard). Recorded on `cpt:twelve-lay-vows`.
- **Śvetāmbara vs Digambara recensions.** I recorded these differences, from memory:
  - nayas: Dig 1.33 = Śv 1.34–35 (five nayas with subdivisions);
  - time: Dig 5.39 "kālaś ca" vs Śv 5.38 "kālaś cety eke";
  - Dig 7.4–8 (the vow-contemplations) are bhāṣya in the Śv text, so sallekhanā is Dig 7.22 = Śv 7.17 and hiṃsā is Dig 7.13 = Śv 7.8;
  - Śv 2.13–14 counts fire and air as mobile;
  - heavens: 16 (Dig) vs 12 (Śv) in 4.19.
- **The "rose-apple-tree parable".** The Digambara form is six travellers and a fruit tree (Gommaṭasāra Jīvakāṇḍa, c. 507–508, recalled). The jambū-tree form belongs to the Śvetāmbara Āvaśyaka commentaries (source not checked).
- **Two different Malliṣeṇas.** The Bhairava-Padmāvatī-kalpa is by the Digambara Malliṣeṇa (11th c.). He is not the Śvetāmbara Malliṣeṇa of the Syādvādamañjarī (1292). There are separate teacher ids for each.
- **Bhaktāmara length.** It has 44 verses in the Śvetāmbara text and 48 in the Digambara.
- **Ānandaghana's Covīsī.** By tradition he completed 22 of the 24 hymns.
- **Yaśovijaya's Yoga Sūtra commentary** covers selected sūtras only.
- **Haribhadra's Yogaśataka and Yogaviṃśikā are in Prakrit.**
- **Śubhacandra (Jñānārṇava, c. 11th c.)** is distinct from Bhaṭṭāraka Śubhacandra (16th c.).
- **Nyāyāvatāra:** authorship is disputed (a later Siddhasena).
- **Ātmasiddhi** has 142 dohās (1896).

## Id alignment and collisions (please check at merge)
- **Adopted U34's ids** to avoid duplicates: `tch:svami-karttikeya`, `tch:nemicandra-siddhantacakravartin`, `tch:jayasena-commentator`, `tch:somadeva-suri`, `tch:devendra-suri-tapa`, `src:kartikeyanupreksa`, `trm:kesa-loca`, `trm:vyavahara-naya`. U34 uses `trm:vyavahara-naya` for Kundakunda's conventional standpoint, so I did the same. Note that `src:kartikeyanupreksa` departs from the slug rule, which would give `karttikeyanupreksa`.
- **Renamed because of homonym collisions** with other units:
  - `trm:ajiva-jain` — U37's `trm:ajiva` is the Pali ājīva, "livelihood";
  - `trm:alocana-jain` — Sāṃkhya ālocana;
  - `trm:upapada-birth` — the Jyotiṣa upapada;
  - `trm:vyavahara-naya-seven` — the third of the seven nayas.
- **Dropped a reference.** U34 dropped `src:gommatasara`, so my `src:gommatasara-jivakanda` and `src:gommatasara-karmakanda` stand alone.
- **Shared ids from other units.** I used `src:saddarsanasamuccaya-haribhadra`, `src:prameyakamalamartanda`, `tch:prabhacandra`, `src:yasastilaka`, `src:adipurana-jinasena`, and U10's yoga terms and concepts, adding Jain definitions to those ids.
- **References still waiting for their owner units:**
  - U51: `pth:jain-fourteen-gunasthanas`, `pth:haribhadra-eight-drstis`, `pth:yoga-sutra-eight-limbs`;
  - U50: `dsp:causation`, `dsp:souls-one-or-distinct`, `dsp:women-caste-liberation`, `dsp:world-real-or-appearance`;
  - U52: `lin:kanji-swami`;
  - U49: `lin:tantra-movement`;
  - Buddhist units: `cpt:two-truths`, `cpt:four-immeasurables`, `cpt:bardo`.

## (1) Checklist — coverage map B2 (philosophy/yoga/practice) and I3 → ids

**Texts and teachers**
- **Tattvārthasūtra:**
  - `src:tattvartha-sutra` with 254 Digambara-numbered teachings (`tea:tattvartha-sutra:1.1` … `10.9`), plus `…:sv-1.34-35` and `…:sv-5.38`;
  - `src:tattvartha-bhasya` (svopajña, disputed) and `dsp:tattvartha-bhasya-authorship`;
  - commentaries: `src:sarvarthasiddhi` (`tch:pujyapada`), `src:tattvartha-rajavarttika` (`tch:akalanka`), `src:tattvartha-slokavarttika` (`tch:vidyananda`), `src:tattvartha-bhasya-vrtti-siddhasenagani` (`tch:siddhasenagani`), `src:tattvartha-vrtti-srutasagara`, `src:tattvarthasara`;
  - author: `tch:umasvati`.
- **Samantabhadra** (`tch:samantabhadra`): `src:aptamimamsa` (9 teachings), `src:ratnakarandasravakacara` (8), `src:svayambhustotra`, `src:yuktyanusasana`, `src:jinasataka`. Commentaries on the Āptamīmāṃsā: `src:astasati`, `src:astasahasri`; also `src:aptapariksa`.
- **Siddhasena Divākara** (`tch:siddhasena-divakara`): `src:sanmati-tarka` (5 teachings), `src:nyayavatara` (disputed), `src:dvatrimsika-siddhasena`, `src:kalyanamandira-stotra`.
- **Akalaṅka:** `src:laghiyastraya`, `src:nyayaviniscaya`, `src:siddhiviniscaya`, `src:astasati`, `src:svarupa-sambodhana` (doubtful).
- **Mallavādin** (`tch:mallavadin`): `src:dvadasaranayacakra`, with `src:nyayagamanusarini` (`tch:simhasuri`).
- **Other logicians:** `src:pariksamukha` (`tch:manikyanandi`), `src:nyayakumudacandra`, `src:pramananayatattvaloka` (`tch:vadidevasuri`), `src:alapapaddhati`, `src:syadvadamanjari` (`tch:mallisena-syadvadamanjari`).
- **Haribhadra** (`tch:haribhadra`, `tch:yakini-mahattara`):
  - yoga: `src:yogadrstisamuccaya` (15 teachings, including all eight views), `src:yogabindu` (5), `src:yogasataka-haribhadra` (2), `src:yogavimsika` (3), `src:vimsativimsika`;
  - doxography and other works: `src:saddarsanasamuccaya-haribhadra` (3), `src:sastravartasamuccaya`, `src:astakaprakarana`, `src:lokatattvanirnaya`, `src:dharmabindu`, `src:anekantajayapataka`, `src:sodasaka`, `src:dhurtakhyana`.
- **Hemacandra** (`tch:hemacandra`, `tch:devacandra-suri`): `src:yogasastra-hemacandra` (22 teachings, all 12 chapters), `src:yogasastra-svopajna-vrtti`, `src:pramanamimamsa`, `src:vitaragastotra`, `src:anyayogavyavacchedika`, `src:ayogavyavacchedika`, `src:mahadevastotra` (ascription uncertain).
- **Śubhacandra** (`tch:subhacandra`): `src:jnanarnava` (7 teachings: reflections, meditator, breath-control warnings, piṇḍastha/padastha/rūpastha-rūpātīta, asad-dhyāna).
- **Yaśovijaya** (`tch:yasovijaya`): `src:adhyatmasara`, `src:adhyatmopanisad`, `src:jnanasara`, `src:yogasutra-vrtti-yasovijaya`, `src:dvatrimsad-dvatrimsika-yasovijaya`, `src:adhyatmamatapariksa`, `src:jain-tarkabhasa`, `src:jnanabindu`, `src:nayopadesa`, `src:syadvadakalpalata`, `src:anandaghana-astapadi`.
- **Ānandaghana** (`tch:anandaghana`): `src:anandaghana-covisi` (stavans 1, 2, 21), `src:anandaghana-bahottari`.
- **Banārsīdās and the Adhyātma movement:**
  - lineage `lin:adhyatma-jain`;
  - teachers `tch:banarasidasa`, `tch:rajamalla`, `tch:rupcand-pande`, `tch:hemraj-pande`, `tch:dyanatray`, `tch:bhudhardas`, `tch:todarmal`, `tch:daulatram` (recent);
  - texts `src:samayasara-nataka`, `src:ardhakathanaka`, `src:banarasivilasa`, `src:pancadhyayi`, `src:moksamarga-prakasaka`, `src:chahdhala`;
  - Amṛtacandra's basis: `src:atmakhyati`, `src:samayasara-kalasa`, `src:purusarthasiddhyupaya`, and 4 teachings on U34's `src:samayasara` (8, 11, 14, 38);
  - critics: `src:yuktiprabodha` (`tch:meghavijaya`), `src:adhyatmamatapariksa`;
  - dispute `dsp:adhyatma-niscaya-and-ritual`.
- **Śrīmad Rājacandra** (`tch:srimad-rajacandra`, recent): `src:atmasiddhi` (6 teachings), `src:apurva-avasara`, `src:moksamala`; disciples `tch:lalluji-muni`, `tch:sobhagbhai`.
- **Other practice and adhyātma texts:**
  - Pūjyapāda: `src:samadhitantra`, `src:istopadesa`, `src:dasabhakti`;
  - Yogīndu and Rāmasiṃha: `src:paramatmaprakasa`, `src:yogasara-yogindu`, `src:pahuda-doha`;
  - Amitagati: `src:yogasara-prabhrta`, `src:samayika-patha-amitagati`;
  - Kārttikeya: `src:kartikeyanupreksa`;
  - Nemicandra: `src:dravyasangraha`, `src:gommatasara-jivakanda`, `src:gommatasara-karmakanda`, `src:labdhisara`, `src:trilokasara`;
  - cosmology: `src:tiloyapannatti`, `src:lokaprakasa`, `src:brhatsangrahani`;
  - conduct and dying: `src:mulacara`, `src:bhagavati-aradhana` (restricted), `src:aradhanasara`, `src:upasakadhyayana-somadeva`, `src:sagaradharmamrta`, `src:anagaradharmamrta`, `src:vasunandi-sravakacara`, `src:padmanandi-pancavimsatika`, `src:atmanusasana`;
  - later adhyātma and meditation: `src:tattvanusasana`, `src:tattvajnanatarangini`, `src:guna-sthana-kramaroha`;
  - karma: `src:karmagrantha-devendrasuri`, `src:navatattva-prakarana`;
  - Śvetāmbara canon and commentaries: `src:visesavasyaka-bhasya` (Gaṇadharavāda, kramavāda), `src:dhyanasataka`;
  - Devacandra and Cidānanda: `src:devacandra-covisi`, `src:adhyatma-gita-devacandra`, `src:cidananda-bahottari`, `src:svarodaya-cidananda` (recent);
  - creator critique: `src:adipurana-jinasena` (ch. 4 only).

**Concepts** (each with members, per-lineage definitions and `rests_on`)
- **Realities and substances:**
  - realities: `cpt:jain-tattvas` (7/9);
  - substances: `cpt:six-dravyas`, `cpt:dravya-guna-paryaya`, `cpt:utpada-vyaya-dhrauvya`, `cpt:pudgala-and-atoms`.
- **Soul and knowledge:**
  - the soul: `cpt:jiva-jain`, `cpt:upayoga`, `cpt:three-upayogas`, `cpt:five-bhavas`, `cpt:ananta-catustaya` (the infinite fourfold);
  - kinds of beings, vitalities and bodies: `cpt:classification-of-jivas`, `cpt:ten-pranas-jain`, `cpt:six-paryaptis`, `cpt:five-bodies`;
  - knowledge: `cpt:five-jnanas`, `cpt:stages-of-mati`, `cpt:kevala-jnana`, `cpt:pramana-jain`, `cpt:four-niksepas`.
- **Many-sidedness:** `cpt:anekantavada`, `cpt:syadvada-saptabhangi` (seven bhaṅgas), `cpt:nayavada` (seven nayas), `cpt:niscaya-vyavahara`.
- **Karma:**
  - kinds of karma: `cpt:karma-jain`, `cpt:eight-karmas` (with subtype counts; the TS 8.4–13 teachings cover all subtypes), `cpt:ghatiya-aghatiya`;
  - bondage: `cpt:four-aspects-of-bandha`, `cpt:causes-of-bondage`;
  - the four processes: `cpt:asrava`, `cpt:bandha`, `cpt:samvara`, `cpt:nirjara`;
  - fruition, merit and passions: `cpt:karma-processes`, `cpt:punya-papa`, `cpt:four-kasayas-sixteen`;
  - `cpt:six-lesyas` (with the parable), `cpt:sixteen-causes-of-tirthankarahood`.
- **Ethics and practice:**
  - vows: `cpt:five-vratas`, `cpt:twelve-lay-vows`, `cpt:eight-mulagunas`, `cpt:vow-bhavanas`;
  - attitudes and non-violence: `cpt:four-bhavanas-maitri`, `cpt:ahimsa-jain`;
  - stopping and austerity: `cpt:three-guptis-five-samitis`, `cpt:ten-dharmas`, `cpt:twelve-anupreksas`, `cpt:twenty-two-parisahas`, `cpt:five-caritras`, `cpt:twelve-tapas`;
  - meditation and duties: `cpt:four-dhyanas` (with subtypes), `cpt:six-avasyakas`.
- **Death and liberation:**
  - dying: `cpt:sallekhana` (restricted: conditions and warnings only), `cpt:kinds-of-death-jain`, `cpt:vigraha-gati`, `cpt:jain-death-transition`;
  - liberation: `cpt:moksa-jain`, `cpt:siddha-state`, `cpt:bhavya-abhavya`.
- **Stages and maps:**
  - Jain stages: `cpt:fourteen-gunasthanas`, `cpt:three-karanas-granthibheda`, `cpt:samyaktva`, `cpt:eleven-pratimas`;
  - selves and discrimination: `cpt:three-atmans`, `cpt:bheda-vijnana`;
  - Haribhadra: `cpt:haribhadra-eight-drstis` (with the correlation to Patañjali's limbs, faults and qualities), `cpt:haribhadra-three-yogas`, `cpt:haribhadra-five-yogas`, `cpt:yogavimsika-five-yogas`, `cpt:four-kinds-of-yogins`, `cpt:apunarbandhaka-caramavarta`, `cpt:four-anusthanas`, `cpt:five-anusthanas`;
  - later yoga: `cpt:three-vairagyas`, `cpt:four-dhyeyas`, `cpt:five-dharanas-jain`, `cpt:four-states-of-mind-hemacandra`.
- **Cosmology:** `cpt:loka-purusa`, `cpt:seven-hells`, `cpt:jambudvipa-madhyaloka`, `cpt:four-orders-of-gods`, `cpt:jain-time-cycle` (ārās), `cpt:no-creator-jain`.
- **Powers, teacher and sound:**
  - `cpt:labdhis-rddhis`, `cpt:kevalin-nature`;
  - `cpt:pancaparamesthin`, `cpt:jain-teacher-transmission`, `cpt:sadguru-marks` (how a teacher is tested), `cpt:four-anuyogas`, `cpt:six-fundamentals`;
  - `cpt:jain-mantra-theory`, `cpt:jain-sound-theory`.
- **Other darśanas and devotion:** `cpt:jain-views-of-other-darsanas`, `cpt:adhyatma-bhakti`, `cpt:three-jewels`, `cpt:five-nirgranthas`.

**Terms:** 406, with Prakrit cross-language forms for the key terms. They include the 14 guṇasthāna names, the 8 dṛṣṭi names and the mantra vocabulary.

**Practices** (54; restricted: `prc:sallekhana`, `prc:anasana`, `prc:kalajnana`, `prc:parakaya-pravesa`, `prc:padmavati-upasana`, `prc:surimantra-sadhana`, `prc:rsimandala-yantra-puja`)
- **Essential duties and confession:** `prc:samayika`, `prc:pratikramana`, `prc:kayotsarga`, `prc:six-avasyakas`, `prc:alocana`, `prc:prayascitta`, `prc:ksamapana`, `prc:paryusana`, `prc:prosadhopavasa`.
- **Vows and conduct:** `prc:mahavratas`, `prc:anuvratas`, `prc:guptis-samitis`, `prc:pratimas`, `prc:ratribhojana-tyaga`, `prc:dana-jain`, `prc:ahimsa`, `prc:diksa-jain`, `prc:kesa-loca`, `prc:mauna`.
- **Austerities:** `prc:tapas`, `prc:anasana`, `prc:avamaudarya`, `prc:rasa-parityaga`, `prc:kayaklesa`, `prc:ayambil`, `prc:navapada-oli`, `prc:vaiyavrttya`, `prc:vinaya`, `prc:svadhyaya`, `prc:vandana`.
- **Meditation:** `prc:anupreksa`, `prc:maitri-adi-bhavana`, `prc:dharma-dhyana`, `prc:sukla-dhyana`, `prc:pindastha-dhyana`, `prc:five-dharanas-jain`, `prc:padastha-dhyana`, `prc:rupastha-dhyana`, `prc:rupatita-dhyana`, `prc:bhedavijnana`, `prc:asana`, `prc:pranayama` (Jain view with warnings), `prc:preksa-dhyana` (recent).
- **Mantra and ritual:** `prc:namaskara-japa`, `prc:anupurvi`, `prc:arham-dhyana`, `prc:stotra-recitation`, `prc:jina-puja`.

**Obstacles:** 27, including the passions, wrong view, the five causes of bondage, the thorns, the transgressions, the follies and prides, sorrowful and cruel meditation, Haribhadra's eight faults, one-sidedness (ekānta) and attachment to powers.

**Mantra and tantra (I3)**
- **Namaskāra:** `src:namaskara-mantra` (five homages and cūlikā, with original), `prc:namaskara-japa`, `trm:namaskara-mantra`, `trm:culika`, `trm:asiausa`, `trm:arham`.
- **Padmāvatī:** `src:bhairava-padmavati-kalpa`, `prc:padmavati-upasana`, `trm:padmavati`, `trm:dharanendra`.
- **Sūrimantra:** `trm:surimantra`, `src:mantrarajarahasya`, `src:surimantra-kalpa-jinaprabha`, `prc:surimantra-sadhana`.
- **Ṛṣimaṇḍala:** `src:rsimandala-stotra`, `prc:rsimandala-yantra-puja`.
- **Hymns:** `src:uvasaggaharam-stotra`, `src:bhaktamara-stotra` (verses 1, 23, 25), `src:kalyanamandira-stotra`.
- **Other:** `src:jvalamalini-kalpa`, `trm:siddhacakra`, `trm:navapada`.

**Path maps**
- **Contributions to U51's maps:** teachings reference `pth:jain-fourteen-gunasthanas` and `pth:haribhadra-eight-drstis`.
- **New maps, banded, with one log line each:** `pth:tattvartha-ten-stages-of-nirjara`, `pth:yogabindu-five-yogas`, `pth:yogavimsika-five-yogas`, `pth:three-atmans`, `pth:jain-four-dhyeyas`, `pth:jain-eleven-pratimas`, `pth:jain-dhyana-ascent`, `pth:haribhadra-four-yogins`.

**Disputes**
- **New:**
  - `dsp:kevali-bhukti` — queued;
  - `dsp:kevala-jnana-darsana-sequence` — partially reconciled under P2, following Yaśovijaya's Jñānabindu;
  - `dsp:kala-as-dravya` — queued;
  - `dsp:tattvartha-bhasya-authorship` — queued;
  - `dsp:adhyatma-niscaya-and-ritual` — partially reconciled under P1 and P4;
  - `dsp:pranayama-and-liberation` — queued;
  - `dsp:number-of-nayas` — reconciled under P2.
- **Referenced (other units own):** `dsp:isvara` (Ādipurāṇa 4, Āptaparīkṣā, AYV 6, ŚVS 3), `dsp:is-there-a-self` (Gaṇadharavāda, Ātmasiddhi 43, ĀM on momentariness), `dsp:omniscience`, `dsp:momentariness`, `dsp:atomic-or-pervasive-self`, `dsp:eternality-of-sound`, `dsp:atomism`, `dsp:can-every-soul-be-liberated`, `dsp:nature-of-liberation`, `dsp:jnana-karma-samuccaya`, `dsp:women-caste-liberation`, `dsp:image-worship-and-inner-worship`, `dsp:yoga-samkhya-isvara`, `dsp:souls-one-or-distinct`, `dsp:world-real-or-appearance`, `dsp:causation`, `dsp:self-awareness-of-cognition`.
- **Views of other darśanas:** `cpt:jain-views-of-other-darsanas`, with teachings from the Sanmati, AYV 30, Lokatattvanirṇaya 38, YDS 129–134, Ṣaḍdarśanasamuccaya, Covīsī 21, Bhaktāmara 25 and Mahādevastotra.

**Ultimate views**
- `ult:jainism` (U35 contribution): the pure soul in its own nature, infinite knowledge, perception, bliss and energy. `tradition_denies_single_ultimate: true`. The caveat reads "all is one" as the collective standpoint (saṃgraha-naya) only; souls are many.
- `ult:adhyatma-jain`.

**Borrowings (7):**
- Digambara → Adhyātma;
- Śvetāśvatara 3.8 ↔ Bhaktāmara 23;
- Buddhist logic → Jain logic;
- Navya-Nyāya → Yaśovijaya;
- tantra → Jain mantraśāstra (disputed);
- bhūtaśuddhi ↔ the five dhāraṇās (low confidence);
- Sant idiom ↔ Ānandaghana.

## (2) Items I am least sure of (check these first)
- **Verse numbers outside the TS:**
  - Āptamīmāṃsā 4, 5, 6, 104, 105 and the 24–27 range; Yuktyanuśāsana 61 ("sarvodaya"); Svayambhūstotra 119 ("ahiṃsā … brahma paramam");
  - Ratnakaraṇḍa 2–5, 43–46, 66, 122, 136–147 (editions number differently);
  - Sanmati 1.3, 3.47, 3.69, and where the necklace simile sits;
  - YDS 13, 15, 16, 129–130, 133–134 (and the physician simile); all dṛṣṭi, three-yoga and yogin-type sections are section-level only;
  - Yogabindu 31; Yogaśataka 2–4; Yogaviṃśikā 1, 2, 19–20;
  - Yogaśāstra 1.15, 1.47–56, 2.2, 2.20, 4.2, 4.5, 4.114, 4.117–122, 4.124–134, 6.1, 6.4–5, 7.8, 7.9–28, 10.1, 12.1, 12.2–4;
  - Samādhitantra 78; Iṣṭopadeśa 50; Yogasāra (Yogīndu) 22; Kārttikeyānuprekṣā 478; Dravyasaṃgraha 2, 47, 49; Gommaṭasāra Jīvakāṇḍa 9–10 and 507–508; Mūlācāra 1.2–3;
  - Puruṣārthasiddhyupāya 5, 8, 42, 44, 177–178; Samayasāra 8, 11, 14, 38 (Amṛtacandra numbering); kalaśa 131; Padmanandi 6.7;
  - Jñānasāra 1, 16.2, 32; Adhyātmasāra 1.2; Ātmasiddhi 1, 10, 24–33, 34–42, 43, 142;
  - Bhaktāmara 23 and 25; Lokatattvanirṇaya 38; Anyayogavyavacchedikā 6 and 30; Mahādevastotra 44.
- **Contents recalled only in outline:**
  - the order of the twelve spokes of the Dvādaśāranayacakra;
  - the list of names in the YDS prabhā view (praśāntavāhitā, visabhāga-parikṣaya, śivavartman, dhruvādhvan);
  - Jñānārṇava's breath-control warnings and asad-dhyāna passage; Hemacandra's warning against meditating on fierce deities (YŚ 9);
  - the Gaṇadharavāda arguments; the Rājavārttika location of the blind-and-lame verse;
  - the Sarvārthasiddhi similes (lamp at 1.1, merchant's house at 7.22);
  - Śākaṭāyana's argument as reported; Yaśovijaya's Jñānabindu reconciliation;
  - the Ardhakathānaka episodes (no verse numbers given);
  - the Samayasāra Nāṭaka chapter structure and prologue;
  - the limb assignment in Ānandaghana's Covīsī 21; whether the "Rām kaho, Rahīm kaho" pada is really Ānandaghana's;
  - details of the Tattvārthabhāṣya praśasti (teachers' names, birthplace);
  - the Śvetāmbara list of the eleven pratimās; the Bhagavatī Ārādhanā's five-death classification.
- **Attributions and people:**
  - attributions: Svarūpasambodhana → Akalaṅka; Tattvānuśāsana → Rāmasena/Nāgasena; Guṇasthānakramāroha → Ratnaśekhara; Ṛṣimaṇḍala → Indrabhūti Gautama; Kalyāṇamandira; Mahādevastotra → Hemacandra; Dhyānaśataka → Jinabhadra;
  - Jinaprabha's Sūrimantra work (its title is uncertain); Siṃhatilaka's Mantrarājarahasya; the date and author identity of the Jvālāmālinī-kalpa (Indranandi); Cidānanda's Svarodaya;
  - Daulatrām's identity and dates; the Ṭoḍarmal execution legend; the dates of Lallujī and Sobhāgbhāī;
  - membership of Dyānatrāy and Bhūdhardās in the Adhyātma movement; Śrīmad Rājacandra's link to it (affinity only);
  - Prekṣā-dhyāna details (recent, low).
- **Terms with low confidence:** `trm:vardhamana-vidya`, `trm:ogha-drsti`, `trm:dharma-samnyasa`, `trm:yoga-samnyasa`, `trm:tattvabhu-dharana`, `trm:unmanibhava`, `trm:audasinya`, `trm:saili`, `trm:sakaladesa` / `trm:vikaladesa` (location in the Rājavārttika).

## (3) Gaps (belong here but not created responsibly)
- **Works and authors not created:** Umāsvāti's Praśamarati; Haribhadra's commentary on the Tattvārthabhāṣya (completed by Yaśobhadra) and Brahmasiddhāntasamuccaya; Anantavīrya's Siddhiviniścaya-ṭīkā; Abhayadeva's Sanmati commentary (author and text); Siddharṣi's Upamitibhavaprapañcā Kathā (allegory; perhaps U34); Devacandra's Nayacakrasāra; Yaśovijaya's Jñānabindu and other nyāya works beyond summary level; Guṇaratna as a teacher entry (his Tarkarahasyadīpikā exists as another unit's source).
- **Teachings not yet anchored:** kevali-samudghāta, the ṛddhi lists (e.g. the 64 Digambara ṛddhis), the 34 atiśayas and 8 prātihāryas (U34 terms exist), and the leśyā-at-death teaching (Śvetāmbara canon; U34's texts).
- **No teachings at all yet** for the Tattvārthabhāṣya beyond 1.1, the praśasti and the Śv variants; the Ślokavārttika; the Aṣṭasahasrī; the Laghīyastraya beyond one; the Jñānārṇava at verse level.
- **The Adhyātma lineage lacks** teachings of its own on sound and language and on death and dying.
- **Recent Jain meditation movements:** Prekṣā-dhyāna is entered only as a practice; Kanji Swami belongs to U52.

## (4) Out of reach
- **Oral or secret:** the wording and practice of the Sūrimantra and the Vardhamāna-vidyā; mantra initiations in the mantra-kalpa traditions.
- **Restricted:** sallekhanā/saṃthārā procedures and durations (conditions and warnings recorded only); prolonged fasts; the ṣaṭkarma rites and yantras of the Padmāvatī and Jvālāmālinī kalpas; Hemacandra's breath-retention methods, omen lists and body-entry practice (summary and his own warnings only).
- **Not local:** the Śvetāmbara recension of the Tattvārthasūtra (with bhāṣya) is not in `sources_raw`, so the Śvetāmbara sūtra numbers are from memory. Editions of the Jñānārṇava number its sargas differently, and collections of Ānandaghana's padas vary.
