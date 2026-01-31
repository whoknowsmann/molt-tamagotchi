#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
EXT_SRC="$SCRIPT_DIR/extensions/molt_display"
EXT_DEST="/mnt/us/extensions/molt_display"
SCREEN_DIR="/mnt/us/molt_pet"

mkdir -p "$EXT_DEST"
cp -r "$EXT_SRC"/* "$EXT_DEST"/
chmod +x "$EXT_DEST"/bin/*.sh
mkdir -p "$SCREEN_DIR"

echo "Installed KUAL extension to $EXT_DEST"
