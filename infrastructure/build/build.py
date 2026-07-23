import os
import subprocess
import shutil
import sys

def build_edition(edition, entry_point):
    """Builds a specific edition of KodeArrow using PyInstaller for production distribution."""
    print(f"--- Starting Build: {edition} on {sys.platform} ---")
    
    # Path setup
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dist_dir = os.path.join(root_dir, "dist", edition)
    work_dir = os.path.join(root_dir, "build", "temp", edition)
    icon_path = os.path.join(root_dir, "assets", "branding", "icon.ico")
    
    # Ensure clean directories
    if os.path.exists(dist_dir): shutil.rmtree(dist_dir)
    if os.path.exists(work_dir): shutil.rmtree(work_dir)
    
    # PyInstaller add-data path separator: ':' on Linux/macOS, ';' on Windows
    sep = os.pathsep
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--name=KodeArrow_{edition}",
        f"--workpath={work_dir}",
        f"--distpath={dist_dir}",
        f"--add-data=assets/branding/icon.ico{sep}assets/branding",
    ]
    
    if os.path.exists(os.path.join(root_dir, "config", ".env")):
        cmd.append(f"--add-data=config/.env{sep}config")
        
    if sys.platform == "win32" and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
        
    cmd.append(entry_point)
    
    try:
        subprocess.run(cmd, check=True, cwd=root_dir)
        exe_name = f"KodeArrow_{edition}.exe" if sys.platform == "win32" else f"KodeArrow_{edition}"
        print(f"--- Successfully Built: {edition} ---")
        print(f"Production binary located at: {os.path.join(dist_dir, exe_name)}")
    except subprocess.CalledProcessError as e:
        print(f"Error building {edition}: {e}")
        sys.exit(1)


def main():
    # Build Standard Edition
    build_edition("Standard", "main.py")
    
    # Optional: Build R-Edition separately if needed, 
    # though main.py handles both via CLI flags.
    # To build a dedicated R-Edition exe:
    # build_edition("REdition", "core/versions/r_edition/main.py")

if __name__ == "__main__":
    main()
