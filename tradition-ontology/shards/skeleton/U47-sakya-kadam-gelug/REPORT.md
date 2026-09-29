# U47-sakya-kadam-gelug — skeleton sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Validator: `python3 scripts/validate_shard.py shards/skeleton/U47-sakya-kadam-gelug`. Result: 0 errors, 1 warning (REPORT.md missing until saved).

Counts: lineages 10 · ultimate 10 · sources 84 · teachers 84 · teachings 251 · terms 60 · concepts 78 · practices 40 · obstacles 15 · paths 6 · phenomenology 12 · disputes 12 · borrowings 11 · interpretation_log 15.

Teaching confidence: high 113 · moderate 118 · low 20. 66 teachings carry `original` (Wylie).

Generators are in `_gen/` (part1 … part11, plus `tengyur.py`, an in-memory reader of the local Derge Tengyur, and `common.py`). Re-running all parts in order rebuilds the shard.

## Local material found and used (all Esukhia Derge Tengyur, public domain)

- **Tōh 2284 — Virūpa's Lamdre root text, the "Vajra Verses"** (`src:lamdre`).
  - It is catalogued under its opening line ("bla ma dam pa'i zhabs pad la btud de / lam 'bras gsung mdo bri bar…").
  - It was not noted in GAPS.md, so please add it there as a find.
  - Teaching refs are Derge folio.line (e.g. `tea:lamdre:139a.7`). Originals are copied line by line.
- **Tōh 3947 — Bodhipathapradīpa** (25 teachings, `v1`–`v70`).
  - Refs are the mechanical 4-line stanza grouping (same scheme as `prepare_texts.tibetan_canon_text`).
  - The e-text has 70 groups. Conventional editions number by one or two differently, and each teaching's notes say so.
- **Tōh 3902 — Satyadvayāvatāra** (12 teachings).
- **Tōh 3951 — Bodhisattvamaṇyāvalī** (8 teachings).
- **Tōh 3960 — Caryāsaṃgrahapradīpa** (7 teachings).
- Sources only, not extracted, ready for Phase D: Tōh 3948 (Pañjikā), 3969, 3953, 4188, 3954, 3930.
- Not local (confirmed by catalogue searches): all Tibetan-authored works, including the lojong texts, as GAPS.md already says.

## (1) Coverage checklist — B6 Sakya / Kadam–Gelug and the unit brief

### Sakya

- **Lineages:** `lin:sakya`. New sub-lineages: `lin:ngor`, `lin:tshar`, `lin:dzongpa`.
- **Khön family and succession:** `tch:khon-konchok-gyalpo`, `cpt:khon-hereditary-succession`.
- **Drokmi and the Lamdre transmission:**
  - Teachers: `tch:drokmi-lotsawa`, `tch:gayadhara`, `tch:seton-kunrig`, `tch:zhangton-chobar`.
  - Concept: `cpt:lamdre-transmission`.
  - Borrowing: `brw:mahasiddha-to-sakya`.
- **Virūpa:** `tch:virupa` (Sakya contribution).
- **Lamdre and the Vajra Verses:**
  - Sources: `src:lamdre`, `src:lamdre-tsokshe`, `src:lamdre-lobshe`, `src:pod-ser`, `src:nyakma`.
  - Teachings: 15 `tea:lamdre:*` (including 141a.6).
- **Three visions:**
  - Concept `cpt:three-visions`; term `trm:nang-sum`; path `pth:lamdre-three-visions`.
  - Teachings: `tea:lamdre:139a.7`, `tea:three-visions-ngorchen:structure`.
  - Practice: `prc:lamdre-tsokshe-contemplation`.
- **Three continua:**
  - Concept `cpt:three-continua`; terms `trm:kunzhi-gyu-gyu`, `trm:khordey-yerme`, `trm:salstong-zungjug`.
  - Teachings: `tea:lamdre:139b.1-3`, `tea:three-continua-ngorchen:structure`.
- **Grounds and signs in the Lamdre:**
  - Path: `pth:lamdre-vajra-verses-grounds`.
  - Concepts: `cpt:lamdre-signs-of-the-grounds`, `cpt:thirteen-grounds-vajradhara`, `cpt:vajra-body-lamdre`, `cpt:four-authorities-lamdre`.
  - Phenomenology: `phn:lamdre-*`.
- **Parting from the Four Attachments:**
  - Sources: `src:parting-from-four-attachments` (4 line-teachings plus `context`), `src:parting-from-four-attachments-drakpa-gyaltsen` (4 teachings), `src:parting-from-four-attachments-gorampa`.
  - Concepts: `cpt:four-attachments`, `cpt:view-free-of-grasping`.
  - Path: `pth:parting-from-four-attachments`. Practice: `prc:parting-four-attachments-contemplation`.
- **Five founding masters:**
  - Concept: `cpt:five-founding-masters`.
  - Teachers: `tch:sachen-kunga-nyingpo`, `tch:sonam-tsemo`, `tch:drakpa-gyaltsen`, `tch:sakya-pandita`, `tch:chogyal-phagpa`.
  - Sources for Sönam Tsemo: `src:gyude-chinam-sonam-tsemo`, `src:chola-jugpai-go`. For Drakpa Gyaltsen: `src:gyude-ngontok-jonshing`. For Phagpa: `src:sheja-rabsel`.
- **Sakya Paṇḍita:**
  - Treasury of Valid Reasoning: `src:tshad-ma-rigs-gter` (U41's id reused).
  - Clarifying the Sage's Intent: `src:thubpai-gongsal`.
  - Three Vows: `src:domsum-rabye`, with 4 teachings including `ch.3.mahamudra`, `ch.3.chinese` and `ch.3.karpo-chigtub` (the "white panacea" and Hwashang critique).
  - Good Sayings: `src:sakya-legshe`. Gateway to Learning: `src:khepa-jugpai-go`, with `cpt:three-activities-of-the-learned`.
- **Gorampa:** `tch:gorampa`; sources `src:taway-shenje` (4 teachings), `src:taway-ngensel`, `src:ngedon-rabsel`.
- **Shākya Chokden:** `tch:shakya-chokden`, `src:golden-lancet`, and his side in `dsp:rangtong-shentong`.
- **Ngor and Tshar founders:** `tch:ngorchen-kunga-zangpo`, `tch:tsarchen-losal-gyatso`, `tch:ngorchen-konchog-lhundrub`.
- **Other Sakya teachers:** Rendawa, Rongtön, Yaktön, Taktsang, Tokmé Zangpo, Butön, Muchen, Amyé Zhab, the 41st Sakya Trizin (recent).

### Kadam

- **Lineages:** `lin:kadam`. New sub-lineages: `lin:kadam-shungpa`, `lin:kadam-lamrimpa`, `lin:kadam-mengakpa`.
- **Atiśa:** `tch:atisa` (Kadam contribution, with the life as the tradition tells it). Borrowings: `brw:prasangika-to-kadam`, `brw:mahayana-to-kadam`.
- **Lamp for the Path:** `src:bodhipathapradipa`, 25 teachings. The three scopes are `tea:bodhipathapradipa:v2-5`, `cpt:three-scopes` and `trm:kyebu-sum`.
- **Atiśa's other works:** `src:satyadvayavatara`, `src:bodhisattvamanyavali`, `src:caryasamgrahapradipa`, `src:bodhimargapradipapanjika`, and five more ritual and advice texts.
- **Teachers:** Dromtönpa, Potowa, Chengawa, Phuchungwa, Gönpawa, Neusurpa, Sharawa, Langri Tangpa, Chekawa, Sé Chilbu, Dölpa, Ben Gungyal, Serlingpa, Dharmarakṣita, Maitrīyogin, Yeshe Ö, Jangchub Ö, Rinchen Zangpo, Nagtso, Gewai Lodrö, Ngok Lekpai Sherab.
- **Eight Verses:** `src:eight-verses-mind-training`, 8 teachings.
- **Seven-Point Mind Training:**
  - `src:seven-point-mind-training`, with one teaching per slogan: 59 teachings, `tea:seven-point-mind-training:1.1` … `7.21`, grouped by point in `location.section`.
  - Commentary: `src:seven-point-commentary-se-chilbu`.
  - Concepts: `cpt:lojong-commitments`, `cpt:lojong-precepts`, `cpt:five-powers-lojong`, `cpt:ultimate-bodhicitta-lojong`, `cpt:relative-bodhicitta-lojong`.
  - Path: `pth:seven-points-mind-training`.
- **Lojong and tonglen:** `prc:lojong`, `prc:tonglen` (this resolves U40's dangling reference), `trm:lojong`, `trm:tonglen`.
- **Other lojong literature:** `src:wheel-of-sharp-weapons`, `src:peacock-neutralizing-poison`, `src:mind-training-great-collection`, `src:thirty-seven-practices` (17 teachings).
- **The three Kadam lineages:** the three sub-lineages above.
- **Four Kadam deities:** `cpt:seven-divine-dharmas-kadam`, `tea:book-of-kadam:seven-divine-dharmas`.
- **Six Kadam texts:** `cpt:kadam-six-texts`, plus a new `src:jatakamala`.
- **Book of Kadam and sixteen drops:** `src:book-of-kadam`, `prc:kadam-sixteen-drops`.
- **Kadam conduct and self-watching:** `prc:kadam-daily-conduct`, `prc:kadam-self-examination`.

### Gelug

- **Lineages:** `lin:gelug`. New sub-lineage: `lin:ganden-oral-lineage`.
- **Tsongkhapa:** `tch:tsongkhapa`, with realization account and `phn:tsongkhapa-realization`.
- **Lamrim Chenmo:** 34 section-level teachings: `tea:lamrim-chenmo:intro.*`, `small.*`, `middle.*`, `great.*`, `calm.*`, `insight.*`, `conclusion.tantra`.
- **Ngagrim Chenmo:** 3 teachings.
- **Three Principal Aspects:** 12 verse teachings plus the summary `10-12`; concept `cpt:three-principal-aspects`; term `trm:lamtso-namsum`; path `pth:three-principal-aspects`.
- **Essence of Eloquence:** `src:legs-bshad-snying-po` (U41's id), 2 teachings.
- **Ocean of Reasoning:** `src:ocean-of-reasoning`.
- **Praise of Dependent Origination:** 3 teachings.
- **Other Tsongkhapa works:**
  - `src:illumination-of-the-thought`, `src:lamrim-dringpa`, `src:lamrim-nyamgur`, `src:foundation-of-all-good-qualities`.
  - Tantric: `src:lamp-illuminating-five-stages`, `src:three-inspirations-naropa`.
  - Vows and teacher: `src:basic-path-to-awakening`, `src:fruit-clusters-of-siddhis`, `src:fulfilling-hopes-of-disciples`.
- **Gyaltsab Je:** `tch:gyaltsab-je`; sources `src:rnam-grel-thar-lam-gsal-byed`, `src:namshe-nyingpo-gyen`, `src:gyalse-jugngog`, `src:eight-difficult-points-memorandum`.
- **Khedrup Je:** `tch:khedrup-je`; sources `src:tongthun-chenmo`, `src:gyude-chinam-khedrup`.
- **Ganden, Drepung and Sera:** `cpt:three-great-seats`, `tch:jamyang-choje`, `tch:jamchen-choje`, `tch:gendun-drup` (Tashi Lhunpo).
- **Dalai and Panchen Lamas:**
  - Concept: `cpt:tulku-succession-gelug`.
  - Teachers: `tch:gendun-drup`, `tch:gendun-gyatso`, `tch:sonam-gyatso`, `tch:dalai-lama-5`, `tch:dalai-lama-7`, `tch:dalai-lama-13` (recent), `tch:dalai-lama-14` (link only; U52 owns), `tch:panchen-lobsang-chokyi-gyaltsen`, `tch:panchen-lobsang-yeshe`.
- **Five great texts and debate curriculum:**
  - Concepts: `cpt:gelug-monastic-curriculum`, `cpt:debate-method-gelug`, `cpt:four-tenet-systems` (contribution).
  - Sources: `src:bsdus-grwa`, `src:lorig`, `src:tarig`, `src:gelug-yigcha`, `src:drubta-chenmo`, `src:precious-garland-of-tenets`, `src:crystal-mirror-tenets`.
  - Practice: `prc:tshad-ma-debate` (contribution).
  - Textbook authors: Jetsün Chökyi Gyaltsen, Panchen Sönam Drakpa, Jamyang Shepa, Könchok Jigme Wangpo, Changkya, Thuken, Yongzin Yeshe Gyaltsen.
- **Eight difficult points:** `cpt:eight-difficult-points`, `trm:kane-gye`, `trm:zhigpa`, `dsp:eight-difficult-points`.
- **Object of negation:** `cpt:object-of-negation`, `trm:gakja`, `trm:medgak`, `trm:mayingak`, `trm:dendrub`, `dsp:object-of-negation-madhyamaka`.
- **Gelug Mahāmudrā:**
  - Sources: `src:gyalwai-shunglam` (3 teachings), `src:yangsal-dronme`.
  - Concept `cpt:gelug-mahamudra`; practice `prc:gelug-mahamudra-meditation`.
  - Lineage teachers: Tokden Jampal Gyatso, Baso, Chökyi Dorje, Ensapa, Sangye Yeshe.
- **Guru yoga:** `src:lama-chopa`, `src:ganden-lhagyama`, `src:migtsema`, `prc:guru-yoga` (contribution), `prc:migtsema-recitation`.
- **Later lamrims:** `src:essence-of-refined-gold`, `src:sacred-word-of-manjusri`, `src:easy-path-lamrim`, `src:swift-path-lamrim`, and the recent `src:liberation-in-the-palm` (with `cpt:four-point-analysis`).

### Brief concepts and practices

- **Three scopes:** `cpt:three-scopes`, with teachings contributed to U51's `pth:lamrim-three-scopes`.
- **Nine stages of calm abiding:** contributions to `cpt:nine-stages-calm-yogacara`, `prc:nine-mental-abidings`, `trm:navakara-cittasthiti`, and U51's `pth:nine-stages-calm-abiding`.
  - Six powers: `cpt:six-powers-samatha`.
  - Four attentions: `cpt:four-attentions-samatha`.
  - Five faults: `obs:five-faults-of-samatha` (contribution).
  - Eight antidotes: `prc:eight-antidotal-formations` (contribution).
  - Laxity: `obs:subtle-laxity`, `trm:jingwa`, `trm:auddhatya`.
  - Prerequisites and pliancy: `cpt:prerequisites-of-calm-abiding`, `cpt:pliancy-lamrim`, `phn:lrc-pliancy`.
- **Union of calm and insight:** `cpt:samatha-vipasyana-union` (contribution), `phn:calm-insight-union-gelug`.
- **Analytical and placement meditation:** `cpt:analytical-and-placement-meditation`, `prc:analytical-meditation`, `prc:placement-meditation`, `trm:chegom`, `trm:joggom`.
- **Four thoughts that turn the mind:** `cpt:four-thoughts-that-turn-the-mind`, `prc:four-thoughts-that-turn-the-mind`, `trm:lodok-namzhi`.
- **Eight worldly concerns:** `obs:eight-worldly-concerns` (contribution), `trm:jigten-chogye`.
- **Exchanging and equalizing:** `cpt:exchanging-self-and-other`, `cpt:equalizing-self-and-other`, `prc:exchanging-self-and-other`, `prc:equalizing-self-and-other` (all contributions).
- **Seven-point cause and effect:** `cpt:seven-point-cause-and-effect`, `prc:seven-point-cause-and-effect`, `pth:seven-point-cause-and-effect`, `trm:adhyasaya`.
- **Renunciation:** `cpt:renunciation`, `trm:ngejung`.
- **Lamrim meditation:** `prc:lamrim-meditation`, `prc:six-preparatory-practices`.
- **Taking adversity as the path:** `prc:taking-adversity-as-path`, `cpt:taking-adversity-as-path`.

### D-checklist extras

- **Consciousness and mind:** `cpt:mind-as-clarity-and-knowing`, `cpt:seven-types-of-mind`, `cpt:three-levels-of-mind-gelug`.
- **Karma, rebirth and ethics:** `cpt:four-characteristics-of-karma`, `cpt:three-sufferings`, `cpt:three-roots-nine-reasons-death`, `cpt:bodhisattva-root-downfalls`, `cpt:tantric-root-downfalls`, `cpt:three-vows` (contribution), `cpt:seven-noble-riches`, `cpt:liberation-gelug`.
- **Death:** contribution to `cpt:signs-of-dissolution`, `cpt:death-bardo-rebirth-as-three-bodies`, `prc:lojong-at-death`, `prc:lion-posture-sleep`.
- **Cosmology:** `cpt:cosmology-gelug`.
- **Restricted, summary plus the texts' own warnings only:** `prc:karmamudra` (Bodhipathapradīpa v66–68), `prc:candali`, `prc:hevajra-sadhana-sakya`, `tea:lamdre:140a.1`, `tea:lamdre:141b.2`, `tea:lamdre:141a.6`.

### Disputes

- **Owned, with both sides, then reconciled or queued:**
  - Queued: `dsp:object-of-negation-madhyamaka` (RQ-U47-1), `dsp:eight-difficult-points` (RQ-U47-2), `dsp:reality-of-universals-tibetan` (RQ-U47-3).
  - Partially reconciled: `dsp:is-the-ultimate-knowable` (P2/P1; includes Atiśa's Satyadvayāvatāra side), `dsp:prasangika-theses` (P1), `dsp:role-of-analysis-in-meditation` (P4), `dsp:monastic-higher-initiations` (P4), `dsp:bodhisattva-vow-prerequisite` (P4/P3).
  - Reconciled: `dsp:paryaya-paramartha-division` (P1).
- **Sides only, no reconciliation block, for the owning units:**
  - `dsp:prasangika-svatantrika` (Gelug and Gorampa sides; U50 owns).
  - `dsp:rangtong-shentong` (Gelug, Gorampa and Shākya Chokden sides; U50 and U48).
  - `dsp:sutra-mahamudra` (Sakya Paṇḍita, a brief Kagyu side, and the First Panchen Lama; U46 owns).
- **Referenced only:** `dsp:sudden-or-gradual` (U50).
- **Ultimate views:**
  - `ult:sakya` (caveat: not a substantial one-reality).
  - `ult:kadam`, `ult:gelug` (both: tradition denies a single ultimate substance; emptiness is a non-affirming negation).
  - `ult:ganden-oral-lineage`, plus brief views for the six sub-lineages.

### Borrowings

11 in total: `brw:kadam-to-gelug`, `brw:kadam-to-kagyu`, `brw:kadam-to-sakya`, `brw:mahasiddha-to-sakya`, `brw:sakya-to-gelug`, `brw:pramana-buddhist-to-sakya`, `brw:prasangika-to-kadam`, `brw:mahayana-to-kadam`, `brw:arya-guhyasamaja-to-gelug`, `brw:kagyu-to-gelug`, `brw:nyingma-to-sakya`.

### Corrections and notes on the brief's list

- **The "fifty-nine slogans"** is the count of the later (Jamgön Kongtrul / modern) arrangement. Chekawa's root text and Sé Chilbu's arrangement do not number them so. The slogan refs here are `point.slogan` in that later order.
- **The three Kadam lineages:** Tibetan histories disagree on who founded the lamrim and oral-instruction lines. Here they are Gönpawa/Neusurpa and Chengawa respectively, at low confidence.
- **The eight difficult points:** the eighth point is given either as the three times or as how a buddha knows conventional phenomena. Both are noted.
- **Sakya Paṇḍita's critique** is aimed at "present-day Mahāmudrā" taught without empowerment, which he likens to Hwashang's teaching. It is recorded as his claim, not as a description of Kagyu teaching.

## (2) Least-sure items (check these first for hallucination)

- **Vajra Verses readings** (`src:lamdre`): the low-confidence teachings are 139b.3, 139b.5-6, 139b.7, 140a.1, 140b.5-6, 141a.3-4, 141b.2, 141a.6, 142b.5 and 142b.6.
  - Also low confidence: `pth:lamdre-vajra-verses-grounds`, `cpt:four-authorities-lamdre` (the list of members), `trm:tsema-zhi`.
  - The originals are exact copies of the local text; the paraphrases are tentative.
- **Titles, existence and dating of Sakya secondary works:** `src:pod-ser`, `src:nyakma` (including "eleven commentaries"), `src:ngedon-rabsel`, `src:golden-lancet` (and the ban), `src:parting-from-four-attachments-gorampa`, `src:chola-jugpai-go`, `src:gyude-ngontok-jonshing`.
- **Dates and lineage positions:** Gayadhara, Seton Kunrig, Zhangtön Chöbar, Muchen, Dzongpa, Amyé Zhab, Chöje Döndrub Rinchen, Tokden Jampal Gyatso, Baso Chökyi Gyaltsen ("Khedrup's brother"), Drubchen Chökyi Dorje, Khedrup Sangye Yeshe, Umapa, Gewai Lodrö.
- **Recalled wordings:**
  - Drakpa Gyaltsen's song, which is summarised only.
  - The Lama Chöpa verses, the Migtsema and the Ganden Lhagyama opening.
  - Sakya Paṇḍita's Three Vows chapter refs and the verse on the "fool's Mahāmudrā".
  - The Good Sayings verse on the king and the sage.
- **Recalled details:**
  - The "warm hand on a shaved head" pliancy image in `phn:lrc-pliancy`.
  - The sixteen drops practice.
  - The Tsongkhapa commentary titles "Fruit Clusters of Siddhis" and "Fulfilling the Hopes of Disciples".
  - The Gelug side of `dsp:monastic-higher-initiations` and the Sakya side of `dsp:bodhisattva-vow-prerequisite`.
- **Lamrim Chenmo refs** are topic names, not pages. The Satyadvayāvatāra and Bodhipathapradīpa stanza numbers are mechanical and may differ by one or two from print editions.

## (3) Gaps (belong here but not created responsibly)

- **Lists not created:**
  - The full eighteen root and forty-six secondary bodhisattva downfalls.
  - The fourteen tantric root downfalls (only the first is named).
  - The Sakya "thirteen golden dharmas".
  - The eight later Lamdre path cycles (lam skor phyi ma brgyad).
  - Sachen's eleven commentaries individually.
  - Potowa's "Heap of Jewels" and the content of the Blue Compendium.
- **Disputes not recorded:**
  - Rendawa's reported critique of the Kālacakra and its defence.
  - The Gelug–Jonang suppression history (U48).
  - Mipham's exchanges with Gelug critics (U45).
  - The recent protector-deity controversy in the Gelug.
- **Lineages and history:**
  - The Bodong tradition (Bodong Chokle Namgyal) and Zhalu (Butön) as separate lineages are not created; Butön is grouped with the Sakya.
  - Tsongkhapa's "four great deeds" are not listed.
  - Details of the Panchen Lama numbering are only noted.
- **Local but not extracted, ready for Phase D:** Atiśa's Pañjikā (Tōh 3948), Vimalaratnalekha (4188), Cittotpādasaṃvaravidhikrama (3969), Śaraṇagamanadeśanā (3953), Mahāyānapathasādhana (3954), Ratnakaraṇḍodghāṭa (3930). The Vajra Verses deserve a full double extraction.
- **Still sought, no local text:** Chekawa's Seven Points, Langri Tangpa's Eight Verses, all of Tsongkhapa's works, Sakya Paṇḍita's works, Gorampa, the Book of Kadam, Mind Training: The Great Collection, the Lamdre commentaries. Likely places are OpenPecha and BDRC.

## (4) Out of reach

- **Oral and restricted transmissions:** the Lamdre Lobshé, the Ganden oral lineage, the single-line transmission of the Book of Kadam.
- **Restricted practices:** completion-stage and consort practices, inner heat, and the signs of the grounds. These are recorded as summaries plus the texts' own warnings only (`restricted: true`).

## Coordination notes for the orchestrator

- **Wylie-slug source ids reused from U41** instead of phonetic slugs, to avoid duplicates: `src:legs-bshad-snying-po`, `src:tshad-ma-rigs-gter`, `src:yid-dang-kun-gzhi`, `src:rnam-grel-thar-lam-gsal-byed`, `src:bsdus-grwa`. This needs an S5 decision if phonetic ids are wanted.
- **New lineage ids to log in DECISIONS.md:** `lin:ngor`, `lin:tshar`, `lin:dzongpa`, `lin:kadam-shungpa`, `lin:kadam-lamrimpa`, `lin:kadam-mengakpa`, `lin:ganden-oral-lineage`. All are real named divisions.
- **Queue entries to add to RECONCILE_QUEUE.md:**
  - RQ-U47-1: object of negation (Tsongkhapa vs Gorampa).
  - RQ-U47-2: eight difficult points.
  - RQ-U47-3: reality of universals (Sangphu vs Sakya Paṇḍita vs Gelug).
- **Possible overlaps with the parallel units:**
  - My `cpt:signs-of-dissolution` (U44) vs U45's `cpt:dissolution-stages`.
  - My `cpt:four-thoughts-that-turn-the-mind` and `prc:four-thoughts-that-turn-the-mind` vs whatever ids U45/U46 use.
  - `trm:kunzhi` (Lamdre vs Nyingma senses).
  - `obs:eight-worldly-concerns` is also defined by U40 and U45.
  - `prc:guru-yoga` is U45's.
- **Remaining undefined references are all registry-owned:** `pth:lamrim-three-scopes`, `pth:nine-stages-calm-abiding`, `pth:five-paths`, `pth:ten-bhumis`, `pth:three-trainings` (U51), and `dsp:sudden-or-gradual` (U50).
- **Resolved:** `prc:tonglen`, which U40 was waiting on, is now defined.
