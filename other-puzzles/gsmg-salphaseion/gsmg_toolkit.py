#!/usr/bin/env python3
"""
GSMG.IO 5 BTC puzzle — SalPhaseIon stage toolkit.

Canonical strings and the two reproduced community findings:
  * STR_B "faed" (570, a-i) --bifid(key=dbifhceg)--> btcseed + 90 + 'z' + 472
  * STR_A "dbbi" (91,  a-i) --OTP(key=INCASE..., res=(c-k)%26)--> 21 + YOUWON + 64

All reproductions VERIFIED against the Telegram community transcript.
"""

# ---- canonical ciphertext strings (a-i) ----
SALPH_STR_A = "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"  # 91
# STR_B recovered from the CyberChef bifid input (base64) in the transcript:
import base64
_B64_B = ("ZmFlZGdnZWVkZmNiZGFiaGhnZ2NhZGNmZWRkZ2ZkZ2JnaWdhYWVkZ2dpYWZhZWNnaGdnY2RhaWhlaGFo"
 "YmFoaWdjZWlmZ2JmZ2VmZ2FpZmFiaWZhZ2FlZ2VhY2diYmVhZ2ZnZ2VlZ2dhZmJhY2dmY2RiZWlmZmFh"
 "ZmNpZGFoZ2RlZWZnaGhjZ2dhZWdkZWJoaGVnZWdoY2VnYWRmYmRpYWdlZmNpY2dnaWZkY2dhYWdnZmJp"
 "Z2FpY2ZiaGVjYWVjYmNlaWFpY2ViZ2JnaWVjZGVnZ2ZnZWdhZWRnZ2ZpaWNpaWlmaWZoZ2djZ2ZnZGNk"
 "Z2dlZmNiZWVpZ2VmaWJnaWJnZ2doaGZiY2dpZmRlaGVkZmRhZ2ljZGJoaWNnYWllZGFlaGFoZ2hoY2lo"
 "ZGdoZmhiaWljZWNiaWljaGloaWlpZ2lkZGdlaGhkZmRjaGNiYWZnZmJoYWhlYWdlZ2VjYWZlaGdjZmdn"
 "Z2djYWdmaGhnaGJhaWhpZGllaGhmZGVnZ2RnY2loZ2dnZ2doYWRhaGlnaWdiZ2VjZ2VkZmNkZ2dhY2Nk"
 "ZWhpaWNpZ2ZiZmZoZ2dhZWlkYmJlaWJiZWlpZmRnZmRoaWVlZWllZWVjaWZkZ2RhaGRpZ2dmaGVnZmlh"
 "ZmZpZ2diY2JjZWhjZWFiZmJlZGJpaWJmYmZkZWRlZWhnaWdmYWFpZ2dhZ2JlaWljaGllZGlmYmVoZ2Jj"
 "Y2FoaGJpaWJpYmJpYmRjYmFoYWlkaGZhaGlpaGlj")
SALPH_STR_B = base64.b64decode(_B64_B).decode()  # 570

INCASE = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
BIFID_KEY = "dbifhceg"

# ---- bifid ----
def make_square(keyword):
    seen=[]
    for ch in keyword.lower():
        if ch=='j': ch='i'
        if ch.isalpha() and ch not in seen: seen.append(ch)
    for ch in "abcdefghiklmnopqrstuvwxyz":
        if ch not in seen: seen.append(ch)
    return seen

def bifid_decode(ct, keyword=BIFID_KEY, period=0):
    sq=make_square(keyword); pos={c:(i//5,i%5) for i,c in enumerate(sq)}
    ct=[('i' if c=='j' else c) for c in ct.lower() if c.isalpha()]
    if period<=0: period=len(ct)
    out=[]
    for s in range(0,len(ct),period):
        block=ct[s:s+period]; seq=[]
        for c in block: r,co=pos[c]; seq+=[r,co]
        half=len(seq)//2; rows,cols=seq[:half],seq[half:]
        for i in range(len(block)): out.append(sq[rows[i]*5+cols[i]])
    return ''.join(out)

# ---- OTP / Vigenere family ----
def otp(cipher, key, op="sub"):
    f={"sub":lambda c,k:(c-k)%26,"keysub":lambda c,k:(k-c)%26,"add":lambda c,k:(c+k)%26}[op]
    return ''.join(chr(f(ord(cipher[i].lower())-97, ord(key[i].lower())-97)+65)
                   for i in range(min(len(cipher),len(key))))

# ---- convenience: the two reproduced results ----
def bifid_result(): return bifid_decode(SALPH_STR_B)
def otp_result():   return otp(SALPH_STR_A, INCASE, "sub")  # -> 21 + YOUWON + 64

if __name__=="__main__":
    b=bifid_result(); o=otp_result()
    assert b.startswith("btcseed"), b[:20]
    assert "YOUWON" in o, o
    print("STR_A len", len(SALPH_STR_A), "STR_B len", len(SALPH_STR_B))
    print("bifid:", b[:60], "...")
    print("otp  :", o)
    i=o.find("YOUWON"); print("before:", o[:i], "| after(64):", o[i+6:])
