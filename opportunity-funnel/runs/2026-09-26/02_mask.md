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

Survivors are ranked by ladder_steps, spend_points_verified, spend_points, priced_ladder_steps, warm_reach, then slug. Spend points count prices with a URL; verified spend points count prices found on the page itself. `[measured, page not checked]` means the price was read in a search result or the page could not be opened.

## Kept rooms (15)

| Rank | Room | Reach | Depth | Ladder steps | Spend (verified/all) | Flags |
|---|---|---|---|---|---|---|
| 1 | small-industrial-property-investors | warm (w3) | d3 (strong) | 8 | 0/5 | none |
| 2 | gre-engineers-india | warm (w1) | d1 (strong) | 8 | 0/4 | ventures: v1 |
| 3 | active-retail-options-traders | search (s1) | d7 (moderate) | 8 | 0/4 | none |
| 4 | small-business-owners-reddit-community | search (s1) | d5 (strong) | 8 | 0/4 | needs trust (search reach); ventures: v4 |
| 5 | bpo-contact-centre-operators-india-philippines | warm (w5) | d5 (strong) | 7 | 0/5 | ventures: v4 |
| 6 | outbound-lead-gen-appointment-setting-agencies | warm (w5) | d5 (strong) | 7 | 0/5 | ventures: v4 |
| 7 | business-brokers-ma-boutiques | search (s1) | d2 (strong) | 7 | 0/5 | needs trust (search reach) |
| 8 | indie-perfumers-launching-brands | search (s1) | d8 (moderate) | 7 | 0/5 | ventures: v2, v4 |
| 9 | startup-founders-409a-83b-deadlines | search (s1) | d2 (strong) | 7 | 0/5 | needs trust (search reach) |
| 10 | lender-insurer-telesales-floors-india | warm (w5) | d5 (strong) | 7 | 0/5 | ventures: v4 |
| 11 | cfa-candidates-community | warm (w2) | d2 (strong) | 7 | 0/4 | employer overlap |
| 12 | d2c-brands-scaling-past-launch | warm (w5) | d5 (strong) | 7 | 0/4 | ventures: v4, v2 |
| 13 | dubai-real-estate-brokerages-telesales | warm (w5) | d5 (strong) | 7 | 0/4 | ventures: v4 |
| 14 | gre-preppers-worldwide-online | warm (w1) | d1 (strong) | 7 | 0/4 | ventures: v1 |
| 15 | salon-spa-owners-india-global | warm (w5) | d5 (strong) | 7 | 0/4 | ventures: v4 |

### 1. Small industrial and warehouse property investors and syndicators (`small-industrial-property-investors`)

- Reach: warm path w3: warehouse and logistics real estate developers, investors and advisers. Owners and syndicators of warehouses and light-industrial buildings are the investors w3 names (warehouse developers, investors, advisers) through the founder's private-equity network. Search reach applies too: the room pays published prices for CoStar, Crexi Intelligence ($249 per month, https://www.trustradius.com/products/crexi/pricing) and A.CRE modelling courses (https://www.adventuresincre.com/pricing/). (confidence high)
- Depth: d3: industrial and logistics real estate (strong). The core paid problems are finding, underwriting, financing and managing industrial property; d3 (industrial and logistics real estate) is a strong depth and d2 covers the valuation and deal documents.
- Supply: nothing needed that the founder lacks and cannot rent. Underwriting, lender packages and JV terms need judgment and process; securities lawyers for the PPM are a rentable licence (r1); the capital itself comes from lenders and investors, not the founder. No large capital, ritual or licensed advocacy at the core.
- Trust needed: yes. Deal judgment and capital-raising help on million-dollar buildings is a high-price, personal B2B service.
- Spend evidence:
  - CoStar market data subscription: $15,000 annually (USD 15000 per year, about USD 15,000.00) [measured, page not checked] <https://www.vendr.com/buyer-guides/costar>
  - A.CRE Accelerator real estate financial modeling course: $697 (USD 697 per package, about USD 697.00) [measured, page not checked] <https://www.adventuresincre.com/pricing/>
  - ARGUS software certification bundle: $900 (USD 900 per package, about USD 900.00) [measured, page not checked] <https://learn.credaglobal.org/products/argus-software-certification-asc-enterprise-bundle>
  - Crexi Intelligence property data and comps, starting plan: $249 per month (USD 249 per month, about USD 249.00) [measured, page not checked] <https://www.trustradius.com/products/crexi/pricing>
  - Reg D private placement memorandum from a flat-fee securities firm (syndication capital raise): $12,000 to $25,000 (USD 12000 per package, about USD 12,000.00) [measured, page not checked] <https://ppmlawyers.com/reg-d-ppm-cost/>

### 2. Indian engineers preparing for the GRE to study abroad (`gre-engineers-india`)

- Reach: warm path w1: Indian engineers and students preparing for the GRE to study abroad. This room is word for word the people w1 covers: Indian engineers preparing for the GRE to study abroad, reached through the founder's GRE product and its users. Search reach also holds: Magoosh sells a 30-day GRE Premium plan at $149 through search (https://gre.magoosh.com/register/premium-30-days) and its GRE book is listed on Flipkart (https://www.flipkart.com/gre-prep-magoosh/p/itmev76vpyxzgymb). (confidence high)
- Depth: d1: GRE quant and verbal (strong). The core paid problem is GRE quant and verbal prep, which is the ledger's d1 (strong). Later steps (registration, counsellors, loans, visa) are outside depth but are not the room's first paid problem.
- Supply: nothing needed that the founder lacks and cannot rent. GRE prep needs judgment, practice and accountability before a fixed test date. No large capital, ritual or licensed advocacy is at the core.
- Trust needed: yes. Self-serve apps sell at $149 without trust, but the likely product here (coaching or a cohort at ₹7,500 to ₹30,000, paid by parents before an exam date) needs a credible guide. Warm reach covers that.
- Spend evidence:
  - GRE online-live coaching programme in India (2026 range): ₹15,000–₹30,000 (INR 15000 per package, about USD 156.71) [measured, page not checked] <https://www.wikatiedu.com/blog/ielts-gre-sat-2026-coaching-fees-exam-guide/>
  - GRE exam registration fee in India: ₹22,550 (INR 22550 per one-off, about USD 235.59) [measured, page not checked] <https://eecglobal.com/blog/gre-fee-registration-india-2026>
  - EEC online live + pre-recorded GRE programme: ₹7,500 (INR 7500 per package, about USD 78.36) [measured, page not checked] <https://eecglobal.com/blog/best-gre-coaching-online-india-2026>
  - Magoosh GRE 1-Month Premium self-study plan: $149 (USD 149 per month, about USD 149.00) [measured, page not checked] <https://testprepinsight.com/reviews/magoosh-gre-review/>

### 3. Active retail options traders (`active-retail-options-traders`)

- Reach: search reach (s1); evidence: https://optionstrat.com/membership. This room buys tools and courses self-serve: OptionStrat sells paid plans from $39.99/month with a free trial, Udemy's options trading topic page shows instructors with 112,000+ students (https://www.udemy.com/topic/options-trading/), and a $49 options course sells on Gumroad (https://loyalitalian.gumroad.com/l/options-trading-course). w2 covers finance professionals, not retail traders. (confidence high)
- Depth: d7: options trading (moderate). Strategy education, position management, backtesting and trade process are options trading, a moderate ledger depth; the founder can tell good from bad in this domain but not at a strong level.
- Supply: nothing needed that the founder lacks and cannot rent. Education, analytics and process coaching need judgment and accountability. Funded-trader capital is step 4 of the ladder and is supplied by prop firms, not the founder, so large capital is not a core need.
- Trust needed: no. Tools and courses at $15 to $100 a month are bought on free trials and reviews without knowing the maker; the exception is advice, which is excluded anyway.
- Spend evidence:
  - Paid options trading Discord or alert community: $47 to $224 monthly (USD 47 per month, about USD 47.00) [measured, page not checked] <https://whop.com/blog/options-trading-guide-discord-servers/>
  - OptionStrat paid membership (Live Tools): $39.99/month (USD 39.99 per month, about USD 39.99) [measured, page not checked] <https://optionstrat.com/membership>
  - Option Alpha automation and backtesting plan: $99/month (USD 99 per month, about USD 99.00) [measured, page not checked] <https://optionalpha.com/pricing>
  - Options trading course sold on Gumroad: $49 (USD 49 per one-off, about USD 49.00) [measured, page not checked] <https://loyalitalian.gumroad.com/l/options-trading-course>

### 4. Small business owners who gather in owner communities online (`small-business-owners-reddit-community`)

- Reach: search reach (s1); evidence: https://smith.ai/pricing/receptionists. w5 covers high-call-volume businesses in India and the Gulf and, per the ledger note, only existing TinyAI clients count as warm, while this room is mostly US and global owners, so it is not warm. Search reach is strong: owners buy AI receptionists from public pricing pages such as Smith.ai (AI plan $95/month), comparison guides list 15 such services priced $25 to $899 a month (https://bubblyphone.com/hub/ai-receptionist-pricing-compared), and Rosie reports over 1,900 businesses using it. (confidence high)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). The room's top paid problems, missed calls and being found when customers ask AI assistants, are AI voice agents and AI search visibility, a strong ledger depth; valuation at a sale (d2) covers a later rung, and staff and cash-flow pains are not covered.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains need a working AI product, judgment on setup and accountability; vendors (atoms) can be rented. Selling the business later may need a licensed broker in some US states, but that rung is not the core.
- Trust needed: yes. It is a B2B service where the product speaks to the owner's customers, so a wrong answer costs them business; even at $49 to $199 a month they want a vendor they can call, which is why comparison guides lean on reviews.
- Spend evidence:
  - My AI Front Desk AI receptionist: $99/mo (USD 99 per month, about USD 99.00) [measured, page not checked] <https://www.myaifrontdesk.com/pricing>
  - Smith.ai AI Receptionist starter plan: $95/month (USD 95 per month, about USD 95.00) [measured, page not checked] <https://smith.ai/pricing/receptionists>
  - Rosie AI answering service, Professional tier: $49/mo (USD 49 per month, about USD 49.00) [measured, page not checked] <https://serviceagent.ai/blogs/rosie-ai-pricing/>
  - Small business valuation before a sale (low end of the range): $2,500 to $5,000 (USD 2500 per one-off, about USD 2,500.00) [measured, page not checked] <https://www.bizworth.com/blog/valuation-costs-what-small-business-owners-should-expect-in-2026>

### 5. Small and mid-sized BPOs and contact-centre operators in India and the Philippines (`bpo-contact-centre-operators-india-philippines`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. Call centres in India are the first item in w5, so the Indian half of the room is exactly the businesses TinyAI sells to; the ledger note says the path is mostly cold unless they are existing clients, and the Philippines is outside w5's geography. Search reach also applies: operators buy dialers and QA tools from search and review sites, e.g. Bonvoice cloud telephony plans from ₹999/mo (https://bonvoice.com/pricing-plans/), Ozonetel on G2 and Capterra, and Enthu.ai call QA at $59 per agent per month (https://enthu.ai/pricing/). (confidence moderate)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). Dialers, call auditing and AI voice agents are the founder's strong domain of AI products for businesses; voice agents and call auditing are named in it.
- Supply: nothing needed that the founder lacks and cannot rent. Tooling, call audits and supervisor training need judgment, vendors and accountability. No large capital, ritual or licensed advocacy.
- Trust needed: yes. A B2B sale to an operator whose client contracts depend on quality scores; they buy from vendors they trust.
- Spend evidence:
  - Ozonetel cloud telephony and dialer, Starter plan per agent seat: $25/user/month (USD 25 per user per month, about USD 25.00) [measured, page not checked] <https://bonvoice.com/insights/ozonetel-pricing-in-india/>
  - Zendesk QA software to score and audit agent calls: $35 per agent, per month, billed annually (USD 35 per agent per month, about USD 35.00) [measured, page not checked] <https://www.zendesk.com/service/quality-assurance/customer-service-quality-assurance-software/>
  - Vapi AI voice-agent platform usage: $0.05 per minute (USD 0.05 per minute, about USD 0.05) [measured, page not checked] <https://vapi.ai/pricing>
  - Enthu.ai conversation intelligence and auto-QA, starting price: $59 per agent per month (USD 59 per agent per month, about USD 59.00) [measured, page not checked] <https://enthu.ai/pricing/>
  - Bonvoice cloud telephony plans in India, entry plan: From ₹999/mo (INR 999 per month, about USD 10.44) [measured, page not checked] <https://bonvoice.com/pricing-plans/>

### 6. Outsourced lead-generation and appointment-setting agencies running outbound call teams (`outbound-lead-gen-appointment-setting-agencies`)

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

### 7. Business brokers and boutique M&A advisers to small companies (`business-brokers-ma-boutiques`)

- Reach: search reach (s1); evidence: https://www.bizbuysell.com/brokers/Rates.aspx. w2 covers investment banking, private equity and finance professionals through colleagues; US business brokers selling $0.5M–$50M companies are a different trade and only a few boutique M&A advisers would be ex-colleagues, so warm is not claimed. The room already buys through search and public marketplaces: BizBuySell publishes a BrokerWorks rate card for broker listings, ValuSource and BizEquity sell valuation software by subscription (BizEquity ~$999/mo, https://deliverables.ai/guides/ai-tools-for-business-brokers-2026), and IBBA University sells the CBI course online. (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). The core paid problems are valuation, information memorandums, buyer outreach and due diligence; d2 (corporate finance, valuation, deal documents and transactions) covers them directly and is strong.
- Supply: nothing needed that the founder lacks and cannot rent. Valuation, memorandums and deal-process judgment are what the room needs; lawyers and accountants for due diligence are rentable licences (r1). No large capital, ritual or licensed advocacy at the core.
- Trust needed: yes. Valuation and memorandum work on a broker's client business is a B2B service sold on credibility, though a self-serve valuation or memo tool would need less.
- Spend evidence:
  - IBBA membership dues: $475 (USD 475 per year, about USD 475.00) [measured, page not checked] <https://en.wikipedia.org/wiki/International_Business_Broker's_Association>
  - BizBuySell listing plans, per listing: $66–$200 per month (USD 66 per month, about USD 66.00) [measured, page not checked] <https://investors.club/how-much-does-bizbuysell-cost/>
  - IBBA University CBI credential course: $2,089 (USD 2089 per package, about USD 2,089.00) [measured, page not checked] <https://ibbauniversity.org/topclass/topclass.do?expand-OfferingDetails-viaTC=1-offeringId%3D296609-viaTC%3D1>
  - IBBA Master's program (advanced deal training): $2,300 (USD 2300 per package, about USD 2,300.00) [measured, page not checked] <https://www.ibba.org/event/ibba-masters-program/>
  - BizEquity valuation platform subscription used by brokers for lead-generation valuations: ~$999/mo (USD 999 per month, about USD 999.00) [measured, page not checked] <https://deliverables.ai/guides/ai-tools-for-business-brokers-2026>

### 8. Independent perfumers and small fragrance brand founders (`indie-perfumers-launching-brands`)

- Reach: search reach (s1); evidence: https://www.udemy.com/course/the-ultimate-online-perfume-course/. This room buys through marketplaces and search: Udemy's best-selling perfume courses are bought by aspiring indie perfumers, Amazon lists perfume making kits with 600+ units bought in recent months (https://www.amazon.com/perfume-making-kit/s?k=perfume+making+kit), and compliance shops sell IFRA certificates and CPSRs online (https://thefragrancefoundry.com/products/ifra-certificate-allergens-certificate-cpsr). No ledger warm path covers hobbyist or indie perfumers. (confidence high)
- Depth: d8: fragrance (moderate). Fragrance (moderate, as an enthusiast) covers formulation, materials and scent judgment, which are the training and product steps. Compliance paperwork, contract filling and selling online are brand-building problems that no ledger depth names, though the founder is walking this ladder with v2.
- Supply: nothing needed that the founder lacks and cannot rent. The compliance step needs a qualified safety assessor, a licence the ledger says can be rented (r1), and bottles and filling come from vendors (r3). No large capital, ritual or licensed advocacy sits at the core.
- Trust needed: no. The room already buys kits, courses and compliance documents self-serve at tens to a few hundred dollars from strangers on marketplaces, so a self-serve guide or toolkit fits search reach; a live cohort would need more trust.
- Spend evidence:
  - Perfume making starter kit: $95 (USD 95 per one-off, about USD 95.00) [measured, page not checked] <https://boisdejasmin.com/2023/12/smell-training-and-perfume-making-kits.html>
  - Formal perfumery training programme: €3,300 (EUR 3300 per course, about USD 3,759.12) [measured, page not checked] <http://frenchperfume.school/intensetechnicaltraining>
  - IFRA-compliant formulas and safety documents before selling: $150–$1,000 (USD 150 per one-off, about USD 150.00) [measured, page not checked] <https://www.packamor.com/blogs/knowledge-hub/how-much-does-it-cost-to-start-a-perfume-brand>
  - IFRA certificate, allergens certificate and CPSR for one fragrance (The Fragrance Foundry, base cost): £299.99 (ex. VAT) (GBP 299.99 per one-off, about USD 397.38) [measured, page not checked] <https://thefragrancefoundry.com/products/ifra-certificate-allergens-certificate-cpsr>
  - Online perfumery training, from a basic course to a full programme with live support: £50 for a basic online course to £2,500 for a comprehensive programme with live support (GBP 50 per course, about USD 66.23) [measured, page not checked] <https://www.karengilbert.co.uk/getting-into-the-fragrance-industry>

### 9. Founders of US-incorporated startups facing 83(b) election and 409A valuation deadlines (`startup-founders-409a-83b-deadlines`)

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

### 10. Lenders' and insurers' tele-sales and collections floors in India (`lender-insurer-telesales-floors-india`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. The w5 text names lenders' and insurers' tele-sales word for word, and this room is in India, so its people are the people the TinyAI path covers; the w5 note says the path is mostly cold unless they are existing clients. Search reach also applies: the floors buy dialers through search, for example Ozonetel is listed with prices and reviews on Capterra India (https://www.capterra.in/software/1023229/ozonetel) and voice-AI vendors publish per-minute rate cards for NBFC collections (https://caller.digital/voice-ai-pricing-india). (confidence high)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). The core paid problems are dialers, AI voice bots for reminders and first-bucket collections, and call auditing for mis-selling and consent; d5 names voice agents and call auditing directly. Only the outsourced recovery agencies at the end of the ladder sit outside it.
- Supply: nothing needed that the founder lacks and cannot rent. The core pains need software, call-auditing judgment and a compliant calling process. Recovery agencies are vendors the lender already hires, and the product is not the collection itself. No large capital, ritual or licensed advocacy is needed.
- Trust needed: yes. A B2B deployment that speaks to a regulated lender's borrowers, priced per seat or per minute across thousands of calls, is bought on references and pilots, not self-serve.
- Spend evidence:
  - AI voice bot for collections and reminders, per minute (Caller Digital rate card): ₹2–12/Minute (INR 2 per minute, about USD 0.02) [measured, page not checked] <https://caller.digital/voice-ai-pricing-india>
  - Ozonetel cloud contact-centre seat, Starter plan: $25/user/month (USD 25 per user per month, about USD 25.00) [measured, page not checked] <https://bonvoice.com/insights/ozonetel-pricing-in-india/>
  - Zendesk QA call-auditing software, per agent: $35 per agent, per month, billed annually (USD 35 per agent per month, about USD 35.00) [measured, page not checked] <https://www.zendesk.com/service/quality-assurance/customer-service-quality-assurance-software/>
  - DLT entity registration fee before outbound calling or SMS (one-time, first platform): Rs. 5,900 (INR 5900 per one-off, about USD 61.64) [measured, page not checked] <https://crm.smsgatewayhub.com/knowledge-base/article/dlt-registration-charges-cost-breakdown-in-india>
  - Vistara AI voicebot for NBFC loan collections, starting rate per minute: ₹2.00/min (INR 2 per minute, about USD 0.02) [measured, page not checked] <https://www.vistaraai.in/voicebot-for-nbfc>

### 11. CFA candidates at all three levels who gather in candidate forums (`cfa-candidates-community`)

- Reach: warm path w2: investment banking, private equity and finance professionals. CFA candidates hold finance jobs, so they are the finance professionals w2 covers, and a banker's current and past colleagues include candidates at all three levels. Search reach also applies: Kaplan Schweser sells Level I packages at $379 to $1,449 (https://www.schweser.com/cfa/level-1/study-packages) and Mark Meldrum sells self-study video packages online, both bought through search. (confidence moderate)
- Depth: d2: corporate finance, valuation, deal documents and transactions (strong). Corporate finance, valuation and financial reporting are a large share of the CFA curriculum and the ledger's strong d2 depth, but the exam also tests ethics, portfolio management, fixed income, derivatives and economics, which the ledger does not list, so the match is partial.
- Supply: nothing needed that the founder lacks and cannot rent. The pains need study structure, judgment on hard topics, accountability to fixed exam windows and study peers; none needs large capital, ritual or licensed advocacy.
- Trust needed: yes. A pass-or-fail outcome with a $1,140 registration at stake and prep prices of $440 to $1,449 means buyers check who is behind a course or cohort, even though big brands sell self-serve from search.
- Spend evidence:
  - CFA Level I registration, early fee: USD 1,140 (USD 1140 per one-off, about USD 1,140.00) [measured, page not checked] <https://finance.uworld.com/cfa/registration-cost-fees/>
  - Kaplan Schweser Level I Premium package: $1,049 (USD 1049 per package, about USD 1,049.00) [measured, page not checked] <https://www.schweser.com/cfa/level-1/study-packages>
  - Kaplan Schweser Level I Essential self-study package: $749 (USD 749 per package, about USD 749.00) [measured, page not checked] <https://www.schweser.com/cfa/level-1/study-packages>
  - Mark Meldrum 2026 Level I Self-Study package (reported price): $440 (USD 440 per package, about USD 440.00) [measured, page not checked] <https://www.markmeldrum.com/product/2026-l1-self-study/>

### 12. Direct-to-consumer brands past launch, scaling on Shopify and marketplaces (`d2c-brands-scaling-past-launch`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. D2C brands are named in the w5 text, and the room's gathering places (D2C Insider, DTC Developers, Bharat Brands) are Indian, so the Indian half of the room sits on the TinyAI path; the note says mostly cold unless existing clients, and the worldwide part is not covered. Search reach applies too: the room buys through app stores, for example Gorgias sells its helpdesk on the Shopify App Store with 700+ reviews (https://apps.shopify.com/helpdesk) and Wati sells WhatsApp API plans from ₹2,499 per month. The founder also runs a D2C brand himself (v2), an insider path the ledger does not list as warm. (confidence moderate)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). The core paid problems past launch are WhatsApp support and cash-on-delivery confirmation, AI voice order calls, and being cited in AI answers; d5 names WhatsApp agents, voice agents and AI search visibility. Paid ads and marketplace expansion sit outside it.
- Supply: nothing needed that the founder lacks and cannot rent. Support automation, voice calls and AI visibility are software and judgment; ad agencies and logistics are vendors. No large capital, ritual or licensed advocacy at the core.
- Trust needed: yes. A voice or WhatsApp agent that talks to a brand's customers is a B2B deployment judged on returns avoided and support quality; a self-serve AI-visibility tracker would need less trust.
- Spend evidence:
  - Interakt WhatsApp Business API plan: ₹3,499 (INR 3499 per month, about USD 36.56) [measured, page not checked] <https://www.zoko.io/post/interakt-pricing-guide>
  - Vapi AI voice platform usage, per minute: $0.05 per minute (USD 0.05 per minute, about USD 0.05) [measured, page not checked] <https://vapi.ai/pricing>
  - Peec AI visibility tracking (brand citations in AI answers): $95 per month (USD 95 per month, about USD 95.00) [measured, page not checked] <https://visible.seranking.com/blog/peec-ai-review/>
  - Wati WhatsApp API Growth plan, India: ₹2,499 per month (INR 2499 per month, about USD 26.11) [measured, page not checked] <https://www.heltar.com/blogs/wati-pricing-in-india-explained-comprehensive-breakdown-2025>

### 13. Dubai real estate brokerages running agent floors and portal listings (`dubai-real-estate-brokerages-telesales`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. The ledger's TinyAI path covers businesses with large call volumes in the Gulf, including tele-sales floors, and Dubai brokerages are the Gulf's largest tele-sales floors; the path is mostly cold except for existing TinyAI clients, and brokerages are not named in the ledger's examples, so the match is by category rather than by name. (confidence moderate)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). Qualifying portal leads and following up by voice and WhatsApp within the calling rules is d5; portal listings, RERA compliance and brokerage itself are outside the ledger, and d3 is industrial real estate, not residential brokerage.
- Supply: nothing needed that the founder lacks and cannot rent. Inbound lead qualification and consented follow-up agents need no licence, large capital or ritual; brokerage itself needs a RERA licence the brokerage already holds, and outbound cold-calling is now regulated in the UAE, so the product must stay on inbound and permitted follow-up.
- Trust needed: yes. The agent would touch leads the brokerage pays AED 10,000 to 30,000 a month for, and could expose it to regulator fines if it calls wrongly, so owners buy after demos and referrals; a B2B service.
- Spend evidence:
  - Portal listing packages on Property Finder and Bayut per brokerage (Stage 1 ladder price): Dh10,000-Dh30,000 each month (AED 10000 per month, about USD 2,722.94) [measured, page not checked] <https://gulfnews.com/business/property/covid-19-spurned-on-ad-rates-uae-brokers-hit-back-at-property-portal-1.70973709>
  - Property Finder listing cost per listing (premium portal, as quoted in a portal comparison): AED 500-2,000+ per listing (AED 500 per per listing, about USD 136.15) [measured, page not checked] <https://joinoliva.com/en/learn/blog/bayut-vs-property-finder-which-to-use>
  - RERA broker card renewal (AED 500 fee plus AED 10 knowledge and AED 10 innovation fees): AED 520 (AED 520 per year, about USD 141.59) [measured, page not checked] <https://egsh.ae/insights/rera-professional-practice-card-dubai>
  - Real estate CRM for a Dubai brokerage (Stage 1 ladder price): AED 200-1,500/mo (AED 200 per month, about USD 54.46) [measured, page not checked] <https://codingclave.com/blog/real-estate-crm-dubai>

### 14. GRE test-takers of every country and field who prepare together in online GRE communities (`gre-preppers-worldwide-online`)

- Reach: warm path w1: Indian engineers and students preparing for the GRE to study abroad. Indian engineers preparing for the GRE are the largest slice of this worldwide room and w1 reaches them through the founder's GRE product and its users; the rest of the room is reached only by search. Search reach clearly applies too: the Magoosh GRE app has 4.8 stars from 10.9K App Store ratings with in-app purchases (https://apps.apple.com/us/app/gre-prep-practice-by-magoosh/id522118003), GregMat sells at $11.99 per month, and r/GRE threads recommend paying for them. (confidence moderate)
- Depth: d1: GRE quant and verbal (strong). The core paid problem is GRE quant and verbal preparation, the ledger's first strong depth; only the application rung at the end of the ladder falls outside it.
- Supply: nothing needed that the founder lacks and cannot rent. The pains need practice content, judgment on quant and verbal, accountability to a test date and study peers; no large capital, ritual or licensed advocacy is involved.
- Trust needed: no. This room buys self-serve prep at $8 to $179 from app stores and search on the strength of reviews, so the likely product is low-price and self-serve; a live cohort or tutoring rung would need more trust.
- Spend evidence:
  - GregMat+ monthly subscription: $11.99 per month (USD 11.99 per month, about USD 11.99) [measured, page not checked] <https://www.gregmat.com/pricing>
  - Magoosh GRE self-study plan: $179 (USD 179 per one-off, about USD 179.00) [measured, page not checked] <https://gre.magoosh.com/plans>
  - Target Test Prep GRE Flexible Preparation, month to month: $179 per month (USD 179 per month, about USD 179.00) [measured, page not checked] <https://gre.targettestprep.com/plans>
  - GRE exam registration: $220 (USD 220 per one-off, about USD 220.00) [measured, page not checked] <https://magoosh.com/gre/gre-exam-fee-and-cost/>

### 15. Salon and spa owners (1 to 10 locations) in India and worldwide (`salon-spa-owners-india-global`)

- Reach: warm path w5: businesses with large call volumes in India and the Gulf. The ledger's TinyAI path names salons in India, which covers the Indian half of this room; the path is mostly cold except for existing TinyAI clients. Search reach also holds worldwide: Fresha for Business has thousands of app-store ratings from salon owners (https://apps.apple.com/us/app/fresha-for-business/id1455346253?see-all=reviews&platform=iphone) and MioSalon is listed with prices on Capterra and SoftwareSuggest. (confidence moderate)
- Depth: d5: AI products for businesses: voice agents, WhatsApp agents, call auditing, AI search visibility (strong). WhatsApp reminders, rebooking and an AI receptionist for missed calls are d5; the services, staff and expansion steps are outside the ledger.
- Supply: nothing needed that the founder lacks and cannot rent. Booking, reminder and missed-call products need no licence, large capital or ritual; the salon's own services are physical work the owner already supplies.
- Trust needed: no. This room already buys booking and WhatsApp reminder software self-serve from app stores and pricing pages at ₹799 to ₹2,500 a month, so a low-priced reminder or rebooking product can sell without trust; a voice agent that answers the salon's phone would need more.
- Spend evidence:
  - Salon booking, billing and GST software, Indian entry plan (Stage 1 ladder price): from ₹799/mo (INR 799 per month, about USD 8.35) [measured, page not checked] <https://salonboost.online/compare-salon-softwares>
  - EaseSeat Elite plan: appointments, billing, CRM and own WhatsApp Business number: ₹849 per month (INR 849 per month, about USD 8.87) [measured, page not checked] <https://easeseat.com/>
  - SalonBoost Premium plan with WhatsApp automation, payroll and marketing: ₹1,499 per month (INR 1499 per month, about USD 15.66) [measured, page not checked] <https://salonboost.online/pricing>
  - MioSalon salon and spa software, starting price in India: INR 2,500 (INR 2500 per month, about USD 26.12) [measured, page not checked] <https://www.softwaresuggest.com/miosalon>

## Cut for rank (60)

These rooms passed every test but ranked below the limit. They are in graveyard.md.

- rank 16: indian-startup-founders-community (ladder 7, spend 0/4, reach search)
- rank 17: indie-hackers-bootstrapped-founders (ladder 7, spend 0/4, reach search)
- rank 18: non-target-students-breaking-into-finance (ladder 7, spend 0/4, reach search)
- rank 19: sat-us-undergrad-india (ladder 7, spend 0/4, reach search)
- rank 20: small-ca-firms-india (ladder 7, spend 0/4, reach search)
- rank 21: private-hospitals-india-ahpi (ladder 7, spend 0/4, reach warm)
- rank 22: test-prep-coaching-institutes-india (ladder 7, spend 0/4, reach warm)
- rank 23: consultants-planning-exit-to-finance (ladder 7, spend 0/4, reach search)
- rank 24: solar-wind-project-developers (ladder 7, spend 0/3, reach warm)
- rank 25: rooftop-solar-installers-epc (ladder 7, spend 0/3, reach search)
- rank 26: laid-off-finance-professionals (ladder 6, spend 0/5, reach warm)
- rank 27: mbb-case-interview-candidates (ladder 6, spend 0/5, reach search)
- rank 28: us-tcpa-ai-voice-outbound-callers (ladder 6, spend 0/5, reach search)
- rank 29: trai-dlt-160-series-outbound-callers (ladder 6, spend 0/5, reach warm)
- rank 30: independent-sponsors-small-pe-firms (ladder 6, spend 0/5, reach warm)
- rank 31: big4-transaction-services-fdd-associates-moving-to-ib-pe (ladder 6, spend 0/4, reach warm)
- rank 32: btech-students-india-reddit-community (ladder 6, spend 0/4, reach warm)
- rank 33: contact-centre-ops-managers (ladder 6, spend 0/4, reach warm)
- rank 34: industrial-brokers-and-developers (ladder 6, spend 0/4, reach warm)
- rank 35: restaurant-owners-india-cloud-kitchens (ladder 6, spend 0/4, reach warm)
- rank 36: brands-leasing-first-warehouse (ladder 6, spend 0/4, reach search)
- rank 37: desi-fragrance-addicts-india-community (ladder 6, spend 0/4, reach search)
- rank 38: first-time-founders-pre-seed (ladder 6, spend 0/4, reach search)
- rank 39: mid-career-searchers-buying-small-business (ladder 6, spend 0/4, reach search)
- rank 40: small-3pl-fulfilment-warehouse-operators (ladder 6, spend 0/4, reach search)
- rank 41: fragrance-enthusiasts-online-forums (ladder 6, spend 0/4, reach search)
- rank 42: dental-practice-owners-clinics (ladder 6, spend 0/3, reach search)
- rank 43: founders-selling-first-online-business (ladder 6, spend 0/3, reach search)
- rank 44: vibe-coders-building-apps-with-ai (ladder 6, spend 0/3, reach search)
- rank 45: sea-energy-companies-issb-climate-reporting (ladder 6, spend 0/3, reach warm)
- rank 46: ci-solar-developers-ipps-southeast-asia (ladder 6, spend 0/2, reach warm)
- rank 47: cre-analysts-underwriting (ladder 5, spend 0/7, reach warm)
- rank 48: valuation-analysts-pursuing-bv-credentials (ladder 5, spend 0/6, reach warm)
- rank 49: first-finance-hires-funded-startups (ladder 5, spend 0/6, reach warm)
- rank 50: corporate-development-associates-in-house-ma (ladder 5, spend 0/5, reach warm)
- rank 51: ib-associates-vps-leaving-banking (ladder 5, spend 0/5, reach warm)
- rank 52: indian-cas-moving-to-finance (ladder 5, spend 0/5, reach warm)
- rank 53: sell-side-equity-research-associates (ladder 5, spend 0/5, reach warm)
- rank 54: ai-agent-builders-freelance (ladder 5, spend 0/5, reach search)
- rank 55: ib-summer-analyst-recruits (ladder 5, spend 0/5, reach search)
- rank 56: indian-developers-moving-into-ai (ladder 5, spend 0/5, reach search)
- rank 57: oil-gas-engineers-mid-career (ladder 5, spend 0/5, reach search)
- rank 58: seo-agency-owners-ai-search (ladder 5, spend 0/5, reach search)
- rank 59: finance-pros-starting-fractional-cfo-practice (ladder 5, spend 0/5, reach warm)
- rank 60: ib-analysts-years-1-3 (ladder 5, spend 0/5, reach warm)
- rank 61: pe-associate-candidates-on-cycle (ladder 5, spend 0/5, reach warm)
- rank 62: mba-ib-associate-switchers (ladder 5, spend 0/5, reach search)
- rank 63: uk-commercial-landlords-mees-epc-deadline (ladder 5, spend 0/4, reach warm)
- rank 64: indian-retail-fno-traders-community (ladder 5, spend 0/4, reach search)
- rank 65: self-directed-value-investors-community (ladder 5, spend 0/4, reach search)
- rank 66: study-abroad-consultancies-india (ladder 5, spend 0/4, reach search)
- rank 67: energy-transition-career-switchers (ladder 5, spend 0/4, reach warm)
- rank 68: finra-series-79-sie-new-hires (ladder 5, spend 0/3, reach warm)
- rank 69: eu-ai-act-deadline-ai-product-teams (ladder 5, spend 0/3, reach search)
- rank 70: retiring-owners-selling-business (ladder 5, spend 0/3, reach search)
- rank 71: fpa-analysts-corporate (ladder 4, spend 0/5, reach search)
- rank 72: project-finance-analysts-energy-infra (ladder 4, spend 0/4, reach warm)
- rank 73: excel-financial-modellers-competition-community (ladder 4, spend 0/3, reach warm)
- rank 74: iim-isb-first-years-finance-consulting-placements (ladder 3, spend 0/7, reach search)
- rank 75: new-pe-associates-first-year (ladder 3, spend 0/5, reach warm)

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

- Search-reach rooms whose product needs trust: small-business-owners-reddit-community, business-brokers-ma-boutiques, startup-founders-409a-83b-deadlines. Search reach suits self-serve products; a product that needs trust usually needs a warm path.
- Rooms that overlap the founder's job (warm path w2/w4 or exclusion x2): cfa-candidates-community. Check the employer's outside-business rules before pursuing.
- Kept rooms that touch existing ventures (tagged, not excluded): gre-engineers-india (v1); small-business-owners-reddit-community (v4); bpo-contact-centre-operators-india-philippines (v4); outbound-lead-gen-appointment-setting-agencies (v4); indie-perfumers-launching-brands (v2, v4); lender-insurer-telesales-floors-india (v4); d2c-brands-scaling-past-launch (v4, v2); dubai-real-estate-brokerages-telesales (v4); gre-preppers-worldwide-online (v1); salon-spa-owners-india-global (v4).

## Price checks

Counts: seen_via_search 466.
