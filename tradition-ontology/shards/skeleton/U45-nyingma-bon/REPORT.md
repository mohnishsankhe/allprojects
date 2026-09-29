# U45-nyingma-bon — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Unit scope: coverage map B6 (Nyingma, Dzogchen, Bön as optional), plus the parts of D/E/F/G that touch these lineages. Lineages owned: `lin:nyingma`, `lin:dzogchen`, `lin:bon`.

## Counts
| entity | n | notes |
|---|---|---|
| lineages | 10 | 3 owned; 7 sub-lineages: `lin:longchen-nyingthig`, `lin:jangter`, `lin:peling`, `lin:dudjom-tersar` (recent), `lin:chokling-tersar` (recent), `lin:zhang-zhung-nyengyu`, `lin:bon-sar` |
| sources | 125 | 50 high / 58 moderate / 17 low; 14 recent |
| teachers | 82 | 22 recent |
| teachings | 101 | 23 read in the local Derge e-texts (folio in `location.section`); 13 with an `original` |
| terms | 100 | includes Nyingma definitions added to shared Sanskrit ids (bodhicitta, dharmakāya, jñāna, samaya, abhiṣeka, bindu, nāḍī, prāṇa, guru, maṇḍala, tantra, tathāgatagarbha…) |
| concepts | 78 | |
| practices | 43 | 8 restricted |
| obstacles | 18 | |
| phenomenology | 17 | |
| paths | 5 | |
| disputes | 5 | |
| borrowings | 6 | |
| ultimate | 3 | |
| interpretation_log | 23 | |

Validator: 0 errors; the only warning is that REPORT.md is missing.

Local material used: the Derge Kangyur Old Tantra section, Tōh 828–844, read with the unit's own script (pyewts). Colophons and key passages were read for:
- Kunjed Gyalpo (D828): 84 chapters. The colophon names Śrī Siṃha and Vairocana as translators.
- Guhyagarbha (D832): 22 chapters.
- Dupa Do (D829): 75 chapters, translated from the Bruzha script by Dharmabodhi, Dānarakṣita and Che btsan skyes.
- Mañjuśrīmitra's Rdo la gser zhun (Tengyur D2591).
- Vimalamitra's Cig car 'jug pa (Tengyur D3910). The colophon names Dharmatāśīla and Yeshe De as translators.
- The Vajrakīla fragment (D439).

Everything else comes from the unit author's knowledge.

## 1. Coverage checklist (B6 and the brief's MUST-COVER list)

**Nyingma: people and history**
- Padmasambhava → `tch:padmasambhava`. It carries the tradition's account (lotus birth, Oḍḍiyāna, Samye, treasures) and the scholarly account (8th c.). Related: `cpt:eight-manifestations-of-padmasambhava`, `cpt:khen-lop-cho-sum`, `tea:pema-kathang:birth`, `tea:pema-kathang:samye`, `tea:zangling-ma:departure`, `src:pema-kathang`, `src:zangling-ma`, `cpt:zangdok-palri`.
- Other royal-period figures: `tch:vimalamitra`, `tch:vairocana-translator`, `tch:yeshe-tsogyal`, `tch:trisong-detsen`, `tch:santaraksita`, `tch:mandarava`, `tch:nyak-jnanakumara`, `tch:nubchen-sangye-yeshe`, `cpt:twenty-five-disciples`.

**Nyingma: transmission and canon**
- Kama and terma → `trm:kama`, `trm:terma`, `trm:dagnang`, `cpt:kama-terma-dagnang`, `cpt:terma-process`, `cpt:six-transmissions-of-terma`, `trm:terton`, `trm:gongter`, `trm:sater`, `trm:dayig`, `trm:kajang`, `trm:tersung`, `trm:yangter`, `tea:dudjom-chojung:terma`.
- Collections: `src:nyingma-gyubum`, `src:nyingma-kama`, `src:rinchen-terdzo`, `src:terton-gyatsa`.
- Guhyagarbha → `src:guhyagarbha-tantra` (teachings from chapters 1, 2, 2/2, 3, 4, 9 and 13, all read locally), `src:mayajala-cycle`, `trm:dagnyam-chenpo`, `cpt:great-purity-and-equality`. Commentaries: `src:konchok-drel`, `src:chogchu-munsel`, `src:osel-nyingpo`.
- Nine vehicles → `cpt:nine-vehicles`, `trm:tekpa-rimgu`, new path map `pth:nyingma-nine-vehicles`, `cpt:three-inner-tantras`, `tea:dudjom-chojung:nine-vehicles`, `tea:mengak-tawai-trengwa:views`, `tea:kunjed-gyalpo:10`.
- Mahāyoga: `trm:mahayoga-nyingma`, `cpt:eighteen-mahayoga-tantras`, `cpt:kagye`, `cpt:eight-vidyadharas`, `cpt:three-samadhis-mahayoga`, `cpt:four-vidyadhara-levels`, `pth:mahayoga-four-vidyadharas`.
- Kagye sādhana tantras (local D838–D844): `src:jampal-lezhi-khorlo`, `src:tachok-rolpa`, `src:heruka-karuna-kridita`, `src:dutsi-nga`, `src:khandroma-melce-barwa`, `src:dragngak-dupa`, `src:jigten-chotod`, `src:vajrakila-root-fragment`.
- Anuyoga: `trm:anuyoga-nyingma`, `src:dupa-do`, `src:kundu-rigpai-do`, `src:yeshe-ngamlog`.

**Dzogchen: series and canon**
- Three series → `cpt:three-series-of-dzogchen`, `trm:semde`, `trm:longde`, `trm:mengagde`, `cpt:four-cycles-of-instruction-series`, `trm:nyingthig`.
- Seventeen Tantras → `src:seventeen-tantras` plus 15 member sources: `src:dra-thalgyur`, `src:trashi-dzeden`, `src:mutik-trengwa`, `src:longdrukpa`, `src:nyida-khajor`, `src:yige-mepa`, `src:rigpa-rangshar`, `src:rigpa-rangdrol`, `src:rinchen-pungpa`, `src:kudung-barwa`, `src:dorsem-nyingi-melong`, `src:kuntuzangpo-tukyi-melong`, `src:tigle-kunsal`, `src:norbu-trako`, `src:senge-tsaldzok`.
- Kunjed Gyalpo → `src:kunjed-gyalpo` (teachings from chapters 1, 2, 4, 9, 10, 14, 31, 32, 33, 44, 45, 46 and 83, all read locally).
- Mind-series scriptures: `src:rigpai-khujug`, `src:dola-serzhun`, `src:minub-gyaltsen`, `src:tsalchen-trugpa`, `src:khyungchen-dingwa`, `src:namkha-che`, `src:semde-chobgye`.

**Dzogchen: the Indian lineage**
- Garab Dorje and the three statements → `tch:garab-dorje`, `src:tsik-sum-ne-dek`, `tea:tsik-sum-ne-dek:1`, `:2`, `:3` (Wylie originals), `cpt:three-statements-of-garab-dorje`, `src:khepa-sri-gyalpo` (recent).
- `tch:manjusrimitra`, `tch:sri-simha`, `tch:jnanasutra`.
- Testaments: `src:gomnyam-drukpa`, `src:zerbu-dunpa`, `src:chokzhag-zhipa`, `cpt:four-chokzhag`.

**Longchenpa**
- `tch:longchenpa`.
- Seven Treasuries → `src:seven-treasuries` plus `src:yishin-dzod`, `src:mengak-dzod`, `src:choying-dzod`, `src:drubta-dzod`, `src:tegchok-dzod`, `src:tsigdon-dzod`, `src:nelug-dzod`, and the autocommentary `src:lunggi-terdzo`.
- Trilogy of Natural Ease → `src:ngalso-korsum` plus `src:semnyi-ngalso`, `src:samten-ngalso`, `src:gyuma-ngalso`, `src:shingta-chenpo`.
- Nyingthig Yabzhi → `src:nyingthig-yabzhi` plus `src:vima-nyingthig`, `src:khandro-nyingthig`, `src:lama-yangtig`, `src:khandro-yangtig`, `src:zabmo-yangtig`.
- Other works: `src:rangdrol-korsum`, `src:chogchu-munsel`.

**Jigme Lingpa (1730–1798, not recent)**
- `tch:jigme-lingpa`, `src:longchen-nyingthig`, `src:yeshe-lama` (teachings on rushen, trekchö, tögal [restricted], bardo), `src:yonten-dzod`, `src:longchen-nyingthig-ngondro`, `src:rigdzin-dupa`, `src:yumka-dechen-gyalmo`, `lin:longchen-nyingthig`, `pth:yeshe-lama-path`.

**Recent Nyingma masters and works**
- Patrul (recent) → `tch:patrul-rinpoche`, `src:kunzang-lamai-shelung` (14 teachings), `pth:kunzang-lamai-shelung-ngondro`.
- Mipham (recent) → `tch:mipham`, `src:ngeshe-dronme`, `src:ketaka-mipham`, `src:osel-nyingpo`, `src:khejug`, `cpt:two-ultimates-mipham`, `cpt:four-valid-cognitions-mipham`, `cpt:sugatagarbha-nyingma`.

**Karma Lingpa and the bardos**
- Bardo Thödol → `tch:karma-lingpa`, `src:zhitro-gongpa-rangdrol`, `src:bardo-thodol`, `src:bardo-root-verses`, `src:chitak-rangdrol`.
- Concepts: `cpt:six-bardos`, `cpt:peaceful-and-wrathful-deities` (42 + 58), `cpt:dissolution-stages`, `cpt:mother-and-child-luminosity`, `cpt:bardo-of-becoming`, `cpt:thukdam`.

**Tertöns**
- `tch:nyangral-nyima-ozer`, `tch:guru-chowang`, `tch:rigdzin-godem`, `tch:pema-lingpa`, `tch:jigme-lingpa`.
- Recent: `tch:chokgyur-lingpa`, `tch:dudjom-lingpa`, `tch:jamyang-khyentse-wangpo`, `tch:jamgon-kongtrul`, `tch:terton-sogyal`, `tch:dudjom-rinpoche`, `tch:khenpo-jigme-phuntsok`.
- Also: `tch:orgyen-lingpa`, `tch:sangye-lingpa`, `tch:dorje-lingpa`, `tch:ratna-lingpa`, `tch:pema-ledrel-tsal`, `tch:terdak-lingpa`, `tch:jatson-nyingpo`.

**Concepts from the brief**
- Rigpa and sem: `trm:rigpa`, `trm:sem`, `cpt:rigpa-and-sem`, `cpt:kunzhi-and-dharmakaya`, `obs:mistaking-alaya-for-awareness`.
- The ground: `cpt:ground-dzogchen`, `trm:zhi`, `trm:kadag`, `trm:lhundrub`, `cpt:primordial-purity`, `cpt:spontaneous-presence`, `cpt:youthful-vase-body`, `cpt:eight-gateways-of-spontaneous-presence`, `cpt:ground-appearances-and-delusion`, `cpt:one-ground-two-paths`, `cpt:three-kinds-of-ignorance`.
- Three aspects: `cpt:essence-nature-compassion`, `trm:ngowo`, `trm:rangzhin`, `trm:tukje`.
- Trekchö: `prc:trekcho`.
- Restricted, summary only: tögal `prc:togal`, dark retreat `prc:dark-retreat`.
- Four visions: `cpt:four-visions-dzogchen`, `trm:nangwa-zhi`, phenomenology `phn:four-visions-1` to `-4`. The path map `pth:dzogchen-four-visions` belongs to U51; I only referenced it.
- Rainbow body: `cpt:rainbow-body`, `trm:jalu`, `phn:rainbow-body-signs`.
- Ngöndro: `prc:ngondro-nyingma`, `prc:four-thoughts-that-turn-the-mind`, `cpt:four-thoughts-that-turn-the-mind`, `prc:refuge-and-prostration`, `prc:generating-bodhicitta`, `prc:vajrasattva-purification`, `prc:mandala-offering`, `prc:kusali-offering`, `prc:guru-yoga`.
- Three roots: `cpt:three-roots`, `trm:tsawa-sum`.
- Phowa (restricted): `prc:phowa`, `phn:phowa-signs`.

**Bön (optional)**
- Teachers: `tch:tonpa-shenrab`, `tch:tapihritsa`, `tch:nangzher-lopo`, `tch:shardza-tashi-gyaltsen` (recent), `tch:tenzin-namdak` (recent), and six others.
- `lin:bon` (Yungdrung Bön), `lin:zhang-zhung-nyengyu`, `src:zhang-zhung-nyengyu`.
- Nine ways → `cpt:bon-nine-ways`, `pth:bon-nine-ways`.
- Other concepts: `cpt:bon-kunzhi-and-rigpa`, `cpt:four-transcendent-lords`, `cpt:bon-four-portals`, `cpt:olmo-lungring`.
- Relation to Buddhism → `dsp:bon-and-buddhism`, with the Buddhist historians' side flagged `reported_by_opponent`.
- `ult:bon`.

**Practices from the brief**
- Deity practice: `prc:generation-stage-mahayoga`, `prc:nyendrub`, `prc:kagye-sadhana`, `prc:vajrakilaya-practice`.
- Tsa-lung (restricted): `prc:tsa-lung`.
- Owned by U45: `prc:vase-breathing` (restricted) and `prc:nine-round-purification`.
- Also: `prc:direct-introduction`, `prc:rushen`, `prc:mind-searching`, `prc:shine-dzogchen`, `prc:dream-yoga`, `prc:bardo-practice`, `prc:liberation-through-hearing`, `prc:jangchog`, `prc:tsok-feast` and others.

**Phenomenology, disputes and ultimate views**
- Nyams: `phn:nyams-bliss-clarity-nonthought`, `cpt:nyams-bliss-clarity-nonthought`.
- Dzogchen and Chan (with the Samye background and the white-panacea critique, which U47 owns) → `dsp:dzogchen-and-chan`. It is partially reconciled under P4, relying on Kunjed Gyalpo ch. 44, which says those without the fortune for Dzogchen should practise cause and result. It links to U50's `dsp:sudden-or-gradual`.
- Ultimate views: `ult:nyingma`, `ult:dzogchen`, `ult:bon`.

**Added beyond the brief**
- Disputes: `dsp:authenticity-of-nyingma-tantras`, `dsp:authenticity-of-terma`, `dsp:mipham-gelug-madhyamaka` (recent).
- Borrowings: `brw:vajrayana-to-nyingma`, `brw:chan-dzogchen` (disputed), `brw:nyingma-bon-dzogchen`, `brw:dzogchen-to-kagyu`, `brw:nyingma-to-rime`, `brw:tathagatagarbha-to-nyingma`.

**Corrections and precisions to the brief (from the local texts)**
- The Kunjed Gyalpo has 84 chapters. Its chapter 31, "the six vajra lines", is the Cuckoo of Awareness verbatim. Its chapter 30 bears the title of "the never-falling victory banner".
- The Dupa Do is 75 chapters and was translated "from the script of Bruzha".
- The Guhyagarbha root has 22 chapters. Its famous "e ma'o … from the unborn all is born" stanza is in chapter 2, not chapter 1.
- Jigme Lingpa is pre-1800 and is not flagged recent.

## 2. Least sure (check these first)
- The thirteen later mind-series titles (`src:semde-chobgye`). Membership of the Seventeen Tantras: 15 titles given, 2 not recalled.
- Titles of the testaments `src:gomnyam-drukpa` and `src:zerbu-dunpa`.
- Class assignments of the local Kagye tantras:
  - D840 assigned to the Yangdag class.
  - D842 assigned to the Mamo class.
- Recension and classification of other local tantras:
  - Which Guhyagarbha recension D834 is.
  - Whether D830 belongs to Anuyoga.
- Member lists reconstructed from memory: `cpt:eight-gateways-of-spontaneous-presence`, `obs:four-ways-of-straying`, `cpt:four-lamps`, `cpt:eight-vidyadharas`, `cpt:eighteen-mahayoga-tantras`, `obs:eight-intrusive-circumstances`, the colour pairings in `cpt:five-lights-and-elements`, and the similes in `phn:shine-five-experiences`.
- Chapter- or section-level references:
  - Longchenpa: `tea:choying-dzod:ch1`, `tea:tsigdon-dzod:ch3-5`, `tea:tegchok-dzod:trekcho-togal`, `tea:drubta-dzod:atiyoga`.
  - Other works: the Samten Migdrön sections, `tea:mengak-tawai-trengwa:atiyoga`, `tea:tegchen-tsuljug:1`, `tea:konchok-drel:1`.
- The paraphrase of `tea:kunjed-gyalpo:14`, whose chain of reasoning is compressed (low confidence).
- Dates: Pema Ledrel Tsal (left undated), Karma Lingpa (1326–1386), Zurpoche, Meu Gongdzö, Dru Gyalwa Yungdrung, Loden Nyingpo, Rigdzin Ngagi Wangpo, Palyul/Dzogchen founders, Shardza's Legshe Dzöd (1922), and Tönpa Shenrab 16,017 BCE (a traditional reckoning, low confidence).
- Bön items at low confidence: `src:yangtse-longchen`, `src:kusum-rangshar`, `src:ma-gyud`, `src:sipai-dzopuk`, `src:gyalwa-chaktri`, the fifteen sessions of the A-tri, `cpt:bon-four-portals`, `cpt:four-transcendent-lords`, `lin:bon-sar`.
- The critics' attributions in `dsp:authenticity-of-nyingma-tantras` (Yeshe Ö's and Zhiwa Ö's ordinances, 'Gö Khukpa Lhetse, Butön's exclusion) and the terma sceptics' loci in `dsp:authenticity-of-terma`.
- Gelug opponents named in `dsp:mipham-gelug-madhyamaka` (Pari Rabsel, Drakar Lobzang Palden).
- Band assignments in `pth:mahayoga-four-vidyadharas` (low) and `pth:yeshe-lama-path`.

## 3. Gaps (belong in scope, not created responsibly)
- The two further Seventeen Tantras. Full lists of the eighteen Mahāyoga tantras (the practice and activity tantras) and of the Anuyoga root sūtras.
- The space-series (klong sde) texts and its nine spaces.
- The 21 semdzin exercises; the twelve Dzogchen teachers (ston pa bcu gnyis).
- The Nyingma higher bhūmis (the 16-ground scheme beyond the ten).
- A complete list of the 25 disciples; the hundred-plus tertöns individually.
- Mindroling, Katok and Palyul traditions in detail; the ngakpa family lineages; the Nyingma shedra curriculum (overlaps with U48 Rimé).
- Nyingma Gyubum contents and volume counts, deliberately omitted.
- Dunhuang Dzogchen manuscripts (Pelliot numbers).
- Nupchen's chapter structure.
- Bön: the canon's structure and volume counts, the monastic (drang srong) vows, the lower four ways' rites in detail, the Menri abbatial lineage, New Bön founders and texts, Bön medicine and astrology, and the Mother Tantra practices.

## 4. Out of reach (restricted, oral, not local)
- Restricted, recorded as summary plus the texts' own warnings only (`restricted: true`): `prc:togal`, `prc:dark-retreat`, `prc:trulkhor`, `prc:tsa-lung`, `prc:vase-breathing`, `prc:completion-stage-anuyoga`, `prc:phowa`, `prc:liberation-rite`, and the teachings `tea:yeshe-lama:togal`, `tea:tegchok-dzod:trekcho-togal`, `tea:kunzang-lamai-shelung:3`. No steps, counts or durations are recorded.
- Oral instruction is the tradition's own requirement for tögal key points, dark retreat and tsa-lung, as stated in the Yeshe Lama and in Kunjed Gyalpo ch. 83.
- Not local, so unverified in this phase: every Nyingma and Bön text except Tōh 828–844, 439, 2591 and 3910. That includes the Nyingma Gyubum, the Seventeen Tantras, Longchenpa, Jigme Lingpa, the terma cycles and the whole Bön canon. Tōh 4726 (Garland of Views) lies beyond the local Tengyur index, which stops at D4464.

## Decisions (please log in DECISIONS.md)
- **Bön family.** `lin:bon`, `lin:zhang-zhung-nyengyu` and `lin:bon-sar` use `family: "shared"`, because Bön is neither Vedic nor an Indian śramaṇa tradition. Each is noted "Optional (Bön)".
- **Homonym ids.**
  - `trm:mahayoga-nyingma` and `trm:anuyoga-nyingma` are kept apart from the haṭha `trm:mahayoga` and the Jain `trm:anuyoga`.
  - `tch:samantabhadra-adibuddha` (the primordial buddha) is kept apart from `tch:samantabhadra` (the bodhisattva, U39).
- **Recent flags.**
  - Getse Paṇḍita and Jigme Gyalwai Nyugu are flagged recent.
  - Jigme Trinle Özer (1745–1821) is not flagged.
- **Nine-vehicles bands.** `pth:nyingma-nine-vehicles` and `pth:bon-nine-ways` have no bands assigned, because they are doxographical hierarchies, not stages of one person's path.
- **Reconcile queue.** Add three entries to RECONCILE_QUEUE.md:
  - RQ-U45-1: `dsp:authenticity-of-nyingma-tantras`
  - RQ-U45-2: `dsp:authenticity-of-terma`
  - RQ-U45-3: `dsp:bon-and-buddhism`
