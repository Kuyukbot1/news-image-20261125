#!/usr/bin/env python3
"""Draw the Wednesday 25 November 2026 world-news front page, 1024x1024.

Fresh build for make.fun news-image-20261125. All 50 stories come from
RESEARCH_25NOV.md (verified Wed 25 Nov 2026, ~01:20-01:45 UTC). Deterministic:
no random, no network, no clock. Pillow only.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

CREAM = (246, 238, 218)
PAPER = (251, 245, 230)
NAVY = (18, 34, 68)
NAVY2 = (30, 54, 98)
INK = (24, 24, 24)
GREY = (96, 92, 82)
RED = (178, 38, 38)
RED_D = (140, 28, 28)
GOLD = (203, 164, 40)
GOLD_L = (233, 206, 112)
LINE = (178, 166, 136)
SEA = (212, 228, 238)
LAND = (233, 219, 190)
WHITE = (255, 255, 255)
GREEN = (44, 122, 48)
BLUE = (40, 90, 172)
AMBER = (190, 120, 0)
PURPLE = (104, 60, 158)
TEAL = (0, 128, 140)
SKY = (168, 205, 228)
SKY_D = (120, 170, 205)

REGION_COLOR = {
    "Americas": RED, "Europe": BLUE, "Mideast": AMBER, "Africa": GREEN,
    "Asia": PURPLE, "Oceania": TEAL, "Global": (88, 88, 88),
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # no italic face shipped; use regular serif
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def centre(d, cx, y, s, font, fill):
    d.text((cx, y), s, font=font, fill=fill, anchor="ma")


def rrect(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- data
# (num, region, topic, headline, deck, label, scene)
FEATURES = [
    (1, "Mideast", "WAR",
     "Houthis hit Riyadh's tallest tower; 11 wounded",
     "Drone strike on the 385 m PIF Tower, the second hit in five days; 11 hurt.",
     "CONFIRMED · REUTERS", "tower"),
    (2, "Americas", "COURTS",
     "Huawei convicted in US trial over Iran business",
     "Brooklyn jury: guilty on 10 of 12 counts, but acquits it of racketeering.",
     "CONFIRMED · BBC", "court"),
    (3, "Americas", "SECURITY",
     "Hackers breach CIA's unclassified systems",
     "An unclassified CIA tool is breached, a source says. No classified data.",
     "REPORTED · REUTERS", "hack"),
    (4, "Europe", "UKRAINE WAR",
     "Zelenskiy: Ukraine hit Russian ship in Gulf of Finland",
     "Kyiv claims Saturday's drone strike; Norway urges caution in such ops.",
     "CONFIRMED · REUTERS", "ship"),
    (5, "Europe", "UKRAINE WAR",
     "Russian strike on Zaporizhzhia kills 2, wounds 22",
     "An overnight attack hits an apartment block; Russia also targets sites in Sumy.",
     "CONFIRMED · WIRE", "flats"),
    (6, "Americas", "MARKETS",
     "Nvidia's bounce fades; shares slide 6%",
     "The relief rally around Huang's return fizzles. Shares are still down about 37%.",
     "REPORTED · REUTERS", "chart"),
    (7, "Americas", "POLITICS",
     "Trump awards Giuliani the Medal of Freedom",
     "The highest US civilian honour goes to the former New York mayor, 82.",
     "CONFIRMED · REUTERS", "medal"),
    (8, "Europe", "POLITICS",
     "Sweden to vote on Kristersson staying as PM",
     "The speaker nominates Kristersson for a 30 November vote, after 72 days.",
     "CONFIRMED · REUTERS", "parliament"),
    (9, "Mideast", "GAZA",
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel, head of Hamas' internal security, is killed in Gaza City.",
     "REPORTED · WIRE", "gaza"),
    (10, "Africa", "FOOTBALL",
     "Senegal reinstated as Africa Cup champions",
     "CAS upholds Senegal's appeal: the 1–0 extra-time win over Morocco stands.",
     "CONFIRMED · REUTERS", "trophy"),
    (11, "Oceania", "CRICKET",
     "England crush Australia to level T20 series",
     "Donald 85 off 32, Salt 58, in a 151-run stand; England chase 185.",
     "CONFIRMED · REUTERS", "cricket"),
    (12, "Europe", "CHESS",
     "Gukesh–Sindarov Game 2 today, scores level",
     "Game 2 starts 15:00 CET in Geneva, Gukesh as White; the match is 0.5–0.5.",
     "CONFIRMED · FIDE", "chess"),
    (13, "Americas", "TRADE",
     "Trump set to unveil new tariffs after probe",
     "A Section 301 probe of 16 trading partners may bring new import duties.",
     "REPORTED · REUTERS", "cargo"),
    (14, "Asia", "AUSTRALIA",
     "Australia apologises to LGBTQ veterans",
     "Canberra apologises to LGBTQ service members for decades of bias.",
     "CONFIRMED · REUTERS", "rainbow"),
    (15, "Global", "TECH",
     "Microsoft declares 'Code Red' after historic outage",
     "The top alert follows the 24-hour Microsoft 365 outage of 12–13 Nov.",
     "REPORTED · REUTERS", "server"),
]

TIMELINE = [
    ("00:30", "Zaporizhzhia strike: 2 killed, 22 hurt"),
    ("01:16", "Australia apologises to LGBTQ veterans"),
    ("11:54", "England crush Australia in 2nd T20I"),
    ("14:00", "Gukesh–Sindarov Game 2 begins in Geneva"),
    ("17:46", "CAS reinstates Senegal as Africa champions"),
    ("21:00", "Wall St: Dow +0.9%, Nasdaq −1.5%"),
    ("Evening", "Trump pardons turkeys; Giuliani honoured"),
]

CHIPS = [("AMERICAS", 12, RED), ("EUROPE", 11, BLUE),
         ("MIDDLE EAST", 8, AMBER), ("ASIA", 8, PURPLE),
         ("AFRICA", 6, GREEN), ("OCEANIA", 2, TEAL), ("GLOBAL", 3, (88, 88, 88))]

# (num, country, one line)
ALSO = [
    (16, "France", "Sarkozy case ordered to trial; hearing Apr 2027"),
    (17, "Germany", "Ifo business sentiment rises to 90.6 in November"),
    (18, "Germany", "Berlin Left expels lawmaker accused of antisemitism"),
    (19, "Germany", "53% now oppose military aid to Ukraine, survey finds"),
    (20, "UK", "Prisoner admits murdering Soham child killer Huntley in jail"),
    (21, "UK", "Compass Group may move its listing to the US"),
    (22, "Spain", "Government challenges Madrid law on unborn children"),
    (23, "Yemen", "Houthis 60 km from Aden but will not take it, army says"),
    (24, "Qatar", "PM: region cannot afford another US–Iran escalation"),
    (25, "Israel", "Eisenkot clinches first coalition pact, with Lieberman"),
    (26, "Iran", "Braced for winter gas shortages as war damage bites"),
    (27, "Türkiye", "Senior AK Party figure Yazici resigns amid fund probe"),
    (28, "Qatar", "Berlin visit: Qatar pledges $16.5bn in new investments"),
    (29, "US", "Consumer confidence jumps to 103.3, a near two-year high"),
    (30, "US", "Fort Hood shooter Hasan seeks stay of execution next week"),
    (31, "US", "Abrego Garcia to leave US voluntarily, fly to Europe"),
    (32, "US", "Radar outage delays flights into Chicago O'Hare"),
    (33, "US", "Farm chief Rollins fights order halting religious emails"),
    (34, "Colombia", "25 held hostage in Cartagena supermarket heist"),
    (35, "Mexico", "Inflation hits six-month high of 3.96%"),
    (36, "India", "BJP and Akali Dal ally for 2027 Punjab elections"),
    (37, "India", "Women's hockey team face China in Champions Trophy"),
    (38, "Japan", "PM: Japan to pay full 2027 ICC share early"),
    (39, "China", "Nvidia suppliers cheer Huang's return"),
    (40, "Myanmar", "UK sanctions five generals after ICJ genocide ruling"),
    (41, "Indonesia", "Seizes 405 t of missile chemical from China ship"),
    (42, "Nepal", "Cricket fans in Qatar dream of Everest heights"),
    (43, "Libya", "Sinking of Russian vessel shows frozen conflict risk"),
    (44, "Libya", "Two naval men die of Benghazi port attack wounds"),
    (45, "Africa", "Ukraine targets Russian networks in Libya, Sudan, Mali"),
    (46, "Morocco", "Federation to appeal CAS Senegal ruling"),
    (47, "Senegal", "About 2,000 migrants reach Canary Islands in 2 days"),
    (48, "Australia", "Gold eases to $3,544/oz ahead of US inflation data"),
    (49, "Global", "WHO chief: lift US fuel blockade on Cuba"),
    (50, "Global", "UN opens 16 Days of Action vs violence against women"),
]

DATECHECK = [
    ("Nvidia reinstates Huang; shares soar 31%", "23 Nov"),
    ("Denmark backs 'ghetto law' evictions", "23 Nov"),
    ("FIFA names 2031/2035 Women's Cup hosts", "23 Nov"),
    ("Liverpool thrash 10-man Man Utd 4–0", "23 Nov"),
    ("COP31 collapses with no deal", "22 Nov"),
    ("England beat Spain 3–2 in Madrid", "15 Nov"),
    ("GTA VI released worldwide", "19 Nov"),
    ("Democrats clinch 258 House seats", "23 Nov"),
    ("India declare 720/9 in New Zealand", "23 Nov"),
    ("Korea minister quits over AI exam row", "23 Nov"),
]

FOOTER = ("Every story was reported on 25 November 2026; disputed claims are "
          "attributed. Sources: AP, Reuters, AFP, BBC, Al Jazeera, UN News. "
          "Original drawings.")


def masthead(d):
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 121], fill=GOLD)
    text(d, (14, 9), "THE DAY IN WORLD NEWS", F(SANS_B, 13), GOLD_L)
    tr = "50 STORIES · 7 REGIONS · EVERY ONE FROM THIS DAY"
    tw = d.textlength(tr, font=F(SANS_B, 13))
    text(d, (W - 14 - tw, 9), tr, F(SANS_B, 13), WHITE)
    centre(d, W // 2, 30, "Wednesday 25 November 2026", F(SERIF_B, 52), WHITE)
    centre(d, W // 2, 96,
           "Houthis hit Riyadh's tower · Huawei convicted · Senegal champions again",
           F(SERIF_I, 14), (255, 214, 130))


def chips_row(d):
    y, x = 126, 12
    for name, n, col in CHIPS:
        s = "%s %d" % (name, n)
        f = F(SANS_B, 11)
        w = d.textlength(s, font=f) + 16
        rrect(d, [x, y, x + w, y + 17], 8, fill=col)
        centre(d, x + w // 2, y + 2, s, f, WHITE)
        x += w + 6


def timeline(d):
    y0 = 150
    d.rectangle([12, y0, W - 12, y0 + 34], fill=NAVY2)
    d.rectangle([12, y0, 62, y0 + 34], fill=RED)
    centre(d, 37, y0 + 10, "UTC", F(SANS_B, 13), WHITE)
    for i in range(25):
        x = 70 + i * (W - 12 - 70 - 8) / 24.0
        d.line([x, y0 + 30, x, y0 + 33], fill=GOLD_L, width=1)
    slots = [(70, 0), (206, 1), (342, 2), (478, 3), (614, 4), (750, 5), (886, 6)]
    f_t, f_e = F(SANS_B, 11), F(SANS, 8)
    for x, i in slots:
        t, ev = TIMELINE[i]
        text(d, (x, y0 + 3), t, f_t, GOLD_L)
        for j, ln in enumerate(wrap(d, ev, f_e, 122)[:2]):
            text(d, (x, y0 + 16 + j * 9), ln, f_e, WHITE)


def scene_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
    d.rectangle([x, y + 44, x + w, y + h], fill=(52, 58, 64))
    for bx, bh in [(52, 44), (88, 56), (128, 40)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 22, y + h], fill=(70, 76, 90))
        for wy in range(6, bh - 4, 8):
            d.rectangle([x + bx + 4, y + h - bh + wy, x + bx + 18, y + h - bh + wy + 3],
                        fill=GOLD_L)
    # the PIF tower, tallest, with a drone strike flash
    d.rectangle([x + 88, y + 2, x + 112, y + h], fill=(150, 160, 178))
    d.rectangle([x + 92, y + 6, x + 108, y + 12], fill=(220, 90, 60))
    d.polygon([(x + 88, y + 2), (x + 100, y - 6), (x + 112, y + 2)], fill=(150, 160, 178))
    d.ellipse([x + 128, y + 6, x + 146, y + 24], fill=(255, 190, 60))
    d.ellipse([x + 132, y + 10, x + 142, y + 20], fill=(255, 230, 120))
    d.polygon([(x + 128, y + 15), (x + 116, y + 13), (x + 116, y + 17)], fill=(90, 90, 90))
    d.line([x + 128, y + 15, x + 112, y + 15], fill=(200, 200, 200), width=1)


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    d.rectangle([x, y + 40, x + w, y + h], fill=(120, 84, 52))
    d.rectangle([x + 20, y + 8, x + 176, y + 16], fill=(96, 66, 40))
    for cx in (30, 70, 110, 150):
        d.rectangle([x + cx, y + 16, x + cx + 10, y + 40], fill=(150, 110, 70))
    d.rectangle([x + 78, y + 22, x + 118, y + 40], fill=(30, 54, 98))
    d.rectangle([x + 84, y + 14, x + 112, y + 22], fill=(20, 38, 74))
    d.ellipse([x + 88, y + 26, x + 108, y + 38], fill=GOLD_L)
    # gavel and chip
    d.rectangle([x + 140, y + 26, x + 168, y + 33], fill=(90, 60, 30))
    d.rectangle([x + 152, y + 33, x + 156, y + 44], fill=(90, 60, 30))
    d.rectangle([x + 24, y + 24, x + 52, y + 38], fill=(20, 38, 74))
    d.rectangle([x + 28, y + 28, x + 48, y + 34], fill=(60, 160, 90))


def scene_hack(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 44))
    d.rectangle([x + 58, y + 10, x + 138, y + 42], fill=(30, 44, 70),
                outline=(80, 120, 170), width=2)
    for i, s in enumerate(["10110", "01101", "11001"]):
        text(d, (x + 64, y + 13 + i * 9), s, F(SANS_B, 9), (80, 200, 120))
    d.polygon([(x + 150, y + 18), (x + 158, y + 10), (x + 166, y + 18),
               (x + 166, y + 34), (x + 150, y + 34)], fill=(200, 60, 50))
    d.rectangle([x + 155, y + 20, x + 161, y + 28], fill=WHITE)
    d.rectangle([x + 44, y + 42, x + 152, y + 48], fill=(60, 70, 90))
    d.ellipse([x + 12, y + 12, x + 34, y + 34], fill=(255, 190, 60))
    d.text((x + 18, y + 16), "!", font=F(SANS_B, 16), fill=RED_D)


def scene_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + 34], fill=SKY)
    d.ellipse([x + 158, y + 4, x + 182, y + 28], fill=(255, 230, 140))
    d.rectangle([x, y + 34, x + w, y + h], fill=(46, 96, 140))
    for wy in (40, 47):
        d.arc([x - 10, y + wy - 4, x + 60, y + wy + 4], 0, 180, fill=WHITE, width=2)
        d.arc([x + 120, y + wy - 4, x + 200, y + wy + 4], 0, 180, fill=WHITE, width=2)
    d.polygon([(x + 52, y + 38), (x + 148, y + 38), (x + 138, y + 26),
               (x + 62, y + 26)], fill=(120, 40, 40))
    d.rectangle([x + 92, y + 12, x + 100, y + 26], fill=(90, 90, 90))
    d.rectangle([x + 96, y + 6, x + 104, y + 12], fill=RED)
    d.polygon([(x + 40, y + 10), (x + 52, y + 14), (x + 40, y + 18)], fill=(60, 60, 60))
    d.line([x + 40, y + 14, x + 28, y + 20], fill=(60, 60, 60), width=2)
    d.ellipse([x + 150, y + 30, x + 164, y + 44], fill=(255, 150, 60))
    d.ellipse([x + 154, y + 34, x + 160, y + 40], fill=(255, 220, 120))


def scene_flats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 70))
    d.rectangle([x + 14, y + 16, x + 66, y + h], fill=(150, 140, 120))
    d.rectangle([x + 78, y + 8, x + 130, y + h], fill=(170, 158, 136))
    d.rectangle([x + 142, y + 20, x + 182, y + h], fill=(140, 128, 108))
    for bx, bw in [(14, 52), (78, 52), (142, 40)]:
        for wy in range(12, h - 6, 10):
            d.rectangle([x + bx + 6, y + wy, x + bx + bw - 6, y + wy + 5],
                        fill=(255, 220, 120))
    d.polygon([(x + 78, y + 8), (x + 104, y - 4), (x + 130, y + 8)], fill=(90, 84, 76))
    d.ellipse([x + 92, y + 2, x + 116, y + 22], fill=(255, 140, 50))
    d.ellipse([x + 98, y + 7, x + 110, y + 17], fill=(255, 200, 90))
    d.rectangle([x + 150, y + 42, x + 190, y + 50], fill=RED)
    d.polygon([(x + 150, y + 42), (x + 158, y + 36), (x + 166, y + 42)], fill=RED)


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 22, 38))
    for gy in (12, 24, 36, 48):
        d.line([x + 8, y + gy, x + w - 8, y + gy], fill=(50, 64, 90), width=1)
    pts = [(12, 14), (40, 18), (68, 12), (96, 26), (124, 22), (152, 40), (184, 48)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d.line([x + ax, y + ay, x + bx, y + by], fill=(230, 70, 60), width=3)
    for ax, ay in pts:
        d.ellipse([x + ax - 3, y + ay - 3, x + ax + 3, y + ay + 3], fill=GOLD_L)
    d.rectangle([x + 128, y + 4, x + 188, y + 16], fill=(230, 70, 60))
    centre(d, x + 158, y + 6, "−6%", F(SANS_B, 10), WHITE)
    text(d, (x + 10, y + 42), "NVDA", F(SANS_B, 10), (140, 160, 200))


def scene_medal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 54, 98))
    for sx in range(8, w, 26):
        d.ellipse([x + sx, y + 6, x + sx + 3, y + 9], fill=WHITE)
    d.polygon([(x + 78, y + 6), (x + 118, y + 6), (x + 108, y + 28),
               (x + 88, y + 28)], fill=(178, 38, 38))
    d.polygon([(x + 88, y + 28), (x + 108, y + 28), (x + 98, y + 34)], fill=(140, 28, 28))
    d.ellipse([x + 74, y + 30, x + 122, y + 54], fill=GOLD)
    d.ellipse([x + 80, y + 34, x + 116, y + 50], outline=(150, 110, 20), width=2)
    centre(d, x + 98, y + 36, "★", F(SANS_B, 14), (150, 110, 20))
    d.rectangle([x + 150, y + 40, x + 190, y + 50], fill=(200, 200, 200))
    d.rectangle([x + 6, y + 40, x + 46, y + 50], fill=(200, 200, 200))


def scene_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 160, y + 4, x + 184, y + 28], fill=(255, 230, 140))
    d.rectangle([x, y + 44, x + w, y + h], fill=(110, 170, 110))
    d.rectangle([x + 48, y + 20, x + 148, y + 44], fill=(232, 222, 200))
    d.polygon([(x + 40, y + 20), (x + 98, y + 2), (x + 156, y + 20)], fill=(178, 60, 50))
    for cx in (56, 76, 96, 116, 136):
        d.rectangle([x + cx, y + 26, x + cx + 8, y + 44], fill=(120, 110, 96))
    d.rectangle([x + 92, y + 32, x + 104, y + 44], fill=(60, 50, 40))
    d.rectangle([x + 10, y + 34, x + 34, y + 44], fill=(200, 200, 210))
    d.rectangle([x + 162, y + 34, x + 186, y + 44], fill=(200, 200, 210))
    d.rectangle([x + 92, y + 44, x + 104, y + 48], fill=(90, 80, 70))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + 30], fill=(240, 190, 120))
    d.rectangle([x, y + 30, x + w, y + h], fill=(120, 100, 80))
    for bx, bh in [(10, 22), (44, 30), (120, 26), (156, 18)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 30, y + h], fill=(90, 78, 66))
        d.rectangle([x + bx + 6, y + h - bh + 5, x + bx + 12, y + h - bh + 11],
                    fill=(255, 220, 140))
    d.ellipse([x + 78, y + 2, x + 108, y + 28], fill=(255, 120, 40))
    d.ellipse([x + 86, y + 8, x + 100, y + 22], fill=(255, 190, 80))
    d.polygon([(x + 84, y + 28), (x + 92, y + 6), (x + 100, y + 28)], fill=(120, 100, 80))
    d.rectangle([x + 130, y + 34, x + 170, y + 44], fill=WHITE)
    d.rectangle([x + 134, y + 38, x + 166, y + 40], fill=RED)
    d.rectangle([x + 140, y + 30, x + 160, y + 34], fill=WHITE)


def scene_trophy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 90, 60))
    d.rectangle([x, y + 44, x + w, y + h], fill=(30, 110, 70))
    d.polygon([(x + 82, y + 8), (x + 114, y + 8), (x + 108, y + 30),
               (x + 88, y + 30)], fill=GOLD)
    d.arc([x + 70, y + 10, x + 86, y + 28], 90, 270, fill=GOLD, width=4)
    d.arc([x + 110, y + 10, x + 126, y + 28], 270, 90, fill=GOLD, width=4)
    d.rectangle([x + 92, y + 30, x + 104, y + 38], fill=GOLD)
    d.rectangle([x + 84, y + 38, x + 112, y + 43], fill=GOLD)
    d.ellipse([x + 22, y + 30, x + 46, y + 54], fill=WHITE)
    d.polygon([(x + 22, y + 40), (x + 34, y + 34), (x + 46, y + 40),
               (x + 40, y + 50), (x + 28, y + 50)], fill=INK)
    d.ellipse([x + 150, y + 30, x + 174, y + 54], fill=WHITE)
    d.polygon([(x + 150, y + 40), (x + 162, y + 34), (x + 174, y + 40),
               (x + 168, y + 50), (x + 156, y + 50)], fill=INK)
    for sx in range(6, w, 18):
        d.ellipse([x + sx, y + 4, x + sx + 3, y + 7], fill=GOLD_L)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 90))
    d.ellipse([x + 10, y + 40, x + 186, y + 62], fill=(90, 150, 70))
    d.rectangle([x + 88, y + 8, x + 108, y + 44], fill=(222, 190, 140))
    d.rectangle([x + 92, y + 4, x + 104, y + 10], fill=(200, 160, 110))
    d.ellipse([x + 140, y + 10, x + 156, y + 26], fill=RED)
    d.line([x + 108, y + 20, x + 140, y + 16], fill=WHITE, width=2)
    for sx in range(20, w, 40):
        d.ellipse([x + sx, y + 46, x + sx + 4, y + 50], fill=WHITE)
    d.rectangle([x + 150, y + 34, x + 190, y + 48], fill=NAVY)
    centre(d, x + 170, y + 36, "188/2", F(SANS_B, 11), WHITE)
    d.rectangle([x + 6, y + 34, x + 46, y + 48], fill=RED)
    centre(d, x + 26, y + 36, "184/8", F(SANS_B, 11), WHITE)


def scene_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    sq = 7
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + 20 + c * sq, y + r * sq,
                             x + 20 + (c + 1) * sq, y + (r + 1) * sq],
                            fill=(90, 60, 40))
    # white king and black queen standing on the board
    d.ellipse([x + 92, y + 8, x + 112, y + 26], fill=WHITE, outline=INK)
    d.rectangle([x + 96, y + 26, x + 108, y + 34], fill=WHITE, outline=INK)
    d.ellipse([x + 140, y + 10, x + 158, y + 26], fill=INK)
    d.rectangle([x + 144, y + 26, x + 154, y + 34], fill=INK)
    d.rectangle([x + 130, y + 44, x + 182, y + 54], fill=NAVY)
    centre(d, x + 156, y + 45, "0.5 – 0.5", F(SANS_B, 10), WHITE)
    text(d, (x + 84, y + 44), "GAME 2", F(SANS_B, 9), RED_D)


def scene_cargo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + 38, x + w, y + h], fill=(46, 96, 140))
    d.rectangle([x + 30, y + 22, x + 166, y + 38], fill=(120, 40, 40))
    d.rectangle([x + 40, y + 10, x + 84, y + 22], fill=(190, 120, 0))
    d.rectangle([x + 92, y + 10, x + 136, y + 22], fill=(40, 90, 172))
    d.rectangle([x + 144, y + 10, x + 166, y + 22], fill=(44, 122, 48))
    for cx in (44, 96, 148):
        d.line([x + cx, y + 14, x + cx + 36, y + 14], fill=WHITE, width=1)
    d.polygon([(x + 170, y + 26), (x + 186, y + 30), (x + 170, y + 34)], fill=RED)
    d.rectangle([x + 8, y + 6, x + 60, y + 18], fill=WHITE)
    centre(d, x + 34, y + 8, "301", F(SANS_B, 10), RED_D)


def scene_rainbow(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + 42, x + w, y + h], fill=(110, 170, 110))
    bands = [(220, 60, 60), (240, 140, 40), (240, 220, 60),
             (60, 170, 80), (60, 110, 200), (130, 70, 170)]
    for i, col in enumerate(bands):
        d.rectangle([x + 60 + i * 12, y + 6, x + 60 + (i + 1) * 12, y + 42], fill=col)
    d.rectangle([x + 56, y + 6, x + 60, y + 46], fill=(90, 80, 70))
    d.ellipse([x + 140, y + 14, x + 162, y + 36], fill=(255, 220, 170))
    d.rectangle([x + 146, y + 36, x + 156, y + 48], fill=(40, 70, 40))
    d.rectangle([x + 138, y + 20, x + 164, y + 24], fill=(40, 70, 40))
    d.ellipse([x + 20, y + 18, x + 40, y + 38], fill=(255, 220, 170))
    d.rectangle([x + 24, y + 38, x + 36, y + 50], fill=(30, 54, 98))


def scene_server(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 44))
    for bx in (52, 96, 140):
        d.rectangle([x + bx, y + 6, x + bx + 34, y + 48], fill=(40, 54, 80),
                    outline=(90, 120, 170), width=1)
        for ry in (12, 24, 36):
            d.ellipse([x + bx + 5, y + ry, x + bx + 9, y + ry + 4], fill=(80, 200, 120))
            d.rectangle([x + bx + 14, y + ry, x + bx + 28, y + ry + 4], fill=(70, 90, 120))
    d.rectangle([x + 8, y + 8, x + 44, y + 22], fill=RED)
    centre(d, x + 26, y + 10, "CODE", F(SANS_B, 9), WHITE)
    centre(d, x + 26, y + 26, "RED", F(SANS_B, 9), WHITE)
    d.rectangle([x + 8, y + 34, x + 44, y + 48], fill=(230, 70, 60))
    centre(d, x + 26, y + 38, "24h", F(SANS_B, 10), WHITE)


SCENES = {
    "tower": scene_tower, "court": scene_court, "hack": scene_hack,
    "ship": scene_ship, "flats": scene_flats, "chart": scene_chart,
    "medal": scene_medal, "parliament": scene_parliament, "gaza": scene_gaza,
    "trophy": scene_trophy, "cricket": scene_cricket, "chess": scene_chess,
    "cargo": scene_cargo, "rainbow": scene_rainbow, "server": scene_server,
}


def draw_scene(d, key, x, y, w, h):
    SCENES[key](d, x, y, w, h)


def card_frame(d, x, y, w, h, region, topic, num, label):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    col = REGION_COLOR[region]
    d.rectangle([x, y + 54, x + w, y + 55], fill=col)
    # number badge
    d.ellipse([x + 4, y + 58, x + 20, y + 74], fill=col)
    centre(d, x + 12, y + 59, str(num), F(SANS_B, 11), WHITE)
    text(d, (x + 24, y + 60), "%s · %s" % (region.upper(), topic),
         F(SANS_B, 9), col)
    # verification badge at the bottom-right of the illustration
    f_lab = F(SANS_B, 8)
    lw = d.textlength(label, font=f_lab) + 10
    rrect(d, [x + w - lw - 4, y + 42, x + w - 4, y + 52], 5, fill=WHITE,
          outline=RED_D, width=1)
    centre(d, x + w - lw // 2 - 4, y + 43, label, f_lab, RED_D)


def card_text(d, x, y, w, headline, deck):
    hl = wrap(d, headline, F(SANS_B, 12), w - 8)
    yy = y + 76
    for ln in hl[:2]:
        text(d, (x + 4, yy), ln, F(SANS_B, 12), INK)
        yy += 13
    dk = wrap(d, deck, F(SANS, 9), w - 8)
    yy = y + 100
    for ln in dk[:2]:
        text(d, (x + 4, yy), ln, F(SANS, 9), GREY)
        yy += 10


# ---------------------------------------------------------------- map
# Simplified continent outlines, in fractions of the map box.
CONTINENTS = [
    # North America
    [(0.03, 0.10), (0.10, 0.04), (0.20, 0.05), (0.26, 0.12), (0.24, 0.20),
     (0.20, 0.28), (0.14, 0.30), (0.10, 0.24), (0.04, 0.18)],
    # South America
    [(0.20, 0.36), (0.27, 0.34), (0.30, 0.42), (0.27, 0.55), (0.22, 0.62),
     (0.19, 0.52), (0.17, 0.42)],
    # Europe
    [(0.44, 0.08), (0.52, 0.05), (0.58, 0.10), (0.56, 0.16), (0.50, 0.18),
     (0.46, 0.14)],
    # Africa
    [(0.44, 0.28), (0.52, 0.26), (0.58, 0.32), (0.57, 0.44), (0.52, 0.56),
     (0.47, 0.50), (0.43, 0.38)],
    # Asia
    [(0.58, 0.06), (0.72, 0.04), (0.88, 0.08), (0.94, 0.16), (0.88, 0.24),
     (0.80, 0.30), (0.72, 0.28), (0.66, 0.34), (0.62, 0.26), (0.58, 0.16)],
    # Australia
    [(0.80, 0.66), (0.90, 0.64), (0.94, 0.72), (0.88, 0.78), (0.80, 0.74)],
]

# (story num, region, fx, fy) pin positions on the map box
PINS = [
    (1, "Mideast", 0.60, 0.34), (2, "Americas", 0.20, 0.14),
    (3, "Americas", 0.25, 0.22), (4, "Europe", 0.56, 0.13),
    (5, "Europe", 0.56, 0.19), (6, "Americas", 0.12, 0.26),
    (7, "Americas", 0.28, 0.15), (8, "Europe", 0.51, 0.07),
    (9, "Mideast", 0.60, 0.40), (10, "Africa", 0.44, 0.36),
    (11, "Oceania", 0.88, 0.70), (12, "Europe", 0.49, 0.15),
    (13, "Americas", 0.12, 0.30), (14, "Asia", 0.86, 0.74),
    (15, "Global", 0.07, 0.16),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LINE, width=1)
    for poly in CONTINENTS:
        pts = [(x + fx * w, y + fy * h) for fx, fy in poly]
        d.polygon(pts, fill=LAND, outline=(170, 150, 110))
    for num, region, fx, fy in PINS:
        px, py = x + fx * w, y + fy * h
        col = REGION_COLOR[region]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=WHITE, width=1)
        centre(d, px, py - 6, str(num), F(SANS_B, 9), WHITE)
    # legend
    ly = y + h - 16
    lx = x + 6
    for name, col in [("Americas", RED), ("Europe", BLUE), ("Mideast", AMBER),
                      ("Africa", GREEN), ("Asia", PURPLE), ("Oceania", TEAL),
                      ("Global", (88, 88, 88))]:
        d.ellipse([lx, ly, lx + 7, ly + 7], fill=col)
        text(d, (lx + 9, ly - 1), name, F(SANS_B, 7), INK)
        lx += 9 + d.textlength(name, font=F(SANS_B, 7)) + 7


def fit_one_line(d, s, font, width):
    if d.textlength(s, font=font) <= width:
        return s
    while len(s) > 4 and d.textlength(s + "…", font=font) > width:
        s = s[:-1]
    return s + "…"


def draw_also_on(d, x, y, w, h):
    text(d, (x, y), "ALSO ON WEDNESDAY 25 NOVEMBER", F(SANS_B, 13), INK)
    d.line([x, y + 17, x + w, y + 17], fill=INK, width=2)
    # build the flow: region headers + items, split into two columns
    groups = [("EUROPE", BLUE, 16, 22), ("MIDDLE EAST", AMBER, 23, 28),
              ("AMERICAS", RED, 29, 35), ("ASIA", PURPLE, 36, 42),
              ("AFRICA", GREEN, 43, 47), ("OCEANIA", TEAL, 48, 48),
              ("GLOBAL", (88, 88, 88), 49, 50)]
    flow = []
    by_num = {n: (c, t) for n, c, t in ALSO}
    for gname, gcol, lo, hi in groups:
        flow.append(("h", gname, gcol))
        for n in range(lo, hi + 1):
            flow.append(("i", n, by_num[n]))
    half = (len(flow) + 1) // 2
    cols = [flow[:half], flow[half:]]
    col_w = (w - 14) // 2
    f_h, f_n, f_t = F(SANS_B, 9), F(SANS_B, 9), F(SANS, 9)
    for ci, col in enumerate(cols):
        cx = x + ci * (col_w + 14)
        yy = y + 22
        for kind, a, b in col:
            if kind == "h":
                text(d, (cx, yy), a, f_h, b)
                yy += 12
            else:
                n, (country, line) = a, b
                badge = str(n)
                bw = 16
                d.ellipse([cx, yy - 1, cx + bw, yy + 11], fill=NAVY2)
                centre(d, cx + bw // 2, yy, badge, F(SANS_B, 8), WHITE)
                s = "%s: %s" % (country, line)
                s = fit_one_line(d, s, f_t, col_w - bw - 5)
                text(d, (cx + bw + 3, yy), s, f_t, INK)
                yy += 12


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(253, 240, 236), outline=RED, width=2)
    text(d, (x + 8, y + 6), "DATE CHECK — LEFT OUT AS OLDER NEWS",
         F(SANS_B, 12), RED_D)
    text(d, (x + 8, y + 22),
         "Every story on this page happened or was first reported on Wednesday 25 November 2026 (UTC).",
         F(SANS, 10), INK)
    text(d, (x + 8, y + 36), "Left out because they happened on an earlier day:",
         F(SANS_B, 10), RED_D)
    col_w = (w - 16) // 2
    f = F(SANS, 10)
    for i, (s, when) in enumerate(DATECHECK):
        cx = x + 8 + (i // 5) * col_w
        yy = y + 48 + (i % 5) * 11
        text(d, (cx, yy), "✕  %s  (%s)" % (s, when), f, INK)
    text(d, (x + 8, y + h - 14),
         "Not yet: Sweden's parliament votes on Kristersson as PM — Mon 30 Nov.",
         F(SANS_B, 10), RED_D)


def draw_footer(d):
    lines = wrap(d, FOOTER, F(SANS, 10), W - 24)
    yy = 986
    for ln in lines:
        centre(d, W // 2, yy, ln, F(SANS, 10), GREY)
        yy += 12


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    masthead(d)
    chips_row(d)
    timeline(d)
    # feature cards: 3 rows x 5 columns
    cw, chh, gap = 196, 128, 5
    for idx, (num, region, topic, headline, deck, label, scene) in enumerate(FEATURES):
        r, c = divmod(idx, 5)
        x = 12 + c * (cw + gap)
        yy = 186 + r * (chh + 3)
        draw_scene(d, scene, x, yy, cw, 54)
        card_frame(d, x, yy, cw, chh, region, topic, num, label)
        card_text(d, x, yy, cw, headline, deck)
    # map + also-on
    text(d, (12, 574), "WHERE IT HAPPENED", F(SANS_B, 13), INK)
    d.line([12, 591, 342, 591], fill=INK, width=2)
    draw_map(d, 12, 596, 330, 258)
    draw_also_on(d, 354, 574, W - 12 - 354, 280)
    # date check + footer
    draw_datecheck(d, 12, 862, W - 24, 118)
    draw_footer(d)
    return img


def main():
    img = build()
    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
