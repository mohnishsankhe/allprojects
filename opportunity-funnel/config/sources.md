# Sources and terms decisions

Rule 4: before a source is used, read its terms of use and its robots rules, then record the decision here and in the run's `RUNLOG.md`.
A decision is valid for 90 days. After that, check again.

Status values: `unchecked` (never checked; do not use yet), `allowed`, `allowed-with-limits` (write the limits), `skip` (write the reason).
"Robots rules" means the site's `robots.txt` file, which says which pages automated tools may fetch.

| Source | Adapter | What it gives | Domains the script must reach | Key needed | Terms to read | Status | Checked | Decision and reason |
|---|---|---|---|---|---|---|---|---|
| Stack Exchange API | `stackexchange` | Public Q&A (about 180 sites: expatriates, academia, money, law, parenting, workplace, travel...) | `api.stackexchange.com` | Optional `STACKEXCHANGE_KEY` (raises the daily quota from 300 to 10,000 requests) | https://stackoverflow.com/legal/api-terms-of-use and content licence https://stackoverflow.com/help/licensing | unchecked | | |
| Hacker News (Algolia search API) | `hackernews` | Public HN stories and comments (tech-heavy rooms only) | `hn.algolia.com` | none | https://hn.algolia.com/api and https://www.ycombinator.com/legal/ | unchecked | | |
| Reddit Data API | `reddit` | Public subreddit posts and comments | `www.reddit.com`, `oauth.reddit.com` | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` | https://redditinc.com/policies/data-api-terms, https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy, https://www.reddit.com/robots.txt | unchecked | | Commercial use and new API access may need Reddit's approval. Read before use. |
| YouTube Data API v3 | `youtube` | Public comments on the videos a room watches | `www.googleapis.com` | `YOUTUBE_API_KEY` | https://developers.google.com/youtube/terms/developer-policies and https://developers.google.com/youtube/terms/api-services-terms-of-service | unchecked | | The policies limit how long API data may be stored. Read before use. |
| Apple App Store reviews feed | `apple_reviews` | Public app reviews (RSS/JSON feed, up to 500 per app per country) | `itunes.apple.com` | none | https://www.apple.com/legal/internet-services/itunes/ and https://itunes.apple.com/robots.txt | unchecked | | |
| Google Play reviews | none | Public app reviews | | | https://play.google.com/about/play-terms/ | skip | 2026-09-26 | No official API for other people's app reviews; collecting them means scraping the store, which Google's terms forbid. |
| Public web pages | `web` | Forum threads, blogs, course and product review pages, price pages | each page's own domain | none | that site's terms and `/robots.txt` (the script checks robots.txt itself) | per site | | Checked per domain at first use. Sites that forbid automated access are skipped. |
| Discourse forums | `discourse` | Public threads on forums built with Discourse (they offer a public JSON view) | each forum's domain | none | that forum's terms and `/robots.txt` | per site | | |
| Search phrasing (Google or Bing autocomplete) | none | How people phrase searches | | | | skip | 2026-09-26 | Google has no official autocomplete API, and automated queries break its terms. Bing's Search APIs were retired in August 2025. Stand-in: question titles from stored Q&A and forum records. |
| Founder's chat exports | `inbox` | Closed-group chats the founder drops in `inbox/closed_groups/<room>/` | none (local files) | none | The founder's own responsibility to have the right to share them | allowed-with-limits | 2026-09-26 | Anonymized by the script before any reading. Never committed (`inbox/` is git-ignored). |
| Founder's customer messages | `inbox` | Customer messages in `inbox/customers/<room>/` (loop runs) | none | none | as above | allowed-with-limits | 2026-09-26 | As above. |

## Decision log

Append one line per check: `- YYYY-MM-DD | source | allowed/skip | reason | URL of the clause read`.
