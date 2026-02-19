from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationAction:
    key_to_press: str
    requires_premium: bool


class NavigationActionUseCase:
    """Domain/application use-case: decide whether and what key to press."""

    def __init__(self, *, is_premium: bool, keypress_port):
        self._is_premium = is_premium
        self._keypress = keypress_port

    def execute(self, action: NavigationAction) -> None:
        if action.requires_premium and not self._is_premium:
            return
        self._keypress.press(action.key_to_press)

