#!/usr/bin/env python3
"""
Systematic AES password search: try every contiguous word n-gram of the
architect speech (and the canonical Matrix Reloaded architect monologue) as the
OpenSSL password — raw, no-spaces, and sha256(hex/raw) forms, across md5/sha256
KDF and AES-128/256. Valid PKCS#7 padding + printable ASCII = unambiguous hit.
"""
import base64, hashlib
from Crypto.Cipher import AES
from aes_attack import b64fix, evp_bytestokey

raw = base64.b64decode(b64fix(
 "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
 "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"))
SALT, CT = raw[8:16], raw[16:]

SPEECH = ("your life is the sum of a remainder of an unbalanced equation inherent to "
 "the programming of this puzzle you are the eventuality of an anomaly which despite "
 "my sincerest efforts i have been unable to eliminate from what is otherwise a "
 "harmony of mathematical precision while it remains a burden to sedulously avoid it "
 "it is not unexpected and thus not beyond a measure of control which has led you "
 "inexorably here you you havent answered my question me quite right interesting that "
 "was quicker than the others please if you find a way to complete the last part of "
 "the puzzle take the private key youve earned it the function of the you is now to "
 "return to the source codes allowing a temporary dissemination of the code you "
 "hopefully carry reinserting the prime basics good luck nevertheless i really hope "
 "youre the one ciao bella o")
MATRIX = ("the door to your right leads to the source and the salvation of zion the door "
 "to your left leads back to the matrix to her and to the end of your species the "
 "function of the one is now to return to the source")
EXTRA = ("door to the right door to your right the source salvation of zion ying yang "
 "yin yang cosmic duality return to the source follow the white rabbit")

def good(pt):
    pad = pt[-1]
    if not (1 <= pad <= 16 and pt[-pad:] == bytes([pad])*pad): return None
    body = pt[:-pad]
    if all(32 <= b < 127 or b in (9,10,13) for b in body):
        try: return body.decode()
        except: return None
    return None

def attempt(pw_bytes):
    for klen in (32, 16):
        for md in (hashlib.md5, hashlib.sha256):
            key, iv = evp_bytestokey(pw_bytes, SALT, klen, 16, md)
            g = good(AES.new(key, AES.MODE_CBC, iv).decrypt(CT))
            if g is not None:
                return f"klen{klen}/{md().name}", g
    return None

def candidates():
    seen = set()
    for text in (SPEECH, MATRIX, EXTRA):
        w = text.split()
        for i in range(len(w)):
            for n in range(1, 14):
                if i+n > len(w): break
                phrase = " ".join(w[i:i+n])
                for form in (phrase, phrase.replace(" ", ""),
                             phrase.capitalize(), phrase.title().replace(" ","")):
                    if form in seen: continue
                    seen.add(form)
                    yield form

def run():
    tested = 0
    for phrase in candidates():
        for pw in (phrase.encode(),
                   hashlib.sha256(phrase.encode()).hexdigest().encode(),
                   hashlib.sha256(phrase.encode()).digest(),
                   hashlib.sha256(phrase.encode()).hexdigest().upper().encode()):
            tested += 1
            r = attempt(pw)
            if r:
                print(f"\n[!!!] HIT phrase={phrase!r} pw-form via {r[0]}: {r[1]}")
                open("MATCH.txt","w").write(f"{phrase}\n{r}")
                return
    print(f"[done] tested ~{tested} password forms, no valid decryption.")

if __name__ == "__main__":
    run()
