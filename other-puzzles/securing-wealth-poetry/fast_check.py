#!/usr/bin/env python3
"""Fast candidate checker using coincurve (libsecp256k1). Same TARGET/paths as
check.py but ~20x faster. check_mnemonic(words) -> list of (path,comp) hits or
None (bad checksum) or [] (valid, no match)."""
import hashlib, hmac
from mnemonic import Mnemonic
import coincurve, base58

TARGET = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"
mnemo = Mnemonic("english")
WLIDX = {w:i for i,w in enumerate(mnemo.wordlist)}
CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H = 0x80000000
PATHS = {
    "m":               [],
    "m/0":             [0],
    "m/0/0":           [0,0],
    "m/0'/0'/0'":      [0|H,0|H,0|H],
    "m/0'/0/0":        [0|H,0,0],
    "m/44'/0'/0'/0/0": [44|H,0|H,0|H,0,0],
    "m/44'/0'/0'/0/1": [44|H,0|H,0|H,0,1],
    "m/49'/0'/0'/0/0": [49|H,0|H,0|H,0,0],
    "m/84'/0'/0'/0/0": [84|H,0|H,0|H,0,0],
}

def _b58c(prefix,payload):
    d=prefix+payload; c=hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]
    return base58.b58encode(d+c).decode()
def _h160(b): return hashlib.new("ripemd160",hashlib.sha256(b).digest()).digest()
def _pubc(priv): return coincurve.PublicKey.from_valid_secret(priv).format(True)
def _pubu(priv): return coincurve.PublicKey.from_valid_secret(priv).format(False)
def _addr(priv,comp): return _b58c(b"\x00",_h160(_pubc(priv) if comp else _pubu(priv)))

def _master(seed):
    I=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest(); return I[:32],I[32:]
def _ckd(k,c,i):
    data=(b"\x00"+k if i&H else _pubc(k))+i.to_bytes(4,"big")
    I=hmac.new(c,data,hashlib.sha512).digest()
    return ((int.from_bytes(I[:32],"big")+int.from_bytes(k,"big"))%CURVE_N).to_bytes(32,"big"),I[32:]
def _derive(seed,path):
    k,c=_master(seed)
    for i in path: k,c=_ckd(k,c,i)
    return k

def valid_checksum_12(words):
    try: bits="".join(format(WLIDX[w],"011b") for w in words)
    except KeyError: return False
    if len(bits)!=132: return False
    ent,cs=bits[:128],bits[128:]
    h=hashlib.sha256(int(ent,2).to_bytes(16,"big")).digest()
    return format(h[0],"08b")[:4]==cs

def check_mnemonic(words, passphrase=""):
    if len(words)==12 and not valid_checksum_12(words):
        return None
    if not mnemo.check(" ".join(words)):
        return None
    seed=Mnemonic.to_seed(" ".join(words),passphrase)
    hits=[]
    for name,path in PATHS.items():
        priv=_derive(seed,path)
        for comp in (True,False):
            if _addr(priv,comp)==TARGET:
                hits.append((name,"comp" if comp else "uncomp"))
    return hits
