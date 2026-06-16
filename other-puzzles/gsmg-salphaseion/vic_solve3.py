#!/usr/bin/env python3
"""General period-15 Vigenere solve: hill-climb shared alphabet h (symbol->index)
AND the 15 key shifts jointly, scored by quadgrams. No key assumption."""
import base64, hashlib, math, random
from collections import defaultdict
from Crypto.Cipher import AES

def evp(pw, salt, kl=32, il=16, md=hashlib.sha256):
    d=b""; p=b""
    while len(d)<kl+il: p=md(p+pw+salt).digest(); d+=p
    return d[:kl], d[kl:kl+il]
blob=open("phase32_aes_blob.txt").read(); raw=base64.b64decode("".join(blob.split())+"===")
pw=hashlib.sha256(b"jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple").hexdigest().encode()
k,iv=evp(pw,raw[8:16]); pt=AES.new(k,AES.MODE_CBC,iv).decrypt(raw[16:]); pt=pt[:-pt[-1]]
vic=pt.decode("latin1").split("\n")[4].replace("\r","")
SYMS=sorted(set(vic),key=ord); SI={c:i for i,c in enumerate(SYMS)}
CIPH=[SI[c] for c in vic]; N=len(CIPH); L=15

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
def decode(h,K):
    return "".join(chr(97+((h[CIPH[p]]-K[p%L])%26)) for p in range(N))

def solve(restarts=10, iters=8000):
    best=None;bt=None;bk=None
    for r in range(restarts):
        h=list(range(26)); random.shuffle(h)
        K=[random.randrange(26) for _ in range(L)]
        cur=qscore(decode(h,K))
        for it in range(iters):
            if random.random()<0.5:
                a,b=random.sample(range(26),2); h[a],h[b]=h[b],h[a]
                sc=qscore(decode(h,K))
                if sc>=cur: cur=sc
                else: h[a],h[b]=h[b],h[a]
            else:
                i=random.randrange(L); old=K[i]; K[i]=random.randrange(26)
                sc=qscore(decode(h,K))
                if sc>=cur: cur=sc
                else: K[i]=old
        if best is None or cur>best:
            best=cur;bt=decode(h,K);bk=K[:]
            print(f"restart {r}: {cur:.0f}  key={''.join(chr(97+x) for x in K)}")
            print("  "+bt[:100])
    return best,bt,bk
if __name__=="__main__":
    sc,txt,K=solve()
    print("\n=== BEST ===",sc,"key=",''.join(chr(97+x) for x in K))
    print(txt)
    open("vic_decoded3.txt","w").write(txt)
