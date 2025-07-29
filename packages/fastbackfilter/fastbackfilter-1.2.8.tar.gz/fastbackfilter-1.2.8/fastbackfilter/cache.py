from __future__ import annotations
import json, os, sqlite3, time
from pathlib import Path
from typing import Optional
from platformdirs import user_cache_dir
from cachetools import LRUCache
from .types import Result
_CACHE_DIR = Path(user_cache_dir("fastback"))
_CACHE_DIR.mkdir(parents=True, exist_ok=True)
_DB = _CACHE_DIR / "results.sqlite3"
try:
    _con = sqlite3.connect(_DB)
    _con.execute("CREATE TABLE IF NOT EXISTS r (p TEXT PRIMARY KEY, t REAL, j TEXT)")
except Exception:
    _con = None
_mem = LRUCache(maxsize=1024)
_DEF_TTL = 86400
def get(path: Path) -> Optional[Result]:
    key = str(path.resolve())
    if key in _mem:
        return Result.model_validate_json(_mem[key])
    if _con:
        row = _con.execute("SELECT t,j FROM r WHERE p=?", (key,)).fetchone()
        if row and (time.time() - row[0] < _DEF_TTL):
            _mem[key] = row[1]
            return Result.model_validate_json(row[1])
    return None
def put(path: Path, res: Result):
    raw = res.model_dump_json()
    key = str(path.resolve())
    _mem[key] = raw
    if _con:
        _con.execute("REPLACE INTO r VALUES(?,?,?)", (key, time.time(), raw))
        _con.commit()
