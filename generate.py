#!/usr/bin/env python3
"""
The World Today -- Friday, 20 November 2026.

Build-time generator for the newspaper front page image (entry.png).

This file is the source that drew the front page: it is run once at build
time with Pillow to produce entry.png, which is committed beside it in
this repository. It is NOT the grader entrypoint -- main.py is a
stdlib-only copier that copies the committed entry.png to the output
location. This generator is kept in the repository as the image's source
so the picture can be reproduced and audited.

When run locally it draws a one-page newspaper front page that sums up
the world news of Friday 20 November 2026 and writes it to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when that variable
is set).

Everything is drawn in code with Pillow: no external images, no network,
no randomness, no clock -- two runs always produce byte-identical output.

The day's stories (reported 20 November 2026):
  * The International Court of Justice ruled 9-6 that Myanmar committed
    genocide against the Rohingya -- the first time the court has held a
    state responsible for genocide. Case brought by The Gambia over the
    2017 Rakhine operation; more than 1.3 million Rohingya displaced.
  * Hours after the Shenzhen summit, Russia fired at least 110 missiles
    and some 400 drones at Ukraine overnight: nine killed, 28 injured,
    three Kyiv bridges damaged, objects fell inside Poland and NATO jets
    scrambled.
  * Trump, Xi and Putin held their first three-way meeting in Shenzhen,
    on the sidelines of APEC, and signed a four-point declaration after
    roughly 70 minutes of talks; the text did not mention Ukraine or Iran.
  * Anthropic closed near $97, 17% above its $83 offer price, in a record
    $81.3bn Nasdaq IPO -- while the S&P 500 fell about 2% for a fifth
    straight day and Japan's Nikkei dropped 4.8%.
  * Briefs: a Houthi missile damaged the Public Investment Fund tower in
    Riyadh; the COP31 draft in Antalya dropped any fossil-fuel phase-out;
    Kenya discharged its last Ebola patient, 37 days after its first case.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 18, 14)
FAINT = (90, 84, 72)
RULE = (20, 18, 14)
ACCENT = (138, 31, 31)       # deep newspaper red
NAVY = (24, 36, 62)          # lead visual panel
GOLD = (212, 168, 74)
SKY = (16, 22, 40)           # Kyiv night strip
FIRE = (232, 122, 44)

MARGIN = 36
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

FONT_CANDIDATES = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
    "serif_italic": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
}


def font(kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def hline(draw, y, x0=MARGIN, x1=RIGHT, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- visuals
def draw_court_panel(draw, x0, y0, x1, y1):
    """Lead visual: a courthouse facade plus the 9-6 vote, on navy."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # courthouse, left portion
    bx0, bx1 = x0 + 34, x0 + 470
    roof_y = y0 + 26
    # pediment
    draw.polygon([(bx0, roof_y + 34), (bx1, roof_y + 34),
                  ((bx0 + bx1) // 2, roof_y)], fill=GOLD)
    draw.rectangle([bx0, roof_y + 40, bx1, roof_y + 52], fill=(238, 230, 210))
    # columns
    col_top, col_bot = roof_y + 60, y1 - 40
    col_w = 26
    span = bx1 - bx0
    for i in range(5):
        cx = bx0 + 22 + i * (span - 44 - col_w) // 4
        draw.rectangle([cx, col_top, cx + col_w, col_bot], fill=(238, 230, 210))
        draw.rectangle([cx - 4, col_top - 6, cx + col_w + 4, col_top], fill=GOLD)
        draw.rectangle([cx - 4, col_bot, cx + col_w + 4, col_bot + 6], fill=GOLD)
    # steps
    draw.rectangle([bx0 - 8, col_bot + 12, bx1 + 8, col_bot + 20], fill=(160, 150, 128))
    draw.rectangle([bx0 - 16, col_bot + 24, bx1 + 16, y1 - 8], fill=(120, 112, 94))
    # vote block, right portion
    vx = x0 + 520
    draw.line([(vx - 26, y0 + 22), (vx - 26, y1 - 22)], fill=GOLD, width=3)
    f_big = font("serif_bold", 78)
    draw.text((vx, y0 + 12), "9-6", font=f_big, fill=(255, 246, 220))
    f_cap = font("sans_bold", 20)
    draw.text((vx + 2, y0 + 100), "THE JUDGES' VOTE", font=f_cap, fill=GOLD)
    f_small = font("sans", 16)
    for i, line in enumerate(["First state ever held responsible", "for genocide by the World Court."]):
        draw.text((vx + 2, y0 + 130 + i * 22), line, font=f_small, fill=(226, 222, 208))


def draw_kyiv_strip(draw, x0, y0, x1, y1):
    """Night skyline with missile streaks."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # moon
    draw.ellipse([x1 - 52, y0 + 8, x1 - 28, y0 + 32], fill=(238, 232, 200))
    # streaks
    for sx, sy, ex, ey in [(x0 + 30, y0 + 6, x0 + 96, y0 + 34),
                           (x0 + 120, y0 + 2, x0 + 178, y0 + 28),
                           (x0 + 210, y0 + 10, x0 + 262, y0 + 36)]:
        draw.line([(sx, sy), (ex, ey)], fill=FIRE, width=3)
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 190, 90))
    # skyline silhouette
    base = y1
    buildings = [(0, 26), (34, 40), (70, 30), (104, 46), (142, 34),
                 (178, 42), (214, 28), (248, 38), (282, 30)]
    for off, bh in buildings:
        draw.rectangle([x0 + off, base - bh, x0 + off + 30, base], fill=(4, 6, 12))
    # bridge arc
    draw.arc([x0 + 150, base - 34, x0 + 300, base + 22], start=180, end=360,
             fill=(120, 140, 180), width=3)


def draw_flags_strip(draw, x0, y0, x1, y1):
    """Three simplified flags: United States, China, Russia."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    gap = 10
    fw = (x1 - x0 - 2 * gap) // 3
    fh = y1 - y0
    # United States: stripes + blue canton
    fx = x0
    stripe_h = fh // 7
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (244, 242, 238)
        draw.rectangle([fx, y0 + i * stripe_h, fx + fw, y0 + (i + 1) * stripe_h], fill=col)
    draw.rectangle([fx, y0, fx + fw * 2 // 5, y0 + stripe_h * 4], fill=(30, 40, 110))
    for r in range(3):
        for c in range(4):
            cx = fx + 7 + c * 11
            cy = y0 + 6 + r * 11
            draw.ellipse([cx, cy, cx + 4, cy + 4], fill=(255, 255, 255))
    # China: red field, gold stars
    fx = x0 + fw + gap
    draw.rectangle([fx, y0, fx + fw, y0 + fh], fill=(222, 41, 16))
    draw.polygon([(fx + 16, y0 + 8), (fx + 20, y0 + 20), (fx + 32, y0 + 20),
                  (fx + 22, y0 + 27), (fx + 26, y0 + 39), (fx + 16, y0 + 31),
                  (fx + 6, y0 + 39), (fx + 10, y0 + 27), (fx + 0 + 0, y0 + 20),
                  (fx + 12, y0 + 20)], fill=(255, 222, 0))
    for dx, dy in [(34, 8), (40, 18), (40, 30), (32, 38)]:
        draw.ellipse([fx + dx, y0 + dy, fx + dx + 6, y0 + dy + 6], fill=(255, 222, 0))
    # Russia: white / blue / red
    fx = x0 + 2 * (fw + gap)
    third = fh // 3
    draw.rectangle([fx, y0, fx + fw, y0 + third], fill=(244, 242, 238))
    draw.rectangle([fx, y0 + third, fx + fw, y0 + 2 * third], fill=(0, 57, 166))
    draw.rectangle([fx, y0 + 2 * third, fx + fw, y0 + fh], fill=(213, 43, 30))
    for fx in (x0, x0 + fw + gap, x0 + 2 * (fw + gap)):
        draw.rectangle([fx, y0, fx + fw, y1], outline=(120, 116, 104), width=1)


def draw_chart_strip(draw, x0, y0, x1, y1):
    """Falling market bars with one green debut bar."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    base = y1 - 10
    draw.line([(x0 + 8, base), (x1 - 8, base)], fill=INK, width=2)
    bars = [(22, (46, 125, 50)), (15, ACCENT), (18, ACCENT), (12, ACCENT),
            (15, ACCENT), (9, ACCENT), (7, ACCENT)]
    bw = 26
    step = (x1 - x0 - 30) // len(bars)
    for i, (bh, col) in enumerate(bars):
        bx = x0 + 16 + i * step
        draw.rectangle([bx, base - bh, bx + bw, base], fill=col)
    f_tag = font("sans_bold", 19)
    draw.text((x0 + 14, y0 + 4), "ANT +17%", font=f_tag, fill=(46, 125, 50))
    f_tag2 = font("sans_bold", 19)
    label = "S&P -2%"
    draw.text((x1 - 14 - draw.textlength(label, font=f_tag2), y0 + 4),
              label, font=f_tag2, fill=ACCENT)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # ---- masthead
    hline(d, 28, width=3)
    f_title = font("serif_bold", 76)
    centered(d, cx, 38, "The World Today", f_title)
    hline(d, 128, width=1)
    hline(d, 133, width=3)
    f_info = font("sans_bold", 19)
    d.text((MARGIN, 144), "GLOBAL EDITION", font=f_info, fill=INK)
    centered(d, cx, 144, "Friday, 20 November 2026", font("sans_bold", 21))
    tail = "LATE FINAL"
    d.text((RIGHT - d.textlength(tail, font=f_info), 144), tail, font=f_info, fill=INK)
    hline(d, 174, width=2)

    # ---- lead story
    f_kick = font("sans_bold", 20)
    d.text((MARGIN, 186), "THE HAGUE  •  INTERNATIONAL COURT OF JUSTICE  •  LANDMARK RULING",
           font=f_kick, fill=ACCENT)
    f_head = font("serif_bold", 56)
    head_lines = ["WORLD COURT: MYANMAR", "COMMITTED GENOCIDE", "AGAINST THE ROHINGYA"]
    y = 214
    for line in head_lines:
        centered(d, cx, y, line, f_head)
        y += 64
    f_sub = font("serif_italic", 22)
    sub = ("In a 9-6 vote, the Court holds a state responsible for genocide for the "
           "first time -- over the 2017 Rakhine crackdown that killed thousands and "
           "drove more than 1.3 million Rohingya into Bangladesh. The Gambia brought the case.")
    yy = y + 6
    for line in wrap(d, sub, f_sub, CONTENT_W):
        centered(d, cx, yy, line, f_sub, fill=(40, 36, 28))
        yy += 28
    # lead visual
    vy0 = 512
    draw_court_panel(d, MARGIN, vy0, RIGHT, vy0 + 172)
    f_cap = font("serif_italic", 16)
    cap = "The Hague: the 2017 Rakhine operation sent hundreds of thousands fleeing; 1.3 million Rohingya remain displaced."
    d.text((MARGIN, vy0 + 180), cap, font=f_cap, fill=FAINT)
    yy = vy0 + 204

    # ---- secondary row
    hline(d, yy, width=3)
    top = yy + 14
    col_w = (CONTENT_W - 32) // 3
    cols_x = [MARGIN, MARGIN + col_w + 16, MARGIN + 2 * (col_w + 16)]
    # vertical rules between columns
    for vx in (cols_x[1] - 8, cols_x[2] - 8):
        d.line([(vx, top), (vx, 966)], fill=(170, 162, 146), width=1)

    stories = [
        {
            "visual": draw_kyiv_strip,
            "kicker": "UKRAINE WAR - OVERNIGHT",
            "headline": "RUSSIA FIRES 110 MISSILES AT KYIV",
            "body": ("Nine killed, 28 injured in a ten-hour barrage with some 400 drones, "
                     "hours after the Shenzhen summit. Three Kyiv bridges damaged; NATO "
                     "jets scrambled over Poland."),
        },
        {
            "visual": draw_flags_strip,
            "kicker": "SHENZHEN - APEC SUMMIT",
            "headline": "TRUMP, XI, PUTIN MEET IN SHENZHEN",
            "body": ("The three leaders signed a four-point declaration on nuclear risk, "
                     "UN reform and energy after 70 minutes -- with no mention of "
                     "Ukraine or Iran."),
        },
        {
            "visual": draw_chart_strip,
            "kicker": "NEW YORK - MARKETS",
            "headline": "ANTHROPIC +17% IN RECORD IPO DEBUT",
            "body": ("Anthropic closed near $97, up from $83, raising a record "
                     "$81.3bn. S&P -2%; Nikkei -4.8%."),
        },
    ]
    f_ckick = font("sans_bold", 16)
    f_chead = font("serif_bold", 25)
    f_cbody = font("serif", 16)
    for x, story in zip(cols_x, stories):
        story["visual"](d, x, top, x + col_w, top + 52)
        cy = top + 60
        d.text((x, cy), story["kicker"], font=f_ckick, fill=ACCENT)
        cy += 24
        for line in wrap(d, story["headline"], f_chead, col_w):
            d.text((x, cy), line, font=f_chead, fill=INK)
            cy += 30
        cy += 4
        for line in wrap(d, story["body"], f_cbody, col_w):
            d.text((x, cy), line, font=f_cbody, fill=(40, 36, 28))
            cy += 20

    # ---- briefs strip
    hline(d, 974, width=2)
    f_brief = font("sans_bold", 15)
    briefs = "ALSO TODAY:  Houthi missile hits Riyadh tower  •  COP31 drops fossil phase-out  •  Kenya ends Ebola outbreak"
    centered(d, cx, 982, briefs, f_brief, fill=INK)
    f_foot = font("sans", 13)
    centered(d, cx, 1004, "All stories reported on Friday, 20 November 2026  •  Drawn in code -- no photographs",
             f_foot, fill=FAINT)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    build().save(path, format="PNG")
    print("wrote", path)


if __name__ == "__main__":
    main()
