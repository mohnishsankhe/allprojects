# U43-pure-land — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map B4 (Pure Land: Amitābha and the recitation of his name, through Hōnen and Shinran) and I1 (Jōdo and Jōdo Shinshū), plus Ji-shū, Yūzū Nenbutsu and later Chinese Pure Land. Generators are in `_gen/`, run in order part1 to part8. `_gen/cb.py` reads the local CBETA files and `_gen/check_refs.py` lists ids referenced here but not defined here.

**Counts:** 11 lineages, 6 ultimate views, 77 sources, 89 teachers, 193 teachings (93 with verified originals), 103 terms, 71 concepts, 27 practices, 14 obstacles, 7 paths, 14 phenomenology items, 14 disputes, 8 borrowings, 36 interpretation-log lines. Validator: 0 errors.

## 1. Coverage checklist

**Lineages owned**
- Registry lineages: lin:pure-land, lin:jodo-shu, lin:jodo-shinshu.
- New sub-lineages (please add to the registry): lin:ji-shu, lin:yuzu-nenbutsu-shu, lin:jodo-shu-chinzei, lin:jodo-shu-seizan, lin:shinshu-honganji-ha, lin:shinshu-otani-ha, lin:shinshu-takada-ha, lin:bailian-zong.
- One ult view for each lineage with a distinct view: ult:pure-land, ult:jodo-shu, ult:jodo-shinshu, ult:ji-shu, ult:yuzu-nenbutsu-shu, ult:bailian-zong. The Chinzei, Seizan and Shinshū branches point to their parent's view.

**Indian basis**
- Larger Sūtra: U39's src:sukhavativyuha-larger is referenced, not re-created. Added teachings:
  - vows 11, 12–13, 17, 19, 20, 22, 35;
  - crosswise-cutting, five-evils, verse-arrogance, womb-birth, entrustment, sutra-remains, hardest-of-hard;
  - Sanskrit skt.vow18, skt.vow19, skt.womb.
- Smaller Sūtra: tea:sukhavativyuha-smaller:skt.10 (Sanskrit §10).
- Contemplation Sūtra: tea:amitayurdhyana-sutra:intro.1–4, :9, :closing, :closing/2.
- Pratyutpanna: U39's entry referenced, plus prc:pratyutpanna-samadhi and tea:dasheng-dayi-zhang:pratyutpanna-question.
- Vasubandhu's Rebirth Treatise (five gates of mindfulness): src:wangsheng-lun (T1524, read in full); tea:wangsheng-lun:230c17-20, 230c21-22, 231a14, 231a24-25, 231b08-24, 231b24-232b04, 232b22-25, 232c03-233a04, 233a05-25; cpt:five-gates-of-mindfulness; prc:five-gates-of-mindfulness; pth:vasubandhu-five-gates; cpt:twenty-nine-adornments.
- Nāgārjuna's easy-practice chapter: U40's src:dasabhumika-vibhasa, with tea:dasabhumika-vibhasa:41b02-06, 41b13-17, 43a09-20, 43b18-19; cpt:easy-and-difficult-practice.
- Five sūtras and one treatise: tea:surangama-sutra:5.mahasthamaprapta, tea:bhadracaripranidhana:pure-land-aspiration, cpt:five-sutras-one-treatise.

**China**
- Huiyuan: tch:huiyuan-lushan; tea:gaoseng-zhuan:358c17-29 (the vow of 123 people, 402); tea:fozu-tongji:262c16-26; phn:huiyuan-visions; cpt:lotus-society.
- Tanluan (other-power): tch:tanluan; src:wangsheng-lun-zhu with 8 teachings (easy path, praise gate and three non-faiths, eight questions, two dharma-bodies, birth of non-birth, two transfers, bodhicitta, other-power); src:luelun-anle-jingtu-yi (3 teachings, local); src:zan-amituo-fo-ji (twelve lights, local).
- Daochuo (last age; two gates): tch:daochuo; src:anle-ji with 13 local teachings (time and capacity, fourth 500-year period, reward land, nianfo samādhi as king of samādhis, Tuṣita comparison, intention for another time, ten recitations, deathbed pact, birth of non-birth, the two gates).
- Shandao:
  - tch:shandao; src:guanjing-shu with 8 recalled teachings: rightly determined act and five right practices, two kinds of deep entrusting, two rivers and white path, reward land, gate of restraint, sincere mind, the Buddha's intent, postscript dream;
  - src:wangsheng-lizan with 5 local teachings: three minds, anjin–kigyō–sagyō, four modes, why calling rather than contemplation, "ten of ten born", the vow paraphrase;
  - src:guannian-famen with 3 local teachings: retreat, deathbed, five augmenting conditions;
  - the willow episode in both accounts: tea:xu-gaoseng-zhuan:684a11-18 and tea:fozu-tongji:263a22-b18.
- Other Tang works:
  - Huaigan (T1960, 3 local teachings);
  - Jingtu shiyi lun (T1961, 6 local teachings);
  - Xifang yaojue, attributed to Kuiji;
  - Wonhyo's Yusim allakdo;
  - Fazhao's five-tone chant: prc:wuhui-nianfo;
  - Feixi.
- Yongming Yanshou: tch:yongming-yanshou; tea:wanshan-tonggui-ji:966b26-c10 (the source is U42's).
- Song–Qing:
  - Zunshi: morning ten recitations, prc:morning-ten-recitations;
  - Lebang wenlei and Fozu tongji: cpt:pure-land-patriarchs;
  - Mao Ziyuan: lin:bailian-zong;
  - Tianru Weize, Chuandeng;
  - Yunqi Zhuhong (tch:yunqi-zhuhong): src:jingtu-yibian (read in full, 3 teachings) and src:amituo-jing-shuchao.
- Ouyi Zhixu: tea:amituo-jing-yaojie:faith-vow-practice, pth:faith-vow-practice-ouyi, cpt:faith-vow-practice.
- Yinguang (recent): tea:yinguang-wenchao, 2 teachings.

**Japan**
- Genshin: src:ojoyoshu with 6 teachings, including deathbed rules; prc:deathbed-rites.
- Kūya: tch:kuya, tea:nihon-ojo-gokuraku-ki:kuya.
- Ryōnin: tch:ryonin, lin:yuzu-nenbutsu-shu, tea:yuzu-nenbutsu-engi:revelation, prc:yuzu-nenbutsu.
- Hōnen:
  - Senchakushū ch. 1, 2, 3, 4, 8, 16 and postscript;
  - One-Sheet Document: tea:ichimai-kishomon:whole;
  - Seven-Article Pledge;
  - letters on one-calling and on how to live;
  - biography (conversion, Ōhara dialogue);
  - trm:senju-nenbutsu, trm:namu-amida-butsu, pth:jodo-shu-anjin-kigyo-sagyo.
- Shinran:
  - Kyōgyōshinshō: 11 teachings covering preface, kyō, gyō, shin (cause, ten benefits, Ajātaśatru), shō, true Buddha and land, transformed lands (three vows, mappō, gods) and postscript with "neither monk nor layman";
  - Shōshinge (3), wasan (5), Mattōshō letters 1, 5 (jinen hōni), antidote, equal-to-Tathāgata, Ichinen tanen mon'i, Yuishinshō mon'i, Gutokushō;
  - shinjin: cpt:shinjin, trm:shinjin;
  - paths: pth:shinran-shinjin-path, pth:shinran-three-vows.
- Tannishō, recorded by Yuien: sections 1–10, 13, 15, the postscript and Rennyo's colophon. Section 3 ("even a good person attains birth, how much more an evil person") is covered by cpt:evil-person-as-true-object and trm:akunin-shoki.
- Rennyo's letters: 5.16 (white ashes), 5.1, law of the land, heresies; cpt:one-great-matter-of-the-afterlife.
- Ippen: lin:ji-shu; Kumano oracle, dancing nenbutsu, death, "casting off"; prc:odori-nenbutsu, prc:fusan (talismans).
- Critics:
  - Myōe: src:zaijarin, bodhicitta;
  - Jōkei: src:kofukuji-sojo, nine errors;
  - Mappō tōmyōki;
  - Nichiren as a side in dsp:exclusive-nenbutsu-controversy.

**Concepts**
- Other-power and self-power: cpt:other-power, cpt:self-power, trm:tariki, trm:jiriki.
- The 48 vows and the 18th vow: our definitions added to cpt:forty-eight-vows and cpt:eighteenth-vow.
- Nine grades of birth: cpt:nine-grades-of-rebirth, pth:nine-grades-of-birth (read in T365).
- Three ages of the Dharma: cpt:three-periods-of-the-dharma, trm:mofa, trm:zhengfa, trm:xiangfa.
- Birth in the Pure Land as the condition for awakening: cpt:birth-in-the-pure-land.
- Pure Land as mind-only: cpt:mind-only-pure-land, trm:weixin-jingtu.
- Deathbed practice: cpt:deathbed-practice, cpt:deathbed-welcome.
- Faith and practice: cpt:faith-vow-practice, dsp:true-cause-of-birth.
- D-checklist per lineage:
  - consciousness: nianfo samādhi, the three minds, shinjin;
  - self: cpt:ordinary-being-fanfu;
  - body: cpt:body-in-the-pure-land;
  - ethics: three meritorious acts, cpt:precepts-and-the-nenbutsu, licensed evil;
  - signs and powers, with the warnings: seeing the Buddha, signs of birth, benefits in the present life, "visions not to be told";
  - transmission: patriarchs, seven masters, secrecy, gojū sōden;
  - cosmology: 29 adornments, true and transformed lands;
  - sound: cpt:name-embodies-all-virtues;
  - death: raigō, zhunian.

**Practices**
- Oral recitation: our lineage forms added to prc:nianfo.
- Visualization: prc:buddhanusmrti-mahayana and prc:sixteen-contemplations (U39's entries; our lineage forms, sources and warnings added).
- Ten recitations at death: prc:deathbed-rites, prc:zhunian, cpt:ten-recitations.
- Also: prc:nianfo-retreat, prc:pure-land-hymns, prc:shinshu-gongyo, prc:myogo-honzon, prc:hoonko, prc:goju-soden, prc:bekiji-nenbutsu.
- prc:shashen-wangsheng (abandoning the body to go to birth) is **restricted**: summary only, recorded as narrative.

**Disputes**
- Requested:
  - dsp:self-power-or-other-power;
  - dsp:pure-land-real-or-mind-only (new; Pure Land vs Chan);
  - dsp:one-calling-or-many-calling (new).
- Others found:
  - dsp:can-grave-offenders-be-born;
  - dsp:amitabha-land-reward-or-transformation;
  - dsp:intention-for-another-time;
  - dsp:tusita-or-sukhavati;
  - dsp:is-bodhicitta-needed-for-birth;
  - dsp:exclusive-nenbutsu-controversy (1205, 1207, 1227, Nichiren);
  - dsp:deathbed-welcome-or-settled-in-life;
  - dsp:true-cause-of-birth;
  - dsp:chan-pure-land-dual-practice;
  - dsp:can-other-practices-lead-to-birth;
  - dsp:sango-wakuran (1797–1806; recent).
- dsp:works-knowledge-grace is only referenced, from Tanluan's other-power teaching.
- **Queued, need RECONCILE_QUEUE entries:** amitabha-land-reward-or-transformation, is-bodhicitta-needed-for-birth, exclusive-nenbutsu-controversy, true-cause-of-birth, can-other-practices-lead-to-birth, sango-wakuran.

**Corrections to the brief** (found by reading the local texts)
- The Sanskrit Larger Sukhāvatīvyūha (GRETIL, Fujita) has **47 vows**, not 48. The Chinese 18th vow is the Sanskrit **19th**, which says "ten turnings of the arising of thought" and speaks of dedicating roots of good.
- The Sanskrit Smaller Sūtra §10 says "bring to mind" (manasikariṣyati) the name for one to seven nights. "Holding the name" (執持名號) is Kumārajīva's wording.
- Nāgārjuna's verse reads 無量力**威德**, not 功德.
- Daochuo frames the present as the Candragarbha's **fourth 500-year period** (the time for repentance and calling the name) as well as 末法.
- The Gaoseng zhuan records the vow of 123 people before an Amitābha image in 402. It does not use the names "White Lotus Society" or "eighteen worthies"; those are later.
- The "four alternatives" on Chan and Pure Land ascribed to Yanshou were searched for and **not found** in the Wanshan tonggui ji (T2017).
- Zongxiao's patriarch list (1200) is Huiyuan plus Shandao, Fazhao, Shaokang, Shengchang and **Zongze**. Zhipan's list of seven (1269) includes Chengyuan and Yanshou instead.
- The Xu gaoseng zhuan says a man who questioned Shandao leapt from the willow. The later Fozu tongji says Shandao himself did.
- T1980 reads 彼佛今現在**世**成佛 where the Japanese quotations have 彼佛今現在成佛.
- Only two changes to the brief's list: the Rebirth Treatise survives only in Chinese (its Sanskrit title is a reconstruction), and Yuien as compiler of the Tannishō is the prevailing view, not certain.

## 2. Least sure — check these first
- **Teachings recalled, not read locally:**
  - all of src:wangsheng-lun-zhu, src:guanjing-shu, src:amituo-jing-yaojie, src:amituo-jing-shuchao and src:dasheng-dayi-zhang;
  - all Japanese teachings;
  - most uncertain among them: tea:ojoyoshu:nenbutsu-foundation (chapter unknown), tea:ojoyoshu:2 (list of the ten pleasures), tea:kurodani-shonin-gotoroku:* (which letters), tea:honen-shonin-gyojo-ezu:* and tea:ippen-hijiri-e:* (scroll numbers), tea:mattosho:1/5/antidote/equal-to-tathagata (letter numbering), tea:rennyo-ofumi:obo and :heresies (composites of several letters), tea:yuishinsho-mon-i:tathagata-fills-world, tea:gutoku-sho:two-pairs-four-levels, tea:godensho:rokkakudo-verse, tea:yuzu-nenbutsu-engi:revelation (wording), tea:ippen-shonin-goroku:sutete-koso, tea:yinguang-wenchao:* (titles and wording), tea:guanjing-shu:4.postscript-dream.
- **Teachers:** tch:homyo, tch:shogei, tch:ryoe-doko, tch:shunjo, tch:jukaku, tch:jiezhu, tch:miaoye, tch:xingce, tch:wei-yuan, tch:daojing, tch:shotatsu, tch:akao-no-doshu. Also Zenran's dates, Huaigan's three-year story, Shaokang's coins, Fazhao's Wutai visions, and Daochuo's bean counting.
- **Sources:** src:wu-fangbian-nianfo-men and src:nianfo-jing (summaries), src:sanmai-hottokki (authenticity disputed), src:ojo-juin, src:matsudai-nenbutsu-jushuin, src:ichinen-tanen-funbetsu-ji, src:ichigon-hodan, src:yuzu-nenbutsu-engi (dates), src:kudensho, src:gaijasho, src:jingtu-shiyao.
- **Doctrinal summaries:**
  - the Chinzei and Seizan positions in their lineage entries and in dsp:can-other-practices-lead-to-birth;
  - cpt:goju-soden and prc:goju-soden;
  - cpt:four-kinds-of-nianfo (attribution to Zongmi);
  - cpt:five-sutras-one-treatise (roles of Wei Yuan and Yinguang);
  - dsp:sango-wakuran (participants omitted);
  - brw:pure-land-to-shingon and brw:huayan-to-yuzu.
- **Path bands:** all bands are interpretive. B5 for shinjin is flagged; Shinshū would object to reading it as "seeing".

## 3. Gaps
- **Texts not local, so no originals:**
  - Tanluan's Commentary (T1819), Shandao's commentary (T1753), Ouyi's Yaojie (T1762), Wonhyo's T1747, Jingying Huiyuan's T1749, Huiyuan–Kumārajīva (T1856);
  - Huiyuan's preface to the nianfo samādhi poems (T52);
  - the Pratyutpanna (T417/418);
  - all of T83/T84 (Senchakushū, Kyōgyōshinshō, Ōjōyōshū) and the Shinshū and Jōdo-shū collected texts.
- **Not created:**
  - Korean Pure Land beyond Wonhyo;
  - Vietnamese Tịnh độ;
  - Chinese Pure Land after 1800 other than Yinguang;
  - the other seven of the ten Shinshū branches (e.g. Bukkōji-ha, Kōshō-ha), the three Seizan schools as separate lineages, and the extinct Chōrakuji, Kuhon-ji and Ichinengi lines;
  - myōkōnin collections;
  - mukaekō and raigō rites and art;
  - folk dancing-nenbutsu traditions;
  - Tibetan Sukhāvatī aspiration prayers and phowa (belong to U45/U46).
- **Restricted practice:** for prc:shashen-wangsheng, explicit warnings by later Pure Land teachers against ending one's life to reach birth were not located.
- **Ids referenced but owned by other units:**
  - teachers and texts: tch:zhiyi (U54), tch:wonhyo (U55), src:rissho-ankoku-ron (U55);
  - lineages lin:tiantai, lin:faxiang, lin:huayan, lin:sanlun, lin:tendai, lin:shingon, lin:nichiren, lin:hwaeom;
  - disputes dsp:works-knowledge-grace and dsp:women-caste-liberation (U50).
- **Ids shared with U42:** tch:yongming-yanshou, tch:yunqi-zhuhong, tch:changlu-zongze, tch:zhongfeng-mingben, trm:weixin-jingtu, src:wanshan-tonggui-ji, src:xu-gaoseng-zhuan.

## 4. Out of reach
- Oral instructions of the gojū sōden.
- Secret "hidden nenbutsu" (kakushi nenbutsu) groups and Zenran's claimed secret teaching (hiji bōmon), known only through its critics.
- Chant melodies (shōmyō, the five-tone chant) as performed.
- Private Shinshū dharma talks and oral transmission in temples.
