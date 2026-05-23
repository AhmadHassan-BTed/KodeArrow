"""Encryption utilities for hardware IDs and sensitive data."""

def encrypt_hardware_id(hardware_id: str) -> str:
    """Encrypt hardware ID using Caesar cipher (shift 3).

    Args:
        hardware_id: The hardware ID to encrypt

    Returns:
        The encrypted hardware ID
    """
    encrypted_chars = []
    for char in hardware_id:
        if char.isalnum():
            if char.isalpha():
                if char.isupper():
                    new_char_code = (ord(char) - ord('A') + 3) % 26 + ord('A')
                    encrypted_chars.append(chr(new_char_code))
                else:
                    new_char_code = (ord(char) - ord('a') + 3) % 26 + ord('a')
                    encrypted_chars.append(chr(new_char_code))
            else:
                new_char_code = (ord(char) - ord('0') + 3) % 10 + ord('0')
                encrypted_chars.append(chr(new_char_code))
    return ''.join(encrypted_chars)
