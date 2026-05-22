"""Hotkey action definitions and data classes.

This module defines the HotKeyAction class which represents a single hotkey
and its associated metadata.
"""

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class HotKeyAction:
    """Represents a single hotkey action with its properties.
    
    This data class encapsulates all information about a hotkey including
    its key binding, target action, premium status, and description.
    
    Attributes:
        key (str): The keyboard shortcut key combination (e.g., 'Ctrl+C').
        target (str): The target action or function name (e.g., 'copy_all').
        is_premium (bool): Whether this hotkey requires premium subscription.
        description (str): Human-readable description of what this hotkey does.
    """
    
    key: str
    target: str
    is_premium: bool = False
    description: str = ""

    def __post_init__(self):
        """Validate hotkey action after initialization.
        
        Raises:
            ValueError: If key or target is empty.
        """
        if not self.key or not self.key.strip():
            raise ValueError("Hotkey 'key' cannot be empty")
        if not self.target or not self.target.strip():
            raise ValueError("Hotkey 'target' cannot be empty")
        logger.debug(f"HotKeyAction created: {self.key} -> {self.target}")

    def __str__(self) -> str:
        """String representation of the hotkey action.
        
        Returns:
            str: Formatted string with key, target, and premium status.
        """
        premium_marker = " [PREMIUM]" if self.is_premium else ""
        return f"{self.key}: {self.target}{premium_marker}"

    def __repr__(self) -> str:
        """Detailed representation of the hotkey action.
        
        Returns:
            str: Full representation with all attributes.
        """
        return (f"HotKeyAction(key={self.key!r}, target={self.target!r}, "
                f"is_premium={self.is_premium}, description={self.description!r})")

    def to_dict(self) -> dict:
        """Convert hotkey action to dictionary format.
        
        Returns:
            dict: Dictionary representation of the hotkey action.
        """
        return {
            'key': self.key,
            'target': self.target,
            'is_premium': self.is_premium,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'HotKeyAction':
        """Create HotKeyAction from dictionary.
        
        Args:
            data (dict): Dictionary containing hotkey action data.
            
        Returns:
            HotKeyAction: New instance created from dictionary data.
            
        Raises:
            KeyError: If required keys are missing from data.
            ValueError: If data validation fails.
        """
        try:
            return cls(
                key=data['key'],
                target=data['target'],
                is_premium=data.get('is_premium', False),
                description=data.get('description', '')
            )
        except KeyError as e:
            logger.error(f"Missing required key in hotkey data: {e}")
            raise ValueError(f"Missing required hotkey data: {e}") from e
