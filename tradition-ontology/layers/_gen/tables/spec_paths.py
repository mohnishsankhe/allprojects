"""Reviewed specs for layers/tables/path_map_correspondence.json.
Stages come from data/paths.json by code (name, gloss, ref, band, rests_on), except where a map below adds stages
from the same text (marked band_source 'this table'). user_facing is computed by build.py.
"""

BANDS = {
    "B0": "entry, turning, qualification, faith, refuge, preliminaries",
    "B1": "ethical foundation and purification",
    "B2": "preparatory discipline (posture, breath, study, devotional or ritual practice)",
    "B3": "withdrawal and one-pointed concentration",
    "B4": "absorption with support (jhāna, samprajñāta samādhi, stable calm)",
    "B5": "first direct seeing / insight / recognition",
    "B6": "cultivation and deepening after seeing",
    "B7": "final liberation",
    "B8": "activity after liberation",
}

# how to turn a stage's text ref into teaching ids when data/paths.json gives no rests_on for the stage
REF_RULES = {
    "pth:anapanasati-sixteen-steps": ("MN 118:", "tea:anapanasati-sutta:mn118:"),
    "pth:bojjhanga-sequence": ("MN 118:", "tea:anapanasati-sutta:mn118:"),
    "pth:gita-devotion-ladder": ("BhG ", "tea:bhagavad-gita:"),
    "pth:tattvartha-ten-stages-of-nirjara": ("TS ", "tea:tattvartha-sutra:"),
    "pth:yoga-sutra-eight-limbs": ("YS ", "tea:yoga-sutra:"),
}

# per-stage cites where the data ref points only at the list verse (YS 2.29 names all eight limbs); the limb's own
# defining sūtra is cited instead
STAGE_CITE_OVERRIDES = {
    ("pth:yoga-sutra-eight-limbs", 6): ["tea:yoga-sutra:3.1"],
    ("pth:yoga-sutra-eight-limbs", 7): ["tea:yoga-sutra:3.2"],
    ("pth:yoga-sutra-eight-limbs", 8): ["tea:yoga-sutra:3.3"],
}

# bands that the objection texts below state as facts about data/paths.json; build.py fails if the data changes
BAND_CLAIMS = [
    ("pth:gita-devotion-ladder", 1, "B1"),
    ("pth:anapanasati-sixteen-steps", 12, "B5"),
    ("pth:anapanasati-sixteen-steps", 16, "B7"),
    ("pth:seven-purifications", 2, "B4"), ("pth:seven-purifications", 3, "B4"), ("pth:seven-purifications", 4, "B4"),
    ("pth:seven-purifications", 5, "B4"), ("pth:seven-purifications", 6, "B4"), ("pth:seven-purifications", 7, "B5"),
    ("pth:jain-fourteen-gunasthanas", 1, None), ("pth:jain-fourteen-gunasthanas", 2, None),
    ("pth:jain-fourteen-gunasthanas", 3, "B0"), ("pth:jain-fourteen-gunasthanas", 4, "B5"),
    ("pth:jain-fourteen-gunasthanas", 5, "B1"), ("pth:jain-fourteen-gunasthanas", 6, "B1"),
    ("pth:tattvartha-ten-stages-of-nirjara", 1, "B5"), ("pth:tattvartha-ten-stages-of-nirjara", 2, "B6"),
]

MAPS = [
    {
        "id": "map:ys-eight-limbs",
        "path_id": "pth:yoga-sutra-eight-limbs",
        "lineage": "lin:patanjala-yoga",
        "name": "Patañjali's eight limbs (YS 2.29–3.8), continued in the YS's own terms to kaivalya",
        "extra_stages": [
            {"order": 9, "name": "viveka-khyāti", "gloss": "discriminative discernment, to which the light of knowledge rises through the limbs", "ref": "YS 2.26, 2.28", "band": "B5", "cites": ["tea:yoga-sutra:2.26", "tea:yoga-sutra:2.28"]},
            {"order": 10, "name": "prānta-bhūmi prajñā", "gloss": "insight at the final stage, sevenfold", "ref": "YS 2.27", "band": "B6", "cites": ["tea:yoga-sutra:2.27"]},
            {"order": 11, "name": "dharma-megha samādhi", "gloss": "the samādhi called 'cloud of dharma', for one without desire even in the highest discernment", "ref": "YS 4.29", "band": "B6", "cites": ["tea:yoga-sutra:4.29"],
             "band_note": "Placed at B6 because YS puts dharmamegha before kaivalya (YS 4.29, 4.34). config/data_model.md names 'dharmamegha as culmination' under B8; that placement does not match the YS order, so it is flagged for review."},
            {"order": 12, "name": "kaivalya", "gloss": "aloneness: the seer established in its own form", "ref": "YS 2.25, 4.34", "band": "B7", "cites": ["tea:yoga-sutra:2.25", "tea:yoga-sutra:4.34"]},
        ],
        "safety_notes": {"prāṇāyāma": "Breath-regulation in YS includes suspension (stambha-vṛtti, YS 2.50). It stays summary-only and is never recommended. Its teachings are restricted in data/, so this stage is not user-facing."},
        "objection_to_alignment": {
            "text": "The Yoga calls these limbs (aṅga), not rungs. Concentration, meditation and samādhi on one object together are saṃyama (YS 3.4). The three are 'inner' in relation to the first five (YS 3.7), and even they are outer to the seedless samādhi (YS 3.8). Through the practice of the limbs, as impurity is destroyed, the light of knowledge rises up to discriminative discernment (YS 2.28): the limbs purify, and they do not match another tradition's attainments stage for stage. Aligning samādhi (B4) with jhāna, or kaivalya (B7) with nibbāna or mokṣa, is the band scheme's claim, not the Yoga's. Kaivalya is the seer's aloneness (YS 4.34), a state the Theravāda and Jain rows of one_truth.json do not accept.",
            "cites": ["tea:yoga-sutra:3.4", "tea:yoga-sutra:3.7", "tea:yoga-sutra:3.8", "tea:yoga-sutra:2.28", "tea:yoga-sutra:4.34"],
        },
        "principle": {"id": "P4-stage", "reason": "The bands are stages of the student (adhikāra). They are used only to place each limb beside other maps' stages, never to equate what is attained."},
    },
    {
        "id": "map:mn118-sixteen-steps",
        "path_id": "pth:anapanasati-sixteen-steps",
        "lineage": "lin:early-buddhism",
        "name": "The sixteen steps of mindfulness of breathing (MN 118:18–21)",
        "extra_stages": [],
        "objection_to_alignment": {
            "text": "In MN 118 the sixteen steps are four tetrads, and each tetrad fulfils one establishment of mindfulness (MN 118:23–28). The establishments fulfil the seven awakening factors, and these fulfil knowledge and liberation (MN 118:29, 118:43). The steps are contemplations trained in together, not attainments passed one by one. Step 12, 'liberating the mind', belongs to the contemplation of mind (MN 118:20, 118:26), not to the noble persons whom the sutta names by the fetters they have ended (MN 118:9–12). The B5–B7 bands that data/paths.json gives to steps 12–16 are interpretive placements, not yet reconciled with this reading. MN 10 gives the fruit as final knowledge or non-return within seven years, or even seven days (MN 10:46): the text fixes no timetable of stages.",
            "cites": ["tea:anapanasati-sutta:mn118:23", "tea:anapanasati-sutta:mn118:28", "tea:anapanasati-sutta:mn118:29", "tea:anapanasati-sutta:mn118:43", "tea:anapanasati-sutta:mn118:20", "tea:anapanasati-sutta:mn118:26", "tea:anapanasati-sutta:mn118:9", "tea:anapanasati-sutta:mn118:12", "tea:satipatthana-sutta:mn10:46"],
        },
        "principle": {"id": "P4-stage", "reason": "The steps are placed by the kind of practice they name (body and calming at B3, rapture and pleasure at B4, and so on). They are not placed as ranks of attainment."},
    },
    {
        "id": "map:mn118-bojjhanga",
        "path_id": "pth:bojjhanga-sequence",
        "lineage": "lin:early-buddhism",
        "name": "The seven awakening factors arising in sequence (MN 118:30–36), fulfilling knowledge and liberation (MN 118:43)",
        "extra_stages": [
            {"order": 8, "name": "vijjā-vimutti", "gloss": "knowledge and liberation, fulfilled by the seven factors", "ref": "MN 118:43", "band": "B7", "cites": ["tea:anapanasati-sutta:mn118:43"]},
        ],
        "objection_to_alignment": {
            "text": "The factors are developed together, each supported by seclusion, dispassion and cessation and ripening in relinquishment (MN 118:42). Their order is the order in which they arise in one sitting's practice, not a ladder of years. Placing them at B3–B4 records only that they belong to cultivation before the fruit named at MN 118:43.",
            "cites": ["tea:anapanasati-sutta:mn118:42", "tea:anapanasati-sutta:mn118:43"],
        },
        "principle": {"id": "P4-stage", "reason": "Placed by what the text says each factor does in practice. No equivalence with the Yoga's limbs or the Gītā's means is implied."},
    },
    {
        "id": "map:mn118-mn10-noble-persons",
        "path_id": None,
        "lineage": "lin:early-buddhism",
        "name": "The noble persons named in MN 118:9–12 and the two fruits of MN 10:46",
        "extra_stages": [
            {"order": 1, "name": "sotāpanna (stream-enterer)", "gloss": "with the ending of three fetters; not liable to fall, fixed in destiny, heading for awakening", "ref": "MN 118:12", "band": "B5", "cites": ["tea:anapanasati-sutta:mn118:12"]},
            {"order": 2, "name": "sakadāgāmī (once-returner)", "gloss": "with three fetters ended and lust, hatred and delusion weakened", "ref": "MN 118:11", "band": "B6", "cites": ["tea:anapanasati-sutta:mn118:11"]},
            {"order": 3, "name": "anāgāmī / anāgāmitā (non-return)", "gloss": "with the five lower fetters ended; one of the two fruits of MN 10", "ref": "MN 118:10; MN 10:46", "band": "B6", "cites": ["tea:anapanasati-sutta:mn118:10", "tea:satipatthana-sutta:mn10:46"]},
            {"order": 4, "name": "arahant; aññā (final knowledge)", "gloss": "taints destroyed, the burden laid down, liberated by final knowledge; the other fruit of MN 10", "ref": "MN 118:9; MN 10:46", "band": "B7", "cites": ["tea:anapanasati-sutta:mn118:9", "tea:satipatthana-sutta:mn10:46"]},
        ],
        "objection_to_alignment": {
            "text": "The noble persons are defined by the fetters they have ended (MN 118:10–12), not by a meditative state or by a self seen. Placing stream-entry at B5, 'first direct seeing', beside the Yoga's discriminative discernment or an Upaniṣadic seeing of the self would be rejected by the Theravāda, which denies that anything seen is a self (see ot:theravada in one_truth.json). The sutta also lists the persons from the highest down (MN 118:9–12). The order here is only the band order.",
            "cites": ["tea:anapanasati-sutta:mn118:9", "tea:anapanasati-sutta:mn118:10", "tea:anapanasati-sutta:mn118:11", "tea:anapanasati-sutta:mn118:12"],
        },
        "principle": {"id": "P4-stage", "reason": "Stages of the noble disciple are placed as stages of the student. What is realised at each stage is described in the Theravāda's own terms only."},
    },
    {
        "id": "map:gita-12-8-12",
        "path_id": "pth:gita-devotion-ladder",
        "lineage": "lin:bhagavata-early",
        "name": "The graded means of BhG 12.8–12",
        "extra_stages": [],
        "objection_to_alignment": {
            "text": "The Gītā gives these as alternatives by capacity, not as stages one passes through: 'if you cannot … then …' (BhG 12.9–11). It also ranks them against the order of ease. Knowledge is better than practice, meditation better than knowledge, and relinquishing the fruit of actions better than meditation, for peace follows relinquishment at once (BhG 12.12). Placing relinquishing the fruit at B1 (data/paths.json) follows the order of ease and inverts the Gītā's own valuation. The alignment is kept only as an ordering by capacity (adhikāra).",
            "cites": ["tea:bhagavad-gita:12.8", "tea:bhagavad-gita:12.9", "tea:bhagavad-gita:12.10", "tea:bhagavad-gita:12.11", "tea:bhagavad-gita:12.12"],
        },
        "principle": {"id": "P4-stage", "reason": "The text itself grades the means by what the student can do (BhG 12.9–11). That is adhikāra, not a sequence of attainments."},
    },
    {
        "id": "map:vism-seven-purifications",
        "path_id": "pth:seven-purifications",
        "lineage": "lin:theravada",
        "name": "The seven purifications (MN 24; Visuddhimagga)",
        "extra_stages": [],
        "objection_to_alignment": {
            "text": "In MN 24 each purification serves only the next, like a relay of chariots, and the holy life is lived for none of them but for final nibbāna without clinging (MN 24). The Visuddhimagga calls purification itself nibbāna (Vism I). The stages are means, so aligning them one for one with other maps' attainments misreads them. In data/paths.json five of the seven are placed at B4 and only the last at B5, so the band scheme compresses the Visuddhimagga's whole insight sequence.",
            "cites": ["tea:rathavinita-sutta:9-15", "tea:visuddhimagga:1/2"],
        },
        "principle": {"id": "P4-stage", "reason": "Placed as stages of the student's purification. Their content is not equated with the other maps' stages."},
    },
    {
        "id": "map:jain-gunasthanas",
        "path_id": "pth:jain-fourteen-gunasthanas",
        "lineage": "lin:jainism",
        "name": "The fourteen stages of quality (guṇasthāna), with TS 9.45",
        "extra_stages": [],
        "objection_to_alignment": {
            "text": "The ladder is defined by the subsidence and destruction of deluding karma: TS 9.45 names 'the subsider', 'the one whose delusion is subsided', 'the destroyer' and 'the one whose delusion is destroyed'. Its order does not follow the bands. Right view without restraint (the 4th stage) comes before partial and careless restraint (the 5th and 6th), so a stage placed at B5 precedes stages placed at B1. The first two stages have no band at all in data/paths.json. The fourteen names come from the Gommaṭasāra (GJK 9–10), not from TS, which gives the ten stages of 9.45.",
            "cites": ["tea:tattvartha-sutra:9.45", "tea:gommatasara-jivakanda:9-10"],
        },
        "principle": {"id": "P4-stage", "reason": "The guṇasthānas are the Jain tradition's own stages of the soul. They are placed by band only for comparison, and the Jain order is kept."},
    },
    {
        "id": "map:ts-9-45-nirjara",
        "path_id": "pth:tattvartha-ten-stages-of-nirjara",
        "lineage": "lin:jainism",
        "name": "The ten stages of increasing shedding of karma (TS 9.45)",
        "extra_stages": [],
        "objection_to_alignment": {
            "text": "TS 9.45 ranks these stages by how much karma is shed, each innumerable times more than the one before. The measure is the shedding of karmic matter, which no other map uses. Right view comes first, and the layman (śrāvaka) and the renouncer (virata) come after it. In data/paths.json the layman and every later stage sit at B6, and the ethical restraint that other maps put at B1 sits after seeing.",
            "cites": ["tea:tattvartha-sutra:9.45"],
        },
        "principle": {"id": "P4-stage", "reason": "Stages of the soul's shedding, placed by band for comparison only."},
    },
]

BAND_NOTES = {
    "B0": "Only the guṇasthāna map places a stage here (the mixed view, 3rd stage), and the Jain order puts it before right view. The other maps begin at B1 or later. The setting of MN 118:17 (seclusion, posture, mindfulness established) precedes the steps but is not a numbered stage.",
    "B8": "No stage of these maps is placed at B8. The marks of the devotee dear to the Lord (BhG 12.13–20) and of the one gone beyond the guṇas (BhG 14.22–26) describe the realised, but they are not stages in these maps.",
}
