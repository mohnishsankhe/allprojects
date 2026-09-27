"""Shared helpers for every pipeline module.

Everything here has a right answer and is done in code (rule 2). Nothing here
prints or stores API keys. All file output is deterministic: JSON is written
with sort_keys, indent 2, ensure_ascii False and a trailing newline.

Public API
----------
Paths
    FUNNEL_ROOT: Path                 root of opportunity-funnel/ (env FUNNEL_ROOT_OVERRIDE wins)
    funnel_root() -> Path              same, re-read from the environment on every call
    config_dir() -> Path               FUNNEL_ROOT/config
    today() -> datetime.date           today, or env FUNNEL_TODAY (YYYY-MM-DD) for tests
    run_dir(run=None) -> Path          RUN folder from "runs/2026-09-26", "2026-09-26", a loop name or a Path
    run_name(run=None) -> str          the run folder's name
    run_date(run=None) -> datetime.date  the date in the run name
    listen_dir(run) -> Path            RUN/03_listen
    room_dir(run, room) -> Path        RUN/03_listen/rooms/<room>
    raw_dir(run, room) -> Path         RUN/03_listen/raw/<room>
    rel(path) -> str                   path relative to FUNNEL_ROOT, for messages
    require_file(path, hint="") -> Path  raise MissingInput (exit 2) if the file is missing

Config
    load_kill_rules() -> dict          config/kill_rules.yaml
    load_ledger() -> dict              config/ledger.yaml
    load_walls() -> dict               {"W1": {"name": "Trigger", "kind": "machine"}, ...} from config/walls.md
    MACHINE_WALLS, HUMAN_WALLS         ranges of wall numbers (1-16, 17-29)

Files
    read_json(path) -> object
    write_json(path, obj) -> None
    read_jsonl(path) -> list[dict]     raises ValidationErrors on a bad line
    write_jsonl(path, rows) -> None
    append_jsonl(path, row) -> None
    read_text(path) -> str
    write_text(path, text) -> None     always ends with one newline

Text and ids
    normalize_ws(s) -> str             Unicode NFC, every whitespace run -> one space, strip
    record_id(url, text) -> str        sha256(url + "\\n" + normalize_ws(text)).hexdigest()[:16]
    domain_of(url) -> str              host, lower case, without "www."
    is_slug(s) -> bool                 lowercase letters, digits, hyphens
    check_slug(s, what="slug") -> str  returns s or raises ValidationErrors (also refuses path traversal)
    pain_id(room, key) -> str          "<room>--<key>"
    split_pain_id(pid) -> (room, key)
    rng_for_run(run) -> random.Random  seeded from the run name

Checks (each returns a list of plain-English error strings, empty when fine)
    check_judgment(obj, where) -> list[str]
    check_number(obj, where, allow_null=False) -> list[str]
    check_price(obj, where) -> list[str]
    is_date(s) -> bool                 "YYYY-MM-DD" and a real calendar date

Graveyard (FUNNEL_ROOT/graveyard.md)
    parse_graveyard() -> list[dict]    [{"date", "stage", "item", "reason", "status": "dead"|"revived", "revivals": [...]}]
    dead_items(kind=None) -> set[str]  items still dead ("room:<slug>", "pain:<id>"); kind filters the prefix.
                                       An item's LAST line in file order decides: a kill line after a revival
                                       kills it again; a revival note under the last kill line revives it.
    dead_entries(kind=None, ignore_date=None) -> dict[item -> entry]
                                       the last kill line of every item still dead, ignoring lines dated
                                       `ignore_date` (a run's own later kills) for the decision as well
    is_dead(item) -> bool
    append_graveyard(date, stage, item, reason) -> bool   True if the file changed; never duplicates a line
    sync_graveyard(date, stage, scope, kills) -> dict
                                       make the lines dated `date` for `stage` match `kills` (item -> reason)
                                       for every item in `scope`: add missing lines, fix reasons, drop lines of
                                       items the rerun keeps (a line with a revival note is kept). Never writes
                                       in a dry run.

Events and secrets
    log_event(run, stage, command, kind, create_run=True, **fields) -> dict | None
                                       appends to RUN/runlog.jsonl; with create_run False it writes nothing
                                       (and returns None) when the run folder does not exist yet
    get_key(name) -> str | None        environment first, then FUNNEL_ROOT/.env; never printed
    set_dry_run(flag), is_dry_run()    the global --dry-run switch

FX
    read_fx_file(run) -> dict          the raw RUN/fx_rates.json
    load_fx(run) -> dict               {"USD": 1.0, "INR": 88.0, ...} (units per USD)
    to_usd(amount, currency, fx) -> float
    from_usd(amount_usd, currency, fx) -> float
    convert(amount, currency_from, currency_to, fx) -> float

Errors and exit codes
    FunnelError(code)                  base class
    ValidationErrors(errors, code=1)   a list of things the model must fix
    MissingInput(message)              exit 2
    Blocked(message)                   exit 3 (network or key), message names the domain or key
    MissingCurrency(currency)          a ValidationErrors naming the currency
    fail(errors, code=1)               print a numbered list and sys.exit(code)
    EXIT_OK, EXIT_VALIDATION, EXIT_MISSING, EXIT_BLOCKED = 0, 1, 2, 3
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import random
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

import yaml

EXIT_OK = 0
EXIT_VALIDATION = 1
EXIT_MISSING = 2
EXIT_BLOCKED = 3

CONFIDENCE_LEVELS = ("high", "moderate", "low")
NUMBER_TAGS = ("measured", "estimate")
SEEN_VIA = ("page", "search")

MACHINE_WALLS = range(1, 17)
HUMAN_WALLS = range(17, 30)

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# A run is `YYYY-MM-DD`, a loop run `YYYY-MM-DD-loop-<room>` or a dry run `YYYY-MM-DD-dry-<room>` (a one-room
# dry run of Stages 3-6 that must not be mistaken for the real run: rooms-known, compare and audit-status skip it).
_RUN_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(?:loop|dry)-[a-z0-9]+(?:-[a-z0-9]+)*)?$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")

_DRY_RUN = False


# --------------------------------------------------------------------------- errors
class FunnelError(Exception):
    """Base class. `code` is the process exit code."""

    code = EXIT_VALIDATION

    def __init__(self, message: str = "", code: int | None = None):
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code

    def error_lines(self) -> list[str]:
        return [self.message] if self.message else []


class ValidationErrors(FunnelError):
    """One or more things the model must fix. Exit code 1."""

    code = EXIT_VALIDATION

    def __init__(self, errors, code: int = EXIT_VALIDATION):
        if isinstance(errors, str):
            errors = [errors]
        self.errors = [str(e) for e in errors]
        super().__init__("; ".join(self.errors), code)

    def error_lines(self) -> list[str]:
        return list(self.errors)


class MissingInput(FunnelError):
    """An input file is missing. Exit code 2."""

    code = EXIT_MISSING


class Blocked(FunnelError):
    """Network or key blocked. Exit code 3. The message names the domain or key."""

    code = EXIT_BLOCKED


class MissingCurrency(ValidationErrors):
    """No exchange rate for a currency. Names the currency."""

    def __init__(self, currency: str):
        self.currency = currency
        super().__init__(
            [f"fx_rates.json: no rate for currency {currency}. "
             f"Add {currency} with its per_usd rate and a URL, then rerun `funnel fx`."]
        )


def fail(errors, code: int = EXIT_VALIDATION) -> None:
    """Print a numbered plain-English list to stderr and exit with `code`."""
    if isinstance(errors, FunnelError):
        code = errors.code
        errors = errors.error_lines()
    elif isinstance(errors, str):
        errors = [errors]
    errors = [str(e) for e in errors] or ["unknown error"]
    label = {EXIT_VALIDATION: "Fix these", EXIT_MISSING: "Missing input", EXIT_BLOCKED: "Blocked"}.get(code, "Error")
    n = len(errors)
    print(f"{label}: {n} item{'s' if n != 1 else ''}", file=sys.stderr)
    for i, err in enumerate(errors, 1):
        print(f"{i}. {err}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------- paths
def funnel_root() -> Path:
    override = os.environ.get("FUNNEL_ROOT_OVERRIDE")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parent.parent


FUNNEL_ROOT: Path = funnel_root()


def config_dir() -> Path:
    return funnel_root() / "config"


def today() -> _dt.date:
    forced = os.environ.get("FUNNEL_TODAY")
    if forced:
        return _dt.date.fromisoformat(forced)
    return _dt.date.today()


def run_name(run=None) -> str:
    """Normalize `runs/2026-09-26`, `2026-09-26`, a loop name or a Path to the run folder name."""
    if run is None:
        return today().isoformat()
    if isinstance(run, Path):
        return run.name
    s = str(run).strip().rstrip("/")
    if os.path.isabs(s):
        return Path(s).name
    if s.startswith("runs/"):
        s = s[len("runs/"):]
    if not _RUN_NAME_RE.match(s):
        raise ValidationErrors(
            [f"--run {run!r}: a run is `runs/YYYY-MM-DD`, `YYYY-MM-DD`, `YYYY-MM-DD-loop-<room-slug>` or, for a "
             f"one-room dry run, `YYYY-MM-DD-dry-<room-slug>`."]
        )
    return s


def run_dir(run=None) -> Path:
    """The RUN folder. Does not create it."""
    if isinstance(run, Path):
        return run
    if run is not None and os.path.isabs(str(run)):
        p = Path(str(run)).resolve()
        runs = (funnel_root() / "runs").resolve()
        if runs not in p.parents:
            raise ValidationErrors([f"--run {run!r}: a run folder must live under {rel(runs)}/."])
        return p
    return funnel_root() / "runs" / run_name(run)


def run_date(run=None) -> _dt.date:
    name = run_name(run)
    return _dt.date.fromisoformat(name[:10])


def listen_dir(run) -> Path:
    return run_dir(run) / "03_listen"


def room_dir(run, room: str) -> Path:
    return listen_dir(run) / "rooms" / check_slug(room, "room")


def raw_dir(run, room: str) -> Path:
    return listen_dir(run) / "raw" / check_slug(room, "room")


def rel(path) -> str:
    """A path relative to the funnel root, for messages."""
    p = Path(path)
    try:
        return str(p.resolve().relative_to(funnel_root().resolve()))
    except ValueError:
        return str(p)


def require_file(path, hint: str = "") -> Path:
    p = Path(path)
    if not p.exists():
        msg = f"{rel(p)} is missing."
        if hint:
            msg += " " + hint
        raise MissingInput(msg)
    return p


# --------------------------------------------------------------------------- config
def load_kill_rules() -> dict:
    with open(config_dir() / "kill_rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_ledger() -> dict:
    with open(config_dir() / "ledger.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_WALL_LINE_RE = re.compile(r"^\s*-\s*\*\*(W\d+)\s+([^:*]+?):?\*\*")


def load_walls() -> dict:
    """W-ID -> {"name": ..., "kind": "machine"|"human"} from config/walls.md."""
    walls: dict[str, dict] = {}
    kind = None
    with open(config_dir() / "walls.md", encoding="utf-8") as f:
        for line in f:
            low = line.lower()
            if low.startswith("## "):
                if "machine" in low:
                    kind = "machine"
                elif "human" in low:
                    kind = "human"
                else:
                    kind = None
                continue
            m = _WALL_LINE_RE.match(line)
            if not m:
                continue
            wid, name = m.group(1), m.group(2).strip()
            num = int(wid[1:])
            k = kind or ("machine" if num in MACHINE_WALLS else "human")
            walls[wid] = {"name": name, "kind": k}
    return dict(sorted(walls.items(), key=lambda kv: int(kv[0][1:])))


# --------------------------------------------------------------------------- files
def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dumps_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def write_json(path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(dumps_json(obj))


def read_jsonl(path) -> list:
    rows = []
    p = Path(path)
    with open(p, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValidationErrors([f"{rel(p)}: line {n}: not valid JSON ({e.msg}). Fix or remove the line."])
    return rows


def dumps_jsonl_row(row) -> str:
    return json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n"


def write_jsonl(path, rows) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(dumps_jsonl_row(row))


def append_jsonl(path, row) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(dumps_jsonl_row(row))


def read_text(path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_text(path, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


# --------------------------------------------------------------------------- text and ids
_WS_RE = re.compile(r"\s+")


def normalize_ws(s: str) -> str:
    """Unicode NFC; every whitespace run becomes one space; strip. Nothing else changes."""
    if s is None:
        return ""
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", str(s))).strip()


def record_id(url: str, text: str) -> str:
    """First 16 hex characters of SHA-256 over url + "\\n" + normalize_ws(text)."""
    payload = (url or "") + "\n" + normalize_ws(text)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def domain_of(url: str) -> str:
    """Host name in lower case without a leading "www."; "" when there is none."""
    if not url:
        return ""
    s = str(url).strip()
    if "://" not in s:
        s = "http://" + s
    host = (urlsplit(s).hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def is_slug(s) -> bool:
    return isinstance(s, str) and bool(_SLUG_RE.match(s))


def check_slug(s, what: str = "slug") -> str:
    """Return `s` if it is a safe slug; otherwise raise ValidationErrors. Refuses path traversal."""
    if not is_slug(s):
        raise ValidationErrors(
            [f"{what} {s!r} is not a valid slug: use lowercase letters, digits and hyphens only "
             f"(no slashes, dots or spaces)."]
        )
    return s


def pain_id(room: str, key: str) -> str:
    return f"{check_slug(room, 'room')}--{check_slug(key, 'pain key')}"


def split_pain_id(pid: str) -> tuple:
    if not isinstance(pid, str) or "--" not in pid:
        raise ValidationErrors([f"pain_id {pid!r} must look like <room-slug>--<pain-key>."])
    room, _, key = pid.partition("--")
    return check_slug(room, "room"), check_slug(key, "pain key")


def rng_for_run(run=None) -> random.Random:
    return random.Random(run_name(run))


def is_date(s) -> bool:
    if not isinstance(s, str) or not _DATE_RE.match(s):
        return False
    try:
        _dt.date.fromisoformat(s)
    except ValueError:
        return False
    return True


# --------------------------------------------------------------------------- checks
def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def check_judgment(obj, where: str) -> list:
    """A judgment object needs `reasoning` (one or two sentences) and `confidence` high/moderate/low."""
    errors = []
    if not isinstance(obj, dict):
        return [f"{where}: must be an object with 'reasoning' and 'confidence'."]
    reasoning = obj.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        errors.append(f"{where}: missing 'reasoning'. Add one or two sentences.")
    conf = obj.get("confidence")
    if conf not in CONFIDENCE_LEVELS:
        errors.append(f"{where}: 'confidence' must be high, moderate or low (got {conf!r}).")
    return errors


def check_number(obj, where: str, allow_null: bool = False) -> list:
    """A model-supplied number: {"value", "tag": measured|estimate, "url"/"record_ids" or "reasoning"}."""
    if not isinstance(obj, dict):
        return [f"{where}: must be an object like {{\"value\": 120, \"tag\": \"estimate\", \"reasoning\": \"...\"}}."]
    errors = []
    value = obj.get("value")
    if value is None:
        if not allow_null:
            errors.append(f"{where}: 'value' is missing. Give a number.")
    elif not _is_number(value):
        errors.append(f"{where}: 'value' must be a number (got {value!r}).")
    tag = obj.get("tag")
    if tag not in NUMBER_TAGS:
        errors.append(f"{where}: 'tag' must be measured or estimate (got {tag!r}).")
    elif tag == "measured":
        url = obj.get("url")
        ids = obj.get("record_ids")
        has_url = isinstance(url, str) and url.strip() != ""
        has_ids = isinstance(ids, list) and len(ids) > 0
        if not (has_url or has_ids):
            errors.append(f"{where}: a measured number needs a 'url' or 'record_ids'.")
    else:
        reasoning = obj.get("reasoning")
        if not isinstance(reasoning, str) or not reasoning.strip():
            errors.append(f"{where}: an estimate needs 'reasoning'.")
    return errors


def check_price(obj, where: str) -> list:
    """A price item: what, price_text (exact), amount, currency (ISO), unit, url, seen_via page|search."""
    if not isinstance(obj, dict):
        return [f"{where}: must be a price object (see config/formats.md, Prices)."]
    errors = []
    for field in ("what", "price_text", "unit"):
        v = obj.get(field)
        if not isinstance(v, str) or not v.strip():
            errors.append(f"{where}: '{field}' is missing or empty.")
    amount = obj.get("amount")
    if not _is_number(amount) or amount < 0:
        errors.append(f"{where}: 'amount' must be a number that is 0 or more (got {amount!r}).")
    cur = obj.get("currency")
    if not isinstance(cur, str) or not _CURRENCY_RE.match(cur):
        errors.append(f"{where}: 'currency' must be a 3-letter ISO code like USD or INR (got {cur!r}).")
    url = obj.get("url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        errors.append(f"{where}: 'url' must start with http:// or https://.")
    seen = obj.get("seen_via")
    if seen not in SEEN_VIA:
        errors.append(f"{where}: 'seen_via' must be page or search (got {seen!r}).")
    return errors


# --------------------------------------------------------------------------- graveyard
_GRAVE_LINE_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) \| ([^|]+?) \| ([^|]+?) \| (.*)$")
_REVIVE_LINE_RE = re.compile(r"^\s+- new evidence\b")


def graveyard_path() -> Path:
    return funnel_root() / "graveyard.md"


def parse_graveyard() -> list:
    """Entries in file order. `status` is "revived" when an indented `- new evidence ...` line follows."""
    p = graveyard_path()
    if not p.exists():
        return []
    entries: list[dict] = []
    current = None
    for raw in read_text(p).splitlines():
        m = _GRAVE_LINE_RE.match(raw)
        if m:
            current = {
                "date": m.group(1),
                "stage": m.group(2).strip(),
                "item": m.group(3).strip(),
                "reason": m.group(4).strip(),
                "status": "dead",
                "revivals": [],
                "line": raw,
            }
            entries.append(current)
            continue
        if current is not None and _REVIVE_LINE_RE.match(raw):
            current["status"] = "revived"
            current["revivals"].append(raw.strip()[2:].strip())
            continue
        if not raw.startswith((" ", "\t")):
            # a blank line, a heading or plain prose ends the current entry
            current = None
    return entries


def _last_entries(kind: str | None = None, ignore_date: str | None = None) -> dict:
    """item -> its last graveyard entry in file order (lines dated `ignore_date` left out)."""
    last: dict = {}
    for e in parse_graveyard():
        if ignore_date is not None and e["date"] == ignore_date:
            continue
        if kind and not e["item"].startswith(kind + ":"):
            continue
        last[e["item"]] = e
    return last


def dead_entries(kind: str | None = None, ignore_date: str | None = None) -> dict:
    """item -> the kill line that keeps it dead. The last line of an item decides (rule 7): a revival note
    revives only the line it sits under, so a later kill line kills the item again. Lines dated
    `ignore_date` are left out of the decision (a run's own later kills must not change an earlier stage)."""
    return {item: e for item, e in _last_entries(kind, ignore_date).items() if e["status"] == "dead"}


def dead_items(kind: str | None = None) -> set:
    """Items still dead. `kind` ("room" or "pain") keeps only items with that prefix."""
    return set(dead_entries(kind))


def is_dead(item: str) -> bool:
    return item in dead_items()


def format_graveyard_line(date, stage, item: str, reason: str) -> str:
    stage_s = str(stage)
    if not stage_s.startswith("stage"):
        stage_s = f"stage {stage_s}"
    reason_s = normalize_ws(reason).replace("|", "/")
    return f"- {date} | {stage_s} | {item} | {reason_s}"


def append_graveyard(date, stage, item: str, reason: str) -> bool:
    """Append one kill line. Never duplicates: the same date, stage and item is written once.

    If that entry exists with a different reason, the reason is replaced in place
    (revival notes under it are kept). Returns True when the file changed.
    """
    line = format_graveyard_line(date, stage, item, reason)
    m = _GRAVE_LINE_RE.match(line)
    assert m, "internal: graveyard line does not match its own format"
    p = graveyard_path()
    if not p.exists():
        write_text(p, "# Graveyard\n\n" + line)
        return True
    text = read_text(p)
    lines = text.splitlines()
    for i, existing in enumerate(lines):
        em = _GRAVE_LINE_RE.match(existing)
        if not em:
            continue
        same = (em.group(1), em.group(2).strip(), em.group(3).strip()) == (m.group(1), m.group(2).strip(), m.group(3).strip())
        if same:
            if em.group(4).strip() == m.group(4).strip():
                return False
            lines[i] = line
            write_text(p, "\n".join(lines))
            return True
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(p, text + line)
    return True


def sync_graveyard(date, stage, scope, kills: dict) -> dict:
    """Make the lines dated `date` for `stage` say exactly what this run of the stage killed.

    `scope` holds every item the stage judged this time; `kills` maps the killed ones to their reason.
    A killed item gets its line added (or its reason fixed in place, revival notes kept). An item in
    `scope` that is not killed loses its line from an earlier rerun on the same date, so a kill the
    model has since fixed does not stay on record; a line the founder revived is kept. Lines of other
    dates, stages or items are never touched. A dry run writes nothing (its kills are not kills).
    Returns {"added", "updated", "removed"}.
    """
    out = {"added": 0, "updated": 0, "removed": 0}
    if is_dry_run():
        return out
    stage_s = str(stage)
    if not stage_s.startswith("stage"):
        stage_s = f"stage {stage_s}"
    date_s = str(date)
    scope_set = {str(i) for i in scope}
    wanted = {str(item): format_graveyard_line(date_s, stage_s, str(item), reason) for item, reason in kills.items()}
    p = graveyard_path()
    lines = read_text(p).splitlines() if p.exists() else ["# Graveyard", ""]
    kept: list = []
    seen: set = set()
    i = 0
    while i < len(lines):
        raw = lines[i]
        m = _GRAVE_LINE_RE.match(raw)
        if not m or m.group(1) != date_s or m.group(2).strip() != stage_s:
            kept.append(raw)
            i += 1
            continue
        item = m.group(3).strip()
        children: list = []
        j = i + 1
        while j < len(lines) and lines[j].startswith((" ", "\t")):
            children.append(lines[j])
            j += 1
        revived = any(_REVIVE_LINE_RE.match(c) for c in children)
        if item in wanted and item not in seen:
            if raw != wanted[item]:
                out["updated"] += 1
            kept.append(wanted[item])
            kept.extend(children)
            seen.add(item)
        elif item in wanted:
            out["removed"] += 1  # a second line for the same date, stage and item: never meant to exist
        elif item in scope_set and not revived:
            out["removed"] += 1
        else:
            kept.append(raw)
            kept.extend(children)
        i = j
    for item, line in wanted.items():
        if item not in seen:
            kept.append(line)
            out["added"] += 1
    if out["added"] or out["updated"] or out["removed"] or not p.exists():
        while kept and not kept[-1].strip():
            kept.pop()
        write_text(p, "\n".join(kept))
    return out


# --------------------------------------------------------------------------- events and secrets
def log_event(run, stage, command: str, kind: str, create_run: bool = True, **fields):
    """Append one event to RUN/runlog.jsonl. The only place a timestamp is written.

    With `create_run` False nothing is written (None is returned) when the run folder does not
    exist: commands that need no run folder must not leave an empty runs/<today>/ behind.
    """
    rd = run_dir(run)
    if not create_run and not rd.exists():
        return None
    rd.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
        "stage": stage,
        "command": command,
        "kind": kind,
    }
    event.update(fields)
    append_jsonl(rd / "runlog.jsonl", event)
    return event


def _read_dotenv() -> dict:
    p = funnel_root() / ".env"
    values: dict[str, str] = {}
    if not p.exists():
        return values
    for raw in read_text(p).splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        k, _, v = line.partition("=")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        values[k.strip()] = v
    return values


def get_key(name: str) -> str | None:
    """An API key by environment-variable name: the environment first, then .env. Never printed."""
    v = os.environ.get(name)
    if v is not None and v.strip():
        return v.strip()
    v = _read_dotenv().get(name)
    if v:
        return v
    return None


def set_dry_run(flag: bool) -> None:
    global _DRY_RUN
    _DRY_RUN = bool(flag)


def is_dry_run() -> bool:
    return _DRY_RUN or os.environ.get("FUNNEL_DRY_RUN") == "1"


# --------------------------------------------------------------------------- fx
def read_fx_file(run) -> dict:
    p = run_dir(run) / "fx_rates.json"
    require_file(p, "Write it (see config/formats.md, FX rates) and run `funnel fx`.")
    data = read_json(p)
    if not isinstance(data, dict) or not isinstance(data.get("rates"), dict):
        raise ValidationErrors([f"{rel(p)}: needs a 'rates' object keyed by currency code."])
    return data


def load_fx(run) -> dict:
    """{"USD": 1.0, "<code>": per_usd, ...}. A bad rate is a validation error."""
    data = read_fx_file(run)
    p = run_dir(run) / "fx_rates.json"
    fx = {"USD": 1.0}
    errors = []
    for code, entry in sorted(data["rates"].items()):
        if not isinstance(code, str) or not _CURRENCY_RE.match(code):
            errors.append(f"{rel(p)}: currency {code!r} must be a 3-letter ISO code.")
            continue
        per_usd = entry.get("per_usd") if isinstance(entry, dict) else entry
        if not _is_number(per_usd) or per_usd <= 0:
            errors.append(f"{rel(p)}: {code}.per_usd must be a positive number (got {per_usd!r}).")
            continue
        fx[code] = float(per_usd)
    if errors:
        raise ValidationErrors(errors)
    return fx


def to_usd(amount, currency: str, fx: dict) -> float:
    cur = (currency or "").upper()
    if cur == "USD":
        return float(amount)
    if cur not in fx:
        raise MissingCurrency(cur or "(empty)")
    return float(amount) / float(fx[cur])


def from_usd(amount_usd, currency: str, fx: dict) -> float:
    cur = (currency or "").upper()
    if cur == "USD":
        return float(amount_usd)
    if cur not in fx:
        raise MissingCurrency(cur or "(empty)")
    return float(amount_usd) * float(fx[cur])


def convert(amount, currency_from: str, currency_to: str, fx: dict) -> float:
    return from_usd(to_usd(amount, currency_from, fx), currency_to, fx)
