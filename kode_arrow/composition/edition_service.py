from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EditionUIActions:
    open_portfolio: callable  # type: ignore[valid-type]


class AppEdition(Protocol):
    def start(self) -> None:
        ...

