from __future__ import annotations

from typing import Callable, Iterable, Protocol


class KeyboardPort(Protocol):
    """Adapter-facing keyboard integration port."""

    def add_hotkey(
        self,
        hotkey: str,
        callback: Callable[[], None],
        *,
        suppress: bool = True,
    ) -> None:
        ...

    def on_press(self, callback: Callable[[object], None]) -> None:
        """Register OS-level key-press listener (used for telemetry)."""
        ...

