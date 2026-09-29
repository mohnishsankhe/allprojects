# P0 Audit — Ontology Insight Generator

Date: 2026-09-29 (IST evening). Auditor: onto-analyst. Data audited: merged `data/` as of the 18:14 IST merge (no merge since).
Every count here comes from scripts, not estimates: `shards/audit/_gen/count.py`, `count2.py`, `count3.py`, `cover.py` (output in `counts.json`).
Levels: `skel` = skeleton (recalled from model knowledge, unchecked) · `src` = sourced · `tv` = text-verified · `unv` = `[unverified]` flag.
Product rule: user-facing output may use **only** `src` and `tv` entries.

## 1. Headline

1. **The ascetic lens (Buddhist and Jain) has no usable entries.** Every Buddhist and Jain teaching (3,601), obstacle (202), practice (471),
   phenomenology item (236), path (85) and concept (1,114) is skeleton. The Phase C sweeps only reached U01–U07, and every upgrade to `sourced` came from them
   (plus the Gītā extraction). So the product's second lens cannot yet cite anything.
2. **Person-layer concepts are almost all skeleton.** Among the core ids, only the five sheaths, three guṇas, the four states and turīya, deep sleep,
   the five prāṇas, the ten vāyus and the nāḍīs are sourced. Kleśas, hindrances, fetters, Jain passions and vṛttis have no sourced id.
3. **What is usable now is Vedic and Upaniṣadic/Epic.** That covers the Gītā (599 tv + 197 src; ch. 1–15 fully tv), the Kaṭha, Taittirīya and Māṇḍūkya (all src),
   66 obstacles, 96 phenomenology items, 207 non-restricted practices, 37 paths and 49 disputes.
4. **The Yoga Sūtra and Vyāsa are 100% skeleton** (195 + 120), even though the full text with the bhāṣya is prepared locally.
5. **Spot-checks.** Of 20 checks, 17 are faithful, 3 partly faithful, 0 unfaithful, plus one sub-claim that could not be checked. The skeleton content for the famous
   verses is accurate. The risks are unsourced glosses, dropped qualifiers and missing restricted flags, not invention.

## 2. Counts — all entity types

| entity | total | skeleton | sourced | text-verified | [unverified] | restricted |
|---|---|---|---|---|---|---|
| teachings | 11,300 | 8,299 | 2,402 | 599 | 1 | 158 |
| sources | 3,695 | 3,119 | 576 | 0 | 0 | 40 |
| lineages | 323 | 292 | 31 | 0 | 0 | 1 |
| teachers | 2,772 | 2,387 | 385 | 0 | 0 | 0 |
| terms | 4,781 | 4,771 | 10 | 0 | 0 | 10 |
| concepts | 2,944 | 2,617 | 327 | 0 | 0 | 27 |
| obstacles | 611 | 545 | 66 | 0 | 0 | 3 |
| practices | 1,525 | 1,302 | 223 | 0 | 0 | 130 |
| paths | 205 | 168 | 37 | 0 | 0 | 9 |
| phenomenology | 740 | 644 | 96 | 0 | 0 | 10 |
| disputes | 455 | 406 | 49 | 0 | 0 | 1 |
| borrowings | 470 | 423 | 47 | 0 | 0 | 1 |
| ultimate views | 208 | 203 | 5 | 0 | 0 | 1 |

Only teachings reach text-verified: 599, all of them Gītā. No entity of any other type is text-verified.

### 2a. By family (lineage family of the entry; "both" = lineages from both families)

| layer | Vedic src | Vedic skel | ascetic src | ascetic skel | both/shared src | both/shared skel |
|---|---|---|---|---|---|---|
| teachings (by source family) | 2,402 + 599 tv | 4,332 | **0** | 3,601 | 0 | 366 |
| obstacles | 63 | 296 | **0** | 202 | 3 | 47 |
| practices | 213 | 751 | **0** | 471 | 10 | 80 |
| phenomenology | 96 | 383 | **0** | 236 | 0 | 25 |
| paths | 37 | 79 | **0** | 85 | 0 | 4 |
| concepts | 318 | 1,280 | **0** | 1,114 | 9 | 223 |
| disputes | 43 | 184 | **0** | 140 | 6 | 82 |

## 3. Counts — what the product needs

**Obstacles by category (skel / src):** obstacle 163/12 · other 65/8 · meditation-fault 62/5 · passion 50/13 · affliction 46/9 · bond 41/11 · impurity 38/3 · karma-type 28/2 · fetter 19/0 · dosa-imbalance 13/2 · hindrance 9/0 · poison 7/0 · guna 4/1

**Phenomenology by kind (skel / src):** state 182/37 · power 112/10 · vision 101/13 · sign 72/11 · bodily 67/5 · difficulty 42/6 · light 41/7 · sound 27/7

All 96 sourced items come from U02–U07 (Upaniṣads, minor Upaniṣads, other Gītās, Purāṇas).

**Practices by category (skel / src / restricted):** ritual 206/54/29 · meditation 202/30/4 · devotion-service 154/20/3 · ethics 119/20/9 · mantra-sound 97/28/1 · inquiry 80/14/0 · sense-withdrawal-concentration 65/12/0 · breath 56/9/12 · posture 52/1/0 · body-daily-rhythm 50/5/6 · visualization-deity 47/8/3 · energy 43/3/32 · sleep-dream-death 43/10/21 · mind-training 40/3/0 · cleansing 31/0/5 · lock-seal 17/6/5

Of the 223 sourced practices, 16 are restricted, which leaves **207 usable**.

**Citation support.** An entity can be sourced while the teachings it cites are skeleton, so the engine must also check the level of each cited teaching.

| layer | sourced, every cited teaching src/tv | sourced, some cited | skeleton, every cited teaching src/tv (promotion candidates) |
|---|---|---|---|
| obstacles | 50 | 13 | 51 |
| practices | 159 | 58 | 75 |
| phenomenology | 95 | 0 | 64 |
| paths | 37 | 0 | 6 |
| disputes | 46 | 2 | 21 |

**Disputes by reconciliation status (skel / src):** queued 244/15 · partially reconciled 132/27 · reconciled 22/7 · no status 8/0

Six of the sourced disputes have sides from both families: `dsp:daiva-or-paurusa`, `dsp:image-worship-and-inner-worship` and `dsp:which-purusartha-is-foremost` are partial; `dsp:buddha-avatara-purpose`, `dsp:varna-origin-purusa-sukta` and `dsp:vedic-ritual-killing-and-ahimsa` are queued.
`dsp:is-there-a-self` and `dsp:nibbana-atta-or-anatta`, which the self/no-self reconciliation depends on, are skeleton.

**Ultimate node.** `ult:the-one` is present. Its anchor, `tea:rgveda:1.164.46`, is **sourced**. Of the 208 lineage views, 5 are sourced.

**Person-layer ids (the ids the person map needs):**

| layer | sourced | skeleton (all) |
|---|---|---|
| sheaths | cpt:five-sheaths | trm:pancakosa, trm:kosa, trm:annamaya-kosa, trm:pranamaya-kosa, trm:manomaya-kosa, trm:vijnanamaya-kosa, trm:anandamaya-kosa, prc:panca-kosa-viveka |
| guṇas | cpt:three-gunas | trm:guna, trm:sattva, trm:rajas, trm:tamas, cpt:gunatita, obs:guna-bondage, phn:guna-signs, phn:marks-of-gunatita, cpt:guna-typology-of-gita-18 |
| states of consciousness | cpt:four-states-and-turya, cpt:turiya, cpt:deep-sleep | cpt:states-of-consciousness, cpt:three-states-and-turiya, trm:jagrat, trm:svapna, trm:susupti, trm:turiya, prc:avastha-traya-viveka |
| kleśas | — | cpt:five-klesas, obs:five-klesas, trm:klesa, trm:kilesa, obs:ten-kilesas, obs:six-root-afflictions-yogacara, obs:twenty-secondary-afflictions, obs:sixteen-upakkilesa |
| hindrances | — | cpt:five-hindrances, obs:five-hindrances, trm:nivarana, obs:six-hindrances-abhidhamma |
| fetters | — | cpt:ten-fetters, obs:ten-fetters, obs:five-lower-fetters, obs:five-higher-fetters, trm:samyojana, obs:nine-samyojanas, obs:ten-fetters-abhidhamma |
| Jain passions | — | obs:four-kasayas, cpt:four-kasayas-sixteen, trm:kasaya, obs:nine-nokasayas, trm:nokasaya |
| vṛttis | — | cpt:five-vrttis, trm:vrtti, trm:vrttisanksaya |
| vital currents | cpt:five-pranas, cpt:ten-vayus, cpt:nadis, trm:samana, trm:udana | cpt:five-vayus, cpt:prana-vayus-yoga, trm:prana, trm:apana, trm:vyana, trm:vayu, trm:nadi |

## 4. Core texts (P1) — teachings and prepared segments

"Verses covered" counts prepared segments that fall inside at least one teaching's ref (ranges expanded).

| text | teachings | skel | src | tv | with original | prepared segments (sources_raw/prepared/) | verses covered | covered by src/tv |
|---|---|---|---|---|---|---|---|---|
| Bhagavad Gītā | 796 | 0 | 197 | 599 | 608 | bhagavad-gita 701 | 701 | 701 (tv 571: ch. 1–15 complete; ch. 16–18 src only) |
| Yoga Sūtra | 195 | 195 | 0 | 0 | 195 | yoga-sutra 195 (with Vyāsa bhāṣya in `commentary_iast`) | 195 | 0 |
| Vyāsa bhāṣya | 120 | 120 | 0 | 0 | 0 | (inside yoga-sutra) | 123 | 0 |
| Māṇḍūkya Up. | 9 | 0 | 9 | 0 | 3 | mandukya-upanisad 12 | 12 | 12 |
| Gauḍapāda-kārikā | 33 | 33 | 0 | 0 | 26 | mandukya-karika 214 | 35 | 0 |
| Vijñāna Bhairava | 132 | 132 | 0 | 0 | 4 | vijnana-bhairava-tantra 162 | 161 | 0 |
| Satipaṭṭhāna MN 10 | 16 | 16 | 0 | 0 | 3 | satipatthana-sutta 41 | 34 | 0 |
| Mahāsatipaṭṭhāna DN 22 | 2 | 2 | 0 | 0 | 0 | mahasatipatthana-sutta 22 | 5 | 0 |
| Ānāpānasati MN 118 | 5 | 5 | 0 | 0 | 2 | anapanasati-sutta 43 | 27 | 0 |
| Heart Sūtra | 8 | 8 | 0 | 0 | 7 | prajnaparamita-hrdaya 9 (T251) + -sanskrit-short 10 | 6/10 | 0 |
| Haṭhayogapradīpikā | 229 | 229 | 0 | 0 | 111 | hatha-yoga-pradipika 387 | 375 | 0 |
| Dhammapada | 22 | 22 | 0 | 0 | 20 | dhammapada 423 | 27 | 0 |
| Visuddhimagga | 83 | 83 | 0 | 0 | 61 | **none** raw GRETIL `2_pali/4_comm/visuddhimagga.md` only | chapter-level refs only | 0 |
| Tattvārtha Sūtra | 257 | 257 | 0 | 0 | 255 | tattvartha-sutra 357 (Digambara recension) | 348 | 0 |
| Taittirīya Up. | 24 | 0 | 24 | 0 | 6 | taittiriya-upanisad 51 | 47 | 47 |
| Kaṭha Up. | 52 | 0 | 52 | 0 | 10 | katha-upanisad 120 | 104 | 104 |

Other prepared texts that could serve later: aṣṭāvakra, avadhūta, Śiva-sūtra, spanda, pratyabhijñāhṛdaya, sāṃkhya-kārikā, MMK, vajracchedikā, Platform Sūtra, Tilopa, Saraha, SN 56.11, all the principal Upaniṣads and the Maitrī.

## 5. Usable now (src/tv only, restricted excluded)

- **Teachings.** Gītā 796 (ch. 1–15 tv; 16–18 src), Kaṭha 52, Taittirīya 24, Māṇḍūkya 9, and the other sourced Vedic teachings (2,402 src in all). Ascetic: none.
- **Layers of the person (Vedic lens).** Five sheaths: cpt:five-sheaths plus TU 2.1–2.5 and 3.2–3.6. Guṇas: cpt:three-gunas plus Gītā ch. 14, 17 and 18 (ch. 14 tv; ch. 17–18 src). States: cpt:four-states-and-turya, cpt:turiya, cpt:deep-sleep, phn:mandukya-the-fourth, MU 1–12. Vital currents: cpt:five-pranas, cpt:ten-vayus, cpt:nadis. Chariot image: cpt:chariot-image, KU 1.3.3–9.
- **Obstacles.** 66 are sourced (50 with every cited teaching src/tv), all Vedic. Examples: obs:avidya, obs:ahankara, obs:kama, obs:trsna, obs:bhaya, obs:soka, obs:samsaya, obs:pramada, obs:manas-cancalya, obs:sanga-attachment, obs:dehatmabuddhi, obs:six-enemies, obs:siddhis-as-obstacles, obs:yogatattva-vighnas.
- **States and phenomenology.** 96 are sourced, 37 of them of kind "state". Examples: phn:mandukya-the-fourth, phn:katha-highest-state, phn:jivanmukta-marks, phn:svetasvatara-first-signs-of-yoga.
- **Practices.** 207 are usable, all Vedic or shared. By category: meditation 30, inquiry 14, sense-withdrawal 12, mantra 28, devotion 20, ethics 17, breath 7. Examples: prc:atma-vicara, prc:neti-neti, prc:pratyahara, prc:dharana, prc:dhyana, prc:nididhyasana, prc:saksi-bhava-astavakra. Caution: sourced prc:pranayama, prc:nadi-sodhana and prc:jnana-pranayama may carry retention details (see §8).
- **Paths.** 37 sourced, all Vedic: eight-limb variants of the Yoga Upaniṣads, pth:katha-inward-withdrawal, pth:varaha-seven-bhumikas, pth:uddhava-gita-three-yogas.
- **Disputes and reconciliations.** 49 sourced; 34 of them are reconciled or partially reconciled. Almost none bears on the person map across the two lenses.
- **Ultimate node.** Usable as framing, with its anchor verse (sourced).

## 6. What is missing

**By layer:**
- **Ascetic lens, every layer.** Hindrances, fetters, the Buddhist kleśas and upakkilesas, the Jain kaṣāyas and nokaṣāyas: 0 sourced. The Buddhist meditation subjects (Vism III) and ānāpānasati: 0 sourced. Buddhist and Jain paths: stages of purification, gunasthānas.
- **Vedic kleśas and vṛttis.** YS/YBh are all skeleton, so obs:five-klesas, cpt:five-vrttis and the nine antarāyas cannot yet be shown.
- **Terms.** 10 of 4,781 are sourced. Glossary lookups (trm:klesa, trm:prana, trm:guna, …) are skeleton.
- **Cross-lens reconciliations.** The self/no-self, mind-luminosity and kaṣāya ↔ kleśa ↔ kleśa-as-affliction equivalences are all skeleton.
- **Phenomenology "difficulty".** 6 sourced, all Vedic. These are the texts' own descriptions of meditative trouble, which the product needs.

**By core text:**
- Yoga Sūtra and Vyāsa, Gauḍapāda, VBT, HYP, MN 10, DN 22, MN 118, Heart, Dhammapada, Visuddhimagga and Tattvārtha: all at 0% src/tv.
- The Dhammapada covers only 27 of 423 verses, the Gauḍapāda-kārikā 35 of 214, DN 22 5 of 22, and MN 118 27 of 43.
- The Visuddhimagga has no prepared segments. Its 83 teachings cite chapter numbers only (for example `3/10`), not paragraphs.
- The Tattvārtha is prepared only in the Digambara recension. Śvetāmbara numbering differs (for example the passions sūtra), and there is no Śvetāmbara text.
- Gītā ch. 16–18: the merger (M) and fidelity pass (F) were stopped, so 130 verses are sourced but not text-verified. That also leaves 41 dangling refs (tea:bhagavad-gita:16.1, 18.47, …) in core-text teachings.

## 7. Spot-checks (20)

Local source first; passages were fetched with code. P = `sources_raw/prepared/<text>/segments.jsonl`.

| # | id (level) | claim checked | verdict | evidence (file · ref · quoted words) |
|---|---|---|---|---|
| 1 | obs:five-klesas (skel) | five kleśas; avidyā is their field; root of karmāśaya; thinned by kriyā-yoga, removed by dhyāna / pratiprasava | faithful | P yoga-sutra 2.3 "avidyāsmitārāgadveṣābhiniveśāḥ kleśāḥ"; 2.4 "avidyā kṣetram uttareṣām"; 2.12 "kleśamūlaḥ karmāśayo"; 2.2 "kleśatanūkaraṇārthaś ca"; 2.11 "dhyānaheyās tadvṛttayaḥ"; 2.10 "te pratiprasavaheyāḥ" |
| 2 | cpt:five-vrttis (skel) | five vṛttis, afflicted or not; vṛtti–saṃskāra wheel; all to be stilled | faithful | P yoga-sutra 1.5 "vṛttayaḥ pañcatayyaḥ kliṣṭākliṣṭāḥ", YBh "vṛttisaṃskāracakram aniśam āvartate"; 1.6 "pramāṇaviparyayavikalpanidrāsmṛtayaḥ"; YBh 1.11 "sukhaduḥkhamohātmikāḥ … niroddhavyāḥ" |
| 3 | obs:five-hindrances (skel) | the five; MN 10 contemplation; DN 2 similes (debt…desert); SN 46.55 water similes | faithful | P satipatthana-sutta mn10:36 "pañcasu nīvaraṇesu … kāmacchandaṁ"; bilara dn2 74.1 "a debt, a disease, a prison, slavery, and a desert crossing"; sn46.55:4.1–12.1 "bowl of water … mixed with dye / heated / moss / stirred by the wind / cloudy" |
| 4 | obs:four-kasayas (skel) | four passions in four grades; "glue" for karma; "conquest is liberation (YŚ 4.5)" | partly | P tattvartha-sutra 8.9 "anantānubaṃdhya-pratyākhyāna-pratyākhyāna-saṃjvalana-vikalpāś caikaśaḥ krodha-māna-māyā-lobhāḥ" ✓. The glue idea rests on TS 8.2 "sakaṣāyatvāj jīvaḥ karmaṇo yogyān pudgalān ādatte", which the entry does not cite. Hemacandra's Yogaśāstra is not local, so YŚ 4.5 **could not be checked**. TS refs are Digambara numbering. |
| 5 | cpt:five-sheaths (src) | TU's five person-shaped selves, brahman as tail; TU 3 the same five; "kośa" is later usage | faithful | P taittiriya-upanisad 2.1.1 "annarasamayaḥ"; 2.2.1 "prāṇamayaḥ … puruṣavidhaḥ … pṛthivī pucchaṃ pratiṣṭhā"; 2.5.1 "brahma pucchaṃ pratiṣṭhā"; 3.2.1–3.6.1 "annaṃ / prāṇo / mano / vijñānaṃ / ānando brahmeti vyajānāt"; no "kośa" in TU. Defects: the Tamil-siddha definition has no rests_on, and the members list is duplicated. |
| 6 | phn:mandukya-the-fourth (src) | description of the fourth | faithful (abridged) | P mandukya-upanisad 7 "nāntaḥprajñaṃ na bahiḥprajñaṃ … prapañcopaśamaṃ śāntaṃ śivam advaitaṃ caturthaṃ manyante". It omits "sa ātmā sa vijñeyaḥ" and four negations. |
| 7 | obs:manas-cancalya (src) | the mind as the monkey of saṃsāra's forest; brought back like a horse in training | faithful | GRETIL `dcs/corpus/GRETIL/sa_mokSopAya.txt` 2,11.56 "mano hi capalaṃ rāma saṃsāravanamarkaṭam"; `raw_etexts/purANam/mAdhva-app/bhagavata-purANam.md` 11.20.19 "भ्राम्यदश्वनवस्थितम् … अतन्द्रितोऽनुरोधेन", 11.20.21 "दम्यस्येवार्वतो मुहुः". The `antidotes` field is empty although the text gives abhyāsa. |
| 8 | prc:anapanasati (skel) | secluded, erect, 16 steps → satipaṭṭhāna → awakening factors → release; "natural breath is known, not controlled" | partly | P anapanasati-sutta mn118:15 "fulfills the four kinds of mindfulness meditation … seven awakening factors … knowledge and freedom" ✓; mn118:17 "sits down cross-legged, sets their body straight" ✓. "Not controlled" is **not in MN 118**: mn118:18 trains "I'll breathe in stilling the physical process". It is an unsourced gloss. |
| 9 | tea:yoga-sutra:1.33 (skel) | friendliness, compassion, gladness and equanimity toward the happy, suffering, virtuous and non-virtuous → clarity of mind | faithful | P yoga-sutra 1.33 "maitrīkaruṇāmuditopekṣāṇāṃ sukhaduḥkhapuṇyāpuṇyaviṣayāṇāṃ bhāvanātaś cittaprasādanam" |
| 10 | tea:yoga-bhasya:1.33 (skel, no original) | white dharma arises → mind clear → one-pointed, steady | faithful | P yoga-sutra 1.33 commentary "śuklo dharma upajāyate / tataś ca cittaṃ prasīdati / prasannam ekāgraṃ sthitipadaṃ labhate" |
| 11 | tea:mandukya-karika:3.44 (skel) | rouse the mind in laya, calm it when distracted, recognize kaṣāya, leave equipoise alone | faithful | P mandukya-karika 3.44 "laye saṃbodhayec cittaṃ vikṣiptaṃ śamayet punaḥ / sakaṣāyaṃ vijānīyāt samaprāptaṃ na cālayet". "Latent impressions" is a commentarial gloss. Linked to the Advaita obs:kasaya, a homonym of the Jain passions (§9). |
| 12 | tea:vijnana-bhairava-tantra:24 (skel, moderate) | prāṇa above, jīva below; fullness by filling the two places of arising | faithful | P vijnana-bhairava-tantra 24 "ūrdhve prāṇo hy adho jīvo visargātmā paroccaret / utpattidvitayasthāne bharaṇād bharitā sthitiḥ". "(the in-breath)" is a bracketed commentarial gloss. |
| 13 | tea:satipatthana-sutta:36-37 (skel) | knowing whether each hindrance is present, how it arises, is abandoned and does not recur | faithful | P satipatthana-sutta mn10:36 "santaṁ vā ajjhattaṁ kāmacchandaṁ 'atthi me ajjhattaṁ kāmacchando'ti pajānāti …"; mn10:37 closing refrain |
| 14 | tea:hatha-yoga-pradipika:2.2 (skel) | breath moves → mind moves; stilled → still; therefore restrain the breath | faithful | P hatha-yoga-pradipika 2.2 "cale vāte calaṃ cittaṃ niścale niścalaṃ bhavet … tato vāyuṃ nirodhayet". The verse instructs breath restraint (see §8). |
| 15 | tea:visuddhimagga:3/10 (skel) | temperaments → meditation subjects | partly | GRETIL `2_pali/4_comm/visuddhimagga.md` l.3263–68 "rāgacaritassa … dasa asubhā kāyagatāsati … ekādasa kammaṭṭhānāni anukūlāni, dosacaritassa cattāro brahmavihārā cattāri vaṇṇakasiṇāni…" ✓. Omitted: the text's own qualifier, l.3269–70 "sabbañcetaṃ ujuvipaccanīkavasena ca atisappāyavasena ca vuttaṃ" (said by direct opposition and extreme suitability; every wholesome development suppresses greed and the rest), and the limited/measureless kasiṇa rule. The locator is chapter-level only. |
| 16 | tea:katha-upanisad:1.3.3-4 (src) | self = rider, body = chariot, buddhi = charioteer, mind = reins, senses = horses | faithful | P katha-upanisad 1.3.3 "ātmānaṃ rathinaṃ viddhi śarīraṃ rathameva tu | buddhiṃ tu sārathiṃ viddhi manaḥ pragrahameva ca"; 1.3.4 "indriyāṇi hayānāhur … bhoktetyāhur manīṣiṇaḥ" |
| 17 | tea:bhagavad-gita:4.3 (tv) | the same ancient yoga told to Arjuna as devotee and friend; highest secret | faithful | P bhagavad-gita 4.3 "sa evāyaṃ mayā te'dya yogaḥ proktaḥ purātanaḥ | bhakto'si me sakhā ceti rahasyaṃ hyetaduttamam" |
| 18 | tea:bhagavad-gita:8.18 (tv) | manifest things arise from the unmanifest at day and dissolve at night | faithful | P bhagavad-gita 8.18 "avyaktādvyaktayaḥ sarvāḥ prabhavantyaharāgame | rātryāgame pralīyante". "(Brahmā's)" is bracketed context from 8.17. |
| 19 | tea:bhagavad-gita:2.49 (tv) | action far inferior to buddhi-yoga; take refuge in buddhi; fruit-seekers wretched | faithful | P bhagavad-gita 2.49 "dūreṇa hyavaraṃ karma buddhiyogād … buddhau śaraṇam anviccha kṛpaṇāḥ phalahetavaḥ" |
| 20 | tea:bhagavad-gita:6.38 (tv) | Arjuna: does one fallen from both perish like a torn cloud? | faithful | P bhagavad-gita 6.38 "kaccin nobhayavibhraṣṭaś chinnābhram iva naśyati | apratiṣṭho" |

**Tally:** 17 faithful, 3 partly faithful (#4, #8, #15), 0 unfaithful. One sub-claim could not be checked (YŚ 4.5 in #4; the text is not local).
**How the 20 were chosen:** entries 17–20 are a random sample (seed 20260929) of the 599 text-verified Gītā teachings; entries 1–16 were chosen because the product will rely on them.
**Two extra checks, both faithful:**
- tea:dhammapada:5: dhammapada 5 "Na hi verena verāni … averena ca sammanti".
- tea:taittiriya-upanisad:2.2-5 (src): the body-part correspondences match 2.2.1–2.5.1 ("prāṇa eva śiraḥ | vyāno dakṣiṇaḥ pakṣaḥ …").

**Caveat.** For teachings, "sourced" means the passage was located and found on-topic (for example the KU 1.3.3-4 check note: "on the same topic"). It is not a word-level fidelity pass. Only tv teachings have had one.

## 8. Fix before user-facing use (prioritised)

1. **Give the ascetic lens usable entries.** Do a targeted text-verification (fidelity pass against the prepared segments), not a full U33–U48 sweep, of: MN 10 (all 41 segments), DN 22, MN 118, SN 46.51/46.55, DN 2 §§67–75; Dhammapada ch. 1, 3, 5, 25 (mind, anger, craving); Heart (Sanskrit short); Visuddhimagga III (subjects, temperaments), IV (hindrances), VIII (breath), IX (brahmavihāras). Prepare Vism segments first; Tattvārtha 6.5, 8.1–2, 8.9, 9.6 (the ten virtues), 9.7 (anuprekṣā); and then upgrade the matching entities: obs:five-hindrances, obs:ten-fetters, obs:five-lower-fetters, obs:ten-kilesas, obs:four-kasayas, obs:nine-nokasayas, cpt:five-hindrances, cpt:ten-fetters, prc:anapanasati, prc:metta-bhavana, the brahmavihāras, prc:anupreksa, prc:samayika.
2. **Vedic person-layer backbone.** Text-verify YS 1.1–1.51 and 2.1–2.55 with the Vyāsa bhāṣya (kleśas, vṛttis, antarāyas 1.30–31, pratipakṣa-bhāvanā 2.33–34, brahmavihāras 1.33). Then upgrade obs:five-klesas, cpt:five-klesas, cpt:five-vrttis, obs:nine-antarayas and the guṇa and prāṇa terms.
3. **Person-layer terms and concepts** (the §3 table: about 60 ids). Verify the definitions and rests_on of each. 4,771 of 4,781 terms are skeleton.
4. **Gītā ch. 16–18.** Run the stopped merger (M) and fidelity pass (F), then the Gītā-wide consistency pass (citta/cetas rendering, errata). This resolves the 41 dangling Gītā refs.
5. **Correct the partly faithful entries.** prc:anapanasati: drop "not controlled", or cite a commentary that says it. tea:visuddhimagga:3/10: add the text's qualifier and a paragraph locator. obs:four-kasayas: cite TS 8.2, mark YŚ 4.5 unchecked, and give the Śvetāmbara numbering. obs:manas-cancalya: fill `antidotes` (abhyāsa, BhP 11.20.18).
6. **Restricted flags.** Flag or review these (keyword scan with code; each item to be confirmed by a person): prc:bhastrika and prc:plavini: HYP kumbhakas; prc:murccha is flagged, these are not. prc:vajroli-gheranda: name collision with vajrolī. prc:white-and-red-khecari. prc:smasana-vasa: "until the body falls". prc:upavasa and prc:prosadhopavasa: fasting. 34 HYP teachings, 5 Gītā/KU/TU teachings (utkrānti) and 5 VBT teachings that link to restricted practices but carry no teaching-level flag. Conversely, prc:tapas is flagged restricted as a whole, which blocks benign citations (YS 2.1, TU 3.2): split it into general austerity and restricted extreme austerity.
7. **Homonyms and dedupe in the product layers.** obs:kasaya (Advaita "latent attachment") vs obs:four-kasayas (Jain). trm:kasaya mixes four senses in one entry (Āyurveda taste, Advaita, Jain, sannyāsa). Near-duplicates: obs: ari-sadvarga / arisadvarga, dehatma-buddhi / dehatmabuddhi, sad-ripu / sadripu, four-viparyasa(s); prc: bhuta-suddhi / bhutasuddhi, bhasma-snana / bhasmasnana, kesa-loca / kesaloca; cpt: 8 pairs, including samskara / samskaras. Separately, 255 terms carry definitions from both families. The engine must pick a definition by lineage and never quote the whole term.
8. **Dangling references in the product layers.** Obstacles: 5 (obs:klesa, obs:klesas, obs:asavas, obs:three-bonds, obs:tirodhana-sakti). Concepts: 38 refs to 28 ids (cpt:emptiness, cpt:four-immeasurables, cpt:five-spiritual-faculties, cpt:bardo, …). Practices: 60 refs to 18 ids, mostly missing lineages. Paths: 6. Disputes: 15. Repo-wide the stats report lists 190 distinct missing ids.

## 9. Risks

- **One-lens output.** If only src/tv entries are allowed, today the "reconcile two lenses" step can show only the Vedic lens. The engine must say this openly ("the ascetic reading is not yet verified"), not fill the gap with skeleton entries.
- **Restricted practices.** 130 practices and 158 teachings are flagged. Sixteen restricted practices are sourced and so pass the level filter:
  - breath and energy: prc:kevala-kumbhaka, prc:sahita-kumbhaka, prc:khecari-mudra, prc:vajroli-amaroli, prc:sakticalana, prc:mahabandha-mahavedha, prc:ksurika-dharana, prc:utkranti-yoga;
  - fasting and giving up the body: prc:prayopavesa, prc:mahaprasthana, prc:candrayana, prc:krcchra-penances;
  - others: prc:abhicara-rites, prc:garbhadhana, prc:tapas, prc:devi-gita-kundalini-dhyana.

  The filter must be `restricted == false` on the entity **and** on every cited teaching and linked practice. HYP 2.2 (faithful) itself says "restrain the breath".
- **Skeleton-only areas.** All Buddhist and Jain material. YS/YBh, HYP, VBT, Gauḍapāda, Dhammapada, Visuddhimagga. 4,771 terms. Every hindrance, fetter and poison category. 406 of 455 disputes, including dsp:is-there-a-self.
- **Homonym ids.** kaṣāya (Jain passion / Advaita latent attachment / astringent taste) and kleśa (Yoga five ≠ Buddhist lists; obs:five-klesas notes this as "partial"). Also trm:vyakarana (grammar ≠ prediction), tch:maitreya ≠ tch:maitreya-bodhisattva, cpt:satkarma (tantric) ≠ cpt:satkarma-doctrine (haṭha). Keyword matching of a user's words to ids will conflate them unless the lineage is carried along.
- **Dangling references.** An engine that follows rests_on or members links will hit missing ids. For example, obs:five-klesas has an equivalence to the missing `obs:klesa`, and obs:five-hindrances mixes ids with plain strings in `members`. Every link must be resolved and dropped if missing.
- **"Sourced" is weaker than it looks.** Sourced teachings passed a locate-and-topic check, not a wording check. Paraphrases may carry glosses (see #8 and #15). Prefer quoting `original` from the prepared segments with the paraphrase marked as a paraphrase. 3,141 merge conflicts are logged (`data/reports/conflicts.jsonl`) and were not reviewed here.
- **Recension and numbering.** TS is Digambara-only. Gītā ch. 13 uses the edition's numbering (vulgate shift, DECISIONS 18:02). Śiva-sūtra refs mix recensions. The engine must cite with the edition named.
- **Not checked in this audit:** merge conflicts, interpretation-log consistency, sources not held locally (e.g. Hemacandra's Yogaśāstra), and the ATLAS pages.
