import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(sys.argv[1])
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
KALAM = "kalam-300-latin.woff2"


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
    open_d, open_w = outline("“", CAVEAT, 54, 4, 222, 700)
    motto_d, motto_w = outline(
        "The exceptional, you have to go and get it.", KALAM, 27, 4 + open_w + 4, 216
    )
    close_d, close_w = outline("”", CAVEAT, 54, 4 + open_w + 8 + motto_w, 222, 700)
    width = max(name_w, open_w + motto_w + close_w + 8) + 24
    body = (
        f'<path fill="{c["ink"]}" d="{name_d}"/>{under}'
        f'<path fill="{c["soft"]}" d="{open_d}{close_d}"/>'
        f'<path fill="{c["ink"]}" d="{motto_d}"/>'
    )
    return svg(width, 236, body)


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

for theme, c in THEMES.items():
    (OUT / f"header-{theme}.svg").write_text(header(c))
    for slug, text in LABELS.items():
        (OUT / f"{slug}-{theme}.svg").write_text(label(text, c))
