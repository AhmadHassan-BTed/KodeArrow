"""Shim for backward compatibility. 
These utilities have been moved to infrastructure."""
from kode_arrow.infrastructure.security.hardware_identifier import get_hardware_id
from kode_arrow.infrastructure.security.encryption import encrypt_hardware_id as encrypt_hardwareID
from kode_arrow.infrastructure.storage.file_utils import create_hidden_file

__all__ = ["get_hardware_id", "encrypt_hardwareID", "create_hidden_file"]
