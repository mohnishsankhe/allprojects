# U22-tamil-siddha — skeleton sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the U22 subagent; the orchestrator saves it.)_

**Owns:** lin:tamil-siddha and lin:siddha-medicine (parent: lin:tamil-siddha). No other sub-lineages were created.

**Counts:** sources 47 · lineages 2 · teachers 37 · teachings 157 · terms 98 · concepts 60 · ult 2 · practices 26 · obstacles 13 · phn 12 · paths 1 · disputes 6 · borrowings 9 · interpretation_log 68. Validator: 0 errors.

## Method
- Every entry is `skeleton`.
- **Local text checks.** The Tamil e-texts under `sources_raw/.../4_drav/tamil/pm/` are GRETIL Devanāgarī transliterations of Project Madurai files. I romanized them to read them (with a scratch script outside the shard). Then `_gen/extract_local_verses.py` pulled the exact verses into `_gen/local_verses.json`. These files were checked:
  - the Siddhar songs, series I: Aḻukaṇṇi, Rāmatēvar, Kaṭuveḷi, Kuṭampai, Caṭṭaimuṉi, Tirumūla ñāṉam, Tiruvaḷḷuvar ñāṉam;
  - Paṭṭiṉattār (series II);
  - Pattirakiriyār's Meyññāṉap pulampal (231 couplets);
  - Tirumantiram verses 1–883 (with gaps);
  - Kuṟaḷ 941–950.
- **Teachings with originals.** 124 teachings carry the exact e-text wording as `original` (script: Devanāgarī transliteration of Tamil). I left the original out in three cases:
  - all 9 restricted teachings;
  - verses whose e-text line has conversion noise (TM 552 and 641, Tiruttillai 17, the Tiruvaḷḷuvar ñāṉam invocation);
  - teachings recalled from memory.
- **Memory teachings.** 21 teachings come from memory, with no original. They are cited by their opening words (incipit) because verse numbers differ between editions: Sivavākkiyar (6), Pāmbāṭṭi (2), the Paṭṭiṉattār narrative verses (3), Tāyumāṉavar (7), Bogar, Vināyakar akaval, and Aḻukaṇṇi 21–22 (a restricted summary).
- **Tirumantiram overlap with U18.** U18 already has TM 270, 724, 1823, 2104, 2397 and 63, so I only reference them. I added TM 67, 69, 70, 552, 641, 643, 722, 725 and 727.
- **Restricted material** (vāci retention, mineral/mercury kaṟpam, alchemy and muppu, amuri, kēcari, hostile rites, living samādhi): these are summaries plus the texts' own warnings only. Nothing else is recorded.

## 1. Checklist (coverage map A7 Tamil Siddhars; I2 Pattinattar and Thayumanavar; the brief's MUST-COVER list)

**The eighteen Siddhars and their lists**
- The lists are in cpt:eighteen-siddhars, recorded as four separate definitions:
  - (1) the popular list with samādhi places;
  - (2) the Tirumantiram's own lineage verses (tea:tirumantiram:67 and :69), checked locally;
  - (3) the poets in the anthology, checked locally;
  - (4) a note that other lists vary.
- cpt:tirumular-lineage-lists covers TM 67–70.

**Teachers**
- These entries are this unit's contribution to other units' registry teachers: tch:agastya, tirumular, bogar, sivavakkiyar, pambatti, idaikkadar, karuvurar, konganar, sattaimuni, nandi (Nantīcar), patanjali, valmiki, tiruvalluvar.
- New ids for the rest of the popular list: tch:sundaranandar, ramadevar, kudambai, kamalamuni, macchamuni, korakkar, dhanvantari.
- New ids for the anthology poets: tch:azhukanni, kaduveli, akappey-siddhar, pattinattar, bhadragiriyar.
- Other new ids: tch:tayumanavar, mauna-guru, pulippani, kalangi-nathar, kanjamalaiyar, teraiyar, yugimuni, kakapusundar, romarishi, pulastiyar, vyaghrapada, avvaiyar.
- Each carries a historicity value; the tradition's accounts are labelled as such.

**Paṭṭiṉattār**
- Entries: tch:pattinattar, src:pattinattar-padalgal and 5 sub-works, and the 5 poems in the eleventh Tirumuṟai (attribution marked disputed).
- 17 teachings.
- dsp:pattinattar-identity, queued. It covers the conflation of two or more poets under one name.

**Tāyumāṉavar**
- Entries: tch:tayumanavar, src:tayumanavar-padalgal, src:paraparakkanni.
- 7 teachings.
- Related concepts and practice: cpt:samarasa, cpt:cumma-iruttal, prc:cumma-iruttal.

**Sivavākkiyar**
- src:sivavakkiyam, with 6 teachings: stone image, caste, temple within, 'running to the light', the rebirth verse, the Vedas (thematic).

**Section-D concepts**
- the ninety-six principles: cpt:ninety-six-tattvas and trm:tonnurraru-tattuvam, anchored in Aḻukaṇṇi 19;
- kāya kaṟpam: cpt:kaya-kalpa, prc:kaya-kalpa (restricted), prc:karpa-mulikai;
- kāya-siddhi: cpt:kaya-siddhi;
- vāci yoga: prc:vasi-yoga (restricted), cpt:vasi;
- the critiques: cpt:siddhar-critique-of-caste, -of-idols-and-ritual, -of-pilgrimage, -of-scripture-and-learning;
- code language: cpt:paripasai, trm:paripasai;
- the body as temple: cpt:body-as-temple;
- immortality claims: cpt:siddhar-immortality-claims, cpt:jiva-samadhi, cpt:cakamal-catal;
- alchemy: cpt:muppu, prc:siddha-alchemy (restricted);
- the ultimate and its terms: cpt:tamil-siddha-ultimate, cpt:vetta-veli, cpt:valai-manonmani;
- the self, mind and states;
- energy anatomy: cakras, nāḍīs, ten vāyus, kuṇḍalinī, five sheaths, three maṇḍalas, and a new map of the deities of the supports (cpt:siddha-cakra-deities, from Pattirakiriyār 66–72, checked locally);
- the guru, the Siddha ethic, karma and rebirth, liberation, aṇṭam–piṇṭam (macrocosm and microcosm), the letters a and u, sound and mantra, āyuḷ parīṭcai (testing the span of life);
- the view of women, recorded faithfully.

**Siddha medicine**
- the three humours: cpt:three-humours-siddha and trm:mukkurram / vata / pitta / kapha (Tamil vaḷi, aḻal, aiyam), anchored in tea:tirukkural:941;
- the eight examinations: cpt:envagai-thervu;
- the pulse: cpt:siddha-nadi-pulse;
- urine signs: cpt:neerkkuri-neikkuri;
- cpt:4448-diseases;
- the seven body-constituents, six tastes and three drug classes;
- the 32 internal and 32 external forms of medicine;
- cpt:parpam-centuram and cpt:pasanam: names and warnings only;
- the tradition's account of transmission;
- medical texts: Bogar 7000, 6 Agastya works, 4 Tēraiyar works, Yūki, Kōrakkar, Koṅkaṇar, Pulippāṇi, Tirumūlar, Yākōpu, plus four 20th-century compilations (the two with dates recalled are flagged recent);
- practices prc:siddha-daily-regimen and prc:tokkanam.

**Relations to other units**
- Tirumūlar and the Tirumantiram (U18): brw:tirumantiram-to-tamil-siddha.
- The Nāths (U21): brw:natha-tamil-siddha; Maccamuṉi and Kōrakkar linked to Matsyendra and Gorakṣa.
- Varma kalai (U58): cpt:varmam, trm:varmam, brw:siddha-medicine-to-varma-kalai.
- Vallalar (U52): brw:tamil-siddha-to-vallalar, cpt:samarasa.
- Also: brw:srividya-tamil-siddha (from Caṭṭaimuṉi's 43 triangles), brw:advaita-tamil-siddha, brw:rasa-sastra-tamil-siddha, brw:ayurveda-siddha-medicine, brw:mahasiddha-tamil-siddha (a scholarly hypothesis).

**Disputes**
- dsp:siddha-vs-agamic-saivism: partially reconciled under P4, with Siddhānta's objections recorded.
- dsp:kaya-siddhi-or-jnana: P4, partial.
- dsp:siddhar-veda-and-scripture: P4, partial.
- dsp:siddhar-rebirth: queued (on Sivavākkiyar's 'the dead are not born again').
- dsp:pattinattar-identity: queued.
- dsp:siddha-ayurveda-relation: queued.
- The caste teachings are tagged with dsp:women-caste-liberation (U50 owns it).

**Other**
- Path map: pth:tirumantiram-eight-limbs, banded like the Yoga Sūtra's eight limbs; pth:saiva-siddhanta-four-padas (U51) is referenced.
- ult:tamil-siddha and ult:siddha-medicine.
- 12 phenomenology items.
- 13 obstacles: new ones such as thieving senses, desire for women, intoxicants, false garb, outward ritualism, caste pride, the restless mind; plus contributions to shared entries such as three-esanas, three-malas, iruvinai, siddhis-as-obstacles.

## Corrections to the task's list
- "Azhukkaṇṇi": the local e-text spells it Aḻukaṇi (aḻukaṇic cittar). I used Aḻukaṇṇi, with id tch:azhukanni.
- Pattirakiriyār's text is 231 couplets. Each asks "ekkālam?" ("when will the day come?"). It is not a list of statements.
- Kuṭampai's song argues against kaṟpam, mantra, seals and yoga for the realized person. This gives an internal Siddhar dispute (dsp:kaya-siddhi-or-jnana).
- Kaṭuveḷi 8 tells the reader to stand by the rule of the Veda, so "the Siddhars reject the Veda" does not hold for every Siddhar. The dispute dsp:siddhar-veda-and-scripture records both voices.
- Pattirakiriyār 151 uses the Śaiva Siddhānta triad pati–paśu–pāśa, so the Siddhar–Siddhānta line is not a clean break.
- I added one Tirumantiram anchor to the humours: TM 727 names aiyam, vātam and pittam removed at different times of day.

## Id conventions
- Tamil personal names follow the registry's conventional romanization: kudambai, kaduveli, azhukanni, sundaranandar, bhadragiriyar.
- tch:tayumanavar uses the IAST slug, because the registry has no id for him.
- Titles use IAST slugs (e.g. src:sattaimuni-nanam, src:bhadragiriyar-meynana-pulampal).

## 2. Least sure (check these first)
- The samādhi places in the popular list of eighteen, and whether that list matches the printed sources (Abhidhāna Cintāmaṇi; Zvelebil's *The Poets of the Powers*).
- **The membership of the ninety-six principles (cpt:ninety-six-tattvas).** The total of 96 is certain. The breakdown I used (including "kaṉma viṭayam 5" and excluding the nine openings) is low confidence. The lists of the eight passions and the three desires are also low.
- **Medical and alchemical works.** These titles and ascriptions are low confidence:
  - src:akattiyar-vaittiya-cintamani, paripuranam, kunavakatam, paripasai, 12000, nanam;
  - src:teraiyar-yamaka-venpa, kunavakatam, noy-anuka-viti;
  - src:yuki-vaittiya-cintamani, korakkar-malai-vakatam, konganar-vata-kaviyam, pulippani-vaittiyam, tirumular-karukkitai-vaittiyam, yakopu-vaittiyam, citta-vaittiya-tirattu;
  - the compilers and dates of Kuṇapāṭam and Nōy nāṭal.
- **Siddha medicine details:** the pulse ratio 1 : ½ : ¼ and the finger placement; the neykkuṟi oil-drop shapes; the 108 varmam count (12 + 96); the examples of the 32 + 32 forms; the kaṟpa herbs named.
- **Life stories:** Tēraiyar's frog story, Pulippāṇi's tiger and the Palani priestly line, Rāmatēvar's Mecca / Yākōpu account, Sundarānandar and the stone elephant, Iṭaikkāṭar and the nine planets, Koṅkaṇar's crane, Pāmbāṭṭi meeting Caṭṭaimuṉi.
- **Tāyumāṉavar:** the section names (Tējōmayāṉantam, Cittarkaṇam, Mauṉakuru vaṇakkam) behind my memory teachings, the ~1,452 stanzas and ~389 Paraparakkaṇṇi couplets, his birthplace at Vedāraṇyam, and his samādhi at Lakṣmīpuram.
- **Sivavākkiyar:** the wording of all 6 memory teachings. In particular, the scope of the "kaṟanta pāl" rebirth verse. Also the identification with Tirumaḻicai Āḻvār.
- The five poems in the eleventh Tirumuṟai (the local file stops at pācuram 825).
- Paraphrases of the obscure verses: Rāmatēvar 10, Caṭṭaimuṉi 5, Tiruvaḷḷuvar ñāṉam 13, 14 and 17, TM 643. All are marked low.

## 3. Gaps (could not responsibly create)
- **Iṭaikkāṭar:** no teaching. I cannot recall any verse wording, so none was invented. The brief asked for Iṭaikkāṭar critique teachings.
- **Akappēy and Pāmbāṭṭi:** only thematic or low teachings; no verse-level wording.
- **Missing e-texts:** the Civavākkiyam, Pāmbāṭṭi, Iṭaikkāṭar, Akappēy and Tāyumāṉavar texts are not in the local e-texts. They are needed in Phase C/D (Project Madurai has them).
- The full contents of the printed Siddhar anthology (Periya ñāṉakkōvai), and the other lists of eighteen (for example the Abhidhāna Cintāmaṇi list).
- Tirumantiram tantras 4–9 are not local. For the Siddha-relevant sections (Vālai and the cakras, the 96 tattvas if the text gives them) I cite only the section titles of the 3rd tantra.
- Siddhar cosmology beyond aṇṭam–piṇṭam and the seasons; how a teacher is tested (beyond "the guru comes of his own accord" and "seek the āriyaṉ").
- Recent (post-1800) Siddha teachers and the institutions of Siddha medicine were not attempted beyond Vallalar, which is referenced to U52.
- **Dangling cross-references:** these guessed ids are for other units to create or merge: cpt:marma, cpt:rasayana, cpt:sandhya-bhasa, cpt:seven-dhatus, cpt:sunyata, cpt:tridosa, prc:rasayana, prc:svara-yoga, prc:yoga-nidra, trm:astavidha-pariksa, trm:marma, trm:rasayana, trm:yoga-nidra.
- **Registry ids not yet created by their owners:** lin:ayurveda, lin:rasa-sastra, lin:mahasiddha, lin:vallalar, lin:varma-kalai, dsp:women-caste-liberation, pth:saiva-siddhanta-four-padas, src:caraka-samhita.

## 4. Out of reach
- Palm-leaf medical and alchemical manuscripts and family physician lineages (oral transmission).
- Muppu, the pāṣāṇam processing and the kaṟpam preparations. These are deliberately veiled by the tradition and restricted here.
- Varmam point locations and techniques (restricted; owned by U58).
- The living samādhi-shrine cults and their oral lore (section I5, left for U59).
