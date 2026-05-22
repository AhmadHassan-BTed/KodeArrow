from __future__ import annotations

from typing import Protocol


class KeypressPort(Protocol):
    def press(self, key: str) -> None:
        ...

