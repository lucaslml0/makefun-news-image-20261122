#!/usr/bin/env python3
"""Draw the 22 November 2026 newspaper front page (1024x1024 PNG).

Fresh implementation: a one-page broadsheet with a masthead, a lead
story, two half-width stories and a three-column row, drawn entirely
with Pillow. No network access; output is deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 34
GUTTER = 16

PAPER = (247, 241, 227)      # warm newsprint
INK = (24, 22, 18)           # near-black
RULE = (24, 22, 18)
RED = (146, 32, 28)          # brick red for kickers
GREY = (96, 90, 80)          # footer grey
BOX_BG = (252, 248, 238)     # slightly lighter panel

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, face, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=face) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, face, fill, leading):
    """Draw lines top-to-bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def story_card(draw, box, kicker, headline, body, head_size=30,
               body_size=19, head_leading=36, body_leading=26):
    """Draw one story inside box=(x, y, w, h); return bottom y used."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=BOX_BG,
                   outline=RULE, width=2)
    pad = 16
    cx = x + pad
    inner = w - 2 * pad
    cy = y + pad

    kicker_face = font(SANS_BOLD, 15)
    draw.text((cx, cy), kicker, font=kicker_face, fill=RED)
    cy += 24
    draw.line([(cx, cy), (cx + inner, cy)], fill=RED, width=2)
    cy += 10

    head_face = font(SERIF_BOLD, head_size)
    head_lines = wrap(draw, headline, head_face, inner)
    cy = text_block(draw, cx, cy, head_lines, head_face, INK, head_leading)

    cy += 6
    body_face = font(SERIF, body_size)
    body_lines = wrap(draw, body, body_face, inner)
    cy = text_block(draw, cx, cy, body_lines, body_face, INK, body_leading)
    return cy


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([8, 8, SIZE - 9, SIZE - 9], outline=RULE, width=3)
    draw.rectangle([14, 14, SIZE - 15, SIZE - 15], outline=RULE, width=1)

    # ---- Masthead ----
    y = MARGIN + 6
    mast = font(SERIF_BOLD, 62)
    title = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(title, font=mast)
    draw.text(((SIZE - tw) / 2, y), title, font=mast, fill=INK)
    y += 78

    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=2)
    y += 12
    date_face = font(SANS_BOLD, 26)
    dateline = "SUNDAY  ·  22 NOVEMBER 2026"
    dw = draw.textlength(dateline, font=date_face)
    draw.text(((SIZE - dw) / 2, y), dateline, font=date_face, fill=RED)
    y += 40
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=4)
    y += 14

    content_w = SIZE - 2 * MARGIN

    # ---- Lead story: the Gulf, full width ----
    lead_h = 218
    story_card(
        draw, (MARGIN, y, content_w, lead_h),
        "CONFLICT — THE GULF",
        "Iran claims strikes on US Patriot radars in Bahrain",
        "Iran's Revolutionary Guard says a combined missile and drone "
        "operation hit two US Patriot air defence radars at the al-Riffa "
        "and Awali bases. Kuwait and Bahrain say the attacks were "
        "intercepted, with no damage reported.",
        head_size=34, body_size=20, head_leading=40, body_leading=27,
    )
    y += lead_h + GUTTER

    # ---- Second row: Lviv + Junín, half width each ----
    half_w = (content_w - GUTTER) // 2
    row2_h = 250
    story_card(
        draw, (MARGIN, y, half_w, row2_h),
        "WAR — LVIV, UKRAINE",
        "Russian strike on Lviv kills two",
        "At least two people were killed and ten injured as a Russian "
        "missile hit a building in Lviv. Zelenskyy called strikes on "
        "the Crimean Bridge a \u201cfair response\u201d.",
        head_size=29, body_size=19, head_leading=34, body_leading=25,
    )
    story_card(
        draw, (MARGIN + half_w + GUTTER, y, half_w, row2_h),
        "DISASTER — JUN\u00cdN, PERU",
        "6.7 quake shakes Peru's Andes",
        "The US Geological Survey put the quake at magnitude 6.7, "
        "34 km north of Jun\u00edn. Felt in Lima, it sent residents "
        "into the streets; no casualties or damage were reported.",
        head_size=29, body_size=19, head_leading=34, body_leading=25,
    )
    y += row2_h + GUTTER

    # ---- Third row: three columns ----
    third_w = (content_w - 2 * GUTTER) // 3
    row3_h = 262
    x3 = MARGIN
    story_card(
        draw, (x3, y, third_w, row3_h),
        "CRIME — SINALOA, MEXICO",
        "\u201cEl Chapo Isidro\u201d captured",
        "Mexican forces captured Fausto Isidro Meza Flores, one of the "
        "FBI's 10 most wanted, in Guasave. At least 11 people were "
        "killed in the gun battles that followed.",
        head_size=26, body_size=18, head_leading=31, body_leading=23,
    )
    x3 += third_w + GUTTER
    story_card(
        draw, (x3, y, third_w, row3_h),
        "TRADE — BRUSSELS & JAKARTA",
        "EU and Indonesia sign trade deal",
        "After a decade of talks, the EU and Indonesia signed a deal "
        "scrapping 98.5% of tariffs between the EU and Southeast "
        "Asia's largest economy.",
        head_size=26, body_size=18, head_leading=31, body_leading=23,
    )
    x3 += third_w + GUTTER
    story_card(
        draw, (x3, y, third_w, row3_h),
        "CLIMATE — ANTALYA, T\u00dcRKIYE",
        "COP31 deadlocked over fossil fuels",
        "Climate talks ran into overtime, deadlocked over fossil "
        "fuels and climate finance, as the latest draft drops any "
        "mention of moving away from coal, oil and gas.",
        head_size=26, body_size=18, head_leading=31, body_leading=23,
    )
    y += row3_h + GUTTER

    # ---- Footer ----
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=1)
    y += 8
    foot = font(SANS, 15)
    line = ("Sources: ANI · Al Jazeera · BBC · AP / USGS · Reuters · CNN · "
            "Global Digest — all dated 21–22 November 2026")
    fw = draw.textlength(line, font=foot)
    draw.text(((SIZE - fw) / 2, y + 2), line, font=foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    build()
