import sys
import os

def get_resource_path(relative_path):
    """ 
    Get absolute path to resource.
    Works for standard development and for PyInstaller bundled executables.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In development, the base path is the project root (2 levels up from this file)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, relative_path)
