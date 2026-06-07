"""Straddling-checkerboard / VIC decoder.

VALIDATED: reproduces the Phase 3.2 VIC step exactly. The prefix digits (1, 4)
are literally the puzzle's hint "one for one, four for one"; the alphabet
'fubcdora/lethingkymvpszjqwx.' is the one derived in Phase 3.2.

The same decoder applied to the SalPhaseIon strings STR_A / STR_B with prime
prefixes {2,3,5,7} (the 2021-03-01 hint) does NOT yield English under any
prefix pair, digit mapping (a-i->1-9 or 0-8), or reversal -- so if these strings
are VIC-enciphered they use a different (still-unknown) keyed alphabet.
"""
from itertools import permutations

PHASE32_ALPHABET = "fubcdora/lethingkymvpszjqwx."  # 8 + 10 + 10 = 28 cells

def make_board(alpha: str, prefixes):
    """10-column straddling checkerboard. Top row = the 8 non-prefix columns,
    then one 10-column row per prefix digit, filled from `alpha` in order."""
    cols = list(range(10))
    singles = [c for c in cols if c not in prefixes]
    table = {}
    i = 0
    for c in singles:
        table[(c,)] = alpha[i]; i += 1
    for p in prefixes:
        for c in cols:
            table[(p, c)] = alpha[i]; i += 1
    return table

def decode(digit_stream, alpha=PHASE32_ALPHABET, prefixes=(1, 4)):
    table = make_board(alpha, list(prefixes))
    pset = set(prefixes)
    out = []
    i = 0
    while i < len(digit_stream):
        d = digit_stream[i]
        if d in pset and i + 1 < len(digit_stream):
            out.append(table.get((d, digit_stream[i + 1]), "?")); i += 2
        else:
            out.append(table.get((d,), "?")); i += 1
    return "".join(out)

def digits(s: str):
    return [int(c) for c in s if c.isdigit()]

PHASE32_NUMBERS = ("15165943121972409169171213758951813141543131412428154191"
                   "312181219433121171617137149110916631213131281491109166"
                   "131412199114371612126021664313711154112")

def selftest():
    out = decode(digits(PHASE32_NUMBERS), PHASE32_ALPHABET, (1, 4))
    expect = "incaseyoumanagetocrackthistheprivatekeysbelongtohalf"
    ok = out.startswith(expect)
    print(f"[{'PASS' if ok else 'FAIL'}] phase3.2 VIC -> {out[:52]}")
    return ok

if __name__ == "__main__":
    selftest()
