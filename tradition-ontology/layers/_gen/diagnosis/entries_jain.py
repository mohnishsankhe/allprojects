"""Jain entries from the Tattvartha Sutra (Digambara recension as prepared locally)."""
from common import *

JL = 'ascetic-jain'
ENTRIES = []
A = ENTRIES.append

G_KA = 'the four passions (kaṣāya; TS 8.9)'
KA_REFS = ["obs:four-kasayas", "obs:kasaya", "cpt:four-kasayas-sixteen", "trm:kasaya"]
KA_DEFS = [
    (LIN_JAIN, "Conduct-deluding karma includes the sixteen passions: anger, pride, deceit and greed, each in four grades named endless-binding (anantānubandhī), non-renunciation (apratyākhyāna), renunciation (pratyākhyāna) and smouldering (saṃjvalana) (TS 8.9, Digambara recension).", [TS('8.9')]),
    (LIN_JAIN, "Because it is with passion (sakaṣāya), the soul takes in matter fit to become karma; that is bondage (TS 8.2). Influx is of two kinds: the one with passion leads to transmigration (sāmparāyika), the one without passion is merely that of movement (īryāpatha) (TS 6.4); the four passions are among the kinds of the first (TS 6.5).", [TS('8.2'), TS('6.4'), TS('6.5')]),
    (LIN_JAIN, "From the rise of the passions comes an intense state that binds conduct-deluding karma (TS 6.14). Passion is one of the states arising from karma (audayika bhāva) (TS 2.6).", [TS('6.14'), TS('2.6')]),
]
KA_STATES = [
    ("anantānubandhī (endless-binding)", "The first of the four grades named in TS 8.9; the name means 'bound up with the endless'. The sūtra gives the name only; the commentaries' account of what each grade obstructs is not cited here.", [TS('8.9')]),
    ("apratyākhyāna (non-renunciation)", "The second grade named in TS 8.9; the name refers to (non-)renunciation. The sūtra gives the name only.", [TS('8.9')]),
    ("pratyākhyāna (renunciation)", "The third grade named in TS 8.9; the name refers to renunciation. The sūtra gives the name only.", [TS('8.9')]),
    ("saṃjvalana (smouldering)", "The fourth, subtlest grade named in TS 8.9; the name means 'flaring' or 'smouldering'. The sūtra gives the name only.", [TS('8.9')]),
]
KA_NOT = " The Tattvārtha Sūtra is terse: it names the passion and its grades but describes little of how it shows itself, so the markers here stay close to the plain sense of the word. Not the Gauḍapāda kaṣāya (GK 3.44), which is a different use of the word; the two must never be merged."
TENDH = lambda word: f"TS 9.6 lists supreme {word} among the ten forms of dharma (supreme forbearance, softness, straightness, purity, truth, restraint, austerity, renunciation, non-possession, celibacy). The names of the first four are the opposites of anger, pride, deceit and greed; the sūtra itself does not state the pairing."
def kasaya(slug, name, refs, marker, cues, mcites, dh, px, not_read, eq, extra_defs=()):
    A(E(f"dx:kasaya-{slug}", name, "passion", G_KA, JL, KA_REFS + refs,
        KA_DEFS + list(extra_defs) + [(LIN_JAIN, TENDH(dh), [TS('9.6')])],
        [(marker, cues, mcites)], not_read + KA_NOT, states=KA_STATES, eq=eq,
        px=[(px, [TS('9.6')]), ("px:anupreksa-ts-9-7", [TS('9.2'), TS('9.7')])]))

kasaya("krodha", "Krodha (anger)", ["obs:krodha", "trm:krodha"],
    "Anger, one of the four passions; TS 7.5 names giving up anger among the supports of the vow of truthfulness, so anger is marked as what pushes speech from the truth.",
    ["I got angry and said things that weren't true", "I flared up at them"], [TS('8.9'), TS('7.5')],
    "forbearance (kṣamā)", "px:uttama-ksama-ts-9-6",
    "Not a medical condition and not a verdict on a person's worth.",
    [("dx:klesa-dvesa", "partial", "Vyāsa lists anger within dveṣa (YB 2.8); the Jain krodha is a passion graded in four intensities that binds karmic matter (TS 8.2, 8.9).", [YB('2.8'), TS('8.9')]),
     ("dx:root-dosa", "partial", "Theravāda hate is a momentary mental factor, a root of the unwholesome (Vism XIV); Jain anger is a passion by which the soul takes in karmic matter.", [VSM(14, 470), TS('8.2')]),
     ("dx:gita-kama-krodha", "partial", "The Gītā's anger is born of desire and of rajas (BhG 2.62, 3.37).", [BG('3.37'), TS('8.9')])],
    extra_defs=[(LIN_JAIN, "Giving up anger, greed, fear and jest, and speaking after reflection, are the five supports of the vow of truthfulness (TS 7.5).", [TS('7.5')])])
kasaya("mana", "Māna (pride)", ["trm:mana"],
    "Pride, one of the four passions, named with its four grades (TS 8.9).",
    ["I felt I was above them", "I couldn't bear to bow to anyone"], [TS('8.9')],
    "softness (mārdava)", "px:uttama-mardava-ts-9-6",
    "Not self-respect and not a medical condition.",
    [("dx:fetter-mana", "partial", "Theravāda conceit is haughtiness and self-exaltation, remaining until the fourth path (Vism XIV, XXII); Jain pride is a passion graded in four intensities.", [VSM(14, 469), TS('8.9')]),
     ("dx:klesa-asmita", "partial", "Asmitā is the seeming oneness of seer and seeing (YS 2.6), not pride as such; related only through the 'I'.", [YS('2.6'), TS('8.9')]),
     ("dx:gita-asuri-sampad", "partial", "The Gītā lists arrogance and conceit among demonic qualities (BhG 16.4).", [BG('16.4'), TS('8.9')])])
kasaya("maya", "Māyā (deceit)", ["trm:maya-kasaya"],
    "Deceit, crookedness, one of the four passions, named with its four grades (TS 8.9).",
    ["I hid what I really meant", "I said one thing and did another"], [TS('8.9')],
    "straightness (ārjava)", "px:uttama-arjava-ts-9-6",
    "Not the Vedāntic māyā (cosmic illusion) — a different word-use — and not a medical condition.",
    [("dx:gita-asuri-sampad", "partial", "The Gītā lists hypocrisy (dambha) among demonic qualities (BhG 16.4).", [BG('16.4'), TS('8.9')]),
     ("dx:carita-raga", "partial", "The Vism lists deceit (māyā) and fraud among the states frequent in the greedy temperament (Vism III).", [VSM(3, 106), TS('8.9')])])
kasaya("lobha", "Lobha (greed)", ["obs:lobha", "trm:lobha"],
    "Greed, one of the four passions; TS 7.5 names giving up greed among the supports of the vow of truthfulness.",
    ["I keep wanting more", "I can't give anything away"], [TS('8.9'), TS('7.5')],
    "purity (śauca)", "px:uttama-sauca-ts-9-6",
    "Not ordinary needs and not a medical condition.",
    [("dx:root-lobha", "partial", "Theravāda greed is a mental factor that grasps like monkey-lime (Vism XIV); Jain greed is a passion that binds karmic matter (TS 8.2).", [VSM(14, 468), TS('8.2')]),
     ("dx:klesa-raga", "partial", "Vyāsa glosses rāga with the word lobha (YB 2.7).", [YB('2.7'), TS('8.9')])],
    extra_defs=[(LIN_JAIN, "Giving up anger, greed, fear and jest, and speaking after reflection, are the five supports of the vow of truthfulness (TS 7.5).", [TS('7.5')])])

A(E("dx:jain-nokasaya", "No-kaṣāya (the nine quasi-passions)", "passion", "the quasi-passions (akaṣāya / no-kaṣāya; TS 8.9)", JL,
    ["obs:nine-nokasayas", "trm:nokasaya"],
    [(LIN_JAIN, "Conduct-deluding karma includes the nine quasi-passions (akaṣāya): laughter, liking, disliking, grief, fear, disgust, and the female, male and neuter sexual feelings (TS 8.9).", [TS('8.9')])],
    [("Laughter, liking, disliking, grief, fear or disgust arising as the rise of conduct-deluding karma (TS 8.9).", ["I felt disgust", "I was afraid", "I couldn't stop laughing it off"], [TS('8.9')])],
    "Not a list of feelings to be suppressed or condemned and not a medical matter: TS 8.9 names them as kinds of conduct-deluding karma. The three sexual feelings are listed as the text lists them, summary only.",
    states=[(n, "Named among the quasi-passions (TS 8.9).", [TS('8.9')]) for n in ["hāsya (laughter)", "rati (liking)", "arati (disliking)", "śoka (grief)", "bhaya (fear)", "jugupsā (disgust)", "veda (the three sexual feelings)"]]))

G_BH = 'the causes of bondage (TS 8.1)'
BH_DEF = (LIN_JAIN, "Wrong view, non-abstention, heedlessness, passion and activity (yoga) are the causes of bondage (TS 8.1).", [TS('8.1')])
A(E("dx:jain-mithyadarsana", "Mithyādarśana (wrong view)", "obstacle", G_BH, JL, ["obs:mithyatva", "trm:mithyadrsti"],
    [BH_DEF, (LIN_JAIN, "Right view is faith in the reals as they are taught (tattvārtha-śraddhāna) (TS 1.2); wrong view is its opposite, and it is also one of the states arising from karma (TS 2.6).", [TS('1.2'), TS('2.6')])],
    [("Not having faith in the reals as the Jain teaching sets them out (TS 1.2).", ["I don't believe the soul is bound by its deeds"], [TS('1.2')])],
    "Not a charge against people of other faiths and not a verdict on a person: in TS it is the first cause of bondage in the Jain account. Other traditions' views are reported, not judged, in this product.",
    eq=[("dx:klesa-avidya", "partial", "Both stand first among the roots of bondage in their systems (TS 8.1; YS 2.4); the reals they concern differ.", [TS('8.1'), YS('2.4')])],
    px=[("px:tattvartha-sraddhana-ts-1-2", [TS('1.2')])]))
A(E("dx:jain-avirati", "Avirati (non-abstention)", "obstacle", G_BH, JL, ["obs:avirati-jain", "trm:avirati-jain"],
    [BH_DEF, (LIN_JAIN, "The vow (vrata) is abstention from harming, falsehood, stealing, unchastity and possessiveness (TS 7.1); non-abstention is not having taken up this abstention.", [TS('7.1')])],
    [("Not holding back from harming, falsehood, stealing, unchastity and possessiveness (TS 7.1).", ["I haven't made any commitment to stop doing harm"], [TS('7.1')])],
    "Not the Yoga's avirati (greed of the mind for objects, YB 1.30): same word, different sense. Not a moral verdict on a person.",
    eq=[("dx:antaraya-avirati", "partial", "Same word, different sense: non-abstention from the five in TS; the mind's greed for objects in the Yoga (YB 1.30).", [TS('7.1'), YB('1.30')])],
    px=[("px:vrata-ts-7-1", [TS('7.1')])]))
A(E("dx:jain-pramada", "Pramāda (heedlessness)", "obstacle", G_BH, JL, ["obs:pramada-jain", "trm:pramada-jain"],
    [BH_DEF, (LIN_JAIN, "Harming is taking life through heedless activity (pramatta-yoga) (TS 7.13).", [TS('7.13')])],
    [("Acting carelessly, so that harm is done through inattention (TS 7.13).", ["I wasn't paying attention and someone got hurt"], [TS('7.13')])],
    "Not a charge of harming and not a medical condition: TS names heedlessness as what makes the taking of life into harming, and as a cause of bondage.",
    eq=[("dx:antaraya-pramada", "partial", "Vyāsa's pramāda is not cultivating the means of samādhi (YB 1.30); the Jain pramāda is the carelessness that makes harm (TS 7.13).", [YB('1.30'), TS('7.13')]),
        ("dx:pamada", "partial", "The Dhammapada's heedlessness is the path to death (Dhp 21).", [DHP('21'), TS('8.1')])],
    px=[("px:vrata-ts-7-1", [TS('7.1'), TS('7.13')])]))

G_DH = 'the inauspicious meditations (TS 9.28–35)'
DH_DEF = (LIN_JAIN, "Meditation (dhyāna) is of four kinds: sorrowful (ārta), cruel (raudra), virtuous (dharmya) and pure (śukla) (TS 9.28); the last two are causes of liberation (TS 9.29).", [TS('9.28'), TS('9.29')])
A(E("dx:jain-arta-dhyana", "Ārta-dhyāna (sorrowful dwelling)", "state", G_DH, JL, ["obs:arta-raudra-dhyana", "trm:arta-dhyana"],
    [DH_DEF, (LIN_JAIN, "Sorrowful dwelling is fixing the mind again and again on the removal of something unpleasant one has met (TS 9.30); the reverse for something pleasant — on regaining it when separated (TS 9.31); on pain (TS 9.32); and on longing for future enjoyment (nidāna) (TS 9.33). It occurs in the unrestrained, the partly restrained and the heedless restrained (TS 9.34).", [TS('9.30'), TS('9.31'), TS('9.32'), TS('9.33'), TS('9.34')])],
    [("The mind fixed again and again on getting rid of what is unpleasant (TS 9.30).", ["I keep thinking how to get rid of this situation"], [TS('9.30')]),
     ("The mind fixed on getting back what is pleasant and lost (TS 9.31).", ["I can't stop thinking about getting back what I lost"], [TS('9.31')]),
     ("The mind fixed on pain (TS 9.32).", ["I keep dwelling on how much it hurts"], [TS('9.32')]),
     ("The mind fixed on future enjoyments (TS 9.33).", ["I keep daydreaming about the pleasures to come"], [TS('9.33')])],
    "Not a medical state and not a judgement on a person's pain: TS names this dwelling so that it can be turned toward virtuous meditation. The product does not interpret pain.",
    states=[("aniṣṭa-saṃyoga", "Meeting the unpleasant.", [TS('9.30')]), ("iṣṭa-viyoga", "Separation from the pleasant.", [TS('9.31')]), ("vedanā", "Pain.", [TS('9.32')]), ("nidāna", "Longing for future enjoyment.", [TS('9.33')])],
    eq=[("dx:companion-daurmanasya", "partial", "Vyāsa's dejection is the mind's agitation when a wish is thwarted (YB 1.31); TS's sorrowful dwelling fixes the mind on removing the unpleasant or regaining the pleasant.", [YB('1.31'), TS('9.31')])],
    px=[("px:dharmya-dhyana-ts-9-36", [TS('9.29'), TS('9.36')]), ("px:anupreksa-ts-9-7", [TS('9.7')])]))
A(E("dx:jain-raudra-dhyana", "Raudra-dhyāna (cruel dwelling)", "state", G_DH, JL, ["obs:arta-raudra-dhyana", "trm:raudra-dhyana"],
    [DH_DEF, (LIN_JAIN, "Cruel dwelling arises from harming, falsehood, theft and guarding the objects of enjoyment; it occurs in the unrestrained and the partly restrained (TS 9.35).", [TS('9.35')])],
    [("The mind dwelling on harming, lying, stealing, or guarding what one enjoys (TS 9.35).", ["I keep thinking about getting back at them", "I keep working out how to cover my lie", "I keep brooding over how to protect what's mine"], [TS('9.35')])],
    "Not a charge of wrongdoing and not a prediction of what a person will do: TS names this dwelling so that it can be turned toward virtuous meditation.",
    states=[("hiṃsā", "Dwelling on harming.", [TS('9.35')]), ("anṛta", "Dwelling on falsehood.", [TS('9.35')]), ("steya", "Dwelling on theft.", [TS('9.35')]), ("viṣaya-saṃrakṣaṇa", "Dwelling on guarding objects of enjoyment.", [TS('9.35')])],
    eq=[("dx:vitarka-himsadi", "partial", "YS 2.34's vitarkas are thoughts of harming and the rest, met by cultivating the opposite; TS 9.35's cruel dwelling arises from harming, falsehood, theft and guarding possessions.", [YS('2.34'), TS('9.35')])],
    px=[("px:dharmya-dhyana-ts-9-36", [TS('9.29'), TS('9.36')]), ("px:maitri-pramoda-karunya-madhyastha-ts-7-11", [TS('7.11')])]))
