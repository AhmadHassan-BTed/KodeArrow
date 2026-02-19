from __future__ import annotations

from typing import Protocol, Tuple


class PremiumPort(Protocol):
    def is_premium(self) -> bool:
        ...

    def validate_and_activate(self, *, email: str, hardware_id: str, premium_file_path: str, is_research: bool) -> Tuple[bool, str]:
        ...

