#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
EXT_SRC="$SCRIPT_DIR/extensions/molt_display"
EXT_DEST="/mnt/us/extensions/molt_display"

mkdir -p "$EXT_DEST"
cp -r "$EXT_SRC"/* "$EXT_DEST"/

echo "Installed KUAL extension to $EXT_DEST"
