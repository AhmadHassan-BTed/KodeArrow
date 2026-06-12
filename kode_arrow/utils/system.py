import os
import sys
import logging
import winreg

APP_NAME = "KodeArrow"
logger = logging.getLogger("KodeArrow.System")

def get_executable_path():
    """Returns the path to the running executable (or python script)."""
    if getattr(sys, 'frozen', False):
        # Running as compiled PyInstaller executable
        return sys.executable
    else:
        # Running as python script
        return os.path.abspath(sys.argv[0])

def is_autostart_enabled():
    """Checks if KodeArrow is currently set to start with Windows."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return value == get_executable_path()
    except FileNotFoundError:
        return False
    except Exception as e:
        logger.warning(f"Error checking autostart: {e}")
        return False

def enable_autostart():
    """Enables Windows autostart for KodeArrow."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, get_executable_path())
        winreg.CloseKey(key)
        return True
    except Exception as e:
        logger.warning(f"Error enabling autostart: {e}")
        return False

def disable_autostart():
    """Disables Windows autostart for KodeArrow."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return True # Already disabled
    except Exception as e:
        logger.warning(f"Error disabling autostart: {e}")
        return False
