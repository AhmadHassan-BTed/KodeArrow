import sys
import os

def get_resource_path(relative_path):
    """ 
    Get absolute path to resource.
    Works for standard development and for PyInstaller bundled executables.
    Handles case differences (Assets vs assets) and extension fallbacks (.ico vs .png) on Linux.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In development, the base path is the project root (2 levels up from this file)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    full_path = os.path.join(base_path, relative_path)
    if os.path.exists(full_path):
        return full_path

    # Case fallback e.g. Assets vs assets
    parts = os.path.normpath(relative_path).split(os.sep)
    if parts:
        first_dir = parts[0]
        alt_dir = 'Assets' if first_dir.lower() == 'assets' and first_dir != 'Assets' else 'assets'
        alt_relative = os.path.join(alt_dir, *parts[1:])
        alt_full_path = os.path.join(base_path, alt_relative)
        if os.path.exists(alt_full_path):
            return alt_full_path

        # Extension fallback (.ico -> .png)
        if relative_path.endswith(".ico"):
            png_relative = relative_path[:-4] + ".png"
            png_full_path = os.path.join(base_path, png_relative)
            if os.path.exists(png_full_path):
                return png_full_path
            alt_png = os.path.join(base_path, alt_dir, *parts[1:])[:-4] + ".png"
            if os.path.exists(alt_png):
                return alt_png

    return full_path


def set_window_icon(app, relative_path=None):
    """
    Safely sets a Tkinter / CustomTkinter window icon for Windows and Linux.
    """
    if relative_path is None:
        relative_path = os.path.join('Assets', 'branding', 'icon.ico')

    icon_path = get_resource_path(relative_path)
    if not os.path.exists(icon_path):
        return

    try:
        if sys.platform == "win32":
            app.iconbitmap(icon_path)
        else:
            from PIL import Image, ImageTk
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            app.iconphoto(True, photo)
            app._icon_photo_ref = photo
    except Exception:
        pass

