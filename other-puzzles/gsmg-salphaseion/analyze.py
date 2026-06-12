#!/usr/bin/env python3
"""
Hypothesis battery for the SalPhaseIon stage. Re-run / extend with new ideas.
Reproduces the two verified findings, then tests conversions of the decoded
material into a private key for the known GSMG addresses (all negative so far),
plus prime-indexed extraction (the documented 'yellow blue primes' lead).
"""
from gsmg_toolkit import *
from btc import check_priv, sha256, GSMG_ADDRS

def primes_upto(n):
    s=[True]*(n+1); s[0:2]=[False,False]
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i,v in enumerate(s) if v]

def main():
    o=otp_result(); i=o.find("YOUWON")
    before, after = o[:i], o[i+6:]
    bifid=bifid_result()
    part0=bifid[7:bifid.find('z')]; part1=bifid.split('z')[1]
    assert bifid.startswith("btcseed") and "YOUWON" in o
    print("Finding 1 (bifid):", bifid[:14], "... single-z split:",
          [len(p) for p in bifid.split('z')])
    print("Finding 2 (otp)  :", f"[{before}] YOUWON [{after}]  ({len(after)} tail)")

    # --- key-derivation hypotheses ---
    cands={"after":after,"before":before,"youwon+after":"YOUWON"+after,
           "otp":o,"part0":part0,"part1":part1,"incase":INCASE,
           "strA":SALPH_STR_A,"strB":SALPH_STR_B}
    hits=[]
    for name,s in cands.items():
        for fn,lbl in [(sha256,"sha256"),(lambda x:sha256(sha256(x)),"2xsha256")]:
            r=check_priv(fn(s.encode() if isinstance(s,str) else s), f"{lbl}({name})")
            if r: hits.append(r)
    def b26(s):
        n=0
        for c in s: n=n*26+(ord(c.upper())-65)
        return (n%2**256).to_bytes(32,"big")
    for name,s in [("after",after),("before",before),("otp",o)]:
        r=check_priv(b26(s), f"base26({name})");  hits.append(r) if r else None

    # --- prime-indexed extraction lead ---
    for name,s in [("after",after),("part1",part1)]:
        P=[p for p in primes_upto(len(s)) if p<len(s)]
        print(f"prime-idx {name}: {''.join(s[p] for p in P)[:60]}")

    print("\nKEY MATCHES:", hits if hits else "NONE",
          "| targets:", list(GSMG_ADDRS))

if __name__=="__main__":
    main()
