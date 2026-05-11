import pystray
import webbrowser
import keyboard
import itertools
import time
import os
from PIL import Image
from ...common.core.base_app import BaseApp
from ...common.config.settings import Config
from ...common.gui.windows import UIWindowManager
from ...common.services.subscription_service import SubscriptionService

class REditionApp(BaseApp):
    """Research Edition (R-Edition) of KodeArrow with telemetry."""
    
    def __init__(self):
        super().__init__("R-Edition")
        self.ui = UIWindowManager()
        self.subscription = SubscriptionService()
        self.stats = {
            "charactersTyped": 0,
            "kodeArrowHotkeys": 0,
            "TotalUsageMinutes": 0
        }
        self.multiplier = 20
        self.last_batch_time = time.time()
        self.resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets", "branding")
        self.icon_path = os.path.join(self.resource_dir, "icon.ico")

    def setup_hotkeys(self):
        keys = ['i', 'j', 'k', 'l']
        
        def track_and_press(k):
            self.stats["kodeArrowHotkeys"] += 1
            if k == 'up': self.press_key('up') if self.is_premium else None
            elif k == 'down': self.press_key('down') if self.is_premium else None
            elif k == 'left': self.press_key('left')
            elif k == 'right': self.press_key('right')

        actions = {
            'i': lambda: track_and_press('up'),
            'j': lambda: track_and_press('left'),
            'k': lambda: track_and_press('down'),
            'l': lambda: track_and_press('right')
        }

        def handle_combo(*k_list):
            for k in k_list:
                actions[k]()

        for r in range(1, 5):
            for combo in itertools.permutations(keys, r):
                keyboard.add_hotkey(f'alt+{"+".join(combo)}', handle_combo, args=combo, suppress=True)
        
        self.register_extended_hotkeys()
        # Track regular typing for research
        keyboard.on_press(self.on_key_press)
        self.logger.info("R-Edition Hotkeys and Telemetry registered.")

    def on_key_press(self, event):
        if event.event_type == 'down':
            self.stats["charactersTyped"] += 1
            if self.stats["charactersTyped"] >= self.multiplier:
                self.process_batch()

    def process_batch(self):
        """Processes and uploads a batch of research data."""
        current_time = time.time()
        interval_minutes = (current_time - self.last_batch_time) / 60
        self.stats["TotalUsageMinutes"] += interval_minutes
        
        self.logger.info(f"Batch limit reached ({self.multiplier}). Uploading telemetry...")
        
        # Upload to Firebase
        email = "research_user@example.com" # Placeholder, would be fetched from premium file
        self.firebase.upload_usage_data("ControlGroup", email, self.stats)
        
        # Reset batch counters
        self.stats["charactersTyped"] = 0
        self.stats["kodeArrowHotkeys"] = 0
        self.last_batch_time = current_time

    def setup_tray(self):
        img = Image.open(self.icon_path)
        
        def open_creator_links():
            webbrowser.open("https://bted.wuaze.com/")
            webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")

        menu = pystray.Menu(
            pystray.MenuItem('Created by Ahmad Hassan', open_creator_links),
            pystray.MenuItem('R-Edition Research Info', self.show_research_info),
            pystray.MenuItem('Visit Portal', self.open_portal, default=True),
            pystray.MenuItem('Exit', self.stop)
        )
        
        self.icon = pystray.Icon("KodeArrowR", img, "KodeArrow R-Edition", menu)

    def show_research_info(self):
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Research Stats", f"Characters: {self.stats['charactersTyped']}\nHotkeys: {self.stats['kodeArrowHotkeys']}")
        root.destroy()

    def open_portal(self):
        webbrowser.open("https://kodearrow.wuaze.com/research")

    def stop(self):
        # Upload data before exiting
        self.stats["TotalUsageMinutes"] = (time.time() - self.start_time) / 60
        self.logger.info("Uploading research data before shutdown...")
        # In a real scenario, we'd find the email from the premium file
        email = "research_user@example.com" 
        self.firebase.upload_usage_data("ControlGroup", email, self.stats)
        super().stop()
