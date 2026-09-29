"""Yoga Sutra + Vyasa entries: klesas, vrttis, antarayas, companions, citta-bhumis, vitarkas, powers as obstacles."""
from common import *

VL = 'vedic-yogic'
G_KLESA = 'the five kleśas (YS 2.3)'
KLESA_STATES = [
    ("prasupta (dormant)", "Present in the mind only as a potency, in seed form; it wakes when its object comes before it.", [YS('2.4'), YB('2.4')]),
    ("tanu (thinned)", "Weakened by cultivating the opposite (pratipakṣa-bhāvanā).", [YS('2.4'), YB('2.4')]),
    ("vicchinna (interrupted)", "Cut off and returning again and again in one form or another: while attachment is at work, anger does not show; attachment at work toward one object is only waiting toward others.", [YS('2.4'), YB('2.4')]),
    ("udāra (active)", "Fully at work: it has found its object.", [YS('2.4'), YB('2.4')]),
    ("dagdha-bīja (burnt seed)", "Vyāsa's fifth condition: in one who has discriminative contemplation (prasaṃkhyāna) the seed is burnt, and even when the object is present it does not sprout again.", [YB('2.4')]),
]
PX_KLESA = [
    ("px:pratipaksa-bhavana-ys-2-33", [YS('2.33'), YB('2.4')]),
    ("px:kriya-yoga-ys-2-1", [YS('2.1'), YS('2.2')]),
    ("px:dhyana-ys-2-11", [YS('2.11'), YB('2.11')]),
]
ENTRIES = []
A = ENTRIES.append

# ---------------- the five klesas ----------------
A(E("dx:klesa-avidya", "Avidyā (not-knowing)", "affliction", G_KLESA, VL,
    ["obs:avidya", "cpt:avidya", "trm:avidya", "obs:fivefold-avidya", "obs:pancaparva-avidya", "obs:five-klesas", "cpt:five-klesas", "trm:klesa"],
    [(LIN_YOGA, "Avidyā is taking the non-eternal, the impure, the painful and what is not the self to be eternal, pure, pleasant and the self (YS 2.5). It is the field (kṣetra) of the other four kleśas, whether they are dormant, thinned, interrupted or active (YS 2.4); Vyāsa adds that all the kleśas are forms of avidyā and wane as avidyā wanes.", [YS('2.3'), YS('2.4'), YS('2.5'), YB('2.4')]),
     (LIN_YOGA, "Avidyā is the cause of the conjunction of seer and seen; when it is absent the conjunction ends, and that ending is the seer's aloneness (kaivalya) (YS 2.24–25).", [YS('2.24'), YS('2.25')]),
     (LIN_YOGA, "Vyāsa on YS 1.8: erroneous cognition (viparyaya) is this avidyā of five parts — the five kleśas, also called darkness, delusion, great delusion, gloom and blind gloom.", [YS('1.8'), YB('1.8')])],
    [("Treating what passes as if it lasts, what is impure as pure, what is painful as pleasant, and what is not the self as the self.",
      ["I was sure this would last forever", "I thought this would finally make me happy for good", "this role is simply who I am"], [YS('2.5')])],
    "Not a lack of information or schooling and not a judgement of intelligence: in YS 2.5 avidyā is a mis-taking about what lasts, what is pure, what is pleasant and what is the self. Not the Buddhist avijjā, which does not assume the real self that the Yoga affirms.",
    eq=[("dx:vrtti-viparyaya", "same-under-standpoint", "Vyāsa (on YS 1.8) calls erroneous cognition 'avidyā of five parts': the same error seen as a modification of mind (vṛtti) and as an affliction (kleśa).", [YB('1.8')]),
        ("dx:fetter-avijja", "partial", "Both name not-seeing as the root of bondage. YS avidyā is the fourfold mis-taking of YS 2.5 and ends in the seer's aloneness; the Theravāda avijjā/moha is blindness of mind and the root of all unwholesome states (Vism XIV), with no self to be uncovered. Theravāda denies the self the Yoga affirms.", [YS('2.5'), VSM(14, 468)]),
        ("dx:root-moha", "partial", "Vism XIV defines moha as blindness of mind that hides the nature of the object; YS avidyā as mis-taking the impermanent, impure, painful and non-self. Similar function, different metaphysics.", [YS('2.5'), VSM(14, 468)]),
        ("dx:jain-mithyadarsana", "partial", "Both stand first among the roots of bondage in their systems (YS 2.3–4; TS 8.1). Jain wrong view is the absence of faith in the reals as the Jain teaching sets them out (TS 1.2); the reals differ.", [YS('2.4'), TS('8.1'), TS('1.2')])],
    px=[("px:viveka-khyati-ys-2-26", [YS('2.26')])] + PX_KLESA))

A(E("dx:klesa-asmita", "Asmitā (I-am-ness)", "affliction", G_KLESA, VL,
    ["obs:asmita", "cpt:asmita", "trm:asmita", "obs:five-klesas"],
    [(LIN_YOGA, "Asmitā is the seeing-power and the power of seeing appearing as if they were one self (YS 2.6). Vyāsa: the puruṣa is the seeing-power, buddhi the power of seeing; their seeming oneness is the kleśa called asmitā; experience depends on it, and when each is known in its own nature there is aloneness. He quotes: 'not seeing the puruṣa as beyond buddhi, distinct in form, conduct and knowledge, one takes buddhi to be the self out of delusion.'", [YS('2.6'), YB('2.6')])],
    [("Taking the mind that thinks, judges and feels — its moods and its knowing — for the one who sees.",
      ["my thoughts are simply me", "when my mind is troubled, I am troubled", "I am whatever my mind concludes"], [YS('2.6'), YB('2.6')])],
    "Not ordinary self-respect or a sense of identity in the social sense: in YS 2.6 it is the seeming oneness of the seer with the instrument of seeing. Not the Buddhist sakkāya-diṭṭhi (which denies any self) and not the Jain māna (pride).",
    states=KLESA_STATES,
    eq=[("dx:fetter-sakkaya-ditthi", "partial", "Both name a false taking of something as self. YS 2.6 confuses the instrument (buddhi) with a real seer that the Yoga affirms; personality view regards any of the five aggregates as self (Vism XVII), and Theravāda affirms no self at all. That denial stands.", [YS('2.6'), VSM(17, 570)]),
        ("dx:fetter-mana", "partial", "Conceit (māna) is haughtiness and self-exaltation (Vism XIV); asmitā is the seeming oneness of seer and seeing. Related in the 'I am' they share, different in definition.", [YS('2.6'), VSM(14, 469)])],
    px=[("px:viveka-khyati-ys-2-26", [YS('2.26')])] + PX_KLESA))

A(E("dx:klesa-raga", "Rāga (attachment)", "affliction", G_KLESA, VL,
    ["obs:raga", "cpt:raga", "trm:raga", "obs:five-klesas"],
    [(LIN_YOGA, "Rāga is what follows upon pleasure (YS 2.7). Vyāsa: in one who has known pleasure, preceded by the memory of pleasure, the greed, thirst and craving (gardha, tṛṣṇā, lobha) for pleasure or for its means — that is rāga.", [YS('2.7'), YB('2.7')])],
    [("Wanting a pleasure again, or the means to it, because it is remembered.",
      ["I keep wanting to go back to that", "I remember how good it felt and I want it again", "I need whatever gets me that feeling"], [YS('2.7'), YB('2.7')]),
     ("Vyāsa: attachment seen toward one object does not mean it is absent toward others; it is at work here and waiting elsewhere.",
      ["as soon as one want is met, another takes its place"], [YB('2.4')])],
    "Not love, affection or enjoyment as such, and not a medical condition: in YS 2.7 it is the pull that follows remembered pleasure. Not identical to the Buddhist lobha or the Jain lobha, which belong to other maps.",
    states=KLESA_STATES,
    eq=[("dx:root-lobha", "partial", "Vyāsa himself glosses rāga with the word lobha (YB 2.7). The Theravāda lobha is a mental factor that grasps its object like bird-lime (Vism XIV), one of three roots, with no self behind it; YS rāga is a kleśa growing in the field of avidyā.", [YB('2.7'), VSM(14, 468)]),
        ("dx:nivarana-kamacchanda", "partial", "Sensual desire as a hindrance is named for what it blocks: the mind's settling on one object (Vism IV). YS rāga covers any remembered pleasure and its means.", [YS('2.7'), VSM(4, 146)]),
        ("dx:kasaya-lobha", "partial", "Jain greed is one of four passions that make the soul take in karmic matter (TS 8.2, 8.9); YS rāga is a kleśa rooted in avidyā. Similar pull, different account of bondage.", [YS('2.7'), TS('8.2'), TS('8.9')]),
        ("dx:gita-kama-krodha", "partial", "The Gītā's desire (kāma) is born of rajas and grows from attachment to objects dwelt on (BhG 2.62, 3.37); YS rāga follows remembered pleasure. Both place desire before anger.", [YS('2.7'), BG('2.62'), BG('3.37')]),
        ("dx:tanha", "partial", "Craving (taṇhā) arises where there is what is dear and agreeable (DN 22); Vyāsa uses the word tṛṣṇā in defining rāga. Different frameworks (kleśa vs origin of suffering).", [YB('2.7'), DN22('19')])],
    px=PX_KLESA))

A(E("dx:klesa-dvesa", "Dveṣa (aversion)", "affliction", G_KLESA, VL,
    ["obs:dvesa", "trm:dvesa", "obs:five-klesas"],
    [(LIN_YOGA, "Dveṣa is what follows upon pain (YS 2.8). Vyāsa: in one who has known pain, preceded by the memory of pain, the resistance, resentment, wish to strike and anger (pratigha, manyu, jighāṃsā, krodha) toward pain or its means — that is dveṣa.", [YS('2.8'), YB('2.8')])],
    [("Pushing against a pain, or whatever brings it, because it is remembered.",
      ["I can't stand anything that reminds me of it", "I want to hit back at whatever hurt me", "I resent them because of what happened"], [YS('2.8'), YB('2.8')])],
    "Not a considered refusal of harm and not a medical condition: in YS 2.8 it is the aversion that follows remembered pain. Not identical to the Buddhist dosa or the Jain krodha.",
    states=KLESA_STATES,
    eq=[("dx:root-dosa", "partial", "Theravāda dosa is ferocity, like a struck snake (Vism XIV); Vyāsa's dveṣa includes resentment, the wish to strike and anger toward remembered pain. Similar, in different maps.", [YB('2.8'), VSM(14, 470)]),
        ("dx:nivarana-byapada", "partial", "Ill will as a hindrance is named for blocking the mind's continuous flow on its object (Vism IV); YS dveṣa is a kleśa following remembered pain.", [YS('2.8'), VSM(4, 146)]),
        ("dx:kasaya-krodha", "partial", "Vyāsa lists krodha within dveṣa; the Jain krodha is one of the four passions with four intensities (TS 8.9). Same word, different system.", [YB('2.8'), TS('8.9')]),
        ("dx:fetter-patigha", "partial", "Resentment (paṭigha) as a fetter binds to the sense sphere until the third path (Vism XXII); Vyāsa uses pratigha in defining dveṣa.", [YB('2.8'), VSM(22, 684)])],
    px=PX_KLESA))

A(E("dx:klesa-abhinivesa", "Abhiniveśa (clinging to life)", "affliction", G_KLESA, VL,
    ["obs:abhinivesa", "trm:abhinivesa", "obs:five-klesas"],
    [(LIN_YOGA, "Abhiniveśa flows on by its own nature and is established even in the wise (YS 2.9). Vyāsa: every living being has the constant wish 'may I not cease to be, may I be'; this dread of dying, found even in a worm just born and not learned from perception, inference or testimony, points to the pain of death known in a former birth; as in the most deluded, so it is established in the learned.", [YS('2.9'), YB('2.9')])],
    [("The wish 'may I not cease to be, may I go on being', and a dread of dying that comes without being taught.",
      ["I dread not existing", "the thought of death grips me even though I understand it", "I just want to go on being"], [YS('2.9'), YB('2.9')])],
    "Not a fault peculiar to a person and not something wrong with them: YS 2.9 says this clinging is found even in the wise. Not a reason to dwell on death; the product never offers death-contemplation as a gentle practice.",
    states=KLESA_STATES,
    eq=[("dx:tanha", "partial", "Vyāsa's 'may I be' is close to the craving for being (bhava-taṇhā) named in DN 22; YS treats it as a kleśa grounded in avidyā about a real self, DN 22 as craving that makes for renewed being, with no self.", [YB('2.9'), DN22('19')])],
    px=[("px:viveka-khyati-ys-2-26", [YS('2.26'), YB('2.4')])] + PX_KLESA))

# ---------------- the five vrttis ----------------
G_VR = 'the five modifications of mind (vṛtti; YS 1.5–11)'
VR_STATES = [
    ("kliṣṭa (afflicted)", "Caused by the kleśas, becoming a field for the store of karma.", [YS('1.5'), YB('1.5')]),
    ("akliṣṭa (unafflicted)", "Having discernment as their object and working against the rule of the guṇas; they can occur even in a stream of afflicted ones.", [YS('1.5'), YB('1.5')]),
]
PX_VR = [("px:abhyasa-vairagya-ys-1-12", [YS('1.12'), YB('1.11')])]
VR_NOT = " Every modification, afflicted or not, is to be stilled in yoga (Vyāsa on YS 1.11); naming one is not a judgement that it is bad."

A(E("dx:vrtti-pramana", "Pramāṇa (valid cognition)", "mind-activity", G_VR, VL,
    ["cpt:five-vrttis", "trm:vrtti", "trm:pramana"],
    [(LIN_YOGA, "Valid cognition is perception, inference and reliable testimony (YS 1.7); it is one of the five modifications, which may be afflicted or unafflicted (YS 1.5–6).", [YS('1.5'), YS('1.6'), YS('1.7'), YB('1.7')])],
    [("Knowing something by seeing it, by reasoning to it, or by trusted word.",
      ["I saw it with my own eyes", "I worked it out", "my teacher told me and I trust it"], [YS('1.7')])],
    "Not an obstacle in itself and not a test of truthfulness: in YS it is one modification of mind among five." + VR_NOT,
    states=VR_STATES, px=PX_VR))

A(E("dx:vrtti-viparyaya", "Viparyaya (erroneous cognition)", "mind-activity", G_VR, VL,
    ["cpt:five-vrttis", "obs:viparyaya", "trm:viparyaya"],
    [(LIN_YOGA, "Erroneous cognition is false knowledge, not resting on the actual form of its object (YS 1.8). Vyāsa: it is overturned by valid cognition, as seeing two moons is overturned by seeing one; it is avidyā of five parts.", [YS('1.8'), YB('1.8')])],
    [("Seeing something as other than it is, until a truer seeing corrects it — the two moons that one moon corrects.",
      ["I was certain, and it turned out I had it the wrong way round", "I saw what I expected, not what was there"], [YS('1.8'), YB('1.8')])],
    "Not a moral failing or a lie; not a medical sign: in YS 1.8 it is simply knowledge that does not match its object." + VR_NOT,
    states=VR_STATES,
    eq=[("dx:klesa-avidya", "same-under-standpoint", "Vyāsa calls erroneous cognition avidyā of five parts: the same error, as a modification of mind (vṛtti) and as an affliction (kleśa).", [YB('1.8')]),
        ("dx:antaraya-bhranti-darsana", "same-under-standpoint", "Vyāsa glosses the obstacle 'wrong seeing' as erroneous cognition (viparyaya-jñāna): the same cognition, as a modification (YS 1.8) and as an obstacle to samādhi (YS 1.30).", [YB('1.30'), YS('1.8')])],
    px=PX_VR))

A(E("dx:vrtti-vikalpa", "Vikalpa (verbal construction)", "mind-activity", G_VR, VL,
    ["cpt:five-vrttis", "obs:vikalpa", "trm:vikalpa"],
    [(LIN_YOGA, "Verbal construction follows word-knowledge and is empty of an object (YS 1.9). Vyāsa: it is neither valid cognition nor error, yet usage runs on the strength of words — as in 'consciousness is the nature of the puruṣa', where one thing is spoken of as if it had another, like 'Caitra's cow'.", [YS('1.9'), YB('1.9')])],
    [("A notion carried by words alone, with nothing standing behind it, yet one lives by it.",
      ["it's just a phrase, but I keep treating it as a thing", "I know it's only words, yet it runs my thinking"], [YS('1.9'), YB('1.9')])],
    "Not lying and not confusion in any medical sense: it is the ordinary working of language described in YS 1.9." + VR_NOT,
    states=VR_STATES, px=PX_VR))

A(E("dx:vrtti-nidra", "Nidrā (sleep)", "mind-activity", G_VR, VL,
    ["cpt:five-vrttis", "obs:nidra", "trm:nidra"],
    [(LIN_YOGA, "Sleep is the modification that rests on the cognition of absence (YS 1.10). Vyāsa: it is a cognition, because on waking one recollects it; like other cognitions it is to be stilled in samādhi.", [YS('1.10'), YB('1.10')])],
    [("Vyāsa's three recollections on waking: 'I slept happily; my mind is clear and sharpens my understanding' — 'I slept badly; my mind is dull, wandering, unsteady' — 'I slept heavily, like one stupefied; my limbs are heavy, my mind tired, lazy, as if robbed'.",
      ["I slept well and woke with a clear mind", "I slept badly and my mind keeps wandering", "I slept like a log and feel heavy and dull"], [YB('1.10')])],
    "Not a sleep problem to be assessed and not a medical matter: YS 1.10 treats sleep as a modification of mind to be understood and stilled. The product does not interpret sleep medically." + VR_NOT,
    states=VR_STATES,
    eq=[("dx:state-susupta", "partial", "YS counts sleep as a modification whose content is absence; the Māṇḍūkya calls deep sleep the third quarter, a mass of knowing, made of bliss (MāU 5), and Gauḍapāda calls it not knowing the real (GK 1.15). Same state, different accounts.", [YS('1.10'), MU('5'), GK('1.15')]),
        ("dx:nivarana-thina-middha", "partial", "The Vism says torpor (middha) can show as nodding and sleep; YS sleep is itself a modification of mind. Related, not the same.", [YS('1.10'), VSM(14, 469)])],
    px=PX_VR))

A(E("dx:vrtti-smrti", "Smṛti (memory)", "mind-activity", G_VR, VL,
    ["cpt:five-vrttis", "trm:smrti"],
    [(LIN_YOGA, "Memory is the not-slipping-away of an object once experienced (YS 1.11). Vyāsa: it is twofold — with an imagined object in dream, with an unimagined one in waking; all memories arise from the experience of the five modifications, and all modifications are of the nature of pleasure, pain and delusion, which are explained under the kleśas as rāga, dveṣa and avidyā.", [YS('1.11'), YB('1.11')])],
    [("An experience that does not slip away but keeps returning to the mind.",
      ["that memory keeps coming back", "I keep reliving what happened"], [YS('1.11'), YB('1.11')])],
    "Not the Buddhist sati (mindfulness), which is a different word-use, and not a memory problem in any medical sense." + VR_NOT,
    states=VR_STATES,
    eq=[("dx:state-svapna", "partial", "Vyāsa says memory in dream has an imagined object; the Māṇḍūkya's dream state is inward-knowing, enjoying the subtle (MāU 4).", [YB('1.11'), MU('4')])],
    px=PX_VR))

# ---------------- the nine antarayas ----------------
G_AN = 'the nine obstacles (antarāya), distractions of the mind (YS 1.30)'
AN_DEF = (LIN_YOGA, "One of the nine distractions (vikṣepa) that Vyāsa calls impurities of yoga (yoga-mala) and adversaries of yoga; they occur together with the modifications of mind, and without them those modifications do not occur.", [YS('1.30'), YB('1.30')])
PX_AN = [("px:ekatattva-abhyasa-ys-1-32", [YS('1.32')]), ("px:abhyasa-vairagya-ys-1-12", [YB('1.31'), YS('1.12')])]
AN_REFS = ["obs:nine-antarayas", "trm:antaraya"]

def antaraya(slug, name, refs, vdef, marker, cues, not_read, eq=None, px=PX_AN, extra_defs=()):
    A(E(f"dx:antaraya-{slug}", name, "obstacle", G_AN, VL, AN_REFS + refs,
        [(LIN_YOGA, vdef, [YS('1.30'), YB('1.30')]), AN_DEF] + list(extra_defs),
        [(marker, cues, [YB('1.30')])], not_read, eq=eq, px=px))

antaraya("vyadhi", "Vyādhi (illness)", ["obs:vyadhi", "trm:vyadhi"],
    "Illness is an imbalance of the bodily constituents, fluids and organs (dhātu-rasa-karaṇa-vaiṣamya), named first among the obstacles to samādhi.",
    "Illness that interrupts practice, as the text lists it.", ["I've been ill and couldn't keep up my practice"],
    "Never a medical finding: the product does not assess illness or suggest any practice for it. The text lists bodily illness only because it interrupts practice; for illness a person needs proper care from others, not this map.", px=[])
antaraya("styana", "Styāna (mental rigidity)", ["obs:styana", "trm:styana"],
    "Rigidity is the mind's unfitness for work (akarmaṇyatā).",
    "The mind will not take up the work; it is unfit for effort.", ["my mind just won't engage", "I sit down to practise and nothing in me will move"],
    "Not tiredness from lack of rest and not a medical condition: Vyāsa defines it only as the mind's unfitness for work.",
    eq=[("dx:nivarana-thina-middha", "partial", "Vyāsa defines styāna as unfitness for work (akarmaṇyatā); the Vism defines torpor (middha) as unwieldiness (akammaññatā) and stiffness (thīna, the Pali form of the word styāna) as lack of drive. The words and the definitions cross over.", [YB('1.30'), VSM(14, 469)])])
antaraya("samsaya", "Saṃśaya (doubt)", ["obs:samsaya", "trm:samsaya", "obs:pramana-samsaya"],
    "Doubt is knowledge that touches both sides: 'it may be thus, it may not be thus'.",
    "Knowing that touches both sides at once: 'it may be so, it may not be so'.", ["maybe this path works, maybe it doesn't", "I can't decide whether any of this is true"],
    "Not honest inquiry, which the texts themselves ask for, and not a verdict on a person's faith: in YB 1.30 it is wavering between two sides that stalls practice.",
    eq=[("dx:nivarana-vicikiccha", "partial", "The Vism defines doubt (vicikicchā) by wavering and indecision, an obstacle to practice (Vism XIV), and in the suttas it concerns wholesome states (DN 2); Vyāsa's saṃśaya is any knowledge touching both sides.", [YB('1.30'), VSM(14, 471), DN2])],
    px=PX_AN + [("px:approach-a-teacher-bg-4-34", [BG('4.34'), BG('4.42')])],
    extra_defs=[(LIN_GITA, "The Gītā: the one without knowledge and faith, whose self is doubt, perishes; for him there is neither this world nor the next nor happiness (BhG 4.40). Cut the doubt born of ignorance, lodged in the heart, with the sword of knowledge, and stand in yoga (BhG 4.42).", [BG('4.40'), BG('4.42')])])
antaraya("pramada", "Pramāda (heedlessness)", ["obs:pramada", "trm:pramada"],
    "Heedlessness is not cultivating the means of samādhi (samādhi-sādhanānām abhāvanam).",
    "Not doing the practice one knows supports samādhi.", ["I know what I should practise but I don't do it", "I keep letting my practice slide"],
    "Not a character flaw to be condemned and not a medical condition: Vyāsa defines it narrowly as not cultivating the means of samādhi. Not the Jain pramāda (TS 7.13), which is a different use of the word.",
    eq=[("dx:guna-tamas", "partial", "The Gītā says tamas binds by heedlessness, laziness and sleep (BhG 14.8); Vyāsa defines heedlessness as not cultivating the means of samādhi.", [YB('1.30'), BG('14.8')]),
        ("dx:jain-pramada", "partial", "In TS, heedless (pramatta) activity is what makes taking life into harming (TS 7.13) and heedlessness is a cause of bondage (TS 8.1); YB's pramāda is about neglecting the means of samādhi.", [YB('1.30'), TS('7.13'), TS('8.1')]),
        ("dx:pamada", "partial", "The Dhammapada calls heedlessness the path to death (Dhp 21); Vyāsa defines it as not cultivating the means of samādhi.", [YB('1.30'), DHP('21')])])
antaraya("alasya", "Ālasya (sloth)", ["obs:alasya", "trm:alasya"],
    "Sloth is not setting to work because of heaviness of body and mind.",
    "Not starting, because body and mind feel heavy.", ["I feel too heavy to begin", "body and mind feel like lead when it's time to sit"],
    "Not a judgement of laziness as a moral fault and not a medical condition; the product does not interpret bodily heaviness medically.",
    eq=[("dx:guna-tamas", "partial", "The Gītā names laziness (ālasya) among the bonds of tamas (BhG 14.8) and among the marks of the tāmasa doer (BhG 18.28).", [YB('1.30'), BG('14.8'), BG('18.28')]),
        ("dx:nivarana-thina-middha", "partial", "Stiffness and torpor (Vism XIV) are lack of drive and unwieldiness; Vyāsa's sloth is not starting because of heaviness.", [YB('1.30'), VSM(14, 469)])])
antaraya("avirati", "Avirati (non-detachment)", ["obs:avirati", "trm:avirati"],
    "Non-detachment is the mind's greed (gardha), made of contact with sense objects.",
    "The mind's greed for contact with objects, keeping it from turning away.", ["I can't let go of my pleasures long enough to practise", "the pull of things keeps winning"],
    "Not a rule against enjoyment and not a medical condition. Not the Jain avirati, which means not having taken the vows of abstention (TS 7.1, 8.1): same word, different sense.",
    eq=[("dx:jain-avirati", "partial", "Same word, different sense: for Vyāsa, greed for contact with objects; in TS, non-abstention from harming, falsehood, theft, unchastity and possessiveness.", [YB('1.30'), TS('7.1'), TS('8.1')])])
antaraya("bhranti-darsana", "Bhrānti-darśana (wrong seeing)", ["obs:bhranti-darsana", "trm:bhranti-darsana"],
    "Wrong seeing is erroneous cognition (viparyaya-jñāna).",
    "Seeing wrongly, as when one moon is seen as two, here in matters of practice.", ["I was sure of something about my practice that turned out false"],
    "Not a hallucination or any medical sign: Vyāsa defines it as erroneous cognition, the same as the modification viparyaya.",
    eq=[("dx:vrtti-viparyaya", "same-under-standpoint", "Vyāsa glosses wrong seeing as erroneous cognition (viparyaya-jñāna): the same cognition, as an obstacle (YS 1.30) and as a modification (YS 1.8).", [YB('1.30'), YS('1.8')])])
antaraya("alabdha-bhumikatva", "Alabdha-bhūmikatva (not gaining a stage)", ["obs:alabdha-bhumikatva", "trm:alabdha-bhumikatva"],
    "Not gaining a stage is the non-attainment of any ground (bhūmi) of samādhi.",
    "Not reaching any settled ground of samādhi.", ["I've practised for a long time and never reach any settled stage"],
    "Not a failure of the person and not a prediction that nothing will come: the text names it only as one of the distractions to be met with practice.")
antaraya("anavasthitatva", "Anavasthitatva (instability)", ["obs:anavasthitatva", "trm:anavasthitatva"],
    "Instability is the mind's not staying established in a ground once gained; for when samādhi is truly gained the mind would stay steady in it.",
    "Losing a ground once gained; the mind does not stay where it reached.", ["I reach a still place and then lose it", "I can't stay where I got to"],
    "Not a sign of anything wrong with the person and not a medical condition: Vyāsa names it so that it can be met with practice and dispassion.")

# ---------------- the four companions ----------------
G_CO = 'the companions of distraction (vikṣepa-sahabhuva; YS 1.31)'
CO_DEF = (LIN_YOGA, "Vyāsa: these companions of distraction occur in the distracted mind; they do not occur in the concentrated mind; the distractions are to be stilled by practice and dispassion.", [YS('1.31'), YB('1.31')])
PX_CO = [("px:ekatattva-abhyasa-ys-1-32", [YS('1.32')]), ("px:maitri-bhavana-ys-1-33", [YS('1.33'), YB('1.33')])]
CO_REFS = ["obs:viksepa-sahabhuva"]
def companion(slug, name, refs, vdef, marker, cues, not_read, eq=None):
    A(E(f"dx:companion-{slug}", name, "obstacle", G_CO, VL, CO_REFS + refs,
        [(LIN_YOGA, vdef, [YS('1.31'), YB('1.31')]), CO_DEF], [(marker, cues, [YS('1.31'), YB('1.31')])], not_read, eq=eq, px=PX_CO))

companion("duhkha", "Duḥkha (pain)", ["trm:duhkha"],
    "Pain is threefold — from oneself, from other beings, from the powers above; it is that by which living beings, struck, strive to be rid of it.",
    "Being struck by pain and straining to be rid of it, while the mind is scattered.", ["it hurts and I just want it gone", "the pain keeps pulling my mind away"],
    "Not a medical assessment of pain: the text names pain as a companion of the distracted mind. The paired practices are the text's means against distraction, not remedies for pain; the product does not interpret bodily pain.")
companion("daurmanasya", "Daurmanasya (dejection)", ["trm:daurmanasya"],
    "Dejection is agitation of the mind from the thwarting of a wish (icchā-vighāta).",
    "The mind shaken because a wish was blocked.", ["I'm upset because what I wanted didn't happen", "I'm shaken because my wish was blocked"],
    "Not a medical condition and not a lasting trait: Vyāsa defines it narrowly as the mind's agitation when a wish is thwarted, a companion of distraction.")
companion("angamejayatva", "Aṅgamejayatva (trembling of the limbs)", ["trm:angamejayatva"],
    "Trembling of the limbs is that which makes the limbs move and shake.",
    "The limbs moving and shaking while the mind is scattered.", ["when my mind is scattered my body won't keep still"],
    "Never a medical sign: the text names unsteadiness of the limbs only as a companion of the distracted mind. The product does not interpret bodily trembling; any persistent bodily trouble is outside this map.")
companion("svasa-prasvasa", "Śvāsa-praśvāsa (disturbed breathing)", ["trm:svasa-prasvasa"],
    "In-breath (śvāsa) is the vital air drawing in outer air; out-breath (praśvāsa) is its expelling the inner air. Named here as companions of distraction, the breath moving with the scattered mind.",
    "Breath drawn in and let out unsteadily along with a scattered mind.", ["my breathing gets uneven when my mind is scattered"],
    "Never a medical sign and never a cue for breath control: the text names the breath only as a companion of distraction. The product does not suggest breath techniques from this entry (YS 1.34's expelling and holding of breath is not paired here).")

# ---------------- cittabhumi ----------------
A(E("dx:cittabhumi", "Citta-bhūmi (the five grounds of mind)", "state", "the five grounds of mind (citta-bhūmi; Vyāsa on YS 1.1)", VL,
    ["cpt:citta-bhumis", "trm:ksipta", "trm:mudha", "trm:viksipta", "trm:ekagra", "trm:niruddha"],
    [(LIN_YOGA, "Vyāsa: samādhi is a property of the mind in all its grounds; the grounds of mind are the restless (kṣipta), the stupefied (mūḍha), the distracted (vikṣipta), the one-pointed (ekāgra) and the stilled (niruddha).", [YS('1.1'), YB('1.1')])],
    [("In the distracted ground, samādhi is subordinate to distraction and does not count as yoga.",
      ["sometimes I settle, but mostly I'm pulled away again"], [YB('1.1')]),
     ("In the one-pointed ground, samādhi lights up what truly is, weakens the kleśas, loosens the bonds of karma and turns toward stilling; with all modifications stilled it is samādhi without support (asaṃprajñāta).", [], [YB('1.1')])],
    "Not a ranking of people and not a verdict on anyone's attainment; the product never tells a person which ground they are in. Vyāsa names the first two grounds without describing them further here.",
    states=[("kṣipta (restless)", "Named as the first ground; not described further in this passage.", [YB('1.1')]),
            ("mūḍha (stupefied)", "Named as the second ground; not described further in this passage.", [YB('1.1')]),
            ("vikṣipta (distracted)", "Samādhi occurs but is subordinate to distraction; not counted as yoga.", [YB('1.1')]),
            ("ekāgra (one-pointed)", "Samādhi with support (saṃprajñāta): lights up the real object, weakens the kleśas.", [YB('1.1')]),
            ("niruddha (stilled)", "All modifications stilled: samādhi without support (asaṃprajñāta).", [YB('1.1')])],
    eq=[("dx:citta-vikkhitta", "partial", "MN 10 names the scattered mind (vikkhitta citta) to be known as such, without describing it; Vyāsa's distracted ground is where samādhi is subordinate to distraction.", [YB('1.1'), MN10('34')]),
        ("dx:gk-viksepa", "partial", "Gauḍapāda's distraction (vikṣepa) is the mind scattered among desires and enjoyments, to be calmed (GK 3.42, 3.44); Vyāsa's distracted ground is a level of the mind in the Yoga's scheme.", [YB('1.1'), GK('3.42'), GK('3.44')])],
    px=[("px:abhyasa-vairagya-ys-1-12", [YS('1.12')])]))

# ---------------- vitarka ----------------
A(E("dx:vitarka-himsadi", "Vitarka (thoughts of harming and the rest)", "obstacle", "the vitarkas that obstruct the restraints (YS 2.33–34)", VL,
    ["obs:vitarka-himsadi", "trm:vitarka", "trm:pratipaksa-bhavana"],
    [(LIN_YOGA, "When one is troubled by vitarkas, cultivate the opposite (YS 2.33). The vitarkas are harming and the rest (the opposites of the restraints) — done, caused to be done, or approved; preceded by greed, anger or delusion; mild, middling or intense; bearing the endless fruit of pain and ignorance: so cultivate the opposite (YS 2.34).", [YS('2.33'), YS('2.34'), YB('2.33'), YB('2.34')])],
    [("Thoughts of harming, lying, stealing and the rest arising — whether one would do the deed, have it done or approve it.",
      ["I keep thinking of hurting them back", "I'm tempted to lie my way out of this", "I'd be glad if someone else did the harm for me"], [YS('2.34')])],
    "Not a charge of wrongdoing and not a prediction of what a person will do: YS 2.34 names these thoughts so that their opposite can be cultivated.",
    states=[("mṛdu (mild)", "Mild vitarka.", [YS('2.34')]), ("madhya (middling)", "Middling vitarka.", [YS('2.34')]), ("adhimātra (intense)", "Intense vitarka.", [YS('2.34')]),
            ("kṛta / kārita / anumodita", "Done oneself, caused to be done, or approved.", [YS('2.34')])],
    eq=[("dx:jain-raudra-dhyana", "partial", "The Jain 'cruel meditation' is dwelling that arises from harming, falsehood, theft and guarding one's possessions (TS 9.35); YS vitarkas are thoughts of violating the restraints, met by cultivating the opposite.", [YS('2.34'), TS('9.35')])],
    px=[("px:pratipaksa-bhavana-ys-2-33", [YS('2.33'), YS('2.34')])]))

# ---------------- powers as obstacles ----------------
A(E("dx:siddhi-upasarga", "Siddhis as upasarga (powers as obstacles)", "obstacle", "powers as obstacles in samādhi (YS 3.37, 3.51)", VL,
    ["obs:siddhis-as-upasarga", "obs:siddhis-as-obstacles", "cpt:siddhis-as-obstacles", "trm:upasarga"],
    [(LIN_YOGA, "These (extraordinary perceptions) are obstacles in samādhi and accomplishments only to the outward-turned mind (YS 3.37). When invited by the exalted ones, one should neither cling nor take pride, because the unwanted would come again (YS 3.51).", [YS('3.37'), YB('3.37'), YS('3.51'), YB('3.51')])],
    [("Unusual perceptions or powers taken as achievements, drawing the mind outward from samādhi.",
      ["I've started having unusual experiences and I feel I'm becoming special", "I'm drawn to the powers more than to stillness"], [YS('3.37')]),
     ("Being courted or praised as advanced, and liking it.", ["people treat me as advanced now and I enjoy it"], [YS('3.51')])],
    "Not a claim that any power exists or has occurred, and not a reading of unusual experiences: the product never interprets such experiences and never encourages seeking powers. YS 3.37 lists them only as obstacles.",
    eq=[("dx:vism-vipassanupakkilesa", "partial", "The Vism's imperfections of insight (light, rapture, bliss and the rest) become imperfections when taken for the path (Vism XX); YS 3.37 calls powers obstacles in samādhi. Similar warning, different paths.", [YS('3.37'), VSM(20, 637)]),
        ("dx:gk-rasasvada", "partial", "Gauḍapāda warns against savouring the happiness of stillness (GK 3.45); YS warns against taking powers as accomplishments. Both are attachments to fruits along the way.", [YS('3.37'), GK('3.45')])],
    px=[("px:sanga-smaya-akarana-ys-3-51", [YS('3.51')])]))
