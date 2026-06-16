#!/usr/bin/env python3
"""
Solve the phase-3.2 "VIC" block (the 1539-char, 26-symbol block inside the
phase-3.2 plaintext) — SOLVED.

Method (Finding 24):
  * decrypt the phase-3.2 blob with the known answer to expose the block;
  * index-of-coincidence period analysis spikes at L=15 (English-like 0.0645);
  * it is a Beaufort cipher, key THEMATRIXHASYOU (15 letters), with the 26
    symbols mapped to the plaintext alphabet by a bijection h. P=(K-h(sym))%26.
  * h is recovered by hill-climbing a quadgram fitness (words_alpha model).

Run: python3 vic_solve.py   (writes nothing; prints the recovered monologue).
The decode is the FULL Architect monologue (confirms the 23/16/7 recipe).
"""
import base64, hashlib, math, random
from collections import defaultdict
from Crypto.Cipher import AES

PH32_ANSWER = b"jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
KEY = "thematrixhasyou"           # 15 letters -> matches the L=15 IoC spike
QUAD_PATH = "/tmp/words_alpha.txt"  # any large English word list works

def evp(pw, salt, kl=32, il=16, md=hashlib.sha256):
    d=b""; p=b""
    while len(d)<kl+il: p=md(p+pw+salt).digest(); d+=p
    return d[:kl], d[kl:kl+il]

def extract_vic_block():
    blob = open("phase32_aes_blob.txt").read()
    raw = base64.b64decode("".join(blob.split())+"===")
    k, iv = evp(hashlib.sha256(PH32_ANSWER).hexdigest().encode(), raw[8:16])
    pt = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:]); pt = pt[:-pt[-1]]
    return pt.decode("latin1").split("\n")[4].replace("\r","")

def ioc(seq):
    from collections import Counter
    n=len(seq); f=Counter(seq)
    return sum(v*(v-1) for v in f.values())/(n*(n-1)) if n>1 else 0

def load_quad():
    q=defaultdict(int)
    for w in open(QUAD_PATH):
        w=w.strip().lower()
        if len(w)>=4:
            for i in range(len(w)-3): q[w[i:i+4]]+=1
    tot=sum(q.values())
    return {k:math.log10(v/tot) for k,v in q.items()}, math.log10(0.01/tot)

def solve():
    vic = extract_vic_block()
    print(f"block len={len(vic)}  flat IoC={ioc(vic):.4f}")
    for L in (5,15,30):
        cols=[vic[i::L] for i in range(L)]
        print(f"  period L={L}: avg col IoC={sum(ioc(c) for c in cols)/L:.4f}")
    SYMS=sorted(set(vic)); SI={c:i for i,c in enumerate(SYMS)}
    CIPH=[SI[c] for c in vic]; K=[ord(c)-97 for c in KEY]
    QLOG,FLOOR=load_quad()
    def dec(h): return "".join(chr(97+((K[i%len(K)]-h[CIPH[i]])%26)) for i in range(len(CIPH)))
    def sc(t): return sum(QLOG.get(t[i:i+4],FLOOR) for i in range(len(t)-3))
    best=None;bt=None
    for _ in range(8):
        h=list(range(26)); random.shuffle(h); cur=sc(dec(h))
        for _ in range(6000):
            a,b=random.sample(range(26),2); h[a],h[b]=h[b],h[a]
            s=sc(dec(h))
            if s>=cur: cur=s
            else: h[a],h[b]=h[b],h[a]
        if best is None or cur>best: best=cur; bt=dec(h)
    print(f"\nbest quadgram score={best:.0f}\n{bt}")

if __name__=="__main__":
    solve()
