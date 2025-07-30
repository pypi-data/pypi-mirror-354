from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class OctetEngine(EngineBase):
    name = "octet"
    cost = 0.0

    def sniff(self, payload: bytes) -> Result:
        return Result(
            candidates=[
                Candidate(
                    media_type="application/octet-stream",
                    confidence=0.0,
                )
            ]
        )
