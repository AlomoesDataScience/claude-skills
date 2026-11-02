#!/bin/sh
# Adds Sprite Studio to the applications menu, pointing at this folder.
# Run it again if you move the folder. Remove the entry with:
#   rm ~/.local/share/applications/sprite-studio.desktop
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
cat > "$APPS/sprite-studio.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Sprite Studio
Comment=Dominions 6 sprite editor
Exec="$HERE/SpriteStudio"
Icon=$HERE/icon.png
Path=$HERE
Terminal=false
Categories=Graphics;2DGraphics;
EOF
chmod +x "$APPS/sprite-studio.desktop"
echo "Added Sprite Studio to the menu ($APPS/sprite-studio.desktop)."
