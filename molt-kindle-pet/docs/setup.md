# Setup guide

## PC setup
1. Ensure Python 3 is installed.
2. From `molt-kindle-pet/pc`, run:
   ```bash
   python3 state_server.py
   ```
3. Edit `pc/state.json` to change the character state.

The server listens on `http://0.0.0.0:8000/state.json` by default.

## Kindle setup
1. Copy `molt-kindle-pet/kindle` to your Kindle (e.g., `/mnt/us/molt-kindle-pet/kindle`).
2. Install KUAL if not already installed.
3. Install Pillow (PIL) for Python 3 on the Kindle.
   - You can transfer a prebuilt wheel and install with `pip3` or use a package you already trust.
4. Run the install script to link the KUAL extension:
   ```bash
   cd /mnt/us/molt-kindle-pet/kindle
   ./install.sh
   ```
5. Create an optional config file to set the PC URL:
   ```bash
   cat <<'CONFIG' > /mnt/us/extensions/molt_display/config.sh
   PC_URL="http://<pc-ip>:8000/state.json"
   CONFIG
   ```

## Using the KUAL menu
- **Start Molt Pet**: Starts the polling loop.
- **Stop Molt Pet**: Stops the polling loop.
- **Update Once (Debug)**: Fetches state once and renders immediately.

## Notes
- The Kindle only re-renders when the `timestamp` changes.
- All visuals are generated at runtime; no binary assets are stored in the repo.
