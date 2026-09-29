# U46-kagyu — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Scope:** coverage map B6: Kagyu (Marpa/Dakpo Kagyu, Karma, Drikung, Drukpa and the other "four great and eight lesser" schools), the Shangpa, and Mahāmudrā.
**Owned lineages:** lin:kagyu (umbrella), lin:karma-kagyu, lin:drikung-kagyu, lin:drukpa-kagyu, lin:shangpa-kagyu.
**Sub-lineages added:** lin:tsalpa-kagyu, lin:barom-kagyu, lin:phagdru-kagyu, lin:taklung-kagyu, lin:trophu-kagyu, lin:martsang-kagyu, lin:yelpa-kagyu, lin:yazang-kagyu, lin:shugseb-kagyu.
**Parent fields:** every school points directly to the lin:kagyu umbrella so that each counts as its own root for convergence. Descent from Phagmodrupa is recorded under transmissions_received. The Shangpa sits under lin:kagyu by name only; a note says so.

**Counts:** sources 52 · teachers 74 · teachings 147 (59 from local Derge texts with verbatim Wylie originals, 88 from memory) · terms 95 · concepts 77 · practices 45 · obstacles 15 · paths 6 · phenomenology 23 · disputes 3 · borrowings 8 · ultimate 5 · interpretation_log 35.

**Validator:** 0 errors.

**Local material used:** Derge Tengyur (Esukhia/Barom digital edition), converted with pyewts:
- Tōh 2338: Karṇatantravajrapada.
- Tōh 2332: bka' dpe phyi ma.
- Tōh 2331: Ājñāsamyakpramāṇa.
- Tōh 2304: Nāropa's Dṛṣṭisaṃkṣipta.
- Tōh 2305: Tilopa's Acintyamahāmudrā. I read only the first sections in detail.
- Tōh 2337: opening and colophon only.
- Tōh 2303 (Gaṅgā Mahāmudrā) and Tōh 2330 (Ṣaḍdharmopadeśa): read, but they belong to U44. I only reference U44's teaching ids for them (tea:ganga-mahamudra:v…, tea:saddharmopadesa-tilopa:1–6).

No Tibetan-authored Kagyu work is available locally.

## 1. Checklist: coverage-map items → ids

**B6 Kagyu, texts and teachers**
- **Tilopa** (teacher entry is U44's: tch:tilopa)
  - Gaṅgā Mahāmudrā (U44: src:ganga-mahamudra), referenced in rests_on.
  - Created: src:acintyamahamudra (5 teachings), src:ajnasamyakpramana (8 teachings), src:mukhakarnaparampara-cintamani.
  - Six words of advice: src:gnad-kyi-gzer-drug, tea:gnad-kyi-gzer-drug:1, cpt:tilopa-six-words.
  - Four transmissions: cpt:four-transmissions-of-tilopa.
- **Nāropa and his Six Yogas** (tch:naropa is U44's)
  - Sources: src:six-yogas-of-naropa (registry id), src:karnatantravajrapada (18 teachings), src:bka-dpe-phyi-ma (21 teachings), src:drstisamksipta (8 teachings), src:naropa-namthar-lhatsun.
  - Concepts: cpt:six-yogas-of-naropa, cpt:three-bardos-naropa, cpt:five-clear-lights, cpt:mother-and-child-clear-light, cpt:learner-and-non-learner-union, cpt:three-appearances, cpt:twelve-similes-of-illusion, cpt:blending-and-transference.
  - Practices: prc:six-yogas-of-naropa, prc:tummo, prc:illusory-body-yoga, prc:dream-yoga (owned here), prc:clear-light-yoga, prc:bardo-yoga, prc:phowa, prc:trongjuk (transference into another body), prc:trulkhor, prc:karmamudra (Kagyu contribution only).
  - Path: pth:six-yogas-of-naropa-sequence.
- **Marpa:** tch:marpa, tch:dagmema, tch:darma-dode, tch:tiphupa, tch:ngok-choku-dorje, tch:tsurton-wangi-dorje, tch:meton-chenpo; src:marpa-namthar with 2 teachings.
- **Milarepa's songs:** tch:milarepa; src:milarepa-gurbum (compiled by tch:tsangnyon-heruka) with 7 teachings; src:milarepa-namthar with 7 teachings; tch:rechungpa, tch:peta-gonkyi, tch:paldarbum, tch:seben-repa, tch:ngendzong-repa, tch:yungton-trogyal, tch:rongton-lhaga.
- **Gampopa, Jewel Ornament of Liberation:**
  - tch:gampopa; src:jewel-ornament-of-liberation with 17 teachings (intro, ch.1–9, 12, 15, 17–21).
  - Structure: cpt:jewel-ornament-six-topics, pth:jewel-ornament-sequence.
  - Other works: src:four-dharmas-of-gampopa, cpt:four-dharmas-of-gampopa, pth:four-dharmas-of-gampopa, src:precious-garland-of-the-supreme-path, src:gampopa-collected-works (4 teachings).
  - Union of the Kadam and Mahāmudrā streams: cpt:union-of-kadam-and-mahamudra, brw:kadam-to-dakpo-kagyu.
- **The Karmapas:** all 17 as teachers, from tch:dusum-khyenpa through tch:dudul-dorje-karmapa-13. From tch:thekchok-dorje (14th) through the two 17th claimants (tch:ogyen-trinley-dorje, tch:trinley-thaye-dorje) they are flagged recent.
  - Rangjung Dorje: src:profound-inner-meaning, src:aspiration-prayer-of-mahamudra (8 teachings), src:distinguishing-consciousness-and-wisdom, src:treatise-on-buddha-nature-rangjung-dorje.
  - Mikyö Dorje: src:chariot-of-the-dakpo-kagyu-siddhas, src:four-session-guru-yoga, src:kagyu-gurtso.
  - Related concepts: cpt:tulku-system, cpt:black-crown.
- **Wangchuk Dorje:** tch:wangchuk-dorje; src:ocean-of-definitive-meaning, src:dispelling-the-darkness-of-ignorance, src:pointing-out-the-dharmakaya.
- **Dakpo Tashi Namgyal:** src:moonbeams-of-mahamudra (10 teachings), src:clarifying-the-natural-state, pth:moonbeams-mahamudra-stages.
- **Shangpa:**
  - Lineage and teachers: lin:shangpa-kagyu; tch:khyungpo-naljor, tch:mokchokpa, tch:kyergangpa, tch:sangye-nyenton, tch:sangye-tonpa, tch:thangtong-gyalpo. Niguma and Sukhasiddhi are U44's teachers.
  - Sources: src:vajra-lines-of-niguma, src:amulet-mahamudra, src:three-integrations, src:white-and-red-khecari, src:deathless-body-and-mind, src:sukhasiddhi-six-dharmas, src:drodon-khakhyabma.
  - Concepts: cpt:niguma-six-dharmas, cpt:shangpa-five-golden-dharmas, cpt:amulet-mahamudra, cpt:three-integrations, cpt:seven-jewels-of-shangpa, cpt:deathless-body-and-mind.
  - Path: pth:shangpa-five-golden-dharmas.
- **Drikung:** lin:drikung-kagyu; tch:jigten-sumgon, tch:sherab-jungne, tch:rigdzin-chokyi-drakpa; src:gongchig; cpt:single-intent, cpt:fivefold-mahamudra, prc:fivefold-mahamudra, pth:fivefold-mahamudra; dsp:three-vows-one-essence.
- **Drukpa:**
  - Lineage and teachers: lin:drukpa-kagyu; tch:lingje-repa, tch:tsangpa-gyare, tch:gotsangpa, tch:lorepa, tch:yang-gonpa, tch:orgyenpa, tch:pema-karpo, tch:zhabdrung-ngawang-namgyal, tch:drukpa-kunley.
  - Sources: src:six-equal-tastes, src:pema-karpo-mahamudra-treasury, src:epitome-of-the-great-symbol, src:epitome-of-the-six-doctrines, src:hidden-description-of-the-vajra-body, src:drukpa-kunley-namthar.
  - Concepts and practices: cpt:six-equal-tastes, prc:six-equal-tastes, cpt:mad-yogin-conduct.
- **Phagmodrupa, Taklung, Tsalpa and the other schools:**
  - Phagmodrupa: tch:phagmodrupa, lin:phagdru-kagyu.
  - Taklung: tch:taklung-thangpa, lin:taklung-kagyu.
  - Tsalpa: tch:lama-zhang, lin:tsalpa-kagyu, src:ultimate-supreme-path-of-mahamudra.
  - Barom and the remaining lesser schools: tch:barom-darma-wangchuk plus the founders of Trophu, Martsang, Yelpa, Yazang and Shugseb.
  - Overview concept: cpt:four-great-and-eight-lesser-kagyu.
- **Jamgön Kongtrul's Kagyu writings (recent):** src:torch-of-certainty (with a teaching), src:kagyu-ngagdzo, prc:three-year-retreat. tch:jamgon-kongtrul is U48's.
- **Other teachers:** tch:go-lotsawa (src:blue-annals, src:go-lotsawa-ratnagotravibhaga-commentary), tch:situ-panchen, tch:pawo-tsuglag-trengwa (src:feast-for-scholars), tch:khedrup-drakpa-senge, tch:karma-trinlepa, tch:bengar-jampal-zangpo (src:dorje-chang-thungma, 5 teachings), tch:tsele-natsok-rangdrol (src:lamp-of-mahamudra), tch:lhatsun-rinchen-namgyal, tch:chogyam-trungpa (recent).
  - Karma Chagmé is U45's teacher; his works were created here: src:union-of-mahamudra-and-dzogchen and src:karma-chagme-mountain-dharma.

**B6 Kagyu, concepts**
- **Four yogas:** cpt:four-yogas-of-mahamudra (with the twelve levels); terms trm:ekagrata, trm:nisprapanca, trm:ekarasa, trm:gomme.
  - Teachings supplied for U51's pth:mahamudra-four-yogas: tea:moonbeams-of-mahamudra:pt.2/6, pt.2/7, pt.2/8 and tea:aspiration-prayer-of-mahamudra:four-yogas.
- **Sūtra, tantra and essence Mahāmudrā:** cpt:three-kinds-of-mahamudra.
- **The co-emergent:** cpt:co-emergent-union, trm:lhenchik-kyejor, trm:sahaja (Kagyu definition), cpt:sahaja.
- **Pointing-out:** cpt:pointing-out-instruction, trm:ngotro, prc:pointing-out.

**Brief extras**
- Śamatha and vipaśyanā: cpt:samatha-vipasyana-in-mahamudra, prc:mahamudra-samatha-with-support, prc:mahamudra-samatha-without-support, prc:looking-at-the-mind, cpt:stillness-movement-awareness.
- Ordinary mind: cpt:ordinary-mind, trm:thamal-gyi-shepa.
- View, meditation, conduct, fruition: cpt:view-meditation-conduct-fruition.
- The preliminaries: cpt:ngondro, prc:ngondro, cpt:four-thoughts-that-turn-the-mind, prc:four-thoughts-that-turn-the-mind, prc:refuge-prostrations, prc:vajrasattva-purification, prc:mandala-offering, prc:guru-yoga, prc:four-session-guru-yoga.
- Guru devotion: cpt:guru-devotion, trm:mogu, trm:adhisthana.
- Cutting the root of mind: prc:cutting-the-root-of-mind.
- Three-year retreat: prc:three-year-retreat (recent).

**Disputes**
- dsp:sutra-mahamudra (new; owned). Three sides: Kagyu, Sakya, Gelug. Status: queued, with candidate readings under P4-stage, P1-level and P6-upaya.
- Sudden or gradual: the Kagyu side is supplied as tea:ajnasamyakpramana:271a.3 and cpt:gradual-and-simultaneous-persons, linked to U50's dsp:sudden-or-gradual.
- dsp:three-vows-one-essence (new): partially reconciled under P2-standpoint, with the traditions' objections recorded.
- dsp:four-yogas-and-the-grounds (new): queued, low confidence.
- Kagyu teachings bearing on U50's dsp:rangtong-shentong are linked to it.

**Section D per lineage**
- Ultimate: ult:kagyu, ult:karma-kagyu, ult:drikung-kagyu, ult:drukpa-kagyu, ult:shangpa-kagyu, with caveats.
- Mind: cpt:luminous-mind, cpt:eight-consciousnesses, cpt:consciousness-and-wisdom, cpt:mind-only, cpt:two-truths, cpt:clarity-emptiness-union, cpt:four-kayas.
- Self: cpt:buddha-nature, cpt:two-selflessnesses.
- Body and matter: cpt:vajra-body, cpt:four-elements.
- Obstacles: 15 entries, including obs:four-deviations-mahamudra, obs:three-strayings-mahamudra, obs:clinging-to-nyam, obs:wind-disorder-from-practice.
- Ethics: cpt:three-vows, cpt:samaya, cpt:mad-yogin-conduct.
- Karma and liberation: cpt:karma, cpt:buddhahood-in-one-lifetime, cpt:deathless-body-and-mind.
- Signs and powers: cpt:siddhis-kagyu, plus 23 phenomenology items.
- Transmission and testing the teacher: cpt:testing-guru-and-disciple, cpt:teacher-disciple-relation, cpt:four-kinds-of-spiritual-friend, cpt:hearing-lineage, cpt:golden-rosary, cpt:seal-of-secrecy, cpt:three-roots, cpt:practice-lineage.
- Cosmology: cpt:rebirth-realms (minimal; nothing distinctively Kagyu).
- Sound and language: cpt:vajra-songs, trm:gur, prc:karmapa-khyenno, prc:om-mani-padme-hum.
- Death and dying: cpt:dying-process, cpt:antarabhava, plus the death-related phenomenology items.

**Corrections to the brief**
- The six dharmas are listed differently by different sources. Tilopa's Tōh 2330 groups the bardo, transference and "entering a town" under Sukhasiddhi. The Karṇatantravajrapada adds karmamudrā.
- Tōh 2330 names the four transmissions as: Caryāpa for caṇḍālī; Nāgārjuna for illusory body and clear light; Lavapa for dream; Sukhasiddhi for bardo and transference. Other Kagyu lists differ.
- Wangchuk Dorje wrote three Mahāmudrā manuals, not two. The middle one, src:dispelling-the-darkness-of-ignorance, has been added.
- The terms "sūtra, tantra and essence Mahāmudrā" look like a late systematization (Jamgön Kongtrul era). Their earlier history is not certain.
- On the first tulku, the tradition names Karma Pakshi, while many scholars date the first formal recognition to Rangjung Dorje. Both accounts are recorded.
- Sukhasiddhi's teacher entry belongs to U44 (tch:sukhasiddhi) and was not re-created here.

## 2. Least-sure items (check these first for hallucination)
- **Source attributions and titles:**
  - src:ajnasamyakpramana: the ascription to Tilopa is from memory; the text read does not name him.
  - src:bka-dpe-phyi-ma: the title rendering and the authorship are uncertain.
  - Titles from memory: src:pema-karpo-mahamudra-treasury, src:go-lotsawa-ratnagotravibhaga-commentary, src:ultimate-supreme-path-of-mahamudra, src:karma-chagme-mountain-dharma.
  - The Tibetan title of src:clarifying-the-natural-state and the Tibetan title of src:naropa-namthar-lhatsun are uncertain.
  - Title and content uncertain: src:vajra-lines-of-niguma, src:deathless-body-and-mind, src:sukhasiddhi-six-dharmas, src:gnad-kyi-gzer-drug, src:drukpa-kunley-namthar.
  - src:six-equal-tastes: the list of the six is from memory.
- **Teachers:**
  - tch:pomdrakpa: name form and relationships.
  - tch:drogmi as Marpa's first teacher.
  - The split of Marpa's transmissions among Ngok, Tsur and Meton.
  - tch:rongton-lhaga and tch:yungton-trogyal.
  - tch:seben-repa, tch:ngendzong-repa, tch:peta-gonkyi, tch:paldarbum.
  - The Shangpa "seven jewels" and their order.
  - The founders of Trophu, Martsang, Yelpa, Yazang and Shugseb.
  - Dates of tch:barom-darma-wangchuk, tch:rigdzin-chokyi-drakpa, tch:lorepa, tch:karma-trinlepa, tch:lhatsun-rinchen-namgyal and tch:bengar-jampal-zangpo, and whether Bengar taught the 7th Karmapa.
  - The founding year of Tsurphu.
- **Structural claims:**
  - The Jewel Ornament's 21-chapter numbering, used for all its refs.
  - The Gongchig's count of about 150 statements in 7 chapters.
  - The Profound Inner Meaning's chapter structure and its 1322 date.
  - The Aspiration Prayer's verse count (about 25); its teachings use section anchors because verse numbers are uncertain.
- **Memory-based teachings with weak locators:**
  - tea:gampopa-collected-works:* (topic anchors only).
  - tea:gongchig:*.
  - tea:ultimate-supreme-path-of-mahamudra:*.
  - tea:six-equal-tastes:1, tea:vajra-lines-of-niguma:1, tea:amulet-mahamudra:three-self-liberations.
  - tea:moonbeams-of-mahamudra:pt.2/3, pt.2/7, pt.2/9.
  - tea:profound-inner-meaning:*.
  - tea:discrimination-of-the-three-vows:ch.3/2 (U47's source).
  - tea:milarepa-gurbum:lachi-snow and tea:precious-garland-of-the-supreme-path:ch.1.
- **Other:**
  - dsp:four-yogas-and-the-grounds: which masters held which correlation is not known.
  - phn:dream-illusion-signs-ajnasamyakpramana: tentative rendering of the Tibetan terms.
  - cpt:blending-and-transference (bsre 'pho as the Ngok tradition's name) and cpt:two-kinds-of-mindfulness.
- **Where the Tengyur passages were cut:** in tea:bka-dpe-phyi-ma:273a.6 two phrases are left unparaphrased (noted in the entry). The 272b.6 passage of Tōh 2331 opens with a list of twelve terms that is paraphrased only as a list.

## 3. Gaps (belong here but could not be created responsibly)
- **No local text for any Tibetan-authored Kagyu work.** Everything from Gampopa, Milarepa, the Karmapas, Moonbeams, the Gongchig, Pema Karpo and the Shangpa is memory-based and needs a sourcing pass (e.g. BDRC e-texts).
- **Kagyu works not created:**
  - The Rechung hearing-lineage corpus.
  - Gampopa's answers to Düsum Khyenpa, as a separate source.
  - Rangjung Dorje's Karma Nyingthig and his tantra commentaries.
  - The 7th Karmapa's pramāṇa work.
  - The 8th Karmapa's Abhisamayālaṅkāra commentary and his shentong-leaning treatise.
  - Situ Paṇchen's works.
  - Götsangpa's and Yangönpa's mountain-dharma cycles, and Pema Karpo's history.
  - Taklung, Barom and Tsalpa literature.
  - Separate Six Yogas manuals of Gampopa and Phagmodrupa.
- **Incarnation lines and branches not created:** Gyaltsap, Situ (except the 8th), Pawo (except the 2nd), Shamar (except the 1st), the Drukchen after Pema Karpo, Drikung Chetsang and Chungtsang, the Zurmang and Nedo branch founders.
- **Owned by other units and still missing:**
  - Tsongkhapa's commentary on the six dharmas and the First Panchen Lama's Mahāmudrā root text (U47). The Gelug side of dsp:sutra-mahamudra has no rests_on until U47 supplies them.
  - Shākya Chokden's defence of Mahāmudrā (U47).
- **Ids guessed for other units:** src:discrimination-of-the-three-vows (U47 may use src:domsum-rabye). tch:drogmi (U47 may use another slug, e.g. tch:drokmi-lotsawa).
- **Dangling registry references**, left for their owners: pth:mahamudra-four-yogas, pth:five-paths, pth:ten-bhumis, pth:nine-stages-calm-abiding (U51); dsp:sudden-or-gradual, dsp:rangtong-shentong (U50); tch:kalu-rinpoche (U52).
- **Not created at all:**
  - The contested recognition of the 17th Karmapa is political. It is recorded as metadata only, not as a dispute.
  - A Kagyu dark-retreat practice: U45 owns dark retreat, and Kagyu usage is uncertain.
- **Wordings omitted under the certainty rule:** the Tibetan of Tilopa's six words, Gampopa's four dharmas and Gampopa's definition of ordinary mind.

## 4. Out of reach
- The sealed whispered-lineage oral instructions. The texts themselves say they are sealed "to the thirteenth generation" and "three times".
- The method details of inner heat and wind practices, the yantra exercises, karmamudrā, phowa, grong 'jug and the Shangpa deathless practices. These are recorded only as summaries with the texts' warnings, by policy.
- Retreat curricula and manuals given only in retreat.
- Collected works of minor Kagyu schools that exist only as undigitized scans.

## Coordination notes
- **Other units' teachers referenced, not re-created:**
  - U44: tch:tilopa, tch:naropa, tch:maitripa, tch:niguma, tch:sukhasiddhi, tch:vajradhara, tch:kukkuripa.
  - U45: tch:karma-chagme, tch:kumaraja.
  - U48: tch:jamgon-kongtrul, tch:taranatha.
  - U47: tch:sakya-pandita, tch:sachen-kunga-nyingpo.
- **U44 overlap:** six Tengyur hearing-lineage texts were created here with lineages [lin:kagyu, lin:mahasiddha]: Tōh 2304, 2305, 2331, 2332, 2337, 2338. They are not in U44's source list. If U44 adds them, merge by id.
- **Shared ids that received Kagyu definitions:**
  - Terms: trm:mahamudra (distinct from the haṭha seal), trm:sahaja, trm:rigpa, trm:citta, trm:jnana, trm:vijnana, trm:sunyata, trm:dharmakaya, trm:nadi, trm:prana, trm:bindu, trm:antarabhava, trm:guru, trm:abhiseka, trm:samaya, trm:shentong (spelled to match the registry's dsp:rangtong-shentong).
  - Concepts: cpt:buddha-nature, cpt:dying-process, cpt:luminous-mind, cpt:two-truths.
- **New Kagyu practice id:** Kagyu Mahāmudrā practice is prc:mahamudra-meditation, kept separate from the haṭha prc:mahamudra.
- **Owned shared practice:** prc:dream-yoga. Shared with U45: prc:guru-yoga, prc:ngondro, cpt:ngondro, cpt:three-roots, trm:nyam.
- **For RECONCILE_QUEUE.md:** dsp:sutra-mahamudra and dsp:four-yogas-and-the-grounds are queued with candidate readings.
- **Interpretation log:** every equivalence, correspondence, path banding and reconciliation has a line in interpretation_log.jsonl (35 lines).
- **Generators:** shards/skeleton/U46-kagyu/_gen/part1…part9 plus common.py and derge.py. Run them in order from tradition-ontology/; each part re-runs safely.
