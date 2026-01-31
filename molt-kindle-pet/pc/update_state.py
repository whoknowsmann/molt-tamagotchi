from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent / "state.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Molt state.json and bump timestamp.")
    parser.add_argument("--state", help="State name (idle, alert, thinking, talking, excited, sleeping, error)")
    parser.add_argument("--text", help="Message to display")
    args = parser.parse_args()

    if STATE_PATH.exists():
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    else:
        data = {"state": "idle", "text": ""}

    if args.state is not None:
        data["state"] = args.state
    if args.text is not None:
        data["text"] = args.text

    data["timestamp"] = int(time.time())
    STATE_PATH.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
