#!/usr/bin/env python3
"""
Targeted attack using prime-derived material from Phase 0.

Key untested hypotheses:
1. Prime numbers 8686159 / 2518101088543 / combined as AES passwords
2. Prime-indexed character extraction from "last words" speech
3. Matrix sum list → key derivation
4. VIC number sequence as password material
5. Yellow/blue prime positions as key indices into STR_A or bifid tail
"""
import base64, hashlib, itertools
from Crypto.Cipher import AES

# ── AES blob (SalPhaseIon) ─────────────────────────────────────────
AES1 = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9"
AES2 = "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"

# ── AES blob (Phase 3.2) ───────────────────────────────────────────
P32_1 = "U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P32_2 = "gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"

def b64fix(s):
    return s + "=" * (-len(s) % 4)

def get_blobs():
    blobs = {}
    blobs['salph']  = base64.b64decode(b64fix(AES1+AES2), validate=False)
    blobs['p32']    = base64.b64decode(b64fix(P32_1+P32_2), validate=False)
    blobs['salph1'] = base64.b64decode(b64fix(AES1), validate=False)
    blobs['p32_1']  = base64.b64decode(b64fix(P32_1), validate=False)
    return blobs

def evp_bytestokey(pw, salt, klen, ivlen, md=hashlib.md5):
    d = b""; prev = b""
    while len(d) < klen + ivlen:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:klen], d[klen:klen+ivlen]

def good_decrypt(raw, pw_bytes):
    """Try multiple KDFs/keylens. Return list of (label, plaintext) hits."""
    if raw[:8] != b"Salted__": return []
    salt, ct = raw[8:16], raw[16:]
    if len(ct) % 16: return []
    hits = []
    for klen in (32, 16):
        for md in (hashlib.md5, hashlib.sha256):
            key, iv = evp_bytestokey(pw_bytes, salt, klen, 16, md)
            pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
            pad = pt[-1]
            if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
                body = pt[:-pad]
                if all(32 <= b < 127 or b in (9,10,13) for b in body):
                    hits.append((f"EVP-{md().name}-AES{klen*8}", body.decode()))
    # PBKDF2
    for klen in (32, 16):
        for digest in ('sha256', 'sha512', 'md5'):
            for iters in (1, 1000, 10000):
                dk = hashlib.pbkdf2_hmac(digest, pw_bytes, salt, iters, dklen=klen+16)
                key, iv = dk[:klen], dk[klen:klen+16]
                pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
                pad = pt[-1]
                if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
                    body = pt[:-pad]
                    if all(32 <= b < 127 or b in (9,10,13) for b in body):
                        hits.append((f"PBKDF2-{digest}-{iters}-AES{klen*8}", body.decode()))
    return hits

def test_password(pw, label, blobs):
    forms = [
        (pw.encode() if isinstance(pw, str) else pw, "raw"),
        (hashlib.sha256((pw.encode() if isinstance(pw, str) else pw)).hexdigest().encode(), "sha256hex"),
        (hashlib.sha256((pw.encode() if isinstance(pw, str) else pw)).digest(), "sha256raw"),
        (hashlib.md5((pw.encode() if isinstance(pw, str) else pw)).hexdigest().encode(), "md5hex"),
    ]
    for pw_bytes, form in forms:
        for blob_name, raw in blobs.items():
            hits = good_decrypt(raw, pw_bytes)
            if hits:
                for kdf, pt in hits:
                    print(f"\n[!!!] HIT  label={label!r}  form={form}  blob={blob_name}  kdf={kdf}")
                    print(f"      PT = {pt!r}")
                    with open("MATCH.txt","a") as f:
                        f.write(f"label={label!r} form={form} blob={blob_name} kdf={kdf}\nPT={pt!r}\n\n")
                return True
    return False

# ── 14×14 matrix ──────────────────────────────────────────────────
MATRIX_ROWS = [
    "00110b0010110y",
    "11b1001110b011",
    "1101110b001001",
    "0110b000011101",
    "0b1000110y0110",
    "100110y010y011",
    "100b1100010y00",
    "b11000000010y0",
    "00011b0111110b",
    "11b111y0110001",
    "1101000y011011",
    "11110010b01100",
    "0b0111010y0110",
    "01b0110110b011",
]

def matrix_sums(y_val, b_val):
    """Compute row sums and col sums with given yellow/blue values."""
    grid = []
    for row in MATRIX_ROWS:
        r = []
        for c in row:
            if c == '0': r.append(0)
            elif c == '1': r.append(1)
            elif c == 'y': r.append(y_val)
            elif c == 'b': r.append(b_val)
        grid.append(r)
    row_sums = [sum(r) for r in grid]
    col_sums = [sum(grid[r][c] for r in range(14)) for c in range(14)]
    return row_sums, col_sums

def matrix_spiral_values(y_val, b_val):
    """Return the full spiral sequence with numeric values."""
    rows = [list(r) for r in MATRIX_ROWS]

    def cell_val(c):
        if c == '0': return 0
        if c == '1': return 1
        if c == 'y': return y_val
        if c == 'b': return b_val

    def top(arr):
        return [cell_val(c) for c in reversed(arr[0])], arr[1:]
    def left(arr):
        out = [cell_val(r[0]) for r in arr]
        return out, [r[1:] for r in arr]
    def bottom(arr):
        return [cell_val(c) for c in arr[-1]], arr[:-1]
    def right(arr):
        out = [cell_val(r[-1]) for r in arr]
        return list(reversed(out)), [r[:-1] for r in arr]

    ordering = [left, bottom, right, top]
    out = []
    while rows and rows[0]:
        for fn in ordering:
            if not rows or not rows[0]: break
            vals, rows = fn(rows)
            out.extend(vals)
    return out

# ── Texts for prime indexing ───────────────────────────────────────
LAST_WORDS = (
    "the door to your right leads to the source and the salvation of zion "
    "the door to your left leads back to the matrix to her and to the end "
    "of your species the function of the one is now to return to the source"
)

ARCHITECT_FULL = (
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

VIC_NUMBER = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"

STR_A = "dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"

INCASE = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"

def isprime(n):
    n = int(n)
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    i = 3
    while i*i <= n:
        if n % i == 0: return False
        i += 2
    return True

def primes_upto(n):
    return [p for p in range(2, n+1) if isprime(p)]

def prime_index_extract(text, primes, offset=0):
    """Extract characters at prime positions (offset=0 for 0-indexed, 1 for 1-indexed)."""
    result = []
    for p in primes:
        idx = p - offset
        if 0 <= idx < len(text):
            result.append(text[idx])
    return "".join(result)

def main():
    print("Loading AES blobs...")
    blobs = get_blobs()
    for name, raw in blobs.items():
        print(f"  {name}: {len(raw)}B salted={raw[:8]==b'Salted__'}")

    tested = 0

    # ── Section 1: Direct prime numbers as passwords ───────────────
    print("\n[1] Testing prime number strings as passwords...")
    prime_pws = [
        "8686159",
        "2518101088543",
        "86861592518101088543",
        "86 86 15 9",
        "8686 15 9",
        "8686159 2518101088543",
        # with underscores / separators
        "8686159_2518101088543",
        # reversed
        "9516868",
        "3458010815122",
        # square of combinations
        "86861592518101088543"[:32],
    ]
    for pw in prime_pws:
        tested += 1
        if test_password(pw, f"prime_number:{pw[:20]}", blobs):
            return

    # ── Section 2: VIC number sequence ────────────────────────────
    print("[2] Testing VIC number sequence as password...")
    vic_forms = [
        VIC_NUMBER,
        VIC_NUMBER[:32],
        VIC_NUMBER[:16],
        VIC_NUMBER[:64],
        str(int(VIC_NUMBER) % (2**256)),
    ]
    for pw in vic_forms:
        tested += 1
        if test_password(pw, f"VIC:{pw[:20]}", blobs):
            return

    # ── Section 3: Matrix sum lists ───────────────────────────────
    print("[3] Testing matrix sum lists as passwords...")
    for y_val, b_val in [(0,1), (5,2), (5,3), (9,15), (0,2), (19,2)]:
        row_s, col_s = matrix_sums(y_val, b_val)
        for slist in [row_s, col_s, row_s+col_s]:
            for sep in ['', ',', ' ']:
                pw = sep.join(str(x) for x in slist)
                tested += 1
                if test_password(pw, f"matrix_sum y={y_val} b={b_val}", blobs):
                    return
            # as bytes directly
            pw_b = bytes(slist)
            tested += 1
            if test_password(pw_b, f"matrix_sum_bytes y={y_val} b={b_val}", blobs):
                return

    # ── Section 4: Matrix spiral ──────────────────────────────────
    print("[4] Testing matrix spiral values as passwords...")
    for y_val, b_val in [(0,1), (5,2), (5,3)]:
        spiral = matrix_spiral_values(y_val, b_val)
        # sum of spiral values at prime positions
        prime_vals = [spiral[p-1] for p in primes_upto(len(spiral)) if p <= len(spiral)]
        for slist in [prime_vals, spiral[:24], spiral]:
            for sep in ['', ',']:
                pw = sep.join(str(x) for x in slist)
                tested += 1
                if test_password(pw, f"spiral y={y_val} b={b_val}", blobs):
                    return

    # ── Section 5: Prime-indexed extraction from last words ───────
    print("[5] Prime-indexed extraction from 'last words' speech...")
    primes_200 = primes_upto(250)

    # Try many variations of the speech and indexing
    speech_variants = {
        'with_spaces_0idx': LAST_WORDS,
        'no_spaces_0idx': LAST_WORDS.replace(' ', ''),
        'upper_0idx': LAST_WORDS.upper(),
        'upper_no_spaces': LAST_WORDS.upper().replace(' ', ''),
    }

    for sname, speech in speech_variants.items():
        for offset in [0, 1]:
            primes = [p for p in primes_200 if p - offset < len(speech)]
            extract = prime_index_extract(speech, primes, offset)
            if 'salvation' in extract.lower() or 'ying' in extract.lower() or 'yang' in extract.lower() or 'zion' in extract.lower():
                print(f"  INTERESTING extract ({sname} offset={offset}): {extract!r}")
            # Also test subsets: only primes <= 24 (yellow/blue primes)
            primes24 = primes_upto(24)
            extract24 = prime_index_extract(speech, primes24, offset)

            tested += 1
            if test_password(extract, f"prime_last_words {sname} off={offset}", blobs):
                return
            tested += 1
            if test_password(extract24, f"prime24_last_words {sname} off={offset}", blobs):
                return

    # Try prime-indexed over full architect speech
    for sname, speech in [('arch_spaces', ARCHITECT_FULL), ('arch_nospace', ARCHITECT_FULL.replace(' ',''))]:
        for offset in [0, 1]:
            extract = prime_index_extract(speech, primes_200, offset)
            tested += 1
            if test_password(extract, f"prime_arch {sname} off={offset}", blobs):
                return

    # ── Section 6: Yellow/blue prime positions as key ─────────────
    print("[6] Yellow/blue prime position extractions...")
    BLUE_PRIMES   = {2,3,7,11,13,17,23}
    YELLOW_PRIMES = {5,19}
    ALL_PRIMES_24 = sorted(BLUE_PRIMES | YELLOW_PRIMES)

    # Extract characters from various strings at these prime positions
    for text_name, text in [('STR_A', STR_A), ('INCASE', INCASE),
                             ('last_words_nospace', LAST_WORDS.replace(' ','')),
                             ('last_words', LAST_WORDS),
                             ('arch', ARCHITECT_FULL.replace(' ',''))]:
        for prime_set, pname in [(ALL_PRIMES_24, 'all24'),
                                  (sorted(BLUE_PRIMES), 'blue'),
                                  (sorted(YELLOW_PRIMES), 'yellow')]:
            for offset in [0, 1]:
                extract = prime_index_extract(text, prime_set, offset)
                tested += 1
                if test_password(extract, f"yb_prime {text_name} {pname} off={offset}", blobs):
                    return

    # ── Section 7: 472-char bifid tail prime indexing ─────────────
    print("[7] Prime indexing the bifid tail (472 chars)...")
    BIFID_TAIL = open('/home/user/Bahs/other-puzzles/gsmg-salphaseion/SALPH_bifid_decoded.txt').read().strip()
    # Extract btcseed prefix and tail
    if BIFID_TAIL.startswith('btcseed'):
        tail_start = BIFID_TAIL.index('z') + 1
        tail_472 = BIFID_TAIL[tail_start:]
    else:
        tail_472 = BIFID_TAIL

    for offset in [0, 1]:
        extract_all = prime_index_extract(tail_472, primes_200, offset)
        extract24 = prime_index_extract(tail_472, primes_upto(24), offset)
        tested += 1
        if test_password(extract_all, f"bifid_tail_primes off={offset}", blobs):
            return
        tested += 1
        if test_password(extract24, f"bifid_tail_primes24 off={offset}", blobs):
            return

    # ── Section 8: STR_A prime indexing ───────────────────────────
    print("[8] Prime indexing STR_A (dbbi)...")
    for offset in [0, 1]:
        extract = prime_index_extract(STR_A, primes_upto(91), offset)
        tested += 1
        if test_password(extract, f"STR_A_primes off={offset}", blobs):
            return
        extract_mod26 = ''.join(chr((ord(c)-ord('a')) % 26 + ord('a')) for c in extract)
        tested += 1
        if test_password(extract_mod26, f"STR_A_primes_mod off={offset}", blobs):
            return

    # ── Section 9: Combined prime numbers with various ops ─────────
    print("[9] Numeric combinations of primes...")
    p1, p2, p3 = 8686159, 2518101088543, 86861592518101088543
    combos = [
        p1 + p2,
        p1 * p2 % (2**256),
        p1 ^ p2,
        str(p1 + p2),
        str(p1 * p2),
        str(p1 ^ p2),
        str(p2 + p3),
        str(p1 * p3 % 10**20),
        # as hex
        hex(p1)[2:],
        hex(p2)[2:],
        hex(p3)[2:],
        hex(p1+p2)[2:],
    ]
    for pw in combos:
        tested += 1
        s = str(pw)
        if test_password(s, f"prime_combo:{s[:20]}", blobs):
            return

    # ── Section 10: "matrixsumlist" as direct encoding ────────────
    print("[10] Matrix sum list as AES key material...")
    # Compute spiral, group into 8s, sum each group
    spiral_01 = matrix_spiral_values(0, 1)  # y=0, b=1
    groups_of_8 = [spiral_01[i:i+8] for i in range(0, 192, 8)]
    group_sums = [sum(g) for g in groups_of_8]  # 24 values, each 0-8

    # These 24 sums as a "list"
    for sep in ['', ',', ' ', '-']:
        pw = sep.join(str(x) for x in group_sums)
        tested += 1
        if test_password(pw, f"group_sums8 sep={sep!r}", blobs):
            return

    # Use only prime-indexed group sums (positions 2,3,5,7,...,23 from 24 groups)
    prime_group_sums = [group_sums[p-1] for p in primes_upto(24) if p <= 24]
    for sep in ['', ',']:
        pw = sep.join(str(x) for x in prime_group_sums)
        tested += 1
        if test_password(pw, f"prime_group_sums sep={sep!r}", blobs):
            return

    # As bytes
    pw_b = bytes(group_sums)
    tested += 1
    if test_password(pw_b, "group_sums_bytes", blobs):
        return
    pw_b = bytes(prime_group_sums)
    tested += 1
    if test_password(pw_b, "prime_group_sums_bytes", blobs):
        return

    # ── Section 11: "last words" word-level prime indexing ────────
    print("[11] Word-level prime indexing of last words...")
    words = LAST_WORDS.split()
    print(f"  Last words has {len(words)} words")
    for offset in [0, 1]:
        prime_words = [words[p-offset] for p in primes_upto(len(words)) if 0 <= p-offset < len(words)]
        pw_joined = ''.join(prime_words)
        pw_spaced = ' '.join(prime_words)
        print(f"  offset={offset} prime words: {prime_words[:8]}...")
        tested += 1
        if test_password(pw_joined, f"word_prime off={offset}", blobs):
            return
        tested += 1
        if test_password(pw_spaced, f"word_prime_spaced off={offset}", blobs):
            return

    # The specific "salvation" and "ying yang" words
    salv_idx = next((i for i,w in enumerate(words) if w == 'salvation'), -1)
    zion_idx = next((i for i,w in enumerate(words) if w == 'zion'), -1)
    print(f"  'salvation' at word index {salv_idx}, 'zion' at {zion_idx}")

    # What primes are near those indices?
    for radius in [0,1,2,3]:
        near = [words[p] for p in primes_upto(max(salv_idx,zion_idx)+radius+1)
                if 0 <= p < len(words)]
        pw = ''.join(near)
        tested += 1
        if test_password(pw, f"near_salvation off={radius}", blobs):
            return

    # ── Section 12: SHA256 of "ourfirsthint"="followthewhiterabbit" ──
    print("[12] SHA256 variants of 'follow the white rabbit'...")
    fwtm_variants = [
        "follow the white rabbit",
        "followthewhiterabbit",
        "Follow the White Rabbit",
        "FOLLOWTHEWHITERABBIT",
        "follow the white rabbit matrix",
        # SHA256 of these
    ]
    for v in fwtm_variants:
        for pw_form in [v, hashlib.sha256(v.encode()).hexdigest(),
                        hashlib.sha256(v.encode()).hexdigest().upper(),
                        hashlib.sha256(v.encode()).digest()]:
            tested += 1
            if test_password(pw_form, f"fwtr:{str(pw_form)[:20]}", blobs):
                return

    # ── Section 13: SHA256("our first hint is your last command") ─
    print("[13] SHA256(hint phrase)...")
    hints = [
        "our first hint is your last command",
        "ourfirsthintisyourlastcommand",
    ]
    for h in hints:
        for pw_form in [h, hashlib.sha256(h.encode()).hexdigest(),
                        hashlib.sha256(h.encode()).hexdigest().upper()]:
            tested += 1
            if test_password(pw_form, f"hint:{str(pw_form)[:25]}", blobs):
                return

    print(f"\n[done] Tested {tested} password candidates across 2 blobs. No hit.")

if __name__ == "__main__":
    main()
