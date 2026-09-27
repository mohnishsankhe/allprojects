# Principles

## The first principle

Ṛgveda 1.164.46: *ekaṃ sad viprā bahudhā vadanti* — "Truth is one; the wise call it by many names."

Every teaching is treated as a view of one truth from a particular **level**, **standpoint**, **path** and **stage**.
This lens operates **only in the interpretation layer**. It never licenses rewriting what a text says.

## The two layers (never mix them)

| Layer | What lives there | Rule |
|---|---|---|
| **Text layer** | `data/teachings/*.jsonl` — verse-anchored records of what a specific passage says | A faithful record. Once fidelity-checked, never altered; only corrected with a logged reason (`correction_log` on the entry + a line in `interpretation_log.jsonl` of kind `text-correction`). |
| **Interpretation layer** | concepts, term equivalences, reconciliations, path-map correspondences, obstacle alignments, convergence counts, the ultimate node | Every interpretive link cites the text-layer entries (`rests_on`: teaching ids) it depends on. Every change is logged in `interpretation_log.jsonl` with its reason. |

## The four tags (every teaching carries all four)

### 1. `level` — level of truth
| value | meaning | examples |
|---|---|---|
| `ultimate` | pāramārthika / paramattha-sacca / paramārtha-satya / niścaya | "Brahman alone is real"; "there is no arising" |
| `conventional` | vyāvahārika / sammuti-sacca / saṃvṛti-satya / vyavahāra | ritual injunctions, ethics, cosmology, the path itself |
| `illusory` | prātibhāsika (Advaita's third level: dream, rope-snake) | the snake seen in the rope |
| `bridging` | the passage explicitly relates two levels | BhG 2.16; MMK 24.8–10 |
| `unmarked` | the passage does not mark its level and the context does not settle it | |

### 2. `standpoint` — the perspective from which it is said (one primary value; optional `naya`)
| value | meaning |
|---|---|
| `absolute` | spoken from the side of the ultimate itself ("I am Brahman"; "no bondage, no liberation") |
| `seeker` | spoken to/for the bound practitioner (instruction, effort, method) |
| `divine` | from the Lord's / deity's side (grace, will, cosmic function, avatāra) |
| `cosmic` | cosmology, creation, the structure and cycles of worlds |
| `substance` | the enduring essence/whole (dravyārthika) |
| `mode` | the changing states, parts, particulars (paryāyārthika) |
| `causal` | causes, conditions, sequence (karma, dependent origination, satkārya) |
| `experiential` | first-person description of states, signs, visions |
| `analytic` | categorial analysis (tattvas, dhammas, padārthas, pramāṇas) |
| `apophatic` | by negation (neti neti, the tetralemma, "empty") |
| `devotional` | relational: servant/master, lover/beloved, child/mother |
| `ritual` | in terms of ritual action and its results |
| `ethical-social` | conduct, duty, community, stages of life |
| `polemical` | stated against an opponent's view (pūrvapakṣa/siddhānta) |

Optional `naya` field (only when the text itself uses or clearly implies it): `niscaya`, `vyavahara`, `naigama`, `sangraha`, `vyavahara-jain`, `rjusutra`, `sabda`, `samabhirudha`, `evambhuta`, `dravyarthika`, `paryayarthika`.

### 3. `path` — path by temperament (one or more)
`action` (karma), `knowledge` (jñāna), `devotion` (bhakti), `meditation` (dhyāna / rāja / samādhi / bhāvanā), `body-breath` (haṭha, prāṇāyāma, mudrā, bandha), `ritual` (yajña, pūjā, kriyā, dīkṣā), `sound` (mantra, nāda, japa, kīrtana), `general` (addressed to all paths).

### 4. `stage` — stage of the student (adhikāra)
`beginner` (manda / prathama), `intermediate` (madhyama), `advanced` (uttama), `realized` (describes the siddha / jīvanmukta / arahant / kevalin), `all`, `unmarked`.
Optional `stage_native`: the tradition's own stage label (e.g. "sādhana-bhakti", "sekha", "guṇasthāna 7", "ārambha-avasthā", "adhimukticaryā-bhūmi").

## The eight reconciliation principles (used only in the interpretation layer)

| # | id | principle | source of the principle |
|---|---|---|---|
| 1 | `P1-level` | **Level of truth** — practical (vyāvahārika) vs ultimate (pāramārthika) | Advaita's levels of reality; the Buddhist two truths |
| 2 | `P2-standpoint` | **Standpoint** — many-sidedness (anekāntavāda), sevenfold predication (syādvāda), standpoints (nayavāda) | Jain logic |
| 3 | `P3-path` | **Path by temperament** — action, knowledge, devotion, meditation, body-breath, ritual, sound; the chosen deity (iṣṭa-devatā) | Bhagavad Gītā's yogas |
| 4 | `P4-stage` | **Stage of the student** (adhikāra) | all traditions |
| 5 | `P5-neyartha` | **Provisional vs definitive** (neyārtha / nītārtha) | Buddhist hermeneutics (Akṣayamatinirdeśa, Saṃdhinirmocana) |
| 6 | `P6-upaya` | **Skillful means** (upāya-kauśalya) | Lotus Sūtra, Vimalakīrti |
| 7 | `P7-arthavada` | **Praise passages** (arthavāda) — exaggerated praise is rhetorical, not doctrinal | Mīmāṃsā |
| 8 | `P8-six-marks` | **The six marks of purport** (ṣaḍ-liṅga): upakrama-upasaṃhāra (opening & closing), abhyāsa (repetition), apūrvatā (novelty), phala (stated result), arthavāda (praise), upapatti (reasoned demonstration) | Mīmāṃsā & Vedānta |

## Rules

1. **Reconcile only in the interpretation layer.** Never rewrite, soften or merge a text-layer teaching.
2. **Every reconciliation** gets a one-line explanation naming the principle used (`principle`: one of the ids above, plus `explanation`).
3. **If no principle reconciles a pair**, put it in `RECONCILE_QUEUE.md` (and `status: "queued"` in `disputes.json`) with candidate readings. **Never label anything a contradiction; label it "not yet reconciled".**
4. **Record every debate faithfully, with both sides, before any reconciliation.** Each side is stated in its own strongest terms, from its own texts.
5. **Reconciliation must not erase distinctions the traditions themselves insist on.** If a tradition explicitly denies an equivalence (e.g. Madhva's eternal difference; Theravāda's rejection of a permanent self; Śaiva Siddhānta's rejection of Advaita's unreality of the world), the reconciliation records that denial and states exactly what it does and does not claim ("reconciled under P2 as complementary standpoints; the Dvaita tradition itself rejects this reconciliation").
6. Equivalences between terms/concepts are graded: `exact`, `partial`, `same-under-standpoint` (with the standpoint named), `analogous`, `contested`.
7. Opponents' reports (e.g. the Ājīvikas known only through Buddhist and Jain texts) are tagged `reported_by_opponent: true` and name the reporting source.
8. Tradition's account vs scholarly account are always separately labeled (dates, authorship, realization).
9. No modern research, psychology or science is used to interpret teachings. Scholarly dating and attribution are allowed only as labeled metadata.
