from __future__ import annotations

from typing import Callable, Tuple

from kode_arrow.domain.ports.premium_port import PremiumPort
from .subscription import SubscriptionService


class SubscriptionPremiumAdapter(PremiumPort):
    def __init__(self, *, premium_file_provider: Callable[[], str]):
        self._subscription = SubscriptionService()
        self._premium_file_provider = premium_file_provider


    def is_premium(self) -> bool:
        path = self._premium_file_provider()
        import os

        return os.path.exists(path)

    def validate_and_activate(
        self,
        *,
        email: str,
        hardware_id: str,
        premium_file_path: str,
        is_research: bool,
    ) -> Tuple[bool, str]:
        return self._subscription.validate_and_activate(
            email,
            hardware_id,
            premium_file_path,
            is_research=is_research,
        )

