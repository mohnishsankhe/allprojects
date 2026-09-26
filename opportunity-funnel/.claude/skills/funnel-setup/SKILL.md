---
name: funnel-setup
description: Opportunity Funnel Stage 0. Interviews the founder one question at a time and writes config/ledger.md (reach, depth, supply, constraints, geography, exclusions, year-four test). Run once, then refresh quarterly. The only stage that waits for the founder.
disable-model-invocation: true
---

# /funnel-setup: Stage 0, the ledger

The ledger says what the founder can actually do. Every later stage filters against it, so it must be true, specific and short.

`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py`. Stay inside `opportunity-funnel/`.

## Steps

1. Run `funnel init`. It creates missing folders (`inbox/...`, `runs/`) and says whether `config/ledger.md` exists and how old it is.
2. **If a ledger exists:** show it. Then go through the seven topics below one at a time, asking "Is this still true? What changed?" Skip to step 4 when done.
3. **If no ledger exists:** interview the founder. Ask **one question per message**, wait for the answer, and ask a short follow-up only when an answer is too vague to filter on. Keep each question short and give one example answer.
   1. **Reach:** Which rooms or communities can you enter warmly within 14 days? Name each one and the path in: a person, a group, a network. (Example: "Final-year engineering students at my old college, through two professors I know.")
   2. **Depth:** In which domains can you tell a good answer from a bad one without help?
   3. **Supply:** Which of these 13 human walls can you credibly *be* today, and for which of the rooms above? Which could you rent through a partner, and who is that partner? List them: W17 Risk transfer (you pay if it's wrong), W18 License, W19 Judgment (people borrow your pick), W20 Accountability (you watch and correct), W21 Advocacy (you fight their battle), W22 Atoms (physical work), W23 Private data (outcomes across many customers), W24 Network (you bring people together), W25 Peers (a cohort going through it together), W26 Facilitation (neutral outsider), W27 Ritual (credible officiant), W28 Witness (seen by someone who knows you), W29 Source (they want it from a person or respected brand).
   4. **Constraints:** Hours per week you can give this. Months of runway. Cash you could hold as a reserve for guarantees. The value of one of your hours, in your currency.
   5. **Geography and languages** you can sell in.
   6. **Exclusions:** rooms or categories you won't consider.
   7. **Year-four test:** which kinds of people would you still want to serve in four years?
   8. **API keys (asked once):** Stage 3 works better with a free YouTube Data API key, and optionally a Stack Exchange key. Reddit now requires pre-approved API access. Do you have any of these, or want to skip them? Never ask the founder to paste a key into the chat. Tell them to put it in `opportunity-funnel/.env` (local) or in the cloud environment's environment variables (cloud session), using the names in `.env.example`.
4. **Write `config/ledger.md`.** Put a plain-English summary first. Then add one fenced `yaml` block in exactly the format of `config/formats.md` (Ledger section). Give every reach, depth, partner and supply entry an id (`r1`, `d1`, `p1`, `s1`...). Supply `rooms` refer to reach ids, or `[any]`. Use the founder's words. Do not add anything the founder didn't say. Leave `confirmed:` empty for now.
5. Run `funnel ledger-check`. Fix anything it reports.
6. **Show the founder the ledger and wait** for their confirmation or corrections. When they confirm, set `confirmed:` to today's date and rerun `funnel ledger-check`.
7. If this is a cloud session, run `funnel preflight --network-only`. It lists which source domains the network blocks. Tell the founder exactly which domains to allow.
