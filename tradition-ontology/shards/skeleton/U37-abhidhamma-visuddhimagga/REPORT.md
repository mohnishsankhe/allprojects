# U37 — Abhidhamma, commentaries, Visuddhimagga system, later Theravāda lineages: skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Validator:** 0 errors, 1 warning (REPORT.md missing before this file is saved).
**Counts:** sources 80, teachers 53, lineages 16, ultimate views 11, teachings 222, terms 190, concepts 58, practices 81, obstacles 18, paths 3, phenomenology 32, disputes 20, borrowings 4, interpretation_log 63.

**How it was built**
- The generators are in `_gen/` (part1–part12). `_gen/abh.py` reads the local sources:
  - the Mahāsaṅgīti Abhidhamma in `sources_raw/bilara-data` (all 7 books present, CC0);
  - the GRETIL Devanāgarī PTS Visuddhimagga, which the script transliterates back to roman and locates by PTS page.
- 109 teachings carry an `original` that I read in those files. Two edits apply to the Visuddhimagga quotations only: ṅ is restored before velars (the e-text writes n), and the avagraha is written as an apostrophe.
- Visuddhimagga teachings are cited by chapter, with the PTS page in `location.section`. Ñāṇamoli paragraph numbers are not claimed.
- Other sources are cited by chapter or section only:
  - the Abhidhammatthasaṅgaha, the aṭṭhakathās and the Vimuttimagga (no local text);
  - modern works (chapter/section refs from memory).

## 1. Coverage checklist (brief items → ids)

**Seven Abhidhamma books**
- src:abhidhamma-pitaka is the parent entry.
- src:dhammasangani: mātikā of 22 tika, 100 Abhidhamma duka and 42 Suttantika duka; four kaṇḍas. Covered by tea:dhammasangani:1.1, 1.1/2, 1.3, 2.1.1, 2.1.5, 2.2.1, 2.2.1/2 and 2.3.2(/2–/6), and by cpt:dhammasangani-matika.
- src:vibhanga: the 18 chapter titles were checked. Covered by tea:vibhanga:6, 6/2, 7, 12, 12/2, 13, 15, 16, 17, 18 and 18/2.
- src:dhatukatha: tea:dhatukatha:1.1.
- src:puggalapannatti: tea:puggalapannatti:1.1, 1.1/2 and 2.1; cpt:types-of-persons.
- src:kathavatthu: 219 kathās in 23 vaggas.
  - Teachings: tea:kathavatthu:1.1, 1.2, 1.6, 2.1-5, 2.9, 4.1, 6.2, 6.6, 7.6, 8.2, 17.3, 18.1, 18.2, 18.7 and 21.6.
  - Disputes: dsp:kv-puggala, dsp:kv-arahant-falling-away, dsp:kv-sabbam-atthi, dsp:kv-arahant-imperfections, dsp:kv-gradual-penetration, dsp:kv-lay-arahant, dsp:kv-unconditioned-dhammas, dsp:kv-transfer-of-gifts, dsp:kv-antarabhava, dsp:kv-everything-due-to-kamma, dsp:kv-buddha-in-human-world, dsp:kv-jhanantarika and dsp:kv-buddhas-in-all-directions.
  - Opponent lineages: lin:andhaka, lin:uttarapathaka and lin:vetulyaka are new; the U38 lineages are referenced.
- src:yamaka: 10 yamakas. tea:yamaka:1.1.1 and 7.1.
- src:patthana: tea:patthana:1.1.1 gives the 24 conditions, quoted verbatim. Further teachings: tea:patthana:1.1.2 and /2–/8, and 1.1.3. Concept: cpt:twenty-four-conditions.

**Abhidhammatthasaṅgaha (9 chapters)**
- tea:abhidhammatthasangaha:1–9/3 (24 teachings).
- Concepts:
  - cpt:four-paramattha-dhammas and cpt:classes-of-consciousness (89/121);
  - cpt:fifty-two-cetasikas, cpt:twenty-eight-rupas, cpt:four-origins-of-matter, cpt:rupa-kalapa and cpt:momentariness;
  - cpt:citta-vithi and cpt:bhavanga;
  - cpt:thirty-one-planes and cpt:death-and-rebirth-linking;
  - cpt:kamma-fourfold-classifications and cpt:pannatti;
  - cpt:heart-base.
- Manuals and sub-commentaries: src:abhidhammavatara, src:namarupapariccheda, src:paramatthavinicchaya, src:saccasankhepa, src:mohavicchedani, src:khemappakarana, src:abhidhammatthavibhavini, src:sankhepavannana and src:paramatthadipani-ledi.

**Visuddhimagga (23 chapters)**
- src:visuddhimagga has 83 teachings: tea:visuddhimagga:1 to 23/4.
- Seven purifications: cpt:seven-purifications-concept; pth:seven-purifications is referenced (U51 owns it).
- Forty subjects, each as a practice:
  - kasiṇas: prc:kasina-earth, -water, -fire, -air, -blue, -yellow, -red, -white, -light, -space;
  - foulnesses: prc:asubha-bloated … prc:asubha-skeleton (10);
  - recollections: prc:buddhanussati, prc:dhammanussati, prc:sanghanussati, prc:silanussati, prc:caganussati, prc:devatanussati, prc:maranassati, prc:kayagatasati, prc:anapanasati and prc:upasamanussati;
  - divine abidings: prc:metta-bhavana, prc:karuna-bhavana, prc:mudita-bhavana and prc:upekkha-bhavana;
  - formless: prc:akasanancayatana, prc:vinnanancayatana, prc:akincannayatana and prc:nevasannanasannayatana;
  - the perception and the defining: prc:ahare-patikulasanna and prc:catudhatuvavatthana.
- Temperaments, impediments, good friend: cpt:six-temperaments; obs:ten-palibodhas; cpt:kalyanamittata.
- Concentration and signs: cpt:three-samadhis, cpt:three-nimittas, cpt:khanika-samadhi and pth:three-samadhis-nimittas (new).
- Insight knowledges: teachings tea:visuddhimagga:21–21/6 and tea:abhidhammatthasangaha:9/2, and cpt:insight-knowledges; pth:sixteen-insight-knowledges is referenced (U51 owns it).
- Ten corruptions of insight: obs:ten-vipassanupakkilesas and phn:corruption-* (4 entries).
- Direct knowledges and their warnings: cpt:six-abhinnas, cpt:ten-iddhis, prc:abhinna-development (with the p. 97 warning) and obs:worldly-iddhi-attachment.
- Also covered:
  - ascetic practices: prc:dhutanga plus the 13 individual dhutaṅgas;
  - virtue, concentration skills and attainments: prc:catuparisuddhi-sila, prc:appana-kosalla, prc:jhana-vasi, prc:nirodha-samapatti and prc:phala-samapatti;
  - insight practices: prc:namarupa-pariccheda, prc:paccaya-pariggaha and prc:kalapa-sammasana.

**Commentaries**
- Buddhaghosa's by Nikāya: src:sumangalavilasini, src:papancasudani, src:saratthappakasini and src:manorathapurani.
- Abhidhamma and Vinaya commentaries: src:atthasalini, src:sammohavinodani, src:pancappakarana-atthakatha, src:samantapasadika and src:kankhavitarani.
- Attributed to Buddhaghosa (doubtful): src:paramatthajotika, src:dhammapada-atthakatha and src:jataka-atthakatha.
- Dhammapāla: src:paramatthadipani-dhammapala, src:paramatthamanjusa and src:nettippakarana-atthakatha.
- Sub-commentaries: src:mulatika and src:anutika.
- Others: src:saddhammappakasini, src:saddhammapajjotika, src:visuddhajanavilasini and src:madhuratthavilasini.
- Upatissa: src:vimuttimagga and tch:upatissa; the Chinese translator is tch:sanghapala.
- Buddhadatta: tch:buddhadatta.
- Sāriputta of Polonnaruwa: tch:sariputta-polonnaruwa, src:saratthadipani, src:saratthamanjusa and src:vinayasangaha.
- Chronicles: src:dipavamsa, src:mahavamsa, src:culavamsa, src:buddhaghosuppatti, src:gandhavamsa and src:sasanavamsa.

**Later lineages (owned; all `recent: true` except the borān tradition)**
- Ledi: lin:ledi and tch:ledi-sayadaw, with the 6 dīpanīs and the Paramatthadīpanī.
- Mahāsi: lin:mahasi, tch:mahasi-sayadaw and tch:mingun-jetavana-sayadaw; practices prc:mahasi-noting, prc:rising-falling and prc:walking-meditation-noting; teachings tea:progress-of-insight:*.
- U Ba Khin – Goenka: lin:u-ba-khin-goenka, tch:saya-thetgyi, tch:u-ba-khin and tch:goenka; practices prc:body-scanning and prc:ten-day-vipassana-course.
- Sunlun: lin:sunlun and prc:sunlun-method.
- Pa-Auk: lin:pa-auk, pth:pa-auk-path and prc:rupa-kalapa-discernment.
- Mogok: lin:mogok (new), tch:mogok-sayadaw and prc:mogok-method.
- Webu: tch:webu-sayadaw.
- Thai Forest:
  - lin:thai-forest;
  - teachers tch:ajahn-sao, tch:ajahn-mun, tch:ajahn-chah, tch:ajahn-lee, tch:ajahn-maha-boowa, tch:ajahn-thate, tch:luang-pu-dune, tch:ajahn-fuang, tch:mae-chee-kaew, tch:ajahn-sumedho and tch:thanissaro-bhikkhu;
  - practices prc:tudong, prc:buddho-recitation and prc:ajahn-lee-breath-method.
- Buddhadāsa: lin:suan-mokkh and tch:buddhadasa.
- Dhammakāya: lin:dhammakaya (new), tch:luang-pu-sodh, prc:dhammakaya-meditation and pth:dhammakaya-inner-bodies.
- Borān kammaṭṭhāna: lin:boran-kammatthana, src:yogavacaras-manual and prc:yogavacara-piti-installation.
- Also new: lin:mahavihara, lin:abhayagiri and lin:dhammayut (with tch:mongkut).

**Disputes (besides the Kathāvatthu ones)**
- Dry insight vs jhāna first: dsp:dry-insight-or-jhana-first.
- Authority of the Abhidhamma: dsp:authority-of-abhidhamma.
- Further disputes:
  - dsp:dependent-origination-three-lives-or-present;
  - dsp:nibbana-atta-or-anatta;
  - dsp:vimuttimagga-visuddhimagga;
  - dsp:ledi-vibhavini;
  - dsp:luminous-citta-reading.
- Of the 20 disputes, 12 are queued ("not yet reconciled") with candidate readings and 8 are partially reconciled. The Theravāda's explicit denials are recorded in `tradition_objections` (e.g. the rejection of nibbāna as attā).

**D checklist, per lineage**
- Ultimate: 11 ult views.
- Self: anattā; cpt:the-one-who-knows; the Dhammakāya atta dispute.
- Body and energy anatomy: cpt:heart-base, rūpa-kalāpa, the Dhammakāya bases, Ajahn Lee's breath points.
- Death: cpt:death-and-rebirth-linking, phn:death-signs, prc:maranassati, prc:deathbed-recollection, prc:abhidhamma-funeral-chanting.
- Sound and language: cpt:magadhi-root-language, trm:pannatti, prc:paritta, trm:buddho, trm:samma-araham.
- Cosmology: cpt:thirty-one-planes, cpt:world-cycles, cpt:five-niyamas, cpt:sasana-decline.
- Teacher and transmission: cpt:kalyanamittata, cpt:abhidhamma-origin-account, cpt:lay-meditation-movement.

**Corrections to the brief's list**
- The "sixteen insight knowledges" are not a numbered list in the Visuddhimagga. It has 9 knowledges within the sixth purification (checked, PTS p. 639). The Abhidhammatthasaṅgaha lists 10 insight knowledges. The sixteen-item list is a later systematization used by Mahāsi and others.
- The Kathāvatthu has 219 kathās in 23 vaggas (counted locally).
- The Abhidhamma's own lists differ from the sutta lists:
  - 6 hindrances (adding ignorance);
  - 10 fetters including envy and avarice;
  - 4 taints (adding views).
- The heart-base is not in the canonical Abhidhamma. The Paṭṭhāna speaks only of an unnamed "matter in dependence on which" the mind-element and mind-consciousness-element occur (read locally); the heart identification is commentarial.
- Webu Sayadaw is recorded as a teacher, not as a lineage.

## 2. Least sure (check these first for hallucination)
- **Minor authors and texts:**
  - authors: Ānanda (Mūlaṭīkā), Culla-Dhammapāla, Kassapa (Mohavicchedanī), Khema, Chapaṭa/Saṅkhepavaṇṇanā, Mahānāma (Saddhammappakāsinī), Upasena;
  - attributions: the Rūpārūpavibhāga and the Paramatthavinicchaya;
  - dates: the Buddhaghosuppatti and the Gandhavaṃsa.
- **Kathāvatthu school attributions:** all come from memory of the commentary. Especially uncertain: kv 7.6, 17.3 and 18.7.
- **Vimuttimagga:** 12 chapters, 14 temperaments, the count of meditation subjects, and Saṅghapāla's dates. The claim that Dhammapāla's ṭīkā names Upatissa (tea:paramatthamanjusa:3 and :18) is low confidence.
- **Ledi:** titles of the dīpanīs (Uttamapurisa-dīpanī especially), the 1897 date of the Paramatthadīpanī, and the dsp:ledi-vibhavini details.
- **Dates and details of recent teachers:**
  - Sunlun and Mogok (and their methods);
  - Mingun Jetavana, U Paṇḍita, Munindra, Dipa Ma, Dhammajayo;
  - Upāli Thera of Ayutthaya;
  - the Dhammakāya 1917 date, its seven bases and its inner bodies.
- **Modern book titles and contents:**
  - U Ba Khin's "Essentials…" and Pa-Auk's "Workings of Kamma";
  - Payutto's 1999 Dhammakaya book;
  - Ajahn Lee's list of resting spots;
  - the Muttodaya quotation;
  - Maha Boowa on the radiant citta.
- **Commentary passages recalled, not read:**
  - the Atthasālinī on the five niyāmas;
  - the Manorathapūraṇī gloss of the luminous mind as bhavaṅga (and its simile);
  - the Papañcasūdanī matching the satipaṭṭhānas to four temperaments;
  - the Mahāvaṃsa chapter numbers (5, 33).
- **The Kheminda–Mahāsi controversy:** participants and date, in historical_debates.
- **Visuddhimagga teachings marked not read locally:** refs 5, 7, 7/2, 8/2, 8/3, 8/7, 9/3, 10/2, 11, 11/2, 11/3, 12/2, 14/4, 16/2, 20/4, 22 and 23/3. Their paraphrases come from memory (moderate confidence).

## 3. Gaps (belong here but not created responsibly)
- **Pa-Auk:** the major Burmese/Pali work(s) (e.g. a "Nibbānagāminipaṭipadā"). Titles uncertain.
- **Sunlun, Mogok, Webu:** primary texts or discourse collections.
- **Other Burmese insight lineages:** Taungpulu, Shwe Oo Min / U Tejaniya, Mohnyin.
- **Burmese Abhidhamma ṭīkās:** Ariyavaṃsa's Maṇisāramañjūsā and Maṇidīpa.
- **Dhammapāla's ṭīkās on the Nikāya commentaries:** titles uncertain.
- **Thai Forest teachers not created:** Luang Pu Sim, Ajahn Khao, Ajahn Waen, Ajahn Juan and others.
- **Primary texts not available:** Luang Pu Sodh's sermons (the Dhammakāya entries rely on secondary knowledge); Cambodian, Lao and Thai borān manuscripts (titles uncertain).
- **Sri Lankan 20th-c. meditation and Abhidhamma teachers:** Kaḍavädduvē Jinavaṃsa, Rerukane Chandawimala, Nāuyane Ariyadhamma, Mātara Ñāṇārāma.
- **Nuns' lineages (thilashin, mae chee):** only Mae Chee Kaew is recorded.
- **Local texts not yet read:** the Samantapāsādikā, Mahāvaṃsa and Dīpavaṃsa are in sources_raw (GRETIL Devanāgarī) but were not read this phase. The GRETIL Abhidhamma e-texts duplicate bilara.
- **Not in sources_raw:** the Abhidhammatthasaṅgaha, Atthasālinī, Sammohavinodanī and Vimuttimagga (the local CBETA subset lacks T32).

## 4. Out of reach / restricted / notes for the merge
- **Oral and restricted transmission:** borān kammaṭṭhāna rites and syllable placements, Sunlun's supervised breathing, and Pa-Auk interview instruction are recorded as summaries only. No breath counts, durations or syllable schemes.
- **Conservative restricted flag:** prc:nesajjikanga (the sitter's practice, never lying down) is flagged `restricted: true` as a prolonged sleep-deprivation austerity.
- **Aligned with U36's ids:** prc:maranassati, prc:metta-bhavana, prc:anapanasati, prc:kayagatasati, prc:buddhanussati, prc:dhutanga, cpt:kalyanamittata, cpt:six-abhinnas, cpt:nirodha-samapatti, obs:seven-anusayas, pth:*.
- **Dangling until U36 writes its files:** cpt:conventional-expression, cpt:four-jhanas, cpt:four-satipatthanas, cpt:nibbana, cpt:samatha-vipassana, cpt:three-trainings, obs:asavas, prc:dhatumanasikara, prc:patikulamanasikara, trm:kalyanamittata. All of these appear in U36's generators.
- **New sub-lineages (parent lin:theravada unless noted):**
  - lin:mahavihara, lin:abhayagiri, lin:dhammakaya, lin:mogok, lin:dhammayut;
  - lin:andhaka (parent lin:mahasanghika), lin:uttarapathaka and lin:vetulyaka (both no parent; known only through Theravāda reports, `reported_by_opponent` noted).
