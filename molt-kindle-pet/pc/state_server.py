from __future__ import annotations

import http.server
import json
import os
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent / "state.json"
HOST = "0.0.0.0"
PORT = int(os.environ.get("MOLT_PORT", "8000"))


class StateHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path != "/state.json":
            self.send_error(404, "Not Found")
            return

        with STATE_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        payload = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer((HOST, PORT), StateHandler)
    print(f"Serving {STATE_PATH} on http://{HOST}:{PORT}/state.json")
    server.serve_forever()
