#!/usr/bin/env python3
"""Normalize Napkin SVG or PNG colors to Phoenix or Kstudy palettes."""

from __future__ import annotations

import argparse
import colorsys
import re
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass
from pathlib import Path


RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Palette:
    dark: RGB
    primary: RGB
    secondary: RGB
    accent: RGB
    pale: RGB
    muted: RGB
    surface: RGB


PALETTES = {
    "phoenix": Palette(
        dark=(59, 11, 118),
        primary=(110, 44, 202),
        secondary=(142, 93, 232),
        accent=(255, 216, 77),
        pale=(241, 235, 255),
        muted=(107, 112, 153),
        surface=(255, 255, 255),
    ),
    "kstudy": Palette(
        dark=(29, 35, 125),
        primary=(36, 125, 249),
        secondary=(1, 152, 207),
        accent=(255, 216, 77),
        pale=(232, 244, 255),
        muted=(107, 112, 153),
        surface=(255, 255, 255),
    ),
}


COLOR_NAMES = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", choices=tuple(PALETTES), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--clear-edge-white",
        action="store_true",
        help="Make near-white PNG pixels connected to the canvas edge transparent.",
    )
    return parser.parse_args()


def parse_color(value: str) -> RGB | None:
    raw = value.strip().lower()
    if raw in COLOR_NAMES:
        return COLOR_NAMES[raw]
    if raw.startswith("#"):
        code = raw[1:]
        if len(code) in (3, 4):
            code = "".join(char * 2 for char in code[:3])
        elif len(code) in (6, 8):
            code = code[:6]
        else:
            return None
        try:
            return tuple(int(code[index : index + 2], 16) for index in (0, 2, 4))
        except ValueError:
            return None
    match = re.fullmatch(r"rgba?\(([^)]+)\)", raw)
    if match:
        parts = [part.strip() for part in match.group(1).split(",")[:3]]
        if len(parts) != 3:
            return None
        channels: list[int] = []
        try:
            for part in parts:
                if part.endswith("%"):
                    channels.append(round(float(part[:-1]) * 2.55))
                else:
                    channels.append(round(float(part)))
        except ValueError:
            return None
        return tuple(max(0, min(255, channel)) for channel in channels)
    return None


def mix(first: RGB, second: RGB, amount: float) -> RGB:
    return tuple(
        round(first[index] * (1 - amount) + second[index] * amount)
        for index in range(3)
    )


def map_color(rgb: RGB, palette: Palette) -> RGB:
    red, green, blue = (channel / 255 for channel in rgb)
    hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue

    if luminance < 0.23:
        return palette.dark
    if saturation < 0.09:
        if luminance > 0.96:
            return palette.surface
        if luminance > 0.72:
            return palette.pale
        if luminance > 0.43:
            return palette.muted
        return palette.dark

    warm_accent = 0.08 <= hue <= 0.19
    if warm_accent:
        if luminance > 0.84:
            return mix(palette.surface, palette.accent, 0.32)
        if luminance > 0.64:
            return mix(palette.surface, palette.accent, 0.55)
        return palette.accent
    elif 0.42 <= hue <= 0.63:
        target = palette.secondary
    else:
        target = palette.primary

    if luminance > 0.84:
        return mix(palette.pale, target, 0.18)
    if luminance > 0.64:
        return mix(palette.pale, target, 0.38)
    if luminance < 0.39:
        return palette.dark
    return target


def to_hex(rgb: RGB) -> str:
    return "#" + "".join(f"{channel:02X}" for channel in rgb)


def normalize_svg(source: Path, output: Path, palette: Palette) -> None:
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(source)
    root = tree.getroot()
    color_attributes = ("fill", "stroke", "color", "stop-color", "flood-color")
    style_pattern = re.compile(
        r"(?P<key>stop-color|flood-color|fill|stroke|color)\s*:\s*(?P<value>[^;]+)",
        re.IGNORECASE,
    )

    def normalize_value(value: str) -> str:
        parsed = parse_color(value)
        return to_hex(map_color(parsed, palette)) if parsed else value

    for element in root.iter():
        for attribute in color_attributes:
            if attribute in element.attrib:
                element.attrib[attribute] = normalize_value(element.attrib[attribute])
        style = element.attrib.get("style")
        if style:
            element.attrib["style"] = style_pattern.sub(
                lambda match: f"{match.group('key')}:{normalize_value(match.group('value'))}",
                style,
            )

    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def pixel_metrics(rgb: RGB) -> tuple[float, float]:
    red, green, blue = (channel / 255 for channel in rgb)
    _, saturation, _ = colorsys.rgb_to_hsv(red, green, blue)
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return luminance, saturation


def clear_edge_white(image: object) -> None:
    width, height = image.size
    pixels = image.load()
    queue: deque[tuple[int, int]] = deque()
    seen: set[tuple[int, int]] = set()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        red, green, blue, alpha = pixels[x, y]
        luminance, saturation = pixel_metrics((red, green, blue))
        if alpha == 0 or luminance < 0.94 or saturation > 0.10:
            continue
        pixels[x, y] = (red, green, blue, 0)
        if x > 0:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))


def normalize_png(
    source: Path,
    output: Path,
    palette: Palette,
    remove_edge_white: bool,
) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(
            "PNG normalization requires Pillow. Prefer SVG or use a Python runtime with Pillow."
        ) from exc

    image = Image.open(source).convert("RGBA")
    if remove_edge_white:
        clear_edge_white(image)
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            if alpha == 0:
                continue
            mapped = map_color((red, green, blue), palette)
            pixels[x, y] = (*mapped, alpha)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main() -> None:
    args = parse_args()
    suffix = args.input.suffix.lower()
    if suffix != args.output.suffix.lower():
        raise SystemExit("Input and output formats must match.")
    palette = PALETTES[args.brand]
    if suffix == ".svg":
        if args.clear_edge_white:
            raise SystemExit("--clear-edge-white is only available for PNG input.")
        normalize_svg(args.input, args.output, palette)
    elif suffix == ".png":
        normalize_png(args.input, args.output, palette, args.clear_edge_white)
    else:
        raise SystemExit("Supported formats: SVG and PNG.")
    print(args.output)


if __name__ == "__main__":
    main()
