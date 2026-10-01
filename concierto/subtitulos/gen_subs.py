"""Karaoke-style lyric subtitles for the Criterio concert video (1920x1080, 40 s).

Word times come from Whisper (small, medium, large-v3) on the final mix, averaged
and shifted ~60 ms early so each word lands as it is sung. Layout is measured with
Pillow and converted to libass units (K = Pillow px per ASS font-size unit).
"""
import sys
from PIL import ImageFont

FONT = sys.argv[1] if len(sys.argv) > 1 else "fonts/NunitoSans-Black.ttf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "criterio_subs.ass"

W, H = 1920, 1080
K = 0.699          # calibrated: libass size 100 == Pillow size 69.9
BASE = 0.27        # with \an5, the baseline sits 0.27*size below \pos
LEAD = 0.06        # show each word slightly before it is sung

WHITE, YELLOW, DARK = "&H00FFFFFF&", "&H0000DAFF&", "&H00181111&"  # #ffda00, #111118

SL, CY = 92, 878           # lyric size and line centre
SK, CYK = 150, 862         # "¡CRITERIO!" size and band centre

LINES = [
    {"words": [("Menú", 3.98), ("en", 5.07), ("foto,", 5.35), ("sumas", 7.05), ("a", 7.45), ("mano", 7.65)], "end": 9.30},
    {"words": [("Tu", 12.40), ("negocio", 12.70), ("a", 13.52), ("punta", 13.75), ("de", 14.25), ("chat", 14.55)], "end": 15.90},
    {"words": [("Cuéntame", 16.75), ("qué", 17.82), ("vendes", 18.25)], "end": 21.40},
    {"key": "¡CRITERIO!", "start": 22.28, "end": 24.10},
    {"words": [("Arman", 24.25), ("el", 24.92), ("pedido,", 25.20), ("te", 26.05), ("llega", 26.25), ("al", 26.78), ("chat", 27.15)], "end": 28.15},
    {"words": [("Trabaja", 28.30), ("menos,", 28.97), ("vende", 30.02), ("más", 30.62)], "band_from": 2, "end": 33.40},
    {"key": "¡CRITERIO!", "start": 36.72, "end": 40.00},
]


def ts(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def font(size):
    return ImageFont.truetype(FONT, size * K)


def rect(w, h):
    return f"m 0 0 l {w:.0f} 0 l {w:.0f} {h:.0f} l 0 {h:.0f}"


def ev(layer, start, end, text, style="Lyric"):
    return f"Dialogue: {layer},{ts(start)},{ts(end)},{style},,0,0,0,,{text}"


def lyric_line(line):
    f = font(SL)
    words = line["words"]
    space = f.getlength(" ")
    widths = [f.getlength(w) for w, _ in words]
    total = sum(widths) + space * (len(words) - 1)
    x = W / 2 - total / 2
    band_from = line.get("band_from")
    out, lefts = [], []
    for i, ((word, t), w) in enumerate(zip(words, widths)):
        lefts.append(x)
        cx = x + w / 2
        x += w + space
        start, end = t - LEAD, line["end"]
        nxt = words[i + 1][1] - LEAD if i + 1 < len(words) else min(end - 0.2, start + 0.9)
        hl = int(max(0.15, min(0.9, nxt - start)) * 1000)
        on_band = band_from is not None and i >= band_from
        pop = r"\fscx70\fscy70\alpha&HFF&\t(0,120,\alpha&H00&\fscx108\fscy108)\t(120,200,\fscx100\fscy100)"
        color = rf"\1c{DARK}\bord0\shad0" if on_band else rf"\1c{YELLOW}\t({hl},{hl + 120},\1c{WHITE})"
        tag = rf"{{\an5\move({cx:.1f},{CY + 18},{cx:.1f},{CY},0,160)\blur1{pop}{color}\fad(0,180)}}"
        out.append(ev(1, start, end, tag + word))
    if band_from is not None:
        # yellow band that wipes in from the left behind the key words
        b0 = f.getbbox(words[band_from][0], anchor="ls")
        bl = f.getbbox(words[-1][0], anchor="ls")
        top = min(f.getbbox(w, anchor="ls")[1] for w, _ in words[band_from:])
        bot = max(f.getbbox(w, anchor="ls")[3] for w, _ in words[band_from:])
        padx, pady = 22, 14
        left = lefts[band_from] + b0[0] - padx
        right = lefts[-1] + bl[2] + padx
        base_y = CY + BASE * SL
        top_y, bot_y = base_y + top - pady, base_y + max(bot, 0) + pady
        bw, bh = right - left, bot_y - top_y
        start = words[band_from][1] - LEAD - 0.04
        tag = (rf"{{\an4\pos({left:.1f},{(top_y + bot_y) / 2:.1f})\p1\1c{YELLOW}\bord0\shad4\4c{DARK}\4a&H90&"
               rf"\fscx0\t(0,160,\fscx100)\fad(0,180)}}")
        out.append(ev(0, start, line["end"], tag + rect(bw, bh) + r"{\p0}"))
    return out


def key_line(line):
    f = font(SK)
    text, start, end = line["key"], line["start"] - LEAD, line["end"]
    b = f.getbbox(text, anchor="ls")
    padx, pady = 46, 26
    bw, bh = (b[2] - b[0]) + 2 * padx, (b[3] - b[1]) + 2 * pady
    # put the ink centre of the text on the band centre
    ink_cy = BASE * SK + (b[1] + b[3]) / 2
    ink_cx = (b[0] + b[2]) / 2 - f.getlength(text) / 2
    tx, ty = W / 2 - ink_cx, CYK - ink_cy
    rot = rf"\org({W / 2:.0f},{CYK})\frz3"
    fade = r"\fad(0,250)" if end < 39.9 else ""
    band = (rf"{{\an5\pos({W / 2:.0f},{CYK}){rot}\p1\1c{YELLOW}\bord0\shad7\4c{DARK}\4a&H80&"
            rf"\fscx0\fscy85\t(0,150,\fscx106\fscy100)\t(150,230,\fscx100){fade}}}")
    txt = (rf"{{\an5\pos({tx:.1f},{ty:.1f}){rot}\1c{DARK}\bord0\shad0"
           rf"\alpha&HFF&\fscx140\fscy140\t(60,170,\alpha&H00&\fscx95\fscy95)\t(170,260,\fscx100\fscy100){fade}}}")
    return [ev(0, start, end, band + rect(bw, bh) + r"{\p0}", "Key"), ev(1, start, end, txt + text, "Key")]


HEADER = f"""[Script Info]
Title: Criterio - letra dinamica
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Nunito Sans Black,{SL},&H00FFFFFF,&H00FFFFFF,&H00181111,&H80181111,0,0,0,0,100,100,0,0,1,3.2,3,5,0,0,0,1
Style: Key,Nunito Sans Black,{SK},&H00181111,&H00181111,&H00181111,&H80181111,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

events = []
for line in LINES:
    events += key_line(line) if "key" in line else lyric_line(line)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(HEADER + "\n".join(events) + "\n")
print(f"{OUT}: {len(events)} events")
