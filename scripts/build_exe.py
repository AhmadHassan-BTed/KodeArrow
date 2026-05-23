import os
import subprocess
import sys

def build():
    # Ensure we run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)

    print("Building KodeArrow executable...")

    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed", # Hides the console terminal
        "--clean", # Cleans PyInstaller cache to prevent bloat
        "--icon=assets/branding/icon.ico",
        "--add-data=assets/branding/icon.ico;assets/branding",
        "--add-data=config/.env;config",
        "--name=KodeArrow",
        "main.py"
    ]

    try:
        subprocess.check_call(pyinstaller_args)
        print("Build complete! Executable is located in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    build()
