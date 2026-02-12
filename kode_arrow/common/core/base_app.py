import os
import sys
import threading
import logging
import pystray
import pyautogui
import keyboard
from PIL import Image
from abc import ABC, abstractmethod
from ..services.firebase_service import FirebaseService
from ..utils.helpers import get_hardware_id, encrypt_hardwareID

class BaseApp(ABC):
    """Abstract Base Class for KodeArrow Application versions."""
    
    def __init__(self, version_name):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.version_name = version_name
        self.firebase = FirebaseService()
        self.hardware_id = get_hardware_id()
        self.encrypted_id = f"B4{encrypt_hardwareID(self.hardware_id)}3TzD{encrypt_hardwareID(encrypt_hardwareID(self.hardware_id))}u"
        self.premium_file = f"{self.encrypted_id}.txt"
        self.icon = None
        self.is_running = True

    @property
    def is_premium(self):
        return os.path.exists(self.premium_file)

    def start(self):
        """Starts the application components."""
        self.logger.info(f"Starting {self.version_name}...")
        self.setup_hotkeys()
        self.setup_tray()
        self.on_startup()
        self.run_tray()

    @abstractmethod
    def setup_hotkeys(self):
        """Register keyboard hooks."""
        pass

    def register_extended_hotkeys(self):
        """Registers the extended suite of navigation hotkeys."""
        extended_keys = {
            'u': 'home',
            'o': 'end',
            'p': 'delete',
            ';': 'backspace',
            '[': 'pageup',
            "'": 'pagedown'
        }
        
        for key, target in extended_keys.items():
            keyboard.add_hotkey(f'alt+{key}', lambda t=target: self.press_key(t) if self.is_premium else None, suppress=True)
        self.logger.info("Extended navigation hotkeys registered.")

    @abstractmethod
    def setup_tray(self):
        """Initialize the system tray icon."""
        pass

    def run_tray(self):
        if self.icon:
            self.icon.run()

    def stop(self):
        """Gracefully shuts down the application."""
        self.is_running = False
        if self.icon:
            self.icon.stop()
        self.logger.info(f"{self.version_name} stopped.")
        sys.exit()

    def on_startup(self):
        """Hook for additional startup logic."""
        pass

    def press_key(self, key):
        """Safely press a key with pyautogui."""
        try:
            pyautogui.press(key)
        except Exception as e:
            self.logger.error(f"Failed to press key {key}: {e}")
