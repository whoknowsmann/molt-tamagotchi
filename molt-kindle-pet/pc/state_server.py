from __future__ import annotations

import http.server
import json
import os
import time
from pathlib import Path
from typing import Any

from renderer import render_png_bytes

STATE_PATH = Path(__file__).resolve().parent / "state.json"
HOST = "0.0.0.0"
PORT = int(os.environ.get("MOLT_PORT", "8000"))

_cached_timestamp: int | None = None
_cached_png: bytes | None = None


def _read_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"state": "idle", "text": "", "timestamp": int(time.time())}

    with STATE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_state(data: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _state_etag(state: dict[str, Any]) -> str:
    timestamp = state.get("timestamp", 0)
    return f'W/"{timestamp}"'


class StateHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("ETag", _state_etag(payload))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path == "/state.json":
            state = _read_state()
            self._send_json(state)
            return

        if self.path == "/screen.png":
            state = _read_state()
            self._send_screen(state)
            return

        self.send_error(404, "Not Found")

    def _send_screen(self, state: dict[str, Any]) -> None:
        global _cached_png, _cached_timestamp

        timestamp = int(state.get("timestamp", 0))
        if _cached_timestamp != timestamp or _cached_png is None:
            _cached_png = render_png_bytes(state.get("state", "idle"), state.get("text", ""))
            _cached_timestamp = timestamp

        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(_cached_png)))
        self.send_header("ETag", _state_etag(state))
        self.end_headers()
        self.wfile.write(_cached_png)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path not in {"/state", "/state.json"}:
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        state = _read_state()
        if isinstance(payload, dict):
            state.update({key: payload[key] for key in ("state", "text") if key in payload})
        state["timestamp"] = int(time.time())
        _write_state(state)
        self._send_json(state)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer((HOST, PORT), StateHandler)
    print(f"Serving {STATE_PATH} on http://{HOST}:{PORT}/state.json")
    print(f"Rendering images on http://{HOST}:{PORT}/screen.png")
    server.serve_forever()
