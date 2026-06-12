#!/usr/bin/env python3
"""
Attack the SalPhaseIon OpenSSL AES blob.

The blob is OpenSSL `enc` output: base64("Salted__" + 8-byte salt + ciphertext).
Key+IV are derived by EVP_BytesToKey(MD5, 1 iter) from password+salt (the legacy
`openssl enc -aes-256-cbc` default; we also try -aes-128 and the newer
PBKDF2/-sha256 variants). A correct password yields valid PKCS#7 padding and
(almost certainly) printable ASCII — an unambiguous, coincidence-proof success.
"""
import base64, hashlib, itertools
from Crypto.Cipher import AES

# AES1 + AES2 chunks from the SalPhaseIon page (z between them = separator, dropped)
AES1 = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9"
AES2 = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"

def b64fix(s):
    return s + "=" * (-len(s) % 4)

def get_blob():
    for combo,label in [(AES1+AES2,"AES1+AES2"), (AES1,"AES1"),
                        (AES1+"z"+AES2,"with-z"), (AES2,"AES2")]:
        raw = base64.b64decode(b64fix(combo), validate=False)
        yield label, raw

def evp_bytestokey(password, salt, key_len, iv_len, md=hashlib.md5):
    d=b""; prev=b""
    while len(d) < key_len+iv_len:
        prev=md(prev+password+salt).digest(); d+=prev
    return d[:key_len], d[key_len:key_len+iv_len]

def try_decrypt(raw, password):
    if raw[:8]!=b"Salted__": return None
    salt=raw[8:16]; ct=raw[16:]
    if len(ct)%16: return None
    pw=password.encode() if isinstance(password,str) else password
    res=[]
    # legacy md5 KDF, AES-256 and AES-128
    for klen in (32,16):
        for md in (hashlib.md5, hashlib.sha256):
            key,iv=evp_bytestokey(pw,salt,klen,16,md)
            pt=AES.new(key,AES.MODE_CBC,iv).decrypt(ct)
            pad=pt[-1]
            if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad:
                body=pt[:-pad]
                try:
                    txt=body.decode("ascii")
                    res.append((f"md={md().name},klen={klen}", txt))
                except:
                    if all(32<=b<127 or b in (9,10,13) for b in body):
                        res.append((f"md={md().name},klen={klen}", repr(body)))
    return res or None

PASSWORDS = [
 "thispassword","matrixsumlist","lastwordsbeforearchichoice",
 "ourfirsthintisyourlastcommand","anstoo","shabef","ans too",
 "our first hint is your last command","last words before archi choice",
 "cosmicduality","cosmic duality","salphaseion","salphaseioncosmicduality",
 "yinyang","ying yang","salvation","yellowblueprimes","btcseed","youwon",
 "matrix sum list","this password","SalPhaseIon","CosmicDuality",
]

def run():
    for label, raw in get_blob():
        ok = raw[:8]==b"Salted__"
        print(f"[{label}] {len(raw)}B salted={ok} ct_len={len(raw)-16 if ok else '-'}")
        if not ok: continue
        for pw in PASSWORDS:
            r=try_decrypt(raw, pw)
            if r:
                for variant,txt in r:
                    print(f"  [!!!] PW='{pw}' ({variant}): {txt}")
    print("done.")

if __name__=="__main__":
    run()
