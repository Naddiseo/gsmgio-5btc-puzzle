# GSMG.IO puzzle — state of the solve & where the frontier is

This document is the "head to toe" map: what is solved, what the exact remaining
unsolved data is, and the most defensible next directions. It complements the
narrative `README.md` (which is the chronological walkthrough + hint archive).

Everything claimed here as *validated* is reproduced by code:
`python3 solver/gsmg_toolkit.py selftest`

---

## 1. The chain, end to end

| Stage | Output | Status |
|-------|--------|--------|
| Phase 0 (image) | `gsmg.io/theseedisplanted` | ✅ validated in code |
| Phase 1 | `theflowerblossoms...` → long URL | ✅ |
| Phase 2 | password → `sha256` decrypts Phase 3 | ✅ |
| Phase 3 | `jacquefresco...principle` → decrypts Phase 3.2 | ✅ validated in code |
| Phase 3.2 EBCDIC+Beaufort | Architect "your life…" speech | ✅ |
| Phase 3.2 VIC | "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF…" | ✅ |
| **Phase 3.2 final AES** | private key? | ❌ unsolved |
| SalPhaseIon (via `sha256` of image text) | several decoded fragments + 1 AES blob + 2 base-9 strings | ⚠️ partial |
| **SalPhaseIon base-9 strings** | ? | ❌ unsolved |
| **SalPhaseIon AES** | private key? | ❌ unsolved |
| Cosmic Duality | ? | ❌ unsolved |

There are **two parallel terminal branches** — the main chain (…→ Phase 3.2) and
SalPhaseIon (reached by hashing the cover image text). The community consensus
(and the creator's hints) is that **SalPhaseIon is the last phase** and Cosmic
Duality is its capstone.

---

## 2. The exact unsolved data (so nobody has to re-derive it)

All of this is in `solver/gsmg_toolkit.py` as named constants.

### 2a. Two AES blobs (one per branch)
See `unverified/final-aes-blobs.md`. Both are AES-256-CBC, decrypt to 64–79
plaintext bytes (private-key sized). Scheme: `passphrase = sha256(password)`.

### 2b. Two SalPhaseIon base-9 strings (`a`–`i`, the real bottleneck)
- `SALPH_STR_A` — 91 chars, **skewed** distribution (b,e,g common; a,d,i rare).
- `SALPH_STR_B` — 570 chars, roughly **uniform** over a–i.

They flank the decoded instruction word **`matrixsumlist`**:

```
… STR_A …  [binary: matrixsumlist]  … STR_B …  z … z … z  "our first hint is your last command"
```

The puzzle's own decoders do **not** crack these:
- `a..i = 1..9 → decimal → hex → ascii` (the method that decodes the `z`-delimited
  sections) yields binary garbage here.
- Treating a–i as base-9 digits, or as digit pairs, → garbage.
- "matrix sum" readings (fold into an R×C matrix for every divisor of 91/570, sum
  rows/cols, map A1Z26 or ascii) → no English. (Swept in code.)

### 2c. Already-decoded SalPhaseIon fragments
`matrixsumlist`, `enter`, `lastwordsbeforearchichoice`, `thispassword`,
`our first hint is your last command`.

---

## 3. The master-password recipe (2023-02-23 official hint)

The binary hint decoded to:

> **yellow blue primes matrix sumlist last words before archichoice yinyang**
> we wont give away **thepassword** its in front of your eyes but youre not
> seeing it — very last step is a true give away promised

Read as an ordered ingredient list for the final password:

| Slot | Resolves to | Confidence |
|------|-------------|-----------|
| `yellow` | **9** (or its spelled/letter forms) | NEW — see below |
| `blue` | **15** (or its spelled/letter forms) | NEW — see below |
| `primes` | a prime number, not yet derived | unknown |
| `matrixsumlist` | result of operating on STR_A/STR_B | unknown |
| `lastwordsbeforearchichoice` | literal string, or the actual last words before Neo's choice | ambiguous |
| `yinyang` | Cosmic Duality token | unknown |
| `thepassword` | "in front of your eyes" — possibly `thispassword` | unknown |

---

## 4. New result: `yellow` and `blue` decoded

Full write-up: `unverified/yellow-blue-2020-hint.md`.

The 2020-01-14 hint ("Yellow has a number and so does Blue. Go back to the first
puzzle piece.") resolves against `puzzle.png`:

- The 14×14 grid's coloured squares are **exactly the 8th bit (LSB) of each of the
  24 bytes** of `gsmg.io/theseedisplanted` — all on multiples of 8.
- Yellow = LSB 0 (even ASCII), Blue = LSB 1 (odd ASCII).
- **Yellow count = 9, Blue count = 15.**

This is the first concrete decoding of the first two recipe slots.

---

## 5. Most promising next directions

1. **Crack `matrixsumlist` over STR_A/STR_B.** This is the linchpin: it both
   unlocks a recipe slot and is the only large undecoded data left. Worth trying:
   columnar transposition keyed by the speech; using STR_A (91, skewed — looks
   like a *message*) as data and STR_B (570, uniform — looks like a *keystream/
   pad*) as a key, or vice-versa; the "matrix" being the 7×13 / 13×7 shape of
   STR_A (note: `matrixsumlist` has 13 letters; 91 = 7×13).
2. **Derive `primes`.** Hints repeatedly stress a prime. Candidates to chase: a
   prime hidden in the speech word/letter counts, or in the grid coordinates.
3. **Re-read the grid as 4 symbols** (white/black/yellow/blue) per "a whole lot
   more", not just binary.
4. **`yinyang` / Cosmic Duality.** Inspect `salphaseion-assets/` and the
   `hints/cosmic-duality-book.png` for the dual/mirror structure (the puzzle
   loves reversal — cf. the 2023-02-23 "reverse binary" hint).

## 6. Reproducing / contributing

```
pip install pillow numpy           # only needed for the image analysis
python3 solver/gsmg_toolkit.py selftest      # confirm all validated steps pass
python3 solver/experiments.py                # re-run the AES password sweep
```

Negative results are valuable here — please add them under `unverified/`.
