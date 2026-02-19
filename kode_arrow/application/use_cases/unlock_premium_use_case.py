from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class UnlockResult:
    success: bool
    message: str


class UnlockPremiumUseCase:
    def __init__(self, *, premium_port, hardware_id: str, premium_file_path: str, is_research: bool):
        self._premium_port = premium_port
        self._hardware_id = hardware_id
        self._premium_file_path = premium_file_path
        self._is_research = is_research

    def execute(self, *, email: str) -> UnlockResult:
        ok, message = self._premium_port.validate_and_activate(
            email=email,
            hardware_id=self._hardware_id,
            premium_file_path=self._premium_file_path,
            is_research=self._is_research,
        )
        return UnlockResult(success=ok, message=message)

