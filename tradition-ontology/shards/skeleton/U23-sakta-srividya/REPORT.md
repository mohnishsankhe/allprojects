# U23-sakta-srividya — Phase B skeleton REPORT
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Counts:** 63 sources · 47 teachers · 157 teachings · 136 terms · 74 concepts · 34 practices · 11 obstacles · 14 phenomenology items · 5 path maps · 6 disputes · 6 borrowings · 4 lineages · 4 ultimate views · 31 interpretation_log lines.
**Validator:** 0 errors (the only warning is that REPORT.md is missing). Generators are `_gen/part1…part10`; `_gen/check_refs.py` confirms that every referenced id exists in this shard, in another skeleton shard or in the registry.
**How the entries were checked:** Every entry is at level `skeleton`. Where I saw the wording or the reference in a local e-text (read-only), I set confidence to high and said so in `notes`. The texts used:
- Lalitā Sahasranāma (LSN): the stotra (peterFreund), and with the Saubhāgyabhāskara (eBhāratī, Nirṇayasāgara 1935).
- Saundaryalaharī (SL): the GRETIL text of Brown's edition (HOS 43), and with Lakṣmīdhara's commentary (Muktabodha M00672).
- Yoginīhṛdaya (YH) with the Dīpikā (M00115); Setubandha (M00052).
- Kāmakalāvilāsa (KKV) with the Cidvallī (M00025); Varivasyārahasya (VR) with the Prakāśa (M00098).
- Paraśurāma Kalpasūtra (PKS): GRETIL text of GOS 22.
- Tantrarāja with the Manoramā (M00122); Jñānārṇava Tantra (M00069); Śrīvidyārṇava (M00217).
- Tripurā and Bahvṛca Upaniṣads (raw_etexts shAktA); Bhāvanā Upaniṣad (eBhāratī); Kaula Upaniṣad with Bhāskararāya (M00028).

## 1. Coverage checklist (A8 plus section D for lin:sakta and lin:srividya)
**Lineages.**
- `lin:sakta` (umbrella) and `lin:srividya` are the two lineages this unit owns.
- I added two sub-lineages: `lin:samaya-srividya` (Lakṣmīdhara's school) and `lin:kaula-srividya` (the Vāmakeśvara–Yoginīhṛdaya line). "Kaula Śrīvidyā" is a descriptive label I chose for grouping.

**Ultimate views.** `ult:sakta` and `ult:srividya`, plus `ult:samaya-srividya` and `ult:kaula-srividya`.

**Goddess texts.**
- Devī Māhātmya: U07 owns the text. I added its recited limbs (`src:devi-kavaca`, `src:argala-stotra`, `src:kilaka-stotra`, `src:pradhanika-rahasya`, `src:vaikrtika-rahasya`, `src:murti-rahasya`) and the related `prc:saptasati-parayana`, `prc:navaratri-vrata`, `prc:kumari-puja` and `cpt:navadurga`.
- Devī Bhāgavata and Devī Gītā: U07 and U06 own them. They are referenced in `dsp:external-or-internal-worship`, `trm:manidvipa` and `trm:kumari`.
- Lalitā Sahasranāma: `src:lalita-sahasranama` with 33 teachings, including the Brahmāṇḍa / Hayagrīva–Agastya frame and its structure. Commentary `src:saubhagyabhaskara` has 8 teachings.
- Lalitā Triśatī: `src:lalita-trisati` and `src:lalita-trisati-bhasya` (ascribed to Śaṅkara; ascription doubtful).
- Saundaryalaharī: `src:saundarya-lahari` with 26 teachings; the Ānandalaharī is verses 1–41; the attribution to Śaṅkara is recorded as the tradition's account and as disputed by scholars. Commentaries: `src:laksmidhara` (7 teachings), `src:saubhagyavardhini` (Kaivalyāśrama) and `src:arunamodini`.

**Śrīvidyā texts.**
- Root tantras and commentaries: `src:vamakesvara-tantra` (= Nityāṣoḍaśikārṇava / Vāmakeśvarīmata), `src:setubandha`, `src:vamakesvarimata-vivarana` (Jayaratha), `src:rjuvimarsini`, `src:artharatnavali`, `src:yoginihrdaya` and `src:yoginihrdaya-dipika` (Amṛtānanda).
- Tantrarāja: `src:tantraraja-tantra` and `src:manorama-tantraraja`.
- Treatises: `src:kamakalavilasa` with `src:cidvalli`, and `src:varivasya-rahasya`.
- Ritual code: `src:parasurama-kalpasutra` (21 teachings), `src:nityotsava`, `src:saubhagyodaya-ramesvara`.
- Śākta Upaniṣads: U04 owns the ids `src:tripura-upanisad`, `src:tripuratapani-upanisad`, `src:bhavana-upanisad`, `src:bahvrca-upanisad` and `src:kaula-upanisad`. I added new teachings on them and three Bhāskararāya commentaries (`src:*-bhasya-bhaskararaya`).
- Compendia and other tantras: `src:srividyarnava-tantra` and `src:jnanarnava-tantra` (the Śākta tantra, kept separate from the Jain `src:jnanarnava`).
- Also added: `src:subhagodaya`, `src:srividyaratnasutra`, `src:lalita-stavaratna`, `src:pancastavi`, `src:laghustava`, `src:muka-pancasati`, `src:abhirami-antati`, `src:kamalamba-navavarana-krtis`, and the five lost Śubhāgama saṃhitās (`src:*-samhita-subhagama`).

**Teachers.**
- New: `tch:bhaskararaya` (full entry), `tch:nrsimhanandanatha`, `tch:punyananda`, `tch:amrtananda`, `tch:umanandanatha`, `tch:natanananda`, `tch:lolla-laksmidhara`, `tch:subhagananda`, `tch:prakasananda-desika`, `tch:parasurama`, `tch:vagdevatas`.
- The twelve upāsakas are in `cpt:twelve-upasakas`, with teacher entries or contributions for Manmatha, Lopāmudrā, Agastya, Indra, Skanda, Śiva and Durvāsas (= Krodhabhaṭṭāraka).
- `tch:hayagriva` and `tch:agastya` got U23 contributions.
- Śaṅkara's link to Śṛṅgeri and Kāñcī is recorded as the tradition's account in the `tch:sankara` contribution and in `tch:gaudapada`.

**Concepts from the brief.**
- Śrī Yantra: `cpt:sri-yantra`, `trm:sricakra`.
- Nine enclosures: `cpt:nine-avaranas`, `pth:sricakra-navavarana`, `trm:avarana`, `trm:cakresvari`, `trm:yogini`.
- Fifteen- and sixteen-syllable mantras, summary only: `cpt:srividya-mantra-structure`, `cpt:three-kutas`, `cpt:kadi-hadi-matas`, `trm:pancadasi`, `trm:sodasi`, `trm:hrllekha`.
- Kāmakalā: `cpt:kamakala`.
- The three cities: `cpt:tripura-triads`, `cpt:three-bodies`.
- Inner worship and the Bhāvanā Upaniṣad: `prc:antaryaga`, `prc:bhavana-sricakra-deha`, `cpt:body-as-sricakra`.
- Samaya and Kaula modes (right- and left-hand): `cpt:samaya-and-kaula-modes`, `cpt:purva-uttara-kaula`, `cpt:fivefold-equality`, `dsp:samaya-or-kaula`.
- Śakti as consciousness-power: `cpt:sakti-as-consciousness-power`.
- Lalitā as Brahman: `cpt:lalita-as-brahman`.
- Gentle and fierce forms: `cpt:gentle-and-fierce-forms`.
- Kuṇḍalinī: a contribution to `cpt:kundalini`, plus `pth:lalita-kundalini-ascent`, `prc:lalita-kundalini-dhyana` and `prc:samaya-kundalini-puja`.
- Māyā as Śakti: `cpt:maya-as-sakti` and `dsp:maya-sakti-or-avidya`.
- The yoni as sacred: `trm:yoni` (Śrīvidyā sense only; Kāmākhyā and menstruation rites belong to U24).

**Other entities.**
- Practices: 34 in all. Main ones are `prc:sricakra-navavarana-puja`, `prc:srividya-diksa`, `prc:srividya-japa`, `prc:srividya-nyasa`, `prc:catuhsasti-upacara` and `prc:lalita-sahasranama-parayana`.
- Path maps: `pth:srividya-krama-diksa`, `pth:sricakra-navavarana`, `pth:yoginihrdaya-three-pujas`, `pth:lalita-kundalini-ascent`, `pth:rudrayamala-births-to-srividya`.
- Disputes: `dsp:samaya-or-kaula`, `dsp:siva-sakti-primacy`, `dsp:external-or-internal-worship`, `dsp:vedic-status-of-tantra` (queued), `dsp:pancamakara-literal-or-substitute`, `dsp:maya-sakti-or-avidya`.
- Borrowings: `brw:kaula-to-srividya`, `brw:mimamsa-to-srividya`, `brw:upanisadic-to-sakta`, `brw:sakta-hatha-kundalini`, `brw:samkhya-to-sakta`, `brw:srividya-to-karnatic-music`.

**Section D checklist.**
- States of consciousness: `cpt:four-states-and-turya`, `cpt:turiya-turiyatita`, `trm:saksin`.
- Self: `trm:jiva`, `trm:aham`, `trm:svavimarsa`.
- Mind: `cpt:lalita-four-weapons`.
- Body and energy: `cpt:body-as-sricakra`, `cpt:nadis`, `cpt:ten-vayus`, `cpt:ten-fires-bhavana`, `cpt:cakras`, `cpt:three-granthis`, `cpt:four-pithas-srividya`, `cpt:thirty-six-tattvas`.
- Obstacles: 11 `obs:*` entries.
- Ethics: `cpt:srividya-conduct`.
- Karma and liberation: `cpt:jivanmukti`, `cpt:five-kinds-of-mukti`, `cpt:bhukti-and-mukti`.
- Powers and their warnings: `cpt:siddhis-in-srividya` and the 14 `phn:*` entries.
- Teacher, lineage and transmission: `cpt:three-diksas`, `cpt:three-oghas`, `cpt:srividya-teacher-disciple`, `cpt:srividya-secrecy`, `cpt:amnayas-srividya`.
- Cosmology and time: `cpt:manidvipa-srinagara`, `cpt:fifteen-nityas`, `cpt:nityas-as-time`, `cpt:five-acts-of-the-goddess`, `cpt:srividya-cosmogony`.
- Sound and language: `cpt:six-meanings-of-mantra`, `cpt:fifteen-meanings-of-pancadasi`, `cpt:nada-kalas-of-uccarana`, `cpt:eight-vagdevatas`, `cpt:levels-of-speech`.
- Death and dying: `cpt:death-in-srividya`.

**Corrections to the brief's MUST-COVER list.**
1. The Nityotsava is Umānandanātha's manual (paddhati) expanding the Paraśurāma Kalpasūtra, not a commentary on it. The commentary is Rāmeśvara's Saubhāgyodaya, usually dated 1831, so it is flagged as recent.
2. Bhāskararāya's Setubandha covers the whole Vāmakeśvara, which he treats as two "four-hundreds" (catuḥśatī): the prior one is the Nityāṣoḍaśikārṇava (5 paṭalas) and the latter is the Yoginīhṛdaya (3 paṭalas). So `src:yoginihrdaya` has `part_of: src:vamakesvara-tantra`. I also added Jayaratha's Vivaraṇa.
3. Brown's edition of the Saundaryalaharī has 103 verses (100 plus 3 appended).
4. Naṭanānanda's commentary on the Kāmakalāvilāsa is called the Cidvallī.
5. The Tantrarāja calls itself the "Kādimata" and has 36 paṭalas. The Manoramā commentary covers paṭalas 1–22 by Subhagānandanātha and 23–36 by his disciple Prakāśānanda Deśika.
6. The list of twelve upāsakas is confirmed as Bhāskararāya quotes it; he refers their twelve vidyās to the Jñānārṇava.
7. The Bahvṛca Upaniṣad (3) also names a Sādi vidyā besides the Kādi and Hādi forms.
8. Bhāskararāya calls the Subhagodaya commentator "Lalla", which supports the name "Lolla Lakṣmīdhara".
9. Bhāskararāya counts the Lalitā Sahasranāma as 51 introductory verses, 182½ verses of names and a closing section: 320 verses in all. By tradition the eight goddesses of speech (Vāgdevatās) composed it.

## 2. Least sure (possible hallucinations — check these first)
**Concept details from memory.**
- The names in `cpt:nine-avaranas`: the cakra names, presiding goddesses and yoginī classes.
- The names of the ten mudrās in `cpt:ten-mudras-srividya`.
- The order and names in `cpt:fifteen-nityas`.
- The full list of the eight bonds in `obs:eight-pasas`. Only "beginning with disgust" was seen in the text.
- `cpt:three-oghas` (the divine, perfected and human streams of gurus).

**Dates and people.**
- Lakṣmīdhara at the court of Pratāparudra Gajapati.
- Bhāskararāya's dates and places.
- The Nityotsava as 1745 and the Saubhāgyodaya as 1831.
- The dates of Puṇyānanda, Amṛtānanda and the Tantrarāja.
- `tch:amritananda-natha-sarasvati` (Devīpuram); the Abhirāmi Paṭṭar legend.

**Low-confidence sources.**
- Authorship or existence: `src:arunamodini` (Kāmeśvarasūri), `src:saubhagyavardhini`, `src:srividyaratnasutra`, `src:sakti-mahimna-stotra`, `src:saubhagyasudhodaya`, `src:gandharva-tantra`, `src:tripurarnava-tantra`, `src:bhaskaravilasa` (said to be by his disciple Jagannātha), `src:syamala-dandaka` (ascription to Kālidāsa), `src:daksinamurti-samhita`, the author of `src:saubhagyaratnakara`.
- Edition details for `src:rjuvimarsini` and `src:artharatnavali`.
- Content of `src:kilaka-stotra`, `src:vaikrtika-rahasya` and `src:murti-rahasya`.

**Low-confidence teachings.**
- `tea:pradhanika-rahasya:1-12` (verse range and details).
- `tea:tantraraja-tantra:1.5` and `tea:tantraraja-tantra:nityas-and-time`.
- `tea:vamakesvara-tantra:4.12-16`: only partly seen, through a quotation in the Dīpikā.
- `tea:vamakesvara-tantra:sricakra` and `tea:vamakesvara-tantra:nityas`: summaries at chapter level.
- `tea:lalita-sahasranama:uttarabhaga`, `tea:lalita-trisati:secrecy`, `tea:tripura-upanisad:10`.

**Interpretive choices.**
- All B-bands on the path maps, especially `pth:sricakra-navavarana` (confidence low).
- Reading the Yoginīhṛdaya's three worships in the order aparā → parāparā → parā.

**Tradition accounts not tied to a checked text.** Śaṅkara installing Śrīcakras at Śṛṅgeri, Kāñcī and Tiruvāṉaikkā; Muttusvāmi Dīkṣitar's initiation (left out).

## 3. Gaps (belong here, not created responsibly)
**Enclosure deities and guru lineage.**
- The attendant deities of each enclosure are not listed by name (the 16 attractions, the 8 Anaṅga goddesses, and so on).
- The names of the gurus in the three streams are not recorded.
- South Indian Śrīvidyā lineages are missing: the maṭha lines, Guhānanda Maṇḍalī, Cidānandanātha. Karapātrī's Śrīvidyā works and Agastya's "Śakti Sūtras" were left out as uncertain.

**Local e-texts not yet extracted.**
- Śrīvidyārṇava (Śaṅkara line, āmnāya scheme), Jñānārṇava (the twelve vidyās), Dakṣiṇāmūrti Saṃhitā.
- Tripurā Rahasya Māhātmya-khaṇḍa (U13 owns the Jñāna-khaṇḍa).
- Pañcastavī and Laghustuti with its commentary.
- Nityotsava, Tripurāsārasamuccaya, Saubhāgyaratnākara.
- The Kaula Upaniṣad beyond the sūtras used here.
- Bhāskararāya's prayoga for the Bhāvanā Upaniṣad.
- The Guptavatī (U07).

**Missing debates.** Kādi versus Hādi superiority; authorship of the Saundaryalaharī; controversies over who may recite the Lalitā Sahasranāma. Women's and caste eligibility belongs to `dsp:women-caste-liberation` (U50). Lakṣmīdhara's eligibility-by-class and PKS 10.82 are relevant inputs to it.

**Śākta Upaniṣads.** Sītā, Annapūrṇā, Sarasvatīrahasya and Saubhāgyalakṣmī have no U23 teachings.

**Regional and later traditions.** Tamil, Kannada, Telugu and Bengali Śākta works beyond the Abhirāmi Antāti; Nepalese Śrīvidyā; Śrīvidyā temples (Kāmākṣī of Kāñcī, Śāradā of Śṛṅgeri, Kamalāmbā of Tiruvārūr, Devīpuram).

**Guru and disciple.** How a guru and disciple are tested in Śrīvidyā manuals, beyond PKS 1.14–25.

## 4. Out of reach
- Mantra syllables, pādukā-mantras, the content of the three-stream guru lists, and full-consecration rites are taught orally under initiation. They are deliberately not reproduced.
- Restricted items are summarised only, with the texts' warnings: `prc:pancamakara`, `prc:rahoyaga`, `cpt:pancamakara`, `trm:pancamakara`, `dsp:pancamakara-literal-or-substitute`. The guru's mahāvedha rite in `prc:samaya-kundalini-puja` is summarised with no method.

## Cross-unit notes and decisions (for DECISIONS.md / RECONCILE_QUEUE.md)
- **Homonym clash on `tch:laksmidhara`.** U02 and U07 use it for the 12th-c. author of the Kṛtyakalpataru. U08 used it for the Saundaryalaharī commentator. U23 uses `tch:lolla-laksmidhara` for the commentator. The merge needs a dedupe.
- **Commentary id.** I reused U08's `src:laksmidhara` as the id of the Lakṣmīdharā commentary. Its authors will union to both teacher ids; the U08 author should be repointed.
- **Overlapping teaching ids on U04's Upaniṣads.** The new ids (e.g. `tea:tripura-upanisad:14`, `tea:bahvrca-upanisad:5`, `tea:bhavana-upanisad:sricakra-puja`) overlap U04's range teachings (`1-11`, `4-9`, `1-5`). The fidelity pass should decide whether to keep both levels.
- **Kādi and Hādi.** Treated as a concept, not as lineages.
- **Reconcile queue.** `dsp:vedic-status-of-tantra` is queued with candidate readings under P4, P7 and P5 (`queue_ref: RQ-U23-vedic-status-of-tantra`). Five disputes are partially reconciled, each with its tradition's objections recorded.
- **Flagged recent.** `tch:muttusvami-diksitar`, `tch:syama-sastri`, `tch:ramesvara-srividya`, `tch:bhairavi-brahmani`, `tch:amritananda-natha-sarasvati`, `tch:ramakrishna` (U23 contribution), `src:kamalamba-navavarana-krtis`, `src:saubhagyodaya-ramesvara`, `brw:srividya-to-karnatic-music`.
