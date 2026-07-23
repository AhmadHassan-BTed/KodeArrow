#!/usr/bin/env bash
# =============================================================================
# KodeArrow — Arch Linux / KDE Plasma Input Permission Setup
# =============================================================================
# Grants non-root user access to /dev/input and /dev/uinput via udev rules.
# =============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
    echo "====================================================================="
    echo "Elevating permissions to configure udev rules for KodeArrow..."
    echo "====================================================================="
    exec sudo bash "$0" "$@"
fi

TARGET_USER="${SUDO_USER:-$USER}"

echo "[1/4] Ensuring 'input' and 'uinput' system groups exist..."
groupadd -f input
groupadd -f uinput

echo "[2/4] Adding user '$TARGET_USER' to 'input' and 'uinput' groups..."
usermod -aG input "$TARGET_USER"
usermod -aG uinput "$TARGET_USER" || true

echo "[3/4] Installing udev rules for /dev/input/ and /dev/uinput..."
UDEV_RULE_PATH="/etc/udev/rules.d/99-kodearrow-input.rules"
cat << 'EOF' > "$UDEV_RULE_PATH"
# KodeArrow Input Device Permissions
KERNEL=="uinput", MODE="0660", GROUP="uinput", OPTIONS+="static_node=uinput"
SUBSYSTEM=="input", MODE="0660", GROUP="input"
EOF

chmod 644 "$UDEV_RULE_PATH"

echo "[4/4] Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger --subsystem-match=input || true

echo "====================================================================="
echo "SUCCESS! KodeArrow input permissions configured."
echo "If this is your first time setting this up, please log out and log back"
echo "in (or restart KDE Plasma) for your group memberships to take effect."
echo "====================================================================="
