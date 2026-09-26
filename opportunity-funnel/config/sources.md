# Sources and terms decisions

Rule 4: before a source is used, read its terms of use and its robots rules, then record the decision here and in the run's `RUNLOG.md`.
A decision is valid for 90 days. "Robots rules" = the site's `robots.txt` file, which says which pages automated tools may fetch.
Status: `unchecked` (don't use yet), `allowed`, `allowed-with-limits` (write the limits), `skip` (write the reason), `blocked-by-network` (the environment can't reach it; not a terms decision).

| Source | Adapter | What it gives | Domains the script must reach | Key needed | Terms to read | Status | Checked | Decision and reason |
|---|---|---|---|---|---|---|---|---|
| Web search (Claude's built-in search tool) | `harvest-search` | Titles and URLs of pages that match a query. No page text, usually no date. | none (runs on Anthropic's servers; results are read from this session's transcript files) | none | Anthropic usage policies; no third-party site is accessed | allowed-with-limits | 2026-09-26 | The only channel that works in this environment. Only titles and URLs are stored, exactly as the search tool returned them. The tool's written summary is never stored or quoted. Titles are thin evidence: tagged `[titles only]`. |
| Stack Exchange API | `stackexchange` | Public Q&A (about 180 sites) with full text and dates | `api.stackexchange.com` | Optional `STACKEXCHANGE_KEY` | https://stackoverflow.com/legal/api-terms-of-use, https://stackoverflow.com/help/licensing | blocked-by-network | 2026-09-26 | Terms not yet read (pages blocked too). Would add full question text with dates. |
| Hacker News (Algolia search API) | `hackernews` | Public HN stories and comments | `hn.algolia.com` | none | https://hn.algolia.com/api, https://www.ycombinator.com/legal/ | blocked-by-network | 2026-09-26 | Would add founder and engineer discussions with dates. |
| Reddit Data API | `reddit` | Public subreddit posts and comments | `www.reddit.com`, `oauth.reddit.com` | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` | https://redditinc.com/policies/data-api-terms, https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy | skip | 2026-09-26 | No key given, and Reddit has required pre-approval for all API access since November 2025. Would add the largest body of first-person posts for most consumer rooms. Reddit titles still appear through web search. |
| YouTube Data API v3 | `youtube` | Public comments on videos a room watches | `www.googleapis.com` (reachable) | `YOUTUBE_API_KEY` | https://developers.google.com/youtube/terms/developer-policies | skip | 2026-09-26 | No key given. Would add thousands of dated comments per room (exam prep, trading, fragrance rooms especially). |
| Apple App Store reviews feed | `apple_reviews` | Public app reviews with dates and ratings | `itunes.apple.com` | none | https://www.apple.com/legal/internet-services/itunes/ | blocked-by-network | 2026-09-26 | Would add dated reviews of competing apps (complaints = unmet pain). |
| Google Play reviews | none | Public app reviews | | | https://play.google.com/about/play-terms/ | skip | 2026-09-26 | No official API for other people's app reviews; collecting them means scraping the store, which Google's terms forbid. |
| Common Crawl (public web archive) | none | Raw copies of public pages | `data.commoncrawl.org` (blocked), `commoncrawl.s3.amazonaws.com` (needs an AWS account) | AWS account | https://commoncrawl.org/terms-of-use | skip | 2026-09-26 | The open copy is blocked by the network; the S3 copy needs an AWS login, which rule 4 forbids us to use. |
| Public web pages | `web` | Forum threads, blogs, review pages, pricing pages, job posts, official deadlines | each page's own domain | none | that site's terms and `/robots.txt` (the script checks robots.txt itself) | blocked-by-network | 2026-09-26 | Would add full page text and let the price checker confirm prices on the page. |
| Discourse forums | `discourse` | Public threads on Discourse forums | each forum's domain | none | that forum's terms and `/robots.txt` | blocked-by-network | 2026-09-26 | |
| Job boards (LinkedIn, Indeed, Naukri, Glassdoor) | none (titles via web search only) | Job posts: a company hiring for a problem already pays for it | | | their terms forbid scraping | allowed-with-limits | 2026-09-26 | Pages are never fetched. Job-post titles and URLs arrive only through web search. |
| Search phrasing (Google or Bing autocomplete) | none | How people phrase searches | | | | skip | 2026-09-26 | Google has no official autocomplete API and forbids automated queries; Bing's Search APIs were retired in August 2025. Stand-in: question and thread titles from web search. |
| Founder's chat exports | `inbox` | Closed-group chats in `inbox/closed_groups/<room>/` | none (local files) | none | The founder's own responsibility | allowed-with-limits | 2026-09-26 | Anonymized by the script before any reading. Never committed. |
| Founder's customer messages | `inbox` | Customer messages in `inbox/customers/<room>/` (loop runs) | none | none | as above | allowed-with-limits | 2026-09-26 | As above. |

## Domains to allow (for a full-text run)
Set the environment's network access to **Full** (the scripts still check robots.txt and terms per site), or allow at least:
`api.stackexchange.com`, `hn.algolia.com`, `itunes.apple.com`, `data.commoncrawl.org`, `stackoverflow.com`, `stackexchange.com`, `www.ycombinator.com`, `www.apple.com`, `developers.google.com`, plus the forum, review, pricing and job-post domains each run lists in its `RUNLOG.md`.

## Decision log
Append one line per check: `- YYYY-MM-DD | source | status | reason | URL of the clause read`.
- 2026-09-26 | web search | allowed-with-limits | titles and URLs only, captured verbatim from session transcripts; summaries never stored | (tool of this session)
- 2026-09-26 | Reddit Data API | skip | pre-approval required since Nov 2025; no key | https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
- 2026-09-26 | YouTube Data API | skip | no API key given | https://developers.google.com/youtube/terms/developer-policies
- 2026-09-26 | Common Crawl on S3 | skip | needs an AWS account login | https://commoncrawl.org/terms-of-use
- 2026-09-26 | Google Play reviews | skip | no official API; scraping forbidden | https://play.google.com/about/play-terms/
