import itertools
import keyboard
import pyautogui
import time
import threading
import logging
from kode_arrow.utils.file import write_to_file
from kode_arrow.utils.network import check_internet_connection
from kode_arrow.config.user_prefs import UserPrefs

logger = logging.getLogger("KodeArrow.Engine")


class HotkeyEngine:
    def __init__(self, is_premium_fn, telemetry_service, usage_file="premium_Key_metadata.txt"):
        self.is_premium = is_premium_fn
        self.telemetry = telemetry_service
        self.usage_file = usage_file
        
        self.total_keyStrokes = 0
        self.total_shortcuts = 0
        self.multiplier = 20
        self.previous_time = time.time()
        self._is_hooked = False
        self._reload_lock = threading.Lock()
        self._last_hook_activity = time.time()
        
        pyautogui.PAUSE = 0.000001
        
        self.load_prefs()

    def load_prefs(self):
        prefs_data = UserPrefs.load()
        prefs = prefs_data["hotkeys"]
        self.modifier = prefs_data.get("modifier", "alt")
        
        self.hk_up = prefs.get("up", "i")
        self.hk_down = prefs.get("down", "k")
        self.hk_left = prefs.get("left", "j")
        self.hk_right = prefs.get("right", "l")
        
        self.hk_home = prefs.get("home", "u")
        self.hk_end = prefs.get("end", "o")
        self.hk_delete = prefs.get("delete", "p")
        self.hk_backspace = prefs.get("backspace", ";")
        self.hk_pageup = prefs.get("pageup", "[")
        self.hk_pagedown = prefs.get("pagedown", "'")

        self.key_actions = {
            self.hk_up: self.up_arrow,
            self.hk_left: self.left_arrow,
            self.hk_down: self.down_arrow,
            self.hk_right: self.right_arrow
        }

    def _hehe(self):
        return True

    def updateData(self):
        self.total_keyStrokes -= 1
        self.total_shortcuts += 1

    def left_arrow(self):
        keyboard.add_hotkey(f'{self.modifier}+left', self._hehe, suppress=True)
        pyautogui.press('left')
        self.updateData()
        keyboard.remove_hotkey(f'{self.modifier}+left')

    def right_arrow(self):
        keyboard.add_hotkey(f'{self.modifier}+right', self._hehe, suppress=True)
        pyautogui.press('right')
        self.updateData()
        keyboard.remove_hotkey(f'{self.modifier}+right')

    def down_arrow(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+down', self._hehe, suppress=True)
            pyautogui.press('down')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+down')

    def up_arrow(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+up', self._hehe, suppress=True)
            pyautogui.press('up')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+up')

    def page_up_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+pageup', self._hehe, suppress=True)
            pyautogui.press('pageup')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+pageup')

    def page_down_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+pagedown', self._hehe, suppress=True)
            pyautogui.press('pagedown')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+pagedown')

    def end_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+end', self._hehe, suppress=True)
            pyautogui.press('end')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+end')

    def home_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+home', self._hehe, suppress=True)
            pyautogui.press('home')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+home')

    def backspace_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+backspace', self._hehe, suppress=True)
            pyautogui.press('backspace')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+backspace')
            
    def delete_key(self):
        if self.is_premium():
            keyboard.add_hotkey(f'{self.modifier}+delete', self._hehe, suppress=True)
            pyautogui.press('delete')
            self.updateData()
            keyboard.remove_hotkey(f'{self.modifier}+delete')

    def _execute_selection(self, key_target):
        alt_was_down = keyboard.is_pressed('alt') or keyboard.is_pressed('left alt') or keyboard.is_pressed('right alt')
        left_alt_was_down = keyboard.is_pressed('left alt')
        right_alt_was_down = keyboard.is_pressed('right alt')
        
        if left_alt_was_down:
            pyautogui.keyUp('left alt')
        if right_alt_was_down:
            pyautogui.keyUp('right alt')
        if alt_was_down and not (left_alt_was_down or right_alt_was_down):
            pyautogui.keyUp('alt')
            
        pyautogui.hotkey('ctrl', 'shift', key_target)
        
        if left_alt_was_down:
            pyautogui.keyDown('left alt')
        if right_alt_was_down:
            pyautogui.keyDown('right alt')
        if alt_was_down and not (left_alt_was_down or right_alt_was_down):
            pyautogui.keyDown('alt')
            
        self.updateData()

    def select_word_left(self):
        self._execute_selection('left')

    def select_word_right(self):
        self._execute_selection('right')

    def select_text_up(self):
        self._execute_selection('up')

    def select_text_down(self):
        self._execute_selection('down')

    def select_text_home(self):
        self._execute_selection('home')

    def select_text_end(self):
        self._execute_selection('end')

    def handle_selection_combination(self, *keys):
        for key in keys:
            if key in self.selection_actions:
                self.selection_actions[key]()

    def handle_combination(self, *keys):
        for key in keys:
            self.key_actions[key]()

    def calculate_user_data(self):
        self.total_keyStrokes += 1
        if self.total_keyStrokes > self.multiplier:
            current_time = time.time()
            time_interval = current_time - self.previous_time
            self.previous_time = current_time

            strokes = self.total_keyStrokes
            shortcuts = self.total_shortcuts

            self.total_shortcuts = 0
            self.total_keyStrokes = 0

            def bg_calc():
                try:
                    write_to_file(self.usage_file, strokes, shortcuts, time_interval / 60)
                    if check_internet_connection():
                        self.telemetry.run_async_upload_threaded()
                except Exception as e:
                    logger.warning(f"Error in background telemetry check: {e}")

            threading.Thread(target=bg_calc, daemon=True).start()

    def increment_total_keyStrokes(self, event):
        if event.event_type == 'down':
             self._last_hook_activity = time.time()
             self.calculate_user_data()

    def is_hook_alive(self):
        """Check if the keyboard hook is still functional.
        
        Strategy: The keyboard library maintains internal state about its hooks.
        We check if the hook callback is still registered AND if we've received
        any hook activity within a reasonable window.
        
        If the user genuinely hasn't typed for a long time, the hook may still
        be alive — so we also check the keyboard library's internal hook state.
        """
        try:
            # Check 1: Is the keyboard library's internal hook still registered?
            # keyboard._hooks is the set of active hook callbacks
            if hasattr(keyboard, '_hooks') and not keyboard._hooks:
                logger.warning("keyboard._hooks is empty — hook likely dead")
                return False
            
            # Check 2: Is the low-level listener thread alive?
            # keyboard._listener is the background thread running the hook
            if hasattr(keyboard, '_listener'):
                listener = keyboard._listener
                if listener is not None and hasattr(listener, 'is_alive'):
                    if not listener.is_alive():
                        logger.warning("keyboard._listener thread is dead")
                        return False
            
            return True
        except Exception:
            logger.exception("Error checking hook health")
            # If we can't determine health, assume it's alive to avoid
            # unnecessary restarts
            return True

    def start(self):
        keys = [self.hk_up, self.hk_left, self.hk_down, self.hk_right]
        mod = self.modifier
        for key in keys:
            if key: keyboard.add_hotkey(f'{mod}+{key}', self.handle_combination, args=(key,), suppress=True)
        for combo in itertools.permutations(keys, 2):
            if all(combo): keyboard.add_hotkey(f'{mod}+{combo[0]}+{combo[1]}', self.handle_combination, args=combo, suppress=True)
        for combo in itertools.permutations(keys, 3):
            if all(combo): keyboard.add_hotkey(f'{mod}+{combo[0]}+{combo[1]}+{combo[2]}', self.handle_combination, args=combo, suppress=True)
        for combo in itertools.permutations(keys, 4):
            if all(combo): keyboard.add_hotkey(f'{mod}+{combo[0]}+{combo[1]}+{combo[2]}+{combo[3]}', self.handle_combination, args=combo, suppress=True)

        if self.hk_home: keyboard.add_hotkey(f'{mod}+{self.hk_home}', self.home_key, suppress=True)
        if self.hk_end: keyboard.add_hotkey(f'{mod}+{self.hk_end}', self.end_key, suppress=True)
        if self.hk_delete: keyboard.add_hotkey(f'{mod}+{self.hk_delete}', self.delete_key, suppress=True)
        if self.hk_backspace: keyboard.add_hotkey(f'{mod}+{self.hk_backspace}', self.backspace_key, suppress=True)
        if self.hk_pageup: keyboard.add_hotkey(f'{mod}+{self.hk_pageup}', self.page_up_key, suppress=True)
        if self.hk_pagedown: keyboard.add_hotkey(f'{mod}+{self.hk_pagedown}', self.page_down_key, suppress=True)

        # Selection hotkeys (Ctrl + Alt + [u, i, o, j, k, l] and permutations)
        selection_mods = [
            "ctrl+alt",
            "ctrl+left alt+right alt",
            "ctrl+right alt+left alt"
        ]
        self.selection_actions = {
            self.hk_home: self.select_text_home,
            self.hk_up: self.select_text_up,
            self.hk_end: self.select_text_end,
            self.hk_left: self.select_word_left,
            self.hk_down: self.select_text_down,
            self.hk_right: self.select_word_right
        }
        self.selection_keys = [k for k in [self.hk_home, self.hk_up, self.hk_end, self.hk_left, self.hk_down, self.hk_right] if k]

        for mod_prefix in selection_mods:
            for key in self.selection_keys:
                keyboard.add_hotkey(f'{mod_prefix}+{key}', self.handle_selection_combination, args=(key,), suppress=True)
            for combo in itertools.permutations(self.selection_keys, 2):
                keyboard.add_hotkey(f'{mod_prefix}+{combo[0]}+{combo[1]}', self.handle_selection_combination, args=combo, suppress=True)
            for combo in itertools.permutations(self.selection_keys, 3):
                keyboard.add_hotkey(f'{mod_prefix}+{combo[0]}+{combo[1]}+{combo[2]}', self.handle_selection_combination, args=combo, suppress=True)

        if not self._is_hooked:
            keyboard.hook(self.increment_total_keyStrokes)
            self._is_hooked = True
            logger.info("Keyboard hook installed")

    def reload_hotkeys(self):
        """Re-register all keyboard hooks. Thread-safe via lock."""
        with self._reload_lock:
            logger.info("Reloading hotkeys...")
            try:
                keyboard.unhook_all_hotkeys()
                self._is_hooked = False
                self.load_prefs()
                self.start()
                logger.info("Hotkeys reloaded successfully")
            except Exception:
                logger.exception("Failed to reload hotkeys")
                raise
