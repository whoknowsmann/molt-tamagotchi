# Molt Kindle Pet (MVP)

Minimal Tamagotchi-style display for a jailbroken Kindle Oasis (10th gen, firmware 5.18.2) using KUAL. The Kindle polls a PC over Wi-Fi for a JSON state and a pre-rendered screen image.

## Features
- Polling-only model (Kindle pulls `/state.json` and `/screen.png` from the PC).
- Static rendering (no animation).
- One-way communication (PC → Kindle).
- Rendering happens on the PC using Pillow; Kindle only runs shell scripts.
- Simple KUAL extension with start/stop/once actions and eips/fbink display support.

## Repository layout
```
molt-kindle-pet/
├── README.md
├── kindle/
│   ├── extensions/
│   │   └── molt_display/
│   │       ├── menu.json
│   │       └── bin/
│   │           ├── start.sh
│   │           ├── stop.sh
│   │           ├── run_once.sh
│   │           └── loop.sh
│   └── install.sh
├── pc/
│   ├── draw_states.py
│   ├── renderer.py
│   ├── state_server.py
│   ├── state.json
│   ├── update_state.py
│   └── requirements.txt
└── docs/
    └── setup.md
```

## Quick start
See [docs/setup.md](docs/setup.md) for full setup steps.

## Quick Test
1. Start the PC server:
   ```bash
   cd pc
   python3 state_server.py
   ```
2. From the PC, verify endpoints:
   ```bash
   curl http://127.0.0.1:8000/state.json
   curl -I http://127.0.0.1:8000/screen.png
   ```
3. On the Kindle, set the PC URL in `/mnt/us/extensions/molt_display/config.sh`:
   ```sh
   PC_URL="http://<pc-ip>:8000"
   ```
4. Launch KUAL → Molt Pet → Start Molt Pet and confirm the display updates.

## Data contract
The PC serves `/state.json`:
```
{
  "state": "idle",
  "text": "short message",
  "timestamp": 1700000000
}
```

## States
`idle`, `alert`, `thinking`, `talking`, `excited`, `sleeping`, `error`
Each state renders a distinct pose/expression in `pc/draw_states.py`.
