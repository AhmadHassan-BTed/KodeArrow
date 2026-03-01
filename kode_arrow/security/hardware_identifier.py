import platform
import subprocess

def get_hardware_id():
    system = platform.system()
    if system == "Windows":
        try:
            import wmi
        except ImportError as exc:
            raise ImportError(
                "The 'wmi' package is required on Windows to read hardware IDs. "
                "Install it with 'pip install wmi' or use the project's requirements.txt."
            ) from exc

        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        return bios.SerialNumber
    elif system == "Darwin":  # macOS
        command = "ioreg -l | grep IOPlatformSerialNumber"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        serial_number = result.stdout.split('=')[-1].strip().strip('"')
        return serial_number
    elif system == "Linux":
        command = "cat /sys/class/dmi/id/product_uuid"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        raise NotImplementedError(f"Unsupported platform: {system}")
