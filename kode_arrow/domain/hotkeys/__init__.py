"""Hotkeys domain module.

Handles hotkey definitions, management, and execution. This module provides
classes and utilities for managing keyboard hotkeys, their configurations,
and registry operations.

Main exports:
    - HotKeyAction: Data class representing a single hotkey
    - HotKeyRegistry: Singleton registry for managing hotkeys
    - HotKeyConfiguration: Static configuration for hotkey sets
"""

from .hotkey_action import HotKeyAction
from .hotkey_registry import HotKeyRegistry
from .hotkey_configuration import HotKeyConfiguration

__all__ = [
    'HotKeyAction',
    'HotKeyRegistry',
    'HotKeyConfiguration',
]
