def encrypt_hardware_id(s):
    encrypted_chars = []
    for char in s:
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
