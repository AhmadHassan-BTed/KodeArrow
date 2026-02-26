import os
import sys
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
import webbrowser

from kode_arrow.security.hardware_identifier import get_hardware_id
from kode_arrow.security.encryption import encrypt_hardware_id
from kode_arrow.services.firebase import FirebaseService
from kode_arrow.services.licensing import LicensingService
from kode_arrow.services.telemetry import TelemetryService
from kode_arrow.ui.tray import SystemTray
from kode_arrow.ui.dialogs import UIWindowManager
from kode_arrow.core.engine import HotkeyEngine
from kode_arrow.utils.file import create_hidden_file, find_email_in_file
from kode_arrow.utils.network import check_internet_connection

class KodeArrowApp:
    def __init__(self, is_research=True):
        self.is_research = is_research
        
        self.hardware_id = get_hardware_id()
        encrypted_inner = encrypt_hardware_id(self.hardware_id)
        encrypted_outer = encrypt_hardware_id(encrypted_inner)
        self.encrypted_id = f"B4{encrypted_inner}3TzD{encrypted_outer}u"
        self.premium_file_path = f"{self.encrypted_id}.txt"
        self.usage_file = "premium_Key_metadata.txt"
        
        self.firebase = FirebaseService()
        self.licensing = LicensingService(self.firebase)
        self.telemetry = TelemetryService(self.firebase, self.premium_file_path, self.usage_file)
        
        # Original script explicitly initializes the hidden file
        create_hidden_file(self.usage_file)

        self.engine = HotkeyEngine(
            is_premium_fn=self.is_premium,
            telemetry_service=self.telemetry,
            usage_file=self.usage_file
        )
        
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'branding', 'icon.ico'))
        self.tray = SystemTray(icon_path=icon_path, on_open_creator_links=self.open_url)

    def is_premium(self):
        return os.path.exists(self.premium_file_path)

    def open_url(self):
        webbrowser.open("http://bted.wuaze.com/")
        webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")
        
    def open_url_buy(self):
        webbrowser.open("http://kodearrow.wuaze.com/")

    def statup_configuration(self):
        try:
            admin_ref = self.firebase.db.collection('admins').document('StartUp_Configurations').collection("version_2.0_research").document('stats')
            doc = admin_ref.get()
            doc_data = doc.to_dict() if doc.exists else {}
            status = doc_data.get('status_flag_2.0_research', False)
            message = doc_data.get('message_2.0_research', "")
            
            if status:
                UIWindowManager.showMessage_versionEnded(message)
                threading.Thread(target=UIWindowManager.close_windows, daemon=True).start()
                if os.path.exists(self.premium_file_path):
                    os.remove(self.premium_file_path)
                self.stop()
            else:
                self.licensing.validate_email_info_on_startup(self.premium_file_path, find_email_in_file, self.is_research)
        except Exception as e:
            print(f"Startup config check failed: {e}")

    async def run_check_and_update_with_timeout(self):
        with ThreadPoolExecutor() as executor:
            try:
                await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(executor, self.statup_configuration), timeout=30)
            except asyncio.TimeoutError:
                messagebox.showinfo("Error", "The current version has expired\nPlease update KodeArrow to the newest version")
                if os.path.exists(self.premium_file_path):
                    os.remove(self.premium_file_path)
                os._exit(0)

    def start_check_and_update(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_check_and_update_with_timeout())
        loop.close()

    def start(self):
        if check_internet_connection():
            threading.Thread(target=self.start_check_and_update).start()
            
        threading.Thread(target=UIWindowManager.show_instructions, args=(self.is_premium(),), daemon=True).start()
        
        self.engine.start()

        def on_unlock():
            threading.Thread(target=UIWindowManager.unlock_functionality, args=(self.submit_key,), daemon=True).start()


        self.tray.build_menu(
            is_premium=self.is_premium(),
            on_unlock=None if self.is_premium() else on_unlock,
            on_exit=self.stop,
            on_open_portfolio=self.open_url,
            on_open_website=self.open_url_buy,
        )
        
        if check_internet_connection():
            self.telemetry.run_async_upload_threaded()
            
        self.tray.run()

    def submit_key(self, email):
        return self.licensing.validate_and_activate(email, self.hardware_id, self.premium_file_path, self.is_research)

    def stop(self):
        if check_internet_connection():
            self.telemetry.run_async_upload_threaded()
        if self.tray:
            self.tray.stop()
        os._exit(0)
