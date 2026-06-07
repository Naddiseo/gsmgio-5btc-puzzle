"""Focused recipe sweep using the confirmed prime set {2,3,5,7} and the
yinyang/duality values, every result verified against the prize addresses.
sha256 KDF only (the validated scheme)."""
import itertools
from gsmg_toolkit import ALL_BLOBS, try_password, looks_like_plaintext
from btc import candidates_from_bytes, check_candidate
from itertools import permutations

prime_forms = ["", "2357","7532","2,3,5,7","primes","prime",
               "2","3","5","7","23","235"]
prime_forms += ["".join(p) for p in permutations("2357")]  # 24 perms
prime_forms = list(dict.fromkeys(prime_forms))

SLOTS = {
    "yellow": ["", "9", "yellow"],
    "blue":   ["", "15", "blue"],
    "primes": prime_forms,
    "matrixsumlist": ["", "matrixsumlist"],
    "lastwords": ["", "lastwordsbeforearchichoice"],
    "yinyang": ["", "yinyang", "cosmicduality"],
    "thepassword": ["", "thispassword", "thepassword"],
}

def check(pw):
    for name, blob in ALL_BLOBS.items():
        pt = try_password(blob, pw, md="sha256")
        if pt is None: continue
        for k in candidates_from_bytes(pt):
            kh = check_candidate(k)
            if kh:
                print(f"*** PRIZE KEY *** pw={pw!r} blob={name} -> {kh}"); return True
        if looks_like_plaintext(pt):
            print(f"printable pw={pw!r} blob={name} -> {pt[:50]!r}")
    return False

total=0; found=False
for combo in itertools.product(*SLOTS.values()):
    pw="".join(combo)
    if not pw: continue
    total+=1
    if check(pw): found=True
print(f"swept {total} combos (sha256, 3 blobs, oracle-verified). prize found: {found}")
