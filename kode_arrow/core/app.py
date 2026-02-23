import os
import sys
import logging
import webbrowser
from tkinter import messagebox
import customtkinter as ctk

from kode_arrow.security.hardware_identifier import get_hardware_id
from kode_arrow.security.encryption import encrypt_hardware_id
from kode_arrow.services.firebase import FirebaseService
from kode_arrow.services.licensing import LicensingService
from kode_arrow.services.telemetry import TelemetryService
from kode_arrow.ui.tray import SystemTray
from kode_arrow.ui.dialogs import UIWindowManager
from kode_arrow.input.simulator import KeyboardSimulator
from kode_arrow.core.engine import HotkeyEngine

class KodeArrowApp:
    """The central application container wiring components together."""

    def __init__(self, is_research=False):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.is_research = is_research
        
        # Hardware ID and File setup
        self.hardware_id = get_hardware_id()
        encrypted_inner = encrypt_hardware_id(self.hardware_id)
        encrypted_outer = encrypt_hardware_id(encrypted_inner)
        self.encrypted_id = f"B4{encrypted_inner}3TzD{encrypted_outer}u"
        self.premium_file = f"{self.encrypted_id}.txt"
        
        # Services
        self.firebase = FirebaseService()
        self.licensing = LicensingService(self.firebase)
        
        self.telemetry = None
        if self.is_research:
            self.telemetry = TelemetryService(
                firebase_service=self.firebase,
                email="research_user@example.com",
                multiplier=20
            )

        # UI
        icon_path = "assets/icon_r.ico" if self.is_research else "assets/icon.ico"
        self.tray = SystemTray(icon_path=icon_path)
        
        # Core Engine
        self.engine = HotkeyEngine(
            simulator=KeyboardSimulator(),
            is_premium=self.is_premium,
            telemetry=self.telemetry
        )

    @property
    def is_premium(self):
        return os.path.exists(self.premium_file)

    def start(self):
        self.logger.info("Starting KodeArrow...")
        UIWindowManager.show_instructions(is_premium=self.is_premium)
        
        self.engine.start()
        
        self.tray.build_menu(
            is_premium=self.is_premium,
            on_unlock=self.unlock if not self.is_research else self.unlock_research,
            on_exit=self.stop,
            on_open_portfolio=lambda: webbrowser.open("https://bted.wuaze.com/"),
            on_open_website=lambda: webbrowser.open("https://kodearrow.wuaze.com/"),
            on_show_research_info=self.show_research_info if self.is_research else None,
            on_open_portal=lambda: webbrowser.open("https://kodearrow.wuaze.com/research") if self.is_research else None
        )
        self.tray.run()

    def unlock(self):
        dialog = ctk.CTkInputDialog(text="Enter Registered Email:", title="Unlock Premium")
        email = dialog.get_input()
        if email:
            success, msg = self.licensing.validate_and_activate(
                email=email, hardware_id=self.hardware_id, 
                premium_file_path=self.premium_file, is_research=False
            )
            if success:
                messagebox.showinfo("Success", "Premium Unlocked! Please restart the app.")
                self.stop()
            else:
                messagebox.showerror("Error", msg)

    def unlock_research(self):
        dialog = ctk.CTkInputDialog(text="Enter Research Email:", title="Unlock Research Edition")
        email = dialog.get_input()
        if email:
            success, msg = self.licensing.validate_and_activate(
                email=email, hardware_id=self.hardware_id, 
                premium_file_path=self.premium_file, is_research=True
            )
            if success:
                messagebox.showinfo("Success", "Premium access unlocked! Please restart the app.")
                self.stop()
            else:
                messagebox.showerror("Error", msg)

    def show_research_info(self):
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        stats = self.telemetry.stats if self.telemetry else {}
        chars = stats.get('charactersTyped', 0)
        hk = stats.get('kodeArrowHotkeys', 0)
        messagebox.showinfo("Research Stats", f"Characters: {chars}\nHotkeys: {hk}")
        root.destroy()

    def stop(self):
        if self.telemetry:
            self.logger.info("Uploading research data before shutdown...")
            self.telemetry.upload_and_reset()
        if self.tray:
            self.tray.stop()
        self.logger.info("KodeArrow stopped.")
        os._exit(0)
