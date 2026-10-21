#!/usr/bin/env python3
"""Compose a KDP-style paperback wrap from predesigned front and back panels."""

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


DPI = 300
BLEED = 0.125
PAPER_MULTIPLIERS = {
    "white": 0.002252,
    "cream": 0.0025,
    "groundwood": 0.00235,
}


def parse_trim(value: str) -> tuple[float, float]:
    try:
        width, height = (float(part) for part in value.lower().split("x", 1))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("trim must look like 6x9") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("trim dimensions must be positive")
    return width, height


def even_pages(pages: int) -> int:
    if pages < 24:
        raise ValueError("page count must be at least 24")
    return pages + pages % 2


def dimensions(pages: int, paper: str, trim: tuple[float, float], dpi: int = DPI) -> tuple[int, int, int]:
    page_count = even_pages(pages)
    spine = page_count * PAPER_MULTIPLIERS[paper]
    width = round((2 * trim[0] + spine + 2 * BLEED) * dpi)
    height = round((trim[1] + 2 * BLEED) * dpi)
    spine_width = round((trim[0] + BLEED + spine) * dpi) - round((trim[0] + BLEED) * dpi)
    return width, height, spine_width


def default_font() -> str | None:
    for path in (
        "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    ):
        if Path(path).exists():
            return path
    return None


def build_cover(
    front_path: Path,
    back_path: Path,
    output: Path,
    pages: int,
    paper: str,
    trim: tuple[float, float],
    spine_text: str = "",
    font_path: str | None = None,
) -> tuple[int, int, int]:
    width, height, spine_width = dimensions(pages, paper, trim)
    back_end = round((trim[0] + BLEED) * DPI)
    spine_end = back_end + spine_width

    canvas = Image.new("RGB", (width, height), "black")
    with Image.open(back_path) as source:
        back = ImageOps.fit(source.convert("RGB"), (back_end, height), Image.Resampling.LANCZOS)
    with Image.open(front_path) as source:
        front = ImageOps.fit(source.convert("RGB"), (width - spine_end, height), Image.Resampling.LANCZOS)
    canvas.paste(back, (0, 0))
    canvas.paste(front, (spine_end, 0))

    if spine_text:
        selected_font = font_path or default_font()
        if not selected_font:
            raise ValueError("provide --font when adding spine text")
        font = ImageFont.truetype(selected_font, 36)
        box = font.getbbox(spine_text)
        strip = Image.new("RGBA", (box[2] - box[0] + 30, box[3] - box[1] + 26), (0, 0, 0, 0))
        ImageDraw.Draw(strip).text((15 - box[0], 13 - box[1]), spine_text, font=font, fill=(220, 230, 235, 255))
        strip = strip.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
        safe_width = spine_width - 2 * round(0.0625 * DPI)
        if strip.width > safe_width:
            raise ValueError(f"spine text is too wide for the {spine_width}px spine")
        canvas.paste(strip, (back_end + (spine_width - strip.width) // 2, (height - strip.height) // 2), strip)

    output.parent.mkdir(parents=True, exist_ok=True)
    preview = output.with_suffix(".jpg")
    canvas.save(preview, "JPEG", quality=96, subsampling=0, dpi=(DPI, DPI))
    canvas.save(output, "PDF", resolution=DPI, quality=100)
    return width, height, spine_width


def self_check() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for name, color in (("front.png", "navy"), ("back.png", "black")):
            Image.new("RGB", (600, 900), color).save(root / name)
        result = build_cover(root / "front.png", root / "back.png", root / "cover.pdf", 101, "groundwood", (6, 9))
        assert result == dimensions(102, "groundwood", (6, 9))
        assert (root / "cover.pdf").exists() and (root / "cover.jpg").exists()
    print("build_kdp_cover self-check passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--front", type=Path)
    parser.add_argument("--back", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pages", type=int)
    parser.add_argument("--paper", choices=tuple(PAPER_MULTIPLIERS))
    parser.add_argument("--trim", type=parse_trim, default=(6, 9))
    parser.add_argument("--spine-text", default="")
    parser.add_argument("--font")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    missing_args = [name for name in ("front", "back", "output", "pages", "paper") if getattr(args, name) is None]
    if missing_args:
        parser.error("missing arguments: " + ", ".join(f"--{name}" for name in missing_args))
    if args.output.suffix.lower() != ".pdf":
        parser.error("--output must end in .pdf")
    missing = [str(path) for path in (args.front, args.back) if not path.is_file()]
    if missing:
        parser.error("missing input: " + ", ".join(missing))
    width, height, spine = build_cover(
        args.front,
        args.back,
        args.output,
        args.pages,
        args.paper,
        args.trim,
        args.spine_text,
        args.font,
    )
    print(f"{args.output}: {width}x{height}px; spine {spine}px; {even_pages(args.pages)} pages")


if __name__ == "__main__":
    main()
