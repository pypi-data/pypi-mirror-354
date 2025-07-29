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
list_engines = lambda: sorted(_engines)
all_engines = lambda: MappingProxyType(_engines)
