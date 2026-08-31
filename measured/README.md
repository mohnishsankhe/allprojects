# MEASURED — hypothesis-test landing site

A pre-launch landing site for an Indian fragrance brand, built as an
**instrument** rather than a brochure. It exists to answer one question on cold
traffic:

> Does proof-framed positioning out-convert hope-framed positioning?

The single conversion event is a waitlist signup. The success metric is
`waitlist_submit` rate **per variant, per unique visitor**.

## Two rules the codebase enforces

**1 — A visitor sees exactly one variant, immediately.**
`proxy.ts` assigns the arm per request and hands it to the render as a header,
so there is no flash of the wrong copy and no duplicate variant markup in the
DOM. A flash would contaminate the experiment and inflate mobile bounce.

**2 — No claim appears that is not in the manifest.**
The brand's pitch is that it publishes its receipts, so claims are data, not
copy. Every number lives in `brand.config.ts`, every status lives in
`content/claims-manifest.json`, and `content/copy.ts` contains prose with
`{tokens}` and no digits at all. Two build checks enforce this rather than
trusting discipline.

## Getting started

```bash
npm install
cp .env.example .env.local     # then fill in WAITLIST_WEBHOOK_URL
npm run dev
```

With `WAITLIST_WEBHOOK_URL` unset the form still validates, but the API returns
a clear "not connected yet" error instead of pretending a signup was stored.

## Scripts

| Command | What it does |
| --- | --- |
| `npm run dev` | Development server |
| `npm run verify` | typecheck → lint → claims lint → unit tests → build → schema check |
| `npm run test` | Vitest unit tests |
| `npm run test:e2e` | Playwright, mobile (360×800) and desktop |
| `npm run lighthouse` | Mobile audit under both modelled and applied 4G throttling |
| `npm run check:claims` | Fails if a number appears outside the config |
| `npm run check:schema` | Fails if any review or rating markup reaches the HTML |

## How the A/B system works

Resolution order on every request: `?v=` → existing `variant` cookie →
random 50/50.

The chosen arm is written twice, and both writes are necessary:

1. onto the **request**, as `x-measured-variant`, because on a first visit the
   cookie exists only on the response — `await cookies()` in the page would not
   see it on that same request;
2. onto the **response**, as an `httpOnly` cookie, so the arm survives.

The client never reads the cookie. The server passes the variant down as a
prop, so what analytics reports and what the visitor saw cannot diverge.

`?v=` is deliberately **not** stripped by a redirect: a redirect would cost a
round trip on cold 4G traffic and mangle UTM-tagged ad URLs. A canonical link
tag keeps search engines from splitting on the param instead.

**The document must never be cached by a shared cache.** `proxy.ts` sets
`Cache-Control: private, no-store`. A CDN serving one visitor's arm to everyone
would destroy the experiment silently, while the site still looked fine.

Variants differ in exactly three ways: the hero block, the waitlist heading,
and section order (hope leads with product, proof leads with the argument).
Order is a real DOM reorder, not CSS `order`, so crawlers and screen readers
get the same narrative the eye does.

## Where things live

```
proxy.ts                 variant assignment (Next 16's replacement for middleware.ts)
brand.config.ts          every number, price, date and flag on the site
content/
  claims-manifest.json   the evidentiary root — 8 claims, each with a status
  manifest.ts            typed loader; an unknown claim id is a type error
  copy.ts                all prose, tokenized, containing no digits
  tokens.ts              {token} interpolation and en-IN price formatting
lib/                     variant, analytics, validation, rate limiting, JSON-LD
app/                     routes: /, /receipts, /api/waitlist, llms.txt, OG, robots, sitemap
components/              the sections
scripts/                 the two honesty checks and the Lighthouse gate
```

## Turning things on

**The street test (§4.7)** is not currently planned, so it renders nothing,
emits no `Event` schema, and its manifest row is hidden. To announce it, set
`streetTestPlanned = true` **and** a real `eventWindow` in `brand.config.ts`.
Announcing a date that does not exist is the one thing this brand cannot do.

**Renaming the brand** is one constant: change `BRAND.name`. The wordmark,
`<title>`, meta description, OG card, `llms.txt` and every copy token follow.
`tests/unit/brand-swap.test.ts` proves it, with one deliberate exception —
`MEASURED` is also a claim status, and the manifest's vocabulary survives a
rename.

## Performance

`npm run lighthouse` reports two LCP numbers, because the two throttling
methods disagree and only one of them reflects a browser:

- **observed** — real 4G throttling applied (1.6 Mbps, 150 ms RTT, 4× CPU) and
  the result measured. This is the gate: **< 2.0 s**, currently ~0.95–1.2 s.
- **modelled** — Lighthouse's default, which runs unthrottled and then models
  what 4G would have done. It is pessimistic and its output moves with the load
  on the machine running it, so it is printed but not gated.

Category scores are gated on the standard mobile preset (≥ 90 each).

The page keeps its weight down by staying server-rendered: the client bundle
carries an observer and a form, not the copy tree. `CountUp`, `InView` and
`FaqTracker` all wrap server-rendered children rather than importing content.

## Analytics and privacy

Plausible, loaded only when `PLAUSIBLE_DOMAIN` is set, with an inline queue stub
so events fired before the script lands are not lost. Every event carries
`variant`.

The site sets **one** cookie, for A/B consistency. That is disclosed in the
footer. Analytics are aggregate and cookie-free, which is why there is no
consent banner.
