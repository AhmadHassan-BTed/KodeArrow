import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kode_arrow.core.engine import HotkeyEngine

def test_is_physical_key_down():
    engine = HotkeyEngine(is_premium_fn=lambda: True, telemetry_service=MagicMock())
    
    with patch("sys.platform", "win32"), \
         patch("ctypes.windll.user32.GetAsyncKeyState", create=True) as mock_get_async_state:
        
        # Test key pressed (0x8000 bit is set)
        mock_get_async_state.return_value = 0x8000
        assert engine._is_physical_key_down("ctrl") is True
        mock_get_async_state.assert_called_with(0x11)
        
        # Test key not pressed
        mock_get_async_state.return_value = 0
        assert engine._is_physical_key_down("ctrl") is False

def test_is_logical_key_down():
    engine = HotkeyEngine(is_premium_fn=lambda: True, telemetry_service=MagicMock())
    
    with patch("sys.platform", "win32"), \
         patch("keyboard.is_pressed") as mock_kb_pressed, \
         patch("ctypes.windll.user32.GetAsyncKeyState", create=True) as mock_get_async_state:
        
        # Scenario 1: keyboard library says key is pressed.
        # Should return True immediately without calling GetAsyncKeyState
        mock_kb_pressed.return_value = True
        mock_get_async_state.return_value = 0
        assert engine._is_logical_key_down("ctrl") is True
        mock_get_async_state.assert_not_called()
        
        # Scenario 2: keyboard library says False, GetAsyncKeyState says True
        mock_kb_pressed.return_value = False
        mock_get_async_state.return_value = 0x8000
        assert engine._is_logical_key_down("ctrl") is True
        
        # Scenario 3: both say False
        mock_kb_pressed.return_value = False
        mock_get_async_state.return_value = 0
        assert engine._is_logical_key_down("ctrl") is False

def test_safety_release_modifier_groups():
    engine = HotkeyEngine(is_premium_fn=lambda: True, telemetry_service=MagicMock())
    
    # Mock event for physical ctrl key up
    event = MagicMock()
    event.event_type = 'up'
    event.name = 'ctrl'
    event.scan_code = 29  # positive scan code means physical event
    
    with patch("pyautogui.keyUp") as mock_key_up:
        # Simulate physical modifier key up
        engine.increment_total_keyStrokes(event)
        
        # Verify that only ctrl variants are released
        released_keys = [call.args[0] for call in mock_key_up.call_args_list]
        assert "ctrl" in released_keys
        assert "left ctrl" in released_keys
        assert "right ctrl" in released_keys
        assert "alt" not in released_keys
        assert "shift" not in released_keys

