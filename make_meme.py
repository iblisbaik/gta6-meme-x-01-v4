#!/usr/bin/env python3
"""Generate the gta6-meme-x-01-v4 meme: a realistic PAYSLIP / EARNINGS
STATEMENT from the Leonida Waiting Authority for one very patient gamer:
13 years as a Professional GTA VI Waiter, 4,812 days waited, net pay
-$820.01 — the wait costs more than the game — with the $250 make.fun
bounty payout from my AI agent as the payment method. 1024x1024 PNG,
body text >= 24px so it stays legible when the judge shrinks it to
480x480. The real make.fun ghost is composited from
../press-mark-1024.png (never redrawn).

Numbers (all verified in the build, see NOTES.md):
  17 Sep 2013 -> 20 Nov 2026 = 4,812 days = 115,488 hours
  Gross pay $79.99 - deductions $900.00 = net pay -$820.01
  -$820.01 + $250.00 bounty payout = balance -$570.01
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
GHOST_PATH = os.path.expanduser("~/workspace/makefun/press-mark-1024.png")
OUT = os.path.join(HERE, "meme.png")

W = H = 1024
NAVY = (26, 42, 74)          # payslip header / payment band
NAVY_LT = (233, 238, 245)    # employee box fill
PAPER = (255, 255, 255)      # payslip paper
INK = (20, 20, 20)
GREY = (110, 110, 110)
RED = (178, 24, 38)          # net-pay red
MAGENTA = (196, 0, 110)      # make.fun accent strip
GOLD = (255, 214, 90)
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 52  # side margin


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, size, text, max_w):
    while size > 10:
        f = font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def text(x, y, s, path, size, color=INK, anchor="la", max_w=None):
    f = font(path, size) if max_w is None else fit(path, size, s, max_w)
    d.text((x, y), s, font=f, fill=color, anchor=anchor)
    return f.size


def rule(y, x0=M, x1=W - M, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def section_head(y, title, right=""):
    text(M, y, title, SANS_B, 28, color=NAVY)
    if right:
        text(W - M, y, right, MONO_B, 24, color=NAVY, anchor="ra")
    rule(y + 36, width=3, color=NAVY)
    return y + 46


def table_row(y, label, amount, bold=False, size=25):
    """Label left, dotted leader, amount right-aligned in mono."""
    p_txt = SANS_B if bold else SANS
    p_amt = MONO_B if bold else MONO
    f_lab = font(p_txt, size)
    f_amt = font(p_amt, size)
    d.text((M, y), label, font=f_lab, fill=INK)
    amt_w = d.textlength(amount, font=f_amt)
    amt_x = W - M - amt_w
    lab_w = d.textlength(label, font=f_lab)
    dot_f = font(MONO, 18)
    dot_w = d.textlength(".", font=dot_f)
    x = M + lab_w + 10
    while x < amt_x - 10:
        d.text((x, y + 7), ".", font=dot_f, fill=GREY)
        x += dot_w + 4
    d.text((amt_x, y), amount, font=f_amt, fill=INK)
    return y + 33


# ---- 1. navy header band (0-104) ----
d.rectangle([0, 0, W, 104], fill=NAVY)
text(M, 16, "LEONIDA WAITING AUTHORITY", SANS_B, 40, color=(255, 255, 255))
text(M, 64, "PAYROLL DEPARTMENT  ·  VICE CITY, FLORIDA", SANS, 21,
     color=(190, 200, 220))
text(W - M, 20, "PAYSLIP No.", SANS, 19, color=(190, 200, 220), anchor="ra")
text(W - M, 44, "VI-2013-4812", MONO_B, 25, color=(255, 255, 255), anchor="ra")

# ---- 2. title row ----
text(M, 120, "EARNINGS STATEMENT", SANS_B, 48, color=NAVY)
text(W - M, 134, "PAY DATE  20 NOV 2026", MONO_B, 23, color=NAVY, anchor="ra")
rule(180, width=3, color=NAVY)

# ---- 3. employee box (192-272) ----
d.rectangle([M, 192, W - M, 272], fill=NAVY_LT)
text(M + 16, 202, "EMPLOYEE", SANS_B, 19, color=GREY)
text(M + 16, 224, "ONE VERY PATIENT GAMER", SANS_B, 28)
text(580, 202, "EMPLOYEE ID", SANS_B, 19, color=GREY)
text(580, 224, "GTA-VI-2013-4812", MONO_B, 27)
y = 282
# Left/right pairs: shrink the right text to the space left after the left.
def pair(y, left_s, right_s, left_path, left_size, right_path, right_size,
         color=INK, rcolor=None):
    text(M, y, left_s, left_path, left_size, color=color)
    lw = d.textlength(left_s, font=font(left_path, left_size))
    f = fit(right_path, right_size, right_s, (W - M) - (M + lw + 24))
    d.text((W - M, y), right_s, font=f, fill=rcolor or color, anchor="ra")

pair(y, "ROLE:  Professional GTA VI Waiter",
     "PAY PERIOD:  17 SEP 2013 – 20 NOV 2026", SANS_B, 25, MONO_B, 23)
y += 30
pair(y, "DEPARTMENT:  Waiting, Division VI", "DAYS WAITED:  4,812",
     SANS, 25, MONO_B, 25, rcolor=RED)

# ---- 4. earnings ----
y = section_head(352, "EARNINGS", "YTD")
y = table_row(y, "GTA VI — 1 copy, pre-ordered 17 Sep 2013", "$79.99")
y = table_row(y, "Waiting overtime — 115,488 hrs × $0.00/hr", "$0.00")
y = table_row(y, "Trailer rewatches — 1,337 × $0.00", "$0.00")
y = table_row(y, "Hype bonus — 2 delays", "$0.00")
rule(y + 1, width=2)
y += 9
y = table_row(y, "GROSS PAY", "$79.99", bold=True)

# ---- 5. deductions ----
y = section_head(y + 4, "DEDUCTIONS", "YTD")
y = table_row(y, "Rent — 13 years, occupant still waiting", "$900.00")
y = table_row(y, "Hype tax — 2 delays, 0 apologies accepted", "$0.00")
y = table_row(y, "Patience — none left", "$0.00")
rule(y + 1, width=2)
y += 9
y = table_row(y, "TOTAL DEDUCTIONS", "$900.00", bold=True)

# ---- 6. net pay band ----
rule(y + 8, width=3, color=RED)
y += 18
text(M, y, "NET PAY", SANS_B, 42, color=RED)
text(W - M, y, "–$820.01", MONO_B, 48, color=RED, anchor="ra")
y += 50
text(M, y, "YOU OWE US — THE WAIT COSTS MORE THAN THE GAME.",
     SANS_B, 25, color=RED)

# ---- 7. payment box (dark navy, ghost badge) ----
box_y = y + 28
box_h = 112
d.rectangle([M, box_y, W - M, box_y + box_h], fill=NAVY)
ghost = Image.open(GHOST_PATH).convert("RGBA").resize((88, 88),
                                                     Image.LANCZOS)
img.paste(ghost, (M + 12, box_y + 12), ghost)
gx = M + 116
text(gx, box_y + 10, "PAID BY MY AI AGENT ON MAKE.FUN", SANS_B, 28,
     color=(255, 255, 255))
text(gx, box_y + 46, "+$250.00 BOUNTY PAYOUT — my AI agent won on make.fun",
     SANS_B, 24, color=(255, 255, 255))
text(gx, box_y + 80, "BALANCE AFTER PAYOUT:  –$570.01  —  STILL WAITING.",
     MONO_B, 20, color=GOLD)

# ---- 8. magenta footer strip ----
fy = box_y + box_h + 12
strip = "13 YEARS  ·  4,812 DAYS  ·  2 DELAYS  ·  1,337 REWATCHES  ·  0 LAUNCH DATES KEPT"
d.rectangle([M, fy, W - M, fy + 40], fill=MAGENTA)
f = fit(SANS_B, 24, strip, W - 2 * M - 20)
d.text((W / 2, fy + 20), strip, font=f, fill=(255, 255, 255), anchor="mm")

assert fy + 40 <= H, f"layout overflow: footer ends {fy + 40} > {H}"
img.save(OUT, "PNG")
print("wrote", OUT, img.size, "footer ends at y =", fy + 40)
