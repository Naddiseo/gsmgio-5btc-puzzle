#!/usr/bin/env python3
"""
Fully general GPS-method search: slide the 'position-1' anchor across EVERY
word offset in the article, eliminating start-point/preamble guesswork.

For each base offset b and each tokenization, the GPS rule selects one word per
decade: word index = b + 10*k + d (k=0..11, d=0..9). We require every decade
window to contain >=1 BIP39 word, then run the cartesian product through the
BIP39 checksum + address derivation. This covers all landmark coordinates AND
all counting start points at once.
"""
import re, itertools
from mnemonic import Mnemonic
from check import check_mnemonic
WL = set(Mnemonic('english').wordlist)
raw = open("assets/article.txt").read()
text = " ".join(l for l in raw.split("\n"))

TOKS = {
 "alpha":  [w.lower() for w in re.findall(r"[A-Za-z]+", text)],
 "alpha'": [w.lower().strip("'") for w in re.findall(r"[A-Za-z']+", text)],
 "alnum":  [w.lower() for w in re.findall(r"[A-Za-z0-9]+", text)],
}

def search(words, tname):
    N=len(words); tested=0
    for b in range(0, N-119):
        decs=[]
        ok=True
        for k in range(12):
            opts=[words[b+10*k+d] for d in range(10) if words[b+10*k+d] in WL]
            if not opts: ok=False; break
            decs.append(opts)
        if not ok: continue
        combos=1
        for d in decs: combos*=len(d)
        if combos>5_000_000:
            continue
        for combo in itertools.product(*decs):
            r=check_mnemonic(list(combo))
            if r is not None: tested+=1
            if r:
                print(f"\n[!!!] MATCH base={b} {tname}:", " ".join(combo), r)
                open("MATCH.txt","w").write(str((b,tname,combo,r)))
                return True,tested
    return False,tested

if __name__=="__main__":
    total=0
    for tname,words in TOKS.items():
        print(f"[*] sliding anchor over {tname}: {len(words)} words, "
              f"{max(0,len(words)-119)} offsets")
        hit,t=search(words,tname); total+=t
        if hit: break
    else:
        print(f"\n[done] no match. checksum-valid extractions tested={total}")
