from __future__ import annotations
from types import MappingProxyType
from .exceptions import UnsupportedType

_engines: dict[str, type] = {}
def register(cls):
    _engines[cls.name] = cls
    return cls
def get(name: str):
    try:
        return _engines[name]
    except KeyError as exc:
        raise UnsupportedType(name) from exc
def list_engines() -> list[str]:
    """Return engine names ordered by ``cost`` attribute."""
    return [
        name
        for name, cls in sorted(
            _engines.items(), key=lambda kv: getattr(kv[1], "cost", 1.0)
        )
    ]
all_engines = lambda: MappingProxyType(_engines)
