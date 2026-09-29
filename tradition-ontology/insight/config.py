"""Paths and settings. Everything configurable lives in config/ and rules/; secrets come from the environment only."""
import json
import os
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # tradition-ontology/
CONFIG = ROOT / "config"
RULES = ROOT / "rules"
LAYERS = ROOT / "layers"
DATA = ROOT / "data"


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Minimal .env reader (KEY=VALUE lines). Never overrides variables already set; .env is git-ignored."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@lru_cache(maxsize=None)
def json_file(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def routing() -> dict:
    return json_file("config/model_routing.json")


def pricing() -> dict:
    return json_file("config/pricing.json")


def data_dir() -> Path:
    """Where personal data lives (SQLite). Outside the repo by default, so it can never be committed."""
    d = Path(os.environ.get("ONTO_DATA_DIR", Path.home() / ".onto-insight"))
    d.mkdir(parents=True, exist_ok=True)
    try:
        d.chmod(0o700)
    except OSError:
        pass
    return d


def retention_days() -> int:
    return int(os.environ.get("ONTO_RETENTION_DAYS", "90"))


def engine_mode() -> str:
    """'model' (Claude API, needs a key), 'rules' (deterministic, offline) or 'auto' (model if a key is set, else rules)."""
    m = os.environ.get("ONTO_ENGINE", "auto").lower()
    if m == "auto":
        return "model" if os.environ.get(routing()["api_key_env"]) else "rules"
    return m
