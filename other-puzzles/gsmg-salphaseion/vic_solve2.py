#!/usr/bin/env python3
"""Given key length 15, solve the symbol->index bijection h so that
P_pos = (h(sym) - K_pos) mod 26  [Vigenere]  or  (K_pos - h(sym)) [Beaufort]
is English. Hill-climb h with quadgrams. Tries several length-15 keys."""
import base64, hashlib, math, random, sys
from collections import Counter, defaultdict
from Crypto.Cipher import AES

def evp(pw, salt, kl=32, il=16, md=hashlib.sha256):
    d=b""; p=b""
    while len(d)<kl+il: p=md(p+pw+salt).digest(); d+=p
    return d[:kl], d[kl:kl+il]
blob=open("phase32_aes_blob.txt").read(); raw=base64.b64decode("".join(blob.split())+"===")
pw=hashlib.sha256(b"jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple").hexdigest().encode()
k,iv=evp(pw,raw[8:16]); pt=AES.new(k,AES.MODE_CBC,iv).decrypt(raw[16:]); pt=pt[:-pt[-1]]
vic=pt.decode("latin1").split("\n")[4].replace("\r","")
SYMS=sorted(set(vic),key=ord)
SI={c:i for i,c in enumerate(SYMS)}
CIPH=[SI[c] for c in vic]   # symbol-id per position (0..25, by ordinal)
N=len(CIPH)

# quadgrams
quad=defaultdict(int)
for w in open("/tmp/words_alpha.txt"):
    w=w.strip().lower()
    if len(w)<4: continue
    for i in range(len(w)-3): quad[w[i:i+4]]+=1
tot=sum(quad.values()); QLOG={q:math.log10(c/tot) for q,c in quad.items()}
FLOOR=math.log10(0.01/tot)
def qscore(t):
    s=0.0
    for i in range(len(t)-3): s+=QLOG.get(t[i:i+4],FLOOR)
    return s

def kvals(key): return [ord(c)-97 for c in key.lower()]

def decode(h, K, mode):
    L=len(K); out=[]
    if mode=="vig":
        for pos,sid in enumerate(CIPH): out.append(chr(97+((h[sid]-K[pos%L])%26)))
    else:  # beaufort
        for pos,sid in enumerate(CIPH): out.append(chr(97+((K[pos%L]-h[sid])%26)))
    return "".join(out)

def solve_key(key, mode, restarts=6, iters=6000):
    K=kvals(key); best=None; bestxt=None
    for r in range(restarts):
        h=list(range(26)); random.shuffle(h)
        cur=qscore(decode(h,K,mode))
        for it in range(iters):
            a,b=random.sample(range(26),2)
            h[a],h[b]=h[b],h[a]
            sc=qscore(decode(h,K,mode))
            if sc>=cur: cur=sc
            else: h[a],h[b]=h[b],h[a]
        if best is None or cur>best:
            best=cur; bestxt=decode(h,K,mode)
    return best,bestxt

KEYS=["thematrixhasyou","followwhiterabbit"[:15],"twentythreecipher"[:15],
      "yellowblueprime","seventeencipherx"[:15],"thereisnospoonxy"[:15],
      "wakeupneoxxxxxxx"[:15],"cosmicdualityxx"[:15]]
MODES=["vig","beau"]
if __name__=="__main__":
    results=[]
    for key in KEYS:
        for mode in MODES:
            sc,txt=solve_key(key,mode)
            results.append((sc,key,mode,txt))
            print(f"key={key!r} mode={mode} score={sc:.0f}")
            print("  "+txt[:100])
    results.sort(reverse=True)
    print("\n=== TOP ===")
    sc,key,mode,txt=results[0]
    print(f"key={key} mode={mode} score={sc:.0f}")
    print(txt)
