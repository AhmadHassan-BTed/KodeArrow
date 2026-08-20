import os
import sys
import subprocess
import logging
from kode_arrow.utils.resource import get_resource_path

logger = logging.getLogger("KodeArrow.LinuxKeyd")

CONF_PATH = "/etc/keyd/kodearrow.conf"

def is_keyd_installed() -> bool:
    """Checks if keyd daemon binary is installed."""
    try:
        res = subprocess.run(["command", "-v", "keyd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return res.returncode == 0
    except Exception:
        return False

def is_keyd_active() -> bool:
    """Checks if kodearrow.conf exists and keyd service is running."""
    if not os.path.exists(CONF_PATH):
        return False
    try:
        res = subprocess.run(["systemctl", "is-active", "--quiet", "keyd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    except Exception:
        return False

def get_default_conf_content() -> str:
    """Returns the default keyd configuration content."""
    conf_template = get_resource_path(os.path.join("config", "kodearrow.conf"))
    if os.path.exists(conf_template):
        with open(conf_template, "r", encoding="utf-8") as f:
            return f.read()
    return """[ids]
*

[alt]
i = up
j = left
k = down
l = right
u = home
o = end
p = delete
semicolon = backspace
leftbrace  = pageup
apostrophe = pagedown

[control+alt]
u = C-S-home
i = C-S-up
o = C-S-end
j = C-S-left
k = C-S-down
l = C-S-right
p = C-delete
semicolon = C-backspace
"""

def apply_keyd_mapping() -> bool:
    """
    Applies the KodeArrow keyd mapping on Linux.
    Returns True if successful.
    """
    if not sys.platform.startswith("linux"):
        return False

    script_path = get_resource_path(os.path.join("scripts", "kodearrow"))
    if os.path.exists(script_path):
        try:
            logger.info("Executing scripts/kodearrow for Linux keyd setup...")
            res = subprocess.run(["sudo", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                logger.info("Linux keyd mapping successfully applied.")
                return True
            else:
                logger.warning("scripts/kodearrow output: %s %s", res.stdout, res.stderr)
        except Exception as e:
            logger.error("Failed to execute scripts/kodearrow: %s", e)

    return is_keyd_active()
