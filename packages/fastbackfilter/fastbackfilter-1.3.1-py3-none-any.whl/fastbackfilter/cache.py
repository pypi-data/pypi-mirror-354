# fastbackfilter/cache.py  – thread-safe SQLite + small in-mem LRU
from __future__ import annotations
import json, os, sqlite3, time
from pathlib import Path
from typing import Optional

from platformdirs import user_cache_dir
from cachetools import LRUCache

from .types import Result

# --------------------------------------------------------------------------- #
# persistent location
# --------------------------------------------------------------------------- #
_CACHE_DIR = Path(user_cache_dir("fastbackfilter"))
_CACHE_DIR.mkdir(parents=True, exist_ok=True)
_DB = _CACHE_DIR / "results.sqlite3"

# create table once (main thread)
with sqlite3.connect(_DB) as _con:
    _con.execute(
        "CREATE TABLE IF NOT EXISTS r "
        "(p TEXT PRIMARY KEY, t REAL, j TEXT)"
    )
    _con.commit()

# small in-memory LRU for hot paths
_mem: LRUCache[str, str] = LRUCache(maxsize=1024)
_DEF_TTL = 24 * 3600  # seconds


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _now() -> float:
    return time.time()


def _serialize(res: Result) -> str:
    return res.model_dump_json()


def _deserialize(raw: str) -> Result:
    return Result.model_validate_json(raw)


# --------------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------------- #
def get(path: Path) -> Optional[Result]:
    key = str(path.resolve())

    # L1: in-mem
    if key in _mem:
        return _deserialize(_mem[key])

    # L2: sqlite
    with sqlite3.connect(_DB) as con:
        row = con.execute(
            "SELECT t, j FROM r WHERE p = ?", (key,)
        ).fetchone()
        if not row:
            return None
        ts, raw = row
        if _now() - ts > _DEF_TTL:
            return None

    _mem[key] = raw
    return _deserialize(raw)


def put(path: Path, result: Result) -> None:
    key = str(path.resolve())
    raw = _serialize(result)
    _mem[key] = raw

    with sqlite3.connect(_DB) as con:
        con.execute(
            "INSERT OR REPLACE INTO r (p, t, j) VALUES (?,?,?)",
            (key, _now(), raw),
        )
        con.commit()
