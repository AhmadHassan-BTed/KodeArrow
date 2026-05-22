"""Hardware identifier module for secure hardware identification.

This module provides abstraction for obtaining and encrypting hardware identifiers
for licensing and device fingerprinting purposes.
"""

import logging
from ...common.utils.helpers import get_hardware_id, encrypt_hardwareID

logger = logging.getLogger(__name__)


class HardwareIdentifier:
    """Manages hardware identification and encryption.
    
    Provides methods to retrieve the current system's hardware ID and encrypt it
    for secure transmission and storage. Wraps the hardware ID utilities from
    the common helpers module.
    """

    def __init__(self):
        """Initialize HardwareIdentifier.
        
        Raises:
            RuntimeError: If hardware ID cannot be obtained on the current system.
        """
        self._hardware_id = None
        self._encrypted_id = None
        try:
            self._hardware_id = self._get_system_hardware_id()
            logger.info("Hardware identifier initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize hardware identifier: {e}")
            raise RuntimeError(f"Could not obtain hardware ID: {e}") from e

    def _get_system_hardware_id(self) -> str:
        """Retrieve the system's hardware ID.
        
        Returns:
            str: The hardware ID of the current system.
            
        Raises:
            Exception: If hardware ID retrieval fails.
        """
        return get_hardware_id()

    def get_hardware_id(self) -> str:
        """Get the unencrypted hardware ID.
        
        Returns:
            str: The raw hardware ID of the system.
        """
        return self._hardware_id

    def get_encrypted_hardware_id(self) -> str:
        """Get the encrypted hardware ID.
        
        The hardware ID is encrypted using a Caesar cipher with shift of 3.
        This is useful for transmission and basic obfuscation.
        
        Returns:
            str: The encrypted hardware ID. Cached after first call.
        """
        if self._encrypted_id is None:
            self._encrypted_id = encrypt_hardwareID(self._hardware_id)
            logger.debug("Hardware ID encrypted successfully")
        return self._encrypted_id

    def validate_hardware_id(self, expected_id: str) -> bool:
        """Validate if a given hardware ID matches the current system's ID.
        
        Useful for verifying licensing information bound to specific hardware.
        
        Args:
            expected_id (str): The hardware ID to validate against.
            
        Returns:
            bool: True if the provided ID matches the current system's ID, False otherwise.
        """
        is_valid = self._hardware_id == expected_id
        if is_valid:
            logger.info("Hardware ID validation passed")
        else:
            logger.warning("Hardware ID validation failed - ID mismatch")
        return is_valid

    def validate_encrypted_hardware_id(self, expected_encrypted_id: str) -> bool:
        """Validate if an encrypted hardware ID matches the current system's encrypted ID.
        
        Args:
            expected_encrypted_id (str): The encrypted hardware ID to validate against.
            
        Returns:
            bool: True if the encrypted IDs match, False otherwise.
        """
        is_valid = self.get_encrypted_hardware_id() == expected_encrypted_id
        if is_valid:
            logger.info("Encrypted hardware ID validation passed")
        else:
            logger.warning("Encrypted hardware ID validation failed - ID mismatch")
        return is_valid
