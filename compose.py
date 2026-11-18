#!/usr/bin/env python3
"""Compose the news-image-20261117 front page (2400x1600 PNG) from four
AI-generated scene images. Original layout; all text drawn with PIL."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1600
BG = (247, 243, 234)      # off-white paper
NAVY = (16, 28, 54)
NAVY2 = (24, 40, 74)
GOLD = (212, 160, 60)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
LINE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def cover(img, tw, th):
    """Center-crop image to fill tw x th."""
    w, h = img.size
    s = max(tw / w, th / h)
    img = img.resize((round(w * s), round(h * s)), Image.LANCZOS)
    x = (img.width - tw) // 2
    y = (img.height - th) // 2
    return img.crop((x, y, x + tw, y + th))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 200], fill=NAVY)
    f_mast = font(SERIF_B, 92)
    t = "THE WORLD IN ONE PICTURE"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 28), t, font=f_mast, fill=WHITE)
    f_date = font(SANS_B, 56)
    t = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 128), t, font=f_date, fill=GOLD)
    d.rectangle([0, 200, W, 208], fill=GOLD)

    # ---- Lead story (left) ----
    LX, LW = 40, 1340
    lead = Image.open("assets/media-generation-news17-qeshm-strike-0-6a2c7b6d-6203-44d5-ab75-1751ef28e930.webp").convert("RGB")
    img.paste(cover(lead, LW, 420), (LX, 224))
    d.rectangle([LX, 224, LX + LW, 644], outline=LINE, width=2)
    f_kick = font(SANS_B, 30)
    d.text((LX, 664), "WAR IN THE GULF  —  LEAD STORY", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 58)
    lines = wrap(d, "U.S. STRIKES QESHM ISLAND AS IRAN HITS U.S. RADAR IN BAHRAIN", f_head, LW)
    draw_wrapped(d, LX, 706, lines, f_head, INK, 68)
    f_stand = font(SANS, 32)
    lines = wrap(d, "U.S. jets hit an Iranian missile site on Qeshm Island; Iran fired drones at a U.S. radar base in Bahrain, its third attack there in five days.", f_stand, LW)
    draw_wrapped(d, LX, 856, lines, f_stand, INK, 44)

    # ---- Sidebar: The Day in Numbers (right) ----
    SX, SW = 1400, 960
    d.rectangle([SX, 224, SX + SW, 990], fill=NAVY)
    f_side = font(SERIF_B, 48)
    d.text((SX + 36, 252), "THE DAY IN NUMBERS", font=f_side, fill=GOLD)
    d.line([SX + 36, 326, SX + SW - 36, 326], fill=GOLD, width=3)
    rows = [
        ("115", "$B Nvidia quarterly revenue, about double a year earlier"),
        ("1441", "drones Russia says it shot down overnight"),
        ("3", "drone attacks on Bahrain in five days"),
        ("2", "second day of strikes on the Kerch Bridge"),
    ]
    f_num = font(SERIF_B, 84)
    f_desc = font(SANS, 32)
    y = 356
    for num, desc in rows:
        d.text((SX + 36, y), num, font=f_num, fill=WHITE)
        lines = wrap(d, desc, f_desc, SW - 320)
        draw_wrapped(d, SX + 300, y + 14, lines, f_desc, WHITE, 42)
        y += 148
    f_foot = font(SANS, 26)
    d.text((SX + 36, 936), "All figures as reported on the day.", font=f_foot, fill=(170, 180, 200))

    # ---- Three secondary panels ----
    panels = [
        ("assets/media-generation-news17-kerch-day-0-599175f3-58d2-4e18-b248-de80106edea0.webp",
         "KERCH BRIDGE HIT AGAIN — SECTION FALLS INTO THE STRAIT",
         "Ukraine struck the Crimea link a second day; Russia hit bridges in Kyiv."),
        ("assets/media-generation-news17-shenzhen-summit-0-57816495-6bee-4735-9667-dfee89929cc7.webp",
         "TRUMP HEADS TO SHENZHEN FOR XI–PUTIN TALKS",
         "China confirms a trilateral summit with Xi, Putin and Trump on Thursday."),
        ("assets/media-generation-news17-nvidia-chip-0-7d266098-bc5d-453d-86d8-a8201be8276d.webp",
         "NVIDIA POSTS $115B QUARTER, WON’T BRING BACK HUANG",
         "Record revenue; ousted chief Jensen Huang stays out."),
    ]
    f_ph = font(SERIF_B, 34)
    f_pc = font(SANS, 26)
    PW, GAP = 760, 20
    for i, (path, head, cap) in enumerate(panels):
        x = 40 + i * (PW + GAP)
        p = Image.open(path).convert("RGB")
        img.paste(cover(p, PW, 190), (x, 1014))
        d.rectangle([x, 1014, x + PW, 1204], outline=LINE, width=2)
        lines = wrap(d, head, f_ph, PW - 16)
        y = draw_wrapped(d, x + 8, 1222, lines, f_ph, INK, 42)
        lines = wrap(d, cap, f_pc, PW - 16)
        draw_wrapped(d, x + 8, y + 6, lines, f_pc, GREY, 34)

    # ---- Bottom ticker ----
    d.rectangle([0, 1452, W, 1560], fill=NAVY)
    t = "ALSO TODAY:  Japan scrambles jets over Russian planes  ·  UK sanctions settlement builders  ·  West urges Israel to open Gaza crossings  ·  Ebola passes 11,000 cases in Congo"
    size = 30
    while size > 18:
        f_tick = font(SANS_B, size)
        if d.textlength(t, font=f_tick) <= 2300:
            break
        size -= 1
    tw = d.textlength(t, font=f_tick)
    d.text(((W - tw) / 2, 1486), t, font=f_tick, fill=WHITE)

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
