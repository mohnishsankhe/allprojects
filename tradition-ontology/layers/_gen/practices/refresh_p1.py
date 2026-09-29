"""P1 practice-layer refresh: add new px: entries and repair existing ones in layers/practices.json.

Run from anywhere:  python3 refresh_p1.py [--write]
Without --write it only validates and prints. All mechanical checks are done here by code.
"""
import copy
import json
import re
import sys
from collections import Counter

ROOT = __import__("os").path.abspath(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT)
from insight import ontology as O, claims  # noqa: E402

PX_PATH = f"{ROOT}/layers/practices.json"
FIELDS = ["id", "name", "lens", "ontology_refs", "tradition", "summary", "steps", "targets", "stage", "duration",
          "warnings", "safety_tier", "tier_reason", "cites", "user_facing"]

DEFAULT_DUR = {"minutes_per_session": [5, 10], "sessions_per_day": 1,
               "basis": "product default for a beginner; the text gives no length"}
ALLDAY_DUR = lambda what: {"minutes_per_session": [5, 10], "sessions_per_day": 1,  # noqa: E731
                           "basis": f"product default for a beginner: one short sitting a day; the text applies the practice to {what} and gives no length"}
NONE_DUR = {"minutes_per_session": None, "sessions_per_day": None,
            "basis": "not set: summary only; the product gives no length for a practice it does not guide"}


def vbt(*v):
    return [f"tea:vijnana-bhairava-tantra:{x}" for x in v]


def dhp(*v):
    return [f"tea:dhammapada:{x}" for x in v]


def ts(*v):
    return [f"tea:tattvartha-sutra:{x}" for x in v]


def ys(*v):
    return [f"tea:yoga-sutra:{x}" for x in v]


def yb(*v):
    return [f"tea:yoga-bhasya:{x}" for x in v]


def bg(*v):
    return [f"tea:bhagavad-gita:{x}" for x in v]


def vism(*v):
    return [f"tea:visuddhimagga:{x}" for x in v]


def hyp(*v):
    return [f"tea:hatha-yoga-pradipika:{x}" for x in v]


# ---------------------------------------------------------------- shared warnings
W_VBT_SECRECY = {
    "text": "The tantra says its teaching is to be kept hidden: it is not to be given to another teacher's disciple, "
            "to the wicked or the cruel, or to one without devotion to the teacher, but to devotees and to the "
            "teacher's circle (VBT 157–159). The product gives only this verse's plain instruction, not the tantra's "
            "wider practice.",
    "cites": vbt(157, 158, 159)}
W_VBT_146 = {
    "text": "The tantra says meditation (dhyāna) is the unmoving understanding, without form and without support; it is "
            "not the imagining of a body, eyes, face, hands and the like (VBT 146). The steps do not ask you to picture "
            "a form.",
    "cites": vbt(146)}
W_YS_LONG = {
    "text": "Practice becomes firm only when cultivated for a long time, without interruption and with earnestness "
            "(satkāra); the sūtra does not present it as quick (YS 1.14).",
    "cites": ys("1.14")}
W_DHP_GRADUAL = {
    "text": "The Dhammapada's counsel is gradual work: 'little by little, moment by moment' the wise blow away their "
            "own stains, as a smith the dross of silver (Dhp 239).",
    "cites": dhp(239)}
W_TS_ARTA = {
    "text": "Nearest general caution in the Tattvārtha (the sūtra gives none for this practice): reflection must not "
            "turn into sorrowful dwelling (ārta-dhyāna), which the sūtra defines as the mind brought back again and "
            "again to getting away from the disagreeable, to the agreeable, to a painful feeling, or to hankering for "
            "future enjoyment (nidāna) (TS 9.30–9.33).",
    "cites": ts("9.30", "9.31", "9.32", "9.33")}
W_TS_VOW = lambda vow: {  # noqa: E731
    "text": f"These are supports (bhāvanā) that steady the vow of {vow}, not the vow itself; the sūtra distinguishes "
            "the partial small vow (aṇuvrata) from the complete great vow (mahāvrata) of the renouncer (TS 7.2–7.3).",
    "cites": ts("7.2", "7.3")}

GENTLE_NO_BODY = "no breath control, gaze, posture technique, austerity or vow"

# ---------------------------------------------------------------- new entries
NEW = []


def add(**e):
    NEW.append(e)


# ======== vedic-yogic: Vijñāna Bhairava (Trika) — gentle
add(id="px:vbt-sound-to-its-end-41",
    name="Following a sound to its end (VBT 41)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-18"], tradition="lin:trika",
    summary="VBT 41: attend, with the mind on nothing else (ananya-cetas), to the long, successively arranged sounds "
            "of stringed and other instruments; the verse says that at the end (pratyanta) one would become of the "
            "form of supreme space (paravyoma). The Vijñāna Bhairava is a Śaiva tantra of the Trika: Bhairava answers "
            "the Goddess with a hundred and twelve teachings of the waveless state (VBT 139), of which this is one.",
    steps=["Sit comfortably where you can hear a long, sustained sound of a stringed or other instrument (VBT 41).",
           "Attend to the sound with the mind on nothing else (ananya-cetas) (VBT 41).",
           "Follow it as the notes succeed one another, until it fades (VBT 41: 'long, successively arranged sounds').",
           "At its very end (pratyanta), stay with that ending (VBT 41).",
           "Close gently."],
    targets=["dx:gita-restless-mind"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY,
              {"text": "This is attention to an outer sound. The tantra's practice of the inner, unstruck sound "
                       "(anāhata, VBT 38) is a different practice and is not part of these steps.",
               "cites": vbt(41, 38)}],
    safety_tier="gentle",
    tier_reason="Listening to an outer sound with undivided attention; " + GENTLE_NO_BODY + ". The tantra's rule of "
                "transmission (VBT 157–159) is shown as a caution; see PRACTICES_REPORT.md (P1 refresh) for this call.",
    cites=vbt(41, 139))

add(id="px:vbt-middle-between-two-61-62",
    name="Resting in the middle between two thoughts (VBT 61–62)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-37", "prc:vbt-dharana-38"], tradition="lin:trika",
    summary="VBT 62: when one object (bhāva) has been let go and awareness (cit) is held back so that it does not go on "
            "to another, abide in the middle between the two (tanmadhya-bhāva); the verse says the contemplation then "
            "blossoms exceedingly. VBT 61: in the cognition of two things, take refuge in the middle and let both go "
            "at once; the verse says that in the middle reality (tattva) shines.",
    steps=["Sit comfortably and let thoughts and perceptions come as they do.",
           "When one object of attention has been let go, do not go on at once to the next (VBT 62).",
           "Stay in the middle between the two (tanmadhya-bhāva) (VBT 62).",
           "Or, when you are aware of two things, take refuge in the middle between them and let both go at once "
           "(VBT 61).",
           "Close gently."],
    targets=["dx:gita-restless-mind", "dx:gk-viksepa"], stage="intermediate", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY,
              {"text": "The 'holding back' in VBT 62 is said of awareness (cit) not going on to another object; it is "
                       "not a holding of the breath.",
               "cites": vbt(62)},
              W_VBT_146],
    safety_tier="gentle",
    tier_reason="Attending to the gap between one object and the next; " + GENTLE_NO_BODY + ". Marked intermediate "
                "because the gap is subtle, not because it is risky.",
    cites=vbt(61, 62))

add(id="px:vbt-watching-a-desire-arise-96",
    name="Watching a desire as it arises (VBT 96)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-71"], tradition="lin:trika",
    summary="VBT 96: observe (avalokya) a desire (icchā) that has suddenly arisen, and bring it to rest (śamaṃ nayet); "
            "the verse says it dissolves right there, from where it arose.",
    steps=["Sit comfortably, or simply pause where you are.",
           "When a desire (icchā) arises suddenly, notice it as it arises (VBT 96).",
           "Look at it (avalokya) (VBT 96).",
           "Bring it to rest (śamaṃ nayet); the verse says it dissolves right where it arose (VBT 96).",
           "Close gently."],
    targets=["dx:klesa-raga", "dx:gita-kama-krodha", "dx:katha-outward-senses", "dx:gk-viksepa"],
    stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY,
              {"text": "VBT 98 speaks of an arisen desire differently: it asks that the mind be placed on it with the "
                       "thought that it is the self. That verse is not part of these steps.",
               "cites": vbt(98)}],
    safety_tier="gentle",
    tier_reason="Noticing a desire and letting it settle; " + GENTLE_NO_BODY + ". VBT 97–98 are kept out (see "
                "px:vbt-desire-as-the-self-97-98).",
    cites=vbt(96))

add(id="px:vbt-unstirred-amid-the-passions-101",
    name="Keeping the understanding unstirred amid desire and anger (VBT 101)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-76"], tradition="lin:trika",
    summary="VBT 101: in the sphere of desire (kāma), anger (krodha), greed (lobha), delusion (moha), pride (mada) and "
            "envy (mātsarya), make the understanding (buddhi) unagitated (nistimita); the verse says that that reality "
            "(tat tattva) remains.",
    steps=["Sit comfortably, or pause where you are.",
           "When desire, anger, greed, delusion, pride or envy is present, notice it: these are the six the verse names "
           "(VBT 101).",
           "Keep the understanding (buddhi) still and unstirred (nistimita) in its presence (VBT 101).",
           "Stay with what remains; the verse says 'that reality remains' (VBT 101).",
           "Close gently."],
    targets=["dx:gita-kama-krodha", "dx:gita-anger-chain", "dx:gita-asuri-sampad"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY, W_VBT_146],
    safety_tier="gentle",
    tier_reason="Holding the understanding steady while a passion is present; " + GENTLE_NO_BODY + ".",
    cites=vbt(101))

add(id="px:vbt-neither-attachment-nor-aversion-125-126",
    name="Neither attachment nor aversion (VBT 125–126)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-99", "prc:vbt-dharana-100"], tradition="lin:trika",
    summary="VBT 126: do not cultivate aversion (dveṣa) anywhere, and do not cultivate attachment (rāga) anywhere; the "
            "verse says that when one is freed from attachment and aversion, Brahman moves in the middle. VBT 125: "
            "knowing that, because Brahman is complete (paripūrṇa), one is the same toward enemy and friend and in "
            "honour and dishonour, one would be happy. The Yoga Sūtra names the same pair among the afflictions (kleśa): "
            "attachment rests on pleasure, aversion on pain (YS 2.3, 2.7–2.8); the tantra's reason for letting them go is Brahman's "
            "completeness.",
    steps=["Sit comfortably.",
           "Notice where attachment (rāga) is pulling and where aversion (dveṣa) is pushing.",
           "Do not cultivate either: the verse says not to cultivate aversion anywhere, nor attachment anywhere "
           "(VBT 126).",
           "Reflect, as the verse puts it, on being the same toward enemy and friend, and in honour and dishonour, "
           "because Brahman is complete (VBT 125).",
           "Close gently."],
    targets=["dx:klesa-raga", "dx:klesa-dvesa"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY],
    safety_tier="gentle",
    tier_reason="A reflection on not feeding attachment or aversion; " + GENTLE_NO_BODY + ".",
    cites=vbt(125, 126) + ys("2.3", "2.7", "2.8"))

add(id="px:vbt-wherever-the-mind-goes-116",
    name="Wherever the mind goes (VBT 116–117)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-90", "prc:vbt-dharana-91"], tradition="lin:trika",
    summary="VBT 116: wherever the mind goes, outside or within, there is the state of Śiva (śiva-avasthā), since he is "
            "all-pervading; the verse asks, 'where will it go?' VBT 117: wherever the consciousness of the "
            "all-pervading Lord shows itself through the senses, it has only that as its nature. The Gītā's advice "
            "for the wandering mind is different: restrain it and bring it back from wherever it goes (BhG 6.26); the "
            "tantra instead sees the all-pervading one wherever it goes.",
    steps=["Sit comfortably and let the mind move.",
           "Notice where it goes, outside or within (VBT 116).",
           "Wherever it has gone, regard that as the state of Śiva (śiva-avasthā), the all-pervading (VBT 116).",
           "Ask, as the verse does: where else could it go? (VBT 116)",
           "Close gently."],
    targets=["dx:gita-restless-mind"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY, W_VBT_146],
    safety_tier="gentle",
    tier_reason="A way of seeing the mind's movement, in the tantra's Śaiva terms; " + GENTLE_NO_BODY + ".",
    cites=vbt(116, 117) + bg("6.26"))

add(id="px:vbt-letting-go-where-the-mind-goes-129",
    name="Letting go wherever the mind goes (VBT 129)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-103"], tradition="lin:trika",
    summary="VBT 129: wherever the mind goes, let go of that very thing at that very moment, by the mind itself, by not "
            "letting it stay (anavasthiti); the verse says one then becomes waveless (nistaraṅga).",
    steps=["Sit comfortably.",
           "Notice where the mind goes (VBT 129).",
           "Let go of that very thing at that moment, with the mind itself, not letting it settle there (VBT 129).",
           "Do the same with the next thing the mind goes to (VBT 129: 'wherever the mind goes').",
           "Close gently."],
    targets=["dx:gita-restless-mind", "dx:gk-viksepa"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_VBT_SECRECY,
              {"text": "The verse says the letting go is done 'by the mind itself' (tenaiva) (VBT 129).",
               "cites": vbt(129)}],
    safety_tier="gentle",
    tier_reason="Letting each object go as the mind reaches it; " + GENTLE_NO_BODY + ".",
    cites=vbt(129))

# ======== vedic-yogic: Vijñāna Bhairava — not gentle (summary only)
add(id="px:vbt-desire-as-the-self-97-98",
    name="Taking an arisen desire as the self (VBT 97–98)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-72", "prc:vbt-dharana-73"], tradition="lin:trika",
    summary="VBT 97: contemplate 'when no desire or knowledge of mine has arisen, who am I then? In truth I am that', "
            "and become absorbed in it. VBT 98: when a desire or a cognition has arisen, place the mind on it with the "
            "thought that it is the self (ātma-buddhi), with the mind on nothing else; the verse says the seeing of "
            "the meaning of reality follows.",
    steps=[], targets=[], stage="intermediate", duration=NONE_DUR,
    warnings=[W_VBT_SECRECY],
    safety_tier="needs-teacher",
    tier_reason="VBT 98 asks that an arisen desire be taken as the self; outside the tantra's non-dual teaching this can "
                "be heard as licence to follow desire. VBT 97 rests on the same doctrine. Left to a teacher; VBT 96 "
                "(bringing a desire to rest) is the gentle entry.",
    cites=vbt(97, 98))

add(id="px:vbt-body-burnt-by-the-fire-of-time-52-53",
    name="The body and the world burnt by the fire of time (VBT 52–53)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-28", "prc:vbt-dharana-29"], tradition="lin:trika",
    summary="VBT 52: contemplate one's own 'city' (the body) as burnt by the fire of time (kālāgni) risen from the "
            "place of time; the verse says an appearance of peace follows at the end. VBT 53: in the same way, "
            "meditate by imagination on the whole world as burnt.",
    steps=[], targets=[], stage="advanced", duration=NONE_DUR,
    warnings=[W_VBT_SECRECY],
    safety_tier="never-recommend",
    tier_reason="A visualisation of one's own body burning. The layer keeps visualisation of burning, death and decay "
                "out of the gentle tier and puts imagery of one's own body's destruction with the death and foulness "
                "contemplations (px:maranasati-vism-8, px:asubha-bhavana-vism-6): never recommended.",
    cites=vbt(52, 53))

add(id="px:vbt-looking-down-into-a-well-115",
    name="Looking down into a well or deep pit (VBT 115)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-89"], tradition="lin:trika",
    summary="VBT 115: standing above a well or other great pit, look down into it; the verse says that for one whose "
            "understanding is free of thought-constructs, dissolution of the mind (citta-laya) comes clearly and "
            "quickly.",
    steps=[], targets=[], stage="advanced", duration=NONE_DUR,
    warnings=[W_VBT_SECRECY],
    safety_tier="never-recommend",
    tier_reason="Standing at the edge of a drop and looking down carries a risk of falling; the product never guides "
                "practice at heights.",
    cites=vbt(115))

add(id="px:vbt-fixed-gaze-76-80-84",
    name="Fixed and unbroken gazing (VBT 76, 80, 84)",
    lens="vedic-yogic", ontology_refs=["prc:vbt-dharana-52", "prc:vbt-dharana-56", "prc:vbt-dharana-60"],
    tradition="lin:trika",
    summary="VBT 76: when space is made variegated by the light of the sun, a lamp or the like, set the gaze right "
            "there; the verse says one's own form shines. VBT 80: fix a rigid gaze on some gross object, then quickly "
            "make the mind supportless. VBT 84: look at the spotless sky with an unbroken gaze and become still.",
    steps=[], targets=[], stage="advanced", duration=NONE_DUR,
    warnings=[W_VBT_SECRECY],
    safety_tier="needs-teacher",
    tier_reason="Fixed, rigid or unbroken gazing, in 76 and 84 at sunlit space or the open sky, where the eyes may turn "
                "toward the sun. The product does not guide gazing at the sun or a strained, unblinking gaze; left to "
                "a teacher.",
    cites=vbt(76, 80, 84))

# ======== vedic-yogic: Yoga Sūtra with Vyāsa — gentle
add(id="px:vitaraga-citta-ys-1-37",
    name="The mind on one who is free of passion (YS 1.37)",
    lens="vedic-yogic", ontology_refs=["prc:vitaraga-visaya-citta"], tradition="lin:patanjala-yoga",
    summary="YS 1.37: or the mind [is steadied] having as its object one who is free of passion (vīta-rāga). Vyāsa: "
            "the yogin's mind, coloured by having the mind of one free of passion as its support (ālambana), gains a "
            "footing of steadiness. It is one of the alternatives (marked 'or', vā) the sūtra gives for steadying "
            "the mind, after practice on a single principle against the distractions (1.30–1.32).",
    steps=["Sit comfortably.",
           "Bring to mind one who is free of passion (vīta-rāga). The sūtra names no one; take one your own tradition "
           "holds to be so (YS 1.37).",
           "Let the mind rest on that one's mind, free of passion, as its support (ālambana) (Vyāsa on 1.37).",
           "When the mind goes to other things, set it again on that support (Vyāsa on 1.32).",
           "Close gently."],
    targets=["dx:antaraya-avirati", "dx:klesa-raga"], stage="all", duration=DEFAULT_DUR,
    warnings=[{"text": "The sūtra and Vyāsa name no person; the product does not choose one for you (YS 1.37 with "
                       "Vyāsa).",
               "cites": ys("1.37") + yb("1.37")},
              W_YS_LONG],
    safety_tier="gentle",
    tier_reason="Resting the mind on the thought of one free of passion; " + GENTLE_NO_BODY + ".",
    cites=ys("1.37") + yb("1.37") + ys("1.30", "1.31", "1.32") + yb("1.32"))

add(id="px:yathabhimata-dhyana-ys-1-39",
    name="Meditation on whatever is agreeable (YS 1.39)",
    lens="vedic-yogic", ontology_refs=["prc:yathabhimata-dhyana"], tradition="lin:patanjala-yoga",
    summary="YS 1.39: or [the mind is steadied] by meditation (dhyāna) on whatever is agreeable (yathābhimata). "
            "Vyāsa: one should meditate on just what is agreeable; the mind, having gained steadiness there, gains a "
            "footing of steadiness in other objects too.",
    steps=["Sit comfortably.",
           "Choose one object that is agreeable to you (yathābhimata) (YS 1.39).",
           "Meditate on just that (Vyāsa on 1.39).",
           "When the mind goes to other things, set it again on the one object (Vyāsa on 1.32).",
           "Close gently; Vyāsa says steadiness gained on one object carries to others (Vyāsa on 1.39)."],
    targets=["dx:antaraya-anavasthitatva", "dx:antaraya-alabdha-bhumikatva"], stage="all", duration=DEFAULT_DUR,
    warnings=[{"text": "Dispassion, the partner of practice (YS 1.12), is freedom from thirst for objects seen or "
                       "heard of (YS 1.15 with Vyāsa); an object that you thirst for does not suit this practice.",
               "cites": ys("1.12", "1.15") + yb("1.15")},
              W_YS_LONG],
    safety_tier="gentle",
    tier_reason="Resting the mind on one agreeable object and bringing it back; " + GENTLE_NO_BODY + ".",
    cites=ys("1.39") + yb("1.39") + yb("1.32"))

# ======== vedic-yogic: Yoga Sūtra — not gentle
add(id="px:pranava-japa-ys-1-27-29",
    name="Repetition of Oṃ and contemplation of its meaning (YS 1.27–1.29)",
    lens="vedic-yogic", ontology_refs=["prc:pranava-japa", "prc:isvara-pranidhana"], tradition="lin:patanjala-yoga",
    summary="YS 1.27: the designator of Īśvara is the praṇava (Oṃ). 1.28: its repetition (japa) and the contemplation "
            "of its meaning. 1.29: from that comes the realization of the inward-turned consciousness and the absence "
            "of the obstacles (antarāya). Vyāsa: for the yogin who repeats the praṇava and contemplates Īśvara, whom "
            "it denotes, the mind becomes one-pointed.",
    steps=[],
    targets=["dx:antaraya-styana", "dx:antaraya-samsaya", "dx:antaraya-pramada", "dx:antaraya-alasya",
             "dx:antaraya-avirati", "dx:antaraya-bhranti-darsana", "dx:antaraya-alabdha-bhumikatva",
             "dx:antaraya-anavasthitatva"],
    stage="intermediate", duration=NONE_DUR,
    warnings=[{"text": "Nearest general caution in the Upaniṣadic family (the sūtra gives none): unless taught by "
                       "another there is no way to this understanding; it is not reached by reasoning.",
               "cites": ["tea:katha-upanisad:1.2.8", "tea:katha-upanisad:1.2.9"]}],
    safety_tier="needs-teacher",
    tier_reason="A mantra practice of devotion to Īśvara. The layer leaves mantra repetition to a teacher (as for Oṃ in "
                "px:omkara-upasana-mau-8-12 and the note in px:ekatattva-abhyasa-ys-1-32). The text gives no danger; "
                "the tier can move to gentle if that policy changes.",
    cites=ys("1.27", "1.28", "1.29") + yb("1.28"))

# ======== vedic-yogic: Bhagavad Gītā 17 — gentle
add(id="px:speech-that-does-not-agitate-bg-17-15",
    name="Speech that does not agitate (BhG 17.15)",
    lens="vedic-yogic", ontology_refs=["prc:threefold-tapas"], tradition="lin:epic-teaching",
    summary="BhG 17.15: speech that causes no agitation (anudvega-kara), that is true (satya), pleasant and beneficial "
            "(priya-hita), and the practice of recitation (svādhyāya-abhyasana) are called austerity of speech. "
            "BhG 17.17: this threefold austerity, practised with the highest faith by people who do not desire its "
            "fruit, is called sāttvic.",
    steps=["Before you speak, check the words against the marks the Gītā gives (BhG 17.15).",
           "Will they cause no agitation (anudvega-kara) in the one who hears? (BhG 17.15)",
           "Are they true, pleasant and beneficial (satya, priya, hita)? (BhG 17.15)",
           "Speak what meets these marks (BhG 17.15).",
           "Once a day, spend a few minutes reciting a text you hold sacred (svādhyāya-abhyasana) (BhG 17.15).",
           "Do it without looking for a reward (BhG 17.17)."],
    targets=["dx:gita-asuri-sampad"], stage="all", duration=ALLDAY_DUR("all speech"),
    warnings=[{"text": "The Gītā calls austerity performed out of a deluded notion, with torment of oneself, or to ruin "
                       "another, tāmasic (BhG 17.19).",
               "cites": bg("17.19")},
              {"text": "Austerity performed to gain respect, honour and reverence, or with hypocrisy, is called "
                       "rājasic, unstable and impermanent (BhG 17.18).",
               "cites": bg("17.18")},
              {"text": "The Gītā's austerity of the body (17.14) includes celibacy; it belongs to other tiers and is not "
                       "part of these steps.",
               "cites": bg("17.14")}],
    safety_tier="gentle",
    tier_reason="Care in speech and a short daily recitation; " + GENTLE_NO_BODY + ". The Gītā calls it austerity "
                "(tapas) of speech, but nothing in it strains the body.",
    cites=bg("17.15", "17.17"))

# ======== ascetic-buddhist: Dhammapada — gentle
add(id="px:appamada-dhp-21-27",
    name="Heedfulness (appamāda, Dhp 21–27)",
    lens="ascetic-buddhist", ontology_refs=["prc:appamada"], tradition="lin:early-buddhism",
    summary="Dhp 21: heedfulness (appamāda) is the path to the deathless; heedlessness (pamāda) the path to death. "
            "Dhp 25: by effort (uṭṭhāna), heedfulness, restraint (saṃyama) and self-control (dama), the wise one "
            "should make an island (dīpa) that no flood can overwhelm. Dhp 26: the wise guard heedfulness like the "
            "best wealth. Dhp 27: do not give yourselves to heedlessness, nor to intimacy with delight in sense "
            "pleasures.",
    steps=["Sit comfortably for a few minutes, at the start or the end of the day.",
           "Recall the verse: heedfulness is the path to the deathless (Dhp 21).",
           "Go through the four things the verse names, one at a time: effort (uṭṭhāna), heedfulness (appamāda), "
           "restraint (saṃyama), self-control (dama). For each, notice one place in your day where it is needed "
           "(Dhp 25).",
           "Guard heedfulness as you would guard your best wealth (Dhp 26).",
           "Close gently."],
    targets=["dx:pamada"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_DHP_GRADUAL,
              {"text": "You yourselves must make the effort; the Tathāgatas only point the way (Dhp 276).",
               "cites": dhp(276)}],
    safety_tier="gentle",
    tier_reason="A short daily reflection on heedfulness; " + GENTLE_NO_BODY + ".",
    cites=dhp(21, 25, 26, 27))

add(id="px:guarding-the-mind-dhp-33-36",
    name="Guarding the mind (Dhp 33–36)",
    lens="ascetic-buddhist", ontology_refs=["prc:citta-rakkha", "prc:citta-damatha"], tradition="lin:early-buddhism",
    summary="Dhp 33: the mind is quivering and unsteady, hard to guard and hard to restrain; the discerning one makes "
            "it straight, as a fletcher straightens an arrow. Dhp 35: it is hard to hold back, swift, alighting where "
            "it wishes; taming it is good, and a tamed mind brings happiness. Dhp 36: it is very hard to see, very "
            "subtle, alighting where it wishes; the wise one should guard the mind (cittaṃ rakkhetha); a guarded mind "
            "brings happiness.",
    steps=["Sit comfortably.",
           "Watch the mind: notice how it quivers and alights where it wishes (Dhp 33, 35).",
           "Each time it alights on something, notice where it has gone (Dhp 35–36).",
           "Guard it (Dhp 36), and set it straight again, as a fletcher straightens an arrow (Dhp 33).",
           "Close gently."],
    targets=["dx:citta-vikkhitta", "dx:nivarana-uddhacca-kukkucca", "dx:fetter-uddhacca"], stage="all",
    duration=DEFAULT_DUR,
    warnings=[W_DHP_GRADUAL,
              {"text": "The chapter goes on to a verse on the body lying discarded on the earth (Dhp 41); that "
                       "reflection on the body's end is not part of these steps.",
               "cites": dhp(41)}],
    safety_tier="gentle",
    tier_reason="Watching and guarding the mind; " + GENTLE_NO_BODY + ". The chapter's verse on the body's end is "
                "left out.",
    cites=dhp(33, 35, 36))

add(id="px:not-harbouring-the-grievance-dhp-3-5",
    name="Not harbouring the grievance (Dhp 3–5)",
    lens="ascetic-buddhist", ontology_refs=[], tradition="lin:early-buddhism",
    summary="Dhp 3–4: 'He abused me, he struck me, he defeated me, he robbed me': in those who harbour (upanayhanti) "
            "such thoughts, enmity (vera) is not stilled; in those who do not harbour them, it is stilled. Dhp 5: "
            "enmities are never stilled in this world by enmity; they are stilled by non-enmity (avera). This is an "
            "ancient, perennial dhamma.",
    steps=["Sit comfortably.",
           "Notice when a grievance repeats itself in the form the verse gives: 'he abused me, he struck me, he "
           "defeated me, he robbed me' (Dhp 3).",
           "See that it is being harboured (upanayhati): held and gone over again (Dhp 3).",
           "Recall the verse: in those who do not harbour such thoughts, enmity is stilled (Dhp 4).",
           "Recall: enmity is never stilled by enmity; it is stilled by non-enmity (Dhp 5).",
           "Close gently."],
    targets=["dx:nivarana-byapada", "dx:root-dosa", "dx:fetter-patigha"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_DHP_GRADUAL,
              {"text": "The Visuddhimagga (a later Theravāda manual) advises that if resentment rises when the mind "
                       "turns to one who did wrong, one should turn first to loving-kindness toward an easier person, "
                       "and only then come back (Vism IX p.298).",
               "cites": vism("9.p298")}],
    safety_tier="gentle",
    tier_reason="A reflection on one's own harbouring of a grievance; " + GENTLE_NO_BODY + ". It is not advice to "
                "stay in, or keep silent about, ongoing harm: a reading that mentions abuse is stopped by the safety "
                "screen before any practice is chosen (SAFETY.md).",
    cites=dhp(3, 4, 5))

add(id="px:restraint-of-body-speech-mind-dhp-231-234",
    name="Guarding body, speech and mind against agitation (Dhp 231–234)",
    lens="ascetic-buddhist", ontology_refs=[], tradition="lin:early-buddhism",
    summary="Dhp 231–233: guard against agitation (pakopa) of the body, of speech and of the mind; be restrained in "
            "each; having abandoned bad conduct of body, speech and mind, practise good conduct in each. Dhp 234: the "
            "steadfast who are restrained in body, in speech and in mind are well restrained. Dhp 222: whoever holds "
            "back arisen anger like a swerving chariot, that one I call a charioteer. Dhp 223: conquer anger by "
            "non-anger.",
    steps=["Through the day, notice when body, speech or mind is stirred up (pakopa) (Dhp 231–233).",
           "When anger has arisen, hold it back, as a charioteer checks a swerving chariot (Dhp 222).",
           "Give speech special care: guard against agitation of speech and practise good conduct in speech "
           "(Dhp 232).",
           "At the end of the day, sit comfortably for a few minutes and recall one such moment: was it body, speech "
           "or mind? Set good conduct of that kind against it (Dhp 231–233).",
           "Close with the verse: those restrained in body, speech and mind are well restrained (Dhp 234)."],
    targets=["dx:root-dosa", "dx:nivarana-byapada", "dx:fetter-patigha"], stage="all",
    duration=ALLDAY_DUR("body, speech and mind through the day"),
    warnings=[W_DHP_GRADUAL,
              {"text": "Do not speak harshly to anyone; those addressed may answer back, and quarrelsome talk is "
                       "painful (Dhp 133).",
               "cites": dhp(133)}],
    safety_tier="gentle",
    tier_reason="Noticing and restraining agitation, with a short review; " + GENTLE_NO_BODY + ".",
    cites=dhp(231, 232, 233, 234, 222, 223))

add(id="px:own-deeds-not-others-faults-dhp-50-252",
    name="Looking at one's own deeds, not others' faults (Dhp 50, 252–253)",
    lens="ascetic-buddhist", ontology_refs=[], tradition="lin:early-buddhism",
    summary="Dhp 50: one should not look at the faults of others, nor at what others have done and left undone; one "
            "should look at one's own deeds, done and undone. Dhp 252: the faults of others are easy to see, one's own "
            "are hard to see. Dhp 253: for one who looks at others' faults, always taking offence (ujjhānasaññī), the "
            "taints (āsava) increase.",
    steps=["Through the day, notice when the mind goes to others' faults, or to what others did or left undone "
           "(Dhp 50).",
           "When it does, turn instead to your own deeds, done and undone (Dhp 50).",
           "At the end of the day, sit comfortably for a few minutes and look at your own deeds, done and left undone "
           "(Dhp 50).",
           "Recall: others' faults are easy to see, one's own are hard to see (Dhp 252).",
           "Close gently."],
    targets=["dx:carita-dosa"], stage="all", duration=ALLDAY_DUR("the whole day"),
    warnings=[W_DHP_GRADUAL,
              {"text": "One should first establish oneself in what is suitable, and only then instruct others "
                       "(Dhp 158).",
               "cites": dhp(158)}],
    safety_tier="gentle",
    tier_reason="Turning attention from others' faults to one's own conduct; " + GENTLE_NO_BODY + ".",
    cites=dhp(50, 252, 253))

# ======== ascetic-buddhist: Visuddhimagga IX — gentle
add(id="px:recalling-the-good-in-one-who-wronged-vism-9",
    name="Recalling the good in one who did you wrong (Vism IX)",
    lens="ascetic-buddhist", ontology_refs=["prc:patigha-vinodana-vism"], tradition="lin:theravada",
    summary="Vism IX p.298: if resentment arises when loving-kindness is turned toward one who did wrong, the meditator "
            "goes back to loving-kindness toward one of the earlier persons and then returns; if it does not subside, "
            "the Visuddhimagga gives further means (p.298–306). One is to recall whatever in that person is calm: in "
            "one only the bodily conduct is calm, in another only the speech, in another only the mind; ignoring the "
            "rest, one recalls only that (p.299–300). Another is to reflect on the ownership of deeds (kamma), one's "
            "own and the other's: 'you are the owner of your kamma, heir to your kamma' (p.301).",
    steps=["Sit comfortably. Begin with loving-kindness toward yourself: 'may I be happy and free from suffering' "
           "(Vism IX p.296).",
           "Bring to mind the person you resent. If resentment rises strongly, go back to loving-kindness toward "
           "yourself or a dear person, then return (IX p.298).",
           "Recall one thing in that person that is calm: their conduct, their speech, or their mind. Leave the rest "
           "aside and dwell on that one calm quality (IX p.299–300).",
           "Reflect on the ownership of deeds: 'I am the owner of my deeds, heir to my deeds'; anger, too, bears its "
           "own fruit (IX p.301).",
           "Close gently."],
    targets=["dx:nivarana-byapada", "dx:root-dosa", "dx:fetter-patigha", "dx:carita-dosa"], stage="all",
    duration=DEFAULT_DUR,
    warnings=[{"text": "Do not begin with a disliked or hostile person; begin with yourself (Vism IX p.296).",
               "cites": vism("9.p296", "9.p296/2")},
              {"text": "The Visuddhimagga's further means include stories of great bodily harm borne without anger and "
                       "an analysis of the body into its parts; they are not part of these steps (IX p.302–306).",
               "cites": vism("9.p302/2", "9.p306")},
              {"text": "Loving-kindness has a near enemy, lust (rāga), which resembles it and must be guarded against, "
                       "and a far enemy, ill will (IX p.319).",
               "cites": vism("9.p319")}],
    safety_tier="gentle",
    tier_reason="Recalling another person's calm conduct and reflecting on ownership of deeds; " + GENTLE_NO_BODY +
                ". The Visuddhimagga's graphic stories and body analysis are left out. It is not advice to stay in "
                "ongoing harm: a reading that mentions abuse is stopped by the safety screen (SAFETY.md).",
    cites=vism("9.p296/2", "9.p298", "9.p299/2", "9.p300", "9.p301/2"))

# ======== ascetic-jain: Tattvārtha Sūtra — gentle
add(id="px:anitya-anupreksa-ts-9-7",
    name="Reflection on impermanence (anitya-anuprekṣā, TS 9.7)",
    lens="ascetic-jain", ontology_refs=["prc:anupreksa"], tradition="lin:jainism",
    summary="TS 9.7 names impermanence (anitya) first among the twelve reflections (anuprekṣā); the activity is "
            "anucintana, thinking on a theme again and again. TS 9.2 counts the reflections among the means of "
            "stopping karmic inflow (saṃvara). TS 5.30 states that what exists is joined with origination (utpāda), "
            "cessation (vyaya) and persistence (dhrauvya): the sūtra does not teach that nothing persists.",
    steps=["Sit comfortably.",
           "Bring to mind something you hold on to: a possession, a situation, a pleasure.",
           "Reflect on its impermanence (anitya): it has arisen, and it will cease (TS 9.7; 5.30).",
           "Return to the thought again and again; that repeated thinking (anucintana) is what the sūtra calls a "
           "reflection (TS 9.7).",
           "Close gently."],
    targets=["dx:kasaya-lobha", "dx:jain-arta-dhyana"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_TS_ARTA,
              {"text": "This reflection is on impermanence, not on death. The sūtra's reflection on 'no refuge' "
                       "(aśaraṇa) is a separate one and is not part of these steps (TS 9.7).",
               "cites": ts("9.7")}],
    safety_tier="gentle",
    tier_reason="A single short reflection from the twelve; " + GENTLE_NO_BODY + ".",
    cites=ts("9.7", "9.2", "5.30"))

add(id="px:asrava-samvara-anupreksa-ts-9-7",
    name="Reflection on inflow and stopping (āsrava- and saṃvara-anuprekṣā, TS 9.7)",
    lens="ascetic-jain", ontology_refs=["prc:anupreksa"], tradition="lin:jainism",
    summary="TS 9.7 names inflow (āsrava) and stopping (saṃvara) among the twelve reflections. The sūtra defines them: "
            "activity (yoga) is the action of body, speech and mind (6.1), and that activity is inflow (6.2); the "
            "inflow of one with passions (sakaṣāya) is sāmparāyika, 'pertaining to the passage to another life' (6.4), and because it "
            "has passions the soul takes in the matter fit to become karma: that is bondage (8.2). Stopping "
            "(saṃvara) is the stopping of inflow (9.1); it comes about through the controls (gupti), the carefulnesses "
            "(samiti), virtue (dharma), the reflections (anuprekṣā), the conquest of hardships (parīṣaha-jaya) and "
            "conduct (cāritra) (9.2).",
    steps=["Sit comfortably.",
           "Reflect that every action of body, speech and mind is activity (yoga), and that activity is inflow "
           "(āsrava) (TS 6.1–6.2).",
           "Reflect that it is inflow joined with the passions (kaṣāya), such as anger, pride, deceit and greed, that "
           "binds (TS 6.4; 8.2; 8.9).",
           "Reflect on stopping (saṃvara): the stopping of inflow, which comes about through control, carefulness, "
           "virtue and reflection, among the means the sūtra names (TS 9.1–9.2).",
           "Close gently."],
    targets=["dx:kasaya-krodha", "dx:kasaya-mana", "dx:kasaya-maya", "dx:kasaya-lobha", "dx:jain-avirati",
             "dx:jain-pramada"],
    stage="all", duration=DEFAULT_DUR,
    warnings=[W_TS_ARTA,
              {"text": "The sūtra's means of stopping also include the conquest of hardships (parīṣaha-jaya), which "
                       "belongs to the ascetic life; it is not part of these steps (TS 9.2).",
               "cites": ts("9.2")}],
    safety_tier="gentle",
    tier_reason="A doctrinal reflection on the sūtra's own definitions; " + GENTLE_NO_BODY + ".",
    cites=ts("9.7", "6.1", "6.2", "6.4", "8.2", "8.9", "9.1", "9.2"))

add(id="px:supports-of-truthful-speech-ts-7-5",
    name="The five supports of truthful speech (TS 7.5)",
    lens="ascetic-jain", ontology_refs=["prc:vow-bhavanas-practice", "prc:guptis-samitis"], tradition="lin:jainism",
    summary="TS 7.3: for the steadiness of each vow there are five contemplations (bhāvanā). TS 7.5: for truthfulness "
            "they are giving up anger (krodha), greed (lobha), fear (bhīrutva) and laughter (hāsya), and speaking in "
            "conformity (anuvīci-bhāṣaṇa). TS 9.4–9.5 name, among the means of stopping inflow, control (gupti), the "
            "proper restraint of activity, and care in speaking (bhāṣā-samiti).",
    steps=["Through the day, before you speak, notice whether anger, greed, fear or joking is pushing the words "
           "(TS 7.5).",
           "If one of them is, give it up before you speak (TS 7.5).",
           "Speak with care and in conformity (anuvīci-bhāṣaṇa), as the sūtra puts it (TS 7.5; 9.5: bhāṣā-samiti).",
           "Hold back speech that is not proper; the sūtra calls proper restraint of activity control (gupti) "
           "(TS 9.4).",
           "At the end of the day, sit comfortably for a few minutes and recall one moment of speech, and which of "
           "the four was at work (TS 7.5)."],
    targets=["dx:kasaya-krodha", "dx:kasaya-lobha", "dx:jain-nokasaya"], stage="all",
    duration=ALLDAY_DUR("all speech"),
    warnings=[W_TS_VOW("truthfulness"), W_TS_ARTA],
    safety_tier="gentle",
    tier_reason="Care in speech with a short daily review; " + GENTLE_NO_BODY + ". It supports the vow of "
                "truthfulness without taking the vow.",
    cites=ts("7.3", "7.5", "9.4", "9.5"))

add(id="px:letting-go-of-liking-and-disliking-ts-7-8",
    name="Letting go of attachment and aversion toward sense objects (TS 7.8)",
    lens="ascetic-jain", ontology_refs=["prc:vow-bhavanas-practice"], tradition="lin:jainism",
    summary="TS 7.8: for non-possession the five contemplations are giving up attachment (rāga) and aversion (dveṣa) "
            "toward the pleasant and unpleasant objects of the senses (manojña-amanojña-indriya-viṣaya); the "
            "commentaries count one for each sense. TS 7.3: such contemplations are for the steadiness of the vows.",
    steps=["Sit comfortably.",
           "Take the senses one at a time: sight, hearing, smell, taste, touch.",
           "For each, bring to mind something pleasant (manojña) to that sense and notice the attachment (rāga) toward "
           "it; then something unpleasant (amanojña), and notice the aversion (dveṣa) (TS 7.8).",
           "Give up the attachment and the aversion, as the sūtra asks (TS 7.8).",
           "Close gently."],
    targets=["dx:kasaya-lobha", "dx:jain-arta-dhyana"], stage="all", duration=DEFAULT_DUR,
    warnings=[W_TS_VOW("non-possession"), W_TS_ARTA],
    safety_tier="gentle",
    tier_reason="A reflection on liking and disliking, sense by sense; " + GENTLE_NO_BODY + ".",
    cites=ts("7.3", "7.8"))

add(id="px:seeing-harm-in-the-faults-ts-7-9-10",
    name="Seeing the harm in violence and the other faults (TS 7.9–7.10)",
    lens="ascetic-jain", ontology_refs=["prc:samvega-vairagya-reflection"], tradition="lin:jainism",
    summary="TS 7.9: in violence and the rest (the five faults of 7.1: violence, falsehood, stealing, unchastity and "
            "possessiveness) one is to see danger (apāya) and blame (avadya), in this world and the next. TS 7.10: or "
            "one is to see them as only suffering (duḥkha).",
    steps=["Sit comfortably.",
           "Bring to mind one of the faults the sūtra names: harming, falsehood, taking what is not given, or "
           "possessiveness (TS 7.1).",
           "See the danger (apāya) and the blame (avadya) it brings, in this world and the next (TS 7.9).",
           "Or see it simply as suffering (duḥkha) (TS 7.10).",
           "Close gently."],
    targets=["dx:jain-raudra-dhyana", "dx:jain-avirati"], stage="all", duration=DEFAULT_DUR,
    warnings=[{"text": "Reflect on the harm, not on the deed itself: the mind dwelling on harming, lying, stealing or "
                       "guarding what one enjoys is what the sūtra calls cruel dwelling (raudra) (TS 9.35).",
               "cites": ts("9.35")},
              W_TS_ARTA,
              {"text": "The steps name four of the sūtra's five faults; the fifth, unchastity (abrahma), is left out "
                       "(TS 7.1).",
               "cites": ts("7.1")}],
    safety_tier="gentle",
    tier_reason="A reflection on the harm of wrong conduct; " + GENTLE_NO_BODY + ". TS 7.12 (reflecting on the nature "
                "of the body, for dread of rebirth) is not included.",
    cites=ts("7.1", "7.9", "7.10"))

add(id="px:noticing-sorrowful-dwelling-ts-9-30-34",
    name="Noticing sorrowful dwelling (ārta-dhyāna, TS 9.30–9.34)",
    lens="ascetic-jain", ontology_refs=[], tradition="lin:jainism",
    summary="TS 9.28: meditation (dhyāna) is of four kinds: sorrowful (ārta), cruel (raudra), virtuous (dharmya) and "
            "white (śukla); 9.29: the latter two are causes of liberation. TS 9.30–9.33: sorrowful dwelling is the "
            "mind brought back again and again (smṛti-samanvāhāra) to getting away from something disagreeable one is "
            "in contact with; the reverse, for something agreeable; to a feeling (vedanā); and to hankering for "
            "future enjoyment (nidāna). TS 9.34: it belongs to the unrestrained, the partly restrained and the "
            "restrained who are careless.",
    steps=["Sit comfortably, or pause where you are.",
           "Notice when the mind keeps coming back to one thing (TS 9.30: 'continuous bringing to mind').",
           "See which of the four it is: getting away from something disagreeable; keeping or regaining something "
           "agreeable; a painful feeling (vedanā); or longing for a future enjoyment (TS 9.30–9.33).",
           "Name it as the sūtra does: sorrowful dwelling (ārta) (TS 9.28, 9.30).",
           "Turn the mind to one of the reflections the sūtra lists among the means of stopping inflow, such as "
           "impermanence (TS 9.2, 9.7).",
           "Close gently."],
    targets=["dx:jain-arta-dhyana"], stage="all", duration=DEFAULT_DUR,
    warnings=[{"text": "The sūtra ties meditation (dhyāna) proper to one with the best bodily frame, lasting up to "
                       "one muhūrta (TS 9.27); this is noticing and reflection, not that meditation.",
               "cites": ts("9.27")},
              {"text": "The sūtra finds sorrowful dwelling not only in the unrestrained but also in the partly "
                       "restrained and in the restrained who are careless (TS 9.34).",
               "cites": ts("9.34")}],
    safety_tier="gentle",
    tier_reason="Noticing and naming a pattern of mind, then turning to a reflection; " + GENTLE_NO_BODY + ".",
    cites=ts("9.28", "9.29", "9.30", "9.31", "9.32", "9.33", "9.34", "9.2", "9.7"))

# ======== ascetic-jain: Tattvārtha Sūtra — not gentle
add(id="px:asarana-samsara-anupreksa-ts-9-7",
    name="The reflections on no refuge and on the round of births (aśaraṇa, saṃsāra; TS 9.7)",
    lens="ascetic-jain", ontology_refs=["prc:anupreksa"], tradition="lin:jainism",
    summary="TS 9.7 names 'no refuge' (aśaraṇa) and 'the round of births' (saṃsāra) among the twelve reflections; the "
            "sūtra gives only the names.",
    steps=[], targets=[], stage="intermediate", duration=NONE_DUR,
    warnings=[W_TS_ARTA],
    safety_tier="needs-teacher",
    tier_reason="The sūtra gives only the names, and the tradition's own account of these two is not in the verified "
                "texts (the commentaries are not yet verified). 'No refuge' is read in the tradition as helplessness "
                "before death, and death contemplation is outside the gentle tier. Left to a teacher.",
    cites=ts("9.7"))

add(id="px:asuci-anupreksa-ts-9-7",
    name="The reflection on impurity (aśuci-anuprekṣā, TS 9.7)",
    lens="ascetic-jain", ontology_refs=["prc:anupreksa"], tradition="lin:jainism",
    summary="TS 9.7 names impurity (aśuci) among the twelve reflections; the sūtra gives only the name.",
    steps=[], targets=[], stage="intermediate", duration=NONE_DUR,
    warnings=[W_TS_ARTA],
    safety_tier="never-recommend",
    tier_reason="In the tradition this is the reflection on the impurity of the body (the commentaries' reading, not "
                "yet verified here): a repulsiveness contemplation, like px:kayagatasati-32-parts-vism-8 and "
                "px:asubha-bhavana-vism-6, which the layer never recommends.",
    cites=ts("9.7"))

# ======== vedic-yogic: Haṭha Yoga Pradīpikā — not gentle
add(id="px:nadanusandhana-hyp-4-65-102",
    name="Attention to the inner sound (nādānusandhāna, HYP 4.65–4.102)",
    lens="vedic-yogic", ontology_refs=["prc:nadanusandhana"], tradition="lin:hatha-yoga",
    summary="HYP 4.65–4.66: attention to the inner sound (nāda), taught by Gorakṣanātha, is accepted even for the dull "
            "and is held the chief of the ways of absorption (laya). 4.67: seated in muktāsana, having taken up the "
            "śāmbhavī seal (mudrā), one listens with one-pointed mind to the inner sound in the right ear. 4.82: "
            "closing the ears with the hands, one fixes the mind on whatever sound one hears until it is steady. "
            "4.87–4.89: one attends to ever subtler sound; the mind, though delighting, is not to move to anything "
            "else; it becomes steady in the sound and dissolves with it.",
    steps=[], targets=["dx:gita-restless-mind"], stage="intermediate", duration=NONE_DUR,
    warnings=[{"text": "The practice is set in the haṭha sequence: its four stages begin with the piercing of the knot "
                       "of Brahmā (HYP 4.69–4.70).",
               "cites": hyp("4.69", "4.70")},
              {"text": "The method uses the śāmbhavī seal and closing the ears with the hands (HYP 4.67, 4.82).",
               "cites": hyp("4.67", "4.82")},
              {"text": "The Pradīpikā names over-exertion (prayāsa) among the six things that destroy yoga (HYP 1.15).",
               "cites": hyp("1.15")}],
    safety_tier="needs-teacher",
    tier_reason="Uses a seal (śāmbhavī), closing the ears with the hands, and sits within the haṭha sequence of "
                "piercing the knots (4.69–4.70); the text's closing of all the sense-openings (4.68) is restricted. "
                "Body technique and stage-claims leave it to a teacher.",
    cites=hyp("4.65", "4.66", "4.67", "4.82", "4.87", "4.88", "4.89"))


# ---------------------------------------------------------------- repairs to existing entries
W_YB21_TEXT_PREFIX = "Nearest general caution in the Yoga Sūtra family (the sūtra's own passage gives none): Vyāsa says discipline"
REPAIRS = []  # (id, description)


def repair(P):
    by = {p["id"]: p for p in P}
    changed = set()
    # 1. YB 2.1 (restricted: it glosses tapas) made four YS entries unusable. Replace that borrowed caution with the
    #    sūtra's own condition on practice (YS 1.14), or drop it where YS 1.14 is already present.
    for pid in ("px:abhyasa-vairagya-ys-1-12", "px:ekatattva-abhyasa-ys-1-32", "px:maitri-bhavana-ys-1-33",
                "px:pratipaksa-bhavana-ys-2-33"):
        p = by[pid]
        has_114 = any(w["cites"] == ys("1.14") for w in p["warnings"])
        new_w = []
        for w in p["warnings"]:
            if w["cites"] == yb("2.1"):
                assert w["text"].startswith(W_YB21_TEXT_PREFIX), (pid, w["text"])
                if has_114:
                    REPAIRS.append((pid, "dropped the YB 2.1 caution (restricted teaching: it glosses tapas); the entry "
                                         "already carries the YS 1.14 caution"))
                    continue
                new_w.append(copy.deepcopy(W_YS_LONG))
                REPAIRS.append((pid, "replaced the YB 2.1 caution (restricted teaching: it glosses tapas) with the "
                                     "sūtra's own condition on practice, YS 1.14"))
                continue
            if w["cites"] == yb("1.14"):
                REPAIRS.append((pid, "dropped the note 'Vyāsa lists austerity and celibacy among what makes practice "
                                     "firm' (YB 1.14 is restricted, so the note cannot be cited; the steps never "
                                     "included those supports)"))
                continue
            new_w.append(w)
        if new_w != p["warnings"]:
            p["warnings"] = new_w
            changed.add(pid)
    # 2. Fidelity: the anuprekṣā step attributed the commentaries' gloss of anyatva to the sūtra itself.
    p = by["px:anupreksa-ts-9-7"]
    old_step = "Reflect on aloneness (ekatva) and on otherness (anyatva): the self is other than the body (TS 9.7)."
    new_step = ("Reflect on aloneness (ekatva) and on otherness (anyatva), as the sūtra names them (TS 9.7); the "
                "commentaries read otherness as the self being other than the body.")
    if old_step in p["steps"]:
        p["steps"] = [new_step if s == old_step else s for s in p["steps"]]
        old_sum = "otherness (of self and body), impurity (of the body)"
        assert old_sum in p["summary"]
        p["summary"] = p["summary"].replace(old_sum, "otherness, impurity (the commentaries read these as the "
                                                     "otherness of self and body and the impurity of the body)")
        REPAIRS.append(("px:anupreksa-ts-9-7", "step and summary no longer attribute the commentaries' gloss of anyatva "
                                              "(self other than body) and aśuci (of the body) to the sūtra, which gives "
                                              "only the names (teaching note on tea:tattvartha-sutra:9.7)"))
        changed.add("px:anupreksa-ts-9-7")
    return changed


# ---------------------------------------------------------------- validation
NO_DIET = re.compile(r"\b(diet|fast(ing)?|food|eat(ing)?|meal|exercise|āsana|asana|posture|physical training|walk(ing)? meditation)\b", re.I)
DANGER = ("mercury", "metal", "cutting the body", "breath retention", "kumbhaka", "sexual", "fast for", "prolonged fast",
          "fasting for")


def all_cites(e):
    return list(e["cites"]) + [c for w in e["warnings"] for c in w["cites"]]


def validate(P, check_ids):
    errs, notes = [], []
    dx_ids = {d["id"] for d in json.load(open(f"{ROOT}/layers/diagnosis.json", encoding="utf-8"))}
    prc = {p["id"]: p for p in json.load(open(f"{ROOT}/data/practices.json", encoding="utf-8"))}
    lins = {l["id"] for l in json.load(open(f"{ROOT}/data/lineages.json", encoding="utf-8"))}
    restricted_prc = O.restricted_practices()
    ids = [p["id"] for p in P]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids: " + str([k for k, v in Counter(ids).items() if v > 1]))
    by = {p["id"]: p for p in P}
    for pid in check_ids:
        e = by[pid]
        if list(e.keys()) != FIELDS:
            errs.append(f"{pid}: field order {list(e.keys())}")
        if e["lens"] not in ("vedic-yogic", "ascetic-buddhist", "ascetic-jain"):
            errs.append(f"{pid}: lens")
        if e["safety_tier"] not in ("gentle", "needs-teacher", "never-recommend"):
            errs.append(f"{pid}: tier")
        if e["stage"] not in ("beginner", "intermediate", "advanced", "all"):
            errs.append(f"{pid}: stage")
        if e["tradition"] not in lins:
            errs.append(f"{pid}: tradition {e['tradition']} not in lineages")
        for t in e["targets"]:
            if t not in dx_ids:
                errs.append(f"{pid}: target {t} not in diagnosis.json")
        for r in e["ontology_refs"]:
            if r not in prc:
                errs.append(f"{pid}: ontology_ref {r} missing")
            elif r in restricted_prc:
                errs.append(f"{pid}: ontology_ref {r} restricted")
        for c in all_cites(e):
            if not O.citable(c):
                t = O.teaching(c)
                errs.append(f"{pid}: cite {c} not citable ({t and (t['level'], t['restricted'])})")
        if not e["warnings"] or any(not w["cites"] or not w["text"].strip() for w in e["warnings"]):
            errs.append(f"{pid}: warnings missing or uncited")
        if not e["cites"]:
            errs.append(f"{pid}: no cites")
        if e["safety_tier"] == "gentle":
            if not (3 <= len(e["steps"]) <= 6):
                errs.append(f"{pid}: {len(e['steps'])} steps")
            if not e["duration"].get("minutes_per_session"):
                errs.append(f"{pid}: duration")
            if not e["targets"]:
                errs.append(f"{pid}: gentle entry without targets")
            text = " ".join([e["name"], e["summary"]] + e["steps"]).lower()
            hit = [d for d in DANGER if d in text]
            if hit:
                errs.append(f"{pid}: danger words {hit}")
            blob = " ".join([e["name"], e["summary"]] + e["steps"] + [w["text"] for w in e["warnings"]])
            m = NO_DIET.search(blob)
            if m:
                notes.append(f"{pid}: excluded under the no-diet route (matches {m.group(0)!r})")
        else:
            if e["steps"]:
                errs.append(f"{pid}: non-gentle entry has steps")
        hits = claims.scan_fields({k: e[k] for k in ("name", "summary", "steps", "warnings", "tier_reason")})
        for h in hits:
            errs.append(f"{pid}: claims hit {h['category']}: {h['match']!r} in {h['sentence'][:80]!r}")
        if e.get("user_facing") is not True:
            errs.append(f"{pid}: user_facing not true")
    return errs, notes


def main():
    P = json.load(open(PX_PATH, encoding="utf-8"))
    before_usable = O.practices()
    before_gentle = O.gentle_practices()
    existing = {p["id"] for p in P}
    for e in NEW:
        assert e["id"] not in existing, f"id exists already: {e['id']}"
        e["user_facing"] = True
    new_entries = [{k: e[k] for k in FIELDS} for e in NEW]
    changed = repair(P)
    P2 = P + new_entries
    errs, notes = validate(P2, [e["id"] for e in new_entries] + sorted(changed))
    print("new entries:", len(new_entries), "| changed existing:", sorted(changed))
    for pid, d in REPAIRS:
        print("  repair", pid, "-", d)
    print("errors:", len(errs))
    for x in errs:
        print("  ERR", x)
    for x in notes:
        print("  NOTE", x)
    print("tiers of new entries:", Counter((e["lens"], e["safety_tier"]) for e in new_entries))
    if errs:
        sys.exit(1)
    out = json.dumps(P2, indent=1, ensure_ascii=False)
    if "--write" in sys.argv:
        open(PX_PATH, "w", encoding="utf-8").write(out)
        O.reset_caches()
        after_usable = O.practices()
        after_gentle = O.gentle_practices()
        missing = [e["id"] for e in new_entries if e["id"] not in after_usable]
        print("written.")
        print("usable before/after:", len(before_usable), len(after_usable))
        print("gentle usable before/after:", len(before_gentle), len(after_gentle))
        print("gentle usable per lens before:", dict(Counter(v["lens"] for v in before_gentle.values())))
        print("gentle usable per lens after:", dict(Counter(v["lens"] for v in after_gentle.values())))
        print("new entries not loaded by practices():", missing)
        for pid in sorted(changed):
            print("  changed", pid, "usable now:", pid in after_usable, "| gentle:", pid in after_gentle)
    else:
        print("dry run; pass --write to write", PX_PATH)


if __name__ == "__main__":
    main()
