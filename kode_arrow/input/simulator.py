import logging
import pyautogui

logger = logging.getLogger(__name__)

class KeyboardSimulator:
    """Simulates keyboard input for automation."""

    def __init__(self, interval: float = 0.0):
        self.interval = interval
        pyautogui.FAILSAFE = True

    def press(self, key: str) -> bool:
        try:
            pyautogui.press(key, interval=self.interval)
            return True
        except Exception as e:
            logger.error(f"Failed to press key '{key}': {e}")
            return False

    def type_text(self, text: str) -> bool:
        try:
            pyautogui.write(text, interval=self.interval)
            return True
        except Exception:
            return False

    def press_combination(self, *keys: str) -> bool:
        if not keys: return False
        try:
            for key in keys: pyautogui.keyDown(key)
            for key in reversed(keys): pyautogui.keyUp(key)
            return True
        except Exception:
            return False
