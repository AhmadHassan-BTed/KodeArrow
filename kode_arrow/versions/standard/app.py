import pystray
import webbrowser
import keyboard
import itertools
from PIL import Image
import os
from ...common.core.base_app import BaseApp
from ...common.config.settings import Config
from ...common.services.subscription_service import SubscriptionService
from ...common.gui.windows import UIWindowManager

class StandardApp(BaseApp):
    """Standard Edition of KodeArrow."""
    
    def __init__(self):
        super().__init__("Standard Edition")
        self.subscription = SubscriptionService()
        self.ui = UIWindowManager()
        self.resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets", "branding")
        self.icon_path = os.path.join(self.resource_dir, "icon.ico")

    def setup_hotkeys(self):
        keys = ['i', 'j', 'k', 'l']
        
        # Mapping functions
        actions = {
            'i': lambda: self.press_key('up') if self.is_premium else None,
            'j': lambda: self.press_key('left'),
            'k': lambda: self.press_key('down') if self.is_premium else None,
            'l': lambda: self.press_key('right')
        }

        def handle_combo(*k_list):
            for k in k_list:
                actions[k]()

        for r in range(1, 5):
            for combo in itertools.permutations(keys, r):
                keyboard.add_hotkey(f'alt+{"+".join(combo)}', handle_combo, args=combo, suppress=True)
        
        self.register_extended_hotkeys()
        self.logger.info("Hotkeys registered.")

    def setup_tray(self):
        img = Image.open(self.icon_path)
        
        def open_creator_links():
            self.open_portfolio()
            webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")

        menu = pystray.Menu(
            pystray.MenuItem('Created by Ahmad Hassan', open_creator_links),
            pystray.MenuItem('Visit KodeArrow', self.open_website, default=True),
            pystray.MenuItem('Exit', self.stop)
        )
        
        self.icon = pystray.Icon("KodeArrow", img, "KodeArrow", menu)

    def open_portfolio(self):
        webbrowser.open("https://bted.wuaze.com/")

    def open_website(self):
        webbrowser.open("https://kodearrow.wuaze.com/")

    def on_startup(self):
        self.logger.info("StandardApp specialized startup logic.")
        if not self.is_premium:
            self.ui.show_instructions(is_premium=False)
        else:
            self.ui.show_instructions(is_premium=True)
