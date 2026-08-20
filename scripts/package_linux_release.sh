#!/usr/bin/env bash
# =============================================================================
# KodeArrow — Production Release Packager for Linux
# =============================================================================
# Creates a standalone lightweight distribution bundle (zip / tar.gz) for Linux
# end-users so they don't need to download or clone the whole source repository.
# =============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${PROJECT_DIR}/dist/KodeArrow_Linux"
ZIP_OUT="${PROJECT_DIR}/dist/KodeArrow_for_linux.zip"

echo "[1/4] Preparing release directory: ${DIST_DIR}"
rm -rf "${DIST_DIR}" "${ZIP_OUT}"
mkdir -p "${DIST_DIR}"

echo "[2/4] Copying installer scripts and configurations..."
cp "${PROJECT_DIR}/scripts/kodearrow" "${DIST_DIR}/kodearrow"
chmod +x "${DIST_DIR}/kodearrow"

cp "${PROJECT_DIR}/config/kodearrow.conf" "${DIST_DIR}/kodearrow.conf"

if [ -f "${PROJECT_DIR}/Assets/branding/icon.png" ]; then
    cp "${PROJECT_DIR}/Assets/branding/icon.png" "${DIST_DIR}/logo.png"
elif [ -f "${PROJECT_DIR}/Assets/branding/logo.png" ]; then
    cp "${PROJECT_DIR}/Assets/branding/logo.png" "${DIST_DIR}/logo.png"
fi

echo "[3/4] Generating standalone user README..."
cat << 'EOF' > "${DIST_DIR}/README.md"
# KodeArrow for Linux

Home-row navigation hotkeys for Arch Linux / KDE Plasma.

## Quick Start

1. **Install Hotkeys (One-Time Setup)**:
   ```bash
   chmod +x kodearrow
   sudo ./kodearrow
   ```
   *Installs keyd and activates Alt+IJKL, Alt+UO, Alt+P/;, Ctrl+Alt+Selection hotkeys kernel-wide.*

2. **Run System Tray Icon**:
   ```bash
   python3 kodearrow-tray.py
   ```

3. **Start automatically on login**:
   ```bash
   python3 kodearrow-tray.py --install-autostart
   ```

4. **Uninstall / Remove Hotkeys**:
   ```bash
   sudo ./kodearrow --remove
   ```

Official Website: https://ahmadhassan-bted.github.io/KodeArrow/
EOF

# Copy tray script
if [ -f "${PROJECT_DIR}/tmp_linux_extracted/KodeArrow/kodearrow-tray.py" ]; then
    cp "${PROJECT_DIR}/tmp_linux_extracted/KodeArrow/kodearrow-tray.py" "${DIST_DIR}/kodearrow-tray.py"
else
    cat << 'EOF' > "${DIST_DIR}/kodearrow-tray.py"
#!/usr/bin/env python3
"""
KodeArrow Tray Application
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICON_PATH = HERE / "logo.png"
GITHUB_URL = "https://github.com/AhmadHassan-BTed/KodeArrow"
AUTOSTART_FILE = Path.home() / ".config" / "autostart" / "kodearrow-tray.desktop"

def install_autostart():
    AUTOSTART_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUTOSTART_FILE.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=KodeArrow Tray\n"
        f"Exec=python3 {Path(__file__).resolve()}\n"
        f"Icon={ICON_PATH}\n"
        "Terminal=false\n"
        "X-GNOME-Autostart-enabled=true\n"
        "Comment=KodeArrow navigation hotkeys tray icon\n"
    )
    print(f"Autostart entry created: {AUTOSTART_FILE}")

def remove_autostart():
    if AUTOSTART_FILE.exists():
        AUTOSTART_FILE.unlink()
        print(f"Removed {AUTOSTART_FILE}")

def run_tray():
    try:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QAction, QDesktopServices, QIcon
        from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon
    except ImportError:
        print("PySide6 required for tray icon. Install with: sudo pacman -S pyside6", file=sys.stderr)
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("No system tray detected in this session.", file=sys.stderr)
        sys.exit(1)

    icon = QIcon(str(ICON_PATH)) if ICON_PATH.exists() else app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
    tray = QSystemTrayIcon(icon)
    tray.setToolTip("KodeArrow — Navigation Hotkeys Active")

    menu = QMenu()
    visit_action = QAction("Visit / Contribute on GitHub", menu)
    visit_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
    menu.addAction(visit_action)

    menu.addSeparator()

    def do_exit():
        tray.hide()
        app.quit()

    exit_action = QAction("Exit", menu)
    exit_action.triggered.connect(do_exit)
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    if "--install-autostart" in sys.argv:
        install_autostart()
    elif "--remove-autostart" in sys.argv:
        remove_autostart()
    else:
        run_tray()
EOF
fi

chmod +x "${DIST_DIR}/kodearrow-tray.py"

echo "[4/4] Creating distribution zip: ${ZIP_OUT}"
cd "${PROJECT_DIR}/dist"
zip -r "${ZIP_OUT}" "KodeArrow_Linux"

echo "====================================================================="
echo "SUCCESS! Production release zip generated at:"
echo "  ${ZIP_OUT}"
echo "====================================================================="
