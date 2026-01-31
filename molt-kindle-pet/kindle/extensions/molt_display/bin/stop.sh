#!/bin/sh
set -eu

PID_FILE="/tmp/molt_display.pid"

if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Stopped Molt Pet"
  fi
  rm -f "$PID_FILE"
else
  echo "No running Molt Pet process"
fi
