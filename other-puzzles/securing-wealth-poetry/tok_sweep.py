#!/usr/bin/env python3
"""
Tokenization sweep for the GPS method. The GPS decade-window search covers ALL
landmark coordinates at once (one word per digit-window k: position in
[10k,10k+9]). The only free variable left is how the article is tokenized into
words. We sweep many conventions; for each we (1) check the necessary condition
that every decade window 0..11 holds >=1 BIP39 word, and if so (2) run the
decade cartesian product through the BIP39 checksum + address derivation.
"""
import re, itertools
from mnemonic import Mnemonic
from check import check_mnemonic
WL = set(Mnemonic('english').wordlist)
raw = open("assets/article.txt").read()
lines = raw.split("\n")

SECTION_HEADERS = {"revolution","fiat","bitcoin","touchpoints","steganography",
    "trithemian seeds","coinmonks","follow","published in"}

def body_from(marker):
    for i,l in enumerate(lines):
        if l.strip().startswith(marker):
            return lines[i:]
    return lines

def make_text(start, drop_headers, drop_short):
    ls = body_from(start)
    out = []
    for l in ls:
        s = l.strip()
        if not s: continue
        if drop_headers and s.lower() in SECTION_HEADERS: continue
        if drop_short and len(s) < 25 and s.lower() not in ("",): continue
        out.append(l)
    return " ".join(out)

TOKS = {
 "alpha'":   lambda t: [w.lower().strip("'") for w in re.findall(r"[A-Za-z']+", t)],
 "alpha":    lambda t: [w.lower() for w in re.findall(r"[A-Za-z]+", t)],
 "alnum":    lambda t: [w.lower() for w in re.findall(r"[A-Za-z0-9]+", t)],
 "ws":       lambda t: [w.strip(".,;:!?()\"'—-’“”").lower() for w in t.split()
                        if w.strip(".,;:!?()\"'—-’“”")],
 "hyph2":    lambda t: [p.lower() for w in re.findall(r"[A-Za-z\-']+", t)
                        for p in re.split(r"[-']", w) if p],  # split hyphens/apostrophes
}
STARTS = ["My grandfather","Securing Wealth","What if","Revolution",
          "A formal authorization","Bitcoin too","While bitcoin"]

def decade_options(words):
    decs=[]
    for k in range(12):
        opts=[(10*k+d, words[10*k+d]) for d in range(10)
              if 10*k+d < len(words) and words[10*k+d] in WL]
        decs.append(opts)
    return decs

def run():
    tested=0; viable=0
    for start in STARTS:
        for dh in (False,True):
            for ds in (False,True):
                txt = make_text(start, dh, ds)
                for tname, tok in TOKS.items():
                    w = tok(txt)
                    decs = decade_options(w)
                    if any(len(d)==0 for d in decs):
                        continue   # GPS impossible with this tokenization
                    viable+=1
                    combos=1
                    for d in decs: combos*=len(d)
                    tag=f"start='{start[:14]}' hdr={int(dh)} short={int(ds)} {tname}"
                    if combos>3_000_000:
                        print(f"[skip] {tag}: {combos:,} combos"); continue
                    print(f"[viable] {tag}: {combos:,} combos -> searching")
                    for combo in itertools.product(*decs):
                        words=[c[1] for c in combo]
                        r=check_mnemonic(words)
                        if r is not None: tested+=1
                        if r:
                            print("\n[!!!] MATCH:", " ".join(words), r, "|", tag,
                                  "| positions", [c[0]+1 for c in combo])
                            open("MATCH.txt","w").write(str((words,r,tag)))
                            return
    print(f"\n[done] viable tokenizations={viable}, checksum-valid tested={tested}, no match")

if __name__=="__main__":
    run()
