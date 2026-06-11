#!/usr/bin/env python3
"""Zden Level 5 solver. Extract 64 rectangles, brute-force interpretation of
'sum of two consecutive rectangle areas = one byte' against the target address."""
import cv2, numpy as np, hashlib, itertools
import coincurve, base58

TARGET = "1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7"
IMG = 'assets/puzzle.png'

def detect():
    im = cv2.imread(IMG, cv2.IMREAD_GRAYSCALE)
    _, th = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
    cnts,hier = cv2.findContours(th, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hier=hier[0]; frames=[]
    for i,c in enumerate(cnts):
        if hier[i][3]==-1:
            x,y,W,H=cv2.boundingRect(c)
            inner=None; ch=hier[i][2]; best=0
            while ch!=-1:
                cx,cy,cw,chh=cv2.boundingRect(cnts[ch])
                if cw*chh>best: best=cw*chh; inner=(cw,chh)
                ch=hier[ch][0]
            frames.append([x,y,W,H,inner])
    pf=[f for f in frames if 120<=f[0]<=770 and f[2]>=8 and f[3]>=4]
    assert len(pf)==64, len(pf)
    return pf

def rows_of(pf):
    pf=sorted(pf,key=lambda f:f[1]+f[3]/2); rows=[]; cur=[pf[0]]
    for f in pf[1:]:
        if (f[1]+f[3]/2)-(cur[-1][1]+cur[-1][3]/2)>40: rows.append(cur); cur=[f]
        else: cur.append(f)
    rows.append(cur)
    for r in rows: r.sort(key=lambda f:f[0])
    assert len(rows)==8 and all(len(r)==8 for r in rows), [len(r) for r in rows]
    return rows

def orderings(rows):
    rm=[f for r in rows for f in r]                                   # row-major
    bs=[f for i,r in enumerate(rows) for f in (r if i%2==0 else r[::-1])]  # boustrophedon
    cols=[[rows[r][c] for r in range(8)] for c in range(8)]
    cm=[f for c in cols for f in c]                                   # column-major
    return {"row":rm,"boustro":bs,"col":cm,"row_rev":rm[::-1]}

def area_of(f, kind):
    x,y,W,H,inner=f; iw,ih=inner if inner else (W,H); t=(W-iw)//2 if inner else 0
    return {"outer":W*H,"inner":iw*ih,"mid":(W-t)*(H-t),
            "outer4":(W*H)//4,"WplusH":W+H,"perim":2*(W+H)}[kind]

def addr(priv,comp):
    pub=coincurve.PublicKey.from_valid_secret(priv).format(comp)
    h=hashlib.new('ripemd160',hashlib.sha256(pub).digest()).digest(); d=b'\x00'+h
    return base58.b58encode(d+hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]).decode()

def check(byts,tag):
    if len(byts)!=32: return False
    priv=bytes(int(b)%256 for b in byts)
    if priv==b'\x00'*32: return False
    for comp in (True,False):
        try:
            if addr(priv,comp)==TARGET:
                print(f"\n[!!!] MATCH {tag} {'comp' if comp else 'uncomp'}\nPRIV {priv.hex()}")
                open('MATCH.txt','w').write(tag+" "+priv.hex()); return True
        except Exception: return False
    return False

OPS={
 "sum%256":      lambda a,b:(a+b)%256,
 "sum//2%256":   lambda a,b:((a+b)//2)%256,
 "diff%256":     lambda a,b:abs(a-b)%256,
 "xor%256":      lambda a,b:(a^b)%256,
 "amod+bmod":    lambda a,b:((a%256)+(b%256))%256,
 "concat16":     lambda a,b:((a%16)*16+(b%16)),
 "sum%256_2":    lambda a,b:(a+b)%256,
}
PAIRINGS={
 "adjacent": lambda s:[(s[k],s[k+1]) for k in range(0,64,2)],
 "half":     lambda s:[(s[k],s[k+32]) for k in range(32)],
 "interleave":lambda s:[(s[2*k],s[2*k+1]) for k in range(32)],
}

def run():
    pf=detect(); rows=rows_of(pf); ords=orderings(rows)
    for oname,seq in ords.items():
        for kind in ["outer","inner","mid","outer4","WplusH","perim"]:
            A=[area_of(f,kind) for f in seq]
            for pname,pf_ in PAIRINGS.items():
                pairs=pf_(A)
                if len(pairs)!=32: continue
                for opname,op in OPS.items():
                    byts=[op(a,b) for a,b in pairs]
                    if check(byts,f"{oname}|{kind}|{pname}|{opname}"):
                        return True
    print("[done] no match across orderings x area-types x pairings x ops")
    return False

if __name__=="__main__":
    run()
