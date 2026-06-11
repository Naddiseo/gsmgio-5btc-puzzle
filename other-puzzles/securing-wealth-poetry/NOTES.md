# "Securing Wealth in Poetry" — 0.03 BTC Puzzle (UNSOLVED)

A 12-word BIP39 seed is hidden in Trithemius' 2019 Coinmonks/Medium article
*"Securing Wealth in Poetry"*. Whoever reconstructs it controls the wallet.

## Target

- **Address:** `1K4ezpLybootYF23TM4a8Y4NyP7auysnRo` (legacy P2PKH)
- **Balance:** ~0.0312 BTC, 2 txs
- **Author:** Trithemius (pen name; the historical Trithemius wrote *Steganographia*)
- **Published:** 2019-02-11 · **Status:** UNSOLVED
- Author's hint: *"If you've read this far, you've read every word required to
  access a wallet with .03 BTC."* → the seed is embedded in the article text,
  in order, "in plain sight".
- Article text: `assets/article.txt`; full archive: `assets/article-archive.mhtml`.

## The three methods the article describes (and a worked GPS proof)

1. **Null cipher** — take the n-th letter of each word. Article's own example:
   *"Fishing freshwater bends ..."* → 3rd letter of each word → "Send Lawyers,
   Guns, and Money."
2. **Story & phone number** — phone-number digits index word positions. Example
   list given: `(2,6,9,18,22,25,45,70,86,100,113,116)`.
3. **Letter & GPS location** — a landmark's coordinates dictate word positions,
   "every digit read increases by ten."

### GPS rule — REVERSE-ENGINEERED AND VERIFIED ✓

From the article's own example ("U.S. Supreme Court 38.8906° N, 77.0044° W"):
take the **12 significant coordinate digits** `3,8,8,9,0,6,7,7,0,0,4,4` and set

    position_k (1-based word index) = digit_k + 10·k      (k = 0..11)

→ `3,18,28,39,40,56,67,77,80,90,104,114`, which **matches the article's stated
indices exactly**. (`decoder.py` asserts this.) Consequence: with 2-digit-degree
coordinates the 12 positions are all ≤ **119**, so a GPS-hidden seed lives
entirely in the first ~119 words of wherever word-counting starts.

## What's been tried here (all negative so far)

- **Printed "Seed Phrase" example** `witch collapse practice feed shame open
  despair creek road again ice least` → **fails BIP39 checksum**. Definitively a
  decoy, not the wallet seed.
- **GPS method** over starts {body, title, "Revolution"} × tokenizations
  {alpha, alpha+numbers, whitespace}: several decade-windows contain **zero**
  BIP39 words (e.g. words 1–9 "my grandfather known to me as ye-ye was" — none
  are seed words), so **no GPS coordinate can yield 12 valid words** under those
  tokenizations. Where coverage existed, ~93 checksum-valid extractions were
  derived and checked — **none** hit the target.
- **The two explicit example index lists** (story & GPS) applied to the main
  article (base-0 and base-1): no valid seed.
- **Numbers/dates as phone-method positions**: no clean seed.
- **Acrostics** (first letter of each paragraph / sentence) and **per-paragraph
  first words**: no seed.

## Open leads (where a solve likely hides)

1. **Exact tokenization** is the crux: does counting include the title, the
   section headers ("Revolution/Fiat/Bitcoin/..."), image captions, numbers,
   hyphenated tokens ("ye-ye", "well-to-do"), apostrophes? Each choice shifts
   every position. The right convention may make all 12 GPS decades non-empty.
2. **Which landmark?** The narrative's emotional center is the grandfather's
   flight through China (Qingdao) → Taiwan → Canada. A landmark with 2-digit
   lat & lon degrees (so 12 digits total) is required — that excludes mainland
   China longitudes (120°E, 3-digit) but fits e.g. Canadian cities (Toronto
   43.6532°N 79.3832°W) or Taiwan-area points.
3. **Derivation path / wallet type** unknown. `check.py` currently tries
   m/44'/0'/0'/0/0, m/0/0, m/0'/0'/0', m/0, m, compressed+uncompressed P2PKH.
   A 2019 wallet might also be Electrum-seed or a different account index.

## Tooling (all verified)

- `decoder.py` — tokenizers, GPS/phone position math, null-cipher; self-tests
  the GPS rule against the article example.
- `check.py` — derives a candidate mnemonic across common paths and compares to
  the target (coincurve-free ecdsa; cross-checked pipeline).
- `search.py` — broad sweep: example index lists + GPS decade-product + (extend
  with new tokenizations/landmarks).

To extend: add tokenizations/landmarks in `search.py` and rerun. Any valid
12-word BIP39 extraction that derives to the target prints `MATCH`.
