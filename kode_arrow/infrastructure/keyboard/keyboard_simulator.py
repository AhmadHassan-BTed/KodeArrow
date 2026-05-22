"""Keyboard simulator module for automating keyboard input.

This module provides abstraction for simulating keyboard presses and character input,
wrapping the pyautogui library for cross-platform keyboard automation.
"""

import logging
import pyautogui

logger = logging.getLogger(__name__)


class KeyboardSimulator:
    """Simulates keyboard input for automation and testing.
    
    Provides methods to press individual keys, type text, and perform keyboard
    combinations. Wraps pyautogui functionality with logging and error handling.
    """

    def __init__(self, interval: float = 0.0):
        """Initialize KeyboardSimulator.
        
        Args:
            interval (float, optional): Delay in seconds between key presses.
                Defaults to 0.0 (no delay). Useful for slowing down automation
                on slower systems.
        """
        self.interval = interval
        # Disable pyautogui's failsafe by default during automation
        pyautogui.FAILSAFE = True
        logger.info(f"KeyboardSimulator initialized with interval={interval}s")

    def press(self, key: str) -> bool:
        """Press and release a single key.
        
        Args:
            key (str): The key to press. Can be a single character or key name
                (e.g., 'a', 'enter', 'ctrl', 'shift', 'alt').
                
        Returns:
            bool: True if the key press was successful, False otherwise.
            
        Raises:
            ValueError: If the key name is invalid or unsupported by pyautogui.
        """
        try:
            pyautogui.press(key, interval=self.interval)
            logger.debug(f"Key pressed: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to press key '{key}': {e}")
            return False

    def type_text(self, text: str, interval: float | None = None) -> bool:
        """Type a string of text.
        
        Args:
            text (str): The text to type.
            interval (float | None, optional): Delay between characters in seconds.
                If None, uses the instance's interval setting. Defaults to None.
                
        Returns:
            bool: True if typing was successful, False otherwise.
            
        Raises:
            ValueError: If text contains unsupported characters.
        """
        try:
            effective_interval = interval if interval is not None else self.interval
            pyautogui.write(text, interval=effective_interval)
            logger.debug(f"Text typed: {text[:50]}{'...' if len(text) > 50 else ''}")
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False

    def press_combination(self, *keys: str) -> bool:
        """Press a combination of keys simultaneously (e.g., Ctrl+C).
        
        Keys are pressed in order and then released in reverse order.
        
        Args:
            *keys: Variable number of key names to press in combination.
                Example: press_combination('ctrl', 'c') for Ctrl+C
                
        Returns:
            bool: True if the combination was successful, False otherwise.
            
        Raises:
            ValueError: If any key name is invalid.
        """
        if not keys:
            logger.warning("No keys provided for combination press")
            return False
            
        try:
            # Press all keys in order
            for key in keys:
                pyautogui.keyDown(key)
            
            # Release all keys in reverse order
            for key in reversed(keys):
                pyautogui.keyUp(key)
                
            logger.debug(f"Key combination pressed: {'+'.join(keys)}")
            return True
        except Exception as e:
            logger.error(f"Failed to press key combination {'+'.join(keys)}: {e}")
            return False

    def set_interval(self, interval: float) -> None:
        """Update the delay interval between key presses.
        
        Args:
            interval (float): Delay in seconds between key presses.
        """
        self.interval = interval
        logger.debug(f"Keyboard interval updated to {interval}s")

    def clear_text(self, num_chars: int) -> bool:
        """Delete a specified number of characters using backspace.
        
        Useful for clearing text that was just typed or already in a field.
        
        Args:
            num_chars (int): Number of characters to delete.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if num_chars < 0:
            logger.warning("Cannot clear negative number of characters")
            return False
            
        try:
            for _ in range(num_chars):
                pyautogui.press('backspace', interval=self.interval)
            logger.debug(f"Cleared {num_chars} characters")
            return True
        except Exception as e:
            logger.error(f"Failed to clear text: {e}")
            return False
