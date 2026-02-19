from __future__ import annotations

from typing import Callable

import keyboard as _keyboard

from kode_arrow.domain.ports.keyboard_port import KeyboardPort


class KeyboardAdapter(KeyboardPort):
    def add_hotkey(
        self,
        hotkey: str,
        callback: Callable[[], None],
        *,
        suppress: bool = True,
    ) -> None:
        _keyboard.add_hotkey(hotkey, callback, suppress=suppress)

    def on_press(self, callback: Callable[[object], None]) -> None:
        _keyboard.on_press(callback)

