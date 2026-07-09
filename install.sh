#!/bin/bash

set -e

echo "Installing FocusDeck..."

INSTALL_DIR="$HOME/.local/share/focusdeck"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

mkdir -p "$INSTALL_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

echo "Downloading FocusDeck binary..."

curl -L \
https://github.com/sm4006/FOCUSDECK/releases/download/v1.0.1/FocusDeck \
-o "$INSTALL_DIR/FocusDeck"

chmod +x "$INSTALL_DIR/FocusDeck"

echo "Downloading icon..."

curl -L \
https://raw.githubusercontent.com/sm4006/FOCUSDECK/main/Logos/focusdeck_logo_oled.png \
-o "$ICON_DIR/focusdeck.png"

cat > "$APP_DIR/focusdeck.desktop" << EOF
[Desktop Entry]
Type=Application
Name=FocusDeck
Exec=$INSTALL_DIR/FocusDeck
Icon=focusdeck
Terminal=false
Categories=Utility;
EOF

echo "FocusDeck installed successfully."
echo "Press Super and search for: FocusDeck"
