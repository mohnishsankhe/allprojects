"""Pali (early Buddhist / Theravada) entries: hindrances, fetters, roots, craving, heedlessness, muddled mindfulness,
MN 10 mind states, Visuddhimagga temperaments and further Visuddhimagga obstacles."""
from common import *

BL = 'ascetic-buddhist'
ENTRIES = []
A = ENTRIES.append

# ---------------- five hindrances ----------------
G_NIV = 'the five hindrances (nīvaraṇa; MN 10, DN 22)'
NIV_REFS = ["obs:five-hindrances", "cpt:five-hindrances", "trm:nivarana"]
def niv_mn10(term):
    return (LIN_EB, f"Contemplating dhammas as the five hindrances: when {term} is present in him the monk knows 'there is {term} in me'; when absent, 'there is no {term} in me'; he knows how the unarisen {term} arises, how the arisen {term} is abandoned, and how the abandoned {term} does not arise again.", [MN10('36'), DN22('13')])
SIMILE_INTRO = "DN 2: while the five hindrances are not abandoned, the monk regards them as a debt, a disease, a prison, slavery and a desert road; when abandoned, as freedom from debt, recovery, release from prison, freedom and a safe land, and gladness springs up. DN 2 applies the five images to the five hindrances together, listing both in the same order; in that order this hindrance stands with the image of "
SIMILE_NOTE = " (The one-to-one pairing of image and hindrance is the commentators' reading; DN 2 gives the images for the set.)"
PX_NIV = [("px:satipatthana-nivarana-contemplation-mn10-36", [MN10('36'), DN22('13')]), ("px:pathavi-kasina-vism-4", [VSM(4, 125)])]
NIV_JHANA = lambda factor: (LIN_TH, f"Vism IV (quoting the Peṭaka): the hindrances are the opponents of the jhāna factors; {factor}. With access concentration the hindrances are suppressed (Vism IV).", [VSM(4, 141), VSM(4, 125)])

A(E("dx:nivarana-kamacchanda", "Kāmacchanda (sensual desire)", "hindrance", G_NIV, BL, NIV_REFS + ["obs:kamacchanda", "trm:kamacchanda"],
    [niv_mn10("sensual desire"),
     (LIN_EB, "DN 2 names the first hindrance as covetousness for the world (abhijjhā): giving it up, the monk dwells with a mind free of covetousness and cleanses the mind of it.", [DN2]),
     (LIN_TH, "Vism IV: on the side of defilement, 'sense pleasures' means sensual desire (kāmacchanda) in its many forms, called desire (chanda), lust (rāga) and so on.", [VSM(4, 140)]),
     NIV_JHANA("concentration (samādhi) is the opponent of sensual desire"),
     (LIN_TH, "Vism XIV has no separate entry for kāmacchanda; its account of greed (lobha) is the nearest definition in the same text: grasping the object like monkey-lime, sticking like meat in a hot pan, not letting go like a lamp-black stain, with seeing enjoyment in things that fetter as its proximate cause.", [VSM(14, 468)])],
    [("The mind lured by sensual desire among various objects does not settle on a single object; overcome by it, it does not take the way that leaves the sense sphere (Vism IV).",
      ["my mind keeps getting lured from one tempting thing to another", "I can't settle because something else attracts me"], [VSM(4, 146)]),
     (SIMILE_INTRO + "a debt." + SIMILE_NOTE, ["my wants keep me in debt", "I'm always paying for what I crave"], [DN2])],
    "Not enjoyment or desire in ordinary life as a fault in itself, and not a medical condition: as a hindrance it is sensual desire that keeps the mind from settling on one object (Vism IV). Not the Yoga's rāga or the Jain lobha, which belong to other maps.",
    eq=[("dx:fetter-kamaraga", "partial", "The same kind of lust named in two lists: as a hindrance it blocks jhāna (Vism IV); as a fetter it binds to the sense sphere and is abandoned only by the third path (Vism XXII).", [VSM(4, 146), VSM(22, 684)]),
        ("dx:root-lobha", "partial", "Vism XIV defines greed; sensual desire as a hindrance is named for what it blocks.", [VSM(14, 468), VSM(4, 146)]),
        ("dx:klesa-raga", "partial", "YS rāga follows remembered pleasure (YS 2.7); the hindrance is sensual desire that blocks concentration (Vism IV).", [YS('2.7'), VSM(4, 146)])],
    px=PX_NIV))

A(E("dx:nivarana-byapada", "Byāpāda (ill will)", "hindrance", G_NIV, BL, NIV_REFS + ["obs:byapada", "trm:byapada"],
    [niv_mn10("ill will"),
     (LIN_EB, "DN 2: giving up ill will and malice, the monk dwells with a mind free of ill will, with sympathy for the welfare of all living beings, and cleanses the mind of it.", [DN2]),
     NIV_JHANA("rapture (pīti) is the opponent of ill will"),
     (LIN_TH, "Vism XIV on hate (dosa), the factor at work in ill will: its characteristic is ferocity, like a snake struck; its function is to spread, like poison, or to burn its own support, like a forest fire; it shows as persecuting, like an enemy who has got his chance; its proximate cause is the grounds for annoyance.", [VSM(14, 470)])],
    [("Hindered by ill will toward the object, the mind does not flow on without break (Vism IV).", ["I keep bumping up against what I dislike and can't settle"], [VSM(4, 146)]),
     ("'He abused me, he struck me, he beat me, he robbed me' — in those who keep such thoughts hatred is not appeased; in those who do not, it is (Dhp 3–4).", ["I keep going over how they insulted me", "I can't stop thinking about what they did to me"], [DHP('3'), DHP('4')]),
     (SIMILE_INTRO + "a disease." + SIMILE_NOTE, ["this resentment sits in me like a sickness"], [DN2])],
    "Not the recognition that something is wrong or harmful, and not a medical condition: it is ill will that keeps pushing against its object (Vism IV, XIV). Not the Yoga's dveṣa or the Jain krodha.",
    eq=[("dx:fetter-patigha", "partial", "Ill will as a hindrance blocks jhāna; resentment (paṭigha) as a fetter binds to the sense sphere until the third path (Vism XXII).", [VSM(4, 146), VSM(22, 684)]),
        ("dx:root-dosa", "partial", "Vism XIV defines hate; the hindrance is ill will as it blocks the mind's flow.", [VSM(14, 470), VSM(4, 146)])],
    px=PX_NIV + [("px:metta-bhavana-vism-9", [DN2, DHP('5'), VSM(9, 318)])]))

A(E("dx:nivarana-thina-middha", "Thīna-middha (stiffness and torpor)", "hindrance", G_NIV, BL, NIV_REFS + ["obs:thina-middha", "trm:thina-middha"],
    [niv_mn10("stiffness and torpor"),
     (LIN_EB, "DN 2: giving up stiffness and torpor, the monk dwells free of them, perceiving light (āloka-saññī), mindful and clearly knowing.", [DN2]),
     NIV_JHANA("applied thought (vitakka) is the opponent of stiffness and torpor"),
     (LIN_TH, "Vism XIV: stiffness (thīna) has lack of drive as its characteristic, removes energy, and shows as sinking; torpor (middha) has unwieldiness as its characteristic, smothers, and shows as drooping or as nodding and sleep; for both the proximate cause is unwise attention to boredom, lazy stretching and the like.", [VSM(14, 469)])],
    [("Overcome by stiffness and torpor the mind is unwieldy (Vism IV).", ["my mind feels stuck and won't move", "I have no drive at all"], [VSM(4, 146)]),
     ("Sinking, drooping, nodding off; bored, stretching lazily (Vism XIV).", ["I keep nodding off when I sit", "I'm listless and keep yawning and stretching"], [VSM(14, 469)]),
     (SIMILE_INTRO + "a prison." + SIMILE_NOTE, ["I feel locked in a dull heaviness"], [DN2])],
    "Not bodily tiredness from lack of rest or any illness, and not a medical condition: it is the mind's lack of drive and unwieldiness as the Vism defines them. The product does not interpret sleepiness medically.",
    eq=[("dx:antaraya-styana", "partial", "Vyāsa's styāna is the mind's unfitness for work (YB 1.30); Vism XIV's torpor is unwieldiness and its stiffness (thīna) lack of drive.", [YB('1.30'), VSM(14, 469)]),
        ("dx:gk-laya", "partial", "Gauḍapāda's laya is the mind dissolving as in sleep (GK 3.35, 3.44); torpor can show as nodding and sleep (Vism XIV).", [GK('3.44'), VSM(14, 469)])],
    px=PX_NIV + [("px:aloka-sanna-dn2-68", [DN2])]))

A(E("dx:nivarana-uddhacca-kukkucca", "Uddhacca-kukkucca (restlessness and remorse)", "hindrance", G_NIV, BL, NIV_REFS + ["obs:uddhacca-kukkucca", "trm:uddhacca-kukkucca"],
    [niv_mn10("restlessness and remorse"),
     (LIN_EB, "DN 2: giving up restlessness and remorse, the monk dwells unagitated, his mind peaceful within.", [DN2]),
     NIV_JHANA("bliss (sukha) is the opponent of restlessness and remorse"),
     (LIN_TH, "Vism XIV: restlessness (uddhacca) has disquiet as its characteristic, like water whipped by wind; unsteadiness as its function, like a flag in the wind; it shows as turmoil, like ash flung up when a stone strikes it; it is distraction of mind. Remorse (kukkucca) has regret afterwards as its characteristic, sorrowing over what was done and not done as its function, and shows as remorse; it is to be regarded as slavery.", [VSM(14, 469), VSM(14, 470)])],
    [("Seized by restlessness and remorse, the mind is unpeaceful and flits about (Vism IV).", ["my mind won't settle, it's blown about", "I can't sit still inside"], [VSM(4, 146)]),
     ("Regret afterwards: sorrowing over what one did and did not do (Vism XIV).", ["I keep regretting what I did and didn't do", "I keep going back over what I should have done"], [VSM(14, 470)]),
     (SIMILE_INTRO + "slavery; Vism XIV likewise says remorse is to be regarded as slavery." + SIMILE_NOTE, ["my worries order me about like a master"], [DN2, VSM(14, 470)])],
    "Not ordinary liveliness or conscience and not a medical condition: kukkucca here is brooding regret over deeds done and not done; the texts do not ask anyone to stop caring about their conduct.",
    eq=[("dx:fetter-uddhacca", "partial", "In the hindrance restlessness is paired with remorse and blocks jhāna; as a fetter, restlessness alone remains until the fourth path (Vism XXII).", [VSM(14, 469), VSM(22, 684)]),
        ("dx:gita-restless-mind", "partial", "The Gītā's restless mind is as hard to hold as the wind (BhG 6.34); Vism XIV's restlessness is like water whipped by wind.", [BG('6.34'), VSM(14, 469)]),
        ("dx:citta-vikkhitta", "partial", "MN 10 names the scattered mind without describing it; Vism XIV calls restlessness 'distraction of mind' (citta-vikkhepa).", [MN10('34'), VSM(14, 469)])],
    px=PX_NIV))

A(E("dx:nivarana-vicikiccha", "Vicikicchā (doubt)", "hindrance", G_NIV, BL, NIV_REFS + ["obs:vicikiccha", "trm:vicikiccha"],
    [niv_mn10("doubt"),
     (LIN_EB, "DN 2: giving up doubt, the monk dwells having crossed over doubt, without perplexity about wholesome states.", [DN2]),
     NIV_JHANA("sustained thought (vicāra) is the opponent of doubt"),
     (LIN_TH, "Vism XIV: doubt has doubting as its characteristic and wavering as its function; it shows as indecision or as taking now one side, now another; its proximate cause is unwise attention; it obstructs practice.", [VSM(14, 471)])],
    [("Stricken by doubt, the mind does not take up the way to jhāna (Vism IV).", ["I can't commit to the practice because I'm not sure of it"], [VSM(4, 146)]),
     ("Wavering, taking now one side, now another (Vism XIV).", ["I keep wavering between teachings", "one day I believe it, the next I don't"], [VSM(14, 471)]),
     (SIMILE_INTRO + "a desert road." + SIMILE_NOTE, ["I feel lost in a wilderness, not knowing which way is safe"], [DN2])],
    "Not honest questioning, which the texts themselves practise, and not a verdict on a person's faith: it is the wavering that blocks practice (Vism XIV).",
    eq=[("dx:fetter-vicikiccha", "exact", "The same mental factor (Vism XIV) named in two lists: as a hindrance it blocks jhāna (Vism IV); as a fetter it binds to rebirth and is cut by the first path (Vism XXII).", [VSM(14, 471), VSM(4, 146), VSM(22, 684)]),
        ("dx:antaraya-samsaya", "partial", "Vyāsa's saṃśaya is knowledge touching both sides (YB 1.30); the Vism's doubt is wavering that obstructs practice.", [YB('1.30'), VSM(14, 471)])],
    px=PX_NIV + [("px:paccaya-pariggaha-vism-19", [VSM(22, 694)])]))

# ---------------- ten fetters ----------------
G_FE = 'the ten fetters (saṃyojana; Vism XXII)'
FE_DEF = (LIN_TH, "Vism XXII: the fetters are ten states, beginning with lust for form, so called because they bind aggregates to aggregates, action to its fruit, and beings to suffering. Lust for form, lust for the formless, conceit, restlessness and ignorance are the five higher fetters; personality view, doubt, adherence to rules and observances, sensual lust and resentment are the five lower fetters.", [VSM(22, 682), VSM(22, 683)])
FE_MN10 = (LIN_EB, "MN 10: contemplating the sense bases, the monk knows the eye, forms, and the fetter that arises dependent on both; how the unarisen fetter arises, how the arisen one is abandoned, and how the abandoned one does not arise again.", [MN10('40')])
FE_REFS = ["obs:ten-fetters", "cpt:ten-fetters", "trm:samyojana"]
def fetter(slug, name, refs, lower, path_text, extra_defs, markers, not_read, eq=None, px=None):
    grp = [("obs:five-lower-fetters" if lower else "obs:five-higher-fetters")]
    A(E(f"dx:fetter-{slug}", name, "fetter", G_FE, BL, FE_REFS + grp + refs,
        [FE_DEF, (LIN_TH, path_text, [VSM(22, 684)]), FE_MN10] + extra_defs, markers, not_read, eq=eq,
        px=px if px is not None else [("px:satipatthana-ayatana-contemplation-mn10-40", [MN10('40')])]))

fetter("sakkaya-ditthi", "Sakkāya-diṭṭhi (personality view)", ["obs:sakkaya-ditthi", "trm:sakkaya-ditthi"], True,
    "Abandoned by the first path (stream-entry) (Vism XXII).",
    [(LIN_TH, "Vism XVII: personality view in twenty forms is clinging to a doctrine of self: the untaught ordinary person regards form as self, and so with the other aggregates.", [VSM(17, 570)]),
     (LIN_TH, "Vism XXII: defining mentality-materiality abandons personality view by substitution of the opposite.", [VSM(22, 694)])],
    [("Regarding the body, feelings, perceptions, formations or consciousness as self (Vism XVII).", ["this body and mind are my self", "my feelings are who I am"], [VSM(17, 570)])],
    "Not having a name, a history or responsibility for one's acts; it is the view that regards the aggregates as self (Vism XVII). Not the Yoga's asmitā: the Yoga affirms a real seer, Theravāda affirms no self.",
    eq=[("dx:klesa-asmita", "partial", "Both name a false taking of something as self; the Yoga affirms a real seer beyond buddhi (YS 2.6), Theravāda denies any self (Vism XVII). The denial stands.", [YS('2.6'), VSM(17, 570)])],
    px=[("px:khandha-contemplation-mn10-38", [MN10('38')]), ("px:namarupa-pariccheda-vism-18", [VSM(22, 694)])])
fetter("vicikiccha", "Vicikicchā (doubt, as a fetter)", ["trm:vicikiccha"], True,
    "Abandoned by the first path (Vism XXII).",
    [(LIN_TH, "Vism XIV: doubt has doubting as its characteristic and wavering as its function; it shows as indecision; it obstructs practice.", [VSM(14, 471)])],
    [("Wavering, taking now one side, now another (Vism XIV).", ["I keep wavering about whether this path is true"], [VSM(14, 471)])],
    "Not honest questioning and not a verdict on a person's faith.",
    eq=[("dx:nivarana-vicikiccha", "exact", "The same mental factor named in the list of hindrances and the list of fetters; the roles differ (blocks jhāna / binds to rebirth).", [VSM(14, 471), VSM(22, 684)])],
    px=[("px:paccaya-pariggaha-vism-19", [VSM(22, 694)])])
fetter("silabbata-paramasa", "Sīlabbata-parāmāsa (adherence to rules and observances)", ["trm:silabbata-paramasa"], True,
    "Abandoned by the first path (Vism XXII).",
    [(LIN_TH, "Vism XVII: clinging to rules and observances is the adherence that purity comes through rules and vows — 'purity by virtue, purity by vow, purity by virtue and vow'.", [VSM(17, 569)])],
    [("Holding that keeping a rule or observance is itself what purifies (Vism XVII).", ["if I keep this rule perfectly I will be pure", "the ritual itself will free me"], [VSM(17, 569)])],
    "Not the keeping of precepts or observances, which the Visuddhimagga itself makes the ground of the path; it is the adherence that purity comes from rule and vow alone.")
fetter("kamaraga", "Kāmarāga (sensual lust)", ["obs:kamaraga", "trm:kamaraga"], True,
    "In its gross form, together with resentment, it is abandoned by the second path; in its subtle form by the third; the form of it that leads to the states of loss goes with the first (Vism XXII).",
    [(LIN_TH, "Vism XIV on greed (lobha): grasping the object like monkey-lime, sticking like meat in a hot pan, not letting go like a lamp-black stain.", [VSM(14, 468)])],
    [("Greed that sticks to its object and will not let go (Vism XIV).", ["I can't let go of wanting it"], [VSM(14, 468)])],
    "Not ordinary enjoyment condemned and not a medical condition.",
    eq=[("dx:nivarana-kamacchanda", "partial", "The same kind of lust in two lists: hindrance to jhāna (Vism IV), fetter to the sense sphere (Vism XXII).", [VSM(4, 146), VSM(22, 684)]),
        ("dx:root-lobha", "partial", "Vism XIV defines greed; sensual lust is its sense-sphere form as a fetter.", [VSM(14, 468), VSM(22, 683)])])
fetter("patigha", "Paṭigha (resentment)", ["trm:patigha"], True,
    "In its gross form abandoned by the second path, in its subtle form by the third (Vism XXII).",
    [(LIN_TH, "Vism XIV on hate (dosa): ferocity like a struck snake; spreading like poison; showing as persecuting, like an enemy who has got his chance.", [VSM(14, 470)])],
    [("Ferocity toward its object, spreading like poison (Vism XIV).", ["I flare up against them every time"], [VSM(14, 470)])],
    "Not the recognition of harm and not a medical condition.",
    eq=[("dx:nivarana-byapada", "partial", "Ill will in the hindrance list, resentment in the fetter list (Vism IV, XXII).", [VSM(4, 146), VSM(22, 684)]),
        ("dx:root-dosa", "partial", "Vism XIV defines hate; resentment is its form as a fetter.", [VSM(14, 470), VSM(22, 683)]),
        ("dx:klesa-dvesa", "partial", "Vyāsa uses the word pratigha in defining dveṣa (YB 2.8).", [YB('2.8'), VSM(22, 683)])])
fetter("ruparaga", "Rūparāga (lust for form)", ["obs:ruparaga", "trm:ruparaga"], False,
    "Abandoned only by the fourth path (arahantship) (Vism XXII).", [],
    [("The Visuddhimagga gives it by name and function only: a lust that binds to existence in the form sphere, remaining until the fourth path.", [], [VSM(22, 682), VSM(22, 684)])],
    "Not attraction to beautiful forms in the everyday sense and never a verdict on a person's stage on the path.")
fetter("aruparaga", "Arūparāga (lust for the formless)", ["obs:aruparaga", "trm:aruparaga"], False,
    "Abandoned only by the fourth path (Vism XXII).", [],
    [("Given by name and function only: a lust that binds to existence in the formless sphere, remaining until the fourth path.", [], [VSM(22, 682), VSM(22, 684)])],
    "Never a verdict on a person's stage on the path.")
fetter("mana", "Māna (conceit)", ["trm:mana"], False,
    "Abandoned only by the fourth path (Vism XXII).",
    [(LIN_TH, "Vism XIV: conceit has haughtiness as its characteristic, self-exaltation as its function, and shows as wanting to be a banner (to be displayed); its proximate cause is greed not joined to views.", [VSM(14, 469)]),
     (LIN_EB, "Dhp 221: give up anger, abandon conceit, go beyond every fetter.", [DHP('221')])],
    [("Holding oneself high, wanting to be displayed (Vism XIV).", ["I need to be seen as better than them", "I want to be the one everyone looks up to"], [VSM(14, 469)])],
    "Not self-respect and not a medical condition; the texts' conceit includes even the subtle 'I am' that remains until the fourth path.",
    eq=[("dx:kasaya-mana", "partial", "Jain pride is one of four passions graded by intensity (TS 8.9); Theravāda conceit is haughtiness remaining until the fourth path (Vism XIV, XXII).", [TS('8.9'), VSM(14, 469)]),
        ("dx:klesa-asmita", "partial", "Asmitā is the seeming oneness of seer and seeing (YS 2.6); conceit is haughtiness and self-exaltation (Vism XIV).", [YS('2.6'), VSM(14, 469)]),
        ("dx:gita-asuri-sampad", "partial", "The Gītā lists arrogance and conceit (darpa, abhimāna) among demonic qualities (BhG 16.4).", [BG('16.4'), VSM(14, 469)])])
fetter("uddhacca", "Uddhacca (restlessness, as a fetter)", ["obs:uddhacca", "trm:uddhacca"], False,
    "Abandoned only by the fourth path (Vism XXII).",
    [(LIN_TH, "Vism XIV: restlessness has disquiet as its characteristic, like water whipped by wind; it is distraction of mind.", [VSM(14, 469)])],
    [("Disquiet, like water whipped by wind (Vism XIV).", ["even when things are fine, something in me won't settle"], [VSM(14, 469)])],
    "Not liveliness and not a medical condition of any kind.",
    eq=[("dx:nivarana-uddhacca-kukkucca", "partial", "Paired with remorse as a hindrance to jhāna; alone as a higher fetter until the fourth path.", [VSM(14, 469), VSM(22, 684)])])
fetter("avijja", "Avijjā (ignorance)", ["trm:avijja"], False,
    "Abandoned only by the fourth path (Vism XXII).",
    [(LIN_TH, "Vism XIV on delusion (moha): blindness of mind or unknowing as its characteristic; non-penetration, or concealing the nature of the object, as its function; it shows as wrong practice or as darkness; its proximate cause is unwise attention; it is the root of all that is unwholesome.", [VSM(14, 468)])],
    [("Blindness of mind that hides how things are (Vism XIV).", ["I just can't see what's really going on"], [VSM(14, 468)])],
    "Not a lack of schooling and not a judgement of intelligence. Not the Yoga's avidyā, which presupposes a real self that Theravāda denies.",
    eq=[("dx:root-moha", "partial", "The fetter list names avijjā; Vism XIV defines moha. The Abhidhamma treats these as one factor, but that equation is not cited here.", [VSM(22, 682), VSM(14, 468)]),
        ("dx:klesa-avidya", "partial", "Both name not-seeing as the root of bondage; the Yoga's avidyā ends in the seer's aloneness (YS 2.25), the Theravāda avijjā is cut by the fourth path with no self uncovered.", [YS('2.5'), VSM(14, 468)])])

# ---------------- three unwholesome roots ----------------
G_RO = 'the three unwholesome roots (lobha, dosa, moha; Vism XIV, XXII)'
RO_REFS = ["cpt:three-roots", "obs:three-poisons", "obs:lobha-krodha-moha"]
PX_RO = [("px:satipatthana-citta-contemplation-mn10-34", [MN10('34'), DN22('12')])]
RO_KILESA = (LIN_TH, "Vism XXII lists greed, hate, delusion, conceit, views, doubt, stiffness, restlessness, shamelessness and fearlessness of wrongdoing as the ten defilements (kilesa).", [VSM(22, 683)])
A(E("dx:root-lobha", "Lobha (greed)", "affliction", G_RO, BL, RO_REFS + ["obs:lobha", "trm:lobha"],
    [(LIN_TH, "Vism XIV: greed has grasping the object as its characteristic, like monkey-lime; sticking as its function, like meat thrown in a hot pan; not letting go as its manifestation, like a lamp-black stain; seeing enjoyment in things that fetter as its proximate cause; growing into a river of craving it carries one to the states of loss.", [VSM(14, 468)]), RO_KILESA,
     (LIN_EB, "MN 10: the monk knows a mind with lust (sarāga) as a mind with lust, and a mind without lust as without lust.", [MN10('34'), DN22('12')])],
    [("Grasping that sticks and will not let go (Vism XIV).", ["I can't let go of it", "it sticks to me"], [VSM(14, 468)]),
     ("There is no fire like lust (Dhp 202, 251).", ["the wanting burns in me"], [DHP('202'), DHP('251')])],
    "Not ordinary wanting condemned and not a medical condition. Not identical to the Yoga's rāga or the Jain lobha.",
    eq=[("dx:klesa-raga", "partial", "Vyāsa glosses rāga with the word lobha (YB 2.7); the Theravāda lobha is a momentary mental factor with no self behind it (Vism XIV).", [YB('2.7'), VSM(14, 468)]),
        ("dx:kasaya-lobha", "partial", "Jain greed is a passion that makes the soul take in karmic matter (TS 8.2, 8.9).", [TS('8.9'), VSM(14, 468)]),
        ("dx:carita-raga", "partial", "The greedy temperament is one in whom greed predominates (Vism III).", [VSM(3, 101), VSM(14, 468)])],
    px=PX_RO))
A(E("dx:root-dosa", "Dosa (hate)", "affliction", G_RO, BL, RO_REFS + ["trm:dosa"],
    [(LIN_TH, "Vism XIV: hate has ferocity as its characteristic, like a snake struck; spreading as its function, like poison, or burning its own support, like a forest fire; persecuting as its manifestation, like an enemy who has got his chance; the grounds for annoyance as its proximate cause; it is like urine mixed with poison.", [VSM(14, 470)]), RO_KILESA,
     (LIN_EB, "MN 10: the monk knows a mind with hate (sadosa) as a mind with hate.", [MN10('34'), DN22('12')])],
    [("Ferocity that spreads and burns its own support (Vism XIV).", ["my anger burns me more than them"], [VSM(14, 470)]),
     ("Hatred is never appeased by hatred; by non-hatred it is appeased (Dhp 5).", ["I want to hate them back"], [DHP('5')])],
    "Not the recognition of harm and not a medical condition. Not identical to the Yoga's dveṣa or the Jain krodha.",
    eq=[("dx:klesa-dvesa", "partial", "Vyāsa's dveṣa includes resentment, the wish to strike and anger toward remembered pain (YB 2.8).", [YB('2.8'), VSM(14, 470)]),
        ("dx:kasaya-krodha", "partial", "Jain anger is a passion graded in four intensities (TS 8.9).", [TS('8.9'), VSM(14, 470)]),
        ("dx:carita-dosa", "partial", "The hating temperament is one in whom hate predominates (Vism III).", [VSM(3, 101), VSM(14, 470)])],
    px=PX_RO + [("px:metta-bhavana-vism-9", [DHP('5'), VSM(9, 318)])]))
A(E("dx:root-moha", "Moha (delusion)", "affliction", G_RO, BL, RO_REFS + ["trm:moha"],
    [(LIN_TH, "Vism XIV: delusion has blindness of mind, or unknowing, as its characteristic; non-penetration, or concealing the nature of the object, as its function; wrong practice or darkness as its manifestation; unwise attention as its proximate cause; it is the root of all that is unwholesome.", [VSM(14, 468)]), RO_KILESA,
     (LIN_EB, "MN 10: the monk knows a mind with delusion (samoha) as a mind with delusion.", [MN10('34'), DN22('12')])],
    [("Blindness of mind; the object's nature hidden (Vism XIV).", ["I can't see my way at all", "everything is murky"], [VSM(14, 468)]),
     ("There is no net like delusion (Dhp 251).", ["I'm caught and can't see how"], [DHP('251')])],
    "Not a lack of intelligence and not a medical condition. Not the Yoga's avidyā.",
    eq=[("dx:klesa-avidya", "partial", "Both are the root not-seeing of their systems; the metaphysics differ (YS 2.5; Vism XIV).", [YS('2.5'), VSM(14, 468)]),
        ("dx:guna-tamas", "partial", "The Gītā's tamas is born of ignorance and deludes (BhG 14.8); Vism's moha is blindness of mind.", [BG('14.8'), VSM(14, 468)]),
        ("dx:carita-moha", "partial", "The deluded temperament is one in whom delusion predominates (Vism III).", [VSM(3, 101), VSM(14, 468)])],
    px=PX_RO))

# ---------------- craving, heedlessness, muddled mindfulness ----------------
A(E("dx:tanha", "Taṇhā (craving)", "affliction", "craving, the origin of suffering (DN 22; Dhp 334–338)", BL, ["obs:trsna", "trm:tanha", "obs:asa-trsna"],
    [(LIN_EB, "DN 22: the origin of suffering is craving that makes for renewed being, bound up with delight and lust, delighting now here, now there: craving for sense pleasures, craving for being, craving for non-being. It arises and settles wherever in the world there is what is dear and agreeable.", [DN22('19')]),
     (LIN_EB, "Dhp 334–335: in one who lives heedlessly craving grows like a creeper; he leaps from life to life like a monkey seeking fruit in the forest; whoever is overcome by this clinging craving, his sorrows grow like grass after rain. Dhp 338: as a tree cut down grows again if its root is unharmed, so while latent craving is not rooted out this suffering arises again and again.", [DHP('334'), DHP('335'), DHP('338')])],
    [("Delighting now here, now there; arising wherever there is what is dear (DN 22).", ["the more I get the more I want", "I jump from one want to the next"], [DN22('19')]),
     ("Growing like a creeper in one who lives heedlessly (Dhp 334).", ["it keeps growing the less I watch it"], [DHP('334')])],
    "Not ordinary needs or wishes condemned and not a medical condition. Not the Yoga's rāga or the Gītā's tṛṣṇā, which sit in other maps.",
    states=[("kāma-taṇhā", "Craving for sense pleasures.", [DN22('19')]), ("bhava-taṇhā", "Craving for being.", [DN22('19')]), ("vibhava-taṇhā", "Craving for non-being.", [DN22('19')])],
    eq=[("dx:klesa-raga", "partial", "Vyāsa defines rāga with the word tṛṣṇā (YB 2.7); craving in DN 22 is the origin of suffering, with no self.", [YB('2.7'), DN22('19')]),
        ("dx:klesa-abhinivesa", "partial", "Vyāsa's 'may I be' (YB 2.9) is close to the craving for being (DN 22).", [YB('2.9'), DN22('19')]),
        ("dx:guna-rajas", "partial", "The Gītā says rajas springs from craving and attachment (BhG 14.7).", [BG('14.7'), DN22('19')])],
    px=[("px:four-truths-contemplation-mn10-44", [MN10('44'), DN22('19')])]))
A(E("dx:pamada", "Pamāda (heedlessness)", "obstacle", "heedlessness (Dhp 21–32)", BL, ["obs:pramada", "trm:pramada"],
    [(LIN_EB, "Heedfulness is the path to the deathless, heedlessness the path to death; the heedful do not die, the heedless are as if dead already (Dhp 21). In one who lives heedlessly craving grows like a creeper (Dhp 334).", [DHP('21'), DHP('334')])],
    [("Letting life slip by without attending to what matters (Dhp 21).", ["I let the days slip by without attending to what matters"], [DHP('21')])],
    "Not a moral condemnation and not a medical condition; not a prediction about anyone's death: 'path to death' is the Dhammapada's own image.",
    eq=[("dx:antaraya-pramada", "partial", "Vyāsa defines heedlessness as not cultivating the means of samādhi (YB 1.30); the Dhammapada makes it the path to death.", [YB('1.30'), DHP('21')]),
        ("dx:jain-pramada", "partial", "In TS heedlessness is a cause of bondage (TS 8.1).", [TS('8.1'), DHP('21')]),
        ("dx:mutthassati", "partial", "Muddled mindfulness (MN 118) and heedlessness (Dhp 21) are named in different texts; both are the opposite of the attending the suttas ask for.", [MN118('26'), DHP('21')])]))
A(E("dx:mutthassati", "Muṭṭhassati (muddled mindfulness)", "obstacle", "named in MN 118", BL, ["trm:sati"],
    [(LIN_EB, "MN 118: 'I do not say there is development of mindfulness of breathing for one who is muddled in mindfulness and not clearly knowing.' Its opposite is mindfulness established and not muddled (upaṭṭhitā sati asammuṭṭhā), with which the awakening factor of mindfulness begins.", [MN118('26'), MN118('30')])],
    [("Mindfulness muddled, not clearly knowing what one is doing (MN 118).", ["I keep losing track of what I'm doing", "I do things without noticing"], [MN118('26')])],
    "Not poor memory and not an attention problem in any medical sense. Not the Yoga's smṛti-vṛtti (memory as a modification of mind): sati here is mindfulness as the suttas use it.",
    px=[("px:sati-sampajanna-mn10-8", [MN10('8')])]))

# ---------------- MN 10 mind states ----------------
G_CI = 'states of mind known in contemplating mind (MN 10, DN 22)'
A(E("dx:citta-sankhitta", "Saṅkhitta citta (contracted mind)", "state", G_CI, BL, ["trm:cittanupassana"],
    [(LIN_EB, "MN 10: the monk knows a contracted mind as contracted and a scattered mind as scattered, as part of contemplating mind in mind.", [MN10('34'), DN22('12')])],
    [("The text names the state and asks only that it be known as it is: 'he knows a contracted mind as contracted'.", ["my mind feels shrunk in on itself"], [MN10('34')])],
    "Not a medical state. MN 10 gives no further description; the commentarial glosses are not cited here.",
    px=[("px:satipatthana-citta-contemplation-mn10-34", [MN10('34')])]))
A(E("dx:citta-vikkhitta", "Vikkhitta citta (scattered mind)", "state", G_CI, BL, ["trm:cittanupassana"],
    [(LIN_EB, "MN 10: the monk knows a scattered mind as scattered, as part of contemplating mind in mind.", [MN10('34'), DN22('12')])],
    [("The text names the state and asks only that it be known as it is: 'he knows a scattered mind as scattered'.", ["my mind is scattered all over the place"], [MN10('34')])],
    "Not a medical state of any kind. MN 10 gives no further description; the commentarial glosses are not cited here.",
    eq=[("dx:cittabhumi", "partial", "Vyāsa's distracted ground (vikṣipta) is where samādhi is subordinate to distraction (YB 1.1); MN 10 names the scattered mind without description.", [YB('1.1'), MN10('34')])],
    px=[("px:satipatthana-citta-contemplation-mn10-34", [MN10('34')])]))

# ---------------- six temperaments (Vism III) ----------------
G_CA = 'the six temperaments (carita; Vism III)'
CA_REFS = ["cpt:six-temperaments", "trm:carita"]
CA_DEF = (LIN_TH, "Vism III: temperament (cariyā) is sixfold — greedy, hating, deluded, faithful, intelligent, speculative; some count fourteen by combining them, but in brief there are six. Temperament, nature (pakati) and predominance (ussannatā) mean the same.", [VSM(3, 101)])
CA_CAVEAT = (LIN_TH, "Vism III itself cautions: this way of discerning temperament by posture and the rest is not handed down in full in the canon or the commentaries but only as the teachers' opinion, so it is not to be taken as authoritative; people of hating temperament and the rest can behave like the greedy when they live diligently, and in one of mixed temperament the separate marks do not appear. A teacher with knowledge of others' minds knows the temperament; otherwise he should ask the pupil.", [VSM(3, 107)])
CA_ORIGIN = (LIN_TH, "Vism III: temperaments arise from the kamma that produced rebirth, according to which of greed, hate, delusion and their opposites were strong or weak when it was done.", [VSM(3, 104)])
CA_NOT = "Not a personality type in any modern sense and not a fixed label: Vism III itself says the behavioural marks are the teachers' opinion, not authoritative, can be adopted by others, and blur in mixed temperaments; the product never assigns a temperament from behaviour alone and never tells a person what they are."
def carita(slug, name, refs, extra_defs, markers, eq, px):
    A(E(f"dx:carita-{slug}", name, "temperament", G_CA, BL, CA_REFS + refs, [CA_DEF, CA_ORIGIN] + extra_defs + [CA_CAVEAT], markers, CA_NOT, eq=eq, px=px))

carita("raga", "Rāga-carita (greedy temperament)", [], [],
    [("Posture: walks gracefully, putting the foot down and lifting it slowly and evenly, the step springy; stands in a pleasing way; arranges his bed unhurriedly and lies down gracefully; when woken rises quickly but answers slowly.", ["I like to do things slowly and gracefully"], [VSM(3, 104), VSM(3, 105)]),
     ("Work: sweeps carefully and evenly without scattering the sand, as if spreading flowers; work skilful, gentle, even and careful; robe neither too tight nor too loose.", ["I like things done neatly and pleasingly"], [VSM(3, 105), VSM(3, 106)]),
     ("Eating: likes rich, sweet food; eats unhurriedly in round mouthfuls, savouring the tastes, glad when he gets something good.", ["I really savour good food"], [VSM(3, 106)]),
     ("Seeing: looks long at even a slightly pleasing sight as if amazed, fastens on small virtues, overlooks real faults, leaves reluctantly.", ["I notice the good in things and hate to leave them"], [VSM(3, 106)]),
     ("States that often occur: deceit, fraud, pride, evil wishes, great wishes, discontent, vanity, fickleness.", ["I'm never quite satisfied", "I like to be admired"], [VSM(3, 106)])],
    [("dx:root-lobha", "partial", "The temperament is a predominance of greed; greed itself is defined in Vism XIV.", [VSM(3, 101), VSM(14, 468)]),
     ("dx:carita-saddha", "partial", "Vism III: the faithful temperament is akin (sabhāga) to the greedy: as greed seeks sense objects, faith seeks virtue; in behaviour alike, in moral quality opposite.", [VSM(3, 102)]),
     ("dx:guna-rajas", "partial", "Different frameworks: a strand of nature in the Gītā (BhG 14.7, 14.12), a predominance in a person in the Vism; both marked by greed.", [BG('14.12'), VSM(3, 101)])],
    [("px:asubha-bhavana-vism-6", [VSM(3, 114)]), ("px:kayagatasati-32-parts-vism-8", [VSM(3, 114)])])
carita("dosa", "Dosa-carita (hating temperament)", [], [],
    [("Posture: walks as if digging with his toes, putting the foot down and lifting it abruptly, the step dragged; stands stiffly; arranges his bed hastily, flings himself down and lies scowling; when woken rises quickly and answers as if annoyed.", ["I do everything in a rush and bump into things"], [VSM(3, 104), VSM(3, 105)]),
     ("Work: grips the broom tightly and sweeps hurriedly, throwing up sand on both sides with a harsh noise, uncleanly and unevenly; work tense, stiff and uneven; robe too tight.", ["I work fast and hard and it comes out rough"], [VSM(3, 105), VSM(3, 106)]),
     ("Eating: likes rough, sour food; eats hurriedly in mouth-filling lumps without savouring; is displeased when he gets something not good.", ["I don't care about the taste, I just eat fast"], [VSM(3, 106)]),
     ("Seeing: does not look long at even a slightly unpleasing sight, as if tired; picks on small faults, discounts real virtues, leaves without regret.", ["I notice the faults first", "I'm quick to find what's wrong"], [VSM(3, 106)]),
     ("States that often occur: anger, resentment, contempt, domineering, envy, avarice.", ["I hold grudges", "I resent it when others do well"], [VSM(3, 107)])],
    [("dx:root-dosa", "partial", "The temperament is a predominance of hate; hate itself is defined in Vism XIV.", [VSM(3, 101), VSM(14, 470)]),
     ("dx:carita-buddhi", "partial", "Vism III: the intelligent temperament is akin to the hating: as hate shuns beings, understanding shuns formations; alike in behaviour, opposite in quality.", [VSM(3, 102)])],
    [("px:brahmavihara-bhavana-vism-9", [VSM(3, 114)]), ("px:colour-kasina-vism-5", [VSM(3, 114)])])
carita("moha", "Moha-carita (deluded temperament)", [], [],
    [("Posture: walks with an unsteady gait, putting the foot down and lifting it hesitantly, the step pressed down abruptly; stands in a muddled way; arranges his bed badly, lies sprawling, mostly face down; when woken gets up slowly with a grunt.", ["I'm clumsy and slow to get going"], [VSM(3, 104), VSM(3, 105)]),
     ("Work: holds the broom loosely and sweeps turning it this way and that, uncleanly and unevenly; work unskilful, muddled, uneven, undecided; robe loose and untidy.", ["I start things and leave them half done"], [VSM(3, 105), VSM(3, 106)]),
     ("Eating: has no fixed liking; eats in small uneven mouthfuls, dropping bits in the dish, smearing his face, mind astray, thinking of this and that.", ["I eat without noticing, thinking about other things"], [VSM(3, 106)]),
     ("Seeing: depends on others — hearing others blame he blames, hearing them praise he praises; himself indifferent with the indifference of unknowing.", ["I just go along with what others think"], [VSM(3, 106)]),
     ("States that often occur: stiffness, torpor, restlessness, remorse, doubt, holding on tenaciously, refusing to let go.", ["I get stuck and won't let go of my view", "I'm often dull and unsure"], [VSM(3, 107)])],
    [("dx:root-moha", "partial", "The temperament is a predominance of delusion; delusion itself is defined in Vism XIV.", [VSM(3, 101), VSM(14, 468)]),
     ("dx:carita-vitakka", "partial", "Vism III: the speculative temperament is akin to the deluded: as delusion is restless through not penetrating, thought is restless through quick imagining.", [VSM(3, 102)]),
     ("dx:guna-tamas", "partial", "Different frameworks: a strand of nature (BhG 14.8, 14.13), a predominance in a person (Vism III); both marked by delusion and dullness.", [BG('14.8'), VSM(3, 107)])],
    [("px:anapanasati-first-tetrad", [VSM(3, 114), MN118('18')])])
carita("saddha", "Saddhā-carita (faithful temperament)", [],
    [(LIN_TH, "Vism III: in the wholesome moments of one of greedy temperament faith is strong, because faith is close to greed in quality; as greed seeks sense objects, faith seeks the special qualities of virtue and the rest; so the faithful temperament is akin to the greedy.", [VSM(3, 102)])],
    [("Posture, work, eating and seeing: like the greedy temperament, being akin to it.", ["I like things done gracefully"], [VSM(3, 105), VSM(3, 106)]),
     ("States that often occur: generosity with an open hand, wanting to see noble ones, wanting to hear the true Dhamma, much gladness, guilelessness, trust in what inspires trust.", ["I love to hear the teaching", "I feel glad when I meet good people"], [VSM(3, 107)])],
    [("dx:carita-raga", "partial", "Akin in behaviour, opposite in moral quality (Vism III).", [VSM(3, 102)])],
    [("px:six-recollections-vism-7", [VSM(3, 114)])])
carita("buddhi", "Buddhi-carita (intelligent temperament)", [],
    [(LIN_TH, "Vism III: in the wholesome moments of one of hating temperament understanding is strong; as hate shuns beings, understanding shuns formations; so the intelligent temperament is akin to the hating.", [VSM(3, 102)])],
    [("Posture, work, eating and seeing: like the hating temperament, being akin to it.", ["I do things briskly"], [VSM(3, 105), VSM(3, 106)]),
     ("States that often occur: being easy to correct, good friendship, moderation in eating, mindfulness and clear knowing, devotion to wakefulness, a sense of urgency at what should stir it, and striving when so stirred.", ["I take correction well", "I'm moved to act when I see how short life is"], [VSM(3, 107)])],
    [("dx:carita-dosa", "partial", "Akin in behaviour, opposite in moral quality (Vism III).", [VSM(3, 102)])],
    [("px:maranasati-vism-8", [VSM(3, 114)]), ("px:upasamanussati-vism-8", [VSM(3, 114)]), ("px:catudhatuvavatthana-vism-11", [VSM(3, 114)]), ("px:ahare-patikulasanna-vism-11", [VSM(3, 114)])])
carita("vitakka", "Vitakka-carita (speculative temperament)", [],
    [(LIN_TH, "Vism III: in one of deluded temperament who strives to arouse wholesome states, obstructive thoughts mostly arise; as delusion is restless through not penetrating, thought is restless through quick imagining; so the speculative temperament is akin to the deluded.", [VSM(3, 102)])],
    [("Posture, work, eating and seeing: like the deluded temperament, being akin to it.", ["I'm scattered in how I do things"], [VSM(3, 105), VSM(3, 106)]),
     ("States that often occur: much talking, fondness for company, dislike of devotion to the wholesome, unsettledness in what he does, 'fuming by night and flaring by day', running hither and thither.", ["I plan all night and rush about all day", "I talk a lot and can't stick with anything"], [VSM(3, 107)])],
    [("dx:carita-moha", "partial", "Akin in behaviour (Vism III).", [VSM(3, 102)])],
    [("px:anapanasati-first-tetrad", [VSM(3, 114), MN118('18')])])

# ---------------- further Visuddhimagga obstacles ----------------
A(E("dx:vism-palibodha", "Palibodha (the ten impediments)", "obstacle", "the ten impediments (palibodha; Vism III)", BL, ["obs:ten-palibodhas", "trm:palibodha"],
    [(LIN_TH, "Vism III: one who would develop concentration should first sever whichever of the ten impediments he has: a dwelling, a family (of supporters), gain, a following, building work, travel, kin, affliction, books, and supernormal power.", [VSM(3, 90)])],
    [("Ties that take up the time and mind a meditator needs: a dwelling, supporters, gain, a following, building work, travel, kin, affliction, study, powers.", ["my duties leave no room to practise", "I'm always travelling", "my studies crowd out practice"], [VSM(3, 90)])],
    "Not advice to abandon one's family or duties: the Visuddhimagga addresses a monk preparing to take up a meditation subject. 'Affliction' is listed as the text lists it; the product does not assess illness.",
    states=[(n, "Named among the ten impediments (Vism III).", [VSM(3, 90)]) for n in
            ["āvāsa (dwelling)", "kula (family of supporters)", "lābha (gain)", "gaṇa (a following)", "kamma (building work)", "addhāna (travel)", "ñāti (kin)", "ābādha (affliction)", "gantha (books)", "iddhi (supernormal power)"]]))
A(E("dx:vism-vipassanupakkilesa", "Vipassanupakkilesa (the ten imperfections of insight)", "obstacle", "the ten imperfections of insight (Vism XX)", BL, ["obs:ten-vipassanupakkilesas", "obs:sixteen-upakkilesa"],
    [(LIN_TH, "Vism XX: in one who has begun insight ten imperfections arise — not in a noble disciple who has reached penetration, nor in one who has given up his meditation subject or is idle, but in one who practises rightly: illumination, knowledge, rapture, tranquillity, bliss, resolution, exertion, assurance, equanimity and attachment.", [VSM(20, 633)]),
     (LIN_TH, "Taking them for the path — 'surely such a thing never arose before; I have reached the path, reached fruition!' — he mistakes what is not the path for the path, leaves his basic meditation subject and sits enjoying the attachment. They are called imperfections as grounds for imperfection, not because they are unwholesome; but attachment is both an imperfection and its ground.", [VSM(20, 637)]),
     (LIN_TH, "Discerning 'illumination and the rest are not the path; insight knowledge free from imperfections on its course is the path', he defines path and not-path.", [VSM(20, 638)])],
    [("Taking lights, joy, calm and the like for arrival and settling into them (Vism XX).", ["I think I've finally reached the goal because of these lights and joy", "these experiences must mean I'm enlightened"], [VSM(20, 637)])],
    "Not a judgement that light, joy or calm are bad — the Vism says they arise in one who practises rightly — and never a verdict on a person's attainment; not a reading of unusual experiences, which the product does not interpret.",
    states=[(n, "Named among the ten imperfections (Vism XX).", [VSM(20, 633)]) for n in
            ["obhāsa (illumination)", "ñāṇa (knowledge)", "pīti (rapture)", "passaddhi (tranquillity)", "sukha (bliss)", "adhimokkha (resolution)", "paggaha (exertion)", "upaṭṭhāna (assurance)", "upekkhā (equanimity)", "nikanti (attachment)"]],
    eq=[("dx:gk-rasasvada", "partial", "Gauḍapāda: do not savour the happiness of stillness (GK 3.45); Vism: attachment to these states is the imperfection that is also unwholesome (Vism XX).", [GK('3.45'), VSM(20, 637)]),
        ("dx:siddhi-upasarga", "partial", "YS 3.37 calls powers obstacles in samādhi; the Vism calls lights and bliss imperfections when taken for the path.", [YS('3.37'), VSM(20, 637)])],
    px=[("px:maggamagga-vavatthana-vism-20", [VSM(20, 638)])]))
A(E("dx:vism-brahmavihara-enemies", "Near and far enemies of the divine abidings", "obstacle", "near and far enemies of the divine abidings (Vism IX)", BL, ["cpt:four-brahmaviharas", "trm:brahmavihara"],
    [(LIN_TH, "Vism IX: each divine abiding has a near enemy that resembles it and a far enemy that is its opposite. Greed is the near enemy of loving-kindness, since both see virtues; ill will is its far enemy. Home-based grief is the near enemy of compassion, cruelty its far enemy. Home-based joy is the near enemy of gladness, aversion (boredom) its far enemy. The home-based equanimity of unknowing is the near enemy of equanimity; greed and resentment are its far enemies. Loving-kindness is the escape from ill will.", [VSM(9, 318), VSM(9, 319)])],
    [("Kindness sliding into attachment; compassion into one's own grief; gladness into worldly joy; equanimity into the indifference of not knowing (Vism IX).", ["my kindness toward them has turned into clinging", "my compassion has become my own misery", "I call it equanimity but really I just don't care"], [VSM(9, 319)])],
    "Not a charge that a person's kindness is false and not a medical matter: the Vism names these so that the divine abidings are guarded.",
    states=[("mettā", "Near enemy: greed. Far enemy: ill will.", [VSM(9, 319)]), ("karuṇā", "Near enemy: home-based grief. Far enemy: cruelty.", [VSM(9, 319)]),
            ("muditā", "Near enemy: home-based joy. Far enemy: aversion (boredom).", [VSM(9, 319)]), ("upekkhā", "Near enemy: home-based equanimity of unknowing. Far enemies: greed and resentment.", [VSM(9, 319)])],
    px=[("px:brahmavihara-bhavana-vism-9", [VSM(9, 318), VSM(9, 319)])]))
