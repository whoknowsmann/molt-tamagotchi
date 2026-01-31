#!/bin/sh
set -eu

EXT_DIR="/mnt/us/extensions/molt_display"
STATE_JSON="/tmp/molt_state.json"
LAST_TS_FILE="/tmp/molt_last_timestamp"

PC_URL="http://127.0.0.1:8000/state.json"
if [ -f "$EXT_DIR/config.sh" ]; then
  # shellcheck disable=SC1090
  . "$EXT_DIR/config.sh"
fi

curl -s --connect-timeout 3 --max-time 5 "$PC_URL" -o "$STATE_JSON" || exit 0

TIMESTAMP=$(python3 - <<'PY'
import json
import sys
with open("/tmp/molt_state.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data.get("timestamp", 0))
PY
)

LAST_TIMESTAMP=0
if [ -f "$LAST_TS_FILE" ]; then
  LAST_TIMESTAMP=$(cat "$LAST_TS_FILE")
fi

if [ "$TIMESTAMP" != "$LAST_TIMESTAMP" ]; then
  echo "$TIMESTAMP" > "$LAST_TS_FILE"
  python3 "/mnt/us/molt-kindle-pet/kindle/renderer/render.py" "$STATE_JSON"
fi
