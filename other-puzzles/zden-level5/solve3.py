#!/usr/bin/env python3
"""Zden LVL5 comprehensive search, verified against the target ADDRESS.
Incorporates the hint-matrix coefficients (col=[1,1,1,2,2,1,1,1], row=[0,9,1,1,1,8,1,9])
and line adjustments for rectangles #40 and #53."""
import hashlib, itertools
import coincurve, base58

TARGET="1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7"
rows=[]
with open('research/Analysis/Results/noLine_A.csv') as f:
    for line in f:
        rows.append(tuple(int(v) for v in line.split(',')))
OUT=[r[0] for r in rows]; INN=[r[1] for r in rows]; SHELL=[r[2] for r in rows]
COLC=[1,1,1,2,2,1,1,1]
ROWC=[0,9,1,1,1,8,1,9]

def addr(priv,comp):
    pub=coincurve.PublicKey.from_valid_secret(priv).format(comp)
    h=hashlib.new('ripemd160',hashlib.sha256(pub).digest()).digest(); d=b'\x00'+h
    return base58.b58encode(d+hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]).decode()

def verify(byts,tag):
    priv=bytes(int(b)%256 for b in byts)
    if priv==b'\x00'*32: return False
    for comp in (True,False):
        try:
            if addr(priv,comp)==TARGET:
                print(f"\n[!!!] MATCH {tag} {'comp' if comp else 'uncomp'}\nPRIV {priv.hex()}")
                open('MATCH.txt','w').write(tag+" "+priv.hex()); return True
        except Exception: return False
    return False

def colof(i): return i%8
def rowof(i): return i//8

# area variants with optional coefficient preprocessing
def make_area(base, coef):
    A=list(base)
    if coef=="col":  A=[A[i]*COLC[colof(i)] for i in range(64)]
    if coef=="row":  A=[A[i]*ROWC[rowof(i)] for i in range(64)]
    if coef=="both": A=[A[i]*COLC[colof(i)]*ROWC[rowof(i)] for i in range(64)]
    if coef=="coldiv": A=[A[i]//COLC[colof(i)] for i in range(64)]
    return A

PAIRS={
 "adj":  [(2*k,2*k+1) for k in range(32)],
 "half": [(k,k+32) for k in range(32)],
 "slide":[(k,k+1) for k in range(32)],
 "colpair": None,
}
TRANS={
 "sum%256":          lambda a,b:(a+b)%256,
 "(-(a+b)+64)%256":  lambda a,b:(-(a+b)+64)%256,
 "(a+b)//2%256":     lambda a,b:((a+b)//2)%256,
 "(a+b)//4%256":     lambda a,b:((a+b)//4)%256,
 "(a%256+b%256)%256":lambda a,b:((a%256)+(b%256))%256,
 "(a+b)%255":        lambda a,b:(a+b)%255,
 "(a+b)mod256_x-1+64":lambda a,b:(-1*((a+b)%256)+64)%256,
 "abs(a-b)%256":     lambda a,b:abs(a-b)%256,
}

def run():
    n=0
    for base_name,base in [("shell",SHELL),("outer",OUT),("inner",INN)]:
        for coef in ["none","col","row","both","coldiv"]:
            A=make_area(base,coef)
            for rev in (False,True):
                seq=A[::-1] if rev else A
                for pname,P in PAIRS.items():
                    if P is None: continue
                    for tname,T in TRANS.items():
                        byts=[T(seq[i],seq[j]) for i,j in P]
                        if len(byts)!=32: continue
                        n+=1
                        if verify(byts,f"{base_name}|coef={coef}|rev={rev}|{pname}|{tname}"):
                            return
    print(f"[done] checked {n} interpretations against address, no match")

if __name__=="__main__":
    run()
