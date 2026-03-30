from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .paths import WORKSPACE_ROOT


MILESTONE_LOCK_PATH = WORKSPACE_ROOT / "milestone.lock.json"


@lru_cache(maxsize=1)
def load_milestone_lock(path: str | Path = MILESTONE_LOCK_PATH) -> dict[str, Any]:
    resolved = Path(path).expanduser().resolve()
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"里程碑锁文件必须是 JSON object: {resolved}")
    return payload


def milestone_id() -> str:
    return str(load_milestone_lock().get("milestone_id", "unknown_milestone"))


def schema_version() -> int:
    return int(load_milestone_lock().get("schema_version", 0))


def capability_level() -> str:
    return str(load_milestone_lock().get("capability_level", "unknown_capability"))

