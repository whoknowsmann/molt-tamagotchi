#!/bin/sh
set -eu

EXT_DIR="/mnt/us/extensions/molt_display"

trap 'exit 0' INT TERM

SLEEP_SECS="${SLEEP_SECS:-3}"
if [ -f "$EXT_DIR/config.sh" ]; then
  # shellcheck disable=SC1090
  . "$EXT_DIR/config.sh"
fi

while true; do
  sh "$EXT_DIR/bin/run_once.sh"
  sleep "$SLEEP_SECS"
done
