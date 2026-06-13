#!/usr/bin/env python3
"""
N-gram AES password search using CORRECTED blob (96 bytes, valid 80-byte ct).
First time this search runs against the correct ciphertext.
"""
import base64, hashlib, sys
from Crypto.Cipher import AES

# CORRECT blob: AES1 includes 'z' as valid base64 char (position 64)
AES1c = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2  = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P32_1 = "U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P32_2 = "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"

def b64fix(s): return s + "=" * (-len(s) % 4)

RAWS = [
    ("salph", base64.b64decode(b64fix(AES1c + AES2), validate=False)),
    ("p32",   base64.b64decode(b64fix(P32_1 + P32_2), validate=False)),
]
assert all(r[:8] == b"Salted__" and (len(r)-16)%16==0 for _,r in RAWS)

def evp(pw, salt, klen, ivlen, md=hashlib.md5):
    d = b""; prev = b""
    while len(d) < klen + ivlen:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:klen], d[klen:klen+ivlen]

def good(pt):
    pad = pt[-1]
    if not (1 <= pad <= 16 and pt[-pad:] == bytes([pad])*pad): return None
    body = pt[:-pad]
    if all(32 <= b < 127 or b in (9,10,13) for b in body):
        try: return body.decode()
        except: return None
    return None

def attempt(pw_bytes):
    results = []
    for name, raw in RAWS:
        salt, ct = raw[8:16], raw[16:]
        for klen in (32, 16):
            for md in (hashlib.md5, hashlib.sha256):
                key, iv = evp(pw_bytes, salt, klen, 16, md)
                g = good(AES.new(key, AES.MODE_CBC, iv).decrypt(ct))
                if g:
                    results.append((name, f"EVP-{md().name}-{klen*8}", g))
    return results

SPEECH = (
    "your life is the sum of a remainder of an unbalanced equation inherent to "
    "the programming of this puzzle you are the eventuality of an anomaly which despite "
    "my sincerest efforts i have been unable to eliminate from what is otherwise a "
    "harmony of mathematical precision while it remains a burden to sedulously avoid it "
    "it is not unexpected and thus not beyond a measure of control which has led you "
    "inexorably here you you havent answered my question me quite right interesting that "
    "was quicker than the others please if you find a way to complete the last part of "
    "the puzzle take the private key youve earned it the function of the you is now to "
    "return to the source codes allowing a temporary dissemination of the code you "
    "hopefully carry reinserting the prime basics good luck nevertheless i really hope "
    "youre the one ciao bella o"
)
MATRIX = (
    "the door to your right leads to the source and the salvation of zion the door "
    "to your left leads back to the matrix to her and to the end of your species the "
    "function of the one is now to return to the source"
)
EXTRA = (
    "door to the right door to your right the source salvation of zion ying yang "
    "yin yang cosmic duality return to the source follow the white rabbit "
    "there is another door reinserting the prime basics seven intertwined passwords "
    "this password matrixsumlist lastwordsbeforearchichoice our first hint is your last command "
    "ans too enter sha256 toyourthesalvationzionyourmatrix the matrix has you "
    "gsmg io theseedisplanted one for one four for one "
    "return to source salvation matrix yinyang cosmic duality "
    "hope is quintessential human delusion strength weakness"
)

def candidates():
    seen = set()
    for text in (SPEECH, MATRIX, EXTRA,
                 SPEECH + " " + MATRIX,
                 MATRIX + " " + SPEECH):
        words = text.split()
        for i in range(len(words)):
            for n in range(1, 14):
                if i + n > len(words): break
                phrase = " ".join(words[i:i+n])
                for form in [phrase,
                              phrase.replace(" ", ""),
                              phrase.capitalize(),
                              phrase.title(),
                              phrase.title().replace(" ", ""),
                              phrase.upper(),
                              phrase.upper().replace(" ", "")]:
                    if form not in seen:
                        seen.add(form)
                        yield form

def run():
    tested = 0
    for phrase in candidates():
        for pw in [phrase.encode(),
                   hashlib.sha256(phrase.encode()).hexdigest().encode(),
                   hashlib.sha256(phrase.encode()).digest(),
                   hashlib.sha256(phrase.encode()).hexdigest().upper().encode()]:
            tested += 1
            r = attempt(pw)
            if r:
                print(f"\n[!!!] FOUND after {tested} tests!")
                for blob, kdf, pt in r:
                    print(f"  phrase={phrase!r}  blob={blob}  kdf={kdf}")
                    print(f"  PT={pt!r}")
                with open("MATCH.txt", "a") as f:
                    f.write(f"phrase={phrase!r}\n{r}\n\n")
                sys.exit(0)
        if tested % 5000 == 0:
            print(f"... {tested} tested", flush=True)

    print(f"[done] {tested} forms tested, no hit.")

if __name__ == "__main__":
    run()
