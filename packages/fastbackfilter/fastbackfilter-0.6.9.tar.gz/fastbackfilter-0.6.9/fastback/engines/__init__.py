# fastback/engines/__init__.py
"""
Auto-import every *.py module in this package so each engine registers itself.

New detector?  Just add a file:

    fastback/engines/gif.py
    --------------------------------
    from ..registry import register
    from .base import EngineBase
    @register
    class GIFEngine(EngineBase):
        name = "gif"
        …

It becomes available instantly.
"""
from importlib import import_module
from pathlib import Path

_pkg_dir = Path(__file__).resolve().parent

for _file in _pkg_dir.glob("*.py"):
    if _file.stem != "__init__":
        import_module(f"{__name__}.{_file.stem}")
