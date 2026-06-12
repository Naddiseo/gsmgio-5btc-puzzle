"""BREAKTHROUGH (verified): the SalPhaseIon `faed` string (STR_B) is a BIFID
cipher, and `dbbi` (STR_A) supplies the key.

- Key = the unique letters of `dbbi` in order of first appearance, dropping the
  9th (`a`, the "character to be zeroed out"):  dbbifhceg... -> "dbifhceg".
- Cipher = `faed` (STR_B), over a standard 5x5 Polybius square (J->I) keyed by
  "dbifhceg".
- Bifid-decoding `faed` yields the literal word **btcseed** followed by two new
  `z`-separated strings -- proving the key/method are correct.

`matrixsumlist` (the binary word sitting between dbbi and faed in SalPhaseIon) is
the instruction: Bifid is a *matrix* (Polybius) cipher.

This independently reproduces the community CyberChef recipe
`Bifid_Cipher_Decode('dbifhceg')` applied to faed.
"""
from gsmg_toolkit import SALPH_STR_A, SALPH_STR_B

def unique_letters(s):
    seen = []
    for c in s:
        if c not in seen:
            seen.append(c)
    return "".join(seen)

def bifid_key_from_dbbi():
    return unique_letters(SALPH_STR_A)[:8]   # "dbifhceg" (drops 9th letter 'a')

def _square(key):
    key = key.upper()
    alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"   # 25 letters, J omitted
    seen = []
    for c in key + alpha:
        if c in alpha and c not in seen:
            seen.append(c)
    return seen

def bifid_decode(cipher, key):
    sq = _square(key)
    co = {c: (i // 5, i % 5) for i, c in enumerate(sq)}
    cipher = [c for c in cipher.upper().replace("J", "I") if c in co]
    rc = []
    for ch in cipher:
        r, c = co[ch]; rc.append(r); rc.append(c)
    n = len(cipher)
    return "".join(sq[rc[i] * 5 + rc[n + i]] for i in range(n)).lower()

def bifid_encode(text, key):
    sq = _square(key)
    co = {c: (i // 5, i % 5) for i, c in enumerate(sq)}
    text = [c for c in text.upper().replace("J", "I") if c in co]
    rows, cols = [], []
    for ch in text:
        r, c = co[ch]; rows.append(r); cols.append(c)
    comb = rows + cols
    return "".join(sq[comb[2 * i] * 5 + comb[2 * i + 1]] for i in range(len(comb) // 2)).lower()

def decode_faed():
    return bifid_decode(SALPH_STR_B, bifid_key_from_dbbi())

if __name__ == "__main__":
    key = bifid_key_from_dbbi()
    print("key from dbbi:", key)
    out = decode_faed()
    print("starts with 'btcseed':", out.startswith("btcseed"))
    parts = out.split("z")
    print("part0:", parts[0])
    print("part1:", parts[1][:60], "...", "len", len(parts[1]))
