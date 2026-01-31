#!/bin/sh
set -eu

EXT_DIR="/mnt/us/extensions/molt_display"
PID_FILE="/tmp/molt_display.pid"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Molt Pet already running"
  exit 0
fi

sh "$EXT_DIR/bin/loop.sh" >/tmp/molt_display.log 2>&1 &

echo $! > "$PID_FILE"

echo "Molt Pet started"
