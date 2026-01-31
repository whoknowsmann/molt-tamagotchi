# Setup guide

## PC setup
1. Ensure Python 3 is installed.
2. Install dependencies from `molt-kindle-pet/pc`:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python3 state_server.py
   ```
4. Update state with the helper script (auto-bumps `timestamp`):
   ```bash
   python3 update_state.py --state thinking --text "Hello from Molt!"
   ```

The server listens on `http://0.0.0.0:8000/` by default and serves:
- `GET /state.json`
- `GET /screen.png`
- `POST /state` (or `/state.json`) to update state and timestamp

## Kindle setup
1. Copy `molt-kindle-pet/kindle` to your Kindle (e.g., `/mnt/us/molt-kindle-pet/kindle`).
2. Install KUAL if not already installed.
3. Run the install script to link the KUAL extension:
   ```sh
   cd /mnt/us/molt-kindle-pet/kindle
   ./install.sh
   ```
4. Create a config file to set the PC URL:
   ```sh
   cat <<'CONFIG' > /mnt/us/extensions/molt_display/config.sh
   PC_URL="http://<pc-ip>:8000"
   CONFIG
   ```
5. Smoke test the PC from the Kindle (requires curl or wget):
   ```sh
   curl http://<pc-ip>:8000/state.json
   ```

## Using the KUAL menu
- **Start Molt Pet**: Starts the polling loop.
- **Stop Molt Pet**: Stops the polling loop.
- **Update Once (Debug)**: Fetches state once and refreshes the display.

## Display tools
The Kindle will try to display the image using:
1. `eips` (preferred)
2. `fbink` (fallback)

If neither is available, the script logs a clear error in the KUAL output/log.

## Troubleshooting
### PC not reachable
- Verify the PC and Kindle are on the same Wi-Fi network.
- Ensure the server is running and listening on `0.0.0.0:8000`.
- Confirm the correct IP in `config.sh`.

### Timestamp not changing
- Use `pc/update_state.py` or `POST /state` so the timestamp updates automatically.
- If you manually edit `pc/state.json`, make sure the `timestamp` value changes.

### Display tool missing
- Install or enable `eips` on the Kindle. If unavailable, install `fbink`.
- Re-run `install.sh` to ensure scripts are in place.
