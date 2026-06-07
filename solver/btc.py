"""Bitcoin P2PKH address derivation (pure Python secp256k1) + WIF parsing.

Purpose: a *verification oracle*. The prize sits at two known addresses, so any
candidate private key recovered from a decrypted blob can be checked instantly:
does it derive to 1GSMG... or 17ucy...?
"""
import hashlib

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

TARGETS = {
    "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe": "half (prize address)",
    "17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa": "better half (second address)",
}

def _inv(a, m=P):
    return pow(a, m - 2, m)

def _add(p, q):
    if p is None: return q
    if q is None: return p
    (x1, y1), (x2, y2) = p, q
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p == q:
        l = (3 * x1 * x1) * _inv(2 * y1) % P
    else:
        l = (y2 - y1) * _inv(x2 - x1) % P
    x3 = (l * l - x1 - x2) % P
    y3 = (l * (x1 - x3) - y1) % P
    return (x3, y3)

def _mul(k, p=(GX, GY)):
    r = None
    while k:
        if k & 1:
            r = _add(r, p)
        p = _add(p, p)
        k >>= 1
    return r

def _b58(b: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = alphabet[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\x00"))) + s

def _hash160(b: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()

def _addr(pubkey: bytes) -> str:
    payload = b"\x00" + _hash160(pubkey)
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return _b58(payload + chk)

def privkey_to_addresses(priv_int: int):
    """Return (compressed_addr, uncompressed_addr) for a private key integer."""
    if not (1 <= priv_int < N):
        return None, None
    x, y = _mul(priv_int)
    unc = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    comp = (b"\x03" if y & 1 else b"\x02") + x.to_bytes(32, "big")
    return _addr(comp), _addr(unc)

def check_candidate(priv_int: int):
    """Return target match info if this key controls either prize address."""
    c, u = privkey_to_addresses(priv_int)
    for a, kind in ((c, "compressed"), (u, "uncompressed")):
        if a in TARGETS:
            return {"address": a, "form": kind, "label": TARGETS[a]}
    return None

def candidates_from_bytes(pt: bytes):
    """Yield candidate private-key integers extracted from a plaintext blob:
    64-hex strings, WIF strings, and the raw 32 bytes themselves."""
    import re
    text = pt.decode("latin-1", "ignore")
    for h in re.findall(r"[0-9a-fA-F]{64}", text):
        yield int(h, 16)
    # WIF
    for w in re.findall(r"[5KL][1-9A-HJ-NP-Za-km-z]{50,51}", text):
        try:
            yield wif_to_int(w)
        except Exception:
            pass
    # raw 32-byte windows
    for i in range(0, max(1, len(pt) - 31)):
        chunk = pt[i:i + 32]
        if len(chunk) == 32:
            yield int.from_bytes(chunk, "big")

def wif_to_int(wif: str) -> int:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = 0
    for ch in wif:
        n = n * 58 + alphabet.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    body = raw[1:-4]  # strip version + checksum
    if len(body) == 33 and body[-1] == 0x01:  # compressed flag
        body = body[:-1]
    return int.from_bytes(body, "big")

if __name__ == "__main__":
    # Known test vectors for privkey = 1
    c, u = privkey_to_addresses(1)
    assert u == "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm", u
    assert c == "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", c
    print("[PASS] secp256k1 -> address vectors (privkey=1)")
    print("       uncompressed:", u)
    print("       compressed:  ", c)
    print("Oracle ready. Targets:")
    for a, k in TARGETS.items():
        print("  ", a, "-", k)
