import itertools
import keyboard
import pyautogui
import time
from kode_arrow.utils.file import write_to_file
from kode_arrow.utils.network import check_internet_connection

class HotkeyEngine:
    def __init__(self, is_premium_fn, telemetry_service, usage_file="premium_Key_metadata.txt"):
        self.is_premium = is_premium_fn
        self.telemetry = telemetry_service
        self.usage_file = usage_file
        
        self.total_keyStrokes = 0
        self.total_shortcuts = 0
        self.multiplier = 20
        self.previous_time = time.time()
        
        pyautogui.PAUSE = 0.000001
        
        self.key_actions = {
            'i': self.up_arrow,
            'j': self.left_arrow,
            'k': self.down_arrow,
            'l': self.right_arrow
        }

    def _hehe(self):
        return True

    def updateData(self):
        self.total_keyStrokes -= 1
        self.total_shortcuts += 1

    def left_arrow(self):
        keyboard.add_hotkey('alt+left', self._hehe, suppress=True)
        pyautogui.press('left')
        self.updateData()
        keyboard.remove_hotkey('alt+left')

    def right_arrow(self):
        keyboard.add_hotkey('alt+right', self._hehe, suppress=True)
        pyautogui.press('right')
        self.updateData()
        keyboard.remove_hotkey('alt+right')

    def down_arrow(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+down', self._hehe, suppress=True)
            pyautogui.press('down')
            self.updateData()
            keyboard.remove_hotkey('alt+down')

    def up_arrow(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+up', self._hehe, suppress=True)
            pyautogui.press('up')
            self.updateData()
            keyboard.remove_hotkey('alt+up')

    def page_up_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+pageup', self._hehe, suppress=True)
            pyautogui.press('pageup')
            self.updateData()
            keyboard.remove_hotkey('alt+pageup')

    def page_down_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+pagedown', self._hehe, suppress=True)
            pyautogui.press('pagedown')
            self.updateData()
            keyboard.remove_hotkey('alt+pagedown')

    def end_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+end', self._hehe, suppress=True)
            pyautogui.press('end')
            self.updateData()
            keyboard.remove_hotkey('alt+end')

    def home_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+home', self._hehe, suppress=True)
            pyautogui.press('home')
            self.updateData()
            keyboard.remove_hotkey('alt+home')

    def backspace_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+backspace', self._hehe, suppress=True)
            pyautogui.press('backspace')
            self.updateData()
            keyboard.remove_hotkey('alt+backspace')
            
    def delete_key(self):
        if self.is_premium():
            keyboard.add_hotkey('alt+delete', self._hehe, suppress=True)
            pyautogui.press('delete')
            self.updateData()
            keyboard.remove_hotkey('alt+delete')

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
        keys = ['i', 'j', 'k', 'l']
        for key in keys:
            keyboard.add_hotkey(f'alt+{key}', self.handle_combination, args=(key,), suppress=True)
        for combo in itertools.permutations(keys, 2):
            keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}', self.handle_combination, args=combo, suppress=True)
        for combo in itertools.permutations(keys, 3):
            keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}', self.handle_combination, args=combo, suppress=True)
        for combo in itertools.permutations(keys, 4):
            keyboard.add_hotkey(f'alt+{combo[0]}+{combo[1]}+{combo[2]}+{combo[3]}', self.handle_combination, args=combo, suppress=True)

        keyboard.add_hotkey('alt+u', self.home_key, suppress=True)
        keyboard.add_hotkey('alt+o', self.end_key, suppress=True)
        keyboard.add_hotkey('alt+p', self.delete_key, suppress=True)
        keyboard.add_hotkey('alt+;', self.backspace_key, suppress=True)
        keyboard.add_hotkey('alt+[', self.page_up_key, suppress=True)
        keyboard.add_hotkey("alt+'", self.page_down_key, suppress=True)

        keyboard.hook(self.increment_total_keyStrokes)
