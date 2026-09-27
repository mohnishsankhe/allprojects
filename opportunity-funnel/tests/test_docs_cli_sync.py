"""Docs and CLI in sync.

Every `funnel <command> [--flags]` usage in `.claude/skills/*/SKILL.md` and `.claude/agents/*.md` must name a
command the CLI has, with flags that command accepts. The usages are parsed from the files at collection time,
one test per usage, so a failure names the file, the line and the exact text. The CLI is read through
`funnel.build_parser()` (the same code the entry point runs). A second check runs `python3 pipeline/funnel.py --help`
from /tmp and from the project folder and expects every documented command in the listing.
"""
import argparse
import re
import subprocess
import sys

import pytest

import funnel
from conftest import PIPELINE, REAL_ROOT

DOC_FILES = sorted(list((REAL_ROOT / ".claude" / "skills").glob("*/SKILL.md")) + list((REAL_ROOT / ".claude" / "agents").glob("*.md")))
# `funnel <command> ...`: a command word after "funnel " (never "/funnel-run", "funnel-walker" or "`funnel` means"),
# then the rest of the usage up to a closing backtick, a line end or the next `funnel ` usage.
USAGE_RE = re.compile(r"(?<![\w/-])funnel ([a-z][a-z0-9-]*)((?:(?!funnel )[^`\n])*)")
FLAG_RE = re.compile(r"(?<!\S)(--[a-z][a-z0-9-]*)")
MUST_BE_DOCUMENTED = {"preflight", "ledger-check", "rooms", "fx", "mask", "harvest-search", "batches", "count", "saturation",
                      "quote-check", "pains", "walks", "pairs", "numbers", "redteam", "audit-packet", "shortlist", "review",
                      "runlog", "progress", "status", "commit-message", "show", "log", "compare", "loop-init", "ingest-inbox"}


def documented_usages() -> list:
    """(doc, line, command, flags, usage text) for every `funnel <command> ...` in the skill and agent files."""
    out = []
    for path in DOC_FILES:
        text = path.read_text(encoding="utf-8")
        for m in USAGE_RE.finditer(text):
            cmd, rest = m.group(1), m.group(2)
            line = text.count("\n", 0, m.start()) + 1
            out.append((path.relative_to(REAL_ROOT).as_posix(), line, cmd, tuple(FLAG_RE.findall(rest)), m.group(0).strip()))
    return out


USAGES = documented_usages()
DOCUMENTED_COMMANDS = sorted({u[2] for u in USAGES})


@pytest.fixture(scope="module")
def commands() -> dict:
    """command name -> its argparse subparser, from the real CLI."""
    parser = funnel.build_parser()
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    return dict(sub.choices)


def test_the_docs_were_parsed():
    assert len(DOC_FILES) >= 6, [p.name for p in DOC_FILES]
    assert len(USAGES) >= 40, "the usage parser found too few `funnel <command>` usages"
    missing = MUST_BE_DOCUMENTED - set(DOCUMENTED_COMMANDS)
    assert not missing, f"commands the skills and agents no longer mention: {sorted(missing)}"


@pytest.mark.parametrize("doc,line,cmd,flags,usage", USAGES, ids=[f"{u[0]}:{u[1]}:{u[2]}" for u in USAGES])
def test_every_documented_command_and_flag_exists(commands, doc, line, cmd, flags, usage):
    assert cmd in commands, (f"{doc}:{line}: `{usage}` names a command the CLI does not have. "
                             f"The CLI has: {', '.join(sorted(commands))}.")
    known = {k for k in commands[cmd]._option_string_actions if k.startswith("--")}
    for flag in flags:
        assert flag in known, f"{doc}:{line}: `{usage}`: `funnel {cmd}` has no flag {flag}. It has: {', '.join(sorted(known))}."


def test_every_documented_command_has_working_help():
    for cmd in DOCUMENTED_COMMANDS:
        r = subprocess.run([sys.executable, str(PIPELINE / "funnel.py"), cmd, "--help"], capture_output=True, text=True, cwd="/tmp")
        assert r.returncode == 0 and r.stdout.startswith(f"usage: funnel {cmd}"), f"{cmd}: {r.stdout[:80]!r} {r.stderr[:200]!r}"
        for doc, line, c, flags, usage in USAGES:
            if c == cmd:
                for flag in flags:
                    assert flag in r.stdout, f"{doc}:{line}: `{usage}`: {flag} is not in `funnel {cmd} --help`"


@pytest.mark.parametrize("cwd,script", [("/tmp", str(PIPELINE / "funnel.py")), (str(REAL_ROOT), "pipeline/funnel.py")],
                         ids=["from-tmp", "from-project-folder"])
def test_help_works_from_any_directory(cwd, script):
    r = subprocess.run([sys.executable, script, "--help"], capture_output=True, text=True, cwd=cwd)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("usage: funnel [-h] [--run RUN] [--dry-run] <command>")
    assert not r.stderr.strip(), f"warnings on --help: {r.stderr}"
    for cmd in DOCUMENTED_COMMANDS:
        assert re.search(rf"^\s+{re.escape(cmd)}\b", r.stdout, re.M), f"{cmd} is not listed by `funnel --help`"
