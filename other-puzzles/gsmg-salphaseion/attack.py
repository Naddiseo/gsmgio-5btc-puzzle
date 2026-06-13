#!/usr/bin/env python3
"""
Consolidated SalPhaseIon / Cosmic-Duality password attack harness.

Replaces the prior dozen one-off brute scripts (all exhausted, no hit). Holds:
  - the verified OpenSSL/CryptoJS `Salted__` decryptor (round-trip checked),
  - both real ciphertexts (salph 96B salt 3ab585348552415d, cosmic 1344B salt 2d3f6fe06dc950e6),
  - a single candidate generator covering every verified puzzle artifact and the
    blue/yellow prime structure from Denis Golovkin's transcript analysis.

Each password is tried as {raw, sha256-hex, sha256-bin, sha256-HEX} x
EVP_BytesToKey{md5,sha256} x AES-{256,192,128}-CBC, with strict PKCS#7 +
printable-ASCII (or nested-Salted__) acceptance. Run: python3 attack.py
"""
import base64, hashlib, os
from Crypto.Cipher import AES

HERE = os.path.dirname(os.path.abspath(__file__))

AES1 = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2 = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
COSMIC = "".join(open(os.path.join(HERE, "cosmic_duality_blob.txt")).read().split())
# The leftover, never-cracked AES from phase 3.2 notebook cell 18 (salt b45a5e3d827593ca).
# Same scheme; upstream of SalPhaseIon in the chain, so a valid third target.
P32_CELL18 = ("U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
              "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4")
def _b(s): return s + "=" * (-len(s) % 4)
BLOBS = {"salph":  base64.b64decode(_b(AES1 + AES2)),
         "cosmic": base64.b64decode(_b(COSMIC)),
         "p32cell18": base64.b64decode(_b(P32_CELL18))}

# ---- verified decryptor ----
def evp(pw, salt, kl, il, md):
    d = b""; p = b""
    while len(d) < kl + il:
        p = md(p + pw + salt).digest(); d += p
    return d[:kl], d[kl:kl + il]

# PGP/OpenPGP first-byte packet tags (issue #51 reports the cosmic plaintext is a
# ~1327-byte PGP/PKESK message — a binary blob our ASCII filter would have rejected).
_PGP_TAGS = {0x85, 0x84, 0x8c, 0xc1, 0x99, 0x98, 0xa3, 0x95, 0xa6, 0xc3}

def ok(pt):
    pad = pt[-1]
    if not (1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad): return None
    b = pt[:-pad]
    if not b: return None
    if b[:8] == b"Salted__": return ("NESTED", b)
    if b[:14] == b"-----BEGIN PGP": return ("PGP-ARMOR", b)
    pr = sum(1 for x in b if 32 <= x < 127 or x in (9, 10, 13)) / len(b)
    if pr >= 0.95: return ("ASCII", b)
    # weak PGP signal: packet-tag first byte (report but flag low-confidence)
    if len(b) >= 32 and b[0] in _PGP_TAGS: return ("PGP?-weak", b)
    return None

def test(s, label):
    pwb = s.encode() if isinstance(s, str) else s
    for fb in (pwb, hashlib.sha256(pwb).hexdigest().encode(),
               hashlib.sha256(pwb).digest(),
               hashlib.sha256(pwb).hexdigest().upper().encode()):
        for bn, raw in BLOBS.items():
            salt, ct = raw[8:16], raw[16:]
            for kl in (32, 24, 16):
                for md in (hashlib.md5, hashlib.sha256):
                    k, iv = evp(fb, salt, kl, 16, md)
                    r = ok(AES.new(k, AES.MODE_CBC, iv).decrypt(ct))
                    if r:
                        print(f"\n[!!! HIT] {label!r} blob={bn} EVP{md().name} "
                              f"AES{kl*8} {r[0]}\n  PT={r[1][:200]!r}")
                        open(os.path.join(HERE, "MATCH.txt"), "a").write(
                            f"{label!r} {bn}\n{r[1]!r}\n\n")
                        return True
    return False

# ---- verified puzzle artifacts ----
STR_A = "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
SUM = "DIFNLREV9E6VARXVF5UF8PE"
OTP_PRE = "VOZIJBDTIQBRGVEOMZNBC"
OTP_TAIL = "XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA"
BIFID = "deoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeld"
INCASE = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
comp = STR_A.replace("be", "y")
BY = "".join(c for c in comp if c in "by")          # 25 tokens: 15 b(blue) + 10 y(yellow)
BITS = BY.translate(str.maketrans("by", "10"))

def gen():
    seen = set()
    singles = [
        STR_A, SUM, SUM.lower(), OTP_PRE.lower(), OTP_TAIL.lower(),
        OTP_PRE.lower() + "youwon" + OTP_TAIL.lower(), "youwon",
        BIFID, "btcseed" + BIFID, "btcseed", INCASE, INCASE.lower(),
        "matrixsumlist", "lastwordsbeforearchichoice", "thispassword",
        "yinyang", "yingyang", "cosmicduality", "salvation", "salvationofzion",
        "followthewhiterabbit", "thematrixhasyou", "halfandbetterhalf",
        BY, comp, BITS, "blueyellow", "yellowblue",
        "ourfirsthintisyourlastcommand", "anstoo",
    ]
    parts = {"sum": SUM.lower(), "by": BY, "bits": BITS, "incase": INCASE.lower(),
             "matrixsumlist": "matrixsumlist", "youwon": "youwon",
             "btcseed": "btcseed", "lastwords": "lastwordsbeforearchichoice",
             "thispassword": "thispassword", "yinyang": "yinyang",
             "salvation": "salvation"}
    cands = [(s, s[:24]) for s in singles]
    ks = list(parts)
    for i in range(len(ks)):
        for j in range(len(ks)):
            if i != j:
                cands.append((parts[ks[i]] + parts[ks[j]], f"{ks[i]}+{ks[j]}"))
    for pw, lbl in cands:
        k = pw.encode() if isinstance(pw, str) else pw
        if k in seen: continue
        seen.add(k)
        yield pw, lbl

if __name__ == "__main__":
    n = 0
    for pw, lbl in gen():
        n += 1
        if test(pw, lbl):
            print(f"SOLVED #{n}"); break
    else:
        print(f"[done] {n} candidates, no hit.")
