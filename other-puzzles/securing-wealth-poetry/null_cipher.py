#!/usr/bin/env python3
"""
Null-cipher attack (the article's first described method: "take the n-th letter
of each word"). Hypothesis: the n-th letter of consecutive words spells the 12
seed words concatenated. We build the n-th-letter string for n=1,2,3 (words too
short to have an n-th letter are skipped, as in the article's example), then
search for any run that segments into 12 BIP39 words forming a valid checksum
that derives to TARGET.

Also tries the simpler "first letter of each word" over the whole article.
"""
import re, sys
from mnemonic import Mnemonic
from check import check_mnemonic
WL = Mnemonic('english').wordlist
WLSET = set(WL)
# index BIP39 words by length for fast segmentation
BYLEN = {}
for w in WL:
    BYLEN.setdefault(len(w), []).append(w)
MINL, MAXL = min(BYLEN), max(BYLEN)

raw = open("assets/article.txt").read()
words_all = re.findall(r"[A-Za-z]+", raw)

def nth_letter_string(words, n):
    return "".join(w[n-1].lower() for w in words if len(w) >= n)

def segment_12(s):
    """Yield every way to split s into exactly 12 BIP39 words (DFS, bounded)."""
    res = []
    def dfs(i, acc):
        if len(acc) == 12:
            if i == len(s):
                res.append(list(acc))
            return
        # prune: remaining must be fillable by (12-len(acc)) words of len MINL..MAXL
        rem = len(s) - i
        need = 12 - len(acc)
        if rem < need*MINL or rem > need*MAXL:
            return
        for L in range(MINL, MAXL+1):
            if i+L > len(s): break
            cand = s[i:i+L]
            if cand in WLSET:
                acc.append(cand); dfs(i+L, acc); acc.pop()
    dfs(0, [])
    return res

def scan(s, tag):
    """Slide a window over s, attempt 12-word segmentation, check address."""
    n = len(s); tested = 0
    # try every starting index; segment_12 enforces exact 12-word consumption
    # to keep it bounded, only attempt windows whose length is plausible (36..96)
    for start in range(n):
        for wlen in range(36, 97):
            if start+wlen > n: break
            seg = segment_12(s[start:start+wlen])
            for words in seg:
                r = check_mnemonic(words)
                if r is not None: tested += 1
                if r:
                    print(f"\n[!!!] MATCH {tag} start={start}:", " ".join(words), r)
                    open("MATCH.txt","w").write(str((tag,start,words,r)))
                    return True, tested
    return False, tested

if __name__ == "__main__":
    total = 0
    for n in (1, 2, 3):
        s = nth_letter_string(words_all, n)
        print(f"[*] n={n} letter-string length {len(s)}")
        hit, t = scan(s, f"nth={n}")
        total += t
        if hit: break
    else:
        print(f"\n[done] no match. checksum-valid tested={total}")
