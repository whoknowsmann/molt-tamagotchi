#!/usr/bin/env python3
"""
Simple HTTP server for the phone display.
Serves static files and proxies /state.json to the main state server.
"""

import http.server
import os
import urllib.request
from pathlib import Path

PORT = 8080
STATE_SERVER = os.environ.get('STATE_SERVER', 'http://localhost:8000')
STATIC_DIR = Path(__file__).parent

class PhoneDisplayHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)
    
    def do_GET(self):
        # Proxy state.json to the state server
        if self.path == '/state.json':
            try:
                with urllib.request.urlopen(f'{STATE_SERVER}/state.json', timeout=5) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', len(data))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_error(502, f'State server error: {e}')
            return
        
        # Serve static files
        super().do_GET()
    
    def end_headers(self):
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    print(f'Phone display server starting on http://0.0.0.0:{PORT}')
    print(f'Proxying state from {STATE_SERVER}')
    print(f'Serving files from {STATIC_DIR}')
    server = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), PhoneDisplayHandler)
    server.serve_forever()
