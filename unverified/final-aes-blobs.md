# The final AES blobs — structure & negative results

**Status:** unsolved. This file records structural facts and the password
attempts already ruled out, so they are not endlessly re-tried.

## The three blobs

There are three OpenSSL `Salted__` AES-256-CBC blobs at the terminal stages:

```
# end of Phase 3.2 (80 ct bytes)
U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z
gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4

# inside SalPhaseIon (80 ct bytes)
U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ

# "Cosmic Duality" header on the SalPhaseIon page (1328 ct bytes) -- the big one
# full text: ../cosmic-duality-assets/cosmic-duality-aes.txt
U2FsdGVkX18tP2/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFe ...
```

## Structural facts

- The two small blobs are **128 chars → 96 bytes**:
  `Salted__` (8) + salt (8) + **80 bytes ciphertext** ⇒ 64–79 plaintext bytes.
- **Cosmic Duality** is **1792 chars → 1344 bytes**: `Salted__` + salt +
  **1328 ct bytes** (83 AES blocks). Big enough for a message *and* both keys —
  this is the most likely final container.
- A raw Bitcoin private key in hex is **exactly 64 chars**, which pads to 80.
  A WIF key is 51–52 chars. Both fit the small blobs.
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

## Verification oracle (new)

The destination addresses are known, so we don't have to guess whether a
decryption "looks right": derive the address from any candidate key and compare.

- `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` — "half"
- `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` — "better half"

`solver/btc.py` implements pure-Python secp256k1 → P2PKH and scans a plaintext
for 64-hex / WIF / raw-32-byte keys, checking each against both addresses (both
compressed and uncompressed). `solver/experiments.py` runs every password attempt
through this oracle automatically.

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
