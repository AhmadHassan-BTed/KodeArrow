import os
import subprocess
import sys
import shutil

def build():
    # Ensure we run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)

    print("Building KodeArrow executable...")

    # Terminate any running instances of KodeArrow to release locks on the target EXE and build directories
    print("Terminating any running instances of KodeArrow.exe...")
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/IM", "KodeArrow.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import time
            time.sleep(1.0)
    except Exception as e:
        print(f"Notice: Failed to run taskkill (may not be active): {e}")

    env_file = os.path.join(project_root, "config", ".env")
    private_env_source = os.path.join(project_root, "private_envs", "KodeArrow.env")
    env_example = os.path.join(project_root, "config", ".env.example")
    
    temp_env_created = False
    
    # Fallback search logic for .env file to prevent build crashes
    if not os.path.exists(env_file):
        if os.path.exists(private_env_source):
            print("config/.env not found, but found private_envs/KodeArrow.env. Copying for the build...")
            os.makedirs(os.path.dirname(env_file), exist_ok=True)
            shutil.copy(private_env_source, env_file)
            temp_env_created = True
        elif os.path.exists(env_example):
            print("config/.env not found. Temporarily copying config/.env.example to proceed with the build.")
            os.makedirs(os.path.dirname(env_file), exist_ok=True)
            shutil.copy(env_example, env_file)
            temp_env_created = True
        else:
            print("Warning: Neither config/.env, private_envs/KodeArrow.env, nor config/.env.example exist!")

    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed", # Hides the console terminal
        "--clean", # Cleans PyInstaller cache to prevent bloat
        "--hidden-import=plyer",
        "--hidden-import=plyer.platforms",
        "--hidden-import=plyer.platforms.win",
        "--hidden-import=plyer.platforms.win.notification",
        "--hidden-import=keyboard",
        "--hidden-import=pyautogui",
        "--hidden-import=pystray",
        "--hidden-import=lucide",
        "--hidden-import=psutil",
        "--hidden-import=wmi",
        "--hidden-import=dotenv",
        "--icon=assets/branding/icon.ico",
        "--add-data=assets/branding/icon.ico;assets/branding",
        "--add-data=config/.env;config",
        "--name=KodeArrow",
        "main.py"
    ]

    try:
        subprocess.check_call(pyinstaller_args)
        print("Build complete! Executable is located in the 'dist' folder.")
        
        # Write KodeArrow.txt release notes to the dist folder dynamically
        dist_dir = os.path.join(project_root, "dist")
        os.makedirs(dist_dir, exist_ok=True)
        txt_file_path = os.path.join(dist_dir, "KodeArrow.txt")
        
        changelog_content = """## KodeArrow v2.5

The Next Evolution in Ergonomics, Performance, and Security. This major update transforms KodeArrow from a static keyboard hook tool into a premium, user-configurable, and highly secure desktop utility. 

This version introduces real-time hotkey remapping, a designer-grade sidebar dashboard, robust portable licensing boundaries, and automated build utilities.

---

## Added

* Home-Row Shortcut Customization:
  - Remap your home-row shortcuts directly from the settings interface (e.g. changing Alt + IJKL).
  - Select your preferred modifier/base key (e.g. `alt`, `ctrl`, `shift`, `windows`) directly from the shortcuts interface to customize your layout.
  - Dynamic hotkey engine reloading—re-binds keys in milliseconds without needing to restart the application.
  - Local preferences are saved securely to '~/.kodearrow_prefs.json' for persistence.
* Universal Community Lifetime Key:
  - Unlock the full premium suite using the creative universal community key 'freeforever@kodearrow.dev'.
  - Bypasses standard 4-device limits to support unlimited active installations.
  - Automatically logs anonymous telemetry stats inside the 'ControlGroup' Firestore collection to support ergonomic research.
* Administrative Registry Tool:
  - New utility 'scripts/add_community_license.py' to cleanly register and manage community keys.
* High-Coverage Test Suite:
  - Dedicated 'tests/test_licensing.py' asserting limit bypass and collection routing boundaries.

---

## Changed

* Secure Portable Licensing:
  - Co-located license status and telemetry keys directly next to the application binary.
  - Eliminates all CWD errors when launched via startup registry or shortcuts, while strictly maintaining secure machine-bound authorization.
* Dynamic Thread-Safe UI Update:
  - Dynamic main-thread refresh (.after()) instantly switches states and hides the Unlock button on success without requiring a reload.
* Unified Visual Palette:
  - Aligned the dashboard accent styles to match the signature rich navy blue (#00207f) of other popup dialogue windows.
* Build Process Termination:
  - Automated process-termination routine terminates background instances of KodeArrow.exe to prevent WinError 5 Permission Denied build crashes.
* Sync scripts:
  - Fully aligned backup/restore scripts with private.envs folder layout.

---

## Hotkeys

| Action              | Default Shortcut           | Configurable? |
| ------------------- | -------------------------- | ------------- |
| Arrow Keys          | Base Key + I / J / K / L   | Yes           |
| Home / End          | Base Key + U / O           | Yes           |
| Delete / Backspace  | Base Key + P / ;           | Yes           |
| Page Up / Page Down | Base Key + [ / '           | Yes           |

---

## Technical Notes

* Input engine based on low-level Win32 keyboard hooks
* Designed for uninterrupted home-row workflows
* Tested across multiple DPI scaling environments

---

## Author

Ahmad Hassan (B-Ted)
"""
        print("Writing KodeArrow.txt to the dist folder...")
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(changelog_content)
        print(f"Successfully wrote {txt_file_path}!")

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
    finally:
        # If we created a temporary env, clean it up to keep the repo clean
        if temp_env_created and os.path.exists(env_file):
            print("Cleaning up temporary config/.env copy...")
            try:
                os.remove(env_file)
            except Exception as e:
                print(f"Failed to clean up temporary config/.env: {e}")

if __name__ == "__main__":
    build()
