# solver/ — reproducible toolkit

A small, dependency-light toolkit for the GSMG.IO puzzle. AES is done through the
`openssl` CLI (exactly how the puzzle was encrypted), so nothing here needs the
often-broken `cryptography` wheel.

## Files

- **`gsmg_toolkit.py`** — validated decoders + the known puzzle data as constants.
  - `decode_phase0(read_grid())` → `gsmg.io/theseedisplanted`
  - `analyze_colors(grid)` → the yellow/blue (9/15, LSB) result
  - `abba_to_ascii`, `aio_decimal_to_ascii` → SalPhaseIon fragment decoders
  - `try_password(blob, password)` → AES attempt using the creator's scheme
    (`passphrase = sha256(password)`, `aes-256-cbc -a -d`)
  - constants: `AES_PHASE32`, `AES_SALPHASEION`, `SALPH_STR_A`, `SALPH_STR_B`
- **`btc.py`** — verification oracle. Pure-Python secp256k1 → P2PKH address, plus
  helpers to pull candidate keys (64-hex / WIF / raw 32-byte) out of a plaintext
  and check them against the two prize addresses. `python3 btc.py` runs its own
  test vectors.
- **`experiments.py`** — recipe-driven AES password sweep across all three blobs,
  with every result run through the oracle (currently all negative; see
  `../unverified/final-aes-blobs.md`).
- **`checkerboard.py`** — straddling-checkerboard / VIC decoder. Reproduces the
  Phase 3.2 VIC exactly (prefixes (1,4) = "one for one, four for one"). Ruled out
  for STR_A/STR_B with prime prefixes.
- **`focused_sweep.py`** — narrower sweep using the confirmed prime set {2,3,5,7}
  (all permutations) and yinyang/duality values, oracle-verified.
- **`strab_sweep.py`** — transformation sweep of the two unsolved base-9 strings
  STR_A/STR_B (base conversions, matrix sums, duality combiners), each candidate
  scored for English and tried as an AES password. See
  `../unverified/salphaseion-strings-and-primes.md`.

## Quick start

```bash
pip install pillow numpy                  # only for read_grid() image analysis
python3 solver/gsmg_toolkit.py selftest   # all checks should print PASS
python3 solver/experiments.py             # AES sweep
```

`selftest` is the contract: it re-derives every *known-solved* step from raw
data, so if it passes you can trust the constants and the AES scheme before
throwing new ideas at the unsolved parts.

## The unsolved frontier in one line

Decode `SALPH_STR_A` / `SALPH_STR_B` under the `matrixsumlist` instruction →
fills the recipe → builds the password for the two AES blobs (the two private
keys). See `../ANALYSIS.md`.
