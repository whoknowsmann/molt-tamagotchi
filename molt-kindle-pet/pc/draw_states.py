from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

STATE_LIST = [
    "idle",
    "alert",
    "thinking",
    "talking",
    "excited",
    "sleeping",
    "error",
]


def _draw_face(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int) -> None:
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=0, width=4)


def _draw_eyes(draw: ImageDraw.ImageDraw, left: tuple[int, int], right: tuple[int, int]) -> None:
    for cx, cy in (left, right):
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=0)


def _draw_mouth(draw: ImageDraw.ImageDraw, bbox: tuple[int, int, int, int], smile: bool) -> None:
    if smile:
        draw.arc(bbox, start=10, end=170, fill=0, width=4)
    else:
        draw.arc(bbox, start=190, end=350, fill=0, width=4)


def draw_state(state: str, size: tuple[int, int]) -> Image.Image:
    width, height = size
    img = Image.new("L", size, 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    center = (width // 2, height // 2 - 150)
    radius = 150

    _draw_face(draw, center, radius)

    left_eye = (center[0] - 50, center[1] - 30)
    right_eye = (center[0] + 50, center[1] - 30)

    if state == "sleeping":
        draw.line((left_eye[0] - 10, left_eye[1], left_eye[0] + 10, left_eye[1]), fill=0, width=4)
        draw.line((right_eye[0] - 10, right_eye[1], right_eye[0] + 10, right_eye[1]), fill=0, width=4)
        draw.text((center[0] + 120, center[1] - 120), "Z", font=font, fill=0)
        draw.text((center[0] + 150, center[1] - 160), "Z", font=font, fill=0)
    elif state == "alert":
        _draw_eyes(draw, left_eye, right_eye)
        draw.ellipse((center[0] + 110, center[1] - 180, center[0] + 160, center[1] - 130), fill=0)
        draw.rectangle((center[0] + 135, center[1] - 120, center[0] + 145, center[1] - 60), fill=0)
    elif state == "thinking":
        _draw_eyes(draw, left_eye, right_eye)
        draw.ellipse((center[0] + 120, center[1] - 140, center[0] + 170, center[1] - 90), outline=0, width=4)
        draw.ellipse((center[0] + 170, center[1] - 170, center[0] + 220, center[1] - 120), outline=0, width=4)
    elif state == "talking":
        _draw_eyes(draw, left_eye, right_eye)
        draw.rectangle((center[0] - 40, center[1] + 40, center[0] + 40, center[1] + 90), outline=0, width=4)
        draw.text((center[0] + 110, center[1] - 50), "...", font=font, fill=0)
    elif state == "excited":
        _draw_eyes(draw, left_eye, right_eye)
        draw.line((center[0] - 80, center[1] - 110, center[0] - 40, center[1] - 70), fill=0, width=4)
        draw.line((center[0] + 80, center[1] - 110, center[0] + 40, center[1] - 70), fill=0, width=4)
        draw.text((center[0] + 110, center[1] - 180), "!", font=font, fill=0)
    elif state == "error":
        draw.line((left_eye[0] - 10, left_eye[1] - 10, left_eye[0] + 10, left_eye[1] + 10), fill=0, width=4)
        draw.line((left_eye[0] - 10, left_eye[1] + 10, left_eye[0] + 10, left_eye[1] - 10), fill=0, width=4)
        draw.line((right_eye[0] - 10, right_eye[1] - 10, right_eye[0] + 10, right_eye[1] + 10), fill=0, width=4)
        draw.line((right_eye[0] - 10, right_eye[1] + 10, right_eye[0] + 10, right_eye[1] - 10), fill=0, width=4)
        draw.rectangle((center[0] - 40, center[1] + 40, center[0] + 40, center[1] + 90), outline=0, width=4)
    else:
        _draw_eyes(draw, left_eye, right_eye)

    _draw_mouth(draw, (center[0] - 60, center[1] + 10, center[0] + 60, center[1] + 80), state in {"idle", "excited"})

    if state == "idle":
        draw.line((center[0] - 140, center[1] + 120, center[0] - 80, center[1] + 160), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 120, center[0] + 80, center[1] + 160), fill=0, width=4)
    elif state == "alert":
        draw.line((center[0] - 140, center[1] + 100, center[0] - 50, center[1] + 60), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 100, center[0] + 50, center[1] + 60), fill=0, width=4)
    elif state == "thinking":
        draw.line((center[0] - 140, center[1] + 140, center[0] - 60, center[1] + 80), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 140, center[0] + 60, center[1] + 80), fill=0, width=4)
    elif state == "talking":
        draw.line((center[0] - 140, center[1] + 120, center[0] - 80, center[1] + 80), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 120, center[0] + 80, center[1] + 80), fill=0, width=4)
    elif state == "excited":
        draw.line((center[0] - 140, center[1] + 60, center[0] - 80, center[1] + 20), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 60, center[0] + 80, center[1] + 20), fill=0, width=4)
    elif state == "sleeping":
        draw.line((center[0] - 140, center[1] + 160, center[0] - 80, center[1] + 160), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 160, center[0] + 80, center[1] + 160), fill=0, width=4)
    elif state == "error":
        draw.line((center[0] - 140, center[1] + 120, center[0] - 80, center[1] + 160), fill=0, width=4)
        draw.line((center[0] + 140, center[1] + 120, center[0] + 80, center[1] + 160), fill=0, width=4)
        draw.rectangle((center[0] - 30, center[1] - 210, center[0] + 30, center[1] - 150), outline=0, width=4)

    return img
