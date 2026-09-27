# Definitions

**Room.** A group of people in the same life situation who gather in findable places and talk to each other. "Engineers applying for a US master's" is a room. "22–26-year-olds" is not: they share an age, not a situation, and they don't gather anywhere as that group.

**Pain.** A problem a room describes in its own words.

**Ladder.** The sequence of paid problems a room faces one after another over the next 2–3 years. Longer ladders make better rooms: a customer you help on step 1 can buy again on steps 2, 3 and 4.

**Failed spend.** Money a person reports spending on something that did not solve the problem. The strongest evidence of real pain: they already paid once and are still stuck.

**Urgency types.** Why the pain can't wait. Exactly one of:
- `acute_pain`: it hurts now (stress, loss, blocked progress).
- `fear`: they dread a bad outcome that hasn't happened yet.
- `deadline_or_rule`: a date or a rule forces action (exam date, filing deadline, visa expiry, compliance).
- `expiring_gain`: an opportunity closes if they don't act (a discount, an admission round, a hiring season).
- `none`: no reason to act soon.

Ranking order when urgency is compared: deadline or rule > acute pain > fear > expiring gain > none.

**Walls.** Points where a person with a perfect AI in their pocket still fails to reach the outcome. The full list, numbered W1–W29, is in `config/walls.md`.
- **Machine walls** (W1–W16) could be closed by the person's own AI as it improves. They **melt**.
- **Human walls** (W17–W29) need something a model can't be. They **hold**.

**Pair.** The product. The machine walls it gets in through (the **entry**: 3 or more machine walls next to each other on the person's path), plus one human wall that **holds** it (keeps customers from replacing you with their own AI).

**Lanes.** Which kind of business a surviving pain can become.
- **Business:** a real pair exists, and the founder can credibly supply the holding human wall.
- **Trade:** machine walls only. Allowed only if the build takes 2 weeks or less, payment is upfront, there are no subscriptions, and an exit date is written from day one. (It will melt, so take the cash and leave on schedule.)
- **Partner:** needs a human wall the founder can't supply. Rent it from a partner for a share of revenue, or kill it.

**Lenses (Stage 1).** Six ways of slicing people into rooms, so the list isn't one-dimensional: `life_stage`, `profession`, `transition` (an event: exams, moves, new parenthood, first job, illness in the family), `obligation` (a deadline or rule: compliance, applications, renewals), `business_type` (small and mid-sized businesses, by industry) and `identity_community` (people who gather around who they are or what they love).

**Reach kinds (Stage 2).**
- **Warm reach:** the room matches one of the founder's warm paths in the ledger. Needed for products that need trust.
- **Search reach:** the room already buys this kind of product through search, app stores or public marketplaces, anywhere in the world. Suits self-serve products.

**Saturation (Stage 3).** We keep collecting until more data stops changing the answer: the last 300 new records add no new pain and change no pain's rank. Three conservative readings apply (logged in REVIEW.md): round 1 builds the pain list, so saturation is tested only from round 2 ("at least 500 records, then continue"); when the latest round brings more than 300 records, the whole round is the window (the order inside a round is only query order); and a window with fewer than 30 member records cannot show a new pain, so the room keeps listening.

**Voice (Stage 3 labels).** Who wrote a record: `member` (someone in the room), `seller` (someone selling a fix), `media` (news, blogs about the room), `other`. Pain counts use member records only. Seller records are evidence that money changes hands.

**US dollars per hour.** What one hour of the founder's time earns in an opportunity: cash left per customer after cash costs, divided by the founder's hours per customer (delivery plus winning the sale). Compared against the ledger's value of an hour.

**Other terms used in outputs**
- **Record:** one stored piece of public text (a post, comment, review, page section or chat message), anonymized, with an ID, URL and date.
- **record_id:** a stable fingerprint (hash) of a record's URL and text. The same text at the same URL always gets the same ID.
- **Verified quote:** a quote the checker script found, word for word, inside the stored record it cites.
- **`[measured]`:** a number taken from stored data or from a page we cite by URL.
- **`[estimate]`:** a number we reasoned our way to. Treat it as a guess with stated assumptions.
- **`[thin]`:** too little data to trust the conclusion much.
- **Acquisition cost:** what it costs, in cash and in the founder's time, to win one paying customer.
- **Price anchor:** what the nearest human substitute (tutor, consultant, agent, lawyer) charges. Buyers compare our price with this, so we never anchor on an app's price.
- **Graveyard:** `graveyard.md`, the list of everything killed, with why.
