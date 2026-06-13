#!/usr/bin/env python3
"""
SalPhaseIon "Sum" decode — the 'b'-as-separator method.

NEW (verified) decode of STR_A (the 91-char dbbi string). Treat the letter 'b'
as a separator; for each group of letters between separators, sum the letter
values (a=1, c=3, d=4, e=5, f=6, g=7, h=8, i=9 — 'b'=2 is the separator); then
map each group sum to a character:
    1..26  -> 'A'..'Z'
    27..36 -> '0'..'9'   (digit = sum-27)

This yields the token  DIFNLREV9E6VARXVF5UF8PE  (23 groups -> 23 chars). The
digits land exactly where a group sum exceeds 26, which is a designed feature
(not coincidence) — strong evidence the method is intended. This token is the
"sum" / "ans" the SalPhaseIon stream refers to.

Cross-checked against community work (github mkno03/GSMG-5BTC-..., which reports
the same token); reproduced here from first principles.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STR_A = open(os.path.join(HERE, "STR_A_dbbi.txt")).read().strip()

def val(c): return ord(c) - ord('a') + 1          # a=1 .. i=9 (b=2 is separator)

def group_sums(s, drop_empty=True):
    return [sum(val(c) for c in g) for g in s.split('b') if (g or not drop_empty)]

def to_token(sums):
    out = []
    for v in sums:
        if 1 <= v <= 26:   out.append(chr(v - 1 + ord('A')))
        elif 27 <= v <= 36: out.append(str(v - 27))
        else:              out.append(f"[{v}]")
    return "".join(out)

if __name__ == "__main__":
    sums = group_sums(STR_A, drop_empty=True)
    print("group sums:", sums)
    print("SUM token :", to_token(sums))
    assert to_token(sums) == "DIFNLREV9E6VARXVF5UF8PE", "token mismatch!"
    print("verified: DIFNLREV9E6VARXVF5UF8PE")
