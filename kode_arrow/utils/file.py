import os
import platform

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
