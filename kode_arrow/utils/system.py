import os
import sys
import logging

if sys.platform == "win32":
    import winreg

APP_NAME = "KodeArrow"
logger = logging.getLogger("KodeArrow.System")


def get_executable_path():
    """Returns the path to the running executable (or python script)."""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(sys.argv[0])


def _get_linux_autostart_path():
    config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    autostart_dir = os.path.join(config_home, "autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    return os.path.join(autostart_dir, "kodearrow.desktop")


def is_autostart_enabled():
    """Checks if KodeArrow is currently set to start on system boot."""
    if sys.platform == "win32":
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return value == get_executable_path()
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.warning(f"Error checking autostart on Windows: {e}")
            return False
    elif sys.platform.startswith("linux"):
        desktop_path = _get_linux_autostart_path()
        return os.path.exists(desktop_path)
    else:
        return False


def enable_autostart():
    """Enables system autostart for KodeArrow."""
    if sys.platform == "win32":
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, get_executable_path())
            winreg.CloseKey(key)
            return True
        except Exception as e:
            logger.warning(f"Error enabling autostart on Windows: {e}")
            return False
    elif sys.platform.startswith("linux"):
        try:
            desktop_path = _get_linux_autostart_path()
            exec_cmd = f"{sys.executable} {get_executable_path()}" if not getattr(sys, 'frozen', False) else get_executable_path()
            content = f"""[Desktop Entry]
Type=Application
Name=KodeArrow
Comment=Professional Productivity & Navigation Tool
Exec={exec_cmd}
Icon=kodearrow
Terminal=false
Categories=Utility;Development;
X-GNOME-Autostart-enabled=true
X-KDE-autostart-after=panel
"""
            with open(desktop_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            logger.warning(f"Error enabling autostart on Linux: {e}")
            return False
    return False


def disable_autostart():
    """Disables system autostart for KodeArrow."""
    if sys.platform == "win32":
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return True
        except Exception as e:
            logger.warning(f"Error disabling autostart on Windows: {e}")
            return False
    elif sys.platform.startswith("linux"):
        try:
            desktop_path = _get_linux_autostart_path()
            if os.path.exists(desktop_path):
                os.remove(desktop_path)
            return True
        except Exception as e:
            logger.warning(f"Error disabling autostart on Linux: {e}")
            return False
    return False

