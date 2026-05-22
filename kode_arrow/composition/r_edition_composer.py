from __future__ import annotations

import time

from .controllers import REditionHotkeyController
from .r_edition_builder import (
    REditionDeps,
    build_reedition_navigation_use_case,
    build_reedition_tray,
    reedition_icon_path,
    now_seconds,
)


class REditionComposer:
    def __init__(self, deps: REditionDeps):
        self._deps = deps

    def build_hotkeys_controller(
        self,
        *,
        is_premium: bool,
        batching,
        on_key_event,
    ) -> REditionHotkeyController:
        nav_use_case = build_reedition_navigation_use_case(
            is_premium=is_premium,
            keypress_port=self._deps.keypress,
        )
        return REditionHotkeyController(
            keyboard_port=self._deps.keyboard,
            navigation_use_case=nav_use_case,
            batching=batching,
            on_key_event=on_key_event,
        )

    def build_tray(
        self,
        *,
        is_premium: bool,
        hardware_id: str,
        premium_file_path: str,
        open_portfolio,
        open_website,
        open_portal,
        show_research_info,
        stop_app,
    ):
        return build_reedition_tray(
            icon_path=reedition_icon_path(),
            deps=self._deps,
            hardware_id=hardware_id,
            premium_file_path=premium_file_path,
            is_premium=is_premium,
            open_portfolio=open_portfolio,
            open_website=open_website,
            open_portal=open_portal,
            show_research_info=show_research_info,
            stop_app=stop_app,
        )

    def now(self) -> float:
        return now_seconds()

