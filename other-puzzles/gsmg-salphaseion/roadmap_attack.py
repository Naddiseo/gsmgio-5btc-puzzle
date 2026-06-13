#!/usr/bin/env python3
"""
Roadmap-driven AES password attack.

Drives candidates from the decoded 2023-02-23 official hint, which lays out the
intended pipeline:
    yellow blue primes -> matrix sumlist -> last words before archichoice
    -> yinyang -> "the password ... is in front of your eyes"

Targets both 96-byte blobs (salph embedded + phase3.2) with EVP_BytesToKey
(md5/sha256, AES-128/256) and raw / sha256(hex,bin,upper) password forms.
"""
import base64, hashlib, sys
from Crypto.Cipher import AES

AES1 = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2 = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P1   = "U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P2   = "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"

def bf(s): return s + "=" * (-len(s) % 4)
BLOBS = {"salph": base64.b64decode(bf(AES1+AES2)), "p32": base64.b64decode(bf(P1+P2))}

def evp(pw, salt, kl, il, md):
    d=b""; p=b""
    while len(d)<kl+il: p=md(p+pw+salt).digest(); d+=p
    return d[:kl], d[kl:kl+il]

def tryd(raw, pwb):
    salt, ct = raw[8:16], raw[16:]; out=[]
    for kl in (32,16):
        for md in (hashlib.md5, hashlib.sha256):
            k,iv=evp(pwb,salt,kl,16,md)
            pt=AES.new(k,AES.MODE_CBC,iv).decrypt(ct); pad=pt[-1]
            if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad and all(32<=b<127 or b in (9,10,13) for b in pt[:-pad]):
                out.append((f"EVP-{md().name}-{kl*8}", pt[:-pad].decode()))
    return out

def test(pw, label):
    pwb = pw.encode() if isinstance(pw,str) else pw
    forms=[(pwb,"raw"),
           (hashlib.sha256(pwb).hexdigest().encode(),"shahex"),
           (hashlib.sha256(pwb).digest(),"shabin"),
           (hashlib.sha256(pwb).hexdigest().upper().encode(),"shaHEX"),
           (hashlib.md5(pwb).hexdigest().encode(),"md5hex")]
    for fb,fn in forms:
        for bn,raw in BLOBS.items():
            for kdf,pt in tryd(raw,fb):
                print(f"\n[!!! HIT] {label!r} form={fn} blob={bn} {kdf}\n  PT={pt!r}")
                open("MATCH.txt","a").write(f"{label!r} {fn} {bn} {kdf}\n{pt!r}\n\n")
                return True
    return False

# ---- roadmap material ----
URL = "gsmg.io/theseedisplanted"          # phase0 output
URLNOSLASH = "gsmgiotheseedisplanted"
SEED = "theseedisplanted"
def primes_upto(n): return [p for p in range(2,n+1) if all(p%i for i in range(2,int(p**.5)+1))]

# blue/yellow ordinals (1..24) among colored cells, computed authoritatively
BLUE_ORD   = [1,2,3,4,6,7,8,11,12,13,14,16,17,20,23]
YELLOW_ORD = [5,9,10,15,18,19,21,22,24]
PRIMES24   = primes_upto(24)
BLUE_PRIMES   = [p for p in PRIMES24 if p in BLUE_ORD]   # 2,3,7,11,13,17,23
YELLOW_PRIMES = [p for p in PRIMES24 if p in YELLOW_ORD] # 5,19

def pick(s, idxs, off=1):
    return "".join(s[i-off] for i in idxs if 0 <= i-off < len(s))

# 2023-02-23 decoded roadmap sentence
ROADMAP = ("yellow blue primes matrix sumlist last words before archichoice yinyang "
           "we wont give away thepassword its in front of your eyes but youre "
           "not seeing it very last step is a true give away promised")
LAST_WORDS = ("the door to your right leads to the source and the salvation of zion "
              "the door to your left leads back to the matrix to her and to the end "
              "of your species the function of the one is now to return to the source")

MATRIX_RS = [6,10,8,7,6,6,5,4,9,9,7,8,7,9]
MATRIX_CS = [8,10,8,10,8,7,3,6,7,5,9,6,6,8]

def candidates():
    seen=set()
    def emit(pw,label):
        key=(pw.encode() if isinstance(pw,str) else pw)
        if key not in seen:
            seen.add(key); yield pw,label
    # yellow/blue prime char extraction over the URL / seed strings
    for nm,s in [("url",URL),("urlnoslash",URLNOSLASH),("seed",SEED)]:
        for off in (0,1):
            yield from emit(pick(s,BLUE_PRIMES,off), f"blueP/{nm}/off{off}")
            yield from emit(pick(s,YELLOW_PRIMES,off), f"yelP/{nm}/off{off}")
            yield from emit(pick(s,sorted(BLUE_PRIMES+YELLOW_PRIMES),off), f"ybP/{nm}/off{off}")
            yield from emit(pick(s,BLUE_ORD,off), f"blue/{nm}/off{off}")
            yield from emit(pick(s,YELLOW_ORD,off), f"yel/{nm}/off{off}")
    # matrixsumlist forms
    for nm,lst in [("rs",MATRIX_RS),("cs",MATRIX_CS),("rscs",MATRIX_RS+MATRIX_CS),("csrs",MATRIX_CS+MATRIX_RS)]:
        for sep in ("",",", " ","-"):
            yield from emit(sep.join(map(str,lst)), f"msl/{nm}/{sep!r}")
        yield from emit(bytes(lst), f"msl_bytes/{nm}")
    # roadmap + last-words n-grams (raw + nospace + sha)
    for txt in (ROADMAP, LAST_WORDS):
        w=txt.split()
        for i in range(len(w)):
            for n in range(1,12):
                if i+n>len(w): break
                ph=" ".join(w[i:i+n])
                yield from emit(ph, f"ng/{ph[:18]}")
                yield from emit(ph.replace(" ",""), f"ngNS/{ph[:18]}")
    # standalone keyword roundup
    for kw in ["yinyang","yingyang","cosmicduality","thepassword","salvation",
               "salvationofzion","thesalvationofzion","yellowblueprimes",
               "matrixsumlist","lastwordsbeforearchichoice","returntothesource",
               URL, URLNOSLASH, SEED]:
        yield from emit(kw, f"kw/{kw[:18]}")

def main():
    print("blobs:", {n:(r[:8]==b'Salted__', len(r)) for n,r in BLOBS.items()})
    t=0
    for pw,label in candidates():
        t+=1
        if test(pw,label):
            print(f"SOLVED at #{t}"); return
        if t%2000==0: print(f"... {t} tested", flush=True)
    print(f"[done] {t} candidates, no hit.")

if __name__=="__main__":
    main()
