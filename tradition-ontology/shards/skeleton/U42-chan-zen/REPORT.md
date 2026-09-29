# U42 — Chan, Seon, Zen: skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent, since subagents cannot write report files in this harness; the orchestrator saves it.)_

**Validator:** 0 errors, 1 warning (REPORT.md missing until this file is saved).

**Counts:**

| entity | count |
|---|---|
| sources | 143 |
| teachers | 228 |
| lineages | 24 |
| ultimate views | 16 |
| teachings | 244 (189 with a verified Chinese `original`) |
| terms | 125 |
| concepts | 63 |
| practices | 34 |
| obstacles | 16 |
| paths | 4 |
| phenomenology | 16 |
| disputes | 11 |
| borrowings | 6 |
| interpretation_log | 28 |

**Reference check:** `_gen/check_refs.py` confirms that every id referenced in this shard is defined here, in another skeleton shard, or in the registry.

## How it was built
- The generators are `_gen/part1…part13`, with shared helpers in `_gen/common.py`.
- `_gen/cb.py` turns CBETA TEI XML into plain text line by line and records each Taishō line and juan. `_gen/cbfind.py` and `_gen/batch_find.py` search that text.
- **Quote check.** Every `original` goes through `Z()`, which normalises punctuation and confirms the quote exists in `sources_raw/cbeta/T/<vol>/<tn>.xml`. If it does not, the build stops.
- **How teachings are referenced:**
  - Most texts: the ref is computed automatically by `ct()` as the Taishō line where the quote starts (e.g. `tea:linji-lu:496c10`), with the juan as `chapter`.
  - Platform Sūtra: refs follow the prepared segments `section.segment` (Zongbao: section 4 = ch. 1 行由 … section 13 = ch. 10 付囑; Dunhuang = CBETA 折 numbering).
  - Kōan collections: refs are case numbers (Wumenguan 1–48, Biyan lu, Congrong lu).
  - Japanese texts, which are not held locally: descriptive anchors such as `tea:genjokoan:to-study-the-self`, with no `original`.
- **Local texts read:**

  | Taishō vol. | texts |
  |---|---|
  | T47 | Linji lu, Dongshan, Caoshan, Guishan, Yangshan, Dahui yulu |
  | T48 | Hongzhi guanglu (Mozhao ming, Zuochan zhen), Rujing (two records), Biyan lu, Congrong lu, Wumenguan, Rentian yanmu, T2007/T2008 Platform Sūtra, Shaoshi liumen, Xinxin ming, Zuishangsheng lun, Chuanxin fayao, Wanling lu, Yongjia ji, Zhengdao ge, Chan Preface, Zongjing lu, Jinsim jikseol, Susim kyol, Changuan cejin, Chixiu Baizhang qinggui |
  | T50 | Xu gaoseng zhuan |
  | T51 | Lidai fabao ji; Jingde chuandeng lu juan 3, 5–15, 28, 30 |

## 1. Coverage checklist (brief items → ids)

**Lineages owned.** Each has a `lineages` entry and an `ult:` view (except Jingzhong):
- Owned by the brief: lin:chan, lin:seon, lin:zen, lin:rinzai, lin:soto, lin:obaku, lin:linji, lin:caodong, lin:yunmen, lin:guiyang, lin:fayan.
- New sub-lineages added: lin:east-mountain, lin:northern-chan, lin:heze, lin:niutou, lin:jingzhong, lin:baotang, lin:hongzhou, lin:yangqi, lin:huanglong, lin:daruma-shu, lin:fuke, lin:jogye, lin:gusan-seonmun.
- Views: ult:chan, ult:seon, ult:zen, ult:rinzai, ult:soto, ult:obaku, ult:linji, ult:caodong, ult:yunmen, ult:guiyang, ult:fayan, ult:northern-chan, ult:heze, ult:hongzhou, ult:niutou, ult:baotang. Each carries a caveat (buddha-nature ≠ an eternal self; names are expedient).

**The 28 Indian and 6 Chinese patriarchs**
- cpt:twenty-eight-indian-patriarchs.
- tea:platform-sutra:13.11 gives the list, verified locally.
- tea:platform-sutra-dunhuang:51.1 gives the different Dunhuang list.
- Teacher entries: tch:sanavasa … tch:prajnatara and tch:bodhidharma. Existing ids are reused for Mahākāśyapa, Ānanda, Upagupta, Pārśva, Aśvaghoṣa, Nāgārjuna and Āryadeva.
- Separate Chan ids for doubtful identifications: tch:vasumitra-chan, tch:buddhamitra-chan, tch:vasubandhu-chan.
- Chinese patriarchs: tch:huike, tch:sengcan, tch:daoxin, tch:hongren, tch:huineng.
- Tradition's account vs scholarly account are kept apart in each entry's `dating` and `notes`.

**Northern and Southern schools**
- Shenxiu and the Northern school: tch:shenxiu, tch:puji, lin:northern-chan, tea:platform-sutra:4.6, 11.1, 11.3.
- Shenhui and the Huatai debate: tch:shenhui, src:nanzong-ding-shifei-lun, tea:nanzong-ding-shifei-lun:huatai, dsp:huatai-true-lineage (queued), tea:platform-sutra-dunhuang:49.1, tea:platform-sutra:11.12.

**Tang masters**
- Nanyue Huairang: tea:platform-sutra:10.32; tile-polishing tea:jingde-chuandeng-lu:240c20.
- Qingyuan: tea:platform-sutra:10.31, tea:jingde-chuandeng-lu:240c02.
- Mazu: tea:jingde-chuandeng-lu:440a03 ('ordinary mind'), 254c03 ('mind is buddha' and 'plum is ripe'); tea:wumenguan:30, 33.
- Baizhang:
  - rule: src:chanmen-guishi, tea:chanmen-guishi:251a04;
  - 'a day without work': tea:chixiu-baizhang-qinggui:1119b01, 1144a27;
  - fox kōan: tea:wumenguan:2.
- Huangbo: tea:chuanxin-fayao:379c18, 380b02, 380a13, 381c05; tea:wanling-lu:387b13.
- Linji:
  - true person of no rank: tea:linji-lu:496c10;
  - four classifications: 497a22;
  - three mysteries and three essentials: 497a19;
  - four shouts: 504a26;
  - 'kill the Buddha': 500b22;
  - awakening: 504c16;
  - also 497a29, 497b17, 497c04, 498a16, 498c02, 502a12;
  - Rentian yanmu devices: 304a11, 311b16.
- Zhaozhou: tea:wumenguan:1, 7, 19, 37.
- Dongshan:
  - five ranks: tea:dongshan-yulu:525c01;
  - ranks of merit: 525c09;
  - three leaks: 513c10;
  - Baojing sanmei: tea:baojing-sanmei:515a17;
  - awakening verse: tea:jingde-chuandeng-lu:321c21.
- Caoshan: tea:caoshan-yulu:527a05.
- Shitou: tea:sandokai:459b08, 459b12, 459b15; tea:jingde-chuandeng-lu:309b13.
- Yaoshan: tea:jingde-chuandeng-lu:311c27.
- Yunmen: tea:biyan-lu:6, tea:wumenguan:21, tea:rentian-yanmu:312a07.
- Fayan: tea:rentian-yanmu:324a01, src:zongmen-shigui-lun.
- Guishan and Yangshan: tea:guishan-yulu:577c04, tea:yangshan-yulu:582a19, tea:rentian-yanmu:321c09; Xiangyan tea:jingde-chuandeng-lu:284a14; Lingyun 285a25.
- Yongjia: tea:zhengdao-ge:395c09, 396a10; tea:yongjia-ji:389b29, 390c04; tea:platform-sutra:10.33.
- Niutou: tea:xinming:457b26. Baotang and Jingzhong: tea:lidai-fabao-ji:185a13, 189a17.

**Song masters and kōan collections**
- Xuedou: src:xuedou-songgu.
- Yuanwu and the Biyan lu: tea:biyan-lu:1, 6, 12, 12.pointer (the sword that kills and gives life).
- Wumen and the Wumenguan: 48 cases confirmed locally; teachings for the preface, cases 1, 2, 3, 6, 7, 14, 18, 19, 21, 23, 29, 30, 33, 37, 41, 46, 47, and the appended Chanzhen and Huanglong's three barriers.
- Hongzhi: tea:mozhao-ming:100a26, 100b07; tea:zuochan-zhen-hongzhi:98a29; tea:hongzhi-guanglu:73c05; Congrong lu tea:congrong-lu:1.
- Dahui: tea:dahui-yulu:884c25, 921c05, 903b29, 910c22, 891b05, 891a07; tea:dahui-shu:921c08.
- Kuoan's Ten Oxherding Pictures: all ten listed in src:ten-oxherding-pictures and tea:ten-oxherding-pictures:1–10. The path map pth:ten-oxherding-pictures is referenced only (U51 owns it).
- Puming's version: tea:puming-oxherding-pictures:1-10 and pth:puming-ten-oxherding-pictures (new).

**Early texts**
- Two Entrances: tea:two-entrances-four-practices:369c21, 369c25, 370a01, and tea:xu-gaoseng-zhuan:551b27.
- Xinxin ming: 376b20, 376c05, 376c15, 377a09.
- Platform Sūtra:
  - Zongbao edition: 55 teachings;
  - Dunhuang edition: 10 teachings;
  - verse contest: 4.6, 4.11, Dunhuang 8.2 and 8.4;
  - no-thought, no-form and non-abiding: 7.3, Dunhuang 17.1;
  - samādhi and prajñā as lamp and light: 7.1;
  - formless precepts, repentance and vows: 9.2–9.5.

**Korea**
- Jinul:
  - Susim kyol: 10 teachings, including sudden awakening/gradual cultivation (1006b15, 1006c11), tracing back the radiance (1007a08, 1007a21) and powers (1006b28);
  - src:ganhwa-gyeoruiron;
  - Suseonsa and the Jogye order (lin:jogye).
- Hyujeong: tea:seonga-gwigam:seon-and-teachings.
- Taego Bou: tch:taego-bou.
- Seongcheol (recent): dsp:seon-sudden-cultivation-debate.

**Japan**
- Eisai: tea:kozen-gokoku-ron:precepts.
- Dōgen:
  - 22 Shōbōgenzō fascicles entered as separate sources, plus Fukanzazengi, Eihei kōroku, Zuimonki, Tenzo kyōkun and Hōkyōki;
  - just sitting and practice-realization: tea:bendowa:practice-realization;
  - dropping off body and mind: tea:hokyoki:dropping-off, tea:rujing-xu-yulu:136c03.
- Keizan: src:denkoroku, tea:zazen-yojinki:faults.
- Musō, Ikkyū, Bassui, Takuan, Bankei (tea:bankei-zenji-seppo:unborn, no-koan) and Suzuki Shōsan all have entries.
- Hakuin:
  - sound of one hand: tea:sekishu-onjo:one-hand;
  - great doubt: tea:itsumadegusa:bell;
  - Zen sickness, naikan and the soft-butter method: tea:yasenkanna:zen-sickness, naikan, soft-butter; prc:naikan-hakuin, prc:nanso-no-ho;
  - Orategama: tea:orategama:activity;
  - kōan curriculum: pth:hakuin-koan-curriculum.
- Ingen and Ōbaku: prc:nianfo-chan, dsp:chan-and-nianfo.
- Tōrei: tea:shumon-mujinto-ron:stages.

**Concepts in the brief** — all present:
- cpt:sudden-and-gradual, cpt:no-mind, cpt:no-thought-no-form-non-abiding;
- cpt:original-face, cpt:great-doubt, cpt:silent-illumination;
- trm:shikantaza (just sitting), cpt:kensho-seeing-nature, cpt:meditation-sickness;
- cpt:mind-to-mind-transmission, cpt:four-line-self-description, cpt:flower-sermon;
- cpt:koan, trm:huatou, cpt:inka-confirmation;
- cpt:five-houses, cpt:ordinary-mind, cpt:killing-and-life-giving-sword.

Further D-checklist items added:
- cpt:four-wisdoms-chan, cpt:four-elements-chan, cpt:tanden-energy-anatomy;
- cpt:three-bodies-in-self-nature, cpt:srenika-heresy, cpt:being-time;
- cpt:mind-only-pure-land, cpt:chan-death-and-dying, cpt:chan-view-of-powers;
- cpt:karma-after-awakening, cpt:pure-rules-qinggui.

**Practices** — all required ones present: prc:zazen, prc:shikantaza, prc:koan-introspection, prc:huatou, prc:silent-illumination, prc:naikan-hakuin, prc:kinhin, prc:samu. 26 more were added.

**Path maps**
- Referenced only (U51 owns them): pth:ten-oxherding-pictures, pth:jinul-sudden-gradual, pth:dogen-practice-realization.
- New maps owned here: pth:dongshan-five-ranks, pth:dongshan-five-ranks-of-merit, pth:puming-ten-oxherding-pictures, pth:hakuin-koan-curriculum.

**Disputes**
- dsp:sudden-or-gradual is referenced only (U50 owns it); the Chan sides are supplied as teachings (Platform Sūtra 7.3 and 11.7, Guishan, Jinul, Huangbo, Moheyan).
- New disputes owned here:
  - Required by the brief: dsp:koan-or-silent-illumination (partially reconciled; P3, P2), dsp:rinzai-or-soto (partially reconciled; P3, P4).
  - Further debates found: dsp:huatai-true-lineage (queued), dsp:hongzhou-all-activity-buddha-nature, dsp:srenika-heresy (queued), dsp:buddha-nature-of-insentient, dsp:chan-and-the-teachings, dsp:daruma-shu-precepts, dsp:seon-sudden-cultivation-debate (recent), dsp:chan-and-nianfo, dsp:indian-patriarch-lineage (queued).

**Corrections to the brief's list**
- The Dunhuang Platform Sūtra has its own lineage list (Huineng is 40th counting from the seven buddhas) and two verses by Huineng. The rebuke of Shenhui as a 'follower of intellectual understanding' is only in the Zongbao edition; the Dunhuang edition instead has a 'prophecy' read as praising Shenhui.
- No Tang text of Baizhang's rule survives. The earliest account is the Chanmen guishi (1004). 'A day without work…' is read locally in the 1338 Chixiu qinggui.
- Rujing's own recorded sayings have 心塵脫落 ('the dust of mind drops off'), not 身心脫落 ('body and mind drop off'). The latter occurs in the later Rujing xu yulu (whose independence is doubtful) and in Dōgen's Hōkyōki.
- The earliest Huike biography (Xu gaoseng zhuan, read locally) says bandits cut off his arm. The Jingde chuandeng lu says he cut it off himself.
- The Book of Equanimity is Wansong's 1224 commentary on Hongzhi's verses, not Hongzhi's own book.
- Shitou's Cantongqi uses the registry id src:sandokai.
- Wumen's appended Chanzhen also condemns 'silent-illumination heretical Chan', so the critique is not Dahui's alone.

## 2. Least-sure items (check these first)
- **Northern-school and Dunhuang texts, from memory:** the Guanxin lun and Dasheng wusheng fangbian men summaries (five expedient means); the content of Shenhui's Huatai charges, including the four-phrase characterisation of Northern practice; Moheyan's 'not thinking, not examining'; the interlocutor's name Chongyuan; the 796 recognition of Shenhui.
- **Numbers and dates, from memory:**
  - Zongmen shigui lun: the list of ten faults;
  - Dahui's Zhengfayanzang: 661 cases (1147);
  - Seonmun yeomsong jip: 1,125 cases;
  - Shūmon kattōshū: 272 cases;
  - Zenrin kushū: 1688 edition (Tōyō Eichō).
- **Attributions:** the claim that the Jinsim jikseol may be by the Jin monk Zhengyan; Hakuyū = Ishikawa Jishun; Dainichi Nōnin's death date; Gasan Jitō receiving transmission via Gessen; the tradition that Hongzhi entrusted his funeral to Dahui.
- **Kōan curriculum and oxherding:** the names of Hakuin's curriculum categories (hosshin, kikan, gonsen, nantō, kōjō, goi, jūjūkinkai, matsugo no rōkan) and their order; Puming's picture titles.
- **Five ranks:** the glosses for the five ranks of merit; all band assignments on the four new path maps (logged as interpretive, low).
- **Japanese paraphrases, no local text:** Shōbōgenzō, Fukanzazengi, Keizan's Zazen yōjinki (where the mind is placed in the palm, hairline and nose), Bankei, Hakuin. The Seon'ga gwigam opening is also unverified.
- **Minor teachers:** the Korean founders (Hongcheok, Hyecheol, Muyeom and their teachers); Niutou Zhiwei; Chuji; Doushuai's dates; the women teachers Miaodao, Wuzhuo Miaozong, Mugai Nyodai and Ryōnen Genso.
- **Jinsim jikseol, ten methods of no-mind:** items 3–10 are partly from memory.
- **Borrowings:** brw:chan-tibet (direction disputed) and brw:tendai-esoteric-zen are low confidence.

## 3. Gaps (belong here but not created responsibly)
- Vietnamese Thiền before Trúc Lâm (the Vinitaruci and Vô Ngôn Thông lines). Trúc Lâm itself is U55's.
- 20th-century Zen and Seon figures and movements: Sanbō Kyōdan (Harada, Yasutani), Kōdō Sawaki, Seung Sahn, Sheng Yen, Kusan. Recent-teacher inclusion is the user's decision (section H); only Xuyun, Gyeongheo, Mangong and Seongcheol were added.
- More women in Chan and Zen (e.g. Shido, Eshun, Satsu). Only six women were added.
- Chan funerary rites for monks and abbots (Chixiu qinggui juan 3 is local but was not extracted); Sōtō lay funeral practice.
- Zongmi's full four-school critique (U54 owns Zongmi); Yongming Yanshou's Pure Land arguments; Hakuin's attitude to nenbutsu (not asserted).
- Restricted-type austerities mentioned in these texts (burning the body or fingers, writing in blood, Ryōnen's face-scarring) are not entered as practices. They are noted only as criticised by Jinul and in teacher notes; no steps are given.
- Japanese kōan collections beyond the Shūmon kattōshū; the Keizan shingi, Denkōroku and Kyōunshū have no teachings; Ikkyū has no teaching.

## 4. Out of reach
- Not held locally:
  - Taishō vols. 80–82 (all Japanese Zen texts);
  - T85 (Dunhuang: Northern school, Lengqie shizi ji, Chuan fabao ji, Shenhui);
  - the Xuzangjing (Zutang ji, Mazu, Baizhang, Zhaozhou records, Chanyuan qinggui, Zuting shiyuan, the oxherding texts, Zongmi's Chart);
  - Korean texts other than T2019 and T2020 (Hanguk Bulgyo Jeonseo).
- All of these would need sourcing (Phase C) or download before text-verification.
- Oral and restricted: the content of the Rinzai kōan curriculum and its capping-phrase answers is transmitted privately in sanzen and is not documented here.
