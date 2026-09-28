# U05-gita-epic — Phase C hallucination sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Scope:** every source (98), teacher (102), lineage (2) and teaching verse ref (487) in `shards/skeleton/U05-gita-epic`. The "least sure" list in the unit's REPORT was checked first.

**Result: 689 checked · 683 confirmed · 5 partially confirmed · 1 corrected · 0 not found.** The validator reports 0 errors.

## How the checks were made
**Local texts (read-only):**
- BORI Critical Edition of the Mahābhārata (DharmicData JSON)
- gita/gita (verses, plus 13 Sanskrit commentaries)
- DharmicData southern-vulgate Rāmāyaṇa
- Gita Press Rāmāyaṇa and Baroda critical Rāmāyaṇa (raw_etexts)
- a vulgate Mahābhārata (sarit)
- GRETIL files: Śaṅkara's bhāṣya, Yāmuna's Gītārthasaṅgraha, the Nārāyaṇīya, the Harivaṃśa critical text, the Gītā with four commentaries
- eBhāratī files: the four-commentary Gītā, the Gītārthasaṅgraha with Deśika's Rakṣā, the Tātparyacandrikā
- Madhva's Gītā works and Jayatīrtha's Nyāyadīpikā
- Muktabodha's Sarvatobhadra
- the Aṣṭādhyāyī with the Kāśikā

**Also used:** `catalog.py` for existence checks, and WebSearch for authors, dates and inscriptions.

**Teachings (`text-locate`):**
- All 325 Gītā teachings were checked verse by verse against the local text (700-verse numbering, with the ch. 13 offset handled). Every ref exists and matches its paraphrase.
- All 162 other teachings were located: single verses read in the Critical Edition; chapter-level refs confirmed by chapter and keyword search.

## Partially confirmed or corrected
- **`tea:moksadharma:12.289`** (low confidence; partial). Confirmed in 12.289: concentrations on stations in the body (12.289.39), the razor's-edge image (12.289.54) and the yogin's powers (12.289.23–29). But the "arrow-maker intent on his arrow" simile is not in this chapter. 12.289.31 has an archer intent on his target. The arrow-maker (*iṣukāra*) appears only at 12.171.61, in Bodhya's list of teachers. Phase D should replace the simile.
- **`src:gita-bhasya-sankara`** (corrected: `dating`). "788–820 CE (most maṭha traditions)" mislabels the older scholarly convention. Some cardinal maṭhas (notably Kāñcī) give 509–477 BCE; Śṛṅgeri cites the 8th c. CE; modern scholarship says c. 700–750. The two accounts are kept separate. U13's `tch:sankara` uses a similar framing and should be flagged in the U13 sweep.
- **`tch:hanuman`** (partial). The summary says "the four sciences" but lists three, and MBh 3.149.31 says three (*tisro vidyāḥ*). Not auto-corrected, because U04 and U06 also emit this teacher and a whole-summary replacement would overwrite their text. U05's wording should say "three".
- **`src:bhasyotkarsadipika` / `tch:dhanapati-suri`** (partial). The text exists (Dhanapati's commentary is in the local gita/gita corpus) and its title and attribution are confirmed. The date is unsettled: one academic source gives Dhanapati 1750–1850; the entry says c. 18th c.
- **`lin:epic-teaching`** (partial). All its texts, teachers and transmission statements are located. But, as the entry says, it is a descriptive grouping of epic material, not a recognized school, so its founder and status cannot be confirmed as such.

## Least-sure items resolved
**Sources**
- **Bhāskara's Gītābhāṣya:** portions survive; Bhāskara is 8th–9th c.
- **Keśava Kāśmīrī's Tattvaprakāśikā:** confirmed, 16th c.
- **Rāmakaṇṭha's Sarvatobhadra:** confirmed; the e-text is local (Muktabodha M00167). Availability corrected to digitized-original.
- **Devabodha's Jñānadīpikā:** the earliest extant Mahābhārata commentary, c. 11th c.
- **Deśika's Gītārthasaṅgraharakṣā:** confirmed in a local eBhāratī text. Availability corrected to digitized-original.
- **Vallabha's Tattvārthadīpanibandha:** its first section (Śāstrārtha-prakaraṇa) deals with the Gītā. It is an independent treatise with a Gītā section, not a verse-by-verse commentary.
- **Gītāmāhātmya:** Padma Purāṇa, Uttarakhaṇḍa, 18 chapters.
- **Manu–Bṛhaspati dialogue:** CE 12.194–199 confirmed (Bṛhaspati asks at 12.194.2–3; Manu speaks in 12.195–199).
- **Uñchavṛtti Upākhyāna:** CE 12.340–353 confirmed (the serpent Padmanābha at 12.343.4; the gleaning sage at 12.351.1).
- **Harivaṃśa chapter count:** 118 confirmed (the local critical text ends at Hv 118.51).
- **Āditya Hṛdaya:** Gita Press 6.105 and DharmicData 6.107; absent from the local Baroda critical text, consistent with reports that the critical edition excised it.

**Teachers:** all six low-confidence teachers are confirmed; only Dhanapati Sūri's dates stay unsettled.

**`tea:ramayana:6.18.33`:** found at Gita Press 6.18.33 in a local text (printed with a half-verse offset). It is 6.12.20 in the Baroda critical text. The DharmicData file lacks Gita Press sarga 18 entirely, which explains the offset the unit noticed.

**The five vulgate-only Yakṣapraśna verses:** all five are in the local vulgate Yakṣa chapter (numbered adhyāya 314 in that edition) and absent from the Critical Edition. Vana-parva 313.116 is web-confirmed for "the greatest wonder"; the other four verse numbers remain unconfirmed.

**`tea:ramayana:2.109.34` (the Buddha verse):** present in both vulgates, absent from the Baroda critical text.

**Commentators' glosses cited in the teaching notes:** all found in the local commentaries — Śaṅkara on 2.12, 6.13, 13.4 and 15.7; Rāmānuja on 13.4 and his two readings of 18.66.

**Epigraphic dating in `lin:bhagavata-early`:** confirmed — the Heliodorus pillar (c. 113 BCE), Ghosuṇḍī and Nānāghāṭ (1st c. BCE), and Pāṇini 4.3.98 (found locally).

**Other points confirmed locally:**
- The Critical Edition chapter counts of all 18 parvans.
- The Gītā as CE 6.23–40 with exactly 700 verses.
- The Nārāyaṇīya chapter lengths.
- The sarga counts of the local Rāmāyaṇa.

## Minor notes for merge or Phase D
- `tea:vyadha-gita:3.197` has location.ref "3.196-197": the id and ref don't match (the content is correct).
- The alternative title "Gokapilīya" for `src:kapila-syumarasmi-samvada` was not confirmed.
- The vulgate range 12.174–365 for the Mokṣadharma was not verified: the local vulgate uses a 375-chapter Śāntiparvan numbering.
- The Madhusūdana date range (1540–1650) overlaps scholarly estimates (c. 1490–1632), but its upper end may be late.
- `tea:mahabharata:11.5-6`: in the text the bees are the desires and the streams of honey are the "tastes of desire" (*kāmarasa*); the paraphrase condenses this.
- For the gap hunter: the local gita/gita corpus has Gītā commentaries under Vallabhācārya's and Puruṣottamajī's names, which bear on the Puṣṭimārga commentary the unit left out.

## Could not be checked
- Exact Gita Press verse numbers for four of the five vulgate-only Yakṣapraśna verses.
- The Rājadharma/Āpaddharma boundary at 12.128/129, which the local JSON cannot show (it has no parvan labels); the range is consistent with the BORI division.
- The contents of editions not held locally: Prameyadīpikā, Tattvaprakāśikā and Bhāskara's Gītābhāṣya (only their existence was confirmed, by web).
- The dispute positions (e.g. Abhinavagupta's and Bhāskara's in `dsp:gita-primary-teaching`) were checked only at the level of each author's known stance, not against their texts.
