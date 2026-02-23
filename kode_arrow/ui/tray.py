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
        is_premium: bool,
        on_unlock: Optional[Callable[[], None]],
        on_exit: Callable[Any, None],
        on_open_portfolio: Callable[[], None],
        on_open_website: Callable[[], None],
    ) -> None:
        img = Image.open(self._icon_path).resize((16, 16))

        menu_items = [
            pystray.MenuItem('Created by Ahmad Hassan', on_open_portfolio),
        ]

        if is_premium:
            menu_items.append(pystray.MenuItem('Visit KodeArrow', on_open_website, default=True))
        else:
            menu_items.append(pystray.MenuItem('Buy here for $2', on_open_website, default=True))
            if on_unlock is not None:
                # pystray wraps callback in lambda (icon, item): ... 
                # We need to adapt it since on_unlock takes no args.
                def wrap_unlock(icon, item):
                    on_unlock()
                menu_items.append(pystray.MenuItem('Already bought? Unlock Here', wrap_unlock))

        def wrap_exit(icon, item):
            on_exit()
            
        menu_items.append(pystray.MenuItem('Exit', wrap_exit))

        self._icon = pystray.Icon("KodeArrow by Ahmad Hassan", img, "KodeArrow by Ahmad Hassan", pystray.Menu(*menu_items))

    def run(self) -> None:
        if self._icon is not None:
            self._icon.run()

    def stop(self) -> None:
        if self._icon is not None:
            self._icon.stop()
