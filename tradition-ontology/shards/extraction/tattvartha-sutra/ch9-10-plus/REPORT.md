# Tattvārtha Sūtra ch.9-10 plus 2.1, 2.7, 5.16, 5.30 — Role S single extraction
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Output folder: /home/user/allprojects/tradition-ontology/shards/extraction/tattvartha-sutra/ch9-10-plus/single/
Scripts: /home/user/allprojects/tradition-ontology/shards/extraction/tattvartha-sutra/ch9-10-plus/_gen/S/ (data1.py holds the entries, gen.py writes the teachings and skeleton decisions, ent.py writes the entity files).

## What was done
- Every `original.text` is copied by code from `sources_raw/prepared/tattvartha-sutra/segments.jsonl`. Edition and licence come from META.json.
- Chapter entries `tea:tattvartha-sutra:ch9` and `ch10` are written. There is no thesis entry.
- Verification is `sourced`, with `protocol: insight-p1-single+spot`, for every teaching.
- The tags use `level: conventional` throughout. I did not mark liberation or the siddha state as `ultimate`, because the sūtras do not mark a level.
- Product-note items follow the text's order and terms. For 9.1-9.7 I listed the guptis, samitis, ten dharmas and twelve anuprekṣās as the sūtras list them. For 9.27-9.46 I listed the four dhyānas, their objects and their holders, with no modern psychology words. The ārta kinds are rendered "pained" and the raudra kinds "fierce".
- The 10.x entries keep the sūtras' order and terms.

## Mandatory rule 1: existing ids read before linking
- I read the `data/` entry of every id I linked. All Jain terms already carry a `lin:jainism` definition in the data.
- I therefore linked the existing ids for gupti, samiti, anuprekṣā, saṃvara, nirjarā, dhyāna, ārta and the other dhyāna terms, dharma, tapas and the rest, and added Jain-sense notes on the entries.
- Linked ids where the Jain sense is one of several senses on the same id: dhyāna, dharma, tapas, vitarka, vīcāra, nidāna, yoga, jīva, siddha, mokṣa, loka, aloka.
- Ids not linked because the data has no Jain sense:
  - trm:tirtha (pilgrimage sense only) → new `trm:tirtha-jain`.
  - trm:antaraya (Purāṇic and Yoga senses only) → new `trm:antaraya-karma`.
  - trm:upadhi, trm:muhurta, trm:gana, trm:kula, trm:sangha, trm:apaya, trm:ajna. I used the existing `trm:ajna-vicaya` and `trm:apaya-vicaya` instead, and named the groups in the paraphrase without a term link.
- New term ids (Jain sense): pulaka, vakusa, kusila, snataka, pariharavisuddhi, suksmasamparaya-caritra, smrti-samanvahara, pratisevana, tirtha-jain, antaraya-karma.
- Contributions to existing ids, with my `rests_on`: trm:chedopasthapana (existing entry has only a Śvetāmbara definition), samvara, gupti, samiti, anuprekṣā, dhyāna, ārta, raudra, dharma-dhyāna and śukla-dhyāna.

## Mandatory rule 2: commentary
Every commentators' reading is in `notes`, labelled "Commentators' reading (Sarvārthasiddhi, Rājavārttika; recalled, not in the local segments)". The local segments contain no commentary. All commentator content is therefore my recollection, not read from a source here. The paraphrases contain only what the sūtra says.

## Recension (Śvetāmbara) — recalled, not checked
- Flagged in notes where it matters.
- 2.7: I recall the Śvetāmbara text adds "ādīni" (jīva-bhavyābhavyatvādīni ca).
- 5.30: I recall it as 5.29 in the Śvetāmbara numbering, because there is no separate "sat dravya-lakṣaṇam" sūtra.
- 9.18: the wording differs in the Śvetāmbara text.
- 9.22: the Śvetāmbara list has ten forms of expiation.
- 9.36: I recall the Śvetāmbara text adding a sūtra that assigns dharmya dhyāna to the upaśānta- and kṣīṇa-kaṣāya stages, which shifts the later numbers by one.
- 9.46: the Śvetāmbara form is "bakuśa".
- I could not verify any of these against a local copy.

## Points for the orchestrator
1. The segments carry no numbers for the counts given in sūtras 9.13-9.17, 9.21 and 9.22 beyond the text itself. Restricted sūtras (9.8-9.17, 9.19) omit counts and lists in the paraphrase.
2. In 9.39 the segment reads "-kriyā-pratipāti" and "-kriyā-nivartīni". I read them as sandhi-joined negatives (apratipātin, anivartin) and said so in the note. The term ids `trm:suksmakriya-apratipati` and `trm:vyuparatakriya-anivarti` already existed with this sense.
3. The segments have some spelling quirks, which I did not alter: "kriryānivartīni" in 9.39 and "miticāritram" in 9.18. The originals are copied exactly.
4. 9.42 (the second śukla dhyāna is without vīcāra) sits beside 9.41 (both first two have vīcāra). I recorded this as the commentators' narrowing in the note, not as a contradiction.
5. `trm:pulaka`, `vakusa`, `kusila` and `snataka` hold only the sūtra's own naming (a slot in the list of five). Their content comes from the commentators and is not recorded, so a later pass with commentary access could enrich them.
6. The contributions to existing concepts and terms may overlap with `karma-passions/final` (for example cpt:five-bhavas and trm:samvara). The merge unions them.
7. I did not run git. I wrote only inside `ch9-10-plus/single` and `ch9-10-plus/_gen/S`.

## Judge checklist
- Check the three low entries: 9.26, 9.41 and 10.3.
- Check the restricted entries 9.8-9.17 and 9.19 for detail leaking into the paraphrase.
- Check my construals of "ekāgra-cintā-nirodha" in 9.27, the parse of the ten names in 9.45 and "pratyekabuddha-bodhita" in 10.9.
- Check that the chapter 9 entry's description of 9.8-9.19 stays summary-only.
