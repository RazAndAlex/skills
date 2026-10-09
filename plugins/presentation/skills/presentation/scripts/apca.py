# -*- coding: utf-8 -*-
"""APCA 0.1.9 (W3 SAPC-APCA reference constants). Lc for text on background."""
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 apca.py --demo")
        sys.exit(2)

def Y(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126729*r**2.4 + 0.7151522*g**2.4 + 0.0721750*b**2.4

def lc(txt, bg):
    Ytxt, Ybg = Y(txt), Y(bg)
    blkThrs, blkClmp, scale = 0.022, 1.414, 1.14
    Ytxt = Ytxt + (blkThrs - Ytxt)**blkClmp if Ytxt < blkThrs else Ytxt
    Ybg  = Ybg  + (blkThrs - Ybg )**blkClmp if Ybg  < blkThrs else Ybg
    if abs(Ybg - Ytxt) < 0.0005: return 0.0
    if Ybg > Ytxt:                       # normal polarity: dark text on light bg
        S = (Ybg**0.56 - Ytxt**0.57) * scale
        out = 0.0 if S < 0.1 else S - 0.027
    else:                                # reverse: light text on dark bg
        S = (Ybg**0.65 - Ytxt**0.62) * scale
        out = 0.0 if S > -0.1 else S + 0.027
    return round(out * 100, 1)

for name, c in [("--text", "#e8e5f2"), ("--text-2", "#aaa5c0"), ("amber", "#e8a33d"),
                ("green", "#8fd4a8"), ("red", "#e4808a"), ("lav", "#b9a6f2")]:
    print("%-9s %s  Lc %s" % (name, c, abs(lc(c, "#0d0c14"))))
