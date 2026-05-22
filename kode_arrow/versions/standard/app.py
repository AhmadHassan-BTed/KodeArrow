from __future__ import annotations

import itertools
import os
import webbrowser
from PIL import Image

import keyboard

from ...common.core.base_app import BaseApp
from ...infrastructure.gui.tray_adapter import TrayAdapter, TrayResources
from ...infrastructure.keyboard.keyboard_adapter import KeyboardAdapter
from ...infrastructure.keyboard.keypress_adapter import KeypressAdapter
from ...infrastructure.services.subscription_premium_adapter import SubscriptionPremiumAdapter
from ...infrastructure.services.firebase_telemetry_adapter import FirebaseTelemetryAdapter
from ...infrastructure.gui.dialog_adapter import DialogAdapter
from ...application.use_cases.navigation_action_use_case import NavigationAction, NavigationActionUseCase
from ...application.use_cases.unlock_premium_use_case import UnlockPremiumUseCase


class StandardApp(BaseApp):
    """Standard Edition of KodeArrow."""

    def __init__(self):
        super().__init__("Standard Edition")

        self._keyboard = KeyboardAdapter()
        self._keypress = KeypressAdapter()
        self._dialog = DialogAdapter()
        self._premium_port = SubscriptionPremiumAdapter(premium_file_provider=lambda: self.premium_file)
        self._telemetry = FirebaseTelemetryAdapter()

        self.resource_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "assets",
            "branding",
        )
        self.icon_path = os.path.join(self.resource_dir, "icon.ico")

    def setup_hotkeys(self):
        # Create navigation handler (premium-gated rule lives in use-case input flags)
        navigation = NavigationActionUseCase(is_premium=self.is_premium, keypress_port=self._keypress)

        actions = {
            'i': NavigationAction(key_to_press='up', requires_premium=True),
            'j': NavigationAction(key_to_press='left', requires_premium=False),
            'k': NavigationAction(key_to_press='down', requires_premium=True),
            'l': NavigationAction(key_to_press='right', requires_premium=False),
        }

        def handle_combo(*k_list):
            for k in k_list:
                navigation.execute(actions[k])

        keys = ['i', 'j', 'k', 'l']
        for r in range(1, 5):
            for combo in itertools.permutations(keys, r):
                hotkey = f"alt+{'+' .join(combo)}".replace(" +", "+")
                self._keyboard.add_hotkey(
                    hotkey,
                    lambda combo=combo: handle_combo(*combo),
                    suppress=True,
                )


        self.register_extended_hotkeys()
        self.logger.info("Hotkeys registered.")

    def setup_tray(self):
        tray = TrayAdapter(
            resources=TrayResources(icon_path=self.icon_path),
            on_open_creator_links=self.open_portfolio,
        )

        def on_exit():
            self.stop()

        def on_open_portfolio():
            self.open_portfolio()

        def on_open_website():
            self.open_website()

        def on_unlock():
            def on_email_submit(email: str):
                use_case = UnlockPremiumUseCase(
                    premium_port=self._premium_port,
                    hardware_id=self.hardware_id,
                    premium_file_path=self.premium_file,
                    is_research=False,
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
            on_show_research_info=None,
            on_open_portal=self.open_website,
        )
        self.icon = tray._icon  # keep compatibility with BaseApp.run_tray

    def open_portfolio(self):
        webbrowser.open("https://bted.wuaze.com/")

    def open_website(self):
        webbrowser.open("https://kodearrow.wuaze.com/")

    def on_startup(self):
        self.logger.info("StandardApp specialized startup logic.")
        # Use existing UI helper directly for now (presentation stays as adapter)
        from ...common.gui.windows import UIWindowManager

        ui = UIWindowManager()
        if not self.is_premium:
            ui.show_instructions(is_premium=False)
        else:
            ui.show_instructions(is_premium=True)

