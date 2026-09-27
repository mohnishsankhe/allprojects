---
name: funnel-listener
description: Opportunity Funnel Stage 3 for ONE room. Plans searches, labels records, checks saturation and drafts the room's pains with verified quotes. Invoked per room in modes plan, label, synthesize (or full when direct fetching works). Fresh context per room.
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Agent
model: claude-opus-5-5
effort: max
---

<!-- Pointer file. The real instructions live in opportunity-funnel/.claude/. It exists so the command works when Claude Code is opened at the repo root. -->

Your full instructions are in `opportunity-funnel/.claude/agents/funnel-listener.md` (path from the repo root). Read that file first and follow it exactly, skipping its frontmatter block. Everything in your task prompt still applies.
