import sys
import os
import pytest

# Ensure project root is in the path for enterprise-wide discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kode_arrow.infrastructure.security.encryption import encrypt_hardware_id

def test_encryption_logic():
    """Validates the core Caesar-style hardware ID encryption."""
    assert encrypt_hardware_id("ABC") == "DEF"
    assert encrypt_hardware_id("xyz") == "abc"
    assert encrypt_hardware_id("123") == "456"

def test_encryption_alphanumeric():
    """Ensures alphanumeric characters are correctly shifted."""
    assert encrypt_hardware_id("A1z") == "D4c"

def test_encryption_non_alphanumeric():
    """Verifies that non-alphanumeric characters are safely ignored by the cipher."""
    assert encrypt_hardware_id("A!1") == "D4"
