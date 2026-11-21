"""Assemble Before-vs-After progression matrices and 6-camera Cycles showcase sheets.

Run either with system Python (when Pillow is installed) or via Blender's bundled Python:
    blender --background --python build_progression_matrix.py -- --mode matrix ...
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    print(
        "ERROR: Pillow (PIL) is not installed in this Python interpreter.\n"
        "Install with `pip install pillow` OR run using Blender's bundled Python:\n"
        "  blender --background --python build_progression_matrix.py -- <args>",
        file=sys.stderr,
    )
    sys.exit(2)


def _strip_blender_args(argv):
    """Strip Blender flags preceding `--` when invoked via `blender --background --python`."""
    if "--" in argv:
        return argv[argv.index("--") + 1 :]
    return argv


def _load_font(size):
    """Load a crisp sans-serif font with clean fallback to PIL's default font."""
    for name in ("arial.ttf", "DejaVuSans-Bold.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fit_tile(path, tile_w, tile_h, label, header_h=44):
    """Resize and center-fit an image into a dark studio tile with a crisp top label."""
    bg = Image.new("RGB", (tile_w, tile_h + header_h), (18, 20, 24))
    draw = ImageDraw.Draw(bg)
    font = _load_font(22)
    draw.rectangle([(0, 0), (tile_w, header_h)], fill=(28, 31, 38))
    draw.text((16, 10), label, fill=(238, 240, 244), font=font)

    with Image.open(path) as img:
        fitted = ImageOps.contain(img.convert("RGB"), (tile_w, tile_h), method=Image.Resampling.LANCZOS)
    ox = (tile_w - fitted.width) // 2
    oy = header_h + (tile_h - fitted.height) // 2
    bg.paste(fitted, (ox, oy))
    return bg


def compose_grid(pairs, cols, out_path, title, tile_w=960, tile_h=540, gap=16):
    """Compose labeled image pairs into a dark-mode studio sheet."""
    if not pairs:
        raise ValueError("No input images provided.")
    rows = (len(pairs) + cols - 1) // cols
    header_h = 44
    title_h = 64 if title else 0
    cell_h = tile_h + header_h

    canvas_w = cols * tile_w + (cols + 1) * gap
    canvas_h = title_h + rows * cell_h + (rows + 1) * gap
    canvas = Image.new("RGB", (canvas_w, canvas_h), (12, 13, 16))
    draw = ImageDraw.Draw(canvas)

    if title:
        title_font = _load_font(30)
        draw.text((gap, 16), title, fill=(245, 247, 250), font=title_font)

    for idx, (img_path, label) in enumerate(pairs):
        r, c = divmod(idx, cols)
        x = gap + c * (tile_w + gap)
        y = title_h + gap + r * (cell_h + gap)
        tile = _fit_tile(img_path, tile_w, tile_h, label, header_h=header_h)
        canvas.paste(tile, (x, y))

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=95)
    print(f"Saved: {out_path} ({canvas_w}x{canvas_h})")


def main():
    parser = argparse.ArgumentParser(description="Build Blender architectural showcase & progression sheets.")
    parser.add_argument("--mode", choices=["matrix", "showcase"], required=True)
    parser.add_argument("--output", required=True, help="Output PNG path.")
    parser.add_argument("--title", default="", help="Optional top banner title.")
    parser.add_argument(
        "--images",
        nargs="+",
        required=True,
        help="Input image paths (matrix: pairs like before1 after1 [before2 after2]; showcase: 6 camera PNGs).",
    )
    parser.add_argument(
        "--labels",
        nargs="*",
        default=None,
        help="Optional labels matching --images.",
    )
    args = parser.parse_args(_strip_blender_args(sys.argv[1:]))

    if args.mode == "matrix":
        default_labels = [f"Stage {i + 1}" for i in range(len(args.images))]
        if len(args.images) == 2:
            default_labels = ["BEFORE (Stage 01 Massing / Baseline)", "AFTER (Studio Polish + Cycles Final)"]
        elif len(args.images) == 4:
            default_labels = [
                "BEFORE — Hero 3/4",
                "AFTER — Hero 3/4 (Cycles Studio Polish)",
                "BEFORE — Site Overview",
                "AFTER — Site Overview (Cycles Studio Polish)",
            ]
        labels = args.labels if args.labels and len(args.labels) == len(args.images) else default_labels
        title = args.title or "Architectural Environment Production — Before vs. After Progression Matrix"
        compose_grid(list(zip(args.images, labels)), cols=2, out_path=args.output, title=title)
    else:
        default_labels = [
            "Cam 01 — Hero 3/4 Exterior",
            "Cam 02 — Aerial Site Overview",
            "Cam 03 — Eye-Level Threshold",
            "Cam 04 — Architectural Detail Close-Up",
            "Cam 05 — Atmospheric Courtyard / Interior",
            "Cam 06 — Section A-A BMesh Cutaway",
        ]
        labels = args.labels if args.labels and len(args.labels) == len(args.images) else default_labels[: len(args.images)]
        title = args.title or "Architectural Environment Production — 6-Camera Cycles Showcase"
        compose_grid(list(zip(args.images, labels)), cols=3, out_path=args.output, title=title, tile_w=800, tile_h=450)


if __name__ == "__main__":
    main()
