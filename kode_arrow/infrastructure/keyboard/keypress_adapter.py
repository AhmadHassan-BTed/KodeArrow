from __future__ import annotations

from kode_arrow.domain.ports.keypress_port import KeypressPort


class KeypressAdapter(KeypressPort):
    def press(self, key: str) -> None:
        import pyautogui

        pyautogui.press(key)

