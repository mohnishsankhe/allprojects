"""New cues for the diagnosis layer's markers (P3: recall of the offline rules engine).

NEW[entry id] = [(start of the marker text, [new cues]), ...]. Applied by add_cues.py to layers/diagnosis.json: each cue
is appended to that marker's "cues" and listed in its "cues_added". Cues only help the rules engine notice a marker
(SCHEMA.md); the marker text, from the sources, is what a mapping rests on. Every cue is first person, present or
habitual, everyday English, and says only what its marker says (practice-setting markers keep the practice setting).

Deliberately NOT given new cues (see the P3 report):
- attainment / goal states listed beside the obstacles, whose own not_to_be_read_as forbids telling a person they are
  in them: dx:gunatita, dx:gita-sthitaprajna, dx:gk-amanibhava, dx:katha-yoga-state, and both markers of
  dx:cittabhumi ("the product never tells a person which ground they are in");
- markers that can only be paraphrased in body, sleep or food words: the posture and eating markers of dx:carita-raga,
  dx:carita-dosa and dx:carita-moha; dx:jain-arta-dhyana "The mind fixed on pain (TS 9.32)".
"""

NEW = {
    # ------------------------------------------------------------------ Yoga Sutra and Bhasya
    "dx:klesa-asmita": [
        ("Taking the mind that thinks", [
            "I take my thoughts to be the real me",
            "when my opinions are criticised I feel attacked myself",
            "I can't tell my thoughts apart from myself",
            "my changing moods feel like my true self",
            "I identify completely with whatever I happen to think",
        ]),
    ],
    "dx:klesa-raga": [
        ("Wanting a pleasure again", [
            "when a trip ends I keep replaying it and wanting it again",
            "I keep going back to the memory of that pleasure",
            "I chase the feeling I had on that holiday",
            "remembering how good it was makes me crave it again",
            "I miss that pleasure so much I plan to repeat it",
        ]),
        ("Vyāsa: attachment seen toward one object", [
            "when one craving fades another one takes its place",
            "my wanting just moves from one object to the next",
            "I drop one attachment and find another waiting",
            "each craving I satisfy is soon replaced by a new one",
        ]),
    ],
    "dx:klesa-dvesa": [
        ("Pushing against a pain", [
            "I avoid anyone who reminds me of what happened",
            "I recoil from everything connected with that old hurt",
            "the memory of how they hurt me makes me push them away",
            "I dislike the whole place because of what happened there",
            "I resent whatever brings back that humiliation",
        ]),
    ],
    "dx:klesa-abhinivesa": [
        ("The wish 'may I not cease to be", [
            "I dread the idea of ceasing to exist",
            "my own death frightens me even though I understand it",
            "a dread of dying grips me on ordinary days",
            "I cling to going on existing whatever happens",
            "I fear my own death more than anything",
        ]),
    ],
    "dx:antaraya-styana": [
        ("The mind will not take up the work", [
            "at prayer time my mind refuses any effort",
            "my mind feels unfit for the effort of meditation",
            "my mind refuses to engage with my studies",
            "my mind stays rigid and unworkable at practice time",
            "I face my practice and my mind does not budge",
        ]),
    ],
    "dx:antaraya-samsaya": [
        ("Knowing that touches both sides", [
            "I waver between believing the teaching and doubting it",
            "I can't settle whether this spiritual path is true",
            "I doubt whether my practice leads anywhere",
            "I stall in my practice because I'm unsure it's true",
            "my mind swings between yes and no about the teachings",
        ]),
    ],
    "dx:antaraya-pramada": [
        ("Not doing the practice one knows", [
            "I keep neglecting my prayers",
            "I let my meditation lapse for weeks at a time",
            "I leave my chanting undone day after day",
            "I skip the practice I know supports my progress",
            "I keep letting my scripture study slide",
        ]),
    ],
    "dx:antaraya-alasya": [
        ("Not starting, because body and mind", [
            "I feel leaden and weighed down at practice time",
            "I drag my feet and don't start my meditation",
            "an inertia comes over me whenever I mean to study",
            "my mind is too weighed down to begin my prayers",
            "sloth keeps me from ever starting my chanting",
        ]),
    ],
    "dx:antaraya-avirati": [
        ("The mind's greed for contact", [
            "I can't turn my mind away from pleasant distractions",
            "my mind reaches greedily for every pleasant thing",
            "my greed for pleasant things keeps me from practising",
            "I stay hooked on whatever pleases my senses",
            "the pull of pleasant things beats my wish to practise",
        ]),
    ],
    "dx:antaraya-bhranti-darsana": [
        ("Seeing wrongly, as when one moon", [
            "I misread what is happening in my practice",
            "I take mistaken ideas about meditation as the truth",
            "I keep getting the teaching backwards and acting on it",
            "I feel certain about my practice and then find I'm mistaken",
        ]),
    ],
    "dx:antaraya-alabdha-bhumikatva": [
        ("Not reaching any settled ground", [
            "I practise daily and never reach steady ground",
            "my practice stays at the same shallow level",
            "I never get beyond the first stage of meditation",
            "after years of sitting I reach no settled stage",
        ]),
    ],
    "dx:antaraya-anavasthitatva": [
        ("Losing a ground once gained", [
            "the steadiness I gain in practice keeps slipping away",
            "I keep losing the ground I gained in meditation",
            "my mind reaches a still point and falls back again",
            "each time I get steady in prayer I slide back",
            "I reach a settled state in meditation and cannot keep it",
        ]),
    ],
    "dx:companion-daurmanasya": [
        ("The mind shaken because a wish", [
            "I get upset and rattled whenever my wishes are thwarted",
            "a thwarted plan leaves me agitated",
            "I'm disturbed for days when a wish of mine is refused",
            "my mind gets churned up when I don't get my way",
            "when my plans are blocked I'm shaken for hours",
        ]),
    ],
    "dx:vitarka-himsadi": [
        ("Thoughts of harming, lying, stealing", [
            "I keep plotting revenge on them",
            "I'm tempted to lie to get out of trouble",
            "the thought of stealing small things tempts me",
            "I approve when others harm the people I dislike",
            "I want someone else to do the harm for me",
            "thoughts of hitting back at them rise in me",
        ]),
    ],
    # ------------------------------------------------------------------ Gita
    "dx:guna-sattva": [
        ("When light, knowledge, arises", [
            "my understanding feels lit up and clear",
            "a brightness of knowing fills me through the day",
            "my perception feels luminous and alert",
            "I see everything with a bright, clear knowing",
        ]),
        ("The sāttvika doer", [
            "I work with zeal and stay unmoved by success or failure",
            "success and failure leave me equally steady",
            "I don't boast about the good work I do",
            "I act with steady enthusiasm and no attachment to the outcome",
        ]),
        ("Sāttvika happiness", [
            "the discipline felt like a burden at first and now brings deep joy",
            "what began as a struggle has turned into a quiet joy",
            "my happiness comes from understanding things clearly for myself",
            "the early effort was grim and the reward is a clear mind",
        ]),
    ],
    "dx:guna-rajas": [
        ("When rajas grows", [
            "I cram my days with one undertaking after another",
            "I pile project upon project",
            "a restless longing drives me from one task to the next",
            "my greed for more keeps me constantly on the go",
            "I can't sit idle and keep grabbing new tasks",
        ]),
        ("The rājasa doer", [
            "I'm eager for the payoff more than the work itself",
            "I'm elated by success and crushed by failure",
            "I chase results greedily and push others aside",
            "I'm swept between joy and grief by how my work turns out",
            "I measure every effort only by what I gain from it",
        ]),
        ("Rājasa happiness", [
            "the thrill is great at first and leaves me empty after",
            "every pleasure I chase turns to regret in the end",
            "the excitement of buying something fades into regret",
            "what delights my senses at first ends up souring",
        ]),
    ],
    "dx:guna-tamas": [
        ("When tamas grows", [
            "a darkness settles over my mind and I stay idle",
            "I sit around in a fog and ignore my duties",
            "my mind is clouded and I let everything slide",
            "I'm inactive and careless about what needs doing",
        ]),
        ("The tāmasa doer", [
            "I put off important tasks for weeks on end",
            "I'm stubborn and refuse to change how I do things",
            "I delay and delay until the deadline has passed",
            "I leave the job half done and lose heart",
            "I procrastinate and sink into gloom",
        ]),
        ("Tāmasa steadiness", [
            "I hold on stubbornly to my grief and my pride",
            "I refuse to let go of old fears and gloom",
            "I find my pleasure in lazing about and forgetting everything",
            "I hang on to my despondency day after day",
        ]),
    ],
    "dx:gita-anger-chain": [
        ("Turning an object over and over", [
            "the more I dwell on it, the more I want it",
            "I turn it over in my mind until I crave it",
            "brooding on something I saw turns into desire for it",
            "I dwell on the thing I saw until I have to have it",
        ]),
        ("Anger born of desire, then clouding", [
            "my anger clouds my judgement completely",
            "in my anger I forget everything I have learned",
            "once I'm angry my good sense deserts me",
            "when I can't have what I want I rage and lose my head",
        ]),
    ],
    "dx:gita-kama-krodha": [
        ("Acting wrongly against one's own wish", [
            "I act against my own better judgement as if pushed",
            "I find myself doing the very thing I resolved not to do",
            "I'm pushed into wrongdoing against my own will",
            "I give in and act wrongly against my own wishes",
        ]),
        ("A fire that cannot be filled", [
            "my wanting is never satisfied, whatever I get",
            "my craving burns like a fire that is never full",
            "my desire hides what I know like a fog",
            "my desire blinds me to what I understand",
        ]),
        ("The surge (vega)", [
            "a surge of wanting rises in me and I strain to hold it",
            "a rush of anger surges through me before I can think",
            "the urge of desire and anger sweeps over me",
            "I feel a wave of anger rising and struggle to bear it",
        ]),
    ],
    "dx:gita-asuri-sampad": [
        ("Hypocrisy, arrogance, conceit", [
            "I act pious in public and behave differently at home",
            "I speak harshly to people I consider beneath me",
            "I'm arrogant and sure I know better than everyone",
            "I flaunt my goodness so people admire me",
            "I'm harsh and conceited with those who work under me",
        ]),
    ],
    "dx:gita-visada": [
        ("Sinking before a duty", [
            "I sink at the thought of the duty in front of me",
            "I'm torn about my duty and can't see the right course",
            "I collapse inside before a task that feels unbearable",
            "I lose heart facing what I'm obliged to do",
        ]),
        ("The body giving way with the mind whirling", [
            "my mind whirls when I face what I have to do",
            "my mind reels before the duty in front of me",
            "everything spins inside me when I think of that duty",
            "I give way inside and my thoughts whirl",
        ]),
        ("Turning to a teacher", [
            "I'm looking for a teacher to show me what is right",
            "I want to ask someone wise to guide me",
            "I'm lost and ready to be taught",
            "I have come to the point of begging for guidance",
        ]),
    ],
    "dx:gita-restless-mind": [
        ("The mind moving off wherever it will", [
            "my mind wanders and drifts off when I pray",
            "my mind runs off to emails and plans in the middle of prayer",
            "I can't keep my mind on the page for a minute",
            "my mind jumps about restlessly whatever I'm doing",
            "my mind darts off in every direction",
        ]),
        ("The senses dragging the mind", [
            "whatever catches my eye drags my mind after it",
            "a sound or a screen pulls my mind away instantly",
            "the sights around me drag my attention off my work",
            "my senses carry my good sense away",
        ]),
    ],
    # ------------------------------------------------------------------ Gaudapada
    "dx:gk-laya": [
        ("In stilling the mind, sinking", [
            "when I meditate I sink into a cosy blankness",
            "my meditation turns into a pleasant fog",
            "in meditation my mind goes blank and dull",
            "during my practice I slip into a comfortable blank",
            "at prayer I sink into a warm dullness",
        ]),
    ],
    "dx:gk-viksepa": [
        ("The mind running out among desires", [
            "when I sit still my mind runs out after pleasures",
            "in meditation my thoughts scatter toward things I enjoy",
            "my mind chases enjoyments the moment I sit quietly",
            "my mind scatters among desires and enjoyments",
        ]),
    ],
    "dx:gk-kasaya": [
        ("The mind neither sunk nor scattered", [
            "in meditation I'm calm with a subtle tint of wanting underneath",
            "my stillness carries a trace of old desires",
            "I'm settled in practice with a hidden pull underneath",
            "my calm is coloured by a hidden residue",
        ]),
    ],
    "dx:gk-rasasvada": [
        ("Enjoying the happiness of stillness", [
            "I linger in the bliss of meditation and go no further",
            "I savour the bliss of stillness and cling to it",
            "I relish the peace of my practice and stop going deeper",
            "I'm hooked on the blissful feeling I get in meditation",
            "I settle for savouring the happiness of stillness",
        ]),
    ],
    "dx:gk-asparsa-fear": [
        ("Drawing back in fear", [
            "as my mind grows quiet in meditation, fear pulls me back",
            "deep stillness in meditation frightens me",
            "I'm afraid of losing myself when meditation goes deep",
            "I back away from the inner silence out of fear",
            "fear of vanishing makes me stop when I meditate",
        ]),
    ],
    # ------------------------------------------------------------------ Katha
    "dx:katha-unrestrained-senses": [
        ("The senses running like vicious horses", [
            "my senses bolt like wild horses",
            "my good sense can't rein in my cravings",
            "my desires drag me wherever they please",
            "my understanding loses control of my senses",
            "I have no grip on the reins of my mind",
        ]),
        ("Going round without arriving", [
            "I go round and round on my spiritual path without arriving",
            "year after year I circle back to the same place in my practice",
            "I keep returning to where I began and never reach the goal",
            "my search goes round in circles and arrives nowhere",
        ]),
    ],
    "dx:katha-outward-senses": [
        ("Looking always outward", [
            "I look outward all day and never look within",
            "my gaze is fixed outward on people and things",
            "my attention is always on what's outside me, never inside",
            "I never turn around to see the one who is looking",
        ]),
        ("Following outward desires", [
            "I run after one outward desire after another",
            "I follow every new desire that comes along",
            "I go from one purchase to the next",
            "my days are one outside pursuit after another",
        ]),
    ],
    "dx:katha-preyas": [
        ("Choosing what is pleasant now", [
            "I pick the easy pleasure over what is good for me",
            "I trade what is good in the long run for pleasure now",
            "I reach for the pleasant thing and skip what is beneficial",
            "I choose the fun option over the worthwhile one every time",
            "I grab what pleases me now and let the good slide",
        ]),
        ("Thinking oneself wise", [
            "I consider myself wise and repeat the same mistakes",
            "I pride myself on knowing and still go round in ignorance",
            "I'm certain I understand and end up back where I began",
            "I act the expert and stay blind to my ignorance",
        ]),
    ],
    # ------------------------------------------------------------------ Buddhist
    "dx:nivarana-kamacchanda": [
        ("The mind lured by sensual desire", [
            "tempting thoughts keep luring my mind off the mantra",
            "my mind won't settle on one object because of what I desire",
            "desire for pleasant things pulls my attention from the prayer",
            "sensual thoughts keep drawing me off my meditation",
            "longing for enjoyable things scatters my focus in practice",
        ]),
    ],
    "dx:nivarana-byapada": [
        ("Hindered by ill will toward the object", [
            "irritation at the noise breaks up my meditation",
            "resentment keeps breaking my concentration in prayer",
            "my prayer keeps snagging on people I dislike",
            "hostile thoughts about someone break into my meditation",
            "my mind bristles at whatever I dislike and can't flow on",
        ]),
        ("'He abused me, he struck me", [
            "I replay the insult over and over for days",
            "I brood about the person who wronged me",
            "I keep going back to how badly they treated me",
            "I keep a mental list of every wrong done to me",
            "I relive the argument in my head for weeks",
        ]),
    ],
    "dx:nivarana-thina-middha": [
        ("Overcome by stiffness and torpor", [
            "my mind turns stiff and dull in meditation",
            "torpor and stiffness grip me at prayer",
            "my mind is rigid and unwieldy when I study",
            "my mind stiffens and drags during chanting",
        ]),
        ("Sinking, drooping", [
            "during meditation I droop and sink lower and lower",
            "I get bored halfway through my prayers and stretch lazily",
            "my head droops while I recite the mantra",
            "I sit to study and slowly sink into boredom",
        ]),
    ],
    "dx:nivarana-uddhacca-kukkucca": [
        ("Seized by restlessness and remorse", [
            "my mind flits about restlessly and can't rest",
            "restless thoughts and regrets churn in me when I sit to pray",
            "I'm agitated inside and my mind hops from worry to worry",
            "my mind is unsettled and jittery whenever I try to be still",
        ]),
        ("Regret afterwards", [
            "I go over old mistakes again and again at night",
            "I torment myself over things I left undone",
            "I keep reliving my mistakes and feeling ashamed",
            "I'm consumed by regret over how I behaved",
            "I keep going over conversations and what I failed to say",
        ]),
        ("DN 2: while the five hindrances", [
            "my regrets rule me like a master rules a servant",
            "I'm a slave to my restless thoughts",
            "my remorse holds me captive",
            "I'm at the beck and call of my worries",
        ]),
    ],
    "dx:nivarana-vicikiccha": [
        ("Stricken by doubt", [
            "doubt about the method stops me from really practising",
            "my doubts about the teaching keep me from practising",
            "uncertainty about the path keeps me from starting",
            "I stand at the edge of the practice, stuck in doubt",
        ]),
        ("Wavering, taking now one side", [
            "I switch between teachers and traditions every few months",
            "I flip between trusting the teaching and dismissing it",
            "I'm torn between two spiritual paths and keep changing sides",
            "one month I'm devoted to the path, the next I drop it",
            "I waver back and forth about which practice is right",
        ]),
    ],
    "dx:fetter-vicikiccha": [
        ("Wavering, taking now one side", [
            "I go back and forth about whether the teaching is true",
            "I keep switching sides about the path I follow",
            "I trust the teaching one week and doubt it the next",
            "my faith in the practice swings from side to side",
        ]),
    ],
    "dx:fetter-silabbata-paramasa": [
        ("Holding that keeping a rule", [
            "I believe the ritual alone makes me pure",
            "I count on my observances to purify me by themselves",
            "I trust that keeping the vows perfectly is what frees me",
            "I'm convinced the correct ritual is all that matters",
            "I rely on the rules themselves to make me pure",
        ]),
    ],
    "dx:fetter-kamaraga": [
        ("Greed that sticks to its object", [
            "my desire sticks to it and won't let go",
            "I stay stuck on wanting that one pleasure",
            "the craving grips me and refuses to let go",
            "I cling to that pleasure like glue",
        ]),
    ],
    "dx:fetter-patigha": [
        ("Ferocity toward its object", [
            "my resentment spreads like poison through the day",
            "I turn fierce toward anyone who crosses me",
            "my anger at one person spills over onto everyone",
            "a fierce hostility toward them flares up in me",
        ]),
    ],
    "dx:fetter-mana": [
        ("Holding oneself high", [
            "I secretly rank myself above my colleagues",
            "I want my achievements to be seen and praised",
            "I hold myself higher than the people around me",
            "I show off to be admired",
            "I seethe when others get the credit I deserve",
        ]),
    ],
    "dx:fetter-uddhacca": [
        ("Disquiet, like water whipped by wind", [
            "my mind is choppy like water in the wind",
            "a disquiet keeps stirring in me",
            "my thoughts churn like whipped-up water",
            "I'm stirred up and agitated inside even at rest",
        ]),
    ],
    "dx:root-lobha": [
        ("Grasping that sticks and will not let go", [
            "I grip tightly to what I own and can't part with it",
            "I hoard things and refuse to give them up",
            "I cling to my possessions and can't let them go",
            "my grasping sticks to whatever I get",
        ]),
        ("There is no fire like lust", [
            "my greed burns in me like a fire",
            "a burning desire for more consumes me",
            "my craving flares up hotter than anything",
            "the fire of wanting keeps burning in me",
        ]),
    ],
    "dx:root-dosa": [
        ("Ferocity that spreads and burns", [
            "my rage hurts me more than the person I'm angry at",
            "my anger burns inside me for days",
            "my fury spreads and scorches me first",
            "my hostility burns me up from inside",
        ]),
        ("Hatred is never appeased by hatred", [
            "I answer hostility with hostility",
            "when someone is cruel to me I hate them in return",
            "I meet their hatred with more hatred of my own",
            "I keep stoking my hatred of them",
        ]),
    ],
    "dx:root-moha": [
        ("Blindness of mind", [
            "my mind is clouded and I miss what is in front of me",
            "I stay blind to the true nature of things",
            "a fog over my mind hides how things truly are",
            "I'm confused about what is really happening to me",
        ]),
        ("There is no net like delusion", [
            "I'm tangled in my own confusion",
            "I'm caught in a net of wrong ideas",
            "my confusion traps me and I can't find the way out",
            "I'm stuck in a web of muddled thinking",
        ]),
    ],
    "dx:tanha": [
        ("Delighting now here, now there", [
            "I delight in one thing and then crave the next",
            "my craving moves from one pleasure to another",
            "my wanting hops from one delight to the next",
            "I get attached to whatever pleases me",
        ]),
        ("Growing like a creeper", [
            "my craving spreads like a creeper when I'm careless",
            "the less attention I pay, the more my wanting grows",
            "my cravings creep further into my days unnoticed",
            "left unwatched, my wanting grows and grows",
        ]),
    ],
    "dx:pamada": [
        ("Letting life slip by", [
            "I drift through the weeks without doing what matters",
            "I waste my days on trivial things",
            "months go by and I never get to what's important",
            "I fritter away my time and neglect what counts",
            "I'm careless with my days and the important things wait",
        ]),
    ],
    "dx:mutthassati": [
        ("Mindfulness muddled", [
            "I go through my day on autopilot",
            "I carry out whole tasks with my mind somewhere else",
            "my awareness is muddled and I do things blindly",
            "I'm only half present in whatever I'm doing",
        ]),
    ],
    "dx:citta-sankhitta": [
        ("The text names the state and asks only that it be known as it is: 'he knows a contracted", [
            "my mind feels contracted and withdrawn",
            "my mind pulls in on itself and narrows",
            "my mind has shrunk into a small tight space",
            "my mind is closed up and withdrawn",
        ]),
    ],
    "dx:citta-vikkhitta": [
        ("The text names the state and asks only that it be known as it is: 'he knows a scattered", [
            "my mind is scattered in a dozen directions",
            "my thoughts are strewn everywhere",
            "my mind is in pieces, going everywhere at once",
            "my attention is split and scattered",
        ]),
    ],
    "dx:carita-raga": [
        ("Work: sweeps carefully", [
            "I do my work carefully, evenly and gracefully",
            "my work is gentle, skilful and even",
            "I tidy so evenly it looks like arranging flowers",
            "I sweep and tidy with a light, even touch",
        ]),
        ("Seeing: looks long", [
            "I gaze at lovely things as if amazed",
            "I fasten on small virtues and overlook real faults",
            "I linger over a beautiful sight and leave reluctantly",
            "I see the best in people and miss their flaws",
        ]),
        ("States that often occur: deceit, fraud", [
            "I'm vain and keen to be admired",
            "my wishes are big and I'm fickle about them",
            "I'm discontented and always after something grander",
            "I bend the truth to look good",
        ]),
    ],
    "dx:carita-dosa": [
        ("Work: grips the broom tightly", [
            "my work is tense, stiff and uneven",
            "I grip my tools tightly and bang about noisily",
            "I clean in a harsh rush and make a mess",
            "I do tasks roughly and hastily",
        ]),
        ("Seeing: does not look long", [
            "I pick on small faults and ignore what is good",
            "I spot every little flaw and dismiss real merits",
            "I turn away quickly from anything that displeases me",
            "I leave places without a backward glance",
        ]),
        ("States that often occur: anger, resentment", [
            "I look down on people with contempt",
            "I'm envious when a colleague is praised",
            "I like to dominate and get my way",
            "I begrudge sharing what I have",
            "resentment smoulders in me for weeks",
        ]),
    ],
    "dx:carita-moha": [
        ("Work: holds the broom loosely", [
            "my work is muddled and undecided",
            "I fumble about and do jobs unevenly",
            "I switch this way and that and the job comes out messy",
            "I go about tasks loosely and without skill",
        ]),
        ("Seeing: depends on others", [
            "I praise what others praise and blame what they blame",
            "I echo whatever the people around me say",
            "I'm indifferent and borrow my views from others",
            "I take my likes and dislikes from the crowd",
        ]),
        ("States that often occur: stiffness", [
            "I hold on to my opinions tenaciously",
            "I'm stubborn and refuse to let go of my ideas",
            "I'm torn by doubt and regret most days",
            "I'm dull and restless by turns",
        ]),
    ],
    "dx:carita-saddha": [
        ("Posture, work, eating and seeing: like the greedy", [
            "I handle my tasks gently and evenly",
            "I linger over lovely sights and leave them reluctantly",
            "I notice small virtues in people and dwell on them",
            "I arrange things neatly and pleasingly",
        ]),
        ("States that often occur: generosity", [
            "I give freely with an open hand",
            "I long to meet holy people and hear them teach",
            "I trust readily where trust is deserved",
            "I'm glad-hearted and guileless with people",
            "I'm drawn to hearing the true teaching",
        ]),
    ],
    "dx:carita-buddhi": [
        ("Posture, work, eating and seeing: like the hating", [
            "I work briskly and firmly",
            "I spot faults quickly and move on",
            "I don't linger over pleasant sights",
            "I leave places briskly without looking back",
        ]),
        ("States that often occur: being easy to correct", [
            "I accept correction easily and change course",
            "I seek out wise friends and heed their advice",
            "a sense of urgency stirs me to strive",
            "seeing how fleeting things are, I strive harder",
        ]),
    ],
    "dx:carita-vitakka": [
        ("Posture, work, eating and seeing: like the deluded", [
            "my work is muddled and I leave it unfinished",
            "I echo other people's praise and blame",
            "I handle my tasks loosely and unevenly",
            "my opinions depend on whoever I last spoke to",
        ]),
        ("States that often occur: much talking", [
            "I chatter endlessly and crave company",
            "I scheme all night and rush around all day",
            "I dislike steady good habits and drift between projects",
            "I love company and find quiet devotion dull",
        ]),
    ],
    "dx:vism-palibodha": [
        ("Ties that take up the time and mind", [
            "family obligations take all the time I set aside for meditation",
            "renovating the house crowds out my meditation",
            "constant travel keeps interrupting my meditation",
            "worry about money pulls my mind away from practice",
            "managing my property takes the hours I need for prayer",
        ]),
    ],
    "dx:vism-vipassanupakkilesa": [
        ("Taking lights, joy, calm", [
            "the calm in my meditation convinces me I have arrived",
            "I take the joy I feel when meditating as proof of success",
            "I settle into the bright experiences as the goal itself",
            "I'm sure these lights in meditation mean I've made it",
        ]),
    ],
    "dx:vism-brahmavihara-enemies": [
        ("Kindness sliding into attachment", [
            "my caring for a friend turns into possessiveness",
            "helping others leaves me drowning in their sorrow",
            "my love for them has turned possessive",
            "my sympathy turns into my own grief",
            "my joy for others slides into chasing my own pleasures",
        ]),
    ],
    # ------------------------------------------------------------------ Jain
    "dx:kasaya-krodha": [
        ("Anger, one of the four passions", [
            "I'm angry for days",
            "I snap at people over small things",
            "my temper flares and I say things that aren't true",
            "in anger I exaggerate and twist the facts",
            "I lose my temper at the slightest delay",
            "I shout in anger and say what I don't mean",
        ]),
    ],
    "dx:kasaya-mana": [
        ("Pride, one of the four passions", [
            "I'm too proud to apologise",
            "I bristle when nobody notices what I've done",
            "I can't bear being corrected by someone junior",
            "I rank myself above everyone I work with",
            "my pride is wounded when someone else is praised",
            "I refuse to bow to anyone",
        ]),
    ],
    "dx:kasaya-maya": [
        ("Deceit, crookedness", [
            "I hide my real intentions from people",
            "I tell little lies to cover my tracks",
            "I show one face at work and another at home",
            "I pretend to agree and quietly do what I like",
            "I twist the truth to get my way",
            "I smile and agree in meetings and then say the opposite",
        ]),
    ],
    "dx:kasaya-lobha": [
        ("Greed, one of the four passions", [
            "I hoard money and can't bear to part with it",
            "I'm greedy for more money and things",
            "I grab for more even when I have plenty",
            "I'm stingy and hate to share what's mine",
            "my greed makes me bend the truth",
        ]),
    ],
    "dx:jain-nokasaya": [
        ("Laughter, liking, disliking", [
            "disgust rises in me at the sight of certain people",
            "grief comes over me without warning",
            "fear grips me in ordinary moments",
            "I burst out laughing at the wrong moments",
            "I'm swept by likes and dislikes all day",
        ]),
    ],
    "dx:jain-avirati": [
        ("Not holding back from harming", [
            "I've taken no vow to refrain from harming",
            "I tell lies freely and don't hold back",
            "I take what isn't mine without restraint",
            "I don't restrain myself from harming or lying",
        ]),
    ],
    "dx:jain-arta-dhyana": [
        ("The mind fixed again and again on getting rid", [
            "I keep scheming how to get away from what I dislike",
            "my mind returns again and again to escaping this unpleasant job",
            "I brood over how to be rid of what annoys me",
            "I keep planning how to get rid of this person",
        ]),
        ("The mind fixed on getting back", [
            "my mind fixes on regaining the comfort I had",
            "I dwell on winning back the good times I lost",
            "I keep plotting to recover the pleasure I lost",
            "I pine for my old comforts and scheme to regain them",
        ]),
        ("The mind fixed on future enjoyments", [
            "I daydream constantly about the pleasures ahead",
            "my mind fixes on the enjoyments I have lined up",
            "I fantasise about future pleasures all the time",
            "I scheme about the luxuries I'm going to buy",
        ]),
    ],
    "dx:jain-raudra-dhyana": [
        ("The mind dwelling on harming", [
            "I keep plotting how to hurt the people who crossed me",
            "I dwell with relish on getting back at them",
            "I work out elaborate lies to protect myself",
            "I brood with pleasure on taking revenge",
            "I fiercely guard my things and plan how to punish thieves",
        ]),
    ],
}
