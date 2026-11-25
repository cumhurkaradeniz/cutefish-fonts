#!/bin/bash
set -e
if command -v apt >/dev/null 2>&1; then
    sudo apt update && sudo apt install -y python3 python3-pyqt5 fontconfig
elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-qt5 fontconfig
elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --noconfirm python python-pyqt5 fontconfig
fi
APP_DIR="$HOME/.local/share/cutefish-fonts"
mkdir -p "$APP_DIR" "$HOME/.local/share/applications"
cp app.py font_mgr.py i18n.py icon.png "$APP_DIR/"
cat << DESKTOP > "$HOME/.local/share/applications/cutefish-fonts.desktop"
[Desktop Entry]
Name=Cutefish Fonts
Comment=Modern Font Manager & Open-Source Font Catalog for Linux
Exec=python3 $APP_DIR/app.py
Icon=$APP_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;Graphics;
StartupWMClass=cutefish-fonts
DESKTOP
echo "Cutefish Fonts kuruldu!"
