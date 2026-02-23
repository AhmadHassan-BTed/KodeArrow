import os
import platform
import subprocess

def remove_hidden_attribute(file_path):
    try:
        subprocess.check_call(["attrib", "-H", file_path], creationflags=0x08000000)
    except subprocess.CalledProcessError as e:
        pass

def add_hidden_attribute(file_path):
    try:
        subprocess.check_call(["attrib", "+H", file_path], creationflags=0x08000000)
    except subprocess.CalledProcessError as e:
        pass

def create_hidden_file(file_path, content=""):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        
        if platform.system() == "Windows":
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
        elif platform.system() in ["Darwin", "Linux"]:
            if not file_path.startswith('.'):
                dir_name = os.path.dirname(file_path)
                base_name = os.path.basename(file_path)
                os.rename(file_path, os.path.join(dir_name, f".{base_name}"))
    except Exception:
        pass

def write_to_file(file_path, total_keyStrokes, total_shortcuts, total_runtime):
    try:
        remove_hidden_attribute(file_path)
        temp_total_keyStrokes, temp_total_shortcuts, temp_total_runtime = read_from_file(file_path)
        with open(file_path, "w") as file:
            file.write(f"{total_keyStrokes+temp_total_keyStrokes}\n{total_shortcuts+temp_total_shortcuts}\n{total_runtime+temp_total_runtime}\n")
        add_hidden_attribute(file_path)
    except Exception:
        pass

def read_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) != 3:
                raise ValueError("File has an unexpected number of lines.")
            return int(lines[0].strip()), int(lines[1].strip()), float(lines[2].strip())
    except Exception:
        return 0, 0, 0.0

def find_email_in_file(path):
    try:
        with open(path, "r") as file:
            for line in file:
                if line.strip().startswith("Email:"):
                    return line.strip().split("Email:")[1].strip()
    except Exception:
        pass
    return None
