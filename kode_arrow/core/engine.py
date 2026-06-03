import itertools
import keyboard
import pyautogui
import time
from kode_arrow.utils.file import write_to_file
from kode_arrow.utils.network import check_internet_connection
from kode_arrow.config.user_prefs import UserPrefs

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

    def handle_combination(self, *keys):
        for key in keys:
            self.key_actions[key]()

    def calculate_user_data(self):
        self.total_keyStrokes += 1
        if self.total_keyStrokes > self.multiplier:
            current_time = time.time()
            time_interval = current_time - self.previous_time
            self.previous_time = current_time

            write_to_file(self.usage_file, self.total_keyStrokes, self.total_shortcuts, time_interval/60)

            if check_internet_connection():
                self.telemetry.run_async_upload_threaded()

            self.total_shortcuts = 0
            self.total_keyStrokes = 0

    def increment_total_keyStrokes(self, event):
        if event.event_type == 'down':
             self.calculate_user_data()
             print(f"Key pressed: {event.name}")

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

        if not self._is_hooked:
            keyboard.hook(self.increment_total_keyStrokes)
            self._is_hooked = True

    def reload_hotkeys(self):
        keyboard.unhook_all_hotkeys()
        self.load_prefs()
        self.start()
