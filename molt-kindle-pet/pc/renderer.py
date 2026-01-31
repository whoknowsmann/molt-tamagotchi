from __future__ import annotations

import textwrap
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from draw_states import STATE_LIST, draw_state

# Kindle Oasis 10th gen screen dimensions
PORTRAIT_WIDTH = 1264
PORTRAIT_HEIGHT = 1680
LANDSCAPE_WIDTH = 1680
LANDSCAPE_HEIGHT = 1264


def _wrap_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width) if text else []


def render_state_image(state: str, message: str, landscape: bool = False) -> Image.Image:
    if state not in STATE_LIST:
        state = "error"

    if landscape:
        width, height = LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT
    else:
        width, height = PORTRAIT_WIDTH, PORTRAIT_HEIGHT

    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    
    # Try to load a nicer font, fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except OSError:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large

    # Draw the state sprite
    sprite = draw_state(state, (width, height))
    image.paste(sprite, (0, 0))

    # State label at top
    label = state.upper()
    draw.text((40, 30), label, font=font_large, fill=0)

    # Message text at bottom
    wrap_width = 50 if landscape else 35
    wrapped = _wrap_text(message, width=wrap_width)
    y = height - 200
    for line in wrapped:
        draw.text((40, y), line, font=font_medium, fill=0)
        y += 35

    # EXIT button in top-right corner - make it obvious on e-ink
    exit_margin = 20
    exit_w, exit_h = 160, 80
    exit_x = width - exit_w - exit_margin
    exit_y = exit_margin
    
    # Draw button with dark border and light gray fill (visible on e-ink)
    draw.rectangle(
        [exit_x, exit_y, exit_x + exit_w, exit_y + exit_h],
        outline=0, width=6
    )
    # Inner rectangle for depth effect
    draw.rectangle(
        [exit_x + 4, exit_y + 4, exit_x + exit_w - 4, exit_y + exit_h - 4],
        outline=80, width=2
    )
    # Draw [X] EXIT text - centered
    draw.text((exit_x + 20, exit_y + 22), "[X] EXIT", font=font_large, fill=0)

    return image


def render_png_bytes(state: str, message: str, landscape: bool = False) -> bytes:
    image = render_state_image(state, message, landscape)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
