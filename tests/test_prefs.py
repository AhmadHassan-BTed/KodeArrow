import sys
import os
import tempfile
import json
import pytest
from unittest.mock import patch

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kode_arrow.config.user_prefs import UserPrefs, DEFAULT_PREFS

def test_default_prefs():
    """Verify that default preferences contain hotkeys, modifier, and theme."""
    assert "hotkeys" in DEFAULT_PREFS
    assert DEFAULT_PREFS["modifier"] == "alt"
    assert DEFAULT_PREFS["theme"] == "light"
    assert DEFAULT_PREFS["hotkeys"]["up"] == "i"

def test_prefs_load_save():
    """Verify loading and saving preferences using a temporary file path."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with patch("kode_arrow.config.user_prefs.PREFS_FILE", tmp_path):
            # Check default behavior when file doesn't exist yet
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            
            loaded = UserPrefs.load()
            assert loaded["modifier"] == "alt"
            assert loaded["theme"] == "light"
            
            # Save custom prefs
            custom = loaded.copy()
            custom["modifier"] = "ctrl"
            custom["theme"] = "dark"
            custom["hotkeys"]["up"] = "w"
            
            success = UserPrefs.save(custom)
            assert success is True
            
            # Load again to verify persistence
            reloaded = UserPrefs.load()
            assert reloaded["modifier"] == "ctrl"
            assert reloaded["theme"] == "dark"
            assert reloaded["hotkeys"]["up"] == "w"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
