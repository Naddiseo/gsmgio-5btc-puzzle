#!/usr/bin/env python3
"""Zden LVL5: empirical search using known-plaintext from the hint string
'09111819 FIX 11122111' => private key starts 09 11 18 19, ends 11 12 21 11.
Search pairing x transform over the 64 shell areas to match those 8 bytes,
then verify the full derived key against the target address."""
import csv, itertools, hashlib
import coincurve, base58

TARGET="1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7"
PREFIX=[0x09,0x11,0x18,0x19]
SUFFIX=[0x11,0x12,0x21,0x11]

# load areas: rows of (outer, inner, shell)
rows=[]
with open('research/Analysis/Results/noLine_A.csv') as f:
    for line in f:
        o,i,s=[int(v) for v in line.split(',')]
        rows.append((o,i,s))
assert len(rows)==64
OUT=[r[0] for r in rows]; INN=[r[1] for r in rows]; SHELL=[r[2] for r in rows]

def addr(priv,comp):
    pub=coincurve.PublicKey.from_valid_secret(priv).format(comp)
    h=hashlib.new('ripemd160',hashlib.sha256(pub).digest()).digest(); d=b'\x00'+h
    return base58.b58encode(d+hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]).decode()

def verify(byts,tag):
    priv=bytes(b%256 for b in byts)
    if priv==b'\x00'*32: return False
    for comp in (True,False):
        try:
            if addr(priv,comp)==TARGET:
                print(f"\n[!!!] MATCH {tag} {'comp' if comp else 'uncomp'}\nPRIV {priv.hex()}")
                open('MATCH.txt','w').write(tag+" "+priv.hex()); return True
        except Exception: return False
    return False

# pairings: list of 32 (idxA, idxB)
def pairings():
    yield "adj",      [(2*k,2*k+1) for k in range(32)]
    yield "half",     [(k,k+32) for k in range(32)]
    yield "interleave_oddeven", [(k,k+1) for k in range(0,64,2)]  # == adj
    yield "slide_first32", [(k,k+1) for k in range(32)]
    yield "col_adj",  None  # handled separately if needed

# transforms applied to (a+b) or to each then combined
def transforms():
    yield "sum%256",        lambda a,b:(a+b)%256
    yield "(-1*(a+b)+64)%256", lambda a,b:(-1*(a+b)+64)%256
    yield "(a+b)//1%256",   lambda a,b:(a+b)%256
    yield "(a+b)//2%256",   lambda a,b:((a+b)//2)%256
    yield "(a+b)//4%256",   lambda a,b:((a+b)//4)%256
    yield "(a%256+b%256)%256", lambda a,b:((a%256)+(b%256))%256
    yield "(a+b)%255",      lambda a,b:(a+b)%255
    yield "64-(a+b)%256",   lambda a,b:(64-((a+b)%256))%256
    yield "(a*b)%256",      lambda a,b:(a*b)%256
    yield "(a-b)%256",      lambda a,b:(a-b)%256

AREAS={"shell":SHELL,"outer":OUT,"inner":INN}

def matches_known(byts):
    return byts[:4]==PREFIX and byts[28:32]==SUFFIX

def run():
    near=[]
    for aname,A in AREAS.items():
        for pname,P in pairings():
            if P is None: continue
            for tname,T in transforms():
                byts=[T(A[i],A[j]) for i,j in P]
                if len(byts)!=32: continue
                # count known-byte matches
                score=sum(1 for k in range(4) if byts[k]==PREFIX[k]) + \
                      sum(1 for k in range(4) if byts[28+k]==SUFFIX[k])
                if score>=2:
                    near.append((score,aname,pname,tname,byts[:4],byts[28:32]))
                if matches_known(byts):
                    print(f"[known-plaintext HIT] {aname}|{pname}|{tname}")
                    verify(byts,f"{aname}|{pname}|{tname}")
    near.sort(reverse=True)
    print("top partial matches to known prefix/suffix (score/8):")
    for n in near[:15]:
        print(" ",n[0],n[1],n[2],n[3],"pre",[hex(x) for x in n[4]],"suf",[hex(x) for x in n[5]])
    if not near:
        print("no partial matches >=2")

if __name__=="__main__":
    run()
