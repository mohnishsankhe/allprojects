---
name: funnel-setup
description: Opportunity Funnel Stage 0. Checks config/ledger.md without interviewing the founder, refreshes its machine-readable transcription config/ledger.yaml, and lists every [assumed] item, default and gap for REVIEW.md. Never asks the founder anything.
disable-model-invocation: true
model: claude-opus-5-5
effort: max
---

# /funnel-setup: Stage 0, the ledger (no interview)

The founder writes `config/ledger.md`. This command never interviews or waits for them (rule 10).
`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py`. Stay inside `opportunity-funnel/`.

1. Run `funnel init`.
2. If `config/ledger.md` is missing: stop and say, in one line, that the founder must write it (the template is the Ledger section of `config/formats.md`). This is the only case where the pipeline cannot proceed.
3. Run `funnel ledger-check`. If it reports that `config/ledger.yaml` no longer matches `ledger.md` (a `text` field not found word for word), update `ledger.yaml` to transcribe the current `ledger.md` exactly: keep the ids stable, copy each bullet into `text`, map human walls to W-IDs (`config/walls.md`), numbers to fields, and state every mapping choice in a `note`. Add nothing the founder didn't write. Anything unclear gets the conservative reading and a `note`.
4. Rerun `funnel ledger-check` until it passes.
5. Report in a few lines: the ledger's sections, every `[assumed]` item (they go to REVIEW.md), human walls the ledger doesn't mention (treated as not supplied), and any conservative reading you applied.
