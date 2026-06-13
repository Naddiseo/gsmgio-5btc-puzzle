#!/usr/bin/env python3
"""
Full AES password attack with CORRECTED blobs.
The salph blob requires 'z' included in AES1 (it's a valid base64 char, not a separator).
AES1_correct = AES1 + 'z' (64 chars total)
"""
import base64, hashlib, sys
from Crypto.Cipher import AES

# ── CORRECT blob assembly ──────────────────────────────────────────
# AES1 ends with 'z' — it IS part of the base64 (base64 char value 51)
AES1_CORRECT = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2         = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P32_1        = "U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P32_2        = "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"

def b64fix(s): return s + "=" * (-len(s) % 4)

BLOBS = {
    "salph": base64.b64decode(b64fix(AES1_CORRECT + AES2), validate=False),
    "p32":   base64.b64decode(b64fix(P32_1 + P32_2), validate=False),
}

for name, raw in BLOBS.items():
    assert raw[:8] == b"Salted__", f"{name} bad header"
    assert (len(raw) - 16) % 16 == 0, f"{name} bad ct len {len(raw)-16}"

def evp_bytestokey(pw, salt, klen, ivlen, md=hashlib.md5):
    d = b""; prev = b""
    while len(d) < klen + ivlen:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:klen], d[klen:klen+ivlen]

def try_decrypt(raw, pw_bytes):
    salt, ct = raw[8:16], raw[16:]
    results = []
    for klen in (32, 16):
        for md in (hashlib.md5, hashlib.sha256):
            key, iv = evp_bytestokey(pw_bytes, salt, klen, 16, md)
            pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
            pad = pt[-1]
            if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
                body = pt[:-pad]
                if all(32 <= b < 127 or b in (9,10,13) for b in body):
                    results.append((f"EVP-{md().name}-AES{klen*8}", body.decode()))
    for klen in (32, 16):
        for digest in ('sha256', 'sha512', 'md5'):
            for iters in (1, 1000):
                dk = hashlib.pbkdf2_hmac(digest, pw_bytes, salt, iters, dklen=klen+16)
                key, iv = dk[:klen], dk[klen:klen+16]
                pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
                pad = pt[-1]
                if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
                    body = pt[:-pad]
                    if all(32 <= b < 127 or b in (9,10,13) for b in body):
                        results.append((f"PBKDF2-{digest}-{iters}-AES{klen*8}", body.decode()))
    return results

def test_pw(pw, label):
    pw_bytes = pw.encode() if isinstance(pw, str) else pw
    forms = [
        (pw_bytes, "raw"),
        (hashlib.sha256(pw_bytes).hexdigest().encode(), "sha256hex"),
        (hashlib.sha256(pw_bytes).digest(), "sha256bin"),
        (hashlib.sha256(pw_bytes).hexdigest().upper().encode(), "sha256hex_upper"),
        (hashlib.md5(pw_bytes).hexdigest().encode(), "md5hex"),
    ]
    for form_bytes, form_name in forms:
        for bname, raw in BLOBS.items():
            hits = try_decrypt(raw, form_bytes)
            for kdf, pt in hits:
                print(f"\n[!!!] HIT  pw={label!r}  form={form_name}  blob={bname}  kdf={kdf}")
                print(f"      PT={pt!r}")
                with open("MATCH.txt", "a") as f:
                    f.write(f"pw={label!r} form={form_name} blob={bname} kdf={kdf}\nPT={pt!r}\n\n")
                return True
    return False

# ── Text sources ───────────────────────────────────────────────────
LAST_WORDS = (
    "the door to your right leads to the source and the salvation of zion "
    "the door to your left leads back to the matrix to her and to the end "
    "of your species the function of the one is now to return to the source"
)
ARCHITECT = (
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
STR_A = "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
INCASE = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"

BLUE_PRIMES   = [2, 3, 7, 11, 13, 17, 23]
YELLOW_PRIMES = [5, 19]
ALL_PRIMES_24 = sorted(BLUE_PRIMES + YELLOW_PRIMES)

def primes_upto(n):
    return [p for p in range(2, n+1) if all(p % i != 0 for i in range(2, p))]

def prime_extract_chars(text, prime_list, offset=0):
    return "".join(text[p - offset] for p in prime_list if 0 <= p - offset < len(text))

def prime_extract_words(text, prime_list, offset=0):
    words = text.split()
    return [words[p - offset] for p in prime_list if 0 <= p - offset < len(words)]

def candidates():
    seen = set()
    def emit(pw, label):
        key = (pw.encode() if isinstance(pw, str) else pw).hex()
        if key not in seen:
            seen.add(key)
            yield pw, label

    words_lw = LAST_WORDS.split()

    # ── 1. Blue/yellow prime word extractions ─────────────────────
    blue_w   = prime_extract_words(LAST_WORDS, BLUE_PRIMES, offset=0)
    yellow_w = prime_extract_words(LAST_WORDS, YELLOW_PRIMES, offset=0)
    all_w    = prime_extract_words(LAST_WORDS, ALL_PRIMES_24, offset=0)

    for name, wlist in [("blue_w", blue_w), ("yellow_w", yellow_w), ("all_w", all_w),
                         ("blue_then_yellow", blue_w+yellow_w),
                         ("yellow_then_blue", yellow_w+blue_w)]:
        for sep in ["", " "]:
            pw = sep.join(wlist)
            yield from emit(pw, f"{name} sep={sep!r}")
        yield from emit(" ".join(wlist).upper(), f"{name}_upper")
        yield from emit("".join(wlist).upper(), f"{name}_upper_nospace")

    # 1-indexed versions
    blue_w1   = prime_extract_words(LAST_WORDS, BLUE_PRIMES, offset=1)
    yellow_w1 = prime_extract_words(LAST_WORDS, YELLOW_PRIMES, offset=1)
    all_w1    = prime_extract_words(LAST_WORDS, ALL_PRIMES_24, offset=1)
    for name, wlist in [("blue_w1", blue_w1), ("yellow_w1", yellow_w1), ("all_w1", all_w1)]:
        for sep in ["", " "]:
            yield from emit(sep.join(wlist), f"{name} sep={sep!r}")

    # ── 2. Char-level prime extraction from various texts ─────────
    all_primes_200 = primes_upto(250)
    for text_name, text in [("last_words", LAST_WORDS),
                             ("last_words_nospace", LAST_WORDS.replace(" ", "")),
                             ("last_words_upper", LAST_WORDS.upper().replace(" ", "")),
                             ("architect_nospace", ARCHITECT.replace(" ", "")),
                             ("STR_A", STR_A)]:
        for offset in [0, 1]:
            # All primes up to len(text)
            extract = prime_extract_chars(text, all_primes_200, offset)
            yield from emit(extract, f"char_prime_all/{text_name}/off{offset}")
            # Only blue/yellow primes
            extract_by = prime_extract_chars(text, BLUE_PRIMES, offset)
            extract_yp = prime_extract_chars(text, YELLOW_PRIMES, offset)
            extract_ap = prime_extract_chars(text, ALL_PRIMES_24, offset)
            for pw, n in [(extract_by, "blue"), (extract_yp, "yellow"), (extract_ap, "all24")]:
                yield from emit(pw, f"char_prime_{n}/{text_name}/off{offset}")

    # ── 3. Prime number strings ────────────────────────────────────
    prime_numbers = [
        "8686159", "2518101088543", "86861592518101088543",
        "8686", "86861", "868615", "86861592518",
        "2518101088543 8686159", "8686159 2518101088543",
        str(8686159 + 2518101088543),
        str(8686159 * 2518101088543 % 10**20),
        hex(8686159)[2:], hex(2518101088543)[2:], hex(86861592518101088543)[2:],
    ]
    for pw in prime_numbers:
        yield from emit(pw, f"prime_number:{pw[:20]}")

    # ── 4. Zeroed-out variations ───────────────────────────────────
    # "Some characters need to be zeroed out" — zero non-prime positions
    # In STR_A: keep only prime-indexed chars, rest → 'a' (0 in a=0 scheme)
    zeroed_stra = ''.join(
        c if (i+1) in set(primes_upto(92)) else 'a'
        for i, c in enumerate(STR_A)
    )
    yield from emit(zeroed_stra, "stra_zeroed_nonprime")

    # In last words: keep only prime-indexed chars, zero rest
    zeroed_lw = ''.join(
        c if i in set(all_primes_200) else chr(ord('a'))
        for i, c in enumerate(LAST_WORDS.replace(" ", ""))
    )
    yield from emit(zeroed_lw, "lastwords_zeroed_nonprime")

    # In the 24-position blue/yellow string, zero non-prime positions
    BLUE = {1,2,3,4,6,7,8,11,12,13,14,16,17,20,23}
    YELLOW = {5,9,10,15,18,19,21,22,24}
    pos24 = {i: (1 if i in BLUE else 0) for i in range(1, 25)}
    # zeroed non-prime: positions 1..24, non-prime → 0
    primes24_set = set(ALL_PRIMES_24)
    zeroed24 = "".join(str(pos24[i]) if i in primes24_set else "0" for i in range(1, 25))
    yield from emit(zeroed24, "24pos_zeroed")
    yield from emit(int(zeroed24, 2).to_bytes(3, 'big').decode('latin1'), "24pos_zeroed_bytes")

    # ── 5. Salvation/zion related strings ─────────────────────────
    for pw in ["salvation", "zion", "salvationzion", "salvationofzion",
               "thesalvationofzion", "the salvation of zion",
               "yingyang", "yinyang", "ying yang", "yin yang",
               "cosmicduality", "cosmic duality", "CosmicDuality",
               "SalPhaseIon", "salphaseion", "SALPHASEION",
               "salvationyingyang", "yingyangsalvation",
               "YOUWON", "youwon", "YOUWONsalvation",
               "btcseed", "BTCSEED",
               "matrixsalvation", "salvationmatrix",
               "leftright", "rightleft", "twodoors", "two doors",
               "thedoor", "twodoor"]:
        yield from emit(pw, f"keyword:{pw}")

    # ── 6. SHA256 of key phrases ───────────────────────────────────
    for phrase in ["follow the white rabbit", "followthewhiterabbit",
                   "our first hint is your last command",
                   "ourfirsthintisyourlastcommand",
                   "the matrix has you", "thematrixhasyou",
                   "there is another door", "thereisanotherdoor",
                   "reinserting the prime basics",
                   "reinsertingtheprimebasics",
                   "lastwordsbeforearchichoice",
                   "thispassword", "matrixsumlist",
                   "enter", "ans too", "anstoo",
                   "the door to your right", "thedoortoyourright",
                   "the source and the salvation of zion",
                   "toyourthesalvationzionyourmatrix",
                   "".join(blue_w), " ".join(blue_w)]:
        pw_sha = hashlib.sha256(phrase.encode()).hexdigest()
        yield from emit(phrase, f"phrase:{phrase[:25]}")
        yield from emit(pw_sha, f"sha256:{phrase[:20]}")
        yield from emit(pw_sha.upper(), f"sha256_upper:{phrase[:15]}")

    # ── 7. N-gram word search of architect speech + last words ─────
    for text in (ARCHITECT, LAST_WORDS,
                 ARCHITECT + " " + LAST_WORDS,
                 LAST_WORDS + " " + ARCHITECT):
        w = text.split()
        for i in range(len(w)):
            for n in range(1, 10):
                if i + n > len(w): break
                phrase = " ".join(w[i:i+n])
                yield from emit(phrase, f"ngram:{phrase[:20]}")
                yield from emit(phrase.replace(" ", ""), f"ngram_nospace:{phrase[:20]}")

    # ── 8. Matrix row/col sums ─────────────────────────────────────
    MATRIX_ROWS_STR = [
        "00110b0010110y", "11b1001110b011", "1101110b001001",
        "0110b000011101", "0b1000110y0110", "100110y010y011",
        "100b1100010y00", "b11000000010y0", "00011b0111110b",
        "11b111y0110001", "1101000y011011", "11110010b01100",
        "0b0111010y0110", "01b0110110b011",
    ]
    for y, b in [(0,1), (5,2), (19,2), (5,3)]:
        grid = [[{'0':0,'1':1,'y':y,'b':b}[c] for c in row] for row in MATRIX_ROWS_STR]
        row_s = [sum(r) for r in grid]
        col_s = [sum(grid[r][c] for r in range(14)) for c in range(14)]
        for slist, name in [(row_s,"row"), (col_s,"col"), (row_s+col_s,"both")]:
            for sep in ["", ",", " "]:
                yield from emit(sep.join(str(x) for x in slist), f"matrix_{name}_y{y}b{b}_{sep!r}")
            yield from emit(bytes(slist), f"matrix_{name}_bytes_y{y}b{b}")

    # ── 9. OTP output segments ────────────────────────────────────
    # The 64-char OTP tail (after YOUWON)
    OTP_TAIL = "XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA"
    OTP_21   = "VOZIJBDTIQBRGVEOMZNBC"
    YOUWON_SEG = "YOUWON"
    for pw in [OTP_TAIL, OTP_21, OTP_TAIL.lower(), OTP_21.lower(),
               OTP_21+OTP_TAIL, YOUWON_SEG+OTP_TAIL,
               prime_extract_chars(OTP_TAIL, all_primes_200, 0),
               prime_extract_chars(OTP_TAIL, all_primes_200, 1),
               prime_extract_chars(OTP_TAIL, ALL_PRIMES_24, 0),
               prime_extract_chars(OTP_TAIL, BLUE_PRIMES, 0)]:
        yield from emit(pw, f"otp:{pw[:20]}")

    # ── 10. INCASE prime extraction ───────────────────────────────
    for offset in [0, 1]:
        extract = prime_extract_chars(INCASE, primes_upto(len(INCASE)), offset)
        yield from emit(extract, f"incase_primes_off{offset}")
        extract24 = prime_extract_chars(INCASE, ALL_PRIMES_24, offset)
        yield from emit(extract24, f"incase_primes24_off{offset}")

    # ── 11. Blue-words + SHA256 of other things ───────────────────
    blue_joined = "".join(blue_w)  # "toyourthesalvationzionyourmatrix"
    for pw in [blue_joined, blue_joined.upper(),
               hashlib.sha256(blue_joined.encode()).hexdigest(),
               hashlib.sha256(blue_joined.upper().encode()).hexdigest(),
               "salvation" + blue_joined,
               blue_joined + "salvation",
               blue_joined + YOUWON_SEG,
               YOUWON_SEG + blue_joined,
               blue_joined[:16], blue_joined[:24]]:
        yield from emit(pw, f"blue_based:{str(pw)[:25]}")


def main():
    print("Blobs loaded (both 96B, valid 5-block ct):")
    for n, r in BLOBS.items():
        print(f"  {n}: salt={r[8:16].hex()} ct_len={len(r)-16}")

    total = 0
    for pw, label in candidates():
        total += 1
        if total % 500 == 0:
            print(f"  ... {total} tested", end="\r", flush=True)
        if test_pw(pw, label):
            print(f"\nSolved at candidate #{total}!")
            return

    print(f"\n[done] Tested {total} candidates, no hit.")

if __name__ == "__main__":
    main()
