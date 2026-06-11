#!/usr/bin/env python3
"""
Broad automated search for the Securing-Wealth-in-Poetry 0.03 BTC seed.

Tries, across several tokenizations and start points:
  (A) the two index lists the article itself prints (story & GPS examples)
  (B) GPS method: one BIP39 word per decade-window k (pos in [10k,10k+9]),
      cartesian product -> checksum -> address (covers ALL GPS coordinates)
  (C) article numbers/dates treated as 'phone' position lists
For every valid BIP39 mnemonic found, derive and compare to TARGET.
"""
import re, itertools, sys
from mnemonic import Mnemonic
from check import check_mnemonic, TARGET
WL = set(Mnemonic('english').wordlist)
raw = open("assets/article.txt").read()
lines = raw.split("\n")

def body_from(marker):
    for i,l in enumerate(lines):
        if l.strip().startswith(marker):
            return " ".join(lines[i:])
    return " ".join(lines)

TOKENIZERS = {
 "alpha":      lambda t: [w.lower().strip("'") for w in re.findall(r"[A-Za-z']+", t)],
 "alpha_pure": lambda t: [w.lower() for w in re.findall(r"[A-Za-z]+", t)],
 "alnum":      lambda t: [w.lower() for w in re.findall(r"[A-Za-z0-9]+", t)],
 "ws":         lambda t: [w.strip(".,;:!?()\"'—-’“”").lower() for w in t.split() if w.strip(".,;:!?()\"'—-’“”")],
}
STARTS = ["My grandfather", "Securing Wealth", "Revolution", "What if"]

IDX_LISTS = {
 "story_example": [2,6,9,18,22,25,45,70,86,100,113,116],
 "gps_example":   [3,18,28,39,40,56,67,77,80,90,104,114],
}

found = []
def try_words(words, tag):
    if len(words)!=12: return
    if any(w not in WL for w in words): return
    r = check_mnemonic(words)
    if r:
        print(f"\n[!!!] MATCH ({tag}):", " ".join(words), r); found.append((tag,words,r))
    return r

def run():
    n_valid_checksum = 0
    for start in STARTS:
        body = body_from(start)
        for tname, tok in TOKENIZERS.items():
            w = tok(body)
            # (A) explicit index lists, base 1 and base 0
            for lname, idx in IDX_LISTS.items():
                for base in (1,0):
                    pick = [w[i-base] for i in idx if 0<=i-base<len(w)]
                    if len(pick)==12 and all(p in WL for p in pick):
                        r=check_mnemonic(pick)
                        if r is not None: n_valid_checksum+=1
                        try_words(pick, f"{start}|{tname}|{lname}|b{base}")
            # (B) GPS decade-window cartesian product
            decades=[]
            ok=True
            for k in range(12):
                opts=[w[10*k+d] for d in range(10) if 10*k+d<len(w) and w[10*k+d] in WL]
                if not opts: ok=False; break
                decades.append(opts)
            if ok:
                combos=1
                for dlist in decades: combos*=len(dlist)
                if combos<=2_000_000:
                    for combo in itertools.product(*decades):
                        r=check_mnemonic(list(combo))
                        if r is not None: n_valid_checksum+=1
                        if r: try_words(list(combo), f"{start}|{tname}|GPS")
                else:
                    print(f"[skip GPS] {start}|{tname}: {combos:,} combos too many")
    print(f"\n[done] valid-checksum mnemonics tested={n_valid_checksum}, matches={len(found)}")

if __name__=="__main__":
    run()
