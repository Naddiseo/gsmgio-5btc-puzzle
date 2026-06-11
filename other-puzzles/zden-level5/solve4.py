#!/usr/bin/env python3
"""Zden LVL5: exhaustive sweep of ALL linear transforms byte=(m*S+c)%MOD over
the 4 documented pairings x 3 area types, verified against the target address.
Covers the hint formula (-1*x+64 => m=255,c=64) and plain mod (m=1,c=0)."""
import hashlib
import coincurve, base58

TARGET="1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7"
rows=[]
with open('research/Analysis/Results/noLine_A.csv') as f:
    for line in f:
        rows.append(tuple(int(v) for v in line.split(',')))
OUT=[r[0] for r in rows]; INN=[r[1] for r in rows]; SHELL=[r[2] for r in rows]

# 1-indexed pairings from README -> 0-indexed
def p(idxpairs): return [(a-1,b-1) for a,b in idxpairs]
PAIR_adj  = p([(2*k-1,2*k) for k in range(1,33)])
PAIR_2 = p([(1,9),(17,25),(33,41),(49,57),(2,10),(18,26),(34,42),(50,58),
            (3,11),(19,27),(35,43),(51,59),(4,12),(20,28),(36,44),(52,60),
            (5,13),(21,29),(37,45),(53,61),(6,14),(22,30),(38,46),(54,62),
            (7,15),(23,31),(39,47),(55,63),(8,16),(24,32),(40,48),(56,64)])
PAIR_3 = p([(1,9),(2,10),(3,11),(4,12),(5,13),(6,14),(7,15),(8,16),
            (17,25),(18,26),(19,27),(20,28),(21,29),(22,30),(23,31),(24,32),
            (33,41),(34,42),(35,43),(36,44),(37,45),(38,46),(39,47),(40,48),
            (49,57),(50,58),(51,59),(52,60),(53,61),(54,62),(55,63),(56,64)])
PAIR_4 = p([(1,2),(9,10),(17,18),(25,26),(33,34),(41,42),(49,50),(57,58),
            (3,4),(11,12),(19,20),(27,28),(35,36),(43,44),(51,52),(59,60),
            (5,6),(13,14),(21,22),(29,30),(37,38),(45,46),(53,54),(61,62),
            (7,8),(15,16),(23,24),(31,32),(39,40),(47,48),(55,56),(63,64)])
PAIRINGS={"adj":PAIR_adj,"trav2":PAIR_2,"trav3":PAIR_3,"trav4":PAIR_4}
AREAS={"shell":SHELL,"outer":OUT,"inner":INN}

# precompute target hash160
_dec=base58.b58decode(TARGET)
TARGET_H160=_dec[1:21]

def h160(b): return hashlib.new('ripemd160',hashlib.sha256(b).digest()).digest()

def check(byts,tag):
    priv=bytes(byts)
    if priv==b'\x00'*32: return False
    try:
        pk=coincurve.PublicKey.from_valid_secret(priv)
    except Exception: return False
    for comp in (True,False):
        if h160(pk.format(comp))==TARGET_H160:
            print(f"\n[!!!] MATCH {tag} {'comp' if comp else 'uncomp'}\nPRIV {priv.hex()}")
            open('MATCH.txt','w').write(tag+" "+priv.hex()); return True
    return False

def run():
    n=0
    for MOD in (256,255):
        for aname,A in AREAS.items():
            for pname,P in PAIRINGS.items():
                S=[A[i]+A[j] for i,j in P]   # 32 sums
                for m in range(256):
                    for c in range(256):
                        byts=[(m*s+c)%MOD & 0xFF for s in S]
                        n+=1
                        if check(byts,f"MOD{MOD}|{aname}|{pname}|m={m}|c={c}"):
                            print(f"checked {n}"); return
    print(f"[done] swept {n} linear transforms, no match")

if __name__=="__main__":
    run()
