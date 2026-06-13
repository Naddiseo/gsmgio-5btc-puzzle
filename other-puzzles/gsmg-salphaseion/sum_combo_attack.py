#!/usr/bin/env python3
"""
Comprehensive combination attack built around the VERIFIED Sum token
(DIFNLREV9E6VARXVF5UF8PE). Combines it with every decoded roadmap artifact,
under the puzzle's sha256 conventions, against all three blobs, with EVP and
PBKDF2 KDFs (AES-128/192/256) and a WIF/nested/ASCII-aware plaintext filter.
"""
import base64, hashlib, itertools, os
from Crypto.Cipher import AES

HERE=os.path.dirname(os.path.abspath(__file__))
AES1="U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2="QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P1="U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P2="gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"
def bf(s): return s+"="*(-len(s)%4)
COSMIC="".join(open(os.path.join(HERE,"cosmic_duality_blob.txt")).read().split())
BLOBS={"salph":base64.b64decode(bf(AES1+AES2)),"p32":base64.b64decode(bf(P1+P2)),"cosmic":base64.b64decode(bf(COSMIC))}

def okpt(pt):
    pad=pt[-1]
    if not(1<=pad<=16 and pt[-pad:]==bytes([pad])*pad):return None
    b=pt[:-pad]
    if not b:return None
    if b[:8]==b"Salted__":return("NESTED",b)
    if b[:1] in (b"5",b"K",b"L") and 50<=len(b)<=53 and all(48<=x<=122 for x in b):return("WIF?",b)
    pr=sum(1 for x in b if 32<=x<127 or x in(9,10,13))/len(b)
    if pr>=0.97:return("ASCII",b)
    return None
def evp(pw,salt,kl,il,md):
    d=b"";p=b""
    while len(d)<kl+il:p=md(p+pw+salt).digest();d+=p
    return d[:kl],d[kl:kl+il]
def alldec(raw,pwb):
    salt,ct=raw[8:16],raw[16:];h=[]
    for kl in(32,24,16):
        for md in(hashlib.md5,hashlib.sha256):
            k,iv=evp(pwb,salt,kl,16,md)
            r=okpt(AES.new(k,AES.MODE_CBC,iv).decrypt(ct))
            if r:h.append(("EVP"+md().name,kl,r))
        for dg in("sha256","sha1"):
            for it in(1,10000,50000):
                dk=hashlib.pbkdf2_hmac(dg,pwb,salt,it,dklen=kl+16)
                r=okpt(AES.new(dk[:kl],AES.MODE_CBC,dk[kl:kl+16]).decrypt(ct))
                if r:h.append((f"PB{dg}{it}",kl,r))
    return h
def test(s,label):
    pwb=s.encode() if isinstance(s,str) else s
    for fb in (pwb,hashlib.sha256(pwb).hexdigest().encode(),hashlib.sha256(pwb).digest(),hashlib.sha256(pwb).hexdigest().upper().encode()):
        for bn,raw in BLOBS.items():
            for kdf,kl,r in alldec(raw,fb):
                print(f"\n[!!! HIT] {label!r} blob={bn} {kdf} AES{kl*8} {r[0]}: {r[1][:160]!r}")
                open(os.path.join(HERE,"MATCH.txt"),"a").write(f"{label!r} {bn} {kdf} {r}\n")
                return True
    return False

SUM="DIFNLREV9E6VARXVF5UF8PE"
H=lambda x:hashlib.sha256((x.encode() if isinstance(x,str) else x)).hexdigest()
arts=[SUM,SUM.lower(),"5","followthewhiterabbit","theseedisplanted","matrixsumlist",
 "lastwordsbeforearchichoice","thispassword","toyourthesalvationzionyourmatrix",
 "salvation","yinyang","yingyang","cosmicduality","anstoo","enter","ciaobellao",
 "bmvjwdszzaoyqpgjaxlzxincipkeut","gdwaokhusrttemmttue",
 "GSMGIO5BTCPUZZLECHALLENGE"]

def gen():
    seen=set()
    def emit(p):
        if p and p not in seen: seen.add(p); return True
        return False
    # singles
    for a in arts:
        if emit(a): yield a
    # ordered pairs (concat + sha-of-pair + sha+sha)
    for a,b in itertools.permutations(arts,2):
        for c in (a+b, H(a)+H(b), H(a+b)):
            if emit(c): yield c
    # triples with SUM anchored, others around
    for b,c in itertools.permutations([x for x in arts if x!=SUM],2):
        for combo in (SUM+b+c, b+SUM+c, H(SUM)+H(b)+H(c)):
            if emit(combo): yield combo

def main():
    print("blobs ready; combination attack starting")
    t=0
    for pw in gen():
        t+=1
        if test(pw,pw[:30] if isinstance(pw,str) else "bin"):
            print(f"SOLVED at #{t}"); return
        if t%2000==0: print(f"... {t} tested", flush=True)
    print(f"[done] {t} tested, no hit.")

if __name__=="__main__": main()
