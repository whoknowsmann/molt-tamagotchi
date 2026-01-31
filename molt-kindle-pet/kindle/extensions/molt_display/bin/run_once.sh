#!/bin/sh
set -eu

EXT_DIR="/mnt/us/extensions/molt_display"
STATE_JSON="/tmp/molt_state.json"
LAST_TS_FILE="/tmp/molt_last_timestamp"
SCREEN_PATH="/mnt/us/molt_pet/screen.png"

PC_URL="http://127.0.0.1:8000"
if [ -f "$EXT_DIR/config.sh" ]; then
  # shellcheck disable=SC1090
  . "$EXT_DIR/config.sh"
fi

STATE_URL="$PC_URL/state.json"
SCREEN_URL="$PC_URL/screen.png"

fetch_url() {
  if command -v curl >/dev/null 2>&1; then
    curl -s --connect-timeout 3 --max-time 8 "$1" -o "$2"
    return $?
  fi
  if command -v wget >/dev/null 2>&1; then
    wget -q -O "$2" "$1"
    return $?
  fi
  echo "Missing curl/wget; cannot fetch $1" >&2
  return 1
}

extract_timestamp() {
  sed -n 's/.*"timestamp"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$1" | head -n 1
}

fetch_url "$STATE_URL" "$STATE_JSON" || exit 0

TIMESTAMP=$(extract_timestamp "$STATE_JSON")
if [ -z "$TIMESTAMP" ]; then
  TIMESTAMP=0
fi

LAST_TIMESTAMP=0
if [ -f "$LAST_TS_FILE" ]; then
  LAST_TIMESTAMP=$(cat "$LAST_TS_FILE")
fi

if [ "$TIMESTAMP" != "$LAST_TIMESTAMP" ]; then
  mkdir -p "$(dirname "$SCREEN_PATH")"
  if fetch_url "$SCREEN_URL" "$SCREEN_PATH"; then
    echo "$TIMESTAMP" > "$LAST_TS_FILE"
  else
    echo "Failed to fetch screen image" >&2
    exit 0
  fi

  if command -v eips >/dev/null 2>&1; then
    eips -g "$SCREEN_PATH"
  elif command -v fbink >/dev/null 2>&1; then
    fbink -g "$SCREEN_PATH"
  else
    echo "No eips or fbink available to display $SCREEN_PATH" >&2
  fi
fi
