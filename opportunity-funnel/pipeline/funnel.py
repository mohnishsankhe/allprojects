#!/usr/bin/env python3
"""Opportunity Funnel command line.

    python3 pipeline/funnel.py <command> [--run RUN] [--dry-run] ...

Works from any working directory. Each module in MODULES exposes
`register(subparsers)`; a missing module is skipped with a one-line warning.
Global flags `--run` and `--dry-run` may come before or after the command.

Exit codes: 0 ok; 1 validation errors (numbered list); 2 missing inputs;
3 blocked (network or key), naming the domain or key.

Public API
----------
    MODULES: list[str]
    build_parser() -> argparse.ArgumentParser
    main(argv=None) -> int
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

import common  # noqa: E402

MODULES = ['records', 'harvest', 'quote_check', 'counts', 'sources', 'prices', 'stage1', 'stage2', 'stage3',
           'stage45', 'stage6', 'outputs', 'admin']


def _add_global_flags(parser: argparse.ArgumentParser, suppress: bool) -> None:
    default = argparse.SUPPRESS if suppress else None
    parser.add_argument("--run", default=default, metavar="RUN",
                        help="run folder: runs/YYYY-MM-DD, YYYY-MM-DD or a loop run name (default: today)")
    parser.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS if suppress else False,
                        help="count ranges become warnings instead of errors")


class _SubParser(argparse.ArgumentParser):
    """A command parser that also accepts the global flags after the command name."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_global_flags(self, suppress=True)


def build_parser(modules=None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="funnel",
        description="Opportunity Funnel scripts. The model does judgment; these do everything with a right answer.",
    )
    _add_global_flags(parser, suppress=False)
    sub = parser.add_subparsers(dest="command", metavar="<command>", parser_class=_SubParser)
    for name in (modules if modules is not None else MODULES):
        if importlib.util.find_spec(name) is None:
            print(f"warning: pipeline/{name}.py is missing; its commands are not available.", file=sys.stderr)
            continue
        mod = importlib.import_module(name)
        register = getattr(mod, "register", None)
        if register is None:
            print(f"warning: pipeline/{name}.py has no register(subparsers); skipped.", file=sys.stderr)
            continue
        register(sub)
    return parser


def _stage_of(args) -> int:
    """The stage a command belongs to, for the run log: the subparser's stage_no, else its --stage, else 0."""
    stage = getattr(args, "stage_no", None)
    if isinstance(stage, int) and not isinstance(stage, bool):
        return stage
    stage = getattr(args, "stage", None)
    if isinstance(stage, int) and not isinstance(stage, bool):
        return stage
    return 0


def _log_failure(args, err: common.FunnelError) -> None:
    """Record the error under the command's own stage. Never creates the run folder: a command that
    failed before anything ran must not leave an empty runs/<today>/ behind."""
    try:
        run = common.run_dir(getattr(args, "run", None))
        common.log_event(run, _stage_of(args), getattr(args, "command", "?"), "error", create_run=False,
                         code=err.code, errors=err.error_lines())
    except Exception:  # noqa: BLE001 - logging must never hide the real error
        pass


def _log_dry_run(args) -> None:
    """Mark the run log when a command ran with --dry-run, so `status` and `progress` can say so."""
    try:
        run = common.run_dir(getattr(args, "run", None))
        common.log_event(run, _stage_of(args), getattr(args, "command", "?"), "note", create_run=False, dry_run=True,
                         review=False, note=f"{getattr(args, 'command', '?')} ran with --dry-run: count ranges were "
                                            f"warnings and missing inputs were skipped; its outputs are not a finished run")
    except Exception:  # noqa: BLE001 - a marker must never break the command
        pass


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return common.EXIT_OK
    if not hasattr(args, "run"):
        args.run = None
    if not hasattr(args, "dry_run"):
        args.dry_run = False
    common.set_dry_run(args.dry_run)
    try:
        rc = args.func(args)
        if args.dry_run:
            _log_dry_run(args)
        return int(rc or 0)
    except common.FunnelError as e:
        _log_failure(args, e)
        try:
            common.fail(e)
        except SystemExit as se:
            return int(se.code or 0)
        return e.code
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
