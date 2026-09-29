# Phase C sourcing report — U02-brahmana-vedanga
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Checked 2026-09-28 to 2026-09-29.
- **Output:** `shards/sourcing/U02-brahmana-vedanga/checks.jsonl`. Drafts and scripts are in `_gen/`.
- **Validation:** `python3 scripts/validate_shard.py shards/sourcing/U02-brahmana-vedanga` gives 0 errors. The only warning is the missing REPORT.md, which is this file.

## 1. Numbers

| entity | entries | checked | confirmed | partially | corrected | not-found |
|---|---|---|---|---|---|---|
| lineages | 8 | 8 | 8 | 0 | 0 | 0 |
| sources | 164 | 164 | 156 | 7 | 1 | 0 |
| teachers | 89 | 89 | 85 | 4 | 0 | 0 |
| teachings | 288 | 288 | 279 | 4 | 5 | 0 |
| disputes | 11 | 11 | 10 | 1 | 0 | 0 |
| borrowings | 5 | 5 | 5 | 0 | 0 | 0 |
| concepts | 89 | 89 | 87 | 1 | 1 | 0 |
| phenomenology | 8 | 8 | 7 | 0 | 1 | 0 |
| practices | 47 | 47 | 39 | 0 | 8 | 0 |
| obstacles | 10 | 10 | 9 | 0 | 1 | 0 |
| paths | 2 | 2 | 2 | 0 | 0 | 0 |
| ultimate | 2 | 2 | 2 | 0 | 0 | 0 |
| terms | 157 | 0 | – | – | – | – |
| **total** | **880** | **723** | **689** | **17** | **17** | **0** |

**Methods (checks.jsonl `method` field):**
- text-locate: 488
- websearch: 86
- catalog: 62
- catalog+websearch: 42
- catalog+text-locate: 26
- text-locate+websearch: 18
- catalog+text-locate+websearch: 1

**Evidence:** 134 checks cite catalog hits and 200 cite web pages. Every `text:` path in `evidence` exists under `sources_raw/`.

**Local texts used:**
- GRETIL: Manu (Kullūka numbering, with Medhātithi numbers alongside), Yājñavalkya, Nārada, Parāśara, Viṣṇu, the four Dharmasūtras, Aṣṭādhyāyī, Mahābhāṣya, Nirukta, Kauṣītaki Br., Gopatha Br., Āśvalāyana GS and the other Gṛhyasūtras, Arthaśāstra, Kāmasūtra, Mādhyandina ŚB, Mitākṣarā.
- DCS: AB, Aitareya Āraṇyaka, JB, ṢB, TB, TS.
- raw_etexts: the Taittirīya corpus including the Āndhra TA, the Pāṇinīya Śikṣā, the Ṛgveda Prātiśākhya, and the accented ŚB kāṇḍa 12.
- eBhāratī: Kullūka, the Dāyabhāga, the Nirṇayasindhu, the Dharmasindhu.
- Prepared Upaniṣads; DharmicData MBh CE.

## 2. Not found (possible hallucinations)

None. Every checked entry was located in a text or confirmed by at least one external source. Where only part of a claim could be verified, the result is `partially-confirmed` (section 4).

## 3. Corrections (17)

A correction replaces the whole field. The tradition's own accounts were left untouched.

**Sources**
- **src:visnusmrti** — `dating`: scholarly 600–800 CE → c. 700–1000 CE, probably Kashmir (Olivelle; Wikipedia). Confidence moderate.

**Teachings** (`location.ref` only; the ids are unchanged)
- **tea:manusmrti:11.261** → 11.260. This is the Aghamarṣaṇa/aśvamedha verse; 11.261 is a different verse.
- **tea:satapatha-brahmana:10.5.2.20** → 10.5.2.19-20. The svāpyaya→svapna pun is at .19.
- **tea:satapatha-brahmana:14.1.1.1-10** → 14.1.1.1-25. The Dadhyañc/madhu part of the paraphrase is at .18–25.
- **tea:apastamba-dharmasutra:1.2.5.5-6** → 1.2.5.4-6.
- **tea:apastamba-dharmasutra:1.8.22.2-8** → 1.8.22.1-8.

**Concepts, phenomenology, obstacles**
- **cpt:paroksa** — `definitions`: the inline locator ŚB 10.5.2.20 → 10.5.2.19.
- **phn:sleep-breaths-enter-self** — `ref` 10.5.2.20 → 10.5.2.19-20.
- **obs:upapataka** — `sources` and the description's reference: MDh 11.60–67 → 11.59–66. The list begins at 11.59; 11.67 is the jātibhraṃśakara category.

**Practices** (`sources`, plus `method_summary` for Aghamarṣaṇa)
- **prc:aghamarsana** — MDh 11.261 → 11.260.
- **prc:kesanta** — MDh 2.65 and ĀśGS 1.18, replacing 2.26–35 and "1".
- **prc:samavartana** — MDh 3.1–4 and ĀśGS 3.8–9.
- **prc:niskramana** — MDh 2.34 and the Nirṇayasindhu 3. ĀśGS has no niṣkramaṇa.
- **prc:karnavedha** — the Nirṇayasindhu 3 ("ṣaṣṭhādimāse karṇavedhaḥ"; Vyāsa's sixteen) and the Dharmasindhu 3 §43.
- **prc:vidyarambha** — the Dharmasindhu 3 and Nirṇayasindhu 3 ("pañcame 'bde vidyārambhaḥ"), plus Arthaśāstra 1.5.7.
- **prc:udakakarma** — YS 3.1–2 → 3.1–5. The water-offering itself is at 3.3–5.
- **prc:sapindikarana** — YS "1 (śrāddha section)" → YS 1.253–255 and ViSmṛ 21.19–23.

## 4. Partially confirmed (17), with the reason

**Sources**
- **src:devatadhyaya-brahmana** — the "colours to the metres" detail is not verified; no local copy.
- **src:satyayana-brahmana** — the lost text is known from quotations, but no specific scholarly page was found.
- **src:siddhahemasabdanusasana** — the 1130–1150 bracket was not checked.
- **src:sankhalikhita-dharmasutra** — the metrical smṛtis exist; the lost prose Dharmasūtra was not verified.
- **src:manvarthamuktavali** — Kullūka's date is disputed: Wisdomlib gives the 12th c., other literature the 13th–15th c.
- **src:apararka-tika** — Aparāditya I reigned 1170–1197 per Wikipedia, against the entry's 1100–1150.
- **src:kamasutra** — the c. 3rd-c. CE date was not confirmed; searches give only a 1st–6th c. range.

**Teachers**
- **tch:vatsyayana-mallanaga** — same dating issue as src:kamasutra.
- **tch:kulluka** — same dating issue as src:manvarthamuktavali.
- **tch:apararka** — same dating issue as src:apararka-tika.
- **tch:haradatta** — Wikipedia dates the Padamañjarī to the 11th c., earlier than the entry's 12th–13th c.; the identity of the two Haradattas is debated.

**Teachings**
- **tea:taittiriya-brahmana:1.1.3.5-6**, **tea:taittiriya-brahmana:1.2.6.7**, **tea:taittiriya-brahmana:2.8.8.1** — the passages are located at anuvāka or prapāṭhaka level, but the local e-texts do not mark the kaṇḍikā or anuvāka numbers.
- **tea:vedanga-jyotisa:y.3** — the verse is genuine Vedāṅga Jyotiṣa but is not in the local Ārca text, and web sources number it differently.

**Dispute and concept**
- **dsp:vedic-ritual-killing-and-ahimsa** — the Jain side's Ācārāṅga 1.4 belongs to another unit and was not checked.
- **cpt:five-year-yuga** — the five year-names are not in the VJ. They are attested exactly in Bṛhatsaṃhitā 8.24, with a variant list in Brahmāṇḍa P. 1.13.

## 5. Findings for the skeleton REPORT and for later phases

**Skeleton gaps that can now be filled**
- *Signs-of-death passage.* It **is** at AA 3.2.4, contrary to gap 3 of the skeleton REPORT: "candramā ivādityo dṛśyate … lohinī dyaur bhavati …", followed by dreams and a pāyasa rite with the Rātrī sūkta (raw_etexts `vedaH/Rg/shakala/AraNyakam/3/2.md`, line 4).
- *Prāṇāgnihotra in the eating rules.* This is BDh 2.7.12.3 in GRETIL numbering (Bühler's 2.12): "prāṇe niviṣṭo 'mṛtaṃ juhomi … prāṇāya svāhā", filling gap 1.
- *Kena Upaniṣad.* It is JUB 4.18–21 (Wikipedia).
- *ŚB kāṇḍa 12.* It is available locally at raw_etexts `sb_gretil/12`, and ŚB 12.5.2 is confirmed.
- *Hārīta.* The brahmavādinī/sadyovadhū quotation is confirmed. It is quoted in the Smṛticandrikā's saṃskāra section (Wisdomlib's Medhātithi on MDh 2.66, notes; Wikipedia "Brahmavadini"). src:haritasmrti and cpt:stri-dharma are therefore confirmed.

**Least-sure locators from the skeleton REPORT (all resolved)**
- Confirmed: ŚB 12.5.2, ŚB 1.2.3.6–9, AB 5.33–34, TA 2.2, GB 1.1.16–30, JB 1.42–44, PB 17.1, Nirukta 2.16, MDh 1.61–63, 2.88–92, 5.83, 3.192–199, 3.267–272, ĀśGS 4.1–6, MaiU 6.9, and the Prāṇāgnihotra Upaniṣad.
- Corrected: ŚB 14.1.1.
- Partial: VJ y.3.

**Doubtful attributions**
- These are confirmed *as debated*, which is how the entries present them:
  - Piṅgala as Pāṇini's brother;
  - Vyāḍi and the Vikṛtivallī;
  - the Nandikeśvara-kāśikā;
  - Viśvarūpa = Sureśvara;
  - Mādhava = Vidyāraṇya;
  - the Kātyāyana identities.
- Haradatta is partial; see section 4.

**Disputes**
- **dsp:niyoga** — the commentarial reconciliation, flagged "from memory", is confirmed. Kullūka on MDh 9.68 quotes Bṛhaspati ("ukto niyogo muninā niṣiddhaḥ svayam eva tu | yugakramād aśakyo 'yaṃ …") and calls the prohibition "kaliyugaviṣayaḥ".
- **dsp:widow-anvarohana** — the low-confidence commentator locators are right.
  - Medhātithi on MDh 5.155 argues that anugamana is suicide (Wisdomlib; Wikipedia "Anumarana").
  - The Mitākṣarā on YS 1.86 has "anvārohaṇe mahān abhyudayaḥ".
- **dsp:inheritance-by-birth-or-death** — both sides are text-located.
  - Mitākṣarā: "janmanaiva svatvam" on YS 2.114ff; "ekaśarīrāvayavānvayena" on YS 1.52.
  - Dāyabhāga: uparama-svatva.
- **dsp:which-purusartha-is-foremost** — MBh CE 12.161 was found locally: Bhīma argues "tasmāt kāmo viśiṣyate" (12.161.28). It could be added as a text.

**Other notes**
- **tea:kausitaki-brahmana:7.6** — the passage is at KB 7.7 in both local editions. The content is confirmed and the id keeps the older citation.
- **The saṃskāra list.** The sixteen members of cpt:samskaras match the common later list (Wikipedia). Vyāsa's sixteen, quoted in the Nirṇayasindhu, differ: they have no vidyārambha or antyeṣṭi and add the taking of the domestic and śrauta fires. This bears out the entry's note that lists vary.
- **New non-registry lineage ids** (lin:arthasastra, lin:kamasastra, lin:nairukta, lin:aitihasika, lin:mitaksara-school, lin:dayabhaga-school) are all real, text-attested schools or groups. Their placement is for the orchestrator.

## 6. What could not be checked

- **Terms (157).** Not in the brief's categories, so not checked.
- **Interpretation layer.** The band assignments in the paths were not checked.
- **Ācārāṅga 1.4.** Another unit's text (dsp:vedic-ritual-killing-and-ahimsa, Jain side).
- **Kaṇḍikā or anuvāka numbers not marked in the local Taittirīya e-texts:** TB 1.1.3.5–6, 1.2.6.7, 2.8.8.1.
- **VJ Yājuṣa numbering:** y.3.
- **Dates left open:** Hemacandra's 1130–1150 bracket; the c. 3rd-c. CE date of the Kāmasūtra and Vātsyāyana; Kullūka; Aparārka; Haradatta; the Nandikeśvara-kāśikā.
- **Texts not read directly:**
  - Jinasena's Ādipurāṇa (parvans 38–40). brw:dharmasastra-samskaras-to-jain is confirmed from Wikipedia "Saṃskāra" and "Jinasena" only.
  - The Caraṇavyūha. cpt:upavedas is confirmed from Dharmawiki and Hindupedia.
  - Medhātithi's Mīmāṃsā usage (brw:mimamsa-to-dharmasastra-hermeneutics is confirmed from the Dāyabhāga and Mitākṣarā).
  - The lost prose Śaṅkha-Likhita and Śāṭyāyana texts.
  - The Devatādhyāya's "colours" detail.
- **Other unverified details:**
  - Oertel's JUB "4.10" numbering note.
  - cpt:preta-to-pitr: the claim that the most distant ancestor leaves the piṇḍa circle. The main doctrine is confirmed at YS 1.253–255 and ViSmṛ 21.19–23.
