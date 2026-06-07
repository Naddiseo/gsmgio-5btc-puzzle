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
- **`experiments.py`** — the recipe-driven AES password sweep (currently all
  negative; see `../unverified/final-aes-blobs.md`).

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
