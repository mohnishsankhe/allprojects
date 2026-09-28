# Morning report — Tradition Ontology

_Written 2026-09-28 07:05 IST. Every number below is generated from `data/` by `scripts/merge.py` and `scripts/report.py`._

## In one paragraph

The run began at 03:53 IST, not in the evening, which left about three hours before this report. Phase A (the frame) is complete and pushed.
Phase B (the skeleton sweep) started 20 units in parallel at about 04:25 IST, the maximum this environment allows. At about 05:00 IST all 20
stopped at once when the account hit its usage limit ("session limit"). That limit reset at 06:20 IST, and the nine
furthest-along units were resumed at 07:02 with their context intact. So this report shows a partial skeleton for 19 of 59 units. Phase C (the
hallucination sweep) and Phase D (the text-verified core) have not produced entries yet: **nothing below is `sourced` or
`text-verified`; everything is `skeleton`**. The texts for Phase D are downloaded and cut into verse-level segments with
standard numbering, ready for extraction.

## 1. What exists

| entity | total | skeleton | sourced | text-verified | [unverified] | recent |
|---|---|---|---|---|---|---|
| sources | 798 | 798 | 0 | 0 | 0 | 10 |
| lineages | 63 | 63 | 0 | 0 | 0 | 1 |
| teachers | 425 | 425 | 0 | 0 | 0 | 16 |
| teachings | 608 | 608 | 0 | 0 | 0 | 0 |
| terms | 0 | 0 | 0 | 0 | 0 | 0 |
| concepts | 0 | 0 | 0 | 0 | 0 | 0 |
| ultimate | 21 | 21 | 0 | 0 | 0 | 0 |
| obstacles | 0 | 0 | 0 | 0 | 0 | 0 |
| practices | 112 | 112 | 0 | 0 | 0 | 0 |
| paths | 0 | 0 | 0 | 0 | 0 | 0 |
| phenomenology | 0 | 0 | 0 | 0 | 0 | 0 |
| disputes | 0 | 0 | 0 | 0 | 0 | 0 |
| borrowings | 0 | 0 | 0 | 0 | 0 | 0 |

Reconciliation queue: 0 · interpretation-log lines: 3 · merge conflicts logged: 79 · dangling references: 1538

- 798 texts (confidence: high 264, moderate 371, low 163); 425 teachers; 63 lineages; 608 verse-anchored
  skeleton teachings (so far from the Yoga Sūtra and Vyāsa, the Vijñāna Bhairava, the Nyāya Sūtra and the Bhāgavata); 112 practices (the Vijñāna
  Bhairava's 112 contemplations); 21 lineage views of the ultimate. Terms, concepts, obstacles, path maps, debates and borrowings
  are 0 so far: the units that produce them (U09–U20 later parts, U50 debates, U51 path maps, U53 glossary) had not reached
  those parts, or had not started, when the limit hit.
- Several skeleton agents checked verse numbers and wording against the downloaded texts as they wrote (e.g. U10 wrote all
  195 sūtras of the Yoga Sūtra against the GRETIL text; U19 wrote the Vijñāna Bhairava's dhāraṇās against the GRETIL text).
  Those entries are still marked `skeleton` until the fidelity gate passes them.

| unit | entries on disk | state |
|---|---|---|
| U01-vedic-samhitas | 88 | partial — resumed |
| U02-brahmana-vedanga | 34 | partial — resumed |
| U03-principal-upanisads | 0 | partial — resumed |
| U04-minor-upanisads | 0 | partial — resumed |
| U05-gita-epic | 202 | partial — resumed |
| U06-other-gitas | 251 | partial — resumed |
| U07-puranas | 312 | partial — resumed |
| U08-agama-catalogue | 173 | partial — resumed |
| U09-samkhya | 74 | partial — resumed |
| U10-yoga | 351 | partial — resumed |
| U11-nyaya-vaisesika | 208 | partial — resumed |
| U12-mimamsa | 0 | partial — resumed |
| U13-advaita | 0 | partial — resumed |
| U15-dvaita | 196 | partial — resumed |
| U16-bhedabheda | 0 | partial — resumed |
| U17-pasupata-kapalika | 10 | partial — resumed |
| U18-saiva-siddhanta | 0 | partial — resumed |
| U19-kashmir-saivism | 373 | partial — resumed |
| U20-virasaiva | 279 | partial — resumed |

## 2. The Map of the One Truth — the ultimate as each tradition names and describes it (21 views so far)

The claim that these are views of one truth is an interpretation-layer claim made only in `config/ultimate_node.json`;
each row keeps the tradition's own objection. Sāṃkhya and Pātañjala Yoga are recorded as **denying** a single ultimate
(many puruṣas).

| lineage | names | description | negations | self | world | personal? | caveat (the tradition's own objection) | level |
|---|---|---|---|---|---|---|---|---|
| Atimārga | Paśupati, Rudra, Maheśvara, Bhairava / Kapālin (Kāpālika) | the Lord (pati) as the one independent cause, acting by his own will; the Lord's knowledge and action are unsurpassed; liberation brings the soul into | the Lord is not dependent on karma (PABh on PS 2.6) | Souls are eternal paśus distinct from the Lord; liberation is the end of their suffering b | The Lord emits and withdraws the effects (the world and the embodied souls) at will; he is | personal | The Atimārga schools are theistic and keep the liberated soul distinct from the Lord; they would reject a reading that d | skeleton |
| Early Bhāgavata devotion (the Nārāyaṇīya | Nārāyaṇa, Vāsudeva, Hari, Puruṣottama, Bhagavat (the Lord), Kṛṣṇa (his manifestation at Ma | Vāsudeva the Lord is the knower of the field, whose self is without guṇas (MBh 12.326.38); the fourfold form (caturmūrti): Vāsudeva, Saṃkarṣaṇa, Prady | without guṇas (nirguṇātmaka) (12.326.38; 12.332.17); not seen by those without one-pointed | The individual self is Saṃkarṣaṇa, arising from Vāsudeva (12.326.38, 12.326.68); the liber | From Aniruddha comes Brahmā, from Brahmā all moving and unmoving beings, at the beginning  | personal | Described both as the Lord with a form and as without guṇas; the later schools that inherit this devotion (Pāñcarātra, V | skeleton |
| Epic teaching (the Mahābhārata's Sāṃkhya | Brahman — beginningless, supreme, imperishable (anādimat paraṃ brahma; akṣara), Puruṣottam | beginningless supreme Brahman, said to be neither being nor non-being (BhG 13.12); with hands and feet everywhere, eyes, heads and faces everywhere, i | neither being nor non-being — na sat tan nāsad ucyate (BhG 13.12); unmanifest, unthinkable | The self in every body is unborn and eternal (BhG 2.20); the Lord is the knower of the fie | The Lord's lower, eightfold nature (earth, water, fire, air, space, mind, intellect, ego)  | both | The epic milieu is plural: it records Sāṃkhya, Yoga, Vedic, Pāñcarātra and Pāśupata views (MBh 12.337.59), differing cou | skeleton |
| Kālāmukha | Śiva (e.g. as Kedāreśvara at Balligāve) | Inscriptions praise Kālāmukha ācāryas as devotees of Śiva and masters of the Lakula-siddhānta; no Kālāmukha doctrinal treatise survives. |  | Not recorded in the tradition's own words. | Not recorded in the tradition's own words. | personal | Known only from inscriptions and from opponents (Yāmuna, Rāmānuja). | skeleton |
| Kāpālika (Somasiddhānta) | Bhairava / Mahābhairava, Kapālin, Soma (Śiva 'with Umā'; name of the doctrine Somasiddhānt | Worshipped as Mahābhairava (Prabodhacandrodaya act 3, an opponent's portrayal).; Kapālin: the skull-bearing form of Śiva whose penance for Brahmā's he |  | Yāmuna reports that for the Kāpālikas liberation comes from knowing and wearing the six in | Not recorded in the tradition's own words. | personal | Known almost entirely through opponents and satirists; no Kāpālika scripture has been identified with certainty. Somasid | skeleton |
| Kashmir Śaivism (non-dual Śaiva tantra o | Paramaśiva, Anuttara (the unsurpassed), Bhairava, Saṃvit / Citi (consciousness), Maheśvara | light (prakāśa) inseparable from self-reflexive awareness (vimarśa); perfect I-ness (pūrṇāhantā); absolutely free (svatantra); cause of the world's es | not the ninefold, not the mass of sounds, not three-headed, not composed of nāda and bindu | Identical: 'consciousness is the self' (Śiva Sūtra 1.1); the individual is Śiva contracted | The world is Śiva's own free self-manifestation unfolded on his own screen (PH 2); real as | both | The tradition insists that the ultimate is active (vimarśa, svātantrya, the five acts) and that the world is real as its | skeleton |
| Kerala tantra (temple-tantra tradition o | Parameśvara (sakala), the seven installed deities as forms of the supreme | From the supreme Lord endowed with existence, consciousness and bliss, and with parts (sakala), arose Śakti; from her Nāda; from Nāda, Bindu (Śāradāti |  |  |  | both | Kerala tantra is a ritual tradition serving several deities; it has no single systematic theology. The Prapañcasāra (att | skeleton |
| Krama (the 'Sequence'; Mahānaya, Mahārth | Kālī, Kālasaṅkarṣiṇī, Anākhya (the nameless), Svasaṃvid (one's own consciousness) | one's own consciousness, whose free and independent variety is the supreme Goddess (TĀ 4.172); the power that projects, knows, counts, moves and sound | the nameless (anākhya) | The goddess is one's own consciousness (svasaṃvid). | The Kālīs emit, hold and devour the world as phases of cognition across object, means and  | both | Known chiefly through Abhinavagupta, Jayaratha and Maheśvarānanda; the Krama stresses the sequence of the goddess's phas | skeleton |
| Lākula | Rudra | The Svacchanda Tantra says the skull-observers and the Pāśupatas stand 'in the Īśvara and in the Dhruva' and are not re-created (11.184); the Lākula g |  | Not recorded in the tradition's own words. | Not recorded in the tradition's own words; scholarship reports an expanded hierarchy of wo | personal | Reconstructed entirely from others' texts; any statement of the Lākula view of the ultimate is provisional. | skeleton |
| Mantramārga (the Path of Mantras) | Śiva, Sadāśiva (the five-faced revealer of scripture), Parameśvara, Bhairava (in the Bhair | The Lord who reveals all scripture through five faces, as five streams (Kāmika pūrva 1.20–27).; Śiva's knowledge (śivajñāna) is the higher knowledge r |  | Disputed within the Mantramārga: the Siddhānta holds the soul eternally distinct, becoming | The Lord acts on the world through his power(s) and mantras; the Siddhānta treats māyā as  | personal | The Mantramārga is not doctrinally uniform. The Saiddhāntikas reject the non-dual reading of their scriptures and the id | skeleton |
| Mantrapīṭha (the Seat of Mantras) | Svacchandabhairava, Bhairava | Svacchandabhairava, a form of Aghora/Bhairava, worshipped with his consort Aghoreśvarī. |  |  |  | personal | Known here only at catalogue level; the Svacchandatantra's own doctrine is recorded by U19. | skeleton |
| Mata (the 'Doctrine'; the Mata scripture | svasambodha (one's own awareness), unbounded and complete | one's own awareness, unbounded (nirmaryāda) and complete (sampūrṇa) - the Mata line quoted at TĀ 4.263a; the undivided (akhaṇḍa) supreme reality (TĀ 4 |  | The ultimate is one's own awareness. | Not recorded. | not-posited | Reconstructed only from the Trika exegetes' reports (Abhinavagupta, Jayaratha); the Mata's own texts are not identified  | skeleton |
| Pāñcarātra | Bhagavān, Vāsudeva, Nārāyaṇa, Para Brahman as ṣāḍguṇya, Lakṣmī-Nārāyaṇa (Lakṣmī Tantra) | The ṣāḍguṇya — possessor of the six qualities — is the supreme Brahman, cause of all causes, free of all pairs of opposites and all limiting adjuncts  | He is called 'without qualities' (nirguṇa) because he is untouched by the qualities of pra | Individual souls depend on Bhagavān; by his grace (śaktipāta) their karmas are equalised a | The world issues from his Śakti in a pure creation (the vyūhas) and an other-than-pure cre | personal | Saṃhitās differ in emphasis (e.g. the Lakṣmī Tantra's Śakti-centred account); Śrīvaiṣṇava readers interpret the Pāñcarāt | skeleton |
| Pāśupata (Pāñcārthika Pāśupata) | Paśupati, Pati, Rudra, Maheśvara / Mahādeva, Śaṅkara, Īśāna | Pati: he 'reaches' and 'protects' the paśus by an infinite power of knowledge and by his lordship (PABh on PS 1.1).; Kāraṇa: by will (kāmitva) he prod | he does not depend on karma or on the soul (na karmāpekṣa, PABh on PS 2.6); he alone is no | The paśus are all sentient beings other than the Lord, even the gods from Brahmā down and  | The effect - the insentient kalās (elements, qualities, organs) and the souls - is eternal | personal | Pāśupata theism keeps the Lord and the soul distinct even in liberation and makes the Lord only the (efficient) cause; i | skeleton |
| Pātañjala Yoga (the Yoga darśana) | puruṣa / draṣṭṛ (the seer), citiśakti (the power of consciousness), kaivalya (aloneness) — | The seer is seeing alone; though pure, it sees by conforming to cognitions (YS 2.20).; Unchanging, it always knows the mind's activities (4.18); consc | not an object (only the seen is object: 4.19); not the mind, not the buddhi-sattva: 'utter | The puruṣa is one's true self (the seer); taking the instrument of seeing for the seer is  | The seen (prakṛti: elements and senses, three guṇas) is real, exists for the sake of the s | both | Yoga posits many puruṣas (2.22; YBh 2.22), a real prakṛti, and Īśvara as a distinct special puruṣa who is not the materi | skeleton |
| Pratyabhijñā (the philosophy of recognit | Maheśvara / Īśvara (the Lord), Paramātman, Citi, Parā vāk (supreme speech) | consciousness whose essence is reflexive awareness, supreme speech arising of itself; this is the Lord's primary freedom and sovereignty (ĪPK 1.5.13); | cannot be established or denied by any means of knowledge, since it is the knower itself ( | The Lord is one's own self, present but unrecognized, as an unrecognized lover gives no de | Objects are the Lord's manifestations, shown as if separate by his power of māyā while res | both | The Pratyabhijñā insists on an enduring conscious subject against the Buddhist denial of self, and on the reality of the | skeleton |
| Sāṃkhya | puruṣa (many), prakṛti / pradhāna / avyakta (one) | Puruṣa: conscious, witness, isolated, neutral, seer, non-agent; neither a producer nor a product; many (SK 3, 11, 17–19).; Prakṛti (mūlaprakṛti, pradh | Puruṣa is neither prakṛti nor vikṛti — neither a producer nor a product (SK 3).; No one (n | The self is puruṣa: each person is a distinct puruṣa, pure consciousness mistakenly identi | The world is the real transformation (pariṇāma) of prakṛti, pre-existing in it (satkārya), | impersonal | Classical Sāṃkhya posits two irreducible kinds of ultimate — the many puruṣas and the one prakṛti — and would reject rea | skeleton |
| Spanda (the doctrine of vibration) | Spanda (vibration), Śaṅkara, Svabhāva (one's own nature), sāmānya-spanda (the universal vi | that in which all this rests and from which it has come forth; its nature is unobstructed (Spandakārikā 1.2); the inner (antarmukha) agency, seat of o | where there is neither pain nor pleasure, neither object nor subject, nor even insentience | It is one's own nature (svabhāva), the knower-agent persisting through all states (SK 1.3, | The world emerges and dissolves with the unmeṣa and nimeṣa of the one Śaṅkara (SK 1.1); al | both | Spanda insists that the ultimate is dynamic; it would reject any account of a static, inactive absolute. | skeleton |
| Trika ('the Triad') | Anuttara, Bhairava, Parā (the supreme Goddess), Kālasaṅkarṣiṇī, Hṛdaya (the Heart) | the Heart of Bhairava, in which the whole moving and unmoving world rests as the great tree rests in the banyan seed (Parātrīśikā 24); Bhairava's stat | the forms of Bhairava with parts (sakala) are for meditation of the confused; in truth he  | The limited individual (nara/aṇu) is Śiva through Śakti; śakti is the door into Śiva (VBT  | The world is the unfolding of the Heart through the letters (mātṛkā) and the tattvas; it i | both | The Trika insists on the triadic self-unfolding of the one and on its own superiority to other revelations. | skeleton |
| Vaikhānasa | Nārāyaṇa, the supreme Brahman (nārāyaṇaparaṃ brahma), Viṣṇu, the five forms: Viṣṇu, Puruṣa | Nārāyaṇa is the supreme Brahman, the highest Self; his highest form is subtle, imperishable and partless (niṣkala); his gross form with parts (sakala) |  | The worshipper attains Viṣṇu's world and nearness to him in graded forms of liberation (sā | Nārāyaṇa is the cause of the whole world; Vikhanas, author of the Sūtra, is born of him (D | personal | The Vaikhānasas insist on the Vedic identity of their worship and would reject being classed with tantric Āgama theologi | skeleton |
| Vidyāpīṭha (the Seat of Vidyās) | Bhairava with the goddess(es), Kapālīśabhairava and Caṇḍā Kāpālinī (Brahmayāmala), Kālasaṅ | The supreme is Bhairava in union with his power(s); in later Vidyāpīṭha texts the goddess becomes primary. |  |  |  | both | Catalogue-level summary; the doctrinal views of the Trika and Kālīkula are recorded by U19/U24. | skeleton |

## 3. The path-map correspondence table

Not built yet: the path-map unit (U51) had not started. The alignment scheme is fixed in `config/data_model.md` — every stage of every
map gets an interpretive band: B0 entry → B1 ethics → B2 preparation → B3 concentration → B4 absorption → B5 first seeing →
B6 cultivation → B7 liberation → B8 activity after liberation. `scripts/report.py` prints the table as soon as maps exist.

## 4. The obstacle correspondence table

Not built yet (no obstacle entries so far). The synthesis pass S2 (`config/briefs/synthesis.md`) aligns kleśas, hindrances,
fetters, kaṣāyas, malas, antarāyas and doṣa imbalances into equivalence clusters once the lineage units have written them.

## 5. The thirty most convergent practices

Not meaningful yet: the only practices so far are the Vijñāna Bhairava's 112 contemplations (one lineage). Convergence
counts (independent lineage roots, sub-lineages counted once) are computed automatically by `scripts/merge.py`.

## 6. The twenty most important open items in the reconciliation queue

The queue is empty because the debates unit (U50) had not started. The fifteen coverage-map debates have fixed ids and will be
recorded side by side before any reconciliation.

## 7. The hallucination sweep

Not started (0 items checked). Its tooling is ready:
- `scripts/catalog.py` is a local catalogue of 25,922 digitized titles (GRETIL, DCS, Muktabodha, eBhāratī, SuttaCentral, CBETA) for existence checks.
- The sweep brief is `config/briefs/sourcing.md`; WebSearch supplies external evidence.
- Direct access to Wikipedia, GRETIL, archive.org and similar sites is blocked by this environment's egress policy (see DECISIONS).

The skeleton's own confidence
split is the best current guide to hallucination risk: 163 of 798 texts and 109 of 425 teachers are self-rated `low`.
Those are checked first.

## 8. Verified so far, and what runs next

Text-verified entries: **0**. Texts downloaded and segmented, ready for double extraction:
aitareya-upanisad (33), anapanasati-sutta (43), astavakra-gita (20), bhagavad-gita (701), brhadaranyaka-upanisad (441), chandogya-upanisad (629), dhammacakkappavattana-sutta (14), dhammapada (423), hatha-yoga-pradipika (387), isa-upanisad (18), katha-upanisad (120), kausitaki-upanisad-sharada (51), kena-upanisad (35), mahasatipatthana-sutta (22), mandukya-karika (214), mandukya-upanisad (12), mulamadhyamakakarika (27), mundaka-upanisad (65), platform-sutra (162), platform-sutra-dunhuang (86), prajnaparamita-hrdaya (9), prajnaparamita-hrdaya-sanskrit-short (10), prasna-upanisad (67), samkhya-karika (72), satipatthana-sutta (41), siva-sutra (75), spanda-karika (53), svetasvatara-upanisad (113), taittiriya-upanisad (48), vajracchedika (127), vijnana-bhairava-tantra (162), yoga-sutra (195).

Next, in order, as the usage limit allows:
1. Finish the 19 started skeleton units (nine resumed now; ten more next) and start the other 40 (U21–U59).
2. Run the hallucination sweep per finished unit.
3. Run the double extraction of the Gītā (6 chunks × extractors A/B, merger, fidelity checker), then the Yoga Sūtra, Upaniṣads,
   Pali suttas and the rest of the Phase D list.
4. Run the synthesis passes S1–S6 once the skeleton is complete, then the gap hunter.

**Pace.** Twenty agents used up the usage window in about 35 minutes, so the run will now go in bursts limited by that ceiling.
Concurrency is capped at about 10 so the orchestrator keeps headroom to merge and commit.

## 9. Coverage gaps

- Units not yet started (40): U14-visistadvaita, U21-natha-aghora, U22-tamil-siddha, U23-sakta-srividya, U24-kali-kaula, U25-alvar-bhakti-theory, U26-regional-bhakti, U27-sant-baul, U28-hatha-texts, U29-hatha-practices, U30-ayurveda-rasa, U31-sound-arts, U32-jyotisa, U33-sramana, U34-jain-canon, U35-jain-philosophy, U36-pali-suttas, U37-abhidhamma-visuddhimagga, U38-early-schools, U39-mahayana-sutras, U40-madhyamaka, U41-yogacara-pramana, U42-chan-zen, U43-pure-land, U44-indian-vajrayana, U45-nyingma-bon, U46-kagyu, U47-sakya-kadam-gelug, U48-jonang-chod-medicine-rime, U49-cross-family, U50-debates, U51-path-maps, U52-recent-teachers, U53-glossary-ultimate, U54-chinese-schools, U55-japan-korea-vietnam-nepal, U56-datta-haridasa-odisha, U57-ascetic-orders, U58-sacred-sciences-body-arts, U59-folk-regional.
- Texts not obtainable in this environment: the Sanskrit Tattvārtha Sūtra; the Sanskrit Vajracchedikā (the Chinese is used); Saraha's
  dohās and Tilopa's Gaṅgā Mahāmudrā (the Tibetan Tengyur has now been downloaded — to be located); Chekawa's lojong root text;
  a clean Maitrī Upaniṣad. See `GAPS.md`.
- Dangling references: 1,538 ids are cited but not yet defined (mostly teachings, terms and concepts owned by units that have not run).

## 10. How to navigate the atlas

- Start at `ATLAS/INDEX.md`. It links section indexes for lineages, texts, teachers, concepts, practices, obstacles, path maps,
  debates and terms, plus `ATLAS/ULTIMATE.md`, the table of every tradition's ultimate.
- Every page shows its verification level (`skeleton` / `sourced` / `text-verified`, and **[unverified]** where the sweep failed to confirm).
- Text pages list the verse-anchored teachings under each text, in verse order, with the four tags.
- Lineage pages gather that lineage's texts, teachers, practices, path maps, debates and its view of the ultimate.
- The machine-readable data is in `data/`, with teachings split by text in `data/teachings/`.
- Run logs: `PROGRESS.md` (resume point), `RUNLOG.md`, `DECISIONS.md`, `GAPS.md`, `RECONCILE_QUEUE.md`.
