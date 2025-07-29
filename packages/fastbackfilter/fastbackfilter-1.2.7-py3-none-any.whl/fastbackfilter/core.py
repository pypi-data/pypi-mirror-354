from __future__ import annotations
import concurrent.futures as cf
import logging
import os
from pathlib import Path
from typing import Any, Iterable, Sequence
from .cache import get as cache_get, put as cache_put
from .exceptions import FastbackError
from .registry import get, list_engines
from .types import Result, Candidate
logger = logging.getLogger(__name__)
def _load_bytes(source: str | Path | bytes, cap: int | None) -> bytes:
    """Return raw bytes, never a Result (guards against cache mix-ups)."""
    if isinstance(source, (str, Path)):
        p = Path(source)
        cached = cache_get(p)
        if isinstance(cached, (bytes, bytearray)):
            return cached[:cap] if cap else bytes(cached)
        data = p.read_bytes() if cap is None else p.read_bytes()[:cap]
        return data
    return source[:cap] if cap else source
def detect(
    source: str | Path | bytes,
    engine: str = "auto",
    *,
    cap_bytes: int | None = 4096,
    engine_order: Iterable[str] | None = None,
    cache: bool = True,
) -> Result:
    payload = _load_bytes(source, cap_bytes)
    if engine != "auto":
        return get(engine)()(payload)
    engines: Sequence[str] = engine_order or list_engines()
    best: Result | None = None
    for name in engines:
        res = get(name)()(payload)
        if res.candidates:
            if best is None or res.candidates[0].confidence > best.candidates[0].confidence:
                best = res
                if res.candidates[0].confidence >= 0.99:
                    break
    if best is None and cap_bytes is not None and isinstance(source, (str, Path)):
        payload = Path(source).read_bytes()
        for name in engines:
            res = get(name)()(payload)
            if res.candidates:
                best = res
                break
    if best is None:
        best = Result(
            candidates=[Candidate(media_type="application/octet-stream", confidence=0.0)]
        )
    if cache and isinstance(source, (str, Path)):
        cache_put(Path(source), best)
    return best
try:
    import anyio as _anyio
    async def detect_async(source: Any, **kw) -> Result:
        return await _anyio.to_thread.run_sync(detect, source, **kw)
except ImportError:
    pass
def scan_dir(
    root: str | Path,
    *,
    pattern: str = "**/*",
    workers: int = os.cpu_count() or 4,
    **kw,
):
    root = Path(root)
    paths = [p for p in root.glob(pattern) if p.is_file()]
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(detect, p, **kw): p for p in paths}
        for fut in cf.as_completed(futs):
            yield futs[fut], fut.result()
