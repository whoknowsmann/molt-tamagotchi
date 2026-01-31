from __future__ import annotations

import textwrap
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from draw_states import STATE_LIST, draw_state

SCREEN_WIDTH = 1264
SCREEN_HEIGHT = 1680


def _wrap_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width) if text else []


def render_state_image(state: str, message: str) -> Image.Image:
    if state not in STATE_LIST:
        state = "error"

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

    return image


def render_png_bytes(state: str, message: str) -> bytes:
    image = render_state_image(state, message)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
