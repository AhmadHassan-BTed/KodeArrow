from typing import Any, Callable, Optional
from PIL import Image

try:
    import pystray
except ImportError:
    pystray = None

class SystemTray:
    def __init__(self, icon_path: str, on_open_creator_links: Optional[Callable[[], None]] = None):
        self._icon_path = icon_path
        self._icon: Optional[Any] = None
        self._on_open_creator_links = on_open_creator_links

    def build_menu(
        self,
        *,
        is_premium_fn: Callable[[], bool],
        on_open_dashboard: Callable[[], None],
        on_unlock: Callable[[], None],
        on_exit: Callable[Any, None],
        on_open_portfolio: Callable[[], None],
        on_open_website: Callable[[], None],
    ) -> None:
        img = Image.open(self._icon_path).resize((16, 16))

        def create_menu_items():
            menu_items = [
                pystray.MenuItem('Open Dashboard', on_open_dashboard, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem('Created by Ahmad Hassan', on_open_portfolio),
            ]

            if is_premium_fn():
                menu_items.append(pystray.MenuItem('Visit KodeArrow', on_open_website))
            else:
                menu_items.append(pystray.MenuItem('Buy here for $2', on_open_website))
                if on_unlock is not None:
                    def wrap_unlock(icon, item):
                        on_unlock()
                    menu_items.append(pystray.MenuItem('Already bought? Unlock Here', wrap_unlock))

            def wrap_exit(icon, item):
                on_exit()
                
            menu_items.append(pystray.MenuItem('Exit', wrap_exit))
            return menu_items

        self._icon = pystray.Icon("KodeArrow by Ahmad Hassan", img, "KodeArrow by Ahmad Hassan", pystray.Menu(create_menu_items))

    def run(self) -> None:
        if self._icon is not None:
            self._icon.run()

    def stop(self) -> None:
        if self._icon is not None:
            self._icon.stop()
