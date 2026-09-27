---
name: funnel-setup
description: Opportunity Funnel Stage 0. Checks config/ledger.md without interviewing the founder, refreshes its machine-readable transcription config/ledger.yaml, and lists every [assumed] item, default and gap for REVIEW.md. Never asks the founder anything.
disable-model-invocation: true
model: claude-opus-5-5
effort: max
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Read `opportunity-funnel/.claude/skills/funnel-setup/SKILL.md` (path from the repo root) and follow it exactly. Skip its frontmatter block. Arguments: `$ARGUMENTS`.
