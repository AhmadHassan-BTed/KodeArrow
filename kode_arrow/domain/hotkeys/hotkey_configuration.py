"""Hotkey configuration management.

This module provides static configuration for standard, premium, and extended
hotkey sets used throughout the application.
"""

import logging
from typing import Dict, List
from .hotkey_action import HotKeyAction

logger = logging.getLogger(__name__)


class HotKeyConfiguration:
    """Static configuration for application hotkeys.
    
    This class provides predefined hotkey configurations for different
    subscription editions (standard, premium, extended). It can be used to
    initialize the hotkey registry with standard sets of hotkeys.
    """

    # Standard edition hotkeys (always available)
    DEFAULT_HOTKEYS: Dict[str, HotKeyAction] = {
        'Ctrl+Alt+A': HotKeyAction(
            key='Ctrl+Alt+A',
            target='autocomplete_all',
            is_premium=False,
            description='Autocomplete all selections on current line'
        ),
        'Ctrl+Alt+C': HotKeyAction(
            key='Ctrl+Alt+C',
            target='copy_all_completions',
            is_premium=False,
            description='Copy all autocomplete suggestions'
        ),
        'Ctrl+Alt+D': HotKeyAction(
            key='Ctrl+Alt+D',
            target='duplicate_line',
            is_premium=False,
            description='Duplicate current line'
        ),
        'Ctrl+Alt+E': HotKeyAction(
            key='Ctrl+Alt+E',
            target='expand_selection',
            is_premium=False,
            description='Expand selection to word boundary'
        ),
        'Ctrl+Alt+L': HotKeyAction(
            key='Ctrl+Alt+L',
            target='format_code',
            is_premium=False,
            description='Format code in current selection'
        ),
    }

    # Premium edition hotkeys (require active subscription)
    PREMIUM_HOTKEYS: Dict[str, HotKeyAction] = {
        'Ctrl+Alt+R': HotKeyAction(
            key='Ctrl+Alt+R',
            target='refactor_selection',
            is_premium=True,
            description='Advanced code refactoring'
        ),
        'Ctrl+Alt+T': HotKeyAction(
            key='Ctrl+Alt+T',
            target='generate_tests',
            is_premium=True,
            description='Generate unit tests from selected code'
        ),
        'Ctrl+Alt+O': HotKeyAction(
            key='Ctrl+Alt+O',
            target='optimize_code',
            is_premium=True,
            description='Optimize code performance'
        ),
        'Ctrl+Alt+S': HotKeyAction(
            key='Ctrl+Alt+S',
            target='suggest_improvements',
            is_premium=True,
            description='Get AI suggestions for improvement'
        ),
        'Ctrl+Alt+P': HotKeyAction(
            key='Ctrl+Alt+P',
            target='profile_code',
            is_premium=True,
            description='Profile code execution and performance'
        ),
    }

    # Extended edition hotkeys (maximum features)
    EXTENDED_HOTKEYS: Dict[str, HotKeyAction] = {
        'Ctrl+Alt+V': HotKeyAction(
            key='Ctrl+Alt+V',
            target='visual_debug',
            is_premium=True,
            description='Visual debugging with breakpoints'
        ),
        'Ctrl+Alt+G': HotKeyAction(
            key='Ctrl+Alt+G',
            target='generate_docs',
            is_premium=True,
            description='Generate documentation from code'
        ),
        'Ctrl+Alt+M': HotKeyAction(
            key='Ctrl+Alt+M',
            target='code_metrics',
            is_premium=True,
            description='Analyze code metrics and complexity'
        ),
        'Ctrl+Alt+I': HotKeyAction(
            key='Ctrl+Alt+I',
            target='ai_review',
            is_premium=True,
            description='AI-powered code review'
        ),
    }

    @classmethod
    def get_standard_hotkeys(cls) -> Dict[str, HotKeyAction]:
        """Get standard edition hotkeys.
        
        Returns:
            Dict[str, HotKeyAction]: Dictionary of standard hotkeys.
        """
        return cls.DEFAULT_HOTKEYS.copy()

    @classmethod
    def get_premium_hotkeys(cls) -> Dict[str, HotKeyAction]:
        """Get premium edition hotkeys.
        
        Returns:
            Dict[str, HotKeyAction]: Dictionary of premium hotkeys.
        """
        return cls.PREMIUM_HOTKEYS.copy()

    @classmethod
    def get_extended_hotkeys(cls) -> Dict[str, HotKeyAction]:
        """Get extended edition hotkeys.
        
        Returns:
            Dict[str, HotKeyAction]: Dictionary of extended hotkeys.
        """
        return cls.EXTENDED_HOTKEYS.copy()

    @classmethod
    def get_all_hotkeys(cls) -> Dict[str, HotKeyAction]:
        """Get all available hotkeys combined.
        
        Returns:
            Dict[str, HotKeyAction]: Dictionary of all hotkeys.
        """
        all_hotkeys = {}
        all_hotkeys.update(cls.DEFAULT_HOTKEYS)
        all_hotkeys.update(cls.PREMIUM_HOTKEYS)
        all_hotkeys.update(cls.EXTENDED_HOTKEYS)
        return all_hotkeys

    @classmethod
    def get_hotkeys_for_edition(cls, edition: str) -> Dict[str, HotKeyAction]:
        """Get hotkeys for a specific edition.
        
        Args:
            edition (str): The edition name: 'standard', 'premium', or 'extended'.
            
        Returns:
            Dict[str, HotKeyAction]: Dictionary of hotkeys for the specified edition.
            
        Raises:
            ValueError: If edition is not recognized.
        """
        edition = edition.lower().strip()
        
        if edition == 'standard':
            return cls.get_standard_hotkeys()
        elif edition == 'premium':
            hotkeys = cls.get_standard_hotkeys()
            hotkeys.update(cls.get_premium_hotkeys())
            return hotkeys
        elif edition == 'extended':
            return cls.get_all_hotkeys()
        else:
            logger.error(f"Unknown edition: {edition}")
            raise ValueError(f"Unknown edition: {edition}. "
                           f"Must be 'standard', 'premium', or 'extended'.")

    @classmethod
    def get_new_hotkeys_for_upgrade(cls, 
                                    from_edition: str, 
                                    to_edition: str) -> Dict[str, HotKeyAction]:
        """Get hotkeys that are unlocked when upgrading editions.
        
        Args:
            from_edition (str): Current edition.
            to_edition (str): Target edition after upgrade.
            
        Returns:
            Dict[str, HotKeyAction]: Dictionary of newly unlocked hotkeys.
            
        Raises:
            ValueError: If editions are not recognized.
        """
        current = cls.get_hotkeys_for_edition(from_edition)
        target = cls.get_hotkeys_for_edition(to_edition)
        
        new_hotkeys = {k: v for k, v in target.items() if k not in current}
        logger.info(f"Upgrade from {from_edition} to {to_edition}: "
                   f"{len(new_hotkeys)} new hotkeys unlocked")
        return new_hotkeys

    @classmethod
    def validate_hotkey_config(cls) -> bool:
        """Validate hotkey configuration for consistency.
        
        Checks for duplicate keys, empty configurations, and other issues.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        all_keys = set()
        
        for hotkey_dict in [cls.DEFAULT_HOTKEYS, cls.PREMIUM_HOTKEYS, cls.EXTENDED_HOTKEYS]:
            for key, action in hotkey_dict.items():
                if key in all_keys:
                    logger.error(f"Duplicate hotkey key found: {key}")
                    return False
                all_keys.add(key)
                
                if not key or not action.target:
                    logger.error(f"Invalid hotkey found: key={key}, target={action.target}")
                    return False
        
        logger.info(f"Hotkey configuration valid: {len(all_keys)} unique hotkeys")
        return True

    @classmethod
    def get_config_summary(cls) -> Dict[str, int]:
        """Get summary of configuration counts.
        
        Returns:
            Dict[str, int]: Dictionary with counts of each hotkey type.
        """
        return {
            'standard': len(cls.DEFAULT_HOTKEYS),
            'premium': len(cls.PREMIUM_HOTKEYS),
            'extended': len(cls.EXTENDED_HOTKEYS),
            'total': len(cls.get_all_hotkeys())
        }
