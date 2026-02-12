import platform
import subprocess
import wmi
import os

def get_hardware_id():
    system = platform.system()
    if system == "Windows":
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        return bios.SerialNumber
    elif system == "Darwin":
        command = "ioreg -l | grep IOPlatformSerialNumber"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        serial_number = result.stdout.split('=')[-1].strip().strip('"')
        return serial_number
    elif system == "Linux":
        command = "cat /sys/class/dmi/id/product_uuid"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    return "UNKNOWN"

def encrypt_hardwareID(s):
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

def create_hidden_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        
        if platform.system() == "Windows":
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
        elif platform.system() in ["Darwin", "Linux"]:
            if not os.path.basename(file_path).startswith('.'):
                new_path = os.path.join(os.path.dirname(file_path), f".{os.path.basename(file_path)}")
                os.rename(file_path, new_path)
    except Exception:
        pass
