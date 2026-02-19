from __future__ import annotations

from typing import Protocol, Callable, Optional


class TrayPort(Protocol):
    def run(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def build_menu(
        self,
        *,
        is_premium: bool,
        on_unlock: Optional[Callable[[], None]],
        on_exit: Callable[[], None],
        on_open_portfolio: Callable[[], None],
        on_open_website: Callable[[], None],
        on_show_research_info: Optional[Callable[[], None]],
        on_open_portal: Callable[[], None],
    ) -> None:
        ...


