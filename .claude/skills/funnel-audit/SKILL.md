---
name: funnel-audit
description: Opportunity Funnel audit intake. Reads the outside auditor's findings from inbox/audit_results/, updates the "Case against" section of each survivor in SHORTLIST.md, and re-ranks if the evidence warrants it, explaining each rank change in one line.
argument-hint: "[--run YYYY-MM-DD] (default: the latest run with a shortlist)"
disable-model-invocation: true
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Read `opportunity-funnel/.claude/skills/funnel-audit/SKILL.md` (path from the repo root) and follow it exactly. Skip its frontmatter block. Arguments: `$ARGUMENTS`.
