from __future__ import annotations

from typing import Callable, Protocol, Optional


class DialogPort(Protocol):
    def show_email_input_dialog(self, on_submit_callback: Callable[[str], None]) -> None:
        ...

    def show_message(self, title: str, message: str) -> None:
        ...

    def show_error(self, title: str, message: str) -> None:
        ...

