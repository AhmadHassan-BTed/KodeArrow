from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

try:
    import pystray
    from pystray import Icon
except ImportError:  # pragma: no cover
    pystray = None
    Icon = object  # type: ignore

from PIL import Image


from kode_arrow.domain.ports.tray_port import TrayPort


@dataclass(frozen=True)
class TrayResources:
    icon_path: str


class TrayAdapter(TrayPort):
    def __init__(self, *, resources: TrayResources, on_open_creator_links: Optional[Callable[[], None]] = None):
        self._resources = resources
        self._icon: Optional[pystray.Icon] = None
        self._on_open_creator_links = on_open_creator_links

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
        img = Image.open(self._resources.icon_path)

        def open_creator_links():
            if self._on_open_creator_links:
                self._on_open_creator_links()
            else:
                on_open_portfolio()

        menu_items = [
            pystray.MenuItem('Created by Ahmad Hassan', open_creator_links),
            pystray.MenuItem('Visit KodeArrow', on_open_website, default=True),
        ]

        if on_show_research_info is not None:
            menu_items.insert(1, pystray.MenuItem('R-Edition Research Info', on_show_research_info))

        if not is_premium and on_unlock is not None:
            menu_items.append(pystray.MenuItem('Already bought? Unlock Here', on_unlock))

        # If caller passed portal handler, always include it (resembles existing behavior)
        menu_items.insert(
            len(menu_items),
            pystray.MenuItem('Visit Portal', on_open_portal) if on_open_portal else pystray.MenuItem('Visit Portal', lambda: None),
        )

        menu_items.append(pystray.MenuItem('Exit', on_exit))

        self._icon = pystray.Icon('KodeArrow', img, 'KodeArrow', pystray.Menu(*menu_items))

    def run(self) -> None:
        if self._icon:
            self._icon.run()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()

