from __future__ import annotations

from typing import NamedTuple


class User(NamedTuple):
    id: int
    username: str
    password_hash: str | None = None
