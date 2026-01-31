# Molt Kindle Pet (MVP)

Minimal Tamagotchi-style display for a jailbroken Kindle Oasis (10th gen, firmware 5.18.2) using KUAL. The Kindle polls a PC over Wi-Fi for a JSON state and renders a simple monochrome sprite + text.

## Features
- Polling-only model (Kindle pulls `/state.json` from PC).
- Static rendering (no animation).
- One-way communication (PC → Kindle).
- All visuals generated dynamically with PIL (no binary assets in repo).
- Simple KUAL extension with start/stop/once actions.

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
│   ├── renderer/
│   │   ├── render.py
│   │   └── draw_states.py
│   └── install.sh
├── pc/
│   ├── state_server.py
│   ├── state.json
│   └── requirements.txt
└── docs/
    └── setup.md
```

## Quick start
See [docs/setup.md](docs/setup.md) for full setup steps.

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

Each state renders a distinct pose/expression in `kindle/renderer/draw_states.py`.
