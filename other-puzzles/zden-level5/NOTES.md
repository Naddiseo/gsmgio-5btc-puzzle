# Zden Crypto Puzzle — Level 5 (UNSOLVED)

Find the 32-byte private key encoded in the image as 64 rectangle "shells".

## Target

- **Address:** `1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7` (vanity, P2PKH)
- **Balance:** 0.0055555 BTC · **Creator:** Zden (crypto.haluska.sk)
- **Start:** 2018-11-09; **relaunched fixed** 2021-12-12 (our image = the "fix")
- **Hint:** *"Sum of two ~~consecutive~~ following rectangles areas creates one
  byte of the private key. Apply more operations to obtain the results in byte
  range."* Also: *"Byte 0x77 is part of the private key."*

## Image structure (verified)

- 950×950, pure binary (0/255), **no antialiasing** → pixel-exact measurement.
- **64 rectangle shells** in an 8×8 grid. Each shell = Outer rect − Inner rect
  (the white frame). Areas measured; they match the research repo's
  `noLine_A.csv` (e.g. rect 1: outer 6264, inner 3780, shell 2484).
- The 2021 "fix" added: a **17px white line under rect #40**, a **6px line under
  rect #53**, a **mini-puzzle hint box** (bottom-left), and the string
  **`09111819 FIX 11122111`** (bottom).

## The mini-puzzle hint (bottom-left box) — the crux

Drawn as a rectangle shell, containing four lines:
```
 -I
 ✶✖+
 LXIV     (= 64)
 /✖/
```
Best community reading: a formula like `-1 * x + 64 /x/`. This is the "more
operations" that maps the area-sum into byte range — and decoding it exactly is
the unsolved crux. The `09111819 FIX 11122111` string most likely encodes a
known-plaintext (key starts `09 11 18 19`, ends `11 12 21 11`) and/or per-
row/col coefficients (rows `[0,9,1,1,1,8,1,9]`, cols `[1,1,1,2,2,1,1,1]`).

## What prior work (HomelessPhD/Zden_LVL5, in `research/`) tried — all FAILED

- Area types: outer / inner / shell.
- 4 pairing traversals (row pairs; column-stride; mixed). See README.
- Transforms: `%256`, min-max normalization ×255. None hit the address.

## What THIS workspace adds

- `solve.py`  — own CV detection (64 frames) + ordering/pairing/op brute force.
- `solve2.py` — known-plaintext search (match `09111819`/`11122111`): **0/8
  bytes matched** under tested pairings/transforms → either the plaintext
  reading or (more likely) the transform differs.
- `solve3.py` — adds hint-matrix row/col coefficients; 720 interps vs address: none.
- `solve4.py` — **exhaustive sweep of every linear transform** `byte=(m·S+c) %
  {256,255}` over all 4 documented pairings × 3 area types (~1.5M keys),
  verified directly against the address. (Covers the hint's `-1·x+64` and plain
  `%256`.) Result: see below.

## Status / open leads

The bottleneck is the exact "more operations" formula in the hint box. If it is
linear mod 256, `solve4.py` settles it. If not (e.g. division/normalization by a
per-list max, or per-cell coefficients, or the line-length adjustments to rects
#40/#53 matter), the next steps are: (1) incorporate the 17px/6px line
adjustments precisely; (2) treat row/col coefficient vectors as multipliers or
divisors; (3) reconsider whether `0x77` and the prefix/suffix are true plaintext
to pin the transform. All tooling verifies any candidate against the address in
milliseconds.
