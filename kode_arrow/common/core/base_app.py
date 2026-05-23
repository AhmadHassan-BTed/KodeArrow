import os
import sys
import logging
from abc import ABC, abstractmethod
from kode_arrow.infrastructure.security.hardware_identifier import get_hardware_id
from kode_arrow.infrastructure.security.encryption import encrypt_hardware_id


class BaseApp(ABC):
    """Abstract Base Class for KodeArrow Application versions."""

    def __init__(self, version_name):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.version_name = version_name
        self.hardware_id = get_hardware_id()
        self.encrypted_id = (
            f"B4{encrypt_hardware_id(self.hardware_id)}"
            f"3TzD{encrypt_hardware_id(encrypt_hardware_id(self.hardware_id))}u"
        )
        self.premium_file = f"{self.encrypted_id}.txt"
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

    @abstractmethod
    def setup_tray(self):
        """Initialize the system tray icon."""
        pass

    @abstractmethod
    def run_tray(self):
        """Run the system tray event loop."""
        pass

    def stop(self):
        """Gracefully shuts down the application."""
        self.is_running = False
        self.logger.info(f"{self.version_name} stopped.")
        sys.exit()

    def on_startup(self):
        """Hook for additional startup logic."""
        pass
