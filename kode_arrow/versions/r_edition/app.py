from __future__ import annotations

import webbrowser

from ...common.core.base_app import BaseApp
from ...composition.r_edition_builder import build_reedition_app_deps
from ...composition.r_edition_composer import REditionComposer


class REditionApp(BaseApp):
    """Research Edition (R-Edition) of KodeArrow with telemetry."""

    def __init__(self):
        super().__init__("R-Edition")

        self._deps = build_reedition_app_deps(
            premium_file_provider=lambda: self.premium_file,
        )
        self._collector = self._deps.collector
        self._batching = self._deps.batching

        self._composer = REditionComposer(self._deps)
        self._hotkeys_controller = self._composer.build_hotkeys_controller(
            is_premium=self.is_premium,
            batching=self._batching,
            on_key_event=self._on_keyboard_event,
        )

        # initialize tray once we have premium-file path & is_premium
        self._tray = self._composer.build_tray(
            is_premium=self.is_premium,
            hardware_id=self.hardware_id,
            premium_file_path=self.premium_file,
            open_portfolio=self.open_portfolio,
            open_website=self.open_port_website,
            open_portal=self.open_portal,
            show_research_info=self.show_research_info,
            stop_app=self.stop,
        )

        self._tray_icon = None

    def _on_keyboard_event(self, event: object) -> None:
        # Research edition counts characters on key-down events
        if getattr(event, "event_type", None) == "down":
            self._batching.record_character_and_maybe_upload()

    def setup_hotkeys(self):
        self._hotkeys_controller.register()

    def setup_tray(self):
        # pystray needs a constructed icon; adapter already has it.
        # Keep same BaseApp compatibility pattern as standard/app.py.
        self._tray_icon = self._tray._icon  # type: ignore[attr-defined]
        self.icon = self._tray_icon

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
        # upload research batch before exiting
        final = dict(self._collector.stats)
        # total minutes = elapsed in current run (BaseApp doesn’t track it)
        # keep existing behavior from legacy implementation by approximating as 0.
        # (batching.reset_batch updates TotalUsageMinutes; this is final snapshot.)
        self.logger.info("Uploading research data before shutdown...")
        self._deps.batching._uploader.execute(data=final)  # type: ignore[attr-defined]
        super().stop()

