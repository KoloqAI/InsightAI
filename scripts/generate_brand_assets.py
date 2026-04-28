"""Generate Insight brand assets (favicon + logos) from a single source design.

Outputs:
    web/public/insight.svg              (theme-aware SVG favicon, light/dark)
    web/public/insight.ico              (16/32/48 px multi-resolution ICO)
    web/public/logo.png                 (400x400 light-theme square mark)
    web/public/logotype.png             (2640x733 light-theme wordmark)
    web/public/logotype-dark.png        (720x320 dark-theme wordmark)
    backend/static/images/logo.png      (512x512 square, used by API + brand seed)
    backend/static/images/logotype.png  (1024x256 wordmark, used by brand seed)

Design philosophy
-----------------
Minimal, monochrome, matches the app's existing palette:

    light theme  -> ink #1C1C1C glyph on transparent
    dark  theme  -> chrome #E9E9E9 glyph on transparent

No coloured plate, no gradient. Letter-i mark + "Insight" wordmark in a
clean bold sans-serif, mirroring the Onyx-style aesthetic.

Re-run any time the brand needs to change. After running, restart the web
server (favicon files + public assets are baked at build time) and re-run
scripts/insight_brand.py to push the new logo PNGs into the running stack.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent

WEB_PUBLIC = REPO_ROOT / "web" / "public"
BACKEND_STATIC = REPO_ROOT / "backend" / "static" / "images"

INK = (28, 28, 28, 255)
CHROME = (233, 233, 233, 255)


def _load_font(target_height_px: int) -> ImageFont.FreeTypeFont:
    """Pick a bold sans-serif font for wordmarks."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, target_height_px)
    return ImageFont.load_default()


def _load_serif_italic(target_height_px: int) -> ImageFont.FreeTypeFont:
    """Pick a serif italic font for the "info" glyph (information-symbol look)."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "/Library/Fonts/Georgia.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, target_height_px)
    return _load_font(target_height_px)


def _measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox, bbox[2] - bbox[0], bbox[3] - bbox[1]


def make_square_mark(size: int, fg: tuple[int, int, int, int]) -> Image.Image:
    """Information glyph: serif italic 'i' inside a circular frame.

    Mirrors the universal info symbol (Unicode U+24D8 'CIRCLED LATIN SMALL
    LETTER I'). Transparent background, monochrome stroke + glyph in `fg`.
    """
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    stroke_w = max(2, int(size * 0.06))
    pad = stroke_w // 2 + max(1, int(size * 0.01))
    draw.ellipse(
        [(pad, pad), (size - 1 - pad, size - 1 - pad)],
        outline=fg,
        width=stroke_w,
    )

    font = _load_serif_italic(int(size * 0.66))
    bbox, text_w, text_h = _measure(draw, "i", font)
    x = (size - text_w) // 2 - bbox[0]
    y = (size - text_h) // 2 - bbox[1]
    draw.text((x, y), "i", font=font, fill=fg)
    return image


def make_wordmark(
    width: int,
    height: int,
    fg: tuple[int, int, int, int],
    include_mark: bool = True,
) -> Image.Image:
    """Horizontal Insight wordmark, transparent background.

    If include_mark, paints the square 'i' mark on the left and "Insight" to
    the right (with a small gap). Otherwise just paints the word centered.
    """
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    text = "Insight"

    if include_mark:
        mark_size = height
        mark = make_square_mark(mark_size, fg)
        image.paste(mark, (0, 0), mark)
        font_size = int(height * 0.62)
        font = _load_font(font_size)
        bbox, text_w, text_h = _measure(draw, text, font)
        x = mark_size + int(height * 0.10) - bbox[0]
        y = (height - text_h) // 2 - bbox[1]
        draw.text((x, y), text, font=font, fill=fg)
    else:
        font_size = int(height * 0.78)
        font = _load_font(font_size)
        bbox, text_w, text_h = _measure(draw, text, font)
        x = (width - text_w) // 2 - bbox[0]
        y = (height - text_h) // 2 - bbox[1]
        draw.text((x, y), text, font=font, fill=fg)

    return image


# Theme-aware SVG favicon: information glyph, dark in light browsers, light in dark.
SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <style>
    .ink { stroke: #1C1C1C; fill: #1C1C1C; }
    @media (prefers-color-scheme: dark) {
      .ink { stroke: #E9E9E9; fill: #E9E9E9; }
    }
  </style>
  <circle cx="32" cy="32" r="28" fill="none" stroke-width="4" class="ink" />
  <text x="32" y="48" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', Times, serif"
        font-style="italic" font-size="42" font-weight="700"
        stroke="none" class="ink">i</text>
</svg>
"""


def main() -> None:
    WEB_PUBLIC.mkdir(parents=True, exist_ok=True)
    BACKEND_STATIC.mkdir(parents=True, exist_ok=True)

    svg_path = WEB_PUBLIC / "insight.svg"
    svg_path.write_text(SVG_TEMPLATE, encoding="utf-8")
    print(f"[ok] wrote {svg_path.relative_to(REPO_ROOT)}")

    ico_path = WEB_PUBLIC / "insight.ico"
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    make_square_mark(256, INK).save(ico_path, format="ICO", sizes=ico_sizes)
    print(f"[ok] wrote {ico_path.relative_to(REPO_ROOT)}  ({ico_sizes})")

    pub_logo = WEB_PUBLIC / "logo.png"
    make_square_mark(400, INK).save(pub_logo, format="PNG")
    print(f"[ok] wrote {pub_logo.relative_to(REPO_ROOT)}  (400x400 light)")

    pub_logotype = WEB_PUBLIC / "logotype.png"
    make_wordmark(2640, 733, INK).save(pub_logotype, format="PNG")
    print(f"[ok] wrote {pub_logotype.relative_to(REPO_ROOT)}  (2640x733 light)")

    pub_logotype_dark = WEB_PUBLIC / "logotype-dark.png"
    make_wordmark(720, 320, CHROME).save(pub_logotype_dark, format="PNG")
    print(
        f"[ok] wrote {pub_logotype_dark.relative_to(REPO_ROOT)}  (720x320 dark)"
    )

    api_logo = BACKEND_STATIC / "logo.png"
    make_square_mark(512, INK).save(api_logo, format="PNG")
    print(f"[ok] wrote {api_logo.relative_to(REPO_ROOT)}  (512x512 api)")

    api_logotype = BACKEND_STATIC / "logotype.png"
    make_wordmark(1024, 256, INK).save(api_logotype, format="PNG")
    print(f"[ok] wrote {api_logotype.relative_to(REPO_ROOT)}  (1024x256 api)")

    print(
        "\n[done] Assets generated.\n"
        "Next:\n"
        "  1. (web/public)        Rebuild & restart web_server.\n"
        "  2. (backend api logo)  python scripts/insight_brand.py\n"
        "  3. Hard-refresh the browser."
    )


if __name__ == "__main__":
    main()
