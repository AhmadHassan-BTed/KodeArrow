import json
import os
from kode_arrow.utils.resource import get_resource_path

# Standard locations
PREFS_FILE = os.path.join(os.path.expanduser("~"), ".kodearrow_prefs.json")

DEFAULT_PREFS = {
    "hotkeys": {
        "up": "i",
        "down": "k",
        "left": "j",
        "right": "l",
        "home": "u",
        "end": "o",
        "delete": "p",
        "backspace": ";",
        "pageup": "[",
        "pagedown": "'"
    },
    "modifier": "alt",
    "theme": "light"
}

class UserPrefs:
    @staticmethod
    def load():
        if not os.path.exists(PREFS_FILE):
            return DEFAULT_PREFS.copy()
        try:
            with open(PREFS_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults in case of missing keys
                prefs = DEFAULT_PREFS.copy()
                if "hotkeys" in data:
                    prefs["hotkeys"].update(data["hotkeys"])
                if "modifier" in data:
                    prefs["modifier"] = data["modifier"]
                if "theme" in data:
                    prefs["theme"] = data["theme"]
                return prefs
        except Exception as e:
            print(f"Error loading prefs: {e}")
            return DEFAULT_PREFS.copy()

    @staticmethod
    def save(prefs_dict):
        try:
            with open(PREFS_FILE, "w") as f:
                json.dump(prefs_dict, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving prefs: {e}")
            return False
