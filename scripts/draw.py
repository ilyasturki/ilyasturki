import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SITE = Path(sys.argv[1])
FONTS = SITE / "public/fonts"
ICONS = SITE / "src/css/sketch/icons"
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "light": {"ink": "#262626", "soft": "#5c5c5c"},
    "dark": {"ink": "#ededed", "soft": "#a8a8a8"},
}

_cache = {}


def face(file, wght=None):
    key = (file, wght)
    if key not in _cache:
        font = TTFont(FONTS / file)
        loc = {"wght": wght} if wght else None
        _cache[key] = (font, font.getGlyphSet(location=loc))
    return _cache[key]


def outline(text, file, size, x, y, wght=None):
    font, glyphs = face(file, wght)
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    cursor = 0.0
    for ch in text:
        name = cmap[ord(ch)]
        glyph = glyphs[name]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x + cursor, y)))
        cursor += glyph.width * scale
    return pen.getCommands(), cursor


CAVEAT = "caveat-latin-wght.woff2"
QUOTE_TAILS = "M7.5 1.5 C 4 3.6, 2.6 7, 3.8 11.2 M15.5 1.5 C 12 3.6, 10.6 7, 11.8 11.2"
QUOTE_DOTS = (
    "M2.2 11.6 a1.7 1.7 0 1 0 3.4 0 a1.7 1.7 0 1 0 -3.4 0 "
    "M10.2 11.6 a1.7 1.7 0 1 0 3.4 0 a1.7 1.7 0 1 0 -3.4 0"
)


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" '
        f'viewBox="0 0 {w:.0f} {h}">{body}</svg>\n'
    )


def header(c):
    name_d, name_w = outline("Ilyas Turki", CAVEAT, 118, 4, 104, 700)
    k = name_w / 590
    under = (
        f'<path d="M6 146 C {6+114*k:.1f} 137, {6+254*k:.1f} 150, {6+414*k:.1f} 141 '
        f'S {6+554*k:.1f} 138, {6+588*k:.1f} 144" fill="none" stroke="{c["ink"]}" '
        f'stroke-width="2.6" stroke-linecap="round"/>'
        f'<path d="M{6+542*k:.1f} 152 C {6+424*k:.1f} 157, {6+324*k:.1f} 149, {6+208*k:.1f} 155" '
        f'fill="none" stroke="{c["soft"]}" stroke-width="1.6" stroke-linecap="round"/>'
    )
    em, base = 34, 214
    k = 0.625 * em / 20
    top = base - 0.92 * em
    mark = (
        f'<path d="{QUOTE_TAILS}" fill="none" stroke="{c["ink"]}" stroke-width="1.7" '
        f'stroke-linecap="round"/><path d="{QUOTE_DOTS}" fill="{c["ink"]}"/>'
    )
    text_x = 4 + 20 * k + 0.08 * em
    motto_d, motto_w = outline(
        "The exceptional, you have to go and get it.", CAVEAT, em, text_x, base, 500
    )
    close_x = text_x + motto_w + 0.06 * em
    motto = (
        f'<g transform="translate(4 {top:.1f}) scale({k:.3f})">{mark}</g>'
        f'<path fill="{c["ink"]}" d="{motto_d}"/>'
        f'<g transform="translate({close_x:.1f} {top:.1f}) scale({k:.3f}) rotate(180 10 8)">{mark}</g>'
    )
    # The site slants the motto from its baseline, as written by hand.
    slant = f'<g transform="translate(4 {base}) skewX(-11) translate(-4 -{base})">{motto}</g>'
    width = max(name_w, close_x + 20 * k) + 24
    body = f'<path fill="{c["ink"]}" d="{name_d}"/>{under}{slant}'
    return svg(width, 232, body)


def label(text, c):
    d, w = outline(text, CAVEAT, 42, 2, 38, 600)
    end = 2 + w * 0.95
    under = (
        f'<path d="M2 50 C {2+(end-2)*0.3:.1f} 45, {2+(end-2)*0.62:.1f} 52, {end:.1f} 46" '
        f'fill="none" stroke="{c["soft"]}" stroke-width="1.8" stroke-linecap="round"/>'
    )
    return svg(w + 8, 58, f'<path fill="{c["ink"]}" d="{d}"/>{under}')


LABELS = {
    "closed-doors": "behind closed doors",
    "machines": "the machines",
    "how-i-work": "how I work",
    "journal": "journal",
}

def site_icon(name, c):
    source = (ICONS / f"{name}.svg").read_text()
    return source.replace("<svg ", f'<svg width="20" height="20" fill="{c["ink"]}" ', 1)


def drawn_icon(strokes, c):
    body = "".join(
        f'<path d="{d}" fill="none" stroke="{c["ink"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        for d in strokes
    )
    shadow = (
        f'<path d="M5 22.2 C 9 21.6, 14 22.6, 19 21.9" fill="none" stroke="{c["ink"]}" '
        f'stroke-opacity="0.4" stroke-width="1.6" stroke-linecap="round"/>'
    )
    return svg(20, 20, "").replace(
        'viewBox="0 0 20 20">', f'viewBox="0 0 24 24">{body}{shadow}'
    )


SNOWFLAKE = [
    "M12.1 2.6 C 11.9 6, 12.2 9, 11.9 12.4 C 12.1 15, 11.8 17.6, 12 20.1",
    "M4.4 7.2 C 7.2 8.7, 9.6 10.2, 12 11.4 C 14.6 12.9, 17 14.3, 19.6 16",
    "M19.5 7 C 16.8 8.6, 14.3 10.1, 12 11.5 C 9.5 13.1, 7 14.5, 4.5 16.1",
    "M9.9 3.9 L 12.1 5.6 L 14.2 3.8",
    "M9.8 19 L 12 17.2 L 14.1 19.1",
    "M4.6 9.9 L 7.2 8.7 L 6.8 6",
    "M17.2 18 L 16.8 15.3 L 19.4 14.1",
    "M17.1 5.1 L 16.8 7.9 L 19.5 9.1",
    "M4.5 13.6 L 7.1 14.8 L 6.8 17.6",
]

SERVER = [
    "M4.6 4.2 C 9 3.8, 15 4.3, 19.5 4 C 19.8 6.2, 19.6 8.5, 19.7 10.3 "
    "C 15 10.7, 9 10.2, 4.4 10.5 C 4.2 8.4, 4.5 6.3, 4.6 4.2",
    "M4.5 13 C 9 12.6, 15 13.1, 19.6 12.8 C 19.8 15, 19.5 17.2, 19.7 19 "
    "C 15 19.4, 9 18.9, 4.4 19.2 C 4.2 17.1, 4.6 15, 4.5 13",
    "M7.4 7.3 L 7.5 7.4",
    "M7.4 16 L 7.5 16.1",
    "M11 7.4 C 13 7.2, 15 7.5, 17 7.3",
    "M11 16.1 C 13 15.9, 15 16.2, 17 16",
]

for theme, c in THEMES.items():
    (OUT / f"icon-aplorio-{theme}.svg").write_text(site_icon("aplorio", c))
    (OUT / f"icon-site-{theme}.svg").write_text(site_icon("crayon", c))
    (OUT / f"icon-nix-config-{theme}.svg").write_text(drawn_icon(SNOWFLAKE, c))
    (OUT / f"icon-infra-apps-{theme}.svg").write_text(drawn_icon(SERVER, c))
    (OUT / f"header-{theme}.svg").write_text(header(c))
    for slug, text in LABELS.items():
        (OUT / f"{slug}-{theme}.svg").write_text(label(text, c))
