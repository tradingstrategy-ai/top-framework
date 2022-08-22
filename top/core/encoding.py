"""JSON encoding for special types."""

import datetime
from typing import Optional


def encode_date(d: datetime.datetime) -> Optional[str]:
    if d:
        assert d.tzinfo is not None, f"Expected timezone aware date, got {d}"
        return d.isoformat()
    return None


def decode_date(s: str) -> Optional[datetime.datetime]:
    if s:
        return datetime.datetime.fromisoformat(s)
    return None
