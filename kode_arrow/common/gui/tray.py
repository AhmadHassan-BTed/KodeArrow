import pystray
import webbrowser
import sys

def create_menu(icon, is_premium_callback, open_url_callback, open_url_buy_callback, unlock_callback, exit_callback):
    menu = [
        pystray.MenuItem('Created by Ahmad Hassan', open_url_callback),
    ]

    if is_premium_callback():
        menu.append(pystray.MenuItem('Visit KodeArrow', open_url_buy_callback, default=True))
    else:
        menu.append(pystray.MenuItem('Buy here for $2', open_url_buy_callback, default=True))
        menu.append(pystray.MenuItem('Already bought? Unlock Here', unlock_callback))
    
    menu.append(pystray.MenuItem('Exit', lambda icon, item: exit_callback()))
    
    icon.menu = pystray.Menu(*menu)
    return icon
