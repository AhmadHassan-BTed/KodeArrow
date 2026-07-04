import sys
import ctypes
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

vk_map = {
    'alt': 0x12,
    'left alt': 0xA4,
    'right alt': 0xA5,
    'ctrl': 0x11,
    'control': 0x11,
    'left ctrl': 0xA2,
    'left control': 0xA2,
    'right ctrl': 0xA3,
    'right control': 0xA3,
    'shift': 0x10,
    'left shift': 0xA0,
    'right shift': 0xA1,
    'win': 0x5B,
    'windows': 0x5B,
    'left win': 0x5B,
    'left windows': 0x5B,
    'right win': 0x5C,
    'right windows': 0x5C,
}


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
        self._during_simulation = False
        self._last_safety_release_time = 0
        
        pyautogui.PAUSE = 0.000001
        
        self.load_prefs()

    def load_prefs(self):
        prefs_data = UserPrefs.load()
        prefs = prefs_data["hotkeys"]
        self.modifier = prefs_data.get("modifier", "alt")
        
        # Pre-calculate modifier variants for fast lookup in key hooks
        mod = (self.modifier or 'alt').lower()
        self._modifier_variants = {mod}
        if 'alt' in mod:
            self._modifier_variants.update(('alt', 'left alt', 'right alt'))
        elif 'ctrl' in mod or 'control' in mod:
            self._modifier_variants.update(('ctrl', 'left ctrl', 'right ctrl', 'control', 'left control', 'right control'))
        elif 'shift' in mod:
            self._modifier_variants.update(('shift', 'left shift', 'right shift'))
        elif 'win' in mod or 'super' in mod or 'meta' in mod:
            self._modifier_variants.update(('windows', 'left windows', 'right windows', 'win', 'left win', 'right win'))

        # The selection/word-action hotkeys registered in start() always require
        # Ctrl+Alt together. The Ctrl desync is handled at the action level
        # (_execute_selection / _execute_word_action avoid injecting synthetic
        # ctrl press/release when it's already physically held). Only Alt needs
        # the safety-net release here — watching Ctrl would cause every normal
        # Ctrl release (e.g. Ctrl+click to select files) to be intercepted.
        self._modifier_variants.update(('alt', 'left alt', 'right alt'))
        
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

    def _is_physical_key_down(self, key_name):
        if sys.platform != 'win32':
            res = keyboard.is_pressed(key_name)
            logger.debug(f"[Physical Check] Non-Win32 key_name={key_name!r} is_down={res}")
            return res
        try:
            vk = vk_map.get(key_name.lower())
            if vk is not None:
                res = bool(ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000)
                logger.debug(f"[Physical Check] key_name={key_name!r} (vk=0x{vk:02X}) is_down={res}")
                return res
        except Exception as e:
            logger.warning(f"Error checking physical key state for {key_name}: {e}")
        res = keyboard.is_pressed(key_name)
        logger.debug(f"[Physical Check] (Fallback) key_name={key_name!r} is_down={res}")
        return res

    def _execute_selection(self, key_target):
        logger.debug(f"[_execute_selection] START target={key_target!r}")
        self._during_simulation = True
        try:
            alt_was_down = self._is_physical_key_down('alt')
            left_alt_was_down = self._is_physical_key_down('left alt')
            right_alt_was_down = self._is_physical_key_down('right alt')
            ctrl_is_down = self._is_physical_key_down('ctrl')
            logger.debug(f"[_execute_selection] Initial states: alt={alt_was_down}, left={left_alt_was_down}, right={right_alt_was_down}, ctrl={ctrl_is_down}")
            
            if left_alt_was_down:
                logger.debug("[_execute_selection] pyautogui.keyUp('left alt')")
                pyautogui.keyUp('left alt')
            if right_alt_was_down:
                logger.debug("[_execute_selection] pyautogui.keyUp('right alt')")
                pyautogui.keyUp('right alt')
            if alt_was_down and not (left_alt_was_down or right_alt_was_down):
                logger.debug("[_execute_selection] pyautogui.keyUp('alt')")
                pyautogui.keyUp('alt')

            if ctrl_is_down:
                # Ctrl is already physically held -- every selection hotkey requires
                # ctrl+alt, so it's guaranteed to be down here. Do NOT press/release it
                # again through pyautogui: injecting a synthetic ctrl-up while the real
                # key is still held is exactly what desyncs the keyboard library's
                # tracking of Ctrl (a known issue with suppress=True hotkeys -- see
                # github.com/boppreh/keyboard issues #442 and #666). Once that happens
                # every later ctrl+alt+... hotkey silently stops matching until Ctrl is
                # physically released and pressed again. Just add Shift on top instead.
                logger.debug(f"[_execute_selection] ctrl already physically down; sending shift+{key_target!r} only")
                pyautogui.keyDown('shift')
                pyautogui.press(key_target)
                pyautogui.keyUp('shift')
            else:
                logger.debug(f"[_execute_selection] ctrl not physically down; pyautogui.hotkey('ctrl', 'shift', {key_target!r})")
                pyautogui.hotkey('ctrl', 'shift', key_target)
            
            # Re-check physical states to avoid race conditions
            if left_alt_was_down:
                p_down = self._is_physical_key_down('left alt')
                logger.debug(f"[_execute_selection] Restoring left alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('left alt')
            if right_alt_was_down:
                p_down = self._is_physical_key_down('right alt')
                logger.debug(f"[_execute_selection] Restoring right alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('right alt')
            if alt_was_down and not (left_alt_was_down or right_alt_was_down):
                p_down = self._is_physical_key_down('alt')
                logger.debug(f"[_execute_selection] Restoring generic alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('alt')
                
            self.updateData()
        finally:
            self._during_simulation = False
            logger.debug("[_execute_selection] END")

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

    def _execute_word_action(self, key_target):
        logger.debug(f"[_execute_word_action] START target={key_target!r}")
        self._during_simulation = True
        try:
            alt_was_down = self._is_physical_key_down('alt')
            left_alt_was_down = self._is_physical_key_down('left alt')
            right_alt_was_down = self._is_physical_key_down('right alt')
            ctrl_is_down = self._is_physical_key_down('ctrl')
            logger.debug(f"[_execute_word_action] Initial states: alt={alt_was_down}, left={left_alt_was_down}, right={right_alt_was_down}, ctrl={ctrl_is_down}")
            
            if left_alt_was_down:
                logger.debug("[_execute_word_action] pyautogui.keyUp('left alt')")
                pyautogui.keyUp('left alt')
            if right_alt_was_down:
                logger.debug("[_execute_word_action] pyautogui.keyUp('right alt')")
                pyautogui.keyUp('right alt')
            if alt_was_down and not (left_alt_was_down or right_alt_was_down):
                logger.debug("[_execute_word_action] pyautogui.keyUp('alt')")
                pyautogui.keyUp('alt')

            if ctrl_is_down:
                # Same reasoning as _execute_selection: Ctrl is already physically
                # held (word actions also only fire under ctrl+alt), so just send the
                # bare key instead of pyautogui.hotkey('ctrl', key_target), which would
                # add a redundant synthetic ctrl press/release on top of the real one.
                logger.debug(f"[_execute_word_action] ctrl already physically down; sending {key_target!r} only")
                pyautogui.press(key_target)
            else:
                logger.debug(f"[_execute_word_action] ctrl not physically down; pyautogui.hotkey('ctrl', {key_target!r})")
                pyautogui.hotkey('ctrl', key_target)
            
            # Re-check physical states to avoid race conditions
            if left_alt_was_down:
                p_down = self._is_physical_key_down('left alt')
                logger.debug(f"[_execute_word_action] Restoring left alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('left alt')
            if right_alt_was_down:
                p_down = self._is_physical_key_down('right alt')
                logger.debug(f"[_execute_word_action] Restoring right alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('right alt')
            if alt_was_down and not (left_alt_was_down or right_alt_was_down):
                p_down = self._is_physical_key_down('alt')
                logger.debug(f"[_execute_word_action] Restoring generic alt. Still physical down? {p_down}")
                if p_down:
                    pyautogui.keyDown('alt')
                
            self.updateData()
        finally:
            self._during_simulation = False
            logger.debug("[_execute_word_action] END")

    def backspace_word(self):
        self._execute_word_action('backspace')

    def delete_word(self):
        self._execute_word_action('delete')

    def handle_selection_combination(self, *keys):
        for key in keys:
            if key in self.selection_actions:
                self.selection_actions[key]()

    def handle_word_combination(self, *keys):
        for key in keys:
            if key in self.word_actions:
                self.word_actions[key]()

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
        # On Windows, simulated events generated by SendInput/pyautogui 
        # have scan_code = 0, which the keyboard library maps as negative virtual keycodes (-vk).
        # We check event.scan_code < 0 to identify and ignore simulated events.
        is_simulated = (event.scan_code < 0)
        logger.debug(f"[Hook Event] event_type={event.event_type!r}, name={event.name!r}, scan={event.scan_code}, is_simulated={is_simulated}, during_sim={getattr(self, '_during_simulation', False)}")
        if event.event_type == 'down':
            self._last_hook_activity = time.time()
            self.calculate_user_data()
        elif event.event_type == 'up':
            # Check if this is a physical keyUp event for the modifier key (e.g. alt)
            # when we are not actively simulating keypresses inside an action
            if not is_simulated and not getattr(self, '_during_simulation', False):
                if event.name in getattr(self, '_modifier_variants', set()):
                    now = time.time()
                    if now - getattr(self, '_last_safety_release_time', 0) > 0.15:
                        self._last_safety_release_time = now
                        self._during_simulation = True
                        try:
                            logger.debug(f"Physical release of modifier '{event.name}' detected; clearing virtual states.")
                            for var in self._modifier_variants:
                                try:
                                    logger.debug(f"Executing safety release: pyautogui.keyUp({var!r})")
                                    pyautogui.keyUp(var)
                                except Exception as e:
                                    logger.warning(f"Error during safety release of {var}: {e}")
                        finally:
                            self._during_simulation = False

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
        # NOTE: '+' inside a keyboard.add_hotkey() string means "these keys held
        # together", not "in this order" -- the library's own canonicalize()
        # treats 'ctrl+alt' and 'alt+ctrl' as the identical key set. Registering
        # both (and all four orderings of the 3-key variant) used to register the
        # same physical combo multiple times over, so every selection/word action
        # fired once per duplicate on a single keypress. Only the distinct key
        # sets are kept below.
        selection_mods = [
            "ctrl+alt",
            "ctrl+left alt+right alt",
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

        # Word actions (Ctrl + Alt + [;, p] and permutations)
        self.word_actions = {
            self.hk_backspace: self.backspace_word,
            self.hk_delete: self.delete_word
        }
        self.word_action_keys = [k for k in [self.hk_backspace, self.hk_delete] if k]

        for mod_prefix in selection_mods:
            for key in self.word_action_keys:
                keyboard.add_hotkey(f'{mod_prefix}+{key}', self.handle_word_combination, args=(key,), suppress=True)
            for combo in itertools.permutations(self.word_action_keys, 2):
                keyboard.add_hotkey(f'{mod_prefix}+{combo[0]}+{combo[1]}', self.handle_word_combination, args=combo, suppress=True)

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