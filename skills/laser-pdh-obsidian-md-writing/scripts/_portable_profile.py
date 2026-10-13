"""Resolve portable Laser/FPGA paths from the Codex profile."""

from __future__ import annotations

import json
import os
from pathlib import Path


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME", "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def load_profile() -> dict:
    path = codex_home() / "laser-fpga-profile.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def profile_path(key: str, fallback: Path) -> Path:
    value = load_profile().get(key)
    return Path(value).expanduser() if isinstance(value, str) and value.strip() else fallback
