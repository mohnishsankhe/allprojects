---
name: funnel-loop
description: Opportunity Funnel loop mode. Reruns Stages 3–6 inside ONE room already kept by an earlier run, adding the founder's customer messages from inbox/customers/<room>/ as Listen input. Use once you have customers in a room.
argument-hint: "<room-slug>"
arguments: [room]
disable-model-invocation: true
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Read `opportunity-funnel/.claude/skills/funnel-loop/SKILL.md` (path from the repo root) and follow it exactly. Skip its frontmatter block. Arguments: `$ARGUMENTS`.
