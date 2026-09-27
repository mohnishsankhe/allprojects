# Stage 2: room mask

Run: 2026-09-26.
111 rooms tested. 75 passed every test. 15 kept (at most 15), 60 cut for rank, 36 killed.

A room passes only if all six tests pass:

- **reach**: the founder can reach the room: a warm path from the ledger, or the room already buys this kind of product through search, app stores or public marketplaces (with an evidence URL).
- **depth**: the room's subject is one where the founder can tell good from bad (a ledger depth id).
- **spend**: at least one concrete price people in the room pay, with a URL, that the price checker did not rule out.
- **ladder**: the room has enough paid problems in sequence (ladder steps).
- **supply**: the room's core pains do not need something the founder lacks and cannot rent.
- **exclusions**: the room does not fall under a ledger exclusion.

Survivors are ranked by ladder_steps, spend_points_verified, spend_points, warm_reach, then slug. Spend points count prices with a URL; verified spend points count prices found on the page itself. `[measured, page not checked]` means the price was read in a search result or the page could not be opened.

## Kept rooms (15)

| Rank | Room | Reach | Depth | Ladder steps | Spend (verified/all) | Flags |
|---|---|---|---|---|---|---|
| 1 | mid-career-searchers-buying-small-business | search (s1) | d2 (strong) | 8 | 0/4 | needs trust (search reach); ventures: v4 |
| 2 | iim-isb-first-years-finance-consulting-placements | search (s1) | d2 (strong) | 7 | 0/7 | needs trust (search reach) |
| 3 | first-finance-hires-funded-startups | warm (w2) | d2 (strong) | 7 | 0/6 | employer overlap; ventures: v4 |
| 4 | valuation-analysts-pursuing-bv-credentials | warm (w2) | d2 (strong) | 7 | 0/6 | employer overlap |
| 5 | finance-pros-starting-fractional-cfo-practice | warm (w2) | d2 (strong) | 7 | 0/5 | employer overlap; ventures: v4, v5 |
| 6 | independent-sponsors-small-pe-firms | warm (w2) | d2 (strong) | 7 | 0/5 | employer overlap; ventures: v4 |
| 7 | laid-off-finance-professionals | warm (w2) | d2 (strong) | 7 | 0/5 | employer overlap |
| 8 | new-pe-associates-first-year | warm (w2) | d2 (strong) | 7 | 0/5 | employer overlap |
| 9 | ib-associates-vps-leaving-banking | warm (w2) | d2 (strong) | 6 | 0/5 | employer overlap |
| 10 | outbound-lead-gen-appointment-setting-agencies | warm (w5) | d5 (strong) | 6 | 0/5 | ventures: v4 |
| 11 | startup-founders-409a-83b-deadlines | search (s1) | d2 (strong) | 6 | 0/5 | needs trust (search reach) |
| 12 | us-tcpa-ai-voice-outbound-callers | search (s1) | d5 (strong) | 6 | 0/5 | needs trust (search reach); ventures: v4 |
| 13 | gre-engineers-india | warm (w1) | d1 (strong) | 6 | 0/4 | ventures: v1 |
| 14 | brands-leasing-first-warehouse | search (s1) | d3 (strong) | 6 | 0/4 | needs trust (search reach); ventures: v4 |
| 15 | first-time-founders-pre-seed | search (s1) | d2 (strong) | 6 | 0/4 | needs trust (search reach) |

### 1. Mid-career professionals leaving a corporate job to buy a small business (self-funded searchers) (`mid-career-searchers-buying-small-business`)

- Reach: search reach (s1); evidence: https://acquisitionlab.com/pricing/. Searchers already buy through search: Acquisition Lab sells a $10,000 lifetime membership and reports 1,200+ members, Searchfunder sells monthly, annual and lifetime memberships, and a Duedilio review page compares paid buyer programs. Many searchers come from banking and PE, so w2 reaches a subset, but the room as defined (mid-career professionals from consulting and corporate jobs too) is wider than finance professionals. (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Valuing the target, checking the seller's numbers, structuring the deal and reading the purchase agreement are corporate finance, valuation and deal documents (d2, strong).
- Supply: nothing needed that the founder lacks and cannot rent. The equity injection and SBA loan are the buyer's own capital, not risk the founder carries. Valuation, diligence and structuring need judgment and accountability; legal and lending steps are rentable licences (r1).
- Trust needed: yes. The buyer is risking savings on a $0.5M to $10M purchase and buys advice at thousands of dollars; only a trusted adviser gets that money. Search reach plus trust is a mismatch to flag.
- Spend evidence:
  - Acquisition Lab lifetime membership (buyer program): $10,000 (USD 10000 per one-off, about USD 10,000.00) [measured, page not checked] <https://acquisitionlab.com/pricing/>
  - Independent SBA-format business valuation: $3,000 to $7,500 (USD 3000 per one-off, about USD 3,000.00) [measured, page not checked] <https://www.bizworth.com/blog/how-much-does-a-business-valuation-cost>
  - Quality of earnings report on the target: $15,000-$25,000 for sub-$3M EBITDA businesses (USD 15000 per one-off, about USD 15,000.00) [measured, page not checked] <https://ctacquisitions.com/quality-of-earnings/>
  - Lawyer-drafted asset purchase agreement: $1,290 (USD 1290 per one-off, about USD 1,290.00) [measured, page not checked] <https://buyouts.ai/alternatives/asset-purchase-agreement>

### 2. First-year students at IIMs, ISB and other top Indian B-schools preparing for finance and consulting summer placements (`iim-isb-first-years-finance-consulting-placements`)

- Reach: search reach (s1); evidence: https://www.preplounge.com/en/premium-membership. The room is B-school students, not yet finance professionals, so the colleague path w2 reaches them only two hops away through IIM and ISB alumni and is not counted. They already buy placement prep through search: PrepLounge Premium (USD $69 a year, 400,000+ peers, coaching packages from USD $199) and India-specific paid bootcamps such as BTribe's MBA Placement Bootcamp '26 with ten one-on-one mock interviews (https://www.btribe.in/courses/MBA-Placement-Bootcamp26-Summer-Internship-Final-Placement-prep-69c4a30587d3de68dbc8f280). (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The finance side of placement prep (valuation, DCF, finance technicals, modelling) sits inside corporate finance and valuation (d2, strong); the consulting side is case interviews (d6, moderate). The room's core problems straddle both, and d2 is listed as the strong one.
- Supply: nothing needed that the founder lacks and cannot rent. Placement prep needs judgment on finance technicals, accountability and peer cohorts, all of which the founder can be. No capital, ritual or licensed advocacy is involved.
- Trust needed: yes. The likely product is placement coaching or a cohort with a personal, high-stakes outcome and a price well above an app, so buyers need to trust the coach. Search reach plus trust is a weakness for this room.
- Spend evidence:
  - Case interview coaching from ex-consultants, per session: $100 to $250 per session (USD 100 per session, about USD 100.00) [measured, page not checked] <https://igotanoffer.com/en/advice/preplounge-alternatives>
  - Wall Street Oasis investment banking interview course (guide and question bank): $199.99 (USD 199.99 per one-off, about USD 199.99) [measured, page not checked] <https://www.wallstreetoasis.com/courses/interview-prep/investment-banking>
  - Wall Street Prep Premium Package (financial modelling): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - Placement-linked investment banking operations programme in India (Imarticus fee range): ₹1 and ₹2 lakhs (INR 100000 per programme, about USD 1,044.76) [measured, page not checked] <https://imarticus.org/blog/investment-banking-courses-fees/>
  - PrepLounge Premium membership, one year of case interview practice with peers: USD $69 (USD 69 per year, about USD 69.00) [measured, page not checked] <https://www.preplounge.com/en/premium-membership>
  - PrepLounge Premium + Coaching package (membership plus up to 5 coaching sessions): USD $199 (USD 199 per package, about USD 199.00) [measured, page not checked] <https://www.preplounge.com/en/shop/premium-memberships-1/premium-coaching>
  - Financial modelling certification course in India with placement support (EY certification price in the 2026 fees list): ₹39,999 (INR 39999 per course, about USD 417.89) [measured, page not checked] <https://quintedge.com/blog/financial-modeling-course-fees-india>

### 3. Ex-bankers and ex-consultants in their first year as the first finance hire at a funded startup (`first-finance-hires-funded-startups`)

- Reach: warm path w2: investment banking, private equity and finance professionals. These are ex-bankers and ex-consultants 3 to 8 years in, so the bankers among them are the founder's past colleagues who left for startups, which is the finance-professionals path w2; the ex-consultant and Big 4 share is reached less directly. Search evidence also exists: they buy fundraising models on public marketplaces such as eFinancialModels (https://www.efinancialmodels.com/downloads/saas-financial-model-193/) and Foresight's SaaS Financial Model at $149 (https://www.openvc.app/blog/startup-financial-model). (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Fundraising models, data rooms, diligence and investor reporting are corporate finance, valuation and deal documents (d2, strong). Bookkeeping and tax are outside it and would need a rented accountant.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains (model, round, board pack, first hire) need judgment and accountability, which the founder can be. Bookkeeping or tax sign-off would need an accountant, which the ledger says can be rented (r1), so nothing is blocked.
- Trust needed: yes. A finance lead staking their first-year reputation on a fundraising model or board pack pays for advice from someone they trust; the price is high and the outcome is personal and visible to the board.
- Spend evidence:
  - Seed-stage pitch deck design for the next round: $4,000–$8,000 (USD 4000 per project, about USD 4,000.00) [measured, page not checked] <https://www.whitepage.studio/blog/pitch-deck-design-cost>
  - Fractional CFO retainer, the benchmark the first finance hire must beat or buy: $3,000-$12,000/month (USD 3000 per month, about USD 3,000.00) [measured, page not checked] <https://eightx.co/blog/fractional-cfo-cost-pricing-guide>
  - Wall Street Prep Premium Package (three-statement and DCF modelling refresher): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - Fundraising consultant retainer to run the round: retainers ($5K-$50K) (USD 5000 per retainer, about USD 5,000.00) [measured, page not checked] <https://freestartupfunding.com/costs/fundraising-consultant>
  - New-manager bootcamp for hiring and managing the first analyst: $500 per person (USD 500 per person, about USD 500.00) [measured, page not checked] <https://www.evolution2revolution.com/new-manager-bootcamp>
  - Foresight (Taylor Davidson) SaaS Financial Model template with fundraising and valuation tabs: $149 (USD 149 per one-off, about USD 149.00) [measured, page not checked] <https://www.openvc.app/blog/startup-financial-model>

### 4. Valuation analysts pursuing a business valuation credential (CVA, ABV, ASA or IBBI registered valuer) (`valuation-analysts-pursuing-bv-credentials`)

- Reach: warm path w2: investment banking, private equity and finance professionals. Valuation analysts at accounting and advisory firms are finance professionals who sit across from bankers on deals and fairness opinions, so w2 reaches them through colleagues, though less directly than bankers themselves. Search reach also exists: paid CVA practice-exam courses on Udemy (https://www.udemy.com/course/certified-valuation-analyst-cva-practice-exams/) and RVO 50-hour courses bought online in India. (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The core paid problem is passing a business valuation credential exam and doing valuation work well, which the ledger's strong corporate finance and valuation domain covers; the Indian exam's law sections (Companies Act, IBC) are the part the founder covers less.
- Supply: nothing needed that the founder lacks and cannot rent. Exam prep and valuation skills need teaching, judgment and accountability; the licence to sign valuation reports belongs to the customer, and no large capital, ritual or licensed advocacy sits at the core.
- Trust needed: no. Exam prep and practice questions at $50 to a few hundred dollars are bought self-serve on Udemy and provider sites; only a mentoring product priced near NACVA's $2,975 training would need trust.
- Spend evidence:
  - IBBI registered valuer mandatory 50-hour training through an RVO: Rs. 20,000 to 25,000 (INR 20000 per package, about USD 208.95) [measured, page not checked] <https://taxguru.in/corporate-law/registered-valuer-insolvency-bankruptcy-board-india-ibbi.html>
  - NACVA CVA five-day training package: $2,975.00 (USD 2975 per package, about USD 2,975.00) [measured, page not checked] <http://web.nacva.com/TL-Website/Files/BV_University/CVA_Standard_Pricing.pdf>
  - NACVA CVA certification exam: $625.00 (USD 625 per one-off, about USD 625.00) [measured, page not checked] <http://web.nacva.com/TL-Website/Files/BV_University/CVA_Standard_Pricing.pdf>
  - IBBI valuation examination, per attempt: Rs. 5,900 per attempt (INR 5900 per one-off, about USD 61.64) [measured, page not checked] <https://taxguru.in/corporate-law/registered-valuer-insolvency-bankruptcy-board-india-ibbi.html>
  - RVO 50-hour course fee (one RVO's listed fee): INR 25,000/- plus 18% GST (INR 25000 per package, about USD 261.19) [measured, page not checked] <https://iovrvfhub.org/single_blog/485>
  - NACVA Ultimate Training and Membership, paid annually: $4,275 (USD 4275 per year, about USD 4,275.00) [measured, page not checked] <https://www.nacva.com/utpe>

### 5. Finance professionals leaving a job to start a fractional CFO or independent finance consulting practice (`finance-pros-starting-fractional-cfo-practice`)

- Reach: warm path w2: investment banking, private equity and finance professionals. Bankers, FP&A managers and controllers going independent are the finance professionals w2 covers, and the founder's current and past colleagues include people making this exact move. Search reach also holds: paid fractional-CFO training programs priced $297 to $12,500 are compared and bought through search (https://fractionalcfoschool.com/blog/best-fractional-cfo-training-programs/). (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The work these people sell (board-ready numbers, three-statement and DCF models, fundraising support) sits inside corporate finance and valuation, where the founder can tell good from bad. Practice-building steps (pricing a retainer, entity setup, marketing) are not a ledger depth, so the match is partial.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains (pricing, first clients, delivering alone) need accountability, judgment on finance work and peers, all of which the founder can be. Entity setup and compliance need accountants or lawyers, which the ledger says can be rented.
- Trust needed: yes. The likely product is coaching or a cohort priced in the hundreds to thousands of dollars, tied to a personal outcome (a working practice), so buyers need to trust the person behind it.
- Spend evidence:
  - Fractional CFO monthly retainer that clients pay (sets the practice's ceiling): $3,000-$12,000/month (USD 3000 per month, about USD 3,000.00) [measured, page not checked] <https://eightx.co/blog/fractional-cfo-cost-pricing-guide>
  - Fractional Connections practitioner community, Accelerator level: $49 per month (USD 49 per month, about USD 49.00) [measured, page not checked] <https://fractionals.ai/fccommunity/>
  - Wall Street Prep Premium Package (three-statement, DCF and modelling refresher): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - Fractional CFO training programs, price range across providers: $297 to $12,500 (USD 297 per one-off, about USD 297.00) [measured, page not checked] <https://fractionalcfoschool.com/blog/best-fractional-cfo-training-programs/>
  - Wharton Emerging CFO Program fee: US$14,000 (USD 14000 per one-off, about USD 14,000.00) [measured, page not checked] <https://executiveeducation.wharton.upenn.edu/online-learning/self-paced-online-programs/emerging-cfo-program/>

### 6. Independent sponsors and small private equity firms buying lower-middle-market companies (`independent-sponsors-small-pe-firms`)

- Reach: warm path w2: investment banking, private equity and finance professionals. Independent sponsors and small PE firms are private equity and finance professionals, often ex-bankers, reachable through the founder's current and past colleagues, which is exactly the w2 path. (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Checking a seller's numbers, building the LBO model and lender package, writing the investor memo and closing documents are corporate finance, valuation and deal documents, the founder's strongest domain.
- Supply: nothing needed that the founder lacks and cannot rent. Modelling, diligence review and investor materials need judgment the founder can supply; closing documents need lawyers who can be rented (r1). Soliciting investors for a fee would need a broker-dealer licence in the US, so the product must stop at materials and analysis, not placement.
- Trust needed: yes. Deal work priced in the thousands to tens of thousands of dollars, with the sponsor's reputation with lenders and investors on the line, is bought only from someone they trust.
- Spend evidence:
  - Quality-of-earnings report on a lower-middle-market deal (Stage 1 ladder price): $10,000 to $20,000 for a focused QoE Lite scope, and $25,000 to $50,000 for a full-scope engagement (USD 10000 per one-off, about USD 10,000.00) [measured, page not checked] <https://systemsix.com/what-does-a-quality-of-earnings-report-cost-pricing-by-deal-size/>
  - Wall Street Prep Premium Package for modelling training (Stage 1 ladder price): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - iGlobal Forum 2026 Independent Sponsors Summit New York, standard independent sponsor pass: $849 (USD 849 per ticket, about USD 849.00) [measured, page not checked] <https://conference.iglobalforum.com/independent-sponsors-conference/register>
  - Quality-of-earnings cost for a sub-$3M EBITDA business, 2026: $15,000-$25,000 (USD 15000 per one-off, about USD 15,000.00) [measured, page not checked] <https://www.bedrockqoe.com/insights/quality-of-earnings-report-cost>
  - Fractional CFO for the portfolio company after closing (Stage 1 ladder price): between $3,000 and $12,000 per month (USD 3000 per month, about USD 3,000.00) [measured, page not checked] <https://pilot.com/blog/fractional-cfo-cost-guide>

### 7. Bankers and finance professionals laid off in the last 90 days (`laid-off-finance-professionals`)

- Reach: warm path w2: investment banking, private equity and finance professionals. Analysts, associates and VPs cut from banks and funds are the finance professionals w2 covers, reached through current and past colleagues who know who was let go. Search reach also holds: IGotAnOffer sells investment banking interview coaching by credit through search (https://igotanoffer.com/en/interview-coaching/role/investment-banker). (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Modelling tests and technical interview prep for the next finance role sit in corporate finance and valuation, where the founder can judge. Resume writing, severance terms and visa transfers are not a ledger depth, so the match covers only the technical half of the core pains.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains (story, technicals, interviews, lane choice) need accountability, judgment and peers, which the founder can be. Severance and non-compete terms need a lawyer, which can be rented, and that is one step, not the core.
- Trust needed: yes. The next job is a personal, high-stakes outcome and the products this room buys (coaching at $100 to $400 an hour, multi-session packages) are sold on the coach's credibility.
- Spend evidence:
  - Executive-level resume rewrite: $350 - $700 (USD 350 per one-off, about USD 350.00) [measured, page not checked] <https://topresume.com/career-advice/how-much-does-a-professional-resume-writing-service-cost>
  - Career coaching by the hour: $75 to $200 per hour (USD 75 per hour, about USD 75.00) [measured, page not checked] <https://www.noomii.com/article/cost-hire-career-coach>
  - Wall Street Oasis investment banking interview course: $199.99 (USD 199.99 per one-off, about USD 199.99) [measured, page not checked] <https://www.wallstreetoasis.com/courses/interview-prep/investment-banking>
  - Wall Street Prep Premium Package, modelling test refresher: $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - IGotAnOffer investment banking interview coaching, credit-based (coaches cost 2 to 5 credits per hour): $50/credit (USD 50 per credit, about USD 50.00) [measured, page not checked] <https://igotanoffer.com/en/interview-coaching/role/investment-banker>

### 8. Bankers and consultants in their first year as a private equity associate (`new-pe-associates-first-year`)

- Reach: warm path w2: investment banking, private equity and finance professionals. First-year private equity associates are exactly the private equity professionals w2 covers, and they are the founder's former banking colleagues one move on. Search reach also exists: the Financial Edge PE Associate micro-degree and similar paid courses are bought through search (https://www.fe.training/product/online-finance-courses/private-equity/the-pe-associate/). (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The core pains (running a live LBO model unchecked, marking up purchase agreements and financing terms, portfolio reporting) are corporate finance, valuation, deal documents and transactions, the founder's strongest depth.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains need judgment on deal work, accountability and peers, which the founder can be. Nothing needs large capital, ritual or licensed advocacy.
- Trust needed: yes. The likely product is coaching or a cohort on live deal work, a personal career outcome with prices in the hundreds to thousands of dollars, which buyers only take from someone they trust.
- Spend evidence:
  - BIWS Private Equity Modeling course bundle: $497 (USD 497 per one-off, about USD 497.00) [measured, page not checked] <https://breakingintowallstreet.com/private-equity-signup-options/>
  - Wall Street Prep Premium Package (three-statement, DCF, LBO refresher): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - Wall Street Prep Premium Package as reviewed by a PE blog (second domain for the same price): $499 ($424 with code EQUITEER) (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://theprivateequiteer.com/wall-street-prep-premium-package-review/>
  - MBA admissions consulting, comprehensive package: $6,950 for 1 school, $8,950 for 2 schools, and $10,950 for 3 schools (USD 6950 per package, about USD 6,950.00) [measured, page not checked] <https://www.personalmbacoach.com/product/comprehensive-packages/>
  - New-manager bootcamp for the first analyst: $500 per person (USD 500 per one-off, about USD 500.00) [measured, page not checked] <https://www.evolution2revolution.com/new-manager-bootcamp>

### 9. Investment banking associates and VPs (4 to 10 years in) planning to leave banking (`ib-associates-vps-leaving-banking`)

- Reach: warm path w2: investment banking, private equity and finance professionals. These are investment banking professionals, exactly the current and past colleagues w2 names. Search evidence exists too: IGotAnOffer sells career coaching to bankers at $100–$250 per session (https://igotanoffer.com/en/career-coaching/investment-banking) and Leland lists IB exit coaches at $50–$400+/hr. (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The paid steps (corporate development and fund interview technicals, a modelling refresh, pricing fractional CFO work) sit in corporate finance and valuation (d2, strong). The pivot-story coaching itself is not a ledger domain, so the match is partial.
- Supply: nothing needed that the founder lacks and cannot rent. A pivot needs judgment on the story, accountability through a quiet search, and peers going through the same move; the founder can be all three. No capital, ritual or licence is needed.
- Trust needed: yes. A career exit is a personal, high-stakes outcome and these buyers are well paid and sceptical; they will only pay a peer they trust.
- Spend evidence:
  - WSO Investment Banking Interview Course (technicals reused for corp dev and fund interviews): $197 (USD 197 per one-off, about USD 197.00) [measured, page not checked] <https://www.wallstreetoasis.com/courses/interview-prep/investment-banking>
  - Wall Street Prep Premium Package (modelling refresh): $499 (USD 499 per one-off, about USD 499.00) [measured, page not checked] <https://www.wallstreetprep.com/self-study-programs/premium-package/>
  - Career coach by the hour: $75 to $200 per hour (USD 75 per hour, about USD 75.00) [measured, page not checked] <https://www.noomii.com/article/cost-hire-career-coach>
  - IGotAnOffer investment banking career coaching session: $100–$250 per session (USD 100 per session, about USD 100.00) [measured, page not checked] <https://igotanoffer.com/en/career-coaching/investment-banking>
  - Leland IB career coaches, hourly range by tier: $50–$400+/hr (USD 50 per hour, about USD 50.00) [measured, page not checked] <https://igotanoffer.com/en/advice/leland-alternatives>

### 10. Outsourced lead-generation and appointment-setting agencies running outbound call teams (`outbound-lead-gen-appointment-setting-agencies`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. These agencies are outbound calling teams, exactly the call centres and tele-sales businesses w5 names, but w5 reaches only the India and Gulf slice of a room that is mostly US, UK and Philippines, and the ledger notes it is mostly cold unless they are existing TinyAI clients. Search reach also holds: agency owners buy dialers and AI setters through review marketplaces (Mojo Dialer reviews and Appointwise pricing on G2, https://www.g2.com/products/mojo-dialer/reviews and https://www.g2.com/products/appointwise/pricing). (confidence moderate)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). The room's core paid problems are dialing, call recording and QA, and cutting cost per appointment with AI callers; voice agents and call auditing are named strong domains in d5.
- Supply: nothing needed that the founder lacks and cannot rent. Dialers, scrubbing, call QA and AI calling are software and judgment; do-not-call compliance is a scrub tool, not licensed advocacy, and nothing here needs large capital or ritual.
- Trust needed: yes. An agency puts client accounts at risk when it changes how calls are made, and B2B retainers or AI-agent builds run to hundreds of dollars a month, so the buyer needs to trust the seller.
- Spend evidence:
  - DialedIn Small Business dialer seat: $79/user/month (annual) or $99/user/month (month-to-month), with a $495/month minimum (USD 79 per user per month, about USD 79.00) [measured, page not checked] <https://prospeo.io/s/dialedin-pricing-reviews-pros-and-cons>
  - NumberBroom TCPA litigator scrub, batch screening: $0.20 per Number (USD 0.2 per number, about USD 0.20) [measured, page not checked] <https://numberbroom.com/tcpa-litigator-scrub>
  - Appointwise AI appointment setter for agencies, Starter plan: $97/month (USD 97 per month, about USD 97.00) [measured, page not checked] <https://www.g2.com/products/appointwise/pricing>
  - Mojo Dialer Agent Access licence (before the $89/month single-line dialer licence): $10 per user per month (USD 10 per user per month, about USD 10.00) [measured, page not checked] <https://www.ringover.com/blog/mojo-dialer-pricing>
  - Vapi voice-agent platform fee for AI first-touch calls: $0.05-per-minute platform fee (USD 0.05 per minute, about USD 0.05) [measured, page not checked] <https://www.happyrobot.ai/hub/vapi-ai-pricing>

### 11. Founders of US-incorporated startups facing 83(b) election and 409A valuation deadlines (`startup-founders-409a-83b-deadlines`)

- Reach: search reach (s1); evidence: https://eqvista.com/409a-valuation/what-is-cost-of-409a-valuation/. Founders are not the investment-banking, PE or finance professionals w2 covers. The room already buys 409A valuations and 83(b) filing through search: Eqvista sells unlimited 409A valuations from $990 a year on a public pricing page (https://eqvista.com/409a-valuation/what-is-cost-of-409a-valuation/), Carta bundles one into its plans, and Clerky sells a managed 83(b) add-on pitched on Hacker News. (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). A 409A is a valuation of common stock, and the raise needs a defended valuation and a term sheet, which is corporate finance and deal documents. The 83(b) election and the Delaware filings are tax and corporate procedure outside d2.
- Supply: nothing needed that the founder lacks and cannot rent. A safe-harbour 409A needs an independent appraiser, a qualification rather than a licence, which the founder can be or rent. Nothing needs large capital, ritual or licensed advocacy.
- Trust needed: yes. A 409A is a document the company, its auditors and later acquirers rely on, so buyers pick an appraiser they trust, even though it sells at $990 to $3,000 through search.
- Spend evidence:
  - Stripe Atlas incorporation of a Delaware C-corp (one-time fee): $500 (USD 500 per one-off, about USD 500.00) [measured, page not checked] <https://sparklaun.ch/compare/stripe-atlas>
  - First 409A valuation, early-stage pricing (Cake Equity guide): $1,000 to $3,000 (USD 1000 per one-off, about USD 1,000.00) [measured, page not checked] <https://www.cakeequity.com/guides/409a-valuation-cost>
  - Pitch deck and model for the raise: $2,000–$5,000 (USD 2000 per one-off, about USD 2,000.00) [measured, page not checked] <https://www.spectup.com/resource-hub/how-much-does-a-pitch-deck-cost>
  - Eqvista unlimited 409A valuations for 12 months, starting tier: $990 (USD 990 per year, about USD 990.00) [measured, page not checked] <https://eqvista.com/409a-valuation/what-is-cost-of-409a-valuation/>
  - Stripe Atlas yearly registered-agent renewal: $100 Renewal (USD 100 per year, about USD 100.00) [measured, page not checked] <https://sparklaun.ch/compare/stripe-atlas>

### 12. US businesses and agencies using AI voice or auto-dialers for outbound calls facing TCPA and FCC rules (`us-tcpa-ai-voice-outbound-callers`)

- Reach: search reach (s1); evidence: https://ringscrub.com/pricing.html. No warm path: w5 is India and the Gulf and this room is US. The room already buys TCPA tools through search: RingScrub sells litigator and DNC scrubbing at $130/month from a public pricing page (https://ringscrub.com/pricing.html), NumberBroom at $0.20 per number (https://numberbroom.com/tcpa-litigator-scrub) and TextP2P at 1¢ per number (https://textp2p.com/contact-scrubs/). (confidence high)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). Consent capture and AI disclosure inside the call flow, running the calls on a voice-agent platform and auditing live calls for violations are voice-agent and call-auditing work, the founder's strong domain. The TCPA law itself and the litigation step are not.
- Supply: nothing needed that the founder lacks and cannot rent. Compliant builds and call audits need judgment and vendors; legal defence needs a licensed lawyer, which is rentable. Insurance against uncapped per-call damages would be large-capital risk transfer the founder cannot supply, but it is not the core product.
- Trust needed: yes. The buyer is a business exposed to statutory damages of $500 to $1,500 per call and is paying for a B2B audit or build; it has to trust the auditor.
- Spend evidence:
  - Voice-agent platform usage (Vapi) per minute of calling: $0.05 per minute (USD 0.05 per minute, about USD 0.05) [measured, page not checked] <https://www.cloudtalk.io/blog/vapi-ai-pricing/>
  - RingScrub DNC and litigator scrubbing subscription: $130/month (USD 130 per month, about USD 130.00) [measured, page not checked] <https://ringscrub.com/pricing.html>
  - NumberBroom batch TCPA litigator screening: $0.20 per Number (USD 0.2 per per number, about USD 0.20) [measured, page not checked] <https://numberbroom.com/tcpa-litigator-scrub>
  - Contact-centre QA software to monitor live calls: around $35 per user per month (USD 35 per user per month, about USD 35.00) [measured, page not checked] <https://www.guideflow.com/blog/contact-center-quality-assurance-software>
  - TextP2P TCPA litigator and DNC contact scrub (minimum $5.00 per scrub): 1¢ per number checked (USD 0.01 per per number, about USD 0.01) [measured, page not checked] <https://textp2p.com/contact-scrubs/>

### 13. Indian engineers preparing for the GRE to study abroad (`gre-engineers-india`)

- Reach: warm path w1: Indian engineers and students preparing for the GRE to study abroad. This room is word for word the people w1 covers: Indian engineers preparing for the GRE to study abroad, reached through the founder's GRE product and its users. Search reach also holds: Magoosh sells a 30-day GRE Premium plan at $149 through search (https://gre.magoosh.com/register/premium-30-days) and its GRE book is listed on Flipkart (https://www.flipkart.com/gre-prep-magoosh/p/itmev76vpyxzgymb). (confidence high)
- Depth: d1: GRE quant and verbal (strong). The core paid problem is GRE quant and verbal prep, which is the ledger's d1 (strong). Later steps (registration, counsellors, loans, visa) are outside depth but are not the room's first paid problem.
- Supply: nothing needed that the founder lacks and cannot rent. GRE prep needs judgment, practice and accountability before a fixed test date. No large capital, ritual or licensed advocacy is at the core.
- Trust needed: yes. Self-serve apps sell at $149 without trust, but the likely product here (coaching or a cohort at ₹7,500 to ₹30,000, paid by parents before an exam date) needs a credible guide. Warm reach covers that.
- Spend evidence:
  - GRE online-live coaching programme in India (2026 range): ₹15,000–₹30,000 (INR 15000 per package, about USD 156.71) [measured, page not checked] <https://www.wikatiedu.com/blog/ielts-gre-sat-2026-coaching-fees-exam-guide/>
  - GRE exam registration fee in India: ₹22,550 (INR 22550 per one-off, about USD 235.59) [measured, page not checked] <https://eecglobal.com/blog/gre-fee-registration-india-2026>
  - EEC online live + pre-recorded GRE programme: ₹7,500 (INR 7500 per package, about USD 78.36) [measured, page not checked] <https://eecglobal.com/blog/best-gre-coaching-online-india-2026>
  - Magoosh GRE 1-Month Premium self-study plan: $149 (USD 149 per month, about USD 149.00) [measured, page not checked] <https://testprepinsight.com/reviews/magoosh-gre-review/>

### 14. E-commerce brands moving out of a 3PL or a garage into their first leased warehouse (`brands-leasing-first-warehouse`)

- Reach: search reach (s1); evidence: https://www.contractscounsel.com/b/commercial-lease-review-cost. w3 covers landlords, investors and advisers, not the tenants in this room, and w5 is warm only for existing TinyAI clients in India and the Gulf, so there is no warm path (w3 gives partners and market knowledge, not customers). Search reach holds: tenants buy commercial lease reviews on the ContractsCounsel marketplace (average $730 flat fee, platform data), rent small units month to month from ReadySpaces and RISE found via search, and pay lease-review services such as LeaseRef. (confidence moderate)
- Depth: d3: industrial and logistics real estate (strong). Choosing, negotiating and later buying industrial space is industrial and logistics real estate, the founder's strong d3; the 3PL-versus-own-space decision and the fit-out sit inside it too. d5 covers only the customer-call step.
- Supply: nothing needed that the founder lacks and cannot rent. Lease review needs a lawyer (rentable, r1) and racking and fit-out need vendors (r3); the founder's judgment on space and lease terms is d3-strong. The tenant, not the founder, signs the lease and pays the deposit, so no large capital, ritual or licensed advocacy is needed.
- Trust needed: yes. A multi-year lease and fit-out is a B2B service with a large, hard-to-reverse outcome; buyers want a named adviser, not a self-serve tool.
- Spend evidence:
  - Flat-fee lawyer review of a commercial lease, average on the ContractsCounsel marketplace: $730 (USD 730 per one-off, about USD 730.00) [measured, page not checked] <https://www.contractscounsel.com/b/commercial-lease-review-cost>
  - Attorney review of a first industrial lease (low end of the range shown; ladder step 2): $600–$2,000 (USD 600 per one-off, about USD 600.00) [measured, page not checked] <https://leaselens.org/commercial-lease-review-cost>
  - Pallet racking for the fit-out (low end of the range shown; ladder step 3): $50 to $500 per pallet position (USD 50 per per pallet position, about USD 50.00) [measured, page not checked] <https://warehousingcosts.com/guides/pallet-racking-costs>
  - Cloud warehouse management system for a small e-commerce operation (low end of the range shown; ladder step 4): $150–$500/month (USD 150 per month, about USD 150.00) [measured, page not checked] <https://warego.co/blog/ecommerce-wms-cost/>

### 15. First-time founders setting up a company and raising a first round (`first-time-founders-pre-seed`)

- Reach: search reach (s1); evidence: https://stripe.com/atlas. No warm path covers first-time founders; the founder's finance and private-equity contacts (w2) are investors, not this room. Founders buy this kind of product through search and public marketplaces at scale: Stripe Atlas incorporates companies for a flat $500, Clerky sells incorporation at $427 (https://sparklaun.ch/compare/clerky) and Slidebean sells pitch-deck software and design from $7 a month to $799 (https://slidebean.com/pricing). (confidence high)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Half of the room's definition is raising a first round: pitch deck, SAFE terms, valuation and the financial model, which sit inside d2 (corporate finance, valuation, deal documents). Incorporation, compliance and first customers are outside depth, so the match is partial.
- Supply: nothing needed that the founder lacks and cannot rent. Deck, terms and model review need judgment (c2 in d2) and accountability; legal filings come from vendors like Stripe Atlas or a rented lawyer (r1). Raising the money itself is the investors' capital, not the founder's, as long as no placement fee is taken.
- Trust needed: yes. Incorporation at $500 is bought self-serve, but deck and terms advice at $2,000 and up shapes a founder's ownership and is bought on credibility. Search reach plus trust is flagged.
- Spend evidence:
  - Stripe Atlas incorporation, one-time fee: $500 (USD 500 per one-off, about USD 500.00) [measured, page not checked] <https://sparklaun.ch/compare/stripe-atlas>
  - Professional pitch deck for a pre-seed raise (typical spend): $2,000–$5,000 (USD 2000 per one-off, about USD 2,000.00) [measured, page not checked] <https://www.spectup.com/resource-hub/how-much-does-a-pitch-deck-cost>
  - Clerky incorporation, pay per filing: $427 (USD 427 per one-off, about USD 427.00) [measured, page not checked] <https://sparklaun.ch/compare/clerky>
  - Slidebean Accelerate plan (pitch deck writing and financial-model help): $99 per month (USD 99 per month, about USD 99.00) [measured, page not checked] <https://www.toolsforhumans.ai/ai-tools/slidebean>

## Cut for rank (60)

These rooms passed every test but ranked below the limit. They are in graveyard.md.

- rank 16: sat-us-undergrad-india (ladder 6, spend 0/4, reach search)
- rank 17: small-3pl-fulfilment-warehouse-operators (ladder 6, spend 0/4, reach search)
- rank 18: small-ca-firms-india (ladder 6, spend 0/4, reach search)
- rank 19: sea-energy-companies-issb-climate-reporting (ladder 6, spend 0/3, reach warm)
- rank 20: founders-selling-first-online-business (ladder 6, spend 0/3, reach search)
- rank 21: bpo-contact-centre-operators-india-philippines (ladder 5, spend 0/5, reach warm)
- rank 22: corporate-development-associates-in-house-ma (ladder 5, spend 0/5, reach warm)
- rank 23: lender-insurer-telesales-floors-india (ladder 5, spend 0/5, reach warm)
- rank 24: small-industrial-property-investors (ladder 5, spend 0/5, reach warm)
- rank 25: trai-dlt-160-series-outbound-callers (ladder 5, spend 0/5, reach warm)
- rank 26: ai-agent-builders-freelance (ladder 5, spend 0/5, reach search)
- rank 27: business-brokers-ma-boutiques (ladder 5, spend 0/5, reach search)
- rank 28: ib-summer-analyst-recruits (ladder 5, spend 0/5, reach search)
- rank 29: indian-developers-moving-into-ai (ladder 5, spend 0/5, reach search)
- rank 30: indie-perfumers-launching-brands (ladder 5, spend 0/5, reach search)
- rank 31: mba-ib-associate-switchers (ladder 5, spend 0/5, reach search)
- rank 32: btech-students-india-reddit-community (ladder 5, spend 0/4, reach warm)
- rank 33: cfa-candidates-community (ladder 5, spend 0/4, reach warm)
- rank 34: d2c-brands-scaling-past-launch (ladder 5, spend 0/4, reach warm)
- rank 35: dubai-real-estate-brokerages-telesales (ladder 5, spend 0/4, reach warm)
- rank 36: gre-preppers-worldwide-online (ladder 5, spend 0/4, reach warm)
- rank 37: private-hospitals-india-ahpi (ladder 5, spend 0/4, reach warm)
- rank 38: restaurant-owners-india-cloud-kitchens (ladder 5, spend 0/4, reach warm)
- rank 39: salon-spa-owners-india-global (ladder 5, spend 0/4, reach warm)
- rank 40: test-prep-coaching-institutes-india (ladder 5, spend 0/4, reach warm)
- rank 41: uk-commercial-landlords-mees-epc-deadline (ladder 5, spend 0/4, reach warm)
- rank 42: consultants-planning-exit-to-finance (ladder 5, spend 0/4, reach search)
- rank 43: desi-fragrance-addicts-india-community (ladder 5, spend 0/4, reach search)
- rank 44: fragrance-enthusiasts-online-forums (ladder 5, spend 0/4, reach search)
- rank 45: indian-retail-fno-traders-community (ladder 5, spend 0/4, reach search)
- rank 46: indian-startup-founders-community (ladder 5, spend 0/4, reach search)
- rank 47: indie-hackers-bootstrapped-founders (ladder 5, spend 0/4, reach search)
- rank 48: non-target-students-breaking-into-finance (ladder 5, spend 0/4, reach search)
- rank 49: self-directed-value-investors-community (ladder 5, spend 0/4, reach search)
- rank 50: study-abroad-consultancies-india (ladder 5, spend 0/4, reach search)
- rank 51: excel-financial-modellers-competition-community (ladder 5, spend 0/3, reach warm)
- rank 52: finra-series-79-sie-new-hires (ladder 5, spend 0/3, reach warm)
- rank 53: dental-practice-owners-clinics (ladder 5, spend 0/3, reach search)
- rank 54: eu-ai-act-deadline-ai-product-teams (ladder 5, spend 0/3, reach search)
- rank 55: retiring-owners-selling-business (ladder 5, spend 0/3, reach search)
- rank 56: rooftop-solar-installers-epc (ladder 5, spend 0/3, reach search)
- rank 57: vibe-coders-building-apps-with-ai (ladder 5, spend 0/3, reach search)
- rank 58: ci-solar-developers-ipps-southeast-asia (ladder 5, spend 0/2, reach warm)
- rank 59: cre-analysts-underwriting (ladder 4, spend 0/7, reach warm)
- rank 60: ib-analysts-years-1-3 (ladder 4, spend 0/5, reach warm)
- rank 61: indian-cas-moving-to-finance (ladder 4, spend 0/5, reach warm)
- rank 62: pe-associate-candidates-on-cycle (ladder 4, spend 0/5, reach warm)
- rank 63: sell-side-equity-research-associates (ladder 4, spend 0/5, reach warm)
- rank 64: fpa-analysts-corporate (ladder 4, spend 0/5, reach search)
- rank 65: mbb-case-interview-candidates (ladder 4, spend 0/5, reach search)
- rank 66: oil-gas-engineers-mid-career (ladder 4, spend 0/5, reach search)
- rank 67: seo-agency-owners-ai-search (ladder 4, spend 0/5, reach search)
- rank 68: big4-transaction-services-fdd-associates-moving-to-ib-pe (ladder 4, spend 0/4, reach warm)
- rank 69: contact-centre-ops-managers (ladder 4, spend 0/4, reach warm)
- rank 70: energy-transition-career-switchers (ladder 4, spend 0/4, reach warm)
- rank 71: industrial-brokers-and-developers (ladder 4, spend 0/4, reach warm)
- rank 72: project-finance-analysts-energy-infra (ladder 4, spend 0/4, reach warm)
- rank 73: active-retail-options-traders (ladder 4, spend 0/4, reach search)
- rank 74: small-business-owners-reddit-community (ladder 4, spend 0/4, reach search)
- rank 75: solar-wind-project-developers (ladder 4, spend 0/3, reach warm)

## Killed rooms (36)

| Room | Failed tests | Why |
|---|---|---|
| admitted-us-masters-predeparture-india | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| canada-express-entry-applicants | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| cat-aspirants-india | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| diy-solar-offgrid-builders-community | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| dpdp-compliance-indian-data-businesses | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| energy-managers-auditors-cem-bee-certification | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| engineers-relocating-gulf-energy-jobs | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| esg-sustainability-professionals-networks | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| eu-uk-cosmetics-allergen-labelling-beauty-brands | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| f1-international-students-us-community | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| f1-opt-students-us-nonresident-tax-filing | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| final-year-btech-placements-india | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| first-time-d2c-brand-founders | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| first-time-managers | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| freelance-gre-gmat-tutors | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| frm-candidates-exam-windows | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| h1b-workers-new-to-us | depth, supply, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); supply: blocked: the room's core pains need licensed_advocacy; exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| h1b-workers-status-clock | depth, supply, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); supply: blocked: the room's core pains need licensed_advocacy; exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| india-beauty-brands-cdsco-legal-metrology-epr | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| indian-fno-traders-itr3-tax-audit | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| indian-pvt-ltd-annual-roc-compliance | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| indians-moving-uae-jobs | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| laid-off-tech-workers | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| mba-admissions-consulting-boutiques | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| mba-applicants-gmat-global | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| ms-abroad-applicants-india | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| nism-certification-renewers-india | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| nri-indian-tax-filers | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| nris-returning-to-india | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| opt-grads-us-job-hunt | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| quant-aspirants-quantnet-community | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| rics-apc-candidates-commercial-property | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| skilled-workers-relocating-germany | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| small-vendors-first-soc2-iso27001-audit | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |
| uae-businesses-corporate-tax-filing | depth, exclusions | depth: no ledger depth domain matches this room (depth.ledger_id is null); exclusions: excluded by x1: Anything that needs a licence I don't hold in the customer's country: medical, legal, regulated investment advice. |
| women-in-finance-professional-networks | depth | depth: no ledger depth domain matches this room (depth.ledger_id is null) |

## For REVIEW.md

- Search-reach rooms whose product needs trust: mid-career-searchers-buying-small-business, iim-isb-first-years-finance-consulting-placements, startup-founders-409a-83b-deadlines, us-tcpa-ai-voice-outbound-callers, brands-leasing-first-warehouse, first-time-founders-pre-seed. Search reach suits self-serve products; a product that needs trust usually needs a warm path.
- Rooms that overlap the founder's job (warm path w2/w4 or exclusion x2): first-finance-hires-funded-startups, valuation-analysts-pursuing-bv-credentials, finance-pros-starting-fractional-cfo-practice, independent-sponsors-small-pe-firms, laid-off-finance-professionals, new-pe-associates-first-year, ib-associates-vps-leaving-banking. Check the employer's outside-business rules before pursuing.
- Kept rooms that touch existing ventures (tagged, not excluded): mid-career-searchers-buying-small-business (v4); first-finance-hires-funded-startups (v4); finance-pros-starting-fractional-cfo-practice (v4, v5); independent-sponsors-small-pe-firms (v4); outbound-lead-gen-appointment-setting-agencies (v4); us-tcpa-ai-voice-outbound-callers (v4); gre-engineers-india (v1); brands-leasing-first-warehouse (v4).

## Price checks

Counts: seen_via_search 466.
