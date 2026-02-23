import keyboard as _keyboard

class KeyboardListener:
    """Wraps the global keyboard hook library to register hotkeys."""

    @staticmethod
    def add_hotkey(hotkey: str, callback, suppress: bool = True) -> None:
        _keyboard.add_hotkey(hotkey, callback, suppress=suppress)

    @staticmethod
    def on_press(callback) -> None:
        _keyboard.on_press(callback)
