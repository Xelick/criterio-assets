"""Giant kinetic lyric type for the Criterio concert video (1920x1080, 40 s).

Retro soft-serif look (Fraunces SuperSoft Wonky Black), cream words with an iris-blue
extrude, key words in brand yellow. Each word pops in as it is sung; short chunks of
one or two lines replace each other. Word times: Whisper consensus (see gen_subs.py).
"""
import sys
from PIL import ImageFont

FONT = sys.argv[1] if len(sys.argv) > 1 else "fonts/Fraunces-SoftBlack.ttf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "criterio_kinetic.ass"
FAMILY = "Fraunces 144pt SuperSoft Wonky Black"

W, H = 1920, 1080
K, BASE = 0.677, 0.29   # calibrated against libass for this font
LEAD = 0.06

CREAM, YELLOW, BLUE = "&H00E6F6FF&", "&H0000DAFF&", "&H00E62727&"  # #FFF6E6, #ffda00, #2727e6

SIZE, MAXW, BOTTOM = 270, 1720, 990    # chunk text size, max line width, block bottom
KEY_SIZE, KEY_CY = 430, 690

# chunks: lines of (word, time); '*' marks a yellow key word
CHUNKS = [
    ([[("Menú", 3.98)], [("en", 5.07), ("foto,", 5.35)]], 6.95),
    ([[("sumas", 7.05)], [("a", 7.45), ("mano", 7.65)]], 9.30),
    ([[("Tu", 12.40), ("negocio", 12.70)]], 13.44),
    ([[("a", 13.52), ("punta", 13.75)], [("de", 14.25), ("*chat", 14.55)]], 15.90),
    ([[("Cuéntame", 16.75)]], 17.74),
    ([[("qué", 17.82)], [("*vendes", 18.25)]], 21.40),
    ("¡Criterio!", 22.28, 24.10),
    ([[("Arman", 24.25), ("el", 24.92)], [("*pedido,", 25.20)]], 25.97),
    ([[("te", 26.05), ("llega", 26.25)], [("al", 26.78), ("*chat", 27.15)]], 28.15),
    ([[("Trabaja", 28.30)], [("menos,", 28.97)]], 29.94),
    ([[("*vende", 30.02)], [("*más", 30.62)]], 33.40),
    ("¡Criterio!", 36.72, 40.00),
]
DROP = 23.58


def ts(t):
    cs = int(round(max(0.0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def ev(layer, start, end, text):
    return f"Dialogue: {layer},{ts(start)},{ts(end)},Kin,,0,0,0,,{text}"


def look(size, color):
    d = max(4, round(size * 0.045))   # extrude depth scales with the type
    return rf"\1c{color}\3c{BLUE}\4c{BLUE}\bord{max(2, round(size * 0.012))}\xshad{d}\yshad{round(d * 1.2)}\4a&H00&"


def pop(k, dur_ms):
    tilt = (-7, 6, -5, 8)[k % 4]
    out = min(140, dur_ms // 3)
    return (rf"\frz{tilt}\fscx0\fscy0\t(0,120,\frz0\fscx116\fscy116)\t(120,210,\fscx100\fscy100)"
            rf"\t({dur_ms - out},{dur_ms},\fscx112\fscy112\alpha&HFF&)")


def chunk(lines, end, k0):
    f = ImageFont.truetype(FONT, SIZE * K)
    space = f.getlength(" ") * 1.4
    widest = max(sum(f.getlength(w.lstrip("*")) for w, _ in ln) + space * (len(ln) - 1) for ln in lines)
    size = SIZE * min(1.0, MAXW / widest)
    f = ImageFont.truetype(FONT, size * K)
    space = f.getlength(" ") * 1.4
    lh = size * 0.98
    out, k = [], k0
    for li, ln in enumerate(lines):
        cy = BOTTOM - (len(lines) - 1 - li) * lh - size * 0.35
        widths = [f.getlength(w.lstrip("*")) for w, _ in ln]
        x = W / 2 - (sum(widths) + space * (len(ln) - 1)) / 2
        for (word, t), w in zip(ln, widths):
            key = word.startswith("*")
            word = word.lstrip("*")
            cx = x + w / 2
            x += w + space
            start = t - LEAD
            dur = int((end - start) * 1000)
            tag = rf"{{\an5\pos({cx:.1f},{cy:.1f})\org({cx:.1f},{cy:.1f}){look(size, YELLOW if key else CREAM)}{pop(k, dur)}}}"
            out.append(ev(1, start, end, tag + word))
            k += 1
    return out, k


def key(text, t, end):
    f = ImageFont.truetype(FONT, KEY_SIZE * K)
    size = KEY_SIZE * min(1.0, 1800 / f.getlength(text))
    start = t - LEAD
    dur = int((end - start) * 1000)
    drop = int((DROP - start) * 1000)
    extra = (rf"\t({drop},{drop + 90},\fscx112\fscy112)\t({drop + 90},{drop + 220},\fscx100\fscy100)"
             rf"\t({dur - 150},{dur},\fscx115\fscy115\alpha&HFF&)") if 0 < drop < dur else rf"\t(300,{dur},\fscx108\fscy108)"
    tag = (rf"{{\an5\pos({W / 2},{KEY_CY})\org({W / 2},{KEY_CY}){look(size, YELLOW)}"
           rf"\frz-12\fscx0\fscy0\t(0,130,\frz-3\fscx122\fscy122)\t(130,240,\fscx100\fscy100){extra}}}")
    return [ev(2, start, end, tag + text)]


HEADER = f"""[Script Info]
Title: Criterio - letra gigante
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Kin,{FAMILY},{SIZE},&H00E6F6FF,&H00E6F6FF,&H00E62727,&H00E62727,0,0,0,0,100,100,0,0,1,2,8,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

events, k = [], 0
for c in CHUNKS:
    if isinstance(c[0], str):
        events += key(*c)
    else:
        evs, k = chunk(c[0], c[1], k)
        events += evs
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(HEADER + "\n".join(events) + "\n")
print(f"{OUT}: {len(events)} events")
