from kode_arrow.input.listener import KeyboardListener
from kode_arrow.input.simulator import KeyboardSimulator

class HotkeyEngine:
    """Manages the mapping of hotkeys to actions and telemetry."""

    def __init__(self, simulator: KeyboardSimulator, is_premium: bool, telemetry=None):
        self.simulator = simulator
        self.is_premium = is_premium
        self.telemetry = telemetry

    def start(self):
        # Register standard hotkeys
        standard_keys = {
            'i': 'up', 'k': 'down', 'j': 'left', 'l': 'right',
            'h': 'delete', 'u': 'backspace'
        }
        for key, target in standard_keys.items():
            self._register_combo(f'capslock+{key}', target, is_premium_required=False)

        # Register extended premium hotkeys
        extended_keys = {
            'u': 'home', 'o': 'end', 'p': 'delete',
            ';': 'backspace', '[': 'pageup', "'": 'pagedown'
        }
        for key, target in extended_keys.items():
            self._register_combo(f'alt+{key}', target, is_premium_required=True)

        if self.telemetry:
            # R-Edition feature: record every key down event
            KeyboardListener.on_press(self._on_key_event)

    def _on_key_event(self, event):
        if getattr(event, "event_type", None) == "down":
            self.telemetry.record_character()

    def _register_combo(self, combo: str, target: str, is_premium_required: bool):
        def handler():
            if is_premium_required and not self.is_premium:
                return # Block if premium required but not active
            self.simulator.press(target)
            if self.telemetry:
                self.telemetry.record_hotkey()

        KeyboardListener.add_hotkey(combo, handler, suppress=True)
