#!/usr/bin/env python3
"""Procedurally generate PNG artwork for The Price of Dawn."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

WIDTH = 1600
HEIGHT = 900
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "images"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]


def mix(
    color_a: Sequence[int], color_b: Sequence[int], ratio: float
) -> tuple[int, int, int]:
    return tuple(int(color_a[i] + (color_b[i] - color_a[i]) * ratio) for i in range(3))


def clamp(value: float, min_value: float = 0, max_value: float = 255) -> int:
    return int(max(min_value, min(max_value, value)))


def gradient(top: Sequence[int], bottom: Sequence[int]) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), top)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / max(HEIGHT - 1, 1)
        draw.line((0, y, WIDTH, y), fill=mix(top, bottom, ratio))
    return img


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        font_path = Path(path)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)
    return ImageFont.load_default()


def overlay_noise(base: Image.Image, darkness: float, seed: int) -> Image.Image:
    rng = random.Random(seed)
    noise = Image.effect_noise((WIDTH, HEIGHT), 64 + rng.randint(0, 32))
    colored = ImageOps.colorize(noise, (10, 8, 6), (140, 120, 100))
    return Image.blend(base, colored, darkness)


def add_vignette(base: Image.Image, amount: float = 0.35) -> Image.Image:
    mask = Image.radial_gradient("L").resize((WIDTH, HEIGHT))
    inverted = ImageOps.invert(mask)
    adjusted = ImageEnhance.Brightness(inverted).enhance(amount)
    overlay = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    return Image.composite(base, overlay, adjusted)


def lighten(color: Sequence[int], factor: float) -> tuple[int, int, int]:
    return tuple(clamp(c + (255 - c) * factor) for c in color)


def darken(color: Sequence[int], factor: float) -> tuple[int, int, int]:
    return tuple(clamp(c * (1 - factor)) for c in color)


def base_canvas(
    sky_top: Sequence[int], sky_bottom: Sequence[int], seed: int
) -> Image.Image:
    canvas = gradient(sky_top, sky_bottom).convert("RGB")
    textured = overlay_noise(canvas, 0.18, seed)
    return textured


def create_parchment(seed: int) -> Image.Image:
    base = Image.new("RGB", (WIDTH, HEIGHT), (190, 170, 135))
    base = overlay_noise(base, 0.25, seed)
    draw = ImageDraw.Draw(base)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=(120, 100, 80), width=3)
    return base.convert("RGBA")


def draw_glow(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    color: Sequence[int],
    alpha: int = 200,
) -> None:
    cx, cy = center
    steps = 6
    for i in range(steps, 0, -1):
        r = radius * (i / steps)
        a = int(alpha * (i / steps) ** 2)
        draw.ellipse(
            (
                cx - r,
                cy - r,
                cx + r,
                cy + r,
            ),
            fill=(*color, a),
        )


def draw_wavy_layer(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    base_y: float,
    amplitude: float,
    color: Sequence[int],
) -> None:
    points: List[tuple[float, float]] = []
    step = WIDTH // 8
    x = -120
    while x <= WIDTH + 120:
        points.append((x, base_y + rand.uniform(-amplitude, amplitude)))
        x += rand.randint(step - 40, step + 40)
    points.extend([(WIDTH + 200, HEIGHT + 50), (-200, HEIGHT + 50)])
    draw.polygon(points, fill=color)


def draw_lantern(
    draw: ImageDraw.ImageDraw, x: float, y: float, radius: float = 10
) -> None:
    color = (234, 180, 90)
    draw_glow(draw, (x, y), radius * 2.2, color, alpha=160)
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        fill=(*color, 230),
        outline=(*darken(color, 0.4), 255),
        width=1,
    )


def draw_people_line(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    baseline: float,
    count: int,
    spread: tuple[int, int],
    color: Sequence[int] = (30, 25, 28),
) -> None:
    start_x = spread[0]
    end_x = spread[1]
    for i in range(count):
        x = start_x + (end_x - start_x) * (i / max(count - 1, 1))
        height = rand.randint(30, 65)
        draw.rectangle(
            (x - 6, baseline - height, x + 6, baseline),
            fill=(*color, 255),
        )
        draw.ellipse(
            (x - 7, baseline - height - 18, x + 7, baseline - height + 2),
            fill=(*lighten(color, 0.2), 255),
        )


def draw_buildings(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    baseline: float,
    count: int,
    color: Sequence[int],
    window_color: Sequence[int],
    tall: bool = False,
) -> None:
    x = -60
    for _ in range(count):
        width = rand.randint(45, 140)
        height = rand.randint(90, 320 if tall else 220)
        top = baseline - height
        draw.rectangle((x, top, x + width, baseline), fill=(*color, 255))
        if rand.random() < 0.85:
            row_y = top + 18
            while row_y < baseline - 18:
                col_x = x + 10
                while col_x < x + width - 10:
                    if rand.random() < 0.55:
                        draw.rectangle(
                            (col_x, row_y, col_x + 6, row_y + 12),
                            fill=(*window_color, 230),
                        )
                    col_x += 22
                row_y += 24
        x += width - rand.randint(-10, 30)


def draw_gate(
    draw: ImageDraw.ImageDraw,
    center: float,
    baseline: float,
    width: float,
    height: float,
    color: Sequence[int],
) -> None:
    left = center - width / 2
    right = center + width / 2
    top = baseline - height
    draw.rectangle((left, top, right, baseline), outline=None, fill=(*color, 255))
    arch_height = height * 0.6
    draw.pieslice(
        (left, baseline - arch_height * 2, right, baseline),
        180,
        360,
        fill=(20, 20, 24, 255),
    )


def draw_circle_of_stones(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    center: tuple[float, float],
    radius: float,
    color: Sequence[int],
) -> None:
    cx, cy = center
    for angle in range(0, 360, 36):
        rad = math.radians(angle)
        r = radius + rand.uniform(-6, 6)
        x = cx + math.cos(rad) * r
        y = cy + math.sin(rad) * r
        stone_height = rand.randint(28, 52)
        draw.rectangle(
            (x - 6, y - stone_height, x + 6, y + 4),
            fill=(*color, 255),
        )


def draw_reeds(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    area: tuple[int, int, int, int],
    color: Sequence[int],
) -> None:
    left, top, right, bottom = area
    for x in range(left, right, 12):
        height = rand.randint(12, 46)
        draw.line(
            (x, bottom, x + rand.randint(-3, 3), bottom - height),
            fill=(*color, 255),
            width=2,
        )


def draw_pillar(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    height: float,
    color: Sequence[int],
) -> None:
    cx, cy = center
    draw.rectangle(
        (cx - 12, cy - height, cx + 12, cy + 10),
        fill=(*color, 255),
        outline=(*lighten(color, 0.1), 255),
        width=2,
    )


def draw_table(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    width: float,
    depth: float,
    color: Sequence[int],
) -> None:
    cx, cy = center
    top = [
        (cx - width / 2, cy),
        (cx + width / 2, cy),
        (cx + width / 2 - depth * 0.3, cy + depth),
        (cx - width / 2 + depth * 0.3, cy + depth),
    ]
    draw.polygon(top, fill=(*color, 240))


def draw_chairs(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    center_line: float,
    count: int,
    color: Sequence[int],
) -> None:
    spacing = WIDTH / (count + 2)
    for i in range(count):
        x = spacing * (i + 1)
        chair_height = rand.randint(60, 90)
        draw.rectangle(
            (x - 15, center_line - chair_height, x + 15, center_line),
            fill=(*color, 255),
        )


def draw_bookshelves(
    draw: ImageDraw.ImageDraw,
    rows: int,
    color: Sequence[int],
) -> None:
    spacing = HEIGHT / (rows + 2)
    for i in range(rows):
        y = spacing * (i + 1)
        draw.rectangle((100, y, WIDTH - 100, y + 12), fill=(*color, 180))


def draw_papers(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    area: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = area
    for _ in range(15):
        x = rand.randint(left, right)
        y = rand.randint(top, bottom)
        w = rand.randint(40, 120)
        h = rand.randint(18, 50)
        draw.rectangle(
            (x, y, x + w, y + h),
            fill=(220, 215, 200, 220),
            outline=(120, 110, 90, 220),
        )


def draw_beds(
    draw: ImageDraw.ImageDraw,
    rand: random.Random,
    rows: int,
    color: Sequence[int],
    occupant: bool = False,
) -> None:
    spacing = WIDTH / (rows + 1)
    for i in range(rows):
        x = spacing * (i + 0.5)
        draw.rectangle(
            (x - 90, HEIGHT * 0.6, x + 90, HEIGHT * 0.65),
            fill=(*color, 255),
        )
        if occupant:
            draw.ellipse(
                (x - 45, HEIGHT * 0.59, x + 45, HEIGHT * 0.64),
                fill=(210, 200, 190, 230),
            )


def draw_single_figure(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    height: float,
    color: Sequence[int],
) -> None:
    x, y = position
    draw.rectangle((x - 12, y - height, x + 12, y), fill=(*color, 255))
    draw.ellipse(
        (x - 14, y - height - 20, x + 14, y - height + 4),
        fill=(*lighten(color, 0.2), 255),
    )


def draw_robed_figure(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    height: float,
    robe_color: Sequence[int],
    accent: Sequence[int] | None = None,
) -> None:
    x, y = position
    base = [
        (x - height * 0.18, y),
        (x, y - height * 0.8),
        (x + height * 0.18, y),
    ]
    draw.polygon(base, fill=(*robe_color, 255))
    draw.ellipse(
        (x - height * 0.12, y - height * 0.95, x + height * 0.12, y - height * 0.7),
        fill=(*lighten(robe_color, 0.25), 255),
    )
    if accent:
        draw.line(
            (x, y - height * 0.8, x, y),
            fill=(*accent, 255),
            width=4,
        )


@dataclass(frozen=True)
class ImageSpec:
    name: str
    category: str
    tags: Sequence[str]
    meta: Dict[str, object] | None = None

    @property
    def seed(self) -> int:
        return abs(hash(self.name)) & 0xFFFFFFFF


def spec_value(spec: ImageSpec, key: str, default):
    if spec.meta and key in spec.meta:
        return spec.meta[key]
    return default


def render_city(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    sky_top = spec_value(spec, "sky_top", (126, 108, 90))
    sky_bottom = spec_value(spec, "sky_bottom", (26, 24, 32))
    img = base_canvas(sky_top, sky_bottom, spec.seed).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    horizon = spec_value(spec, "horizon", 560)
    layer_color = spec_value(spec, "layer_color", (42, 38, 44))
    for depth, offset in enumerate((280, 220, 170)):
        color = lighten(layer_color, depth * 0.05)
        draw_wavy_layer(draw, rand, horizon - offset, 45 + depth * 10, (*color, 255))

    if "river" in spec.tags:
        water_height = horizon - 60
        water = ImageDraw.Draw(img, "RGBA")
        water_color = (40, 55, 70, 200)
        water.rectangle((0, water_height, WIDTH, HEIGHT), fill=water_color)
        for wave in range(35):
            y = water_height + rand.randint(10, 280)
            water.line(
                (rand.randint(0, WIDTH - 120), y, rand.randint(120, WIDTH), y),
                fill=(140, 150, 160, 60),
                width=rand.randint(1, 3),
            )

    skyline_color = spec_value(spec, "skyline_color", (52, 48, 58))
    window_color = spec_value(spec, "window_color", (220, 170, 110))
    draw_buildings(
        draw, rand, horizon, 18, skyline_color, window_color, tall="tower" in spec.tags
    )

    if "tower" in spec.tags:
        tower_x = WIDTH * 0.55
        draw.rectangle(
            (
                tower_x - 70,
                horizon - 360,
                tower_x + 70,
                horizon,
            ),
            fill=(*darken(skyline_color, 0.1), 255),
        )
        for y in range(int(horizon - 340), int(horizon), 26):
            if rand.random() < 0.75:
                draw.rectangle(
                    (tower_x - 40, y, tower_x + 40, y + 14),
                    fill=(*window_color, 230),
                )

    if "walls" in spec.tags:
        wall_y = horizon - 40
        draw.rectangle(
            (0, wall_y, WIDTH, wall_y + 30),
            fill=(*darken(skyline_color, 0.3), 255),
        )

    if "gate" in spec.tags:
        draw_gate(draw, WIDTH / 2, horizon + 20, 240, 220, darken(skyline_color, 0.25))

    if "road" in spec.tags:
        road = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        rdraw = ImageDraw.Draw(road, "RGBA")
        rdraw.polygon(
            (
                WIDTH * 0.35,
                HEIGHT,
                WIDTH * 0.47,
                horizon + 120,
                WIDTH * 0.53,
                horizon + 120,
                WIDTH * 0.65,
                HEIGHT,
            ),
            fill=(60, 55, 50, 220),
        )
        img = Image.alpha_composite(img, road)

    if "bridge" in spec.tags:
        bridge_y = horizon - 40
        draw.rectangle(
            (WIDTH * 0.25, bridge_y - 20, WIDTH * 0.75, bridge_y + 20),
            fill=(70, 65, 60, 240),
        )

    if "lanterns" in spec.tags:
        for x in range(120, WIDTH - 120, 120):
            draw_lantern(draw, x, horizon - 30, radius=8)

    if "crowd" in spec.tags:
        draw_people_line(draw, rand, HEIGHT - 80, 14, (120, WIDTH - 120))

    if "circle" in spec.tags:
        draw_circle_of_stones(draw, rand, (WIDTH / 2, horizon + 40), 160, (70, 65, 60))

    if "glow" in spec.tags:
        draw_glow(draw, (WIDTH / 2, horizon + 40), 150, (240, 160, 80), alpha=140)

    if "figures" in spec.tags:
        draw_people_line(draw, rand, horizon + 90, 10, (WIDTH * 0.2, WIDTH * 0.8))

    result = img.convert("RGB")
    return add_vignette(result)


def render_land(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    sky_top = spec_value(spec, "sky_top", (110, 96, 82))
    sky_bottom = spec_value(spec, "sky_bottom", (28, 26, 32))
    img = base_canvas(sky_top, sky_bottom, spec.seed).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    horizon = spec_value(spec, "horizon", 520)
    base_color = spec_value(spec, "layer_color", (48, 44, 48))
    for depth, offset in enumerate((260, 200, 140)):
        color = lighten(base_color, depth * 0.06)
        draw_wavy_layer(draw, rand, horizon - offset, 60 + depth * 20, (*color, 255))

    foreground_color = spec_value(spec, "foreground", (55, 48, 42))
    draw_wavy_layer(draw, rand, horizon - 40, 40, (*foreground_color, 255))

    if "marsh" in spec.tags or "water" in spec.tags:
        water = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        wdraw = ImageDraw.Draw(water, "RGBA")
        wdraw.rectangle(
            (0, horizon, WIDTH, HEIGHT),
            fill=(50, 70, 70, 220),
        )
        for _ in range(50):
            y = rand.randint(int(horizon + 10), HEIGHT - 20)
            x1 = rand.randint(50, WIDTH - 150)
            x2 = x1 + rand.randint(40, 200)
            wdraw.line((x1, y, x2, y), fill=(190, 200, 210, 60), width=2)
        img = Image.alpha_composite(img, water)

    if "road" in spec.tags:
        path = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(path, "RGBA")
        pdraw.polygon(
            (
                WIDTH * 0.4,
                HEIGHT,
                WIDTH * 0.46,
                horizon + 110,
                WIDTH * 0.54,
                horizon + 110,
                WIDTH * 0.6,
                HEIGHT,
            ),
            fill=(70, 60, 50, 220),
        )
        img = Image.alpha_composite(img, path)

    if "circle" in spec.tags:
        draw_circle_of_stones(
            draw,
            rand,
            (WIDTH / 2, horizon + 60),
            160,
            (90, 80, 72),
        )

    if "glow" in spec.tags:
        draw_glow(draw, (WIDTH / 2, horizon + 40), 170, (240, 168, 90), alpha=130)

    if "lanterns" in spec.tags:
        for x in (WIDTH * 0.35, WIDTH * 0.5, WIDTH * 0.65):
            draw_lantern(draw, x, horizon + 40, radius=12)

    if "wayshrine" in spec.tags:
        draw_pillar(draw, (WIDTH * 0.5, horizon + 50), 140, (130, 120, 110))

    if "offerings" in spec.tags:
        for offset in (-40, 0, 40):
            draw.rectangle(
                (
                    WIDTH * 0.5 - 60 + offset,
                    horizon + 90,
                    WIDTH * 0.5 - 30 + offset,
                    horizon + 110,
                ),
                fill=(170, 150, 110, 255),
            )

    if "traveler" in spec.tags:
        draw_people_line(
            draw,
            rand,
            horizon + 150,
            1,
            (int(WIDTH * 0.48), int(WIDTH * 0.52)),
        )

    if "heron" in spec.tags:
        draw.line(
            (
                WIDTH * 0.7,
                horizon + 120,
                WIDTH * 0.72,
                horizon + 60,
            ),
            fill=(210, 210, 210, 255),
            width=3,
        )
        draw.line(
            (
                WIDTH * 0.72,
                horizon + 60,
                WIDTH * 0.74,
                horizon + 110,
            ),
            fill=(210, 210, 210, 255),
            width=3,
        )

    if "reeds" in spec.tags:
        draw_reeds(
            draw,
            rand,
            (50, int(horizon + 40), WIDTH - 50, HEIGHT - 30),
            (70, 120, 90),
        )

    if "figures" in spec.tags:
        draw_people_line(
            draw,
            rand,
            horizon + 140,
            9,
            (int(WIDTH * 0.3), int(WIDTH * 0.7)),
        )

    result = img.convert("RGB")
    return add_vignette(result)


def render_interior(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    sky_top = spec_value(spec, "sky_top", (88, 74, 66))
    sky_bottom = spec_value(spec, "sky_bottom", (22, 18, 22))
    img = base_canvas(sky_top, sky_bottom, spec.seed).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    horizon = spec_value(spec, "horizon", int(HEIGHT * 0.45))
    floor_color = spec_value(spec, "floor_color", (42, 34, 30))
    draw.rectangle((0, horizon, WIDTH, HEIGHT), fill=(*floor_color, 255))
    for x in range(-200, WIDTH + 200, 80):
        draw.line(
            (x, horizon, x + 220, HEIGHT),
            fill=(20, 18, 16, 90),
            width=1,
        )

    if "lanterns" in spec.tags:
        for x in range(140, WIDTH - 140, 160):
            draw_lantern(draw, x, 120, radius=10)

    if "fireplace" in spec.tags:
        draw.rectangle((80, horizon - 60, 220, horizon + 30), fill=(50, 40, 35, 255))
        draw_glow(draw, (150, horizon - 10), 60, (255, 150, 90), alpha=150)

    if "desk" in spec.tags:
        draw_table(draw, (WIDTH / 2, horizon + 40), WIDTH * 0.6, 160, (80, 60, 52))

    if "documents" in spec.tags:
        draw_papers(
            draw,
            rand,
            (
                int(WIDTH * 0.25),
                int(horizon + 20),
                int(WIDTH * 0.75),
                int(horizon + 160),
            ),
        )

    if "council" in spec.tags:
        draw_chairs(draw, rand, horizon + 150, 7, (60, 52, 48))

    if "chairs" in spec.tags and "council" not in spec.tags:
        draw_chairs(draw, rand, horizon + 180, 5, (54, 44, 38))

    if "stage" in spec.tags:
        draw.rectangle(
            (120, horizon + 40, WIDTH - 120, horizon + 140), fill=(48, 38, 34, 255)
        )

    if "musicians" in spec.tags:
        draw_people_line(draw, rand, horizon + 140, 4, (200, WIDTH - 200))

    if "audience" in spec.tags:
        draw_people_line(draw, rand, HEIGHT - 90, 9, (140, WIDTH - 140))

    if "benches" in spec.tags:
        for y in range(int(horizon + 40), HEIGHT - 80, 90):
            draw_table(draw, (WIDTH / 2, y), WIDTH * 0.7, 100, (70, 55, 46))

    if "tools" in spec.tags:
        draw_papers(
            draw,
            rand,
            (
                int(WIDTH * 0.15),
                int(horizon + 20),
                int(WIDTH * 0.85),
                int(horizon + 120),
            ),
        )

    if "kitchen" in spec.tags:
        for row in range(2):
            y = horizon + 60 + row * 120
            draw_table(draw, (WIDTH / 2, y), WIDTH * 0.8, 120, (85, 66, 52))
            for x in range(200, WIDTH - 200, 140):
                draw.ellipse((x - 18, y + 20, x + 18, y + 50), fill=(200, 150, 90, 255))

    if (
        "tables" in spec.tags
        and "kitchen" not in spec.tags
        and "benches" not in spec.tags
    ):
        draw_table(draw, (WIDTH / 2, horizon + 120), WIDTH * 0.5, 120, (75, 60, 50))

    if "beds" in spec.tags:
        draw_beds(draw, rand, 4, (70, 60, 56), occupant="patients" in spec.tags)

    if "practitioner" in spec.tags:
        draw_single_figure(draw, (WIDTH * 0.75, horizon + 220), 120, (100, 90, 100))

    if "painting" in spec.tags:
        draw.rectangle(
            (WIDTH - 260, horizon - 80, WIDTH - 60, horizon + 20),
            fill=(200, 180, 90, 255),
        )

    if "shelves" in spec.tags:
        draw_bookshelves(draw, 4, (60, 50, 45))

    if "lab" in spec.tags:
        for x in range(220, WIDTH - 220, 160):
            draw.ellipse(
                (x - 20, horizon + 60, x + 20, horizon + 120), fill=(160, 200, 220, 200)
            )

    if "rods" in spec.tags:
        for x in range(260, WIDTH - 260, 180):
            draw.rectangle(
                (x - 12, horizon - 60, x + 12, horizon + 140), fill=(140, 130, 150, 255)
            )
            draw_glow(draw, (x, horizon - 30), 50, (210, 180, 110), alpha=120)

    if "figure" in spec.tags:
        draw_single_figure(draw, (WIDTH * 0.6, horizon + 200), 140, (60, 54, 64))

    result = img.convert("RGB")
    return add_vignette(result)


def render_portrait(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    sky_top = spec_value(spec, "sky_top", (96, 84, 76))
    sky_bottom = spec_value(spec, "sky_bottom", (24, 20, 26))
    img = base_canvas(sky_top, sky_bottom, spec.seed).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    count = spec_value(spec, "count", 1)
    spacing = WIDTH / (count + 1)
    for i in range(count):
        x = spacing * (i + 1)
        y = HEIGHT * 0.75
        robe_color = spec_value(
            spec,
            f"robe_color_{i}",
            (
                70 + rand.randint(-10, 10),
                60 + rand.randint(-10, 10),
                55 + rand.randint(-10, 10),
            ),
        )
        accent_color = spec_value(spec, "accent_color", (200, 150, 90))
        draw_robed_figure(
            draw,
            (x, y),
            360,
            robe_color,
            accent_color if "accent-line" in spec.tags else None,
        )

        if "halo" in spec.tags:
            draw_glow(draw, (x, y - 250), 120, (220, 180, 110), alpha=90)

        if "crown" in spec.tags:
            draw.polygon(
                (
                    (x - 40, y - 320),
                    (x - 10, y - 260),
                    (x + 10, y - 320),
                    (x + 40, y - 260),
                ),
                fill=(220, 190, 140, 255),
            )

        if "lantern" in spec.tags:
            draw_lantern(draw, x + 90, y - 80, radius=14)

        if "book" in spec.tags:
            draw.rectangle(
                (x - 80, y - 100, x - 10, y - 50),
                fill=(160, 120, 90, 255),
            )

        if "satchel" in spec.tags:
            draw.rectangle(
                (x + 20, y - 110, x + 90, y - 40),
                fill=(120, 80, 60, 255),
            )

        if "hands" in spec.tags:
            draw.ellipse(
                (x - 30, y - 180, x + 30, y - 140),
                outline=(220, 200, 180, 255),
                width=4,
            )

        if "shrine" in spec.tags:
            draw.rectangle(
                (x - 120, y - 80, x + 120, y - 20),
                fill=(90, 80, 70, 255),
            )

        if "altar" in spec.tags:
            draw.rectangle(
                (WIDTH * 0.35, HEIGHT * 0.78, WIDTH * 0.65, HEIGHT * 0.84),
                fill=(70, 60, 55, 255),
            )

    result = img.convert("RGB")
    return add_vignette(result)


def render_document(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    img = create_parchment(spec.seed)
    draw = ImageDraw.Draw(img, "RGBA")

    if "notebook" in spec.tags:
        draw.rectangle((360, 220, 1240, 680), fill=(220, 210, 190, 255))
        for y in range(240, 670, 24):
            draw.line((380, y, 1220, y), fill=(180, 170, 150, 255), width=1)
        for _ in range(80):
            x = rand.randint(390, 1200)
            y = rand.randint(250, 650)
            draw.line(
                (x, y, x + rand.randint(20, 80), y + rand.randint(-8, 8)),
                fill=(50, 40, 40, 255),
                width=2,
            )
        draw.line((900, 220, 900, 680), fill=(110, 80, 70, 255), width=6)
        draw.rectangle((1260, 360, 1350, 600), fill=(120, 80, 60, 255))

    if "letter" in spec.tags:
        draw.rectangle((520, 320, 1080, 560), fill=(230, 220, 200, 255))
        draw.polygon(
            ((520, 320), (1080, 320), (800, 520)),
            fill=(210, 200, 180, 255),
        )
        draw.ellipse((750, 430, 850, 530), fill=(150, 60, 50, 255))
        font = load_font(40)
        draw.text((580, 600), "Shelf 4-17-3", font=font, fill=(90, 70, 60, 255))

    if "scorecard" in spec.tags:
        font = load_font(36)
        headers = [
            "Consent vs Utility",
            "Loyalty vs Honesty",
            "Individual vs Collective",
            "Action vs Inaction",
            "Truth vs Mercy",
            "Justice vs Forgiveness",
        ]
        top = 160
        for idx, header in enumerate(headers):
            y = top + idx * 90
            draw.rectangle(
                (180, y, WIDTH - 180, y + 70), outline=(100, 80, 60, 255), width=2
            )
            draw.text((200, y + 10), header, font=font, fill=(80, 60, 50, 255))
            for session in range(1, 6):
                x = 600 + session * 120
                draw.text((x, y + 20), f"S{session}", font=font, fill=(90, 70, 60, 255))
                x1 = x + rand.randint(-20, 20)
                y1 = y + 30 + rand.randint(-10, 10)
                x2 = x1 + rand.randint(20, 40)
                y2 = y1 + rand.randint(6, 18)
                draw.ellipse(
                    (x1, y1, x2, y2),
                    outline=(60, 50, 45, 255),
                    width=2,
                )

    result = img.convert("RGB")
    return result


def render_map(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    img = create_parchment(spec.seed)
    draw = ImageDraw.Draw(img, "RGBA")
    font = load_font(42)

    if spec.meta and spec.meta.get("variant") == "city":
        districts = spec_value(
            spec,
            "districts",
            [
                "Ashring",
                "Lowmark",
                "Spire",
                "Dawnhalls",
                "Outer Ring",
                "Ashfen Gate",
            ],
        )
        center = (WIDTH / 2, HEIGHT / 2)
        radius = 260
        for idx, name in enumerate(districts):
            angle_start = (2 * math.pi / len(districts)) * idx
            angle_end = (2 * math.pi / len(districts)) * (idx + 1)
            points = [center]
            for step in range(6):
                angle = angle_start + (angle_end - angle_start) * (step / 5)
                r = radius + rand.randint(-20, 40)
                points.append(
                    (
                        center[0] + math.cos(angle) * r,
                        center[1] + math.sin(angle) * r,
                    )
                )
            draw.polygon(points, outline=(90, 70, 60, 255), fill=(210, 190, 150, 80))
            label_angle = (angle_start + angle_end) / 2
            lx = center[0] + math.cos(label_angle) * (radius + 60)
            ly = center[1] + math.sin(label_angle) * (radius + 60)
            draw.text((lx - 80, ly - 20), name, font=font, fill=(70, 50, 45, 255))
        draw.ellipse(
            (
                center[0] - 80,
                center[1] - 80,
                center[0] + 80,
                center[1] + 80,
            ),
            outline=(50, 40, 35, 255),
            width=4,
        )
        draw.text(
            (center[0] - 90, center[1] - 20),
            "Varenhold",
            font=font,
            fill=(40, 30, 30, 255),
        )
    else:
        territories = spec_value(
            spec,
            "territories",
            [
                "Solenne",
                "Graymere Holds",
                "Arveth",
                "Ashfen",
                "Dusk Parishes",
            ],
        )
        center = (WIDTH / 2, HEIGHT / 2)
        for idx, name in enumerate(territories):
            angle = (2 * math.pi / len(territories)) * idx
            points: List[tuple[float, float]] = []
            for step in range(6):
                theta = angle + step * 0.2
                radius = 180 + rand.randint(40, 160)
                points.append(
                    (
                        center[0] + math.cos(theta) * radius,
                        center[1] + math.sin(theta) * radius,
                    )
                )
            draw.polygon(points, outline=(90, 70, 60, 255), fill=(210, 190, 150, 90))
            lx = sum(p[0] for p in points) / len(points)
            ly = sum(p[1] for p in points) / len(points)
            draw.text((lx - 80, ly - 20), name, font=font, fill=(70, 50, 45, 255))
        draw.ellipse(
            (
                center[0] - 60,
                center[1] - 60,
                center[0] + 60,
                center[1] + 60,
            ),
            fill=(160, 130, 110, 255),
            outline=(60, 40, 35, 255),
            width=4,
        )
        draw.text(
            (center[0] - 90, center[1] - 20),
            "Varenhold",
            font=font,
            fill=(40, 30, 30, 255),
        )
        draw.line(
            (center[0] - 400, center[1] + 180, center[0] + 400, center[1] + 220),
            fill=(60, 90, 120, 255),
            width=12,
        )

    result = img.convert("RGB")
    return result


def render_diagram(spec: ImageSpec) -> Image.Image:
    img = create_parchment(spec.seed)
    draw = ImageDraw.Draw(img, "RGBA")
    font = load_font(48)
    center = (WIDTH / 2, HEIGHT / 2)
    radius = 260
    for i in range(10):
        angle = (2 * math.pi / 10) * i - math.pi / 2
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        draw.ellipse(
            (x - 35, y - 35, x + 35, y + 35), outline=(80, 60, 50, 255), width=4
        )
        draw.text((x - 15, y - 20), str(i + 1), font=font, fill=(50, 40, 33, 255))
        draw.line((center[0], center[1], x, y), fill=(110, 90, 70, 200), width=3)
    draw.ellipse(
        (
            center[0] - radius - 30,
            center[1] - radius - 30,
            center[0] + radius + 30,
            center[1] + radius + 30,
        ),
        outline=(130, 100, 80, 180),
        width=6,
    )
    draw.text(
        (WIDTH * 0.65, HEIGHT * 0.2), "6 seconds", font=font, fill=(60, 40, 35, 255)
    )
    result = img.convert("RGB")
    return result


def render_tabletop(spec: ImageSpec) -> Image.Image:
    rand = random.Random(spec.seed)
    img = base_canvas((120, 85, 60), (70, 45, 35), spec.seed).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    for x in range(0, WIDTH, 60):
        draw.line((x, 0, x, HEIGHT), fill=(80, 55, 40, 120), width=2)

    for _ in range(6):
        x = rand.randint(160, WIDTH - 200)
        y = rand.randint(120, HEIGHT - 200)
        w = rand.randint(160, 300)
        h = rand.randint(120, 200)
        draw.rectangle((x, y, x + w, y + h), fill=(230, 220, 200, 255))
        draw.line((x, y, x + w, y + h), fill=(150, 130, 110, 255), width=2)

    draw.rectangle((WIDTH * 0.65, 140, WIDTH * 0.9, 360), fill=(210, 190, 140, 255))
    draw.ellipse((320, 160, 420, 260), fill=(200, 30, 30, 255))
    draw.polygon(
        ((500, 500), (560, 520), (540, 580), (480, 560)),
        fill=(90, 110, 150, 255),
    )
    draw_lantern(draw, WIDTH * 0.8, HEIGHT * 0.3, radius=20)
    draw.rectangle(
        (WIDTH * 0.2, HEIGHT * 0.65, WIDTH * 0.45, HEIGHT * 0.78),
        fill=(190, 150, 110, 255),
    )
    draw.text(
        (WIDTH * 0.22, HEIGHT * 0.67),
        "Varenhold",
        font=load_font(48),
        fill=(60, 40, 30, 255),
    )

    result = img.convert("RGB")
    return result


def render_image(spec: ImageSpec) -> Image.Image:
    if spec.category == "city":
        return render_city(spec)
    if spec.category == "land":
        return render_land(spec)
    if spec.category == "interior":
        return render_interior(spec)
    if spec.category == "portrait":
        return render_portrait(spec)
    if spec.category == "document":
        return render_document(spec)
    if spec.category == "map":
        return render_map(spec)
    if spec.category == "diagram":
        return render_diagram(spec)
    if spec.category == "tabletop":
        return render_tabletop(spec)
    raise ValueError(f"Unknown category: {spec.category}")


IMAGE_SPECS: Sequence[ImageSpec] = [
    ImageSpec(
        "amber-lantern-concert",
        "interior",
        ["lanterns", "stage", "musicians", "audience"],
    ),
    ImageSpec("amber-workshop-interior", "interior", ["lanterns", "benches", "tools"]),
    ImageSpec(
        "ashfen-gate-arrival", "city", ["walls", "gate", "road", "lanterns", "figures"]
    ),
    ImageSpec("ashfen-marsh-travel", "land", ["marsh", "road", "reeds", "traveler"]),
    ImageSpec("ashfen-wayshrine", "land", ["wayshrine", "offerings", "lanterns"]),
    ImageSpec("ashring-scorched-stones", "land", ["circle", "heron"]),
    ImageSpec(
        "ceva-doss-sunlight-painting", "interior", ["lanterns", "painting", "tables"]
    ),
    ImageSpec("character-creation-table", "tabletop", []),
    ImageSpec("corven-notebook", "document", ["notebook"]),
    ImageSpec("corven-sealed-letter", "document", ["letter"]),
    ImageSpec("council-hall-interior", "interior", ["council", "lanterns", "chairs"]),
    ImageSpec("dawnborn-trio", "portrait", ["halo"], meta={"count": 3}),
    ImageSpec(
        "dawnhall-food-kitchen",
        "interior",
        ["kitchen", "lanterns", "tables", "audience"],
    ),
    ImageSpec("erem-wadewalker", "land", ["marsh", "reeds", "traveler"]),
    ImageSpec(
        "god-auris",
        "portrait",
        ["halo", "shrine", "accent-line"],
        meta={"accent_color": (230, 190, 120)},
    ),
    ImageSpec("god-dara", "portrait", ["lantern", "shrine", "accent-line"]),
    ImageSpec("god-morthis", "portrait", ["halo", "hands"]),
    ImageSpec("god-twin-crowns", "portrait", ["halo", "crown", "accent-line"]),
    ImageSpec("god-veth", "portrait", ["lantern", "book"]),
    ImageSpec("god-wanderer", "land", ["wayshrine", "road", "traveler", "lanterns"]),
    ImageSpec(
        "grey-sickness-ward",
        "interior",
        ["beds", "lanterns", "practitioner", "patients"],
    ),
    ImageSpec(
        "high-passes-shadow-cloth",
        "land",
        ["road", "traveler"],
        meta={"sky_top": (140, 130, 120), "foreground": (80, 75, 70)},
    ),
    ImageSpec("highmark-council-hall", "city", ["walls", "gate", "lanterns", "road"]),
    ImageSpec("inversion-circle-diagram", "diagram", []),
    ImageSpec(
        "lowmark-care-house",
        "interior",
        ["beds", "painting", "lanterns", "practitioner", "patients"],
    ),
    ImageSpec(
        "map-graymere-reaches",
        "map",
        [],
        meta={
            "territories": [
                "Solenne",
                "Graymere Holds",
                "Arveth Compact",
                "Ashfen Clans",
                "Dusk Parishes",
            ]
        },
    ),
    ImageSpec("moral-scorecard-table", "document", ["scorecard"]),
    ImageSpec("npc-brother-edoran", "portrait", ["hands", "accent-line"]),
    ImageSpec("npc-chancellor-ostenveld", "portrait", ["lantern", "accent-line"]),
    ImageSpec("npc-lira-cain", "portrait", ["satchel", "lantern"]),
    ImageSpec("npc-sera-voss", "portrait", ["halo"]),
    ImageSpec("npc-theron-waide", "portrait", ["book"]),
    ImageSpec(
        "restorer-compound-dawn", "city", ["walls", "road", "lanterns", "figures"]
    ),
    ImageSpec(
        "session1-chancellors-study",
        "interior",
        ["fireplace", "desk", "documents", "lanterns"],
    ),
    ImageSpec("session1-opening", "interior", ["shelves", "lanterns", "documents"]),
    ImageSpec("session2-opening", "diagram", []),
    ImageSpec(
        "session2-theron-disclosure",
        "interior",
        ["desk", "documents", "figure", "lanterns"],
    ),
    ImageSpec("session3-isolde-lab", "interior", ["lab", "tools", "lanterns"]),
    ImageSpec("session3-opening", "interior", ["lab", "rods", "lanterns"]),
    ImageSpec("session4-opening", "land", ["circle", "glow", "lanterns"]),
    ImageSpec("session4-reckoning-street", "city", ["circle", "figures", "lanterns"]),
    ImageSpec("session5-ashring-assembly", "land", ["circle", "figures", "glow"]),
    ImageSpec("session5-opening", "land", ["circle", "lanterns"]),
    ImageSpec("the-dawnborn-public", "city", ["crowd", "lanterns", "figures"]),
    ImageSpec("the-desperate-lowmark", "city", ["crowd", "lanterns", "road"]),
    ImageSpec("the-night-of-the-ritual", "land", ["circle", "glow"]),
    ImageSpec("the-spire-tower", "city", ["tower", "lanterns"]),
    ImageSpec("theron-archive-stacks", "interior", ["shelves", "lanterns", "figure"]),
    ImageSpec(
        "varenhold-district-map",
        "map",
        [],
        meta={
            "variant": "city",
            "districts": [
                "Ashring",
                "Lowmark",
                "Spire",
                "Dawnhalls",
                "Outer Ring",
                "Ashfen Gate",
            ],
        },
    ),
    ImageSpec("varenhold-last-morning", "land", ["circle", "glow"]),
    ImageSpec(
        "varenhold-river-approach",
        "city",
        ["river", "bridge", "lanterns", "tower", "walls"],
    ),
    ImageSpec("varenhold-twilight-cityscape", "city", ["river", "lanterns", "tower"]),
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in IMAGE_SPECS:
        image = render_image(spec)
        output_path = OUTPUT_DIR / f"{spec.name}.png"
        image.save(output_path, "PNG")
        print(f"Generated {output_path.name}")


if __name__ == "__main__":
    main()
