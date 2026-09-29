# Privacy

## Who can use it
- Adults (18+) only. The age question comes first. Under 18, the reading is declined before anything is stored.
- Explicit consent is required before any processing. The person ticks the consent box, and its text and version are
  recorded (`rules/consent.json`).

## What is collected
- Only what the reading needs: the answers to the intake questions, free text or a pasted dialogue, the age as a
  number, and the consent timestamp and version.
- There is no name, email, phone, location or date of birth, and no tracking or analytics.
- Quotes that contain an email address, a phone number or a link are never used as evidence.

## Where it is kept, and for how long
- **Storage.** Answers, reports and check-ins are encrypted at rest with Fernet in a local SQLite file.
  - The file sits outside the repository (`ONTO_DATA_DIR`, default `~/.onto-insight`, mode 0700).
  - The key comes from `ONTO_DATA_KEY`, or from a key file with mode 0600.
- **Retention.** Data is kept for 90 days by default (`ONTO_RETENTION_DAYS`). `purge` deletes older records; run it
  daily (RUNBOOK.md).
- **After a safety stop**, the person's words are not kept. Only the route is recorded, and it is stored encrypted;
  the plain-text columns hold only a coarse status (ok, insufficient, stopped).
- **The person id** is taken only from the request body or the `X-Person-Id` header, never from the URL, so it does
  not reach access logs.

## The person's controls
- **View and export:** "My data" returns everything held about the person, as JSON.
- **Delete:** removes every reading and check-in and the person record, then vacuums the database file.

## Model calls
- With the model engine on, the person's words are sent to Anthropic's API to produce the reading. The consent text
  says so.
- The words are wrapped as data, never as instructions.
- The API base URL comes only from `ONTO_ANTHROPIC_BASE_URL`, default `https://api.anthropic.com`.

## What personal data is never used for
- Posts. The content engine draws only on the texts and on scenes written by the product.
- Evaluations. They use synthetic personas only.
- Logs. Logs hold ids, routes, step names, costs and error kinds, never text.
- The repository. `.env`, `sources_raw/`, databases and key files are git-ignored, and nothing personal is committed.
