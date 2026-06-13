#!/usr/bin/env python3
"""
GSMG phase AES decryptor — CONFIRMED scheme.

Reverse-engineered from the *solved* earlier phases (whose answers are public):
each phase blob is OpenSSL/CryptoJS `Salted__` AES-256-CBC, where:

    passphrase = sha256_HEX(answer)          # the 64-char hex digest, as text
    key, iv    = EVP_BytesToKey(md=SHA256, passphrase, salt, 1 iter)   # AES-256
    plaintext  = AES-256-CBC-decrypt(ciphertext)  ; strip PKCS#7

VERIFIED here:
  * Phase 2   answer "causality"  ->  "The ironic 2name of the keymakers ..."
  * Phase 3.2 answer "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
              ->  "I've been waiting for you. You have many questions ..."

i.e. the KDF digest is **SHA-256, not MD5** (newer `openssl enc` default), and the
passphrase is the *hex* sha256 of the answer string (answers are concatenations
of the phase's sub-solutions). This is the exact scheme the SalPhaseIon "shabef"
(=sha256) labels point to, and the template for the unsolved Cosmic answer.
"""
import base64, hashlib

def evp_bytestokey(pw, salt, klen=32, ivlen=16, md=hashlib.sha256):
    d=b""; prev=b""
    while len(d) < klen+ivlen:
        prev = md(prev+pw+salt).digest(); d += prev
    return d[:klen], d[klen:klen+ivlen]

def decrypt(blob_b64, answer):
    from Crypto.Cipher import AES
    raw = base64.b64decode("".join(blob_b64.split()) + "===")
    assert raw[:8] == b"Salted__", "not a Salted__ blob"
    salt, ct = raw[8:16], raw[16:]
    passphrase = hashlib.sha256(answer.encode()).hexdigest().encode()
    key, iv = evp_bytestokey(passphrase, salt)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt[-pad:] == bytes([pad])*pad:
        pt = pt[:-pad]
    return pt

if __name__ == "__main__":
    PHASE2 = ("U2FsdGVkX18GKGYS1D7X7VjxWz6uUyPFszr8dVvtOIrJqioWHgT69JJnzJGDVOvF"
              "QYWh5BEZxFPXmMq1cbyy3dVVDgLhF050xlDy2J5grtKw9jUOO4oFNRgoD+1dlukX"
              "pd8ccg++kkXgE9mGBP6lQbukDiSjY4mnR2Mv6ydIncrRqacQNVEmEgM4fGTi1ANz")
    out = decrypt(PHASE2, "causality")
    print("Phase 2 (answer='causality') ->")
    print(out.decode("latin1")[:120])
    assert out.startswith(b"The ironic 2name"), "scheme check failed!"
    print("\nSCHEME VERIFIED: passphrase=sha256hex(answer), EVP-sha256, AES-256-CBC")
