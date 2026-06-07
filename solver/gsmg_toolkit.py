"""
GSMG.IO 5 BTC puzzle - reproducible solver toolkit.

Every function in here is either:
  (a) VALIDATED - it reproduces a publicly-known/solved step, or
  (b) EXPERIMENTAL - clearly marked, used to probe the unsolved frontier.

Nothing here depends on the (broken in some envs) `cryptography` package; AES is
handled through the `openssl` CLI, which is also exactly how the puzzle creator
encrypted each stage.

Run `python3 gsmg_toolkit.py selftest` to confirm the validated steps still pass.
"""

from __future__ import annotations
import base64
import hashlib
import subprocess
from collections import Counter

# ---------------------------------------------------------------------------
# Known data (verbatim from the puzzle)
# ---------------------------------------------------------------------------

PHASE0_URL = "gsmg.io/theseedisplanted"

# The two AES blobs that gate the prize. Both are OpenSSL `Salted__` AES-256-CBC.
# Each decrypts to 80 bytes of ciphertext == 64-79 bytes of plaintext, i.e. the
# exact size of a 64-hex-char private key (the VIC clue: the keys belong to
# "half and better half", matching the 1.25 + 3.75 BTC split).
AES_PHASE32 = (
    "U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
    "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"
)
AES_SALPHASEION = (
    "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
    "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
)

# SalPhaseIon: the two big, still-unsolved base-9 (a..i) strings, with the
# decoded `matrixsumlist` instruction sitting between them.
SALPH_STR_A = (
    "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbf"
    "beeggecbedcibfbffgigbeeeabe"
)
SALPH_STR_B = (
    "faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahi"
    "gceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgd"
    "eefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaec"
    "bceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgi"
    "bggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihii"
    "igiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeg"
    "gdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiif"
    "dgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeeh"
    "gigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic"
)

# ---------------------------------------------------------------------------
# AES (OpenSSL-compatible) -- VALIDATED against phase 3 -> 3.2
# ---------------------------------------------------------------------------
# The creator's scheme, used at every encrypted stage:
#   passphrase = sha256_hexdigest(plaintext_password)
#   openssl aes-256-cbc -a -d   (default KDF == sha256 on modern openssl)

def openssl_decrypt(blob_b64: str, passphrase: str, md: str = "sha256") -> bytes | None:
    """Decrypt an OpenSSL 'Salted__' base64 blob. Returns plaintext or None."""
    p = subprocess.run(
        ["openssl", "aes-256-cbc", "-d", "-a", "-md", md, "-pass", f"pass:{passphrase}"],
        input=blob_b64.encode(), capture_output=True,
    )
    return p.stdout if p.returncode == 0 else None


def try_password(blob_b64: str, password: str, md: str = "sha256") -> bytes | None:
    """Try a *plaintext* password: hashes it the way the puzzle does, then decrypts."""
    passphrase = hashlib.sha256(password.encode()).hexdigest()
    return openssl_decrypt(blob_b64, passphrase, md=md)


def looks_like_plaintext(pt: bytes | None) -> bool:
    if not pt:
        return False
    printable = sum(1 for b in pt if 32 <= b < 127) / len(pt)
    return printable > 0.85


# ---------------------------------------------------------------------------
# SalPhaseIon decoders -- VALIDATED
# ---------------------------------------------------------------------------

def abba_to_ascii(s: str) -> str:
    """a=0,b=1 binary -> ascii. Reproduces 'matrixsumlist' / 'enter'."""
    bits = s.replace(" ", "").replace("a", "0").replace("b", "1")
    return "".join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits) - 7, 8))


def aio_decimal_to_ascii(s: str) -> str:
    """a..i=1..9, o=0 -> read as decimal int -> hex -> ascii.
    Reproduces 'lastwordsbeforearchichoice' / 'thispassword'."""
    import binascii
    tr = str.maketrans("abcdefghio", "1234567890")
    h = hex(int(s.replace(" ", "").translate(tr)))[2:]
    if len(h) % 2:
        h = "0" + h
    return binascii.unhexlify(h).decode("latin-1")


# ---------------------------------------------------------------------------
# Phase-0 puzzle image -- VALIDATED (reproduces gsmg.io/theseedisplanted)
# ---------------------------------------------------------------------------

def _classify(px):
    r, g, b = px
    if r > 140 and g > 140 and b < 130:
        return "Y"  # yellow
    if b > 120 and b - r > 40 and b - g > 40:
        return "U"  # blue
    if r < 100 and g < 100 and b < 100:
        return "K"  # black
    if r > 150 and g > 150 and b > 150:
        return "W"  # white
    return "?"


def _find(name: str) -> str:
    """Locate an asset whether run from repo root or solver/."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (name, os.path.join(here, "..", name), os.path.join(here, name)):
        if os.path.exists(cand):
            return cand
    return name


def read_grid(png_path: str | None = None, N: int = 14):
    """Return the NxN color grid of the puzzle image (above the red line)."""
    from PIL import Image
    import numpy as np
    im = np.array(Image.open(_find(png_path or "puzzle.png")).convert("RGB")).astype(int)
    G = im[:1047, :1048]
    H, W, _ = G.shape
    ch, cw = H / N, W / N
    grid = []
    for r in range(N):
        row = []
        for c in range(N):
            y, x = int((r + .5) * ch), int((c + .5) * cw)
            med = np.median(G[y - 12:y + 12, x - 12:x + 12].reshape(-1, 3), axis=0)
            row.append(_classify(med))
        grid.append(row)
    return grid


def spiral_ccw(N: int):
    """Counter-clockwise, outside-in spiral starting top-left going DOWN.
    This is the ordering that decodes phase 0."""
    top, bottom, left, right = 0, N - 1, 0, N - 1
    coords = []
    while top <= bottom and left <= right:
        for r in range(top, bottom + 1):
            coords.append((r, left))
        for c in range(left + 1, right + 1):
            coords.append((bottom, c))
        for r in range(bottom - 1, top - 1, -1):
            coords.append((r, right))
        for c in range(right - 1, left, -1):
            coords.append((top, c))
        top += 1; bottom -= 1; left += 1; right -= 1
    return coords


def decode_phase0(grid):
    coords = spiral_ccw(len(grid))
    bits = "".join("0" if grid[r][c] in ("W", "Y") else "1" for r, c in coords)
    return "".join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits) - 7, 8))


def analyze_colors(grid):
    """Yellow/Blue analysis behind the 2020-01-14 hint.
    Returns dict with counts and the byte indices each color marks."""
    coords = spiral_ccw(len(grid))
    ypos = [i + 1 for i, (r, c) in enumerate(coords) if grid[r][c] == "Y"]
    upos = [i + 1 for i, (r, c) in enumerate(coords) if grid[r][c] == "U"]
    return {
        "yellow_count": len(ypos),
        "blue_count": len(upos),
        "yellow_spiral_pos": ypos,
        "blue_spiral_pos": upos,
        # every colored square sits on a multiple of 8 == the LSB (8th bit) of a byte
        "yellow_bytes": [p // 8 for p in ypos],
        "blue_bytes": [p // 8 for p in upos],
        "all_on_byte_boundary": all(p % 8 == 0 for p in ypos + upos),
    }


# ---------------------------------------------------------------------------
# Self test
# ---------------------------------------------------------------------------

def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    # SalPhaseIon decoders
    b1 = ("abbabbababbaaaababbbabaaabbbaabaabbabaababbbbaaaabbbaabbabbbaba"
          "babbabbababbabbaaabbabaababbbaabbabbbabaa")
    check("abba -> matrixsumlist", abba_to_ascii(b1) == "matrixsumlist")
    b2 = "abbaabababbabbbaabbbabaaabbaabababbbaaba"
    check("abba -> enter", abba_to_ascii(b2) == "enter")
    s1 = ("agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde")
    check("aio -> lastwordsbeforearchichoice",
          aio_decimal_to_ascii(s1) == "lastwordsbeforearchichoice")
    s2 = "cfobfdhgdobdgooiigdocdaoofidh"
    check("aio -> thispassword", aio_decimal_to_ascii(s2) == "thispassword")

    # AES scheme (needs the on-disk phase3.2 blob to fully validate; skip if absent)
    import os
    blob_path = _find("phase3-assets/phase3.2-aes.txt")
    if os.path.exists(blob_path):
        pw = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
        passph = hashlib.sha256(pw.encode()).hexdigest()
        with open(blob_path) as fp:
            blob = fp.read()
        pt = openssl_decrypt(blob, passph)
        check("AES phase3.2 decrypts to Architect intro",
              pt is not None and pt.startswith(b"I've been waiting for you"))

    # Puzzle image (needs PIL/numpy + puzzle.png; skip if absent)
    try:
        grid = read_grid()
        check("phase0 image -> gsmg.io/theseedisplanted",
              decode_phase0(grid) == PHASE0_URL)
        a = analyze_colors(grid)
        check("yellow=9 blue=15 on byte boundaries",
              a["yellow_count"] == 9 and a["blue_count"] == 15 and a["all_on_byte_boundary"])
    except Exception as e:  # pragma: no cover
        print(f"[SKIP] image checks ({e})")

    print("\nALL GOOD" if ok else "\nSOME CHECKS FAILED")
    return ok


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    else:
        print(__doc__)
        print("Commands: selftest")
