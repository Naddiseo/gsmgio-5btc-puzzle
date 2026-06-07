"""EXPERIMENTAL password sweep against the two final AES blobs.
All results below are NEGATIVE so far (documented for the record)."""
import itertools, hashlib
from gsmg_toolkit import AES_PHASE32, AES_SALPHASEION, try_password, looks_like_plaintext

BLOBS = {"phase3.2": AES_PHASE32, "salphaseion": AES_SALPHASEION}

# Tokens grouped by the 2023-02-23 recipe slot. Each slot lists candidate spellings.
SLOTS = {
    "yellow": ["", "yellow", "9", "nine", ".thdplntd"],
    "blue":   ["", "blue", "15", "fifteen", "gsmgio/eseeisae"],
    "primes": ["", "primes", "prime"],
    "matrixsumlist": ["", "matrixsumlist"],
    "lastwords": ["", "lastwordsbeforearchichoice"],
    "yinyang": ["", "yinyang", "cosmicduality", "yinandyang"],
    "thepassword": ["", "thispassword", "thepassword", "enter"],
}

def sweep():
    slots = list(SLOTS.values())
    total = 0
    hits = []
    for combo in itertools.product(*slots):
        pw = "".join(combo)
        if not pw:
            continue
        total += 1
        for name, blob in BLOBS.items():
            for md in ("sha256", "md5"):
                pt = try_password(blob, pw, md=md)
                if looks_like_plaintext(pt):
                    hits.append((name, md, pw, pt))
                    print(f"HIT [{name}/{md}] pw={pw!r} -> {pt!r}")
    print(f"tested {total} concatenations x2 blobs x2 KDFs; printable hits: {len(hits)}")
    return hits

# Also: single known plaintext tokens, and a few obvious transforms
SINGLES = [
    "thispassword", "enter", "matrixsumlist", "lastwordsbeforearchichoice",
    "yinyang", "cosmicduality", "thematrixhasyou", "thematrixhasyouenter",
    "ourfirsthintisyourlastcommand", "theseedisplanted",
    "gsmg.io/theseedisplanted", "thismatrixhasyou",
]

def singles():
    for pw in SINGLES:
        for name, blob in BLOBS.items():
            for md in ("sha256", "md5"):
                pt = try_password(blob, pw, md=md)
                if looks_like_plaintext(pt):
                    print(f"SINGLE HIT [{name}/{md}] pw={pw!r} -> {pt!r}")
    print("singles done")

if __name__ == "__main__":
    singles()
    sweep()
