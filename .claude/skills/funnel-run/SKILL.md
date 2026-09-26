---
name: funnel-run
description: Opportunity Funnel full run at maximum depth. Stages 1–6, red team and audit packet, ending with SHORTLIST.md, REVIEW.md and RUNLOG.md in runs/YYYY-MM-DD/. Never asks the founder anything; checkpoints to PROGRESS.md and git after every stage and every Stage 3 room.
argument-hint: "[--run YYYY-MM-DD] [--only-room <slug>] (resume a run folder; dry-run one room)"
disable-model-invocation: true
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Read `opportunity-funnel/.claude/skills/funnel-run/SKILL.md` (path from the repo root) and follow it exactly. Skip its frontmatter block. Arguments: `$ARGUMENTS`.
