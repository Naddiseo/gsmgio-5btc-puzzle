#!/usr/bin/env python3
"""Bitcoin helpers: privkey (32 bytes / int / hex) -> P2PKH addresses, and
checks against the known GSMG puzzle addresses. Uses coincurve."""
import hashlib
import coincurve, base58

# The only two OFFICIAL known puzzle addresses (per puzzle owner / community).
GSMG_ADDRS = {
    "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe": "main puzzle / final prize address",
    "17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa": "where half the funds moved during the halving",
}

def _h160(b): return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()
def _b58c(prefix, payload):
    d=prefix+payload; c=hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]
    return base58.b58encode(d+c).decode()

def priv_to_addrs(priv32):
    """Return {compressed_addr, uncompressed_addr} for a 32-byte private key."""
    if not (0 < int.from_bytes(priv32,"big") < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141):
        return {}
    pk=coincurve.PublicKey.from_valid_secret(priv32)
    out={}
    out["comp"]=_b58c(b"\x00", _h160(pk.format(True)))
    out["uncomp"]=_b58c(b"\x00", _h160(pk.format(False)))
    return out

def check_priv(priv32, label=""):
    a=priv_to_addrs(priv32)
    for kind,addr in a.items():
        if addr in GSMG_ADDRS:
            print(f"[!!!] MATCH {label} {kind}: {addr}  ({GSMG_ADDRS[addr]})")
            return (label,kind,addr)
    return None

def sha256(s):
    if isinstance(s,str): s=s.encode()
    return hashlib.sha256(s).digest()

if __name__=="__main__":
    # sanity: a known privkey=1 address
    print(priv_to_addrs((1).to_bytes(32,"big")))
