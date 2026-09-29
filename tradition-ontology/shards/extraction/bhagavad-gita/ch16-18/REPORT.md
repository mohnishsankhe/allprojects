# Gītā ch16–18 merger (M) report
_(Returned as text by the merger subagent and saved verbatim by the orchestrator.)_

claude-opus-5-5 (Opus 5.5); effort setting: not visible to me.

Summary:
- The Gītā ch16-18 merge is done and validates with 0 errors in both `merged/` and the chunk dir; the one warning is "REPORT.md missing", which is expected.
- `merged/teachings.jsonl` holds 137 entries: 130 whole-verse entries, 3 chapter entries, 3 sentence entries (16.1-3, 17.5-6, 18.51-53) and `tea:bhagavad-gita:thesis`.
- Entities: concepts 35, disputes 2, obstacles 27, paths 1, phenomenology 5, practices 21, teachers 5, terms 117, ultimate 1. `disagreements.jsonl` has 648 lines; per-entry counts sum to 446.
- Skeleton decisions: 61, of which 51 upgrade, 10 correct and 0 retire.
- Checked by code: every `original` equals its segment, every linked id exists in data/ or merged/, all cross-refs resolve, no "ego" wording remains, every one of the 130 verses has an entry.
- Not checked:
  - Commentators' and schools' positions are recalled, not read from the bhāṣyas, and are marked so.
  - Tag and paraphrase choices are my judgement.
  - Notes are combined by code (A's notes plus B's non-duplicate sentences), so some repetition remains.

Files:
- /home/user/allprojects/tradition-ontology/shards/extraction/bhagavad-gita/ch16-18/merged/ (teachings.jsonl with the thesis, 9 entity files, skeleton_decisions.jsonl)
- /home/user/allprojects/tradition-ontology/shards/extraction/bhagavad-gita/ch16-18/disagreements.jsonl
- Drafts: /home/user/allprojects/tradition-ontology/shards/extraction/bhagavad-gita/ch16-18/_gen/M/ — entry point merge_m.py; also decisions.py, paras.py, entities_m.py, skeleton_m.py, thesis.py, checks.py

## Decisions for DECISIONS.md

- **Sentence entries** (split-verse rule):
  - Kept: 16.1-3, 17.5-6 and 18.51-53. The same-id skeleton entries 16.1-3 and 17.5-6 are upgraded or corrected into them; skeleton 18.50-53 now points to 18.50 plus the 18.51-53 span.
  - A's 16.13-16 is not kept. 16.13 has its own finite verbs inside the quoted speech (prāpsye, asti, bhaviṣyati), the same reason 14.22-25 was dropped. 16.13-15 open with "[they think:]", and the notes record the frame "iti ajñāna-vimohitāḥ … patanti".
  - Considered and not written:
    - 16.11-12: it describes conduct rather than stating a ground, result or definition.
    - 16.17-18 and 18.36-37: the first verse of each has a main clause.
- **Id harmonisation:**
  - cpt:five-causes-of-action (not A's five-factors); it uses the verses' word kāraṇa/hetu.
  - prc:om-tat-sat (not B's om-tat-sat-in-rites).
  - obs:mamatva (not the Purāṇic obs:mamata).
  - obs:manitva (not obs:mana, which is the Buddhist fetter).
  - prc:svadharma-anusthana (not prc:svakarma, which is from the Sāṃkhya-sūtra).
  - prc:isvararpana (not prc:isvararpana-karma, which is Bhāṭṭa Mīmāṃsā).
  - cpt:samatva → cpt:equanimity.
  - Phenomenology: phn:bhagavad-gita-delusion-destroyed-memory-regained, phn:bhagavad-gita-sanjaya-rejoicing, phn:bhagavad-gita-three-kinds-of-happiness.
  - New: trm:brahmabhuya contribution for 18.53 (as at 14.26); trm:brahmabhuta is now tied to 18.54 only.
- **Checked against data/ senses and not linked:**
  - Homonyms: trm:yaksa (Kena sense), trm:mana (Jain, Buddhist and Gauḍīya senses), trm:dosa (the entry mixes Pali dosa = hatred), trm:gati (Buddhist and Jain destinations; never linked for parā gati before), trm:adhisthana (controller, substratum or blessing, not "seat"), trm:bhuta-sarga (Sāṃkhya), trm:hari (Dvaita formula), trm:puja (āgamic rites), trm:svapna (dream), trm:mukta.
  - School-specific entries: obs:stabdhata (Dvaita), cpt:adhikara (Mīmāṃsā), cpt:buddhi (Sāṃkhya), cpt:antaryamin, prc:sattvika-tyaga (Viśiṣṭādvaita), cpt:bhakti-after-knowledge, cpt:twofold-nistha at 18.50.
  - Words not in the verse: trm:mumuksu, trm:trivarga, trm:purusartha.
  - prc:brahmacarya: neither extractor linked it; trm:brahmacarya is linked at 17.14.
- **18.66:** cpt:prapatti and trm:prapatti are deliberately not linked (B's choice kept). The notes record the carama-śloka reading (recalled) and why.
  - dsp:is-prapatti-an-upaya is linked, because its Viśiṣṭādvaita side cites 18.66.
  - dsp:duties-after-prapatti is not linked (it does not cite the verse).
  - B's dsp:renunciation-or-action-gita is not linked here (that dispute cites 18.1-12).
- **Dispute back-links added** where the data/ dispute cites the verse:
  - dsp:gita-primary-teaching at 18.17, 18.46, 18.54-56 and 18.64-66.
  - dsp:works-knowledge-grace at 18.56 and 18.66 (skeleton link carried).
  - dsp:status-of-veda at 16.23-24 (skeleton link carried).
  - dsp:souls-one-or-distinct at 18.55 (skeleton link carried). **Locus for U50.**
- **Renderings aligned with earlier merges:**
  - niyata karma "allotted action" (3.8), including in entity texts.
  - svādhyāya "recitation" (4.28); parā gati "the highest goal"; padam "place" (15.5); vijñāna left untranslated (7.2).
  - 18.65 worded as the text-verified 9.34.
  - "brahman" lower-case, as in ch13-15; "the sense of 'I'", never "ego".
  - Reflexive ātman kept open as "one's self" (16.21, 16.22, 18.16, 18.39); ātma-buddhi left open (18.37).
  - 16.8 aparaspara-sambhūta literal, not Śaṅkara's "mutual union"; 18.33 avyabhicāriṇyā construed with dhṛti (feminine).
- **Tags:**
  - The guṇa-classification 18.19-40 is "analytic"; the happiness verses stay "experiential".
  - The triads 18.7-9 and 17.17-19 are "seeker"; 17.14-16 are "ethical-social".
  - 18.17 is bridging/absolute/advanced, as 5.8.
  - 18.20, 18.54 and 18.55 are level "unmarked" (as 6.27); 18.71 is "beginner" (as 13.26); 17.23 is unmarked/ritual.
  - Types are the union of A and B where they differ; confidence is the lower of the two.
- **Ch. 13 cross-refs:** both extractors cited 700-verse numbers. They are renumbered to this edition: 13.16 → 13.17, 13.17 → 13.18, 13.7 → 13.8-12, 13.10 → 13.11.
- **Skeleton reconciliation ch16-18:** 61 → 51 upgrade, 10 correct, 0 retire. The 10 corrected, and why:
  - 16.1-3: jñānayoga as Śaṅkara's dvandva reading.
  - 16.6-7 and 18.29-32: pravṛtti/nivṛtti rendered as "ways".
  - 16.8: "mutual union".
  - 16.9-18: "lost souls" and "until death".
  - 17.7-10: kaṭu rendered "bitter".
  - 18.13-16: "(the body)" gloss and "Sāṃkhya doctrine".
  - 18.36-39: ātma-buddhi construal chosen.
  - 18.41-48: vijñāna rendered "realization".
  - 18.63: "than all secrets" (that superlative belongs to 18.64).
  - The skeleton's critical-text originals, including 17.23 with oṃ, are not carried.
- **Thesis:** `tea:bhagavad-gita:thesis` is written at confidence "moderate". It states what the six marks point to, in the text's words, and ends by saying the marks do not settle what "abandoning all dharmas" means or which means is final. The traditions' theses are only in its notes (recalled) and in dsp:gita-primary-teaching.
- **Errata for the post-ch18 pass** (kept as printed, noted per verse):
  - Speaker headings: as a separate line inside 16.1 and 18.2; fused to the first word at 17.1, 17.2, 18.73 and 18.74.
  - "śrṛṇu" at 16.6, 17.2, 17.7, 18.4, 18.29, 18.36, 18.64; "śrṛṇuyād" at 18.71.
  - Misplaced vowel signs: niśicatāḥ 16.11, tatitravidhaṃ 17.17, niśicataṃ 18.6, syātitrabhir 18.40, bhakitaṃ 18.68, kaśicanme 18.69.
  - asurīṃ 16.20; 17.23 lacks oṃ (supplied only as "[Oṃ]" in the paraphrase); 17.25 truncated at "mokṣakāṅkṣi"; "~l" at 18.17 and 18.71; 18.78 ends with "||18.78|".
- **For S5:**
  - The data/ trm:dosa entry conflates Skt doṣa with Pali dosa (= dveṣa).
  - trm:adhisthana and trm:mana hold mixed senses.
  - New ids to check: cpt:om-tat-sat (beside trm:om-tat-sat), obs:darpa, trm:dambha, trm:darpa, trm:hri, trm:astikya, trm:karma-codana, trm:karma-samgraha, cpt:sastra-as-pramana, cpt:karma-codana-and-karma-samgraha, cpt:three-kinds-of-sacrifice.
  - The path's bands (A's) are interpretive.
