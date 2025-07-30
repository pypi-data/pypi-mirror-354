from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class XMLEngine(EngineBase):
    name = "xml"
    _MAGIC = b"<?xml"
    def sniff(self, payload: bytes) -> Result:
        window = payload[:1 << 20]
        idx = window.find(self._MAGIC)
        cand = []
        if idx != -1:
            conf = 1.0 if idx == 0 else 0.90 - min(idx / (1 << 20), 0.1)
            cand.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=conf,
                )
            )
        return Result(candidates=cand)
