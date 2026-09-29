# Decisions

Conservative choices made without asking, with reasons. Newest last.

- 2026-09-28 04:08 IST — **Session start time.** The run began at 03:53 IST on 2026-09-28, so "tonight" is about three hours before the 07:00 IST morning report. Phases B–D run in parallel where possible; the morning report reflects whatever is finished at 07:00, and work continues afterwards.
- 2026-09-28 04:08 IST — **Network access.** This cloud container's egress policy blocks direct access to Wikipedia, GRETIL, SuttaCentral.net, archive.org, sacred-texts, CBETA online, 84000, BDRC, Muktabodha, Wikisource and similar sites (HTTP 403 at the proxy). GitHub (git clone, raw.githubusercontent.com) is allowed, and the WebSearch tool works. Therefore: (a) source texts come from openly licensed GitHub-hosted corpora (SuttaCentral bilara-data [CC0], the DCS Sanskrit corpus, sanskrit/raw_etexts, CBETA XML P5, Esukhia Derge Kangyur/Tengyur, gita/gita, GITenberg); (b) the hallucination sweep confirms facts through WebSearch result titles/URLs/snippets and through the downloaded catalogues, and records the evidence URLs; (c) anything reachable only on blocked sites is listed in GAPS.md.
- 2026-09-28 04:08 IST — **Data folder.** The JSON/JSONL files named in Part 6 live in `data/` (not the folder root) to keep the root readable; logs and reports stay at the root.
- 2026-09-28 04:08 IST — **Shards + merge.** Subagents write per-unit shards; `scripts/merge.py` is the only writer of `data/`. This avoids parallel write conflicts and gives a reproducible merge with a conflict log.
- 2026-09-28 04:08 IST — **Units.** The skeleton sweep uses 59 units (one per lineage or lineage group; see config/registry.md). Section I (the user's addendum) arrived before launch and was folded in: six new units (U54–U59) and scope additions to U08, U17, U19, U22, U24, U26, U27, U34, U35, U38, U43, U52.
- 2026-09-28 04:08 IST — **Standpoint vocabulary.** "Standpoint" is tagged with a controlled list (absolute, seeker, divine, cosmic, substance, mode, causal, experiential, analytic, apophatic, devotional, ritual, ethical-social, polemical) plus an optional Jain `naya`, so that P2 can be applied across traditions; see config/principles.md.
- 2026-09-28 04:08 IST — **Path-map bands.** To build one correspondence table across all path maps, every stage gets an interpretive band B0–B8 (entry → ethics → preparation → concentration → absorption → first seeing → cultivation → liberation → post-liberation activity). Bands are interpretation-layer claims, not text-layer claims.
- 2026-09-28 04:08 IST — **Recent teachers' ids** use their common romanised names (tch:ramakrishna) rather than the IAST slug, because that is how they are known; registry ids win over the slug rule.
- 2026-09-28 04:37 IST — **Concurrency cap.** The environment allows at most 20 concurrent subagents. The skeleton sweep therefore runs as a rolling queue: U01–U20 first, then each finished slot launches the next unit (U21 → U59). Each queued unit's scope and checklist is saved in `config/briefs/units/<unit>.md` so launches are reproducible and a restart can resume from PROGRESS.md.
- 2026-09-28 04:45 IST — **A thirteenth teaching type, `narrative`.** Part 7 requires reading and extracting every verse. Purely framing verses (e.g. the battlefield narration of Bhagavad Gītā 1) teach nothing doctrinal; forcing them into one of the twelve types would misrepresent them. They are recorded with type `narrative` so the text layer is complete without distortion.
- 2026-09-28 04:45 IST — **Paraphrase basis and [AI-translated].** Verified-core paraphrases are made directly from the original-language text (e.g. the Sanskrit of the Gītā), not from any modern copyrighted translation. They are marked `[AI-translated]` only for texts that have no published translation (Wave 4), as Part 5 specifies; every teaching carries `translation_basis` stating how its paraphrase was made.
- 2026-09-28 04:45 IST — **Gītā text.** The Sanskrit vulgate from github.com/gita/gita (Unlicense) is used for the root text: 701 verse entries, including the extra verse at the head of chapter 13 found in some editions (Śaṅkara's text has 700). Its bundled modern translations (Sivananda, Gambhirananda, Purohit, etc.) are third-party works and are not used or stored. Its Sanskrit commentaries (Śaṅkara, Rāmānuja, Madhva, Abhinavagupta, Śrīdhara, Madhusūdana and others) are public-domain texts, reserved for Wave 2.
- 2026-09-28 04:51 IST — **Slot allocation.** With 20 concurrent subagents and 59 skeleton units, running the phases strictly one after another would leave the 07:00 report with nothing sourced or verified. The skeleton sweep keeps most slots, but as slots free up a few are given to the hallucination sweep of finished units and to the verified-core extraction (Gītā first). The phases don't depend on each other at the unit level: extraction upgrades matching skeleton entries at merge time.
- 2026-09-28 04:51 IST — **Verified-core editions.** Principal Upaniṣads use the Advaita Śāradā (Śṛṅgeri) mūla texts with traditional adhyāya.section.verse numbering (e.g. Kaṭha 1.3.3), not Olivelle's continuous vallī numbering used in some GRETIL files; BĀU 3.9's closing tree verses are numbered 3.9.28.1–7 as conventionally cited. Yoga Sūtra: 195 sūtras as in Vyāsa's recension (3.56 of some editions does not occur). Sāṃkhya Kārikā: 72 verses as in the Jayamaṅgalā edition.
- 2026-09-28 07:03 IST — **Pacing under the usage limit.** Twenty concurrent Opus subagents exhausted the account's usage window in about 35 minutes, and the orchestrator was stopped along with them. From now on, concurrency is held to about 10, so the orchestrator keeps headroom to merge, commit and report. Interrupted agents are resumed with their context instead of being relaunched from scratch, so no reading is repeated.
- 2026-09-28 07:19 IST — **Sub-lineages added by units are accepted when they are real divisions the texts themselves name.** U08 added lin:mantrapitha, lin:vidyapitha, lin:vama-srotas, lin:garuda-tantra, lin:bhuta-tantra (parent lin:mantramarga — the streams and pīṭhas of the Śaiva scriptures); U15 added four Mādhva maṭha lineages; U20 added lin:pancacarya, lin:sarana-vacana, lin:aradhya-saiva. They are kept; convergence counts treat sub-lineages as one root, so they cannot inflate convergence.
- 2026-09-28 07:19 IST — **Subagent reports.** The harness refuses report-file writes by subagents; each unit returns its REPORT.md as text and the orchestrator saves it verbatim (extracted from the hand-back, not retyped).
- 2026-09-28 07:47 IST — **Recent lineages created by units are kept and flagged `recent: true` for the user's inclusion/exclusion decision (Part 5, Wave 5)** — e.g. lin:arya-samaj (U01, for Dayānanda's reading of the Saṃhitās).

## 2026-09-28 08:00 IST — id clash src:tatparyacandrika
- U05 used `src:tatparyacandrika` for Vedānta Deśika's Tātparyacandrikā (sub-commentary on Rāmānuja's Gītā-bhāṣya); U15 used it for Vyāsatīrtha's Tātparyacandrikā (Dvaita, on Jayatīrtha's Tattvaprakāśikā); U14 created `src:tatparyacandrika-desika`.
- Conservative choice: the bare id stays with Vyāsatīrtha's work (the one commonly called "the Candrikā" and cited by U15's Candrikāprakāśa); Deśika's work is `src:tatparyacandrika-desika`. Implemented as an orchestrator id remap (`config/id_remap.json`, applied by `scripts/merge.py` to U05's shard only; each remap is listed in data/reports/conflicts.jsonl). No unit shard was edited.

## 2026-09-28 08:21 IST — extractor independence (shared scratchpad)
- Gītā ch01-03: extractors A and B both used the session's shared scratchpad folder `bg/` for drafts, and B's part files overwrote A's p1/p2 drafts. A reports it saw only B's file names, line counts and first ids, never content, and rebuilt from its own private drafts; independence judged preserved (the merger's disagreement log will show whether the two readings are genuinely independent).
- Fix for all later double extractions: each extractor drafts only in `shards/extraction/<slug>/<chunk>/_gen/<ROLE>/` (git-ignored) and is told never to use the shared scratchpad or any other role's folder.

## 2026-09-28 08:43 IST — homonym tch:laksmidhara
- U02 and U07 use `tch:laksmidhara` for Bhaṭṭa Lakṣmīdhara, minister of Govindacandra and author of the Kṛtyakalpataru (12th c.); U08 used it for the Saundaryalaharī commentator; U23 created `tch:lolla-laksmidhara` for the commentator (Bhāskararāya calls him "Lalla").
- Conservative choice: the bare id stays with the Kṛtyakalpataru author (two units, and the registry-style dharmaśāstra use); U08's use is remapped to `tch:lolla-laksmidhara` via `config/id_remap.json` (all three U08 entries that mention it — src:laksmidhara, tch:laksmidhara, tea:laksmidhara:31 — refer to the commentator). The commentary itself keeps the id `src:laksmidhara`.

## 2026-09-28 08:44 IST — new sub-lineage lin:bhakti-sastra (U25)
- U25 created `lin:bhakti-sastra` for the Nārada and Śāṇḍilya Bhakti Sūtras (the texts name a "bhakti-śāstra", NBS 76, and "bhaktyācāryas", NBS 83) plus Vopadeva's Muktāphala and Viṣṇupurī's Bhaktiratnāvalī. Parent `lin:bhagavata-early` on the tradition's account (Nārada and Śāṇḍilya as Bhāgavata/Pāñcarātra sages), not as a claim of historical continuity; this keeps convergence counts from treating the sūtras as an independent root. Accepted (conservative: it adds no independent root).
- U25 also split Bhakti "hearing" (`prc:sravana-bhakti`) from Vedāntic hearing (`prc:sravana`), linked as analogous; and disambiguated `src:tiruppallantu-periyalvar` from U18's Śaiva `src:tiruppallantu`.

## 2026-09-28 08:48 IST — U27 lineage choices
- `lin:baul` is marked family "shared" (Vaiṣṇava-Sahajiyā, Nāth and — on a scholarly hypothesis — Buddhist Sahajiyā streams, plus Muslim Fakirs); all other Sant lineages "vedic" with a note that the Sants reject Veda and Qur'ān alike. Accepted: "shared" is the conservative label for a lineage the traditions themselves describe as crossing Hindu and Muslim lines.
- New named sub-lineages accepted (all recognized divisions): kabir-chaura, dharamdasi-kabir-panth, niranjani, ramsnehi, charandasi, satnami, garibdasi, radhasoami-agra, radha-soami-satsang-beas, ruhani-satsang, santmat-maharshi-mehi, balarami, sahebdhani. `lin:satnami` covers three distinct movements (Narnaul, Jagjīvandās, Ghāsīdās) and is flagged for splitting in Wave 2.
- Sikh scripture (src:adi-granth) is recorded as context only (out of scope), as are Sufi orders.
- Deliberately not recorded: the Sant Mat five names and the Kartābhajā mantra (initiatory secrets).

## 2026-09-28 08:51 IST — U26 lineages; classificatory groupings excluded from convergence
- U26 created `lin:mirabai` (no formal sampradāya — the entry says so), `lin:ramdasi` (Samartha sampradāya), `lin:rasik-ramanandi`, the four Ekaśaraṇa saṃhatis, and `lin:regional-bhakti-poets` — a classificatory grouping (Narsinh Mehta, Annamācārya, Tyāgarāja, Caṇḍīdās, Vidyāpati, Bhadrācala Rāmadās), not a tradition. Accepted.
- Conservative choice: `lin:regional-bhakti-poets` and U05's descriptive `lin:epic-teaching` are added to the UMBRELLAS set in scripts/merge.py, so they never count as independent roots in convergence counts (a practice attested only by poets in that grouping counts as 0 roots from it).
- U26 kept `tch:sena` as one entry (Marathi and Hindi Sena), with the identity dispute noted; and used `trm:hita-radhavallabha` because `trm:hita` already names the Upaniṣadic hitā channels.

## 2026-09-28 08:54 IST — Gītā extraction: id harmonisation (merger ch01-03)
- Where the two extractors used different ids for the same thing, the merger reused an existing skeleton/data id when one matched exactly (cpt:niskama-karma, cpt:senses-mind-intellect-hierarchy, cpt:gita-transmission, cpt:liberation, obs:attachment-to-fruits, prc:isvararpana, phn:arjuna-despondency, phn:awake-in-the-night-of-beings, dsp:renunciation-or-action-gita). B's cpt:sat-and-asat was not used (in data/ it names being/non-being at the origin); the Gītā 2.16 idea is cpt:real-and-unreal. Later Gītā chunks use the same ids (sent to the ch04-06 merger).
- Flagged for S5 dedupe: cpt:samatva ≈ cpt:equanimity; cpt:imperishable-embodied-self ≈ cpt:the-self; prc:indriya-samyama ≈ prc:indriya-nigraha.
- Skeleton reconciliation ch1–3: 73 skeleton teachings → 72 upgrade, 1 correct (3.10–16: the skeleton's gloss of brahman in 3.15 as "the Veda" is a commentators' reading), 0 retire.

## 2026-09-28 09:06 IST — Gītā edition errata (pending text-layer correction)
- The gita/gita Devanāgarī has old-font conjunct glitches carried into the IAST (e.g. निश्िचतं → "niśicataṃ" for niścitaṃ, "kaśicat" for kaścit, "śrṛṇu" for śṛṇu, "ścaśurāḥ" for śvaśurāḥ, a stray nukta at 1.26) and speaker headings inside some verses. Extractors keep `original` exactly as printed (text layer never silently altered) and note each glitch.
- Decision: after all 18 chapters are text-verified, one logged text-correction pass will normalise these glitches in `original.text` (each change with a correction_log item citing the Devanāgarī and the standard reading), and the prepared segments will be regenerated with a documented errata table. Until then the glitches stand, noted per verse.
- First text-verified chunk: Gītā 1–3 — 165 teachings (151 passed, 14 fixed, 0 failed by the fidelity checker); examples of fixes: 2.16 no longer picks "unreal/real" over "non-existent/existent"; 2.43 kāmātman read reflexively; "ego" replaced by "the sense of 'I' (ahaṃkāra)"; 3.42's "he" no longer linked to ātman as if the text said so.

## 2026-09-28 09:12 IST — U30 lineage family and homonyms
- `lin:ayurveda` and `lin:rasa-sastra` marked family "shared" (Āyurveda calls itself an upāṅga of the Atharvaveda but Buddhist and Jain authors wrote within it; Rasa is mainly Śaiva but has Buddhist-ascribed and Jain-commented works). Accepted. Sub-lineages lin:atreya-sampradaya, lin:dhanvantari-sampradaya, lin:kerala-astavaidya (low) accepted.
- Homonym teacher ids kept apart: tch:nagarjuna-siddha / tch:nagarjuna; tch:govinda-rasahrdaya / tch:govinda-bhagavatpada; tch:vyadi-rasasiddha / tch:vyadi; tch:kumarasiras-bharadvaja / tch:bharadvaja; tch:sarngadhara-vaidya / tch:sarngadhara-anthologist. śamana filed as trm:samsamana to avoid colliding with trm:samana (the breath).

## 2026-09-29 16:00 IST — weekly usage limit; resumption policy
- 2026-09-28 ~09:20 IST every running subagent (13) stopped with "You've hit your weekly limit · resets Sep 29, 10am (UTC)". Partial shards were committed as they stood. Resumed after the reset (2026-09-29 15:59 IST) by messaging each stopped agent (it continues from its own transcript and the files on disk), not by relaunching, so no finished work is redone.
- Pacing from now on: at most ~10 concurrent subagents, and the orchestrator keeps merges/atlas builds to milestones, because the weekly allowance — not wall time — is the binding constraint. Nothing in scope is dropped; the run simply continues across allowance windows.
- U31 (sound arts) had already handed back its complete report before the stop; saved (0 validator errors).

## 2026-09-29 16:05 IST — Gītā extraction: scheme for split verses (merger ch04-06)
- Every verse keeps one whole-verse entry. A half-verse "/2" entry is not kept when the halves are one thought. A sentence-span entry `tea:bhagavad-gita:<c>.<v1>-<v2>` is kept only when one verse of the sentence has no main clause and the span states a ground, result or definition (ch04-06: 5.8-9, 5.27-28, 6.20-23). Instructional sequences run verse by verse with a "[continuing <ref>]" marker. Applies to all later Gītā chunks.
- Skeleton reconciliation ch4–6: 67 → 63 upgrade, 4 correct (5.14-15, 6.10-32, 6.13-14, 6.40-45: the skeleton had put a commentator's gloss into the paraphrase), 0 retire.

## 2026-09-29 16:17 IST — verification level of entities touched by text extraction
- Fidelity checkers raise TEACHINGS to text-verified. Entity entries (terms, concepts, practices, …) are shared across units and carry several lineages' definitions, so an extraction chunk does not raise the whole entity: it adds a `verification.checks` record (phase D, method text, result confirmed/corrected) to the entry. The merge will show per-entity "checked against text by N chunks" without presenting other units' skeleton definitions as verified. (Proposed by the ch04-06 fidelity checker; adopted as the conservative choice.)
- Gītā 4–6 text-verified: 124 teachings — 109 passed, 15 fixed, 0 failed. Pattern to watch in all chunks (for the misreading hunter): citta/cetas flattened to "mind", reflexive ātman read as "the self" (4.40 saṃśayātman), a paraphrase silently picking one commentator's construal (5.15 vibhu, 5.17 tad-ātman, 6.7 paramātmā).

## 2026-09-29 16:28 IST — Jain duplicate ids (U33/U34/U35)
- The Uvāsagadasāo had two ids: U33 `src:uvasagadasao` (Prakrit form) and U34 `src:upasakadasa` (the registry's Sanskrit pattern). Kept `src:upasakadasa`; U33's source and its three teachings (tea:uvasagadasao:6, :7, :7/2 → tea:upasakadasa:…) remapped via config/id_remap.json.
- The debate on whether the kevalin eats had two ids: U34 `dsp:kevalin-eats` (the id the brief fixes) and U35 `dsp:kevali-bhukti`. Kept `dsp:kevalin-eats`; both units' references remapped, so the two sides lists union at merge.
- U34's other shared ids (Mūlācāra, Bhagavatī Ārādhanā, Tiloyapaṇṇatti, Kundakunda commentaries, Ādipurāṇa, …) are the same ids as U35's and union at merge; no remap needed.

## 2026-09-29 16:38 IST — sourcing corrections apply per unit, before merging
- A Phase C correction replaces a field (e.g. a practice's `sources` list). Applied after merging, it would overwrite what OTHER units contributed to a shared id. scripts/merge.py now applies each sweep's corrections to the checked unit's own shard entries before entities are merged (logged in correction_log and interpretation_log as before); apply_checks only records the check and raises skeleton → sourced.

## 2026-09-29 16:40 IST — Gītā extraction: merger ch07-09
- Scheme (as fixed by the ch04-06 merge): one whole-verse entry per verse, no '/2' entries; the merger added two sentence entries that neither extractor wrote, `tea:bhagavad-gita:8.9-10` and `tea:bhagavad-gita:8.12-13`, because 8.9 (relative clause) and 8.12 (absolutives) have no main clause and each span states a result (like 5.27-28). The skeleton teaching 8.12-13 is upgraded to the entry of the same id.
- Ids: A's `cpt:aisvara-yoga` kept over B's `cpt:yogam-aisvaram` (stem form; name keeps 'yogam aiśvaram'). Existing Gītā-unit ids preferred over school-specific ones: cpt:surrender-to-the-lord (not cpt:prapatti), prc:saranagati (not prc:prapatti), cpt:two-paths-after-death (not cpt:devayana-pitryana), cpt:day-and-night-of-brahma (not cpt:ages-and-day-of-brahma), cpt:gita-transmission (not cpt:secrecy-and-eligibility), prc:utkranti-yoga (restricted, summary only; not A's prc:gita-yogic-departure), obs:dvandva (not obs:dvandva-moha), trm:ahankara, trm:karma-bandha; B's cpt:punaravrtti-anavrtti -> cpt:rebirth (+ cpt:liberation where non-return is stated, as ch04-06 at 5.17); B's obs:karma-bondage -> cpt:bondage-of-action. A's undefined disputes mapped (dsp:saguna-nirguna -> dsp:bhagavad-gita-the-lords-embodiment; dsp:women-caste-liberation -> dsp:devotee-birth-and-caste; dsp:souls-one-or-distinct -> dsp:bhakti-jnana-precedence at 7.18, dropped at 9.15). Term links follow the verse's words: trm:devayana/trm:pitryana not linked and A's entries for them not kept (the Gītā does not use the words, as ch04-06 did with trm:guru). New: trm:anavrtti (8.23, 8.26; exact equivalent of trm:apunaravrtti).
- Cross-references to ch. 13 use this edition's numbering (one higher than the 700-verse numbering): 7.4 -> 13.6, 8.20 -> 13.28, 9.19 -> 13.13; each entry's notes say so.
- Flagged for S5 dedupe/equivalence: cpt:last-thought (ch01-03, 2.72) ≈ cpt:last-thought-at-death (U05; chs. 7-9); cpt:two-paths-after-death ≈ cpt:devayana-pitryana; cpt:surrender-to-the-lord ≈ cpt:prapatti; prc:saranagati ≈ prc:prapatti.
- Skeleton reconciliation ch7–9: 46 → 40 upgrade, 6 correct (7.1-2 and 9.1-2 vijñāna glossed 'realization'; 7.4-5 'ego'; 8.3-4 visarga as 'creative offering' and 'its own nature'; 8.11 'celibacy'; 9.4-5 'divine yoga' for yogam aiśvaram), 0 retire.

## 2026-09-29 16:53 IST — U40 ids
- Śāntarakṣita's Tattvasaṅgraha: U09 cited it as `src:tattvasangraha-santaraksita`; U12, U31 and U40 use `src:tattvasangraha` (Sadyojyoti's work is `src:tattvasangraha-sadyojyoti`). U09's reference remapped to `src:tattvasangraha`.
- Homonyms kept apart by U40: `tch:haribhadra-buddhist` (Ālokā author) vs `tch:haribhadra` (Jain); `tch:jayananda-madhyamaka` vs `tch:jayananda` (Bengali Vaiṣṇava poet).
- U40 note: MMK 24.18 alone states the identity of dependent origination, emptiness, dependent designation and the middle way (24.19 says no dharma is non-empty because none is not dependently arisen).

## 2026-09-29 17:00 IST — U41 lineages and dispute overlaps
- New lineages accepted (real, named schools or doxographic divisions): `lin:satyakaravada`, `lin:alikakaravada` (sub-divisions of Yogācāra per the Indian/Tibetan doxographies), `lin:dilun`, `lin:shelun` (Chinese Yogācāra-lineage schools), `lin:hosso` (Japanese Faxiang).
- Dispute overlaps for S6: `dsp:are-things-momentary` (U09) ≈ `dsp:momentariness` (U11); `dsp:object-independent-of-mind` (U10) ≈ `dsp:external-objects`. Not remapped (each may carry a differently framed question); S6 relates them or merges sides with a logged decision.
- Pramāṇavārttika teaching ids in U41 follow the local e-text's chapter order (1 Pramāṇasiddhi, 2 Pratyakṣa, 3 Svārthānumāna, 4 Parārthānumāna); each teaching's notes give the usual (Tibetan/Miyasaka) citation. Later extraction must keep one convention and say which.

## 2026-09-29 17:04 IST — Taittirīya preparation fix (sharada_parse)
- The Phase C sweep of U03 found TU 3.8–3.9 missing from the prepared text. Cause: the advaita-shAradA edition prints TU 1.12, 3.8 and 3.9 without a verse number, and the parser silently dropped sections with no number.
- Fix (conservative, nothing invented): a section with no number is kept as verse 1 of that section, with a note saying the edition prints it unnumbered. The śānti invocations before TU 2.1 and 3.1 are kept in separate fields (invocation_deva/_iast) rather than merged into the first verse. In TU 1.1 the invocation is the section's own text, so it stays as the text. Commentary colophons ("iti śrīmat… bhāṣye …") are stripped.
- Result: TU has 51 segments (48 before). New: 1.12.1, 3.8.1, 3.9.1. Every earlier ref keeps its number. The other ten Upaniṣads keep their segment counts.

## 2026-09-29 17:08 IST — Lojong root text: reconstruct from lemmata; modern commentaries only confirm wording
- No open e-text gives Chekawa's Seven Points root on its own. The classical commentary in *Blo sbyong legs bshad kun 'dus* (OpenPecha-Data P000258, a Derge xylograph edition; pre-modern, public domain) quotes every root line as a headword ("… ། །ཞེས་བསྟན་ཏོ" / "ཅེས་པ").
- Conservative choice: the Phase D lojong unit rebuilds the root from those headwords, in the order the commentary gives them. For each line it records every place the line is quoted. Other quotations (Bodhicaryāvatāra, Suhṛllekha, Kadam sayings, and so on) are kept apart as quotations, not root.
- Two twentieth-century commentaries on OpenPecha (P000209, P000200) are used only to check that a headword's wording matches. None of their own commentary is quoted or extracted, because their licence is not stated in the repository metadata.
- The order and wording of the root differ between recensions. Every difference is recorded in RECONCILE_QUEUE-style notes on the source, never settled by choosing one.
- The Eight Verses (Langri Thangpa, 11th c.) come from Chekawa's own narrative commentary (P000222, 12th c.). Both works are public domain; the e-text is openly distributed on GitHub.

## 2026-09-29 17:18 IST — Gītā ch10-12 merger (M) decisions (reported by the merger; recorded by the orchestrator)
- **Sentence entries** under the split-verse rule: 10.4-5, 12.3-4, 12.6-7, 12.13-14, 12.18-19. These ids equal skeleton ids, which are upgraded. No span for 10.12-13 (10.12 has its own main clause), 11.9-11, 11.26-27 or 11.41-42 (narration or a request). Those verses carry "[continuing X]" markers instead.
- **Id harmonisation.** One way to write each id, kept consistent with ch07-09:
  - practices: prc:smarana for fixing manas/buddhi on the Lord; prc:abhyasa; prc:kirtana for 10.9 "speaking of me to one another"; prc:vibhuti-cintana; prc:avyakta-upasana;
  - terms: trm:vac, not trm:vak; trm:ahankara for nirahaṅkāra; trm:ananya-bhakti for ananyatā;
  - concept: cpt:qualities-of-the-devotee.
- **Homonyms deliberately not linked:**
  - trm:nimitta (the Pali meditation sign); 11.33 uses trm:nimitta-matra;
  - trm:nidhana (the closing part of a sāman chant), at 11.18 and 11.38;
  - cpt:real-and-unreal at 11.37;
  - tch:rama at 10.31 (the verse gives only "Rāma"; tch:parasurama also exists).
- **Dispute.** dsp:bhagavad-gita-lord-or-unmanifest (12.1–5) absorbs B's dsp:bhagavad-gita-manifest-or-unmanifest-worship and the undefined dsp:saguna-nirguna at those verses. Its two sides, Śaṅkara and Rāmānuja, are marked recalled with low confidence; check them against the bhāṣyas in Wave 2.
- **Tags.** A means and its result is tagged conventional. Portraits of the devotee and descriptions of the Lord are unmarked. Vision verses take path devotion; 11.48 and 11.53 take ritual. 12.2 is advanced, with stage_native yuktatama (parallel 6.47).
- **For the Gītā-wide consistency pass:**
  - ch01-03 did not link dsp:violence-and-svadharma at 2.18–38, although that dispute cites those verses;
  - dedupe prc:vandana ≈ prc:namaskara;
  - decide whether "fixing manas and buddhi on the Lord" is its own practice or part of prc:smarana.
- **Errata for the post-ch18 correction pass:**
  - misspellings: 10.1 and 10.18 śrṛ-; 10.14 vyakitaṃ; 10.29 stray nukta; 10.41 tejoṃ'śa-; 11.6 and 11.22 aśivanau; 11.51 tavasaumyaṃ; 11.54 dṛṣṭuṃ; 12.17 and 12.19 bhakitamān;
  - layout: 12.1 and 12.2 headings fused to the verse; ch12 segments lack line breaks; lines broken inside sandhi at 11.15, 11.17, 11.19, 11.29, 11.30, 11.38, 11.46 and 11.48.

## 2026-09-29 17:27 IST — U45 (Nyingma, Dzogchen, Bön) decisions (reported by the unit; recorded by the orchestrator)
- **Bön family.** lin:bon, lin:zhang-zhung-nyengyu and lin:bon-sar take family "shared" and are marked optional. Bön is neither Vedic nor an Indian śramaṇa tradition; it is kept because the brief allows it as optional.
- **Homonym ids.**
  - trm:mahayoga-nyingma and trm:anuyoga-nyingma stay separate from the haṭha trm:mahayoga and the Jain trm:anuyoga.
  - tch:samantabhadra-adibuddha (the primordial buddha) stays separate from tch:samantabhadra (the bodhisattva).
- **Recent flags.** Getse Paṇḍita and Jigme Gyalwai Nyugu are flagged recent. Jigme Trinle Özer (1745–1821) and Jigme Lingpa (1730–1798) are not.
- **No bands for doxographies.** pth:nyingma-nine-vehicles and pth:bon-nine-ways get no B0–B8 bands. They rank vehicles; they are not stages of one person's path.
- **Reconcile queue.** The queued disputes dsp:authenticity-of-nyingma-tantras, dsp:authenticity-of-terma and dsp:bon-and-buddhism reach RECONCILE_QUEUE.md through the merge, which regenerates it. The unit's labels RQ-U45-1, -2 and -3 are not used.
- **Corrections found in the local Derge texts.**
  - Kunjed Gyalpo has 84 chapters, and its ch. 31 is the Cuckoo of Awareness.
  - The Dupa Do has 75 chapters.
  - The Guhyagarbha has 22 chapters, and its "e ma'o" stanza is in ch. 2.

## 2026-09-29 17:30 IST — U43 (Pure Land) and U44 (Indian Vajrayāna) decisions (reported by the units; recorded by the orchestrator)
- **U43 new sub-lineages.** These are accepted as unit-owned ids; no registry change is needed, because the registry lists only mandatory ids:
  - lin:ji-shu, lin:yuzu-nenbutsu-shu;
  - lin:jodo-shu-chinzei, lin:jodo-shu-seizan (both point to ult:jodo-shu);
  - lin:shinshu-honganji-ha, lin:shinshu-otani-ha, lin:shinshu-takada-ha (all point to ult:jodo-shinshu);
  - lin:bailian-zong.
- **U43 corrections from the local texts.**
  - The Sanskrit Larger Sukhāvatīvyūha has 47 vows; the Chinese 18th vow corresponds to Sanskrit vow 19.
  - The Smaller Sūtra §10 has manasikariṣyati, where Kumārajīva has 執持名號.
  - Nāgārjuna's verse reads 無量力威德.
  - The Gaoseng zhuan records the vow of 123 people in 402 without the names "White Lotus Society" or "eighteen worthies"; those are later.
  - The "four alternatives" ascribed to Yanshou were not found in T2017.
  - In the Xu gaoseng zhuan it is a questioner who leaps from the willow; in the later Fozu tongji it is Shandao.
- **U43 restricted practice.** prc:shashen-wangsheng (abandoning the body for birth) is recorded as narrative summary only. The unit found no later teacher's warning to attach; the Phase C sweep should look for one.
- **U44 sub-lineages.** lin:arya-guhyasamaja, lin:jnanapada-guhyasamaja, lin:cakrasamvara and lin:kalacakra are created, each with its own ult view. lin:kalacakra covers the Indian phase; U48 and U47 may reference it for the Tibetan phase.
- **U44 homonyms.**
  - tch:aryadeva-tantric and tch:candrakirti-tantric are separate from the Madhyamaka masters.
  - tch:nagarjuna-siddha (from U30) serves as the tantric Nāgārjuna.
  - The tradition's identification of each with the Madhyamaka master is recorded in notes, not merged.
- **U44 84-siddha list.** It is based on Tōh 2292, the siddhas' realization songs (src:caturasiti-siddha-bodhihrdaya), because Abhayadatta's lives are not in the Derge Tengyur. src:caturasiti-siddha-pravrtti is kept for the lives, which are from memory with low confidence.
- **U44 Tibetan-based paraphrases.** These carry ai_translated and a translation_basis note. Wylie originals are sliced to the verse lines of the sense unit.
- **CBETA completed.** All of Taishō 1–55 plus 85 and the selected Xuzangjing volumes are now local (825 MB), which makes several "not local" items in the U42 and U43 reports checkable: Shandao T1753, Ouyi T1762, Tanluan T1819, Jingying Huiyuan T1749, Wonhyo T1747, T1856 and T52. Taishō 56–84 (Japanese texts) are not distributed by CBETA.

## 2026-09-29 17:42 IST — U46 (Kagyu) decisions (reported by the unit; recorded by the orchestrator)
- **Kagyu schools as separate roots.** Every Kagyu school points directly to the lin:kagyu umbrella, so each counts as its own root for convergence; lin:kagyu is a classificatory umbrella. Descent from Phagmodrupa is recorded in transmissions_received. The Shangpa sits under lin:kagyu by name only, with a note.
- **Shared Tengyur texts.** Six hearing-lineage texts were created by U46: Tōh 2304, 2305, 2331, 2332, 2337 and 2338. U44 references Tōh 2303 and 2330. If a later unit creates the same Tōh number under another id, remap it in config/id_remap.json.
- **Mahāmudrā ids.** prc:mahamudra-meditation (Kagyu) stays separate from the haṭha prc:mahamudra. trm:mahamudra carries both senses, with the homonym noted.
- **Political recognition.** The contested recognition of the 17th Karmapa is recorded as metadata on both teacher entries, not as a doctrinal dispute.
- **Guessed ids.** src:discrimination-of-the-three-vows and tch:drogmi are to be remapped if U47 uses other ids; check this when U47 finishes.

## 2026-09-29 17:44 IST — Convergence: branches of one transmission count once (revises the U46 note above)
- The data model counts "distinct independent lineage roots", where sub-lineages of one root count once. lin:chan (with lin:seon and lin:zen beneath it), lin:pure-land and lin:kagyu had been in the UMBRELLAS set, so each of their branches counted as its own root: Linji, Caodong, Rinzai and Sōtō, or Karma, Drikung and Drukpa Kagyu. That inflates convergence, because these branches are one transmission and not independent witnesses.
- Conservative fix in scripts/merge.py:
  - The three are removed from UMBRELLAS, so their branches collapse into lin:chan, lin:pure-land and lin:kagyu.
  - UMBRELLAS keeps only classificatory groupings that are not transmissions (Vedānta, Mahāyāna, Śramaṇa, the tantra movement, Sant, and so on).
  - A new OWN_ROOTS set lists lineages filed under a family name but separately transmitted. It holds only lin:shangpa-kagyu (Khyungpo Naljor from Niguma and Sukhasiddhi, not from Marpa).
- The U46 note "each Kagyu school counts as its own root" is superseded; the shards are unchanged.
- Remaps for U46's guessed ids (config/id_remap.json): tch:drogmi → tch:drokmi-lotsawa; src:discrimination-of-the-three-vows → src:domsum-rabye, with its two teachings → tea:domsum-rabye:ch.3 and :ch.3/2.

## 2026-09-29 17:44 IST — U47 (Sakya, Kadam, Gelug) decisions (reported by the unit; recorded by the orchestrator)
- **New sub-lineages** (real named divisions): lin:ngor, lin:tshar, lin:dzongpa, lin:kadam-shungpa, lin:kadam-lamrimpa, lin:kadam-mengakpa, lin:ganden-oral-lineage.
- **Wylie-slug source ids.** U47 reuses U41's Wylie ids (src:legs-bshad-snying-po, src:tshad-ma-rigs-gter, src:yid-dang-kun-gzhi, src:rnam-grel-thar-lam-gsal-byed, src:bsdus-grwa) instead of creating phonetic duplicates. The house style (Wylie or phonetic) is left for S5.
- **Seven Points.** "Fifty-nine slogans" is the later (Kongtrul-era) arrangement. The skeleton's tea:seven-point-mind-training:P.S refs follow it and say so. The Phase D lojong unit reconstructs the root from the classical commentary's lemmata (see the lojong entry above) and maps each line to these ids.
- **Sakya Paṇḍita's Mahāmudrā critique** is recorded as his claim about "present-day" teaching given without empowerment, not as a description of Kagyu teaching.
- **Queued disputes** (dsp:object-of-negation-madhyamaka, dsp:eight-difficult-points, dsp:reality-of-universals-tibetan) reach RECONCILE_QUEUE.md through the merge. The unit's labels RQ-U47-n are not used.
- **Duplicates for S5:** cpt:signs-of-dissolution vs cpt:dissolution-stages; the four-thoughts ids; obs:eight-worldly-concerns (U40, U45, U47); trm:kunzhi (Lamdre vs Nyingma senses).

## 2026-09-29 17:44 IST — U04 hallucination sweep: generator-default editions
- The same fabricated default found in U03 appears in U04: all 95 Muktikā sources carried one Adyar edition string. That string wrongly attached Brahmayogin's commentary to Schrader's 1912 critical edition. The sweep corrected each source to the Adyar volume for its own group, with Schrader 1912 added separately for the 16 texts in his volume.
- Overlong verse ranges were also corrected to where the content is found: Sarasvatīrahasya, Pañcabrahma, Sītā, Kṛṣṇa, Sarvasāra, Haṃsa and Mahāvākya.
- Sweeps of later units keep the explicit instruction to look for generator defaults.

## 2026-09-29 17:51 IST — U48 (Jonang, Chöd, Shije, Sowa Rigpa, Rimé) decisions (reported by the unit; recorded by the orchestrator)
- **Sowa Rigpa family.** lin:sowa-rigpa takes family "shared": Buddhist in frame, largely Āyurvedic in content, and also used by Bön physicians. Its sub-lineages are lin:jangpa-medicine and lin:zurkharpa-medicine.
- **Restricted content.** Mercury processing (btso thal), bloodletting and moxibustion, the Chöd body offering and haunted-place practice are recorded as summary plus the tradition's warnings only.
- **Homonym.** Bloodletting is trm:targa, kept apart from Sanskrit trm:tarka (reasoning).
- **Butön's lineage.** tch:buton is filed under lin:sakya and lin:kalacakra, because no Zhalu lineage exists.
- **Opponents known only from the tradition.** In dsp:chod-orthodoxy the unnamed critics' side has lineage null, a party description and reported_by_opponent true; they are known only from the Chöd tradition's own narratives.
- **Corrections to the brief.**
  - Machig's root text (bka' tshoms chen mo) is distinct from the Great or Complete Explanation (phung po gzan skyur ba'i rnam bshad).
  - Shākya Chokden was Sakya, not Jonang.
  - Chöd is not institutionally a branch of Shije.
  - The Four Tantras have 6 + 31 + 92 + 27 = 156 chapters.

## 2026-09-29 18:01 IST — Gītā ch. 13: skeleton citations shifted to this edition's numbering (fix in scripts/merge.py)
- **The problem.** The ch13-15 merger found that skeleton units cite ch. 13 in the 700-verse numbering: U05 says so in its note on 13.1-2, and U13 cites Śaṅkara's commentary, which comments on 700 verses. The text layer follows this edition, whose extra opening verse 13.1 makes 13.N(vulgate) = 13.N+1. Seven skeleton ids (13.12, 13.18, 13.21, 13.22, 13.23, 13.26, 13.34) would otherwise have merged into different verses, and the ranges would have pointed one verse off.
- **The fix.** For shards of phase skeleton only, the merge rewrites every id tea:bhagavad-gita:13.N[-M][/k] to 13.N+1[-M+1][/k]. It also shifts the location of the skeleton's own ch. 13 teachings, with a numbering_note. Extraction shards already use this edition's numbering and are untouched.
  - Skeleton decisions use the merger's skeleton_id_edition field, falling back to the shifted id.
  - Sourcing checks on skeleton entries are shifted the same way.
  - Sourcing corrections are looked up by the id as written in the shard.
- **Known risk.** A skeleton citation that already used this edition's numbering would now be off by one. None was found: only U05 and U13 cite ch. 13, and both use the 700-verse numbering. Future skeleton and synthesis work must cite ch. 13 in this edition's numbering; synthesis shards are not shifted.

## 2026-09-29 18:01 IST — Gītā ch13-15 merger (M) decisions (reported by the merger; recorded by the orchestrator)
- **Sentence entries.** 13.6-7 and 13.8-12 are kept: each first verse lacks a verb and the last gives the definition. B's 14.22-25 is not kept, because 14.22 has its own finite verbs; 14.23-25 is written instead. There is no span for 13.4-5 or 15.3-4.
- **Disputes.**
  - dsp:bhagavad-gita-ksetrajna-and-the-lord (13.3, 13.23), dsp:bhagavad-gita-jiva-as-amsa (15.7) and dsp:bhagavad-gita-aksara-purusa (15.16-18) are kept, each at low confidence with every side marked recalled; check them against the bhāṣyas in Wave 2.
  - Links to the registry ids dsp:souls-one-or-distinct and dsp:saguna-nirguna are mapped to these three disputes.
  - Loci passed to U50: souls-one-or-distinct at 13.3, 13.23 and 15.7; saguna-nirguna at 13.15, 14.27 and 15.16-18.
- **Id harmonisation.**
  - cpt:samatva → cpt:equanimity; cpt:ksara-aksara-purusottama → cpt:three-purusas; cpt:jiva-as-amsa → cpt:jiva-as-part-of-brahman.
  - prc:avyabhicarini-bhakti → prc:ananya-bhakti; prc:prapatti → prc:saranagati.
  - trm:mahad-brahma → trm:mahat.
  - Compound terms folded into their base terms: trm:samatva, trm:ahankara, trm:acarya, trm:sanga, trm:parama-dhama.
- **Homonyms not linked:** trm:mahesvara (māheśvara), trm:asakti (aśakti), trm:dvara (the Pāśupata term), cpt:nine-gated-city at 14.11, and cpt:real-and-unreal at 13.13. Term links were dropped wherever the word is not in the verse.
- **Tags.** Descriptions are unmarked. A means and its result, and the list 13.8-12, are tagged "all". 14.21-25 is realized, with stage_native guṇātīta. 14.2 is realized. 13.26 is beginner.
- **For S5.**
  - Dedupes: trm:ahamkara ≈ trm:ahankara (U05 uses ahamkara); obs:manitva vs obs:mana, obs:mana-pride and obs:abhimana.
  - Rename data/ cpt:liberation (currently "Liberation (mokṣa) in later Mīmāṃsā") to "Liberation (mokṣa)", keeping the Mīmāṃsā sense as one definition among others.
- **Errata for the post-ch18 pass.**
  - Misspellings: śrṛṇu (13.4), viniśicataiḥ (13.5), asakitar (13.10), bhakitar (13.11), liṃgais (14.21), bhakitayogena (14.26), parimārgitavya (15.4, missing its anusvāra).
  - Layout: speaker headings fused at 13.2, 14.1, 14.21, 14.22 and 15.1; no line breaks in 13.2–15.20; words split across the pāda break at 15.3 and 15.5.
