#!/usr/bin/env python3
"""Draw a 1024x1024 front-page collage summing up world news of
Thursday 19 November 2026. Output: entry.png in this directory."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, color, lh=None):
    lh = lh or int(f.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += lh
    return y


def tag_chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = font(SANS_B, 15)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 16, y + 24], radius=4, fill=bg)
    d.text((x + 8, y + 4), label, font=f, fill=fg)
    return tw + 16


def panel(d, x, y, w, h, tag, tag_bg, headline, summary, accent,
          hf_size=21, sf_size=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(255, 255, 255),
                        outline=(200, 200, 200), width=1)
    d.rectangle([x, y, x + 6, y + h], fill=accent)
    tag_chip(d, x + 16, y + 12, tag, tag_bg)
    hf = font(SANS_B, hf_size)
    hlh = int(hf_size * 1.22)
    lines = wrap(d, headline, hf, w - 32)
    yy = text_block(d, x + 16, y + 46, lines[:3], hf, (15, 15, 15), hlh)
    sf = font(SANS, sf_size)
    slh = int(sf_size * 1.28)
    # Cap summary lines to what fits inside the panel with a bottom margin.
    room = (y + h - 8) - (yy + 4)
    max_slines = max(1, room // slh)
    slines = wrap(d, summary, sf, w - 32)
    text_block(d, x + 16, yy + 4, slines[:max_slines], sf, (60, 60, 60), slh)


def main():
    img = Image.new("RGB", (W, H), (240, 238, 232))
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 104], fill=(12, 24, 54))
    d.rectangle([0, 104, W, 108], fill=(198, 32, 32))
    d.text((24, 14), "THE WORLD TODAY", font=font(SERIF_B, 52),
           fill=(255, 255, 255))
    d.text((24, 72), "Thursday 19 November 2026  •  World news in one image",
           font=font(SANS_B, 19), fill=(255, 214, 90))
    d.text((700, 30), "FRONT PAGE", font=font(SANS_B, 26), fill=(255, 255, 255))
    d.text((700, 66), "15 stories • 1 day", font=font(SANS, 17),
           fill=(200, 210, 230))

    # ---- Lead panel: GTA VI (left, with drawn Vice City sunset scene) ----
    LX, LY, LW, LH = 16, 120, 612, 280
    d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=8,
                        fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    # Sunset sky (scene height 132)
    for i in range(132):
        r = int(255 - i * 0.55)
        g = int(120 + i * 0.55)
        b = int(90 + i * 0.9)
        d.line([(LX + 1, LY + 1 + i), (LX + LW - 1, LY + 1 + i)], fill=(r, g, b))
    # Sun (top right, clear of buildings)
    d.ellipse([LX + 520, LY + 14, LX + 584, LY + 78], fill=(255, 236, 150))
    # Skyline silhouettes (short, tops stay below the title text)
    for bx, bw, bh in [(20, 70, 40), (100, 55, 55), (165, 80, 42), (255, 60, 58),
                       (325, 75, 38), (410, 60, 50), (480, 70, 34)]:
        d.rectangle([LX + bx, LY + 132 - bh, LX + bx + bw, LY + 132],
                    fill=(40, 20, 60))
    # Sea strip
    d.rectangle([LX + 1, LY + 132, LX + LW - 1, LY + 146], fill=(20, 90, 130))
    # Neon sign
    d.text((LX + 24, LY + 28), "VICE CITY", font=font(SANS_B, 44),
           fill=(255, 255, 255))
    d.text((LX + 26, LY + 82), "GTA VI IS HERE", font=font(SANS_B, 22),
           fill=(255, 236, 150))
    tag_chip(d, LX + 16, LY + 158, "LEAD  •  GAMING", (198, 32, 32))
    hf = font(SANS_B, 25)
    yy = text_block(d, LX + 16, LY + 190, wrap(
        d, "Grand Theft Auto VI begins global rollout — gamers enter Vice City",
        hf, LW - 32)[:2], hf, (15, 15, 15), 30)
    sf = font(SANS, 16)
    text_block(d, LX + 16, yy + 4, wrap(
        d, "Launch day: the most anticipated game ever arrives worldwide.",
        sf, LW - 32)[:1], sf, (60, 60, 60), 20)

    # ---- Right column: 2 panels ----
    RX, RW = 644, 364
    panel(d, RX, 120, RW, 136, "DIPLOMACY", (12, 90, 160),
          "Trump, Xi and Putin hold trilateral talks in Shenzhen",
          "Three leaders meet at the APEC summit.",
          (12, 90, 160), hf_size=19, sf_size=15)
    panel(d, RX, 264, RW, 136, "MARKETS", (0, 130, 80),
          "Anthropic's historic Nasdaq debut: $83 a share, $81.3B raised",
          "The biggest IPO ever.",
          (0, 130, 80), hf_size=19, sf_size=15)

    # ---- Grid: 6 panels, 3 cols x 2 rows ----
    cols = [(16, 324), (352, 324), (688, 320)]
    rows = [412, 620]
    stories = [
        ("CONFLICT", (160, 30, 30),
         "US and Iran exchange fire again",
         "US hit a missile site on Qeshm Island; Iran struck a US base in Kuwait and a radar site in Bahrain."),
        ("CONFLICT", (160, 30, 30),
         "Israeli troops launch rare ground operation in central Gaza",
         "Forces move into an area left under last year's ceasefire deal."),
        ("WAR IN EUROPE", (90, 60, 140),
         "Crimea bridge attacked again — traffic suspended",
         "A new Ukrainian strike halts traffic for a second day running."),
        ("EUROPE", (20, 90, 140),
         "EU proposes a €45 billion loan for Ukraine",
         "Kyiv would repay it only after Russia pays reparations."),
        ("TECH", (120, 60, 160),
         "Nvidia's new chief promises earlier raises, more stock",
         "Acting CEO Colette Kress speaks at her first all-hands; H-series chip shipments to China stop."),
        ("SPACE", (40, 40, 90),
         "Voyager 1 reaches a one-light-day milestone",
         "NASA confirms the landmark at a news conference today."),
    ]
    for i, (tag, bg, head, summ) in enumerate(stories):
        x, w = cols[i % 3]
        y = rows[i // 3]
        panel(d, x, y, w, 196, tag, bg, head, summ, bg)

    # ---- Ticker strip ----
    TY = 828
    d.rectangle([0, TY, W, TY + 72], fill=(12, 24, 54))
    d.text((16, TY + 6), "ALSO TODAY", font=font(SANS_B, 17), fill=(255, 214, 90))
    tf = font(SANS, 15)
    tick = ("Cyclone Akvan strengthens off India  •  Fed minutes: most officials expect "
            "more rate hikes if inflation stays high  •  Australia sanctions Israeli "
            "settlers over West Bank expansion")
    text_block(d, 16, TY + 30, wrap(d, tick, tf, W - 32)[:2], tf,
               (255, 255, 255), 19)

    # ---- Footer ----
    d.rectangle([0, 912, W, 916], fill=(180, 180, 180))
    ff = font(SANS, 15)
    text_block(d, 16, 928, wrap(d,
        "Also: ICJ ruling due on Myanmar Rohingya genocide case  •  Democrat Peltola "
        "wins Alaska Senate seat  •  Canada–China ties under Carney.  All stories from "
        "Thursday 19 November 2026.", ff, W - 32)[:2], ff, (80, 80, 80), 19)
    d.text((16, 988), "THE WORLD TODAY — 19 NOV 2026", font=font(SANS_B, 14),
           fill=(120, 120, 120))

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
