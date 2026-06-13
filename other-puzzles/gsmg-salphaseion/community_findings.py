#!/usr/bin/env python3
"""
Two verified tools/findings from the 2026-06 community-log review.

1) FEFEFE image marker  (find_fefefe_marker):
   The puzzle image (puzzle.png) contains exactly ONE 25x25 grid cell colored
   (254,254,254) instead of pure white (255,255,255) — a deliberate "glitch in
   the matrix" / "in the eye of the beholder" marker, located just LEFT of the
   rabbit. Verified position: grid cell (row 7, col 4) in the 14x14 matrix
   (0-indexed) = spiral index 163 (0-based) = byte 21, bit 3 of the phase-0
   URL decode (URL char #21 = 'n' in gsmg.io/theseedisplanted).

2) Bacon (rot-1) cipher  (fBacon / tBacon):
   A community-used encoding: standard Baconian on a/b, but with an inverted
   (NOT, &0x7f) alphabet. Decodes a/b strings to ASCII. Used by chat members to
   pass Matrix-quote banter (e.g. "everythingthathasabeginninghasanend"); the
   puzzle's own a/b strings (binary1->matrixsumlist, binary2->enter) are plain
   8-bit ASCII, NOT Baconian, so this is a tool rather than a puzzle step.
"""

def fBacon(s):
    s = "".join(c for c in s if c in "ab")
    return "".join(
        chr(~int(s[i:i+5].translate(str.maketrans("ab", "01")), 2) & 0x7F)
        for i in range(0, len(s) - len(s) % 5, 5)
    )

def tBacon(s):
    return "".join(
        bin(~(ord(ch) ^ 0x7F) & 0b11111)[2:].zfill(5).translate(str.maketrans("01", "ba"))
        for ch in s
    )

def find_fefefe_marker(png_path):
    from PIL import Image
    im = Image.open(png_path).convert("RGBA")
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if px[x, y] == (254, 254, 254, 255):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    cell = w / 14.0
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    return {"row": int(cy/cell), "col": int(cx/cell),
            "px_count": len(xs), "bbox": (min(xs), min(ys), max(xs), max(ys))}

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    png = os.path.join(here, "..", "..", "puzzle.png")
    print("FEFEFE marker:", find_fefefe_marker(png))
    print("Bacon self-test:", fBacon(tBacon("hello")))
