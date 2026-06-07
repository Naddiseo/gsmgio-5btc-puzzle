"""EXPERIMENTAL password sweep against all three terminal AES blobs, with a
verification oracle: any decrypted plaintext is scanned for private keys that
control the two prize addresses.

All results so far are NEGATIVE (documented for the record). Run:
    python3 experiments.py
"""
import itertools
from gsmg_toolkit import ALL_BLOBS, try_password, looks_like_plaintext
from btc import candidates_from_bytes, check_candidate

# Tokens grouped by the 2023-02-23 recipe slot.
SLOTS = {
    "yellow": ["", "yellow", "9", "nine", ".thdplntd"],
    "blue":   ["", "blue", "15", "fifteen", "gsmgio/eseeisae"],
    "primes": ["", "primes", "prime"],
    "matrixsumlist": ["", "matrixsumlist"],
    "lastwords": ["", "lastwordsbeforearchichoice"],
    "yinyang": ["", "yinyang", "cosmicduality", "yinandyang"],
    "thepassword": ["", "thispassword", "thepassword", "enter"],
}

SINGLES = [
    "thispassword", "enter", "matrixsumlist", "lastwordsbeforearchichoice",
    "yinyang", "cosmicduality", "thematrixhasyou", "thematrixhasyouenter",
    "ourfirsthintisyourlastcommand", "theseedisplanted",
    "gsmg.io/theseedisplanted", "thismatrixhasyou",
]


def verify_keys(pt: bytes):
    """If the plaintext contains a key controlling a prize address, report it."""
    for k in candidates_from_bytes(pt):
        hit = check_candidate(k)
        if hit:
            return hit
    return None


def attempt(password):
    """Try a password against every blob/KDF; report printable text or a key hit."""
    found = []
    for name, blob in ALL_BLOBS.items():
        for md in ("sha256", "md5"):
            pt = try_password(blob, password, md=md)
            if pt is None:
                continue
            key_hit = verify_keys(pt)
            if key_hit:
                print(f"*** PRIZE KEY *** blob={name} md={md} pw={password!r} -> {key_hit}")
                found.append((name, md, password, key_hit, pt))
            elif looks_like_plaintext(pt):
                print(f"printable: blob={name} md={md} pw={password!r} -> {pt[:60]!r}")
                found.append((name, md, password, None, pt))
    return found


def run():
    print("== singles ==")
    for pw in SINGLES:
        attempt(pw)
    print("== recipe sweep ==")
    total = 0
    for combo in itertools.product(*SLOTS.values()):
        pw = "".join(combo)
        if pw:
            total += 1
            attempt(pw)
    print(f"swept {total} recipe concatenations across {len(ALL_BLOBS)} blobs x2 KDFs. done.")


if __name__ == "__main__":
    run()
