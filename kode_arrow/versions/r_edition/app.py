from __future__ import annotations

import itertools
import os
import time
import webbrowser

from ...common.core.base_app import BaseApp
from ...infrastructure.gui.dialog_adapter import DialogAdapter
from ...infrastructure.gui.tray_adapter import TrayAdapter, TrayResources
from ...infrastructure.keyboard.keyboard_adapter import KeyboardAdapter
from ...infrastructure.keyboard.keypress_adapter import KeypressAdapter
from ...infrastructure.services.firebase_telemetry_adapter import FirebaseTelemetryAdapter
from ...infrastructure.services.subscription_premium_adapter import SubscriptionPremiumAdapter

from ...application.use_cases.navigation_action_use_case import NavigationAction, NavigationActionUseCase
from ...application.use_cases.telemetry.research_batching_service import ResearchBatchingService
from ...application.use_cases.telemetry.usage_collector import UsageCollector
from ...application.use_cases.telemetry.upload_usage_use_case import UploadUsageUseCase
from ...application.use_cases.unlock_premium_use_case import UnlockPremiumUseCase


class REditionApp(BaseApp):
    """Research Edition (R-Edition) of KodeArrow with telemetry."""

    def __init__(self):
        super().__init__("R-Edition")

        self._keyboard = KeyboardAdapter()
        self._keypress = KeypressAdapter()
        self._dialog = DialogAdapter()

        self._premium_port = SubscriptionPremiumAdapter(premium_file_provider=lambda: self.premium_file)
        self._telemetry = FirebaseTelemetryAdapter()

        self.multiplier = 20
        self._collector = UsageCollector(multiplier=self.multiplier)
        self._uploader = UploadUsageUseCase(
            telemetry_port=self._telemetry,
            collection="ControlGroup",
            email="research_user@example.com",
        )
        self._batching = ResearchBatchingService(collector=self._collector, uploader=self._uploader)

        self.resource_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "assets",
            "branding",
        )
        self.icon_path = os.path.join(self.resource_dir, "icon.ico")
        self._start_time = time.time()

    def setup_hotkeys(self):
        keys = ['i', 'j', 'k', 'l']

        navigation = NavigationActionUseCase(is_premium=self.is_premium, keypress_port=self._keypress)

        def track_and_execute(k: str) -> None:
            self._batching.record_hotkey()
            if k == 'up':
                navigation.execute(NavigationAction(key_to_press='up', requires_premium=True))
            elif k == 'down':
                navigation.execute(NavigationAction(key_to_press='down', requires_premium=True))
            elif k == 'left':
                navigation.execute(NavigationAction(key_to_press='left', requires_premium=False))
            elif k == 'right':
                navigation.execute(NavigationAction(key_to_press='right', requires_premium=False))

        actions = {
            'i': lambda: track_and_execute('up'),
            'j': lambda: track_and_execute('left'),
            'k': lambda: track_and_execute('down'),
            'l': lambda: track_and_execute('right'),
        }

        def handle_combo(*k_list):
            for k in k_list:
                actions[k]()

        for r in range(1, 5):
            for combo in itertools.permutations(keys, r):
                hotkey = f"alt+{'+' .join(combo)}".replace(" +", "+")
                self._keyboard.add_hotkey(
                    hotkey,
                    lambda combo=combo: handle_combo(*combo),
                    suppress=True,
                )

        self.register_extended_hotkeys()
        self._keyboard.on_press(self.on_key_press)
        self.logger.info("R-Edition Hotkeys and Telemetry registered.")

    def on_key_press(self, event):
        if getattr(event, 'event_type', None) == 'down':
            self._batching.record_character_and_maybe_upload()

    def setup_tray(self):
        def open_creator_links():
            webbrowser.open("https://bted.wuaze.com/")
            webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")

        tray = TrayAdapter(
            resources=TrayResources(icon_path=self.icon_path),
            on_open_creator_links=open_creator_links,
        )

        def on_exit():
            self.stop()

        def on_open_portfolio():
            self.open_portfolio()

        def on_open_website():
            self.open_port_website()

        def on_open_portal():
            self.open_portal()

        def on_show_research_info():
            self.show_research_info()

        def on_unlock():
            def on_email_submit(email: str):
                use_case = UnlockPremiumUseCase(
                    premium_port=self._premium_port,
                    hardware_id=self.hardware_id,
                    premium_file_path=self.premium_file,
                    is_research=True,
                )
                result = use_case.execute(email=email)
                if result.success:
                    self._dialog.show_message(
                        "Success",
                        "Premium access unlocked! Please restart the application to apply changes.",
                    )
                else:
                    self._dialog.show_error("Unlock Failed", f"Error: {result.message}")

            self._dialog.show_email_input_dialog(on_email_submit)

        tray.build_menu(
            is_premium=self.is_premium,
            on_unlock=on_unlock if not self.is_premium else None,
            on_exit=on_exit,
            on_open_portfolio=on_open_portfolio,
            on_open_website=on_open_website,
            on_show_research_info=on_show_research_info,
            on_open_portal=on_open_portal,
        )

        self.icon = tray._icon

    def show_research_info(self):
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        stats = self._collector.stats
        messagebox.showinfo(
            "Research Stats",
            f"Characters: {stats['charactersTyped']}\nHotkeys: {stats['kodeArrowHotkeys']}",
        )
        root.destroy()

    def open_portfolio(self):
        webbrowser.open("https://bted.wuaze.com/")
        webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")

    def open_port_website(self):
        webbrowser.open("https://kodearrow.wuaze.com/")

    def open_portal(self):
        webbrowser.open("https://kodearrow.wuaze.com/research")

    def stop(self):
        final = dict(self._collector.stats)
        final["TotalUsageMinutes"] = (time.time() - self._start_time) / 60
        self.logger.info("Uploading research data before shutdown...")
        self._uploader.execute(data=final)
        super().stop()

