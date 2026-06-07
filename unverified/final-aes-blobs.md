# The two final AES blobs — structure & negative results

**Status:** unsolved. This file records structural facts and the password
attempts already ruled out, so they are not endlessly re-tried.

## The two blobs

There are exactly two OpenSSL `Salted__` AES-256-CBC blobs left at the end of the
two terminal branches of the puzzle:

```
# end of Phase 3.2
U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z
gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4

# inside SalPhaseIon
U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
```

## Structural facts

- Both base64 strings are **128 chars → 96 bytes**.
- Layout = `Salted__` (8) + salt (8) + **80 bytes ciphertext**.
- 80 ciphertext bytes ⇒ **64–79 bytes of plaintext** (after PKCS#7 padding).
- A raw Bitcoin private key in hex is **exactly 64 chars**, which pads to 80.
  A WIF key is 51–52 chars. Both fit.
- The Phase 3.2 VIC-cipher line decoded to:
  *"IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER
  HALF AND THEY ALSO NEED FUNDS TO LIVE"* — note **keys**, plural, and the prize
  itself is split across two addresses (1.25 + 3.75 BTC).

**Working hypothesis:** each blob decrypts to one of the two private keys
("half" and "better half").

## Encryption scheme (validated)

Confirmed by reproducing the Phase 3 → 3.2 step:

```
passphrase = sha256_hexdigest(plaintext_password)
openssl aes-256-cbc -a -d            # default KDF = sha256 on modern openssl
```

So a correct guess of the *plaintext* password `P` should make
`try_password(blob, P)` return printable bytes.

## Attempts ruled out (no printable plaintext, both blobs, sha256 & md5 KDF)

- All single decoded tokens: `thispassword`, `enter`, `matrixsumlist`,
  `lastwordsbeforearchichoice`, `yinyang`, `cosmicduality`, `thematrixhasyou`,
  `ourfirsthintisyourlastcommand`, `theseedisplanted`, etc.
- ~4,800 concatenations following the 2023-02-23 recipe slots
  (`yellow|blue|primes|matrixsumlist|lastwords|yinyang|thepassword`),
  with `yellow ∈ {9, nine, yellow, .thdplntd}`, `blue ∈ {15, fifteen, blue,
  gsmgio/eseeisae}`, etc. — see `solver/experiments.py`.

Run them yourself: `python3 solver/experiments.py`

## What's missing to make this tractable

The recipe has slots whose *values* are still unknown:
- **primes** — the "prime part" (hints 2021-03-01, 2023-01-09, 2023-01-12). No
  confirmed prime has been derived from the puzzle data yet.
- **matrixsumlist** — almost certainly an *instruction* operating on the two
  unsolved SalPhaseIon base-9 strings (`SALPH_STR_A`, `SALPH_STR_B`), not a
  literal token. Until those decode, this slot is blank.

Both gaps point back to the **two unsolved base-9 (a–i) strings in SalPhaseIon**
as the real bottleneck. See `ANALYSIS.md`.
