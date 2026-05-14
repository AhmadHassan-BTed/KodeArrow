import os
import subprocess
import sys
import shutil

def build():
    # Ensure we run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)

    print("Building KodeArrow executable...")

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
        "--hidden-import=plyer.platforms.win.notification",
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
