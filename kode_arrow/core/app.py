import os
import sys
import asyncio
import threading
import logging
import time
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
from kode_arrow.ui.dashboard import DashboardWindow
from kode_arrow.core.engine import HotkeyEngine
from kode_arrow.core.resilience import WatchdogThread
from kode_arrow.utils.file import create_hidden_file, find_email_in_file
from kode_arrow.utils.network import check_internet_connection

logger = logging.getLogger("KodeArrow.App")

# Maximum number of tray restart attempts before giving up
TRAY_MAX_RETRIES = 10
TRAY_RETRY_DELAY = 2  # seconds


class KodeArrowApp:
    def __init__(self, is_research=True):
        self.is_research = is_research
        self._watchdog = None
        
        self.hardware_id = get_hardware_id()
        encrypted_inner = encrypt_hardware_id(self.hardware_id)
        encrypted_outer = encrypt_hardware_id(encrypted_inner)
        self.encrypted_id = f"B4{encrypted_inner}3TzD{encrypted_outer}u"
        
        # Co-locate license and usage files in the application's executable/script directory.
        # This keeps the activation state secure and co-located with the binary (preventing unauthorized global bypass),
        # while resolving startup/shortcut folder CWD location shifts.
        if getattr(sys, "frozen", False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            
        self.premium_file_path = os.path.join(app_dir, f"{self.encrypted_id}.txt")
        self.usage_file = os.path.join(app_dir, "premium_Key_metadata.txt")

        # Automatically extract and place KodeArrow.txt instructions file in the executable folder on click/startup
        txt_path = os.path.join(app_dir, "KodeArrow.txt")
        if not os.path.exists(txt_path):
            try:
                changelog_content = """## KodeArrow v2.5

The Next Evolution in Ergonomics, Performance, and Security. This major update transforms KodeArrow from a static keyboard hook tool into a premium, user-configurable, and highly secure desktop utility. 

This version introduces real-time hotkey remapping, a designer-grade sidebar dashboard, portable licensing boundaries, and automated build utilities.

---

## Added

* Home-Row Shortcut Customization:
  - Remap your home-row shortcuts directly from the settings interface (e.g. changing Alt + IJKL).
  - Dynamic hotkey engine reloading—re-binds keys in milliseconds without needing to restart the application.
  - Local preferences are saved securely to '~/.kodearrow_prefs.json' for persistence.
* Universal Community Lifetime Key:
  - Unlock the full premium suite using the creative universal community key 'freeforever@kodearrow.dev'.
  - Bypasses standard 4-device limits to support unlimited active installations.
  - Automatically logs anonymous telemetry stats inside the 'ControlGroup' Firestore collection to support ergonomic research.
* Administrative Registry Tool:
  - New utility 'scripts/add_community_license.py' to cleanly register and manage community keys.
* High-Coverage Test Suite:
  - Dedicated 'tests/test_licensing.py' asserting limit bypass and collection routing boundaries.

---

## Changed

* Secure Portable Licensing:
  - Co-located license status and telemetry keys directly next to the application binary.
  - Eliminates all CWD errors when launched via startup registry or shortcuts, while strictly maintaining secure machine-bound authorization.
* Dynamic Thread-Safe UI Update:
  - Dynamic main-thread refresh (.after()) instantly switches states and hides the Unlock button on success without requiring a reload.
* Unified Visual Palette:
  - Aligned the dashboard accent styles to match the signature rich navy blue (#00207f) of other popup dialogue windows.
* Build Process Termination:
  - Automated process-termination routine terminates background instances of KodeArrow.exe to prevent WinError 5 Permission Denied build crashes.
* Sync scripts:
  - Fully aligned backup/restore scripts with private.envs folder layout.

---

## Hotkeys

| Action              | Default Shortcut                     | Configurable? |
| ------------------- | ------------------------------------ | ------------- |
| Arrow Keys          | Alt + I / J / K / L                  | Yes           |
| Home / End          | Alt + U / O                          | Yes           |
| Delete / Backspace  | Alt + P / ;                          | Yes           |
| Page Up / Page Down | Alt + [ / '                          | Yes           |
| Word/Line Selection | Ctrl + Alt + U / I / O / J / K / L    | Yes (follows) |
| (Selection Option)  | Ctrl + Both Alts + U/I/O/J/K/L       | Yes (follows) |
| Word Delete / Bksp  | Ctrl + Alt + P / ;                   | Yes (follows) |

---

## Technical Notes

* Input engine based on low-level Win32 keyboard hooks
* Designed for uninterrupted home-row workflows
* Tested across multiple DPI scaling environments

---

## Author

Ahmad Hassan (B-Ted)
"""
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(changelog_content)
            except Exception as e:
                logger.warning(f"Failed to generate KodeArrow.txt on startup: {e}")
        
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
        
        from kode_arrow.utils.resource import get_resource_path
        icon_path = get_resource_path(os.path.join("assets", "branding", "icon.ico"))
        self.tray = SystemTray(icon_path=icon_path, on_open_creator_links=self.open_url)

    def is_premium(self):
        return os.path.exists(self.premium_file_path)

    def open_url(self):
        webbrowser.open("https://ahmadhassan-bted.github.io/KodeArrow/")
        webbrowser.open("https://www.linkedin.com/in/ahmad-hassan-52ab4225b/")
        
    def open_url_buy(self):
        webbrowser.open("http://ahmadhassan-bted.github.io/KodeArrow/")

    def open_dashboard(self):
        def on_unlock(on_success=None):
            def submit_and_callback(email):
                res = self.submit_key(email)
                if res and on_success:
                    on_success()
                return res
            threading.Thread(target=UIWindowManager.unlock_functionality, args=(submit_and_callback,), daemon=True).start()
            
        threading.Thread(
            target=DashboardWindow.open,
            args=(self.is_premium, self.open_url_buy, self.stop, self.engine.reload_hotkeys, on_unlock),
            daemon=True
        ).start()

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
            logger.warning(f"Startup config check failed: {e}")

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
            threading.Thread(target=self.start_check_and_update, daemon=True).start()
            
        threading.Thread(target=UIWindowManager.show_instructions, args=(self.is_premium(),), daemon=True).start()
        
        self.engine.start()
        logger.info("Hotkey engine started")

        # =====================================================================
        # Start the Watchdog — monitors hook health and power events
        # =====================================================================
        self._watchdog = WatchdogThread(engine=self.engine, heartbeat_interval=30)
        self._watchdog.start()
        logger.info("Watchdog thread started")

        def on_unlock(on_success=None):
            def submit_and_callback(email):
                res = self.submit_key(email)
                if res and on_success:
                    on_success()
                return res
            threading.Thread(target=UIWindowManager.unlock_functionality, args=(submit_and_callback,), daemon=True).start()

        self.tray.build_menu(
            is_premium_fn=self.is_premium,
            on_open_dashboard=self.open_dashboard,
            on_unlock=on_unlock,
            on_exit=self.stop,
            on_open_portfolio=self.open_url,
            on_open_website=self.open_url_buy,
        )
        
        if check_internet_connection():
            self.telemetry.run_async_upload_threaded()

        # =====================================================================
        # Tray retry loop — if pystray dies (e.g. after sleep/wake GDI handle
        # invalidation), rebuild the tray and re-enter the event loop.
        # =====================================================================
        for tray_attempt in range(1, TRAY_MAX_RETRIES + 1):
            try:
                if tray_attempt > 1:
                    logger.warning(
                        "Tray restart attempt %d/%d",
                        tray_attempt, TRAY_MAX_RETRIES
                    )
                    # Rebuild the tray icon from scratch
                    from kode_arrow.utils.resource import get_resource_path
                    icon_path = get_resource_path(os.path.join("assets", "branding", "icon.ico"))
                    self.tray = SystemTray(icon_path=icon_path, on_open_creator_links=self.open_url)
                    self.tray.build_menu(
                        is_premium_fn=self.is_premium,
                        on_open_dashboard=self.open_dashboard,
                        on_unlock=on_unlock,
                        on_exit=self.stop,
                        on_open_portfolio=self.open_url,
                        on_open_website=self.open_url_buy,
                    )
                
                logger.info("Starting system tray event loop (attempt %d)", tray_attempt)
                self.tray.run()
                
                # If run() returns cleanly (user chose Exit), break out
                logger.info("System tray exited cleanly")
                break
                
            except Exception:
                logger.exception(
                    "System tray crashed on attempt %d/%d",
                    tray_attempt, TRAY_MAX_RETRIES
                )
                if tray_attempt < TRAY_MAX_RETRIES:
                    time.sleep(TRAY_RETRY_DELAY)
                else:
                    logger.critical("All tray restart attempts exhausted — re-raising")
                    raise

    def submit_key(self, email):
        return self.licensing.validate_and_activate(email, self.hardware_id, self.premium_file_path, self.is_research)

    def stop(self):
        logger.info("KodeArrow shutting down...")
        try:
            if check_internet_connection():
                self.telemetry.run_async_upload_threaded()
        except Exception:
            logger.exception("Failed to upload telemetry during shutdown")
        
        try:
            if self._watchdog:
                self._watchdog.stop()
        except Exception:
            logger.exception("Failed to stop watchdog during shutdown")
        
        try:
            if self.tray:
                self.tray.stop()
        except Exception:
            logger.exception("Failed to stop tray during shutdown")
        
        os._exit(0)
