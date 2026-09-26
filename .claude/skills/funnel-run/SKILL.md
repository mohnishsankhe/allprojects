---
name: funnel-run
description: Opportunity Funnel full run. Stages 1–6 plus the audit packet, ending with SHORTLIST.md, REVIEW.md and RUNLOG.md in runs/YYYY-MM-DD/. Runs to the end without stopping; needs a confirmed ledger from /funnel-setup.
argument-hint: "[--rooms N] [--run YYYY-MM-DD] [--only-room <slug>] (optional: limit the number of rooms, reuse a run folder, dry-run one room)"
disable-model-invocation: true
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Read `opportunity-funnel/.claude/skills/funnel-run/SKILL.md` (path from the repo root) and follow it exactly. Skip its frontmatter block. Arguments: `$ARGUMENTS`.
