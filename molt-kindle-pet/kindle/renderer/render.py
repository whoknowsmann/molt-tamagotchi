from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

from draw_states import STATE_LIST, draw_state

SCREEN_WIDTH = 1264
SCREEN_HEIGHT = 1680
OUTPUT_PATH = Path("/tmp/molt_display.png")


def _wrap_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width) if text else []


def render_state(state_path: Path) -> None:
    with state_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    state = data.get("state", "idle")
    if state not in STATE_LIST:
        state = "error"

    message = data.get("text", "")

    image = Image.new("L", (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    sprite = draw_state(state, (SCREEN_WIDTH, SCREEN_HEIGHT))
    image.paste(sprite, (0, 0))

    label = f"STATE: {state.upper()}"
    draw.text((40, 40), label, font=font, fill=0)

    wrapped = _wrap_text(message, width=40)
    y = SCREEN_HEIGHT - 300
    for line in wrapped:
        draw.text((40, y), line, font=font, fill=0)
        y += 25

    image.save(OUTPUT_PATH)
    subprocess.run(["/usr/bin/eips", "-g", str(OUTPUT_PATH)], check=False)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: render.py /path/to/state.json")
        return 1
    render_state(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
