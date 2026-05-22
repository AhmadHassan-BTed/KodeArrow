from __future__ import annotations

import webbrowser

from ...common.core.base_app import BaseApp
from ...composition.standard_composer import StandardComposer
from ...composition.standard_builder import build_standard_app_deps


class StandardApp(BaseApp):
    """Standard Edition of KodeArrow."""

    def __init__(self):
        super().__init__("Standard Edition")

        self._composer = StandardComposer(
            deps=build_standard_app_deps(premium_file_provider=lambda: self.premium_file)
        )

    def setup_hotkeys(self):
        controller = self._composer.build_hotkeys_controller(is_premium=self.is_premium)
        controller.register()
        self.register_extended_hotkeys()
        self.logger.info("Hotkeys registered.")

    def setup_tray(self):
        tray = self._composer.build_tray(
            is_premium=self.is_premium,
            hardware_id=self.hardware_id,
            premium_file_path=self.premium_file,
            open_portfolio=self.open_portfolio,
            open_website=self.open_website,
            stop_app=self.stop,
        )
        self.icon = tray._icon  # keep compatibility with BaseApp.run_tray

    def open_portfolio(self):
        webbrowser.open("https://bted.wuaze.com/")

    def open_website(self):
        webbrowser.open("https://kodearrow.wuaze.com/")

    def on_startup(self):
        self.logger.info("StandardApp specialized startup logic.")
        self._composer.on_startup_ui(is_premium=self.is_premium)


