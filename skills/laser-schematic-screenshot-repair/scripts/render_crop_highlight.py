#!/usr/bin/env python3
"""Render a PDF page, crop it, optionally draw precise highlight boxes."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, Tuple

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyMuPDF is required: pip install pymupdf") from exc

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: pip install pillow") from exc


Rect = Tuple[int, int, int, int]
Color = Tuple[int, int, int]


def parse_rect(value: str) -> Rect:
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected x1,y1,x2,y2")
    try:
        rect = tuple(int(p) for p in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("rect values must be integers") from exc
    x1, y1, x2, y2 = rect
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError("rect must satisfy x2>x1 and y2>y1")
    return rect  # type: ignore[return-value]


def parse_color(value: str) -> Color:
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("expected r,g,b")
    try:
        color = tuple(int(p) for p in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color values must be integers") from exc
    if any(p < 0 or p > 255 for p in color):
        raise argparse.ArgumentTypeError("color values must be in 0..255")
    return color  # type: ignore[return-value]


def validate_rect_inside(rect: Rect, width: int, height: int, label: str) -> None:
    x1, y1, x2, y2 = rect
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        raise SystemExit(
            f"{label} {rect} is outside image bounds {width}x{height}"
        )


def render_page(pdf_path: Path, page_number: int, scale: float) -> Image.Image:
    if page_number < 1:
        raise SystemExit("--page is 1-based and must be >= 1")
    doc = fitz.open(pdf_path)
    try:
        if page_number > doc.page_count:
            raise SystemExit(f"PDF has {doc.page_count} pages; requested {page_number}")
        page = doc.load_page(page_number - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        mode = "RGB" if pix.n == 3 else "RGBA"
        return Image.frombytes(mode, (pix.width, pix.height), pix.samples).convert("RGB")
    finally:
        doc.close()


def draw_boxes(
    image: Image.Image,
    boxes: Iterable[Rect],
    color: Color,
    width: int,
) -> None:
    draw = ImageDraw.Draw(image)
    for rect in boxes:
        validate_rect_inside(rect, image.width, image.height, "--box")
        x1, y1, x2, y2 = rect
        for offset in range(width):
            draw.rectangle(
                (x1 - offset, y1 - offset, x2 + offset, y2 + offset),
                outline=color,
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path, help="source PDF path")
    parser.add_argument("--page", required=True, type=int, help="1-based page number")
    parser.add_argument("--scale", type=float, default=8.0, help="render scale")
    parser.add_argument("--crop", type=parse_rect, help="crop rect in rendered-page pixels")
    parser.add_argument(
        "--box",
        action="append",
        type=parse_rect,
        default=[],
        help="highlight rect in cropped-image pixels; repeatable",
    )
    parser.add_argument("--box-width", type=int, default=3, help="highlight line width")
    parser.add_argument("--color", type=parse_color, default=(210, 0, 0), help="r,g,b")
    parser.add_argument("--output", required=True, type=Path, help="output PNG path")
    parser.add_argument("--render-output", type=Path, help="optional full-page render PNG")
    parser.add_argument(
        "--backup-existing",
        action="store_true",
        help="copy existing output to .old_lowres.png before overwriting",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"source PDF not found: {args.pdf}")
    if args.scale <= 0:
        raise SystemExit("--scale must be positive")
    if args.box_width < 1:
        raise SystemExit("--box-width must be >= 1")

    image = render_page(args.pdf, args.page, args.scale)
    if args.render_output:
        args.render_output.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.render_output)

    if args.crop:
        validate_rect_inside(args.crop, image.width, image.height, "--crop")
        image = image.crop(args.crop)

    draw_boxes(image, args.box, args.color, args.box_width)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.backup_existing and args.output.exists():
        backup = args.output.with_name(args.output.stem + ".old_lowres" + args.output.suffix)
        if not backup.exists():
            shutil.copy2(args.output, backup)

    image.save(args.output)
    print(f"output={args.output}")
    print(f"size={image.width}x{image.height}")
    print(f"bytes={args.output.stat().st_size}")


if __name__ == "__main__":
    main()
