"""Gita, Taittiriya, Mandukya, Gaudapada and Katha entries."""
from common import *

VL = 'vedic-yogic'
ENTRIES = []
A = ENTRIES.append

# ---------------- three gunas (Gita 14) ----------------
G_GU = 'the three guṇas (BhG 14.5)'
GU_DEF = (LIN_GITA, "Sattva, rajas and tamas are the guṇas born of nature (prakṛti); they bind the imperishable embodied one in the body (BhG 14.5). Now one prevails, now another, overpowering the other two (BhG 14.10).", [BG('14.5'), BG('14.10')])
GU_YS = (LIN_YOGA, "The Yoga Sūtra describes the seen (prakṛti) as having the nature of illumination, activity and inertia (prakāśa, kriyā, sthiti) — the three guṇas' characters — existing for experience and liberation (YS 2.18).", [YS('2.18'), YB('2.18')])
PX_GU = [("px:guna-witnessing-bg-14-19-23", [BG('14.19'), BG('14.23')]), ("px:bhakti-yoga-bg-14-26", [BG('14.26')])]
GU_REFS = ["cpt:three-gunas", "trm:guna"]

A(E("dx:guna-sattva", "Sattva (clarity)", "guna", G_GU, VL, GU_REFS + ["trm:sattva"],
    [(LIN_GITA, "Sattva, being stainless, is illuminating and free from affliction; yet it binds, by attachment to happiness and attachment to knowledge (BhG 14.6); it attaches to happiness (14.9); from it knowledge arises (14.17); those established in it go upward (14.18).", [BG('14.6'), BG('14.9'), BG('14.17'), BG('14.18')]), GU_DEF, GU_YS],
    [("When light, knowledge, arises in all the gates of the body, sattva has grown (BhG 14.11).", ["things are clear to me", "I see and understand plainly"], [BG('14.11')]),
     ("The sāttvika doer: free of attachment, not boasting of 'I', full of steadiness and zeal, unchanged by success or failure (BhG 18.26).", ["I did my part and I'm steady whether it works out or not"], [BG('18.26')]),
     ("Sāttvika happiness: like poison at first and like nectar at the end, born of the clarity of one's own understanding (BhG 18.37).", ["it was hard at first but it has become a deep contentment"], [BG('18.37')])],
    "Not simply 'good' and not a finished state: the Gītā says sattva too binds, by attachment to happiness and to knowledge (BhG 14.6). Not a personality type and not a label for a person; the guṇas shift from moment to moment (BhG 14.10).",
    eq=[("dx:guna-rajas", "partial", "The guṇas are not separate things in a person but three strands that overpower one another in turn (BhG 14.10).", [BG('14.10')])],
    px=PX_GU))

A(E("dx:guna-rajas", "Rajas (passion, activity)", "guna", G_GU, VL, GU_REFS + ["trm:rajas"],
    [(LIN_GITA, "Rajas has the nature of passion (rāgātmaka), springing from craving and attachment; it binds by attachment to action (BhG 14.7); it attaches to action (14.9); from it greed arises (14.17); those in rajas stay in the middle (14.18). Desire and anger are born of the guṇa rajas (3.37).", [BG('14.7'), BG('14.9'), BG('14.17'), BG('14.18'), BG('3.37')]), GU_DEF, GU_YS],
    [("When rajas grows: greed, busy activity, the undertaking of actions, unrest, longing (BhG 14.12).", ["I can't stop taking on more", "I'm restless and always want the next thing", "I keep starting new projects"], [BG('14.12')]),
     ("The rājasa doer: passionate, eager for the fruit of action, greedy, harmful, impure, swept by joy and grief (BhG 18.27).", ["I only care whether I get the result", "I swing between elation and grief over how it goes"], [BG('18.27')]),
     ("Rājasa happiness: from the meeting of senses and objects, like nectar at first and like poison in the end (BhG 18.38).", ["it felt wonderful at first and now it's turned sour"], [BG('18.38')])],
    "Not a personality type and not a medical condition; not a condemnation of activity as such. The Gītā describes rajas as one of three strands of nature that bind (BhG 14.5, 14.7).",
    eq=[("dx:carita-raga", "partial", "The Gītā's rajas is a strand of nature in all beings, marked by greed and passion (BhG 14.7, 14.12); the Vism's greedy temperament is a predominance of greed in a person's make-up, marked by posture, work, eating and seeing (Vism III). Different frameworks; both marked by greed.", [BG('14.12'), VSM(3, 101), VSM(3, 104)]),
        ("dx:gita-kama-krodha", "partial", "Desire and anger are born of rajas (BhG 3.37).", [BG('3.37')])],
    px=PX_GU))

A(E("dx:guna-tamas", "Tamas (darkness, inertia)", "guna", G_GU, VL, GU_REFS + ["trm:tamas"],
    [(LIN_GITA, "Tamas is born of ignorance and deludes all embodied beings; it binds by heedlessness, laziness and sleep (BhG 14.8); covering knowledge, it attaches to heedlessness (14.9); from it come heedlessness, delusion and ignorance (14.17); those in it go downward (14.18).", [BG('14.8'), BG('14.9'), BG('14.17'), BG('14.18')]), GU_DEF, GU_YS],
    [("When tamas grows: darkness, inactivity, heedlessness, delusion (BhG 14.13).", ["everything feels murky and I can't get moving", "I keep neglecting what matters", "I feel confused and inert"], [BG('14.13')]),
     ("The tāmasa doer: unsteady, coarse, obstinate, deceitful, malicious, lazy, despondent, procrastinating (BhG 18.28).", ["I keep putting it off", "I dig in my heels and won't budge", "I've lost heart and let it drift"], [BG('18.28')]),
     ("Tāmasa steadiness: the kind by which one does not let go of sleep, fear, grief, despondency and pride (BhG 18.35); tāmasa happiness deludes at the start and after, arising from sleep, laziness and heedlessness (18.39).", ["I cling to sleep and my grievances", "I take comfort in just switching off"], [BG('18.35'), BG('18.39')])],
    "Not a medical condition and never a diagnosis of low mood; not a label for a person. The Gītā describes tamas as one of three strands of nature binding every embodied being (BhG 14.5, 14.8).",
    eq=[("dx:carita-moha", "partial", "The Gītā's tamas is a strand of nature marked by delusion, heedlessness, laziness and sleep (BhG 14.8, 14.13); the Vism's deluded temperament is a predominance of delusion in a person, with stiffness, torpor and doubt among its frequent states (Vism III). Different frameworks.", [BG('14.8'), VSM(3, 107)]),
        ("dx:gk-laya", "partial", "Gauḍapāda's laya is the mind dissolving as in sleep during stilling (GK 3.35, 3.44); tamas binds by sleep (BhG 14.8).", [BG('14.8'), GK('3.44')]),
        ("dx:antaraya-alasya", "partial", "Laziness is a bond of tamas (BhG 14.8) and a Yoga obstacle defined by heaviness (YB 1.30).", [BG('14.8'), YB('1.30')]),
        ("dx:antaraya-pramada", "partial", "Heedlessness is a bond of tamas (BhG 14.8); Vyāsa defines it as not cultivating the means of samādhi.", [BG('14.8'), YB('1.30')])],
    px=PX_GU))

A(E("dx:gunatita", "Guṇātīta (one gone beyond the guṇas)", "state", "the marks of one beyond the guṇas (BhG 14.21–26)", VL,
    ["cpt:gunatita", "phn:marks-of-gunatita", "trm:gunatita"],
    [(LIN_GITA, "One who does not hate illumination, activity or delusion when they arise, nor long for them when they cease; who sits as if indifferent, unshaken by the guṇas, knowing 'the guṇas are acting'; the same in pain and pleasure, praise and blame, honour and dishonour, toward friend and foe, giving up all self-started undertakings — is said to have gone beyond the guṇas (BhG 14.22–25). One who serves me with unswerving devotion goes beyond them (14.26).", [BG('14.22'), BG('14.23'), BG('14.24'), BG('14.25'), BG('14.26')])],
    [("Not hating the play of the guṇas when present, not longing for it when gone; steady, knowing 'the guṇas are acting' (BhG 14.22–23).", [], [BG('14.22'), BG('14.23')])],
    "Never a label to attach to a person and never a verdict on attainment: the product does not tell anyone they are beyond the guṇas. Listed so that the Gītā's picture of the goal is available beside the obstacles.",
    px=PX_GU))

# ---------------- Gita obstacles ----------------
A(E("dx:gita-anger-chain", "The chain from dwelling on objects to ruin", "obstacle", "the chain of BhG 2.62–63", VL,
    ["obs:anger", "trm:krodha", "trm:sanga", "trm:kama", "obs:sanga-attachment"],
    [(LIN_GITA, "For one who dwells on sense objects, attachment to them arises; from attachment desire is born; from desire, anger; from anger comes delusion; from delusion, confusion of memory; from the loss of memory, the ruin of understanding; from the ruin of understanding one perishes (BhG 2.62–63). But one who moves among objects with senses free of attachment and aversion and under control attains clarity (prasāda) (2.64), and in clarity all sorrows end (2.65).", [BG('2.62'), BG('2.63'), BG('2.64'), BG('2.65')])],
    [("Turning an object over and over in the mind until attachment and desire form.", ["I can't stop thinking about it and now I really want it"], [BG('2.62')]),
     ("Anger born of desire, then clouding: losing track of what one knows, and judgement failing.", ["I got so angry I forgot everything I know", "my judgement just went"], [BG('2.62'), BG('2.63')])],
    "Not a prediction about a person's future and not a claim about any medical process: it is the Gītā's own sequence from dwelling on objects to ruin, given so that it can be cut early (BhG 2.64).",
    states=[("dhyāna of objects", "Dwelling on sense objects.", [BG('2.62')]), ("saṅga", "Attachment arises.", [BG('2.62')]), ("kāma", "Desire is born of attachment.", [BG('2.62')]),
            ("krodha", "Anger is born of desire.", [BG('2.62')]), ("saṃmoha", "Delusion comes from anger.", [BG('2.63')]), ("smṛti-vibhrama", "Confusion of memory comes from delusion.", [BG('2.63')]),
            ("buddhi-nāśa", "Ruin of understanding comes from loss of memory.", [BG('2.63')]), ("praṇāśa", "From the ruin of understanding one perishes.", [BG('2.63')])],
    eq=[("dx:gita-kama-krodha", "exact", "The same desire and anger of the Gītā, here shown as links in a chain (BhG 2.62–63) and there named as the one enemy (3.37).", [BG('2.62'), BG('3.37')]),
        ("dx:klesa-raga", "partial", "YS rāga follows remembered pleasure (YS 2.7); the Gītā's attachment and desire grow from dwelling on objects (BhG 2.62).", [BG('2.62'), YS('2.7')])],
    px=[("px:indriya-samyama-bg-2-58-61", [BG('2.58'), BG('2.61'), BG('2.64')])]))

A(E("dx:gita-kama-krodha", "Kāma-krodha (desire and anger, the enemy)", "obstacle", "desire-anger, the enemy born of rajas (BhG 3.37)", VL,
    ["obs:kama", "obs:anger", "trm:kama", "trm:krodha", "trm:lobha", "obs:lobha-krodha-moha"],
    [(LIN_GITA, "Asked what drives a person to wrong even against his will, as if by force (BhG 3.36), Kṛṣṇa answers: it is desire, it is anger, born of the guṇa rajas, all-devouring, greatly evil — know it as the enemy here (3.37). As smoke covers fire, dust a mirror and the womb the embryo, it covers knowledge (3.38–39); the senses, mind and understanding are its seat (3.40). Desire, anger and greed are the threefold gate of hell, destroying the self; give them up (16.21).", [BG('3.36'), BG('3.37'), BG('3.38'), BG('3.39'), BG('3.40'), BG('16.21')])],
    [("Acting wrongly against one's own wish, as if pushed by force (BhG 3.36).", ["I did it even though I didn't want to", "something takes over and I act against myself"], [BG('3.36')]),
     ("A fire that cannot be filled, covering knowledge as smoke covers fire (BhG 3.38–39).", ["no amount is ever enough", "it clouds everything I know"], [BG('3.38'), BG('3.39')]),
     ("The surge (vega) born of desire and anger; one who can bear it here, before leaving the body, is joined in yoga and happy (BhG 5.23).", ["the urge rises up and I have to ride it out"], [BG('5.23')])],
    "Not a condemnation of all wanting or of all anger as such, and not a medical condition: the Gītā names desire-anger born of rajas as the enemy that covers knowledge (BhG 3.37–39).",
    eq=[("dx:guna-rajas", "partial", "Born of rajas (BhG 3.37).", [BG('3.37')]),
        ("dx:klesa-dvesa", "partial", "Vyāsa counts anger within dveṣa, following remembered pain (YB 2.8); the Gītā derives anger from desire (BhG 2.62).", [YB('2.8'), BG('2.62')]),
        ("dx:kasaya-krodha", "partial", "Jain anger is a passion that makes the soul take in karmic matter (TS 8.2, 8.9); the Gītā's anger is born of rajas and covers knowledge.", [BG('3.37'), TS('8.9')]),
        ("dx:root-dosa", "partial", "Theravāda dosa is ferocity, a root of the unwholesome (Vism XIV); the Gītā's anger is born of desire and of rajas.", [BG('3.37'), VSM(14, 470)])],
    px=[("px:indriya-samyama-bg-2-58-61", [BG('3.41'), BG('2.61')]), ("px:bearing-the-surge-bg-5-23", [BG('5.23')])]))

A(E("dx:gita-asuri-sampad", "Āsurī sampad (the demonic endowment)", "obstacle", "the demonic endowment (BhG 16.4)", VL,
    ["trm:krodha"],
    [(LIN_GITA, "Hypocrisy, arrogance, conceit, anger, harshness and ignorance belong to one born to the demonic endowment (BhG 16.4); it leads to bondage (16.5).", [BG('16.4'), BG('16.5')])],
    [("Hypocrisy, arrogance, conceit, anger, harshness, ignorance (BhG 16.4).", ["I put on a show of being good", "I look down on them", "I spoke harshly and didn't care"], [BG('16.4')])],
    "Not a verdict that a person is demonic and not a label for anyone: the Gītā lists qualities to be recognised and left, and says Arjuna himself was born to the divine endowment (BhG 16.5).",
    eq=[("dx:kasaya-mana", "partial", "Jain pride (māna) is one of four passions (TS 8.9); the Gītā lists arrogance and conceit (darpa, abhimāna) among demonic qualities.", [BG('16.4'), TS('8.9')]),
        ("dx:kasaya-maya", "partial", "Jain deceit (māyā) and the Gītā's hypocrisy (dambha) overlap in showing what one is not.", [BG('16.4'), TS('8.9')]),
        ("dx:fetter-mana", "partial", "Theravāda conceit is haughtiness and self-exaltation (Vism XIV).", [BG('16.4'), VSM(14, 469)])]))

A(E("dx:gita-visada", "Viṣāda and kārpaṇya (Arjuna's dejection)", "state", "Arjuna's dejection (BhG 1.28–2.9)", VL,
    ["obs:visada", "trm:visada", "trm:karpanya"],
    [(LIN_GITA, "Seeing his own kin ready to fight, Arjuna, overcome with pity and sinking, speaks (BhG 1.28): his limbs give way, his mouth dries, his body trembles and his hair stands on end (1.29); his bow slips from his hand, his skin burns, he cannot stand, his mind seems to whirl (1.30). Then: 'my nature struck by the fault of weakness (kārpaṇya), my mind confused about dharma, I ask you: tell me for certain what is better; I am your disciple, teach me, I have come to you' (2.7).", [BG('1.28'), BG('1.29'), BG('1.30'), BG('2.7')])],
    [("Sinking before a duty that seems unbearable, not knowing what is right.", ["I can't go on with what I have to do", "I no longer know what the right thing is"], [BG('1.28'), BG('2.7')]),
     ("The body giving way with the mind whirling, as the text narrates it (BhG 1.29–30).", ["my limbs give way when I think of it", "my mind is spinning and I can't stand firm"], [BG('1.29'), BG('1.30')]),
     ("Turning to a teacher: 'teach me, I have come to you' (BhG 2.7).", ["I need someone to tell me clearly what to do"], [BG('2.7')])],
    "Never a diagnosis or a medical condition: the Gītā presents Arjuna's collapse as the starting point of the teaching, not as something wrong with him. The bodily signs are the text's narrative, not medical signs; if a person describes serious distress, the product does not interpret it and points them to people who can help.",
    eq=[("dx:companion-daurmanasya", "partial", "Vyāsa's dejection is the mind's agitation when a wish is thwarted (YB 1.31); Arjuna's viṣāda is a collapse before a duty, confused about dharma (BhG 2.7).", [YB('1.31'), BG('2.7')])],
    px=[("px:approach-a-teacher-bg-4-34", [BG('2.7'), BG('4.34')]), ("px:atma-anatma-viveka-bg-2-11-30", [BG('2.11')])]))

A(E("dx:gita-restless-mind", "Cañcala manas (the restless mind)", "obstacle", "the restless mind and turbulent senses (BhG 6.34, 2.60, 2.67)", VL,
    ["obs:manas-cancalya", "phn:bhagavad-gita-senses-carry-off-mind", "obs:turbulent-senses"],
    [(LIN_GITA, "Arjuna: the mind is restless, turbulent, strong and obstinate; I think it as hard to hold as the wind (BhG 6.34). Kṛṣṇa: no doubt the mind is hard to hold and moving, but it is held by practice and dispassion (6.35). The turbulent senses carry off by force the mind even of a wise man who strives (2.60); the mind that follows the roving senses carries off understanding as the wind a ship on the water (2.67).", [BG('6.34'), BG('6.35'), BG('2.60'), BG('2.67')])],
    [("The mind moving off wherever it will, restless and unsteady (BhG 6.26, 6.34).", ["my mind won't stay put", "holding my mind is like holding the wind"], [BG('6.26'), BG('6.34')]),
     ("The senses dragging the mind after objects, carrying understanding away (BhG 2.60, 2.67).", ["my senses pull me away even when I know better"], [BG('2.60'), BG('2.67')])],
    "Not a medical condition of any kind: the Gītā treats the restless mind as the ordinary state of the untrained mind, to be held by practice and dispassion (BhG 6.35).",
    eq=[("dx:nivarana-uddhacca-kukkucca", "partial", "Theravāda restlessness is disquiet, like water whipped by wind (Vism XIV); the Gītā's mind is as hard to hold as the wind (BhG 6.34). Similar image, different frameworks.", [BG('6.34'), VSM(14, 469)]),
        ("dx:gk-viksepa", "partial", "Gauḍapāda's distraction is the mind scattered among desires and enjoyments, to be calmed (GK 3.42, 3.44).", [BG('6.34'), GK('3.44')]),
        ("dx:katha-unrestrained-senses", "partial", "The Kaṭha's senses run like vicious horses when the mind is unyoked (KU 1.3.5); the Gītā's turbulent senses carry off the mind (BhG 2.60).", [BG('2.60'), KU('1.3.5')])],
    px=[("px:abhyasa-vairagya-bg-6-35", [BG('6.35')]), ("px:returning-the-mind-bg-6-26", [BG('6.26')])]))

A(E("dx:gita-sthitaprajna", "Sthitaprajña (one of steady wisdom)", "state", "the marks of one of steady wisdom (BhG 2.55–72)", VL,
    ["cpt:sthitaprajna", "phn:bhagavad-gita-sthitaprajna-marks", "trm:sthitaprajna"],
    [(LIN_GITA, "When one gives up all desires that come to the mind and is content in the self by the self, one is called of steady wisdom (BhG 2.55): unshaken in sorrow, without craving in pleasures, free of passion, fear and anger (2.56); withdrawing the senses from their objects as a tortoise its limbs (2.58); into whom desires flow as waters into the full, unmoving ocean (2.70).", [BG('2.55'), BG('2.56'), BG('2.58'), BG('2.70')])],
    [("Unshaken in sorrow, without craving in pleasure, free of passion, fear and anger (BhG 2.56).", [], [BG('2.56')])],
    "Never a verdict on a person's attainment and never a standard to shame anyone with: the product does not tell a person they are or are not of steady wisdom. Listed so that the Gītā's picture of the goal is available beside the obstacles.",
    px=[("px:indriya-samyama-bg-2-58-61", [BG('2.58'), BG('2.61')])]))

# ---------------- five sheaths (TU 2.1-2.5) ----------------
G_SH = 'the five sheaths (TU 2.1–2.5)'
SH_NOT = " TU itself speaks of five 'selves' (ātman) made of food, breath, mind, understanding and bliss, each filled by the one within; 'sheath' (kośa) is the later Vedānta name. Not an anatomy, not an energy map and not a medical statement."
SH_REFS = ["cpt:five-sheaths", "trm:kosa"]
def sheath(slug, name, refs, defs, marker, cues, mcites, bhrgu_ref, not_read, eq=None):
    A(E(f"dx:sheath-{slug}", name, "sheath", G_SH, VL, SH_REFS + refs, defs, [(marker, cues, mcites)], not_read + SH_NOT, eq=eq,
        px=[("px:bhrgu-inquiry-tu-3", [TU('3.1.1'), TU(bhrgu_ref)])]))

sheath("annamaya", "Annamaya (the self made of food)", ["trm:annamaya", "trm:annamaya-kosa"],
    [(LIN_UPA, "From the self came space, air, fire, water, earth, plants, food; from food the person. This person is made of the essence of food; this is its head, its right side, its left side, its trunk, its tail and support (TU 2.1.1). From food creatures are born, by food they live, into food they go at the end (TU 2.2.1).", [TU('2.1.1'), TU('2.2.1')])],
    "The body taken as oneself: born of food, living by food, returning to food.", ["I am this body", "when my body is tired, I am finished"], [TU('2.1.1'), TU('2.2.1')], '3.2.1',
    "Not a claim about diet or bodily care: the Upaniṣad names the body as the outermost self in order to lead inward.",
    eq=[("dx:katha-unrestrained-senses", "partial", "The Kaṭha calls the body the chariot of the self (KU 1.3.3); the Taittirīya calls it the self made of food (TU 2.1.1).", [KU('1.3.3'), TU('2.1.1')])])
sheath("pranamaya", "Prāṇamaya (the self made of breath)", ["trm:pranamaya", "trm:pranamaya-kosa"],
    [(LIN_UPA, "Other than and within the self made of food is the self made of breath (prāṇa), which fills it and is also of human shape: prāṇa is its head, vyāna its right side, apāna its left side, space its trunk, earth its tail and support (TU 2.2.1). Gods, humans and animals breathe after breath; breath is the life-span of beings (TU 2.3.1).", [TU('2.2.1'), TU('2.3.1')])],
    "Oneself taken as breath, vitality and life-span.", ["I'm only as alive as my vitality", "when my strength goes, I go"], [TU('2.2.1'), TU('2.3.1')], '3.3.1',
    "Not a breath technique and not an energy diagnosis: the product never suggests breath control from this entry.",
    eq=[("dx:vital-prana", "partial", "In TU 2.2.1 prāṇa is the head of the self made of breath; Vyāsa locates prāṇa in mouth and nose up to the heart (YB 3.39).", [TU('2.2.1'), YB('3.39')])])
sheath("manomaya", "Manomaya (the self made of mind)", ["trm:manomaya", "trm:manomaya-kosa"],
    [(LIN_UPA, "Within the self made of breath is the self made of mind: the Yajus is its head, the Ṛc its right side, the Sāman its left side, instruction (ādeśa) its trunk, the Atharvāṅgiras its tail and support (TU 2.3.1). 'From which words turn back, with the mind, not reaching it — one who knows the bliss of brahman fears nothing' (TU 2.4.1).", [TU('2.3.1'), TU('2.4.1')])],
    "Oneself taken as the mind of words, wishes and thoughts.", ["I am my thoughts", "whatever I think, that's me"], [TU('2.3.1')], '3.4.1',
    "Not a judgement of a person's thinking.",
    eq=[("dx:katha-unrestrained-senses", "partial", "In the Kaṭha the mind is the reins (KU 1.3.3); in the Taittirīya the self made of mind is the third 'self'.", [KU('1.3.3'), TU('2.3.1')])])
sheath("vijnanamaya", "Vijñānamaya (the self made of understanding)", ["trm:vijnanamaya", "trm:vijnanamaya-kosa"],
    [(LIN_UPA, "Within the self made of mind is the self made of understanding: faith (śraddhā) is its head, right order (ṛta) its right side, truth (satya) its left side, yoga its trunk, greatness (mahas) its tail and support (TU 2.4.1). Understanding performs the sacrifice and the rites; if one knows understanding as brahman and does not swerve from it, leaving evils in the body, one attains all desires (TU 2.5.1).", [TU('2.4.1'), TU('2.5.1')])],
    "Oneself taken as the one who understands, decides and acts.", ["I am the one who knows and decides", "my judgement is who I really am"], [TU('2.4.1'), TU('2.5.1')], '3.5.1',
    "Not a test of intelligence.",
    eq=[("dx:katha-unrestrained-senses", "partial", "In the Kaṭha understanding (buddhi) is the charioteer (KU 1.3.3); in the Taittirīya the self made of understanding is the fourth 'self'.", [KU('1.3.3'), TU('2.4.1')])])
sheath("anandamaya", "Ānandamaya (the self made of bliss)", ["trm:anandamaya", "trm:anandamaya-kosa"],
    [(LIN_UPA, "Within the self made of understanding is the self made of bliss: the dear (priya) is its head, delight (moda) its right side, great delight (pramoda) its left side, bliss (ānanda) its trunk, brahman its tail and support (TU 2.5.1). One who knows the bliss of brahman fears nothing and is not troubled by 'why did I not do good, why did I do evil' (TU 2.9.1).", [TU('2.5.1'), TU('2.9.1')])],
    "Oneself taken as the joy of what is dear and delightful.", ["in my deepest joy I feel most myself"], [TU('2.5.1')], '3.6.1',
    "Not a promise of bliss and not a verdict on anyone's attainment.",
    eq=[("dx:state-susupta", "partial", "The Māṇḍūkya calls the deep-sleep self (prājña) 'made of bliss, enjoyer of bliss' (MāU 5); the Taittirīya's self made of bliss is the innermost of the five, with brahman as its support.", [MU('5'), TU('2.5.1')])])

# ---------------- five vital currents ----------------
G_VC = 'the five vital currents (TU 1.7.1; Vyāsa on YS 3.39)'
VC_NOT = "Not a physiological, medical or energy map and not a basis for any breath technique: the core texts only name and locate these currents. The product never suggests breath control or 'mastery' from this entry; the powers YS 3.39–40 ascribe to mastering udāna and samāna are summary only."
VC_REFS = ["cpt:five-pranas", "trm:prana"]
VC_DEF_TU = (LIN_UPA, "TU 1.7.1 names prāṇa, vyāna, apāna, udāna and samāna as the inner (adhyātma) fivefold, alongside eye, ear, mind, speech and touch.", [TU('1.7.1')])
VC_DEF_YB = (LIN_YOGA, "Vyāsa: life is the working of all the senses, marked by prāṇa and the rest; its action is fivefold, and prāṇa is the chief.", [YS('3.39'), YB('3.39')])
def vital(slug, name, refs, yb_text, extra_defs, marker, mcites, eq=None):
    A(E(f"dx:vital-{slug}", name, "vital-current", G_VC, VL, VC_REFS + refs,
        [(LIN_YOGA, yb_text, [YB('3.39')]), VC_DEF_YB, VC_DEF_TU] + extra_defs,
        [(marker, [], mcites)], VC_NOT, eq=eq))

vital("prana", "Prāṇa (the forward breath)", ["trm:prana"],
    "Prāṇa moves through mouth and nose and works as far as the heart.",
    [(LIN_UPA, "Prāṇa is the head of the self made of breath (TU 2.2.1). The self leads prāṇa upward and casts apāna downward (KU 2.2.3).", [TU('2.2.1'), KU('2.2.3')])],
    "Located by Vyāsa in mouth and nose, working as far as the heart; led upward (KU 2.2.3).", [YB('3.39'), KU('2.2.3')],
    eq=[("dx:sheath-pranamaya", "partial", "Prāṇa is the head of the self made of breath (TU 2.2.1).", [TU('2.2.1')])])
vital("apana", "Apāna (the downward breath)", ["trm:apana"],
    "Apāna, so called from leading away (apanayana), works as far as the soles of the feet.",
    [(LIN_UPA, "Apāna is the left side of the self made of breath (TU 2.2.1); it is cast downward (KU 2.2.3).", [TU('2.2.1'), KU('2.2.3')])],
    "Located by Vyāsa as working as far as the soles of the feet; cast downward (KU 2.2.3).", [YB('3.39'), KU('2.2.3')],
    eq=[("dx:sheath-pranamaya", "partial", "Apāna is the left side of the self made of breath (TU 2.2.1).", [TU('2.2.1')])])
vital("samana", "Samāna (the equalising breath)", ["trm:samana"],
    "Samāna, so called from leading evenly (samaṃ nayana), works as far as the navel.",
    [], "Located by Vyāsa as working as far as the navel.", [YB('3.39')])
vital("udana", "Udāna (the upward breath)", ["trm:udana"],
    "Udāna, so called from leading upward (unnayana), works as far as the head.",
    [], "Located by Vyāsa as working up to the head.", [YB('3.39')])
vital("vyana", "Vyāna (the pervading breath)", ["trm:vyana"],
    "Vyāna is the pervading one (vyāpin).",
    [(LIN_UPA, "Vyāna is the right side of the self made of breath (TU 2.2.1).", [TU('2.2.1')])],
    "Described by Vyāsa as pervading.", [YB('3.39')],
    eq=[("dx:sheath-pranamaya", "partial", "Vyāna is the right side of the self made of breath (TU 2.2.1).", [TU('2.2.1')])])

# ---------------- Mandukya states ----------------
G_MU = 'the four quarters of the self (MāU 2–7)'
MU_DEF = (LIN_UPA, "All this is brahman; this self is brahman; this self has four quarters (MāU 2).", [MU('2')])
PX_MU = [("px:omkara-upasana-mau-8-12", [MU('8'), MU('12')])]
MU_REFS = ["cpt:four-states-and-turya"]
A(E("dx:state-jagrat", "Jāgarita (waking; Vaiśvānara)", "state-of-consciousness", G_MU, VL, MU_REFS + ["trm:jagrat", "trm:vaisvanara"],
    [(LIN_UPA, "The first quarter is Vaiśvānara, whose place is waking: outward-knowing, with seven limbs and nineteen mouths, enjoying the gross (MāU 3).", [MU('3')]), MU_DEF,
     (LIN_GK, "Gauḍapāda: the waking and dream selves are joined with dream and sleep; dream belongs to one who grasps things otherwise than they are, sleep to one who does not know the real (GK 1.14–15).", [GK('1.14'), GK('1.15')])],
    [("Knowing turned outward, taking in the gross world (MāU 3).", ["I'm caught up in the world out there"], [MU('3')])],
    "Not 'being awake' as the highest state: Gauḍapāda counts waking as bound up with dream and sleep (GK 1.14). Not a medical state of alertness.",
    px=PX_MU))
A(E("dx:state-svapna", "Svapna (dream; Taijasa)", "state-of-consciousness", G_MU, VL, MU_REFS + ["trm:svapna", "trm:taijasa"],
    [(LIN_UPA, "The second quarter is Taijasa, whose place is dream: inward-knowing, with seven limbs and nineteen mouths, enjoying the subtle (MāU 4).", [MU('4')]), MU_DEF,
     (LIN_GK, "Gauḍapāda: dream is grasping things otherwise than they are (GK 1.15).", [GK('1.15')])],
    [("Knowing turned inward, living among images from within (MāU 4).", ["in the dream I lived among images from inside me"], [MU('4')])],
    "Not dream interpretation: the product never reads meanings into a person's dreams. Not a medical matter.",
    px=PX_MU))
A(E("dx:state-susupta", "Suṣupta (deep sleep; Prājña)", "state-of-consciousness", G_MU, VL, MU_REFS + ["cpt:deep-sleep", "trm:susupti", "trm:prajna-mandukya"],
    [(LIN_UPA, "Where the sleeper desires no desire and sees no dream, that is deep sleep. The third quarter is Prājña, whose place is deep sleep: become one, a mass of knowing, made of bliss, enjoying bliss, with thought as its mouth (MāU 5). This is the lord of all, the knower of all, the inner controller, the source of all, the arising and passing away of beings (MāU 6).", [MU('5'), MU('6')]), MU_DEF,
     (LIN_GK, "Gauḍapāda: Prājña is joined with sleep without dream; sleep belongs to one who does not know the real (GK 1.14–15). In deep sleep the mind dissolves; the restrained mind does not dissolve (GK 3.35).", [GK('1.14'), GK('1.15'), GK('3.35')])],
    [("Sleep in which nothing is desired and no dream is seen (MāU 5).", ["I slept and knew nothing, wanted nothing, saw no dreams"], [MU('5')])],
    "Not a sleep assessment and not a medical matter. Not the goal: Gauḍapāda distinguishes the dissolving of mind in sleep from the restrained mind that does not dissolve (GK 3.35).",
    eq=[("dx:vrtti-nidra", "partial", "YS counts sleep as a modification of mind to be stilled (YS 1.10); the Māṇḍūkya makes deep sleep a quarter of the self (MāU 5).", [YS('1.10'), MU('5')]),
        ("dx:sheath-anandamaya", "partial", "Prājña is 'made of bliss' (MāU 5), as the innermost self of the Taittirīya is (TU 2.5.1).", [MU('5'), TU('2.5.1')]),
        ("dx:gk-laya", "partial", "Gauḍapāda's laya is the mind dissolving as it does in deep sleep (GK 3.35, 3.44).", [GK('3.35'), GK('3.44')])],
    px=PX_MU))
A(E("dx:state-turiya", "Turīya (the fourth)", "state-of-consciousness", G_MU, VL, MU_REFS + ["cpt:turiya", "trm:turiya", "phn:mandukya-the-fourth"],
    [(LIN_UPA, "Not inward-knowing, not outward-knowing, not both, not a mass of knowing, not knowing, not unknowing; unseen, beyond dealings, ungraspable, without marks, unthinkable, unnameable; its essence the knowing of the one self, the stilling of the world, peaceful, auspicious, non-dual — this they consider the fourth; this is the self, this is to be known (MāU 7).", [MU('7')]), MU_DEF,
     (LIN_GK, "Gauḍapāda: in the fourth, those who are certain see neither sleep nor dream; when the errors of dream and sleep are gone one reaches the fourth (GK 1.14–15).", [GK('1.14'), GK('1.15')])],
    [("Described only by negation: neither inward- nor outward-knowing, the stilling of the world (MāU 7).", [], [MU('7')])],
    "Never a label for a person's experience: the product does not certify states or tell anyone they have reached the fourth. MāU 7 describes it by negation; it is not a trance or a special feeling to be sought.",
    eq=[("dx:gk-amanibhava", "partial", "Gauḍapāda's no-mind state is brahman when the mind neither dissolves nor scatters (GK 3.46); the fourth is described by negation (MāU 7). Both in the Advaita reading of the Māṇḍūkya.", [MU('7'), GK('3.46')])],
    px=PX_MU))

# ---------------- Gaudapada: obstacles to stilling the mind ----------------
G_GK = 'obstacles to stilling the mind (GK 3.42–45)'
PX_GK = [("px:manonigraha-gk-3-40-46", [GK('3.40'), GK('3.41'), GK('3.44')])]
A(E("dx:gk-laya", "Laya (dissolving into torpor)", "obstacle", G_GK, VL, ["obs:laya", "trm:laya"],
    [(LIN_GK, "The mind, even when well settled in dissolution (laya), is to be restrained by the right means, for dissolution is as harmful as desire (GK 3.42). In laya, awaken the mind (GK 3.44). In deep sleep the mind dissolves; restrained, it does not dissolve (GK 3.35).", [GK('3.42'), GK('3.44'), GK('3.35')])],
    [("In stilling the mind, sinking into a pleasant blankness, as in sleep.", ["in meditation I just drift off into a pleasant blank", "I go quiet but it's more like dozing"], [GK('3.42'), GK('3.35')])],
    "Not sleepiness to be assessed and not a medical matter; not the goal: Gauḍapāda says laya is as harmful as desire (GK 3.42).",
    eq=[("dx:nivarana-thina-middha", "partial", "Torpor in the Vism can show as nodding and sleep (Vism XIV); GK's laya is the mind dissolving as in sleep. Both are to be roused; the frameworks differ.", [GK('3.44'), VSM(14, 469)])],
    px=PX_GK))
A(E("dx:gk-viksepa", "Vikṣepa (scattering)", "obstacle", G_GK, VL, ["obs:viksepa", "trm:viksepa"],
    [(LIN_GK, "The mind scattered among desires and enjoyments is to be restrained by the right means (GK 3.42). Remembering that all is suffering, turn it back from desires and enjoyments; remembering that all is the unborn, one sees nothing born (GK 3.43). When scattered, calm it again (GK 3.44).", [GK('3.42'), GK('3.43'), GK('3.44')])],
    [("The mind running out among desires and enjoyments.", ["my mind keeps running after one pleasure or another", "I can't keep my mind from scattering"], [GK('3.42')])],
    "Not a medical matter of any kind: GK 3.42–44 describe the ordinary scattering of the mind in the work of stilling it.",
    eq=[("dx:nivarana-uddhacca-kukkucca", "partial", "Restlessness in the Vism is disquiet, 'distraction of mind' (Vism XIV); GK's vikṣepa is scattering among desires. Different frameworks.", [GK('3.42'), VSM(14, 469)])],
    px=PX_GK + [("px:recollecting-suffering-and-the-unborn-gk-3-43", [GK('3.43')])]))
A(E("dx:gk-kasaya", "Kaṣāya (latent colouring; Gauḍapāda)", "obstacle", G_GK, VL, ["trm:kasaya"],
    [(LIN_GK, "Know the mind when it has kaṣāya (sakaṣāya); when it has reached sameness, do not disturb it (GK 3.44). The verse names this state between dissolving and scattering without describing it further.", [GK('3.44')])],
    [("The mind neither sunk nor scattered, yet not free: something still colours it (GK 3.44).", ["I'm quiet, but something is still holding on underneath"], [GK('3.44')])],
    "Not the Jain kaṣāya (the four passions of TS 8.9): the same word in a different system; the two must never be merged. GK 3.44 gives only the name; later Advaita commentary glosses it, and that gloss is not cited here.",
    eq=[("dx:klesa-raga", "partial", "YS describes kleśas that remain dormant or thinned (YS 2.4); GK 3.44 asks that the still-coloured mind be recognised. Related idea of a latent residue, in different systems.", [GK('3.44'), YS('2.4')])],
    px=PX_GK))
A(E("dx:gk-rasasvada", "Rasāsvāda (savouring the happiness)", "obstacle", G_GK, VL, ["obs:rasasvada", "trm:rasasvada", "phn:advaita-rasasvada"],
    [(LIN_GK, "Do not savour the happiness there; become unattached through wisdom; with effort make the steady mind, and the one that moves out, one (GK 3.45).", [GK('3.45')])],
    [("Enjoying the happiness of stillness and settling for it.", ["the calm is so sweet I just want to stay in it", "I've started chasing that blissful feeling"], [GK('3.45')])],
    "Not a warning against joy as such and not a verdict on anyone's attainment: GK 3.45 asks only that the happiness of stillness not be savoured and clung to.",
    eq=[("dx:vism-vipassanupakkilesa", "partial", "The Vism's attachment (nikanti) to light, rapture and bliss is the one imperfection that is also unwholesome (Vism XX); GK 3.45 warns against savouring the happiness of stillness.", [GK('3.45'), VSM(20, 637)])],
    px=PX_GK))
A(E("dx:gk-asparsa-fear", "Fear of the no-contact yoga (asparśa-yoga)", "obstacle", "named by Gauḍapāda (GK 3.39)", VL, ["phn:gk-asparsa-fear"],
    [(LIN_GK, "The yoga called 'no-contact' (asparśa) is hard for all yogis to see; the yogis are afraid of it, seeing fear where there is no fear (GK 3.39). Fearlessness depends on restraining the mind (GK 3.40).", [GK('3.39'), GK('3.40')])],
    [("Drawing back in fear from the stilling of the mind, as if something would be lost.", ["when it gets very still I get scared and pull back"], [GK('3.39')])],
    "Not a fear to be diagnosed and not a medical matter; not a push to go further: the product never urges anyone past fear in practice. GK 3.39 names the fear so it can be understood.",
    px=PX_GK))
A(E("dx:gk-amanibhava", "Amanībhāva (the no-mind state)", "state", "the stilled mind (GK 3.31–35, 3.46–47)", VL, ["phn:gk-amanibhava", "trm:amanibhava"],
    [(LIN_GK, "All this duality is seen by the mind; when the mind becomes no-mind (amanībhāva), duality is not perceived (GK 3.31). When through knowing the truth of the self it no longer imagines, it becomes no-mind (GK 3.32). When the mind neither dissolves nor scatters, unmoving and without appearance, it is brahman (GK 3.46): self-abiding, peaceful, with nirvāṇa, indescribable, the highest happiness (GK 3.47).", [GK('3.31'), GK('3.32'), GK('3.46'), GK('3.47')])],
    [("Neither dissolving nor scattering, without movement or appearance (GK 3.46).", [], [GK('3.46')])],
    "Never a label for a person's experience and never a verdict on attainment: listed so that the obstacles of GK 3.42–45 can be read against the state they obstruct.",
    px=PX_GK))

# ---------------- Katha ----------------
A(E("dx:katha-unrestrained-senses", "Unrestrained senses (the chariot)", "obstacle", "the chariot of KU 1.3.3–13", VL,
    ["cpt:chariot-image", "obs:thieving-senses", "obs:turbulent-senses", "trm:indriya"],
    [(LIN_UPA, "Know the self as the rider, the body as the chariot, understanding (buddhi) as the charioteer, the mind as the reins; the senses are the horses, their objects the roads (KU 1.3.3–4). For one without understanding, whose mind is ever unyoked, the senses are out of control like the vicious horses of a charioteer (1.3.5); such a one, mindless and ever impure, does not reach that place but comes to saṃsāra (1.3.7).", [KU('1.3.3'), KU('1.3.4'), KU('1.3.5'), KU('1.3.7')])],
    [("The senses running like vicious horses because understanding does not hold the reins of the mind (KU 1.3.5).", ["my senses run away with me", "I know better but I can't hold the reins"], [KU('1.3.5')]),
     ("Going round without arriving (KU 1.3.7).", ["I keep going round in circles and never get anywhere"], [KU('1.3.7')])],
    "Not a character judgement and not a medical condition: the Kaṭha's image shows the order of rider, charioteer, reins and horses so that it can be set right (KU 1.3.6, 1.3.9).",
    states=[("avijñānavān (without understanding)", "Mind unyoked, senses like vicious horses (KU 1.3.5, 1.3.7).", [KU('1.3.5'), KU('1.3.7')]),
            ("vijñānavān (with understanding)", "Mind ever yoked, senses controlled like good horses; reaches the end of the road, Viṣṇu's highest place (KU 1.3.6, 1.3.8–9).", [KU('1.3.6'), KU('1.3.8'), KU('1.3.9')])],
    eq=[("dx:gita-restless-mind", "partial", "The Gītā's turbulent senses carry off the mind (BhG 2.60, 2.67); the Kaṭha's senses run like vicious horses when the mind is unyoked (KU 1.3.5).", [KU('1.3.5'), BG('2.60')])],
    px=[("px:katha-inward-withdrawal-1-3-13", [KU('1.3.13')])]))
A(E("dx:katha-outward-senses", "Outward-turned senses", "obstacle", "named in KU 2.1.1–2", VL, ["obs:thieving-senses", "trm:indriya"],
    [(LIN_UPA, "The self-existent pierced the openings outward; therefore one looks outward, not at the inner self. Some wise one, desiring immortality, turned his eyes inward and saw the inner self (KU 2.1.1). The childish follow outward desires and walk into the net of widespread death (KU 2.1.2).", [KU('2.1.1'), KU('2.1.2')])],
    [("Looking always outward, never at the one who looks.", ["I'm always looking out at things, never inward"], [KU('2.1.1')]),
     ("Following outward desires one after another (KU 2.1.2).", ["I chase one outside thing after another"], [KU('2.1.2')])],
    "Not a fault in the person: the Kaṭha says the senses were made to face outward (KU 2.1.1). Not a medical matter.",
    px=[("px:inward-turned-gaze-ku-2-1-1", [KU('2.1.1')])]))
A(E("dx:katha-preyas", "Choosing the pleasant (preyas) over the good", "obstacle", "the pleasant and the good (KU 1.2.1–6)", VL, ["obs:preyas", "cpt:sreyas-preyas", "trm:preyas", "trm:sreyas"],
    [(LIN_UPA, "The good (śreyas) is one thing, the pleasant (preyas) another; both bind a person with different aims. It goes well with the one who takes the good; the one who chooses the pleasant falls short of the aim (KU 1.2.1). The wise one examines and distinguishes them and chooses the good; the dull one chooses the pleasant for getting and keeping (1.2.2). Living within ignorance, thinking themselves wise, the deluded go round like the blind led by the blind (1.2.5); the goal beyond does not appear to the childish one, heedless, deluded by wealth, who thinks 'this world is, there is no other' (1.2.6).", [KU('1.2.1'), KU('1.2.2'), KU('1.2.5'), KU('1.2.6')])],
    [("Choosing what is pleasant now over what is good, for the sake of getting and keeping (KU 1.2.2).", ["I always go for what feels good now", "I know what's good for me but I choose the comfortable thing"], [KU('1.2.2')]),
     ("Thinking oneself wise while going round in ignorance (KU 1.2.5).", ["I was sure I knew better and ended up where I started"], [KU('1.2.5')])],
    "Not a condemnation of pleasure and not a moral verdict on a person: the Kaṭha asks for discernment between the two (KU 1.2.2).",
    eq=[("dx:klesa-avidya", "partial", "The Kaṭha sets the pleasant within ignorance (avidyā) and the good with knowledge (KU 1.2.4–5); YS avidyā is the mis-taking of YS 2.5.", [KU('1.2.5'), YS('2.5')])],
    px=[("px:sreyas-preyas-viveka-ku-1-2-2", [KU('1.2.2')])]))
A(E("dx:katha-yoga-state", "Yoga as the firm holding of the senses", "state", "the highest course (KU 2.3.10–11)", VL, ["trm:indriya"],
    [(LIN_UPA, "When the five knowings rest together with the mind and understanding does not stir, that they call the highest course (KU 2.3.10). This firm holding of the senses they consider yoga; then one becomes heedful, for yoga is arising and passing away (KU 2.3.11).", [KU('2.3.10'), KU('2.3.11')])],
    [("The senses and mind at rest, understanding not stirring (KU 2.3.10).", [], [KU('2.3.10')])],
    "Never a verdict on a person's attainment: listed as the Kaṭha's own picture of the state its obstacles block.",
    px=[("px:katha-inward-withdrawal-1-3-13", [KU('1.3.13')])]))
