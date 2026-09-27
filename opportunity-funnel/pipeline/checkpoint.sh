#!/usr/bin/env bash
# Checkpoint (rule 12): refresh PROGRESS.md's auto-status block, then commit and push opportunity-funnel/ only.
# Usage: pipeline/checkpoint.sh RUN "what was finished"
# Safe to call from parallel agents: a lock serializes git, and a commit with nothing new is skipped.
set -u
RUN="${1:?usage: checkpoint.sh RUN MESSAGE}"
MSG="${2:?usage: checkpoint.sh RUN MESSAGE}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FUNNEL="$(dirname "$HERE")"
REPO="$(git -C "$FUNNEL" rev-parse --show-toplevel)"
BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
LOCK="${FUNNEL_GIT_LOCK:-/tmp/funnel-git.lock}"

(
  flock -w 300 9 || { echo "checkpoint: could not get the git lock in 5 minutes"; exit 1; }
  python3 "$FUNNEL/pipeline/funnel.py" --run "$RUN" progress >/dev/null 2>&1 || echo "checkpoint: 'funnel progress' failed (PROGRESS.md auto block not refreshed)"
  git -C "$REPO" add -- "$FUNNEL"
  if git -C "$REPO" diff --cached --quiet; then
    echo "checkpoint: nothing new to commit"
  else
    git -C "$REPO" commit -q -m "funnel: checkpoint - $MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0115cHwxiv7H724voU6jWo53" && echo "checkpoint: committed '$MSG'"
  fi
  for wait in 2 4 8 16; do
    git -C "$REPO" push -q origin "$BRANCH" 2>/dev/null && { echo "checkpoint: pushed to $BRANCH"; exit 0; }
    sleep "$wait"
  done
  echo "checkpoint: push failed after 4 tries (commit is saved locally)"
) 9>"$LOCK"
