#!/usr/bin/env python3
"""Solve the phase-3.2 period-15 polyalphabetic block (Vigenere with scrambled
alphabet). Builds a quadgram model from words_alpha, hill-climbs the symbol->index
permutation g; per column the best Caesar shift K_j is found by chi-square."""
import base64, hashlib, math, random
from collections import Counter, defaultdict
from Crypto.Cipher import AES

def evp(pw, salt, kl=32, il=16, md=hashlib.sha256):
    d=b""; p=b""
    while len(d)<kl+il: p=md(p+pw+salt).digest(); d+=p
    return d[:kl], d[kl:kl+il]

blob = open("phase32_aes_blob.txt").read()
raw = base64.b64decode("".join(blob.split())+"===")
salt, ct = raw[8:16], raw[16:]
pw = hashlib.sha256(b"jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple").hexdigest().encode()
k, iv = evp(pw, salt)
pt = AES.new(k, AES.MODE_CBC, iv).decrypt(ct); pt = pt[:-pt[-1]]
vic = pt.decode("latin1").split("\n")[4].replace("\r","")

SYMS = sorted(set(vic), key=ord)
assert len(SYMS)==26
sidx = {c:i for i,c in enumerate(vic)}  # unused
NUMS = [SYMS.index(c) for c in vic]  # ordinal index 0-25 per ciphertext position
L = 15

# ---- quadgram model from words_alpha ----
print("building quadgram model...")
quad = defaultdict(int)
with open("/tmp/words_alpha.txt") as f:
    for w in f:
        w=w.strip().lower()
        if len(w)<4: continue
        for i in range(len(w)-3):
            quad[w[i:i+4]] += 1
total = sum(quad.values())
QLOG = {q: math.log10(c/total) for q,c in quad.items()}
FLOOR = math.log10(0.01/total)
print(f"  {len(quad)} quadgrams")

ENG = {'a':8.2,'b':1.5,'c':2.8,'d':4.3,'e':12.7,'f':2.2,'g':2.0,'h':6.1,'i':7.0,
 'j':0.15,'k':0.77,'l':4.0,'m':2.4,'n':6.7,'o':7.5,'p':1.9,'q':0.095,'r':6.0,
 's':6.3,'t':9.1,'u':2.8,'v':0.98,'w':2.4,'x':0.15,'y':2.0,'z':0.074}
eng=[ENG[chr(97+i)] for i in range(26)]; s=sum(eng); eng=[e/s for e in eng]

# columns of ordinal-index values
COLS = [[NUMS[i] for i in range(c,len(NUMS),L)] for c in range(L)]
COLCNT = [Counter(c) for c in COLS]

def best_shifts(g):
    # g: list mapping ordinal-index -> plaintext-index (a permutation)
    # for each column choose Caesar shift minimizing chi-square
    shifts=[]
    for cnt in COLCNT:
        N=sum(cnt.values())
        # distribution over plaintext-index after applying g
        gd=Counter()
        for oi,c in cnt.items(): gd[g[oi]] += c
        best=0; bestchi=1e18
        for sh in range(26):
            chi=0.0
            for i in range(26):
                obs=gd.get((i+sh)%26,0); exp=eng[i]*N
                chi+=(obs-exp)**2/exp
            if chi<bestchi: bestchi=chi; best=sh
        shifts.append(best)
    return shifts

def decode(g, shifts):
    out=[]
    for pos,oi in enumerate(NUMS):
        p=(g[oi]-shifts[pos%L])%26
        out.append(chr(97+p))
    return "".join(out)

def qscore(text):
    s=0.0
    for i in range(len(text)-3):
        s+=QLOG.get(text[i:i+4],FLOOR)
    return s

def solve():
    best_overall=None; best_g=None; best_sh=None
    for restart in range(8):
        g=list(range(26)); random.shuffle(g)
        sh=best_shifts(g)
        cur=qscore(decode(g,sh))
        T=0
        for it in range(4000):
            a,b=random.sample(range(26),2)
            g[a],g[b]=g[b],g[a]
            sh2=best_shifts(g)
            sc=qscore(decode(g,sh2))
            if sc>cur:
                cur=sc; sh=sh2
            else:
                g[a],g[b]=g[b],g[a]
        if best_overall is None or cur>best_overall:
            best_overall=cur; best_g=g[:]; best_sh=sh
            print(f"restart {restart}: score={cur:.0f}")
            print("  "+decode(g,sh)[:120])
    return best_g,best_sh,best_overall

if __name__=="__main__":
    g,sh,sc=solve()
    txt=decode(g,sh)
    print("\n=== BEST ===")
    print("score:",sc)
    print("shifts:",sh, "->", "".join(chr(97+x) for x in sh))
    print(txt)
    open("vic_decoded.txt","w").write(txt)
