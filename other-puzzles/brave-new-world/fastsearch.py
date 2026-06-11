#!/usr/bin/env python3
"""
Fast exhaustive ordering search over a FIXED 12-word set, using coincurve.

Rationale: if we are confident about *which* 12 words make up the mnemonic but
not their order, then 12! = 479,001,600 orderings is exhaustively searchable.
coincurve (libsecp256k1) makes each derivation ~0.05-0.1 ms, and we shard the
12! space across processes by fixing the first word per worker (12 shards).

Only ~1/16 orderings pass the BIP39 checksum; the rest are skipped before any
EC work. For each valid mnemonic we derive the standard legacy paths and
compare to TARGET.
"""
import sys, os, hashlib, hmac, itertools, time
from multiprocessing import Process, Queue
from mnemonic import Mnemonic
import coincurve, base58

TARGET = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
mnemo = Mnemonic("english")
wl = mnemo.wordlist
widx = {w:i for i,w in enumerate(wl)}
CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H = 0x80000000
PATHS = [
    [44|H,0|H,0|H,0,0],
    [0,0],
    [0|H,0|H,0|H],
    [0],
    [],
    [44|H,0|H,0|H,0,1],   # next receiving index, just in case
]

def b58check(p,pay):
    d=p+pay; c=hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]
    return base58.b58encode(d+c).decode()
def h160(b): return hashlib.new("ripemd160",hashlib.sha256(b).digest()).digest()
def pub_comp(priv):
    return coincurve.PublicKey.from_valid_secret(priv).format(compressed=True)
def pub_uncomp(priv):
    return coincurve.PublicKey.from_valid_secret(priv).format(compressed=False)
def addr(priv, comp=True):
    return b58check(b"\x00", h160(pub_comp(priv) if comp else pub_uncomp(priv)))

def master(seed):
    I=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest(); return I[:32],I[32:]
def ckd(k,c,i):
    if i&H: data=b"\x00"+k+i.to_bytes(4,"big")
    else:   data=pub_comp(k)+i.to_bytes(4,"big")
    I=hmac.new(c,data,hashlib.sha512).digest()
    ki=(int.from_bytes(I[:32],"big")+int.from_bytes(k,"big"))%CURVE_N
    return ki.to_bytes(32,"big"),I[32:]
def derive(seed,path):
    k,c=master(seed)
    for i in path: k,c=ckd(k,c,i)
    return k

def valid_checksum(words):
    # 12 words -> 132 bits; verify the 4-bit checksum without full mnemo.check
    b = "".join(format(widx[w],"011b") for w in words)
    ent, cs = b[:128], b[128:]
    h = hashlib.sha256(int(ent,2).to_bytes(16,"big")).digest()
    return format(h[0],"08b")[:4] == cs

def worker(first, others, q):
    n=0; valid=0
    for perm in itertools.permutations(others):
        words=(first,)+perm
        if not valid_checksum(words):
            continue
        valid+=1
        seed=Mnemonic.to_seed(" ".join(words),"")
        for path in PATHS:
            priv=derive(seed,path)
            for comp in (True,False):
                if addr(priv,comp)==TARGET:
                    q.put(("MATCH"," ".join(words),path,comp)); return
        n+=1
    q.put(("done",first,valid))

def run(wordset):
    assert len(wordset)==12
    print(f"[*] exhaustive ordering search over: {wordset}",flush=True)
    print(f"[*] 12! = 479,001,600 orderings, ~1/16 valid checksum",flush=True)
    q=Queue(); procs=[]
    for first in wordset:
        others=[w for w in wordset if w is not first]
        # use index-based removal to keep duplicates correct
        others=list(wordset); others.remove(first)
        p=Process(target=worker,args=(first,others,q)); p.start(); procs.append(p)
    done=0; t0=time.time()
    while done<len(wordset):
        msg=q.get()
        if msg[0]=="MATCH":
            print("\n[!!!] MATCH:",msg[1],"path",msg[2],"comp",msg[3],flush=True)
            with open("MATCH.txt","w") as f: f.write(str(msg))
            for p in procs: p.terminate()
            return
        done+=1
        print(f"  shard '{msg[1]}' done, valid_checksum={msg[2]} ({done}/12) elapsed={time.time()-t0:.0f}s",flush=True)
    print(f"[done] no match for this word set. elapsed={time.time()-t0:.0f}s",flush=True)

if __name__=="__main__":
    if len(sys.argv)>1:
        ws=sys.argv[1].split()
    else:
        ws=["welcome","brave","world","order","stable","moon","tower","food","this","subject","real","black"]
    run(ws)
