#!/bin/sh
set -eu

EXT_DIR="/mnt/us/extensions/molt_display"

trap 'exit 0' INT TERM

while true; do
  sh "$EXT_DIR/bin/run_once.sh"
  SLEEP_SECS=$(python3 - <<'PY'
import random
print(random.randint(2, 5))
PY
)
  sleep "$SLEEP_SECS"
done
