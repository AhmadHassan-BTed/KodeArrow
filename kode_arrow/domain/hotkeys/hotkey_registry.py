"""Hotkey registry for managing hotkey definitions and lookup.

This module provides a central registry for all hotkeys in the application,
allowing registration, lookup, and management of hotkey actions.
"""

import logging
from typing import Dict, List, Optional
from .hotkey_action import HotKeyAction

logger = logging.getLogger(__name__)


class HotKeyRegistry:
    """Registry for managing hotkey definitions.
    
    This class provides a singleton-like registry for hotkeys, allowing
    applications to register, retrieve, and manage hotkey actions in a
    centralized location.
    
    Attributes:
        _hotkeys (Dict[str, HotKeyAction]): Internal dictionary storing hotkeys.
    """
    
    _instance: Optional['HotKeyRegistry'] = None

    def __new__(cls):
        """Implement singleton pattern.
        
        Returns:
            HotKeyRegistry: The singleton instance of HotKeyRegistry.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the hotkey registry."""
        if self._initialized:
            return
        self._hotkeys: Dict[str, HotKeyAction] = {}
        self._initialized = True
        logger.info("HotKeyRegistry initialized")

    def register_hotkey(self, action: HotKeyAction) -> bool:
        """Register a new hotkey action.
        
        Args:
            action (HotKeyAction): The hotkey action to register.
            
        Returns:
            bool: True if registration successful, False if key already exists.
            
        Raises:
            TypeError: If action is not a HotKeyAction instance.
        """
        if not isinstance(action, HotKeyAction):
            logger.error(f"Invalid action type: {type(action)}")
            raise TypeError(f"Expected HotKeyAction, got {type(action)}")
        
        if action.key in self._hotkeys:
            logger.warning(f"Hotkey '{action.key}' already registered")
            return False
        
        self._hotkeys[action.key] = action
        logger.info(f"Registered hotkey: {action.key} -> {action.target}")
        return True

    def register_hotkeys(self, actions: List[HotKeyAction]) -> int:
        """Register multiple hotkey actions.
        
        Args:
            actions (List[HotKeyAction]): List of hotkey actions to register.
            
        Returns:
            int: Number of hotkeys successfully registered.
        """
        count = 0
        for action in actions:
            if self.register_hotkey(action):
                count += 1
        logger.info(f"Registered {count} hotkeys")
        return count

    def unregister_hotkey(self, key: str) -> bool:
        """Unregister a hotkey action.
        
        Args:
            key (str): The hotkey key to unregister.
            
        Returns:
            bool: True if unregistration successful, False if key not found.
        """
        if key not in self._hotkeys:
            logger.warning(f"Hotkey '{key}' not found in registry")
            return False
        
        del self._hotkeys[key]
        logger.info(f"Unregistered hotkey: {key}")
        return True

    def get_hotkey(self, key: str) -> Optional[HotKeyAction]:
        """Retrieve a hotkey action by key.
        
        Args:
            key (str): The hotkey key to retrieve.
            
        Returns:
            Optional[HotKeyAction]: The hotkey action if found, None otherwise.
        """
        return self._hotkeys.get(key)

    def list_hotkeys(self) -> List[HotKeyAction]:
        """Get all registered hotkey actions.
        
        Returns:
            List[HotKeyAction]: List of all registered hotkey actions.
        """
        return list(self._hotkeys.values())

    def list_hotkeys_by_premium(self, is_premium: bool) -> List[HotKeyAction]:
        """Get hotkeys filtered by premium status.
        
        Args:
            is_premium (bool): Filter for premium hotkeys (True) or standard (False).
            
        Returns:
            List[HotKeyAction]: List of hotkeys matching the premium status.
        """
        return [action for action in self._hotkeys.values() 
                if action.is_premium == is_premium]

    def list_standard_hotkeys(self) -> List[HotKeyAction]:
        """Get all standard (non-premium) hotkeys.
        
        Returns:
            List[HotKeyAction]: List of standard hotkey actions.
        """
        return self.list_hotkeys_by_premium(False)

    def list_premium_hotkeys(self) -> List[HotKeyAction]:
        """Get all premium hotkeys.
        
        Returns:
            List[HotKeyAction]: List of premium hotkey actions.
        """
        return self.list_hotkeys_by_premium(True)

    def get_hotkey_by_target(self, target: str) -> Optional[HotKeyAction]:
        """Get a hotkey by its target action name.
        
        Args:
            target (str): The target action name to search for.
            
        Returns:
            Optional[HotKeyAction]: The first hotkey with matching target, or None.
        """
        for action in self._hotkeys.values():
            if action.target == target:
                return action
        return None

    def hotkey_exists(self, key: str) -> bool:
        """Check if a hotkey key is registered.
        
        Args:
            key (str): The hotkey key to check.
            
        Returns:
            bool: True if the hotkey is registered, False otherwise.
        """
        return key in self._hotkeys

    def count_hotkeys(self) -> int:
        """Get total number of registered hotkeys.
        
        Returns:
            int: Total count of registered hotkeys.
        """
        return len(self._hotkeys)

    def clear_all(self) -> None:
        """Clear all registered hotkeys.
        
        WARNING: This will remove all hotkeys from the registry.
        """
        count = len(self._hotkeys)
        self._hotkeys.clear()
        logger.warning(f"Cleared all {count} hotkeys from registry")

    def to_dict(self) -> Dict[str, dict]:
        """Export all hotkeys as dictionary.
        
        Returns:
            Dict[str, dict]: Dictionary representation of all hotkeys.
        """
        return {key: action.to_dict() for key, action in self._hotkeys.items()}
