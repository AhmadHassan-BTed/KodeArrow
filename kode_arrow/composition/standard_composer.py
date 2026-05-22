from __future__ import annotations

from dataclasses import dataclass

from kode_arrow.common.gui.windows import UIWindowManager

from .controllers import StandardHotkeyController
from .standard_builder import (
    StandardEditionDeps,
    build_standard_navigation_use_case,
    build_standard_tray,
    standard_icon_path,
)



@dataclass(frozen=True)
class StandardComposer:
    deps: StandardEditionDeps

    def build_hotkeys_controller(self, *, is_premium: bool) -> StandardHotkeyController:
        nav_use_case = build_standard_navigation_use_case(
            is_premium=is_premium,
            keypress_port=self.deps.keypress,
        )
        return StandardHotkeyController(keyboard_port=self.deps.keyboard, navigation_use_case=nav_use_case)

    def build_tray(
        self,
        *,
        is_premium: bool,
        hardware_id: str,
        premium_file_path: str,
        open_portfolio,
        open_website,
        stop_app,
    ):
        return build_standard_tray(
            icon_path=standard_icon_path(),
            deps=self.deps,
            hardware_id=hardware_id,
            premium_file_path=premium_file_path,
            is_premium=is_premium,
            open_portfolio=open_portfolio,
            open_website=open_website,
            stop_app=stop_app,
        )

    def on_startup_ui(self, *, is_premium: bool) -> None:
        ui = UIWindowManager()
        ui.show_instructions(is_premium=is_premium)

