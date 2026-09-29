# U39-mahayana-sutras — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map B4, the Mahāyāna sūtras and buddha-nature (the Tathāgatagarbha sūtras and the Ratnagotravibhāga). This unit owns lin:mahayana and lin:tathagatagarbha, plus the three Pure Land sūtra source entries. Generators are in `_gen/` (part1–part8). `texts.py` is the reader for the local e-texts; `check_refs.py` finds dangling ids.

Counts: 2 lin · 2 ult · 98 src · 53 tch · 265 tea · 139 trm · 87 cpt · 38 prc · 14 obs · 14 phn · 3 pth · 8 dsp · 13 brw · 22 interpretation-log lines.

Validator: 0 errors.

Of the 265 teachings, 171 were located in local texts and 91 quote the original. The texts used were:
- GRETIL Sanskrit (Vaidya's BST editions, Harrison–Watanabe and Gilgit Vajracchedikā, Johnston's RGV, the Potala-manuscript Vimalakīrti, Kimura's Pañcaviṃśati, Vorobyova-Desyatovskaya's Kāśyapaparivarta);
- CBETA Chinese: T235, T251, T353, T360, T365, T366, T374;
- the Derge Kangyur/Tengyur title catalogue, for Tōhoku numbers.

## Locator conventions (stated in each source's notes)
- **Aṣṭasāhasrikā:** chapter (parivarta) 1–32, with Vaidya's page.
- **Vajracchedikā:** Conze's section numbers, with the Taishō T235 lines.
- **Heart:** sentences s1–s10 of the short recension, long.1–2 for the long one.
- **Lotus:** Kumārajīva's 28-chapter numbering (as the brief uses), with the Sanskrit chapter and Vaidya page.
- **Vimalakīrti:** Sanskrit chapter.paragraph (vkn), with Kumārajīva's chapter.
- **Laṅkāvatāra:** chapter.pPAGE (Vaidya).
- **RGV:** Johnston's chapter.verse.
- **Mahāparinirvāṇa:** T374 juan (fascicle).
- **Śrīmālā:** T353 chapter.
- **Saṃdhinirmocana:** Lamotte's Tibetan chapter numbering.
- **Avataṃsaka:** 80-fascicle chapter numbering.
- **Gaṇḍavyūha:** Vaidya's section number.

## 1. Checklist (brief items → ids)
- **Perfection of Wisdom**
  - 8,000 lines: src:astasahasrika-prajnaparamita (32 chapters) and tea:…:1, 1/2–1/5, 2, 2/2, 3, 6, 7, 8, 11 (Māra's deeds), 12, 14, 16, 16/2, 17, 19, 20, 22, 24, 26, 30 (Sadāprarudita), 31 (Dharmodgata), 32.
  - Māra's deeds are also obs:mara-deeds. The irreversibility signs are cpt:signs-of-irreversibility and phn:astasahasrika-irreversible-signs.
  - 25,000 lines: src:pancavimsatisahasrika-prajnaparamita; the list of emptinesses is tea:…:1 and cpt:twenty-emptinesses (twenty items, read locally).
  - 100,000 lines: src:satasahasrika-prajnaparamita (source only).
  - Other PP texts: 18,000 and 10,000 lines, Ratnaguṇasaṃcayagāthā, Saptaśatikā, Adhyardhaśatikā, Suvikrāntavikrāmin, Svalpākṣarā, Kauśika, Ekākṣarī, T220, Renwang.
- **Diamond:** src:vajracchedika with 31 teachings covering §§2–32.
  - "A is not A, therefore called A": tea:vajracchedika:8, 13, 17, 20, 30 and cpt:diamond-dialectic.
  - "A mind that abides nowhere": tea:vajracchedika:10, 10/2.
  - The final verse: tea:vajracchedika:32 (nine similes, Gilgit Sanskrit) and 32/2 (Kumārajīva's six); cpt:diamond-nine-similes.
- **Heart:** src:prajnaparamita-hrdaya with tea s3, s4, s6, s7, s8, s9 (the mantra), long.1 and long.2 (the long version).
- **Lotus:** src:saddharmapundarika.
  - Skillful means and the one vehicle: tea ch. 2, 2/2–2/4.
  - Parables: burning house (3), lost son (4), medicinal herbs (5), conjured city (7), jewel in the robe (8), topknot jewel (14), physician (16); collected in cpt:lotus-seven-parables.
  - Eternal lifespan: 16 and 17. Nāga princess: 12/2. Avalokiteśvara: 25.
  - Also: 1, 10, 11, 12, 15, 18, 20, 21, 23 (restricted), 26, 28.
  - Companions: src:wuliangyi-jing and src:guan-puxian-jing.
- **Avataṃsaka:** src:avatamsaka-sutra (60- and 80-fascicle versions given as alternate titles); tea 1, 5, 11, 16, 20, 37.
  - **Gaṇḍavyūha:** src:gandavyuha; tea 3, 28, 30, 44, 54, 55, 56. The full list of Sudhana's friends, read from the local headings, is in cpt:sudhana-spiritual-friends. Samantabhadra's vows: src:bhadracaripranidhana and cpt:samantabhadra-vows.
  - **Daśabhūmika:** all ten grounds by name (tea 1–10, cpt:ten-bhumis, terms trm:pramudita … trm:dharmamegha).
- **Laṅkāvatāra:** src:lankavatara-sutra.
  - Eight consciousnesses: 2.p20, 2.p52; cpt:eight-consciousnesses.
  - Ālaya = tathāgatagarbha: 6.p90; cpt:alaya-tathagatagarbha-identity.
  - Mind-only: 2, cpt:mind-only.
  - Four dhyānas: 2.p41, pth:lankavatara-four-dhyanas.
  - Meat chapter: 8.
  - Also: sudden and gradual purification 2.p25; five lineages 2.p27; icchantika 2.p28; the garbha is not the tīrthikas' self 2.p33; "not a syllable" 3.p59; finger and moon 3.p80.
- **Vimalakīrti:** src:vimalakirtinirdesa.
  - Silence: 8.33 (Kumārajīva ch. 9).
  - The goddess and Śāriputra: 6.14.
  - The sick bodhisattva: 4.7, 4.12, 4.16.
  - Pure land in the pure mind: 1.14.
  - Also: 2.3, 2.7, 3.3, 3.44, 5, 6.1, 7.2, 8.31, 8.32, 9, 10, 11.
- **Saṃdhinirmocana:** src:samdhinirmocana-sutra.
  - Three turnings: 7/2, cpt:three-turnings.
  - Three natures and three naturelessnesses: 6 and 7.
  - Ādāna-vijñāna: 5.
  - Śamatha and vipaśyanā: 8.
  - Also: 2, 3, 4, 9, 10.
- **Śrīmālā:** src:srimaladevi-sutra with T353 chapters 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13.
- **Tathāgatagarbha Sūtra:** nine similes in tea:tathagatagarbha-sutra:2 and cpt:tathagatagarbha-nine-similes.
- **Mahāparinirvāṇa:** src:mahaparinirvana-sutra-mahayana.
  - Buddha-nature in all beings: juan 7, 27, 27/2.
  - Permanence, bliss, self, purity: juan 2 and cpt:four-guna-paramitas.
  - Icchantika: juan 9, 26, 27/2, 36.
  - Also: meat (4), vajra body (3), the blind men and the elephant (32), Kauṇḍinya chapter (39).
- **Two Śūraṅgamas:**
  - src:surangama-samadhi-sutra.
  - src:surangama-sutra (T945): seven locations of mind (1); the seeing-nature (2); twenty-five perfect penetrations (6); four clear instructions (6/2); the mantra (7); stages (8, pth:surangama-fifty-five-stages); fifty demonic states as warnings (9-10, obs:fifty-skandha-maras); sudden principle and gradual practice (10).
  - Disputed Indian origin: recorded as scholarly attribution on the source.
- **Samādhirāja:** src:samadhiraja-sutra; 9.17, 9.19, 9.27, 4.
- **Pure Land sūtras:**
  - Larger: vows (48 in T360), vow18, fulfilment, three-grades.
  - Smaller: 1, 10, 11.
  - Contemplation: 1-13, 8, 14, 16; pth:sixteen-contemplations; cpt:nine-grades-of-rebirth.
- **Other sūtras:**
  - Akṣayamati: nitartha, pratisarana.
  - Kāśyapaparivarta: §§56-60, 63, 64, 65, 70-71.
  - src:maharatnakuta. Suvarṇaprabhāsa: 2, 4, 18. src:pratyutpanna-samadhi-sutra: 3.
  - Kāraṇḍavyūha: p291, p297. Bhaiṣajyaguru: vows.
  - Kṣitigarbha: src:ksitigarbha-pranidhana-sutra (vows) and src:dasacakra-ksitigarbha-sutra.
  - Plus about 30 further sūtras (Ugra, Upāyakauśalya, Śālistamba, Anavatapta, Ākāśagarbha, Triskandhaka, Brahmajāla/Fanwang and others).
- **Ratnagotravibhāga:**
  - Five chapters and dual attribution (Maitreya/Asaṅga — Tibetan; Sāramati — Chinese) on the source.
  - Teachings: 1.1, 1.27, 1.28, 1.29, 1.34, 1.35, 1.47, 1.55-57, 1.96-98 (nine similes), 1.154-155, 1.156-157, 2, 3, 4, 5.
  - Commentaries: src:ratnagotravibhaga-vyakhya plus the Tibetan commentaries (Gyaltsab, Gö Lotsawa, Rangjung Dorje, Kongtrul, Mipham).
- **Concepts:** cpt:bodhisattva-path, cpt:bodhicitta-sutra, cpt:six-paramitas, cpt:ten-paramitas, cpt:ten-bhumis, cpt:emptiness-prajnaparamita, cpt:skillful-means, cpt:one-vehicle, cpt:buddha-nature, cpt:three-bodies-sutra, cpt:pure-lands, cpt:dharani-types, cpt:permanence-of-dharmakaya.
- **Practices:** prc:sutra-recitation, prc:sutra-copying, prc:dharani-recitation, prc:buddhanusmrti-mahayana, prc:pratyutpanna-samadhi, prc:sixteen-contemplations, prc:bodhisattva-vow, prc:bodhicittotpada and 30 others.
- **Disputes (new ids):**
  - dsp:can-all-beings-attain-buddhahood (queued; Daosheng and Saichō–Tokuitsu debates).
  - dsp:one-vehicle-or-three (queued; three carts vs four).
  - dsp:which-turning-is-definitive (queued under P5, the Buddhists' own hermeneutic; related to dsp:rangtong-shentong).
  - dsp:buddha-nature-self-or-emptiness (partially reconciled P1/P6, with the Jonang, Gelug and Theravāda objections recorded).
  - dsp:mahayana-buddhavacana (queued).
  - dsp:permanence-of-the-tathagata and dsp:is-meat-eating-permitted (partially reconciled).
  - dsp:womens-bodies-and-buddhahood (partially reconciled P1).
- **Views of the ultimate:** ult:mahayana, ult:tathagatagarbha.
- **D-checklist:** covered per lineage through terms, concepts and teachings. The Mahāyāna sūtras have no energy anatomy; the body is treated only as impermanent (Vimalakīrti 2.7) and as the three bodies.

### Corrections to the brief
- The Vimalakīrti "ch. 9" silence is Kumārajīva's numbering; it is Sanskrit ch. 8 (vkn 8.33).
- The Lotus chapters the brief cites (12, 16, 25) are Kumārajīva's; in the Sanskrit they are 11, 15 and 24.
- The "sign of faith" in the Buddha's lifespan (seeing him on the Vulture Peak) is in K17 (Skt 16), not K16.
- "Forty-eight vows" is T360's count; the Sanskrit and other versions give different numbers.
- The Diamond's final verse has nine similes in Sanskrit and six in Kumārajīva.
- The RGV's "three reasons" are 1.27 (with the alternative formulation 1.28) in Johnston's numbering.

## 2. Least-sure items (check these first)
- **T945 Śūraṅgama (not local):** all fascicle refs are from memory, and so are the quoted lines 反聞聞自性，性成無上道, 不作聖心…, 理則頓悟…. The whole of pth:surangama-fifty-five-stages is from memory.
- **Saṃdhinirmocana:** chapter contents, the ādāna verse and the ch. 7 "one vehicle with intention" claim are from memory.
- **Tathāgatagarbha Sūtra tea 1–3:** T666 is not local.
- **Aṅgulimālīya, Mahābherī, Mahāmegha:** summaries and the hail simile, all low confidence.
- **Avataṃsaka:** 80-fascicle chapter placements (ch. 16 "at first arising", ch. 20 painter verse, ch. 37).
- **Low-confidence sources and one-line summaries:** src:dharanisvararaja-sutra (Toh number not found), src:ghanavyuha-sutra, src:gaganaganjapariprccha, src:mahamegha-sutra, src:bodhisattvapratimoksa-sutra.
- **Dispute details:**
  - The Faxiang "principle vs practice buddha-nature" distinction.
  - The Mahāvaṃsa suppression of the Vetullavāda (kings named from memory).
  - Yijing's criticism of body-burning, used as a warning in prc:body-burning-offering.
  - The three-cart vs four-cart attribution.
- **Chapter-level teachings marked "checked" that were only partly checked:**
  - Daśabhūmika: the ground names and structure were read locally, but details such as the five fears and ten vows are from memory.
  - RGV ch. 2–5: the colophons were read, the contents are from memory.
- **Teachers:** tch:paramiti (tradition only); the dates for tch:prajna-translator; the Yeshe De and Jinamitra dates.
- **Ids that need a merge decision:**
  - tch:maitreya-bodhisattva is the same figure as U36's tch:metteyya. It is kept separate because tch:maitreya is the Upaniṣadic sage.
  - trm:vyakarana-prediction was created because trm:vyakarana already means grammar.
  - trm:jianxing (Śūraṅgama sense) is distinct from Chan's kenshō.

## 3. Gaps (belong here but not created responsibly)
- No teachings for the Śatasāhasrikā, 18,000, Ratnaguṇasaṃcayagāthā, Karuṇāpuṇḍarīka details, Ratnamegha, Dharmasaṃgīti, Sāgaramati, Gaganagañja, Tathāgataguhya, Pitāputrasamāgama, Bodhisattvapiṭaka, Rāṣṭrapāla or the Mahāmegha prophecy (source entries only).
- The Chinese title of the Dharmasaṃgīti and the Tōhoku number of the Dhāraṇīśvararāja were not identified.
- The Dazhidu lun and Abhisamayālaṃkāra were left to U40/U41. Tiantai, Huayan and Pure Land school doctrine were left to U54/U43.
- The exact lists were not asserted for:
  - the forty-eight vows (only 18, 19 and 20 are named);
  - the Brahmajāla's forty-eight minor precepts;
  - the Ākāśagarbha root downfalls;
  - the Avataṃsaka's 140 daily vows.
- The Śūraṅgama's fifty states were not enumerated individually.
- No Tibetan-script or Chinese originals were quoted for texts not held locally.

## 4. Out of reach
- Chinese Taishō vols. 9–10, 13, 16 and 19 (Lotus T262, Avataṃsaka T278/279/293, Vimalakīrti T475, Laṅkāvatāra T670–672, Saṃdhinirmocana T676, Tathāgatagarbha T666, Śūraṅgama T945, Pratyutpanna T418) are not in the local CBETA subset.
- The Tibetan Derge texts are present, but only their titles were used in this phase.
- The Saṃdhinirmocana, Tathāgatagarbha Sūtra, Anūnatvāpūrṇatva and Akṣayamati Sanskrit are lost apart from citations.
- Restricted material: prc:body-burning-offering (Lotus 23) is recorded as a summary with the texts' own warnings only, and the Sadāprarudita and tigress narratives as story only. The intensive 90-day form of the Pratyutpanna samādhi is summarized without method.
