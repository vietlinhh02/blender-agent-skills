"""Write a credited preview PNG without modifying the source image."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def watermark(source, destination, label, font_path):
    with Image.open(source) as original:
        preview = ImageOps.exif_transpose(original).convert("RGBA")
    width, height = preview.size
    margin = max(2, round(min(width, height) * 0.025))
    padding = max(2, margin // 2)
    draw_layer = Image.new("RGBA", preview.size)
    draw = ImageDraw.Draw(draw_layer)
    font_size = max(8, min(36, round(min(width, height) * 0.05)))

    while font_size >= 6:
        font = (ImageFont.truetype(font_path, font_size) if font_path
                else ImageFont.load_default(size=font_size))
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
        text_width, text_height = right - left, bottom - top
        if (text_width + 2 * (margin + padding) <= width
                and text_height + 2 * (margin + padding) <= height):
            break
        font_size -= 1
    else:
        raise ValueError("Preview is too small for the credit; use a shorter label or a larger preview.")

    x2, y2 = width - margin - 1, height - margin - 1
    x1 = x2 - text_width - 2 * padding + 1
    y1 = y2 - text_height - 2 * padding + 1
    draw.rounded_rectangle((x1, y1, x2, y2), radius=padding, fill=(15, 18, 23, 210))
    draw.text((x1 + padding - left, y1 + padding - top), label,
              font=font, fill=(255, 255, 255, 255))

    credited = Image.alpha_composite(preview, draw_layer)
    with destination.open("xb") as file:
        credited.save(file, format="PNG")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, help="Path for a new PNG")
    parser.add_argument("--text", default="vietlinhh02")
    parser.add_argument("--font", help="Path to a TTF or OTF font")
    args = parser.parse_args()
    label = args.text.strip()
    if not label or "\n" in label or "\r" in label:
        parser.error("credit text must be one nonempty line")
    if args.destination.suffix.lower() != ".png":
        parser.error("destination must be a PNG")
    try:
        watermark(args.source, args.destination, label, args.font)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
