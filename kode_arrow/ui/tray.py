from typing import Any, Callable, Optional
from PIL import Image

try:
    import pystray
except ImportError:
    pystray = None

class SystemTray:
    """Manages the system tray icon."""

    def __init__(self, icon_path: str, on_open_creator_links: Optional[Callable[[], None]] = None):
        self._icon_path = icon_path
        self._icon: Optional[Any] = None
        self._on_open_creator_links = on_open_creator_links

    def build_menu(
        self,
        *,
        is_premium: bool,
        on_unlock: Optional[Callable[[], None]],
        on_exit: Callable[[], None],
        on_open_portfolio: Callable[[], None],
        on_open_website: Callable[[], None],
        on_show_research_info: Optional[Callable[[], None]] = None,
        on_open_portal: Optional[Callable[[], None]] = None,
    ) -> None:
        img = Image.open(self._icon_path)

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

        if on_open_portal:
            menu_items.append(pystray.MenuItem('Visit Portal', on_open_portal))
            
        menu_items.append(pystray.MenuItem('Exit', on_exit))

        self._icon = pystray.Icon('KodeArrow', img, 'KodeArrow', pystray.Menu(*menu_items))

    def run(self) -> None:
        if self._icon is not None:
            self._icon.run()

    def stop(self) -> None:
        if self._icon is not None:
            self._icon.stop()
