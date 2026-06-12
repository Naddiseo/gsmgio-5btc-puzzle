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
| **Cosmic Duality AES** (1328 ct bytes) | the two private keys? | ❌ unsolved — the main target |

There are **two parallel terminal branches** — the main chain (…→ Phase 3.2) and
SalPhaseIon (reached by hashing the cover image text). The community consensus
(and the creator's hints) is that **SalPhaseIon is the last phase** and Cosmic
Duality is its capstone.

---

## 2. The exact unsolved data (so nobody has to re-derive it)

All of this is in `solver/gsmg_toolkit.py` as named constants.

### 2a. Three AES blobs
See `unverified/final-aes-blobs.md`. All AES-256-CBC, scheme
`passphrase = sha256(password)`:
- `AES_PHASE32` and `AES_SALPHASEION` — 80 ct bytes each (private-key sized).
- `AES_COSMIC_DUALITY` — **1328 ct bytes**, the large blob under the "Cosmic
  Duality" header on the SalPhaseIon page. The likely final payload (message +
  both keys). Captured in `cosmic-duality-assets/cosmic-duality-aes.txt`.

**Verification oracle:** the two destination addresses are known
(`1GSMG…` / `17ucy…`), so any candidate private key in a decrypted blob can be
confirmed immediately — `solver/btc.py` derives the address from a key and checks
it. This turns "does this password work?" from a guess into a definitive test.

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
| `yellow` | **9** (grid colour count) | decoded — see §4 |
| `blue` | **15** (grid colour count) | decoded — see §4 |
| `primes` | an arrangement of **{2, 3, 5, 7}** | set confirmed by hint; arrangement unknown |
| `matrixsumlist` | **40585734329412479690520338541901772425587069158131163878976** — the phase-0 grid as a 196-bit number with the 4 bunny squares zeroed ("four zeros omitted") | **value confirmed** (`solver/matrix_value.py`); how it enters the password is unknown |
| `lastwordsbeforearchichoice` | literal string, or the Architect's two-door / "salvation of Zion" speech | ambiguous |
| `yinyang` | Cosmic Duality (yin-yang of two galaxies = light/dark = yellow/blue). **The creator's single confirmed unlock** ("once you hit a yin-yang, solved in 2 h") — unreached by anyone | unknown |
| `thepassword` | "in front of your eyes" — the assembled result | unknown |

The Phase 3.2 speech names the structure: *"reinserting the prime basics … seven
intertwined passwords"* — and the recipe has exactly **7** slots.

**Anchor (Jrk confirmed): the prize is a *regular Bitcoin private key*** — a random
256-bit value, so it is *stored encrypted* in a blob, not derived from a
passphrase. The recipe password decrypts that blob → the 64-hex key, verifiable
against the two vanity addresses via `solver/btc.py`.

**Status of the assembly:** every concatenation of the known/candidate values
(literal names, the matrix number, all primes arrangements, every yinyang
spelling) has been tested against all three blobs, both KDFs, both passphrase
modes, and oracle-checked — **all negative**. So either `yinyang` ≠ a literal
word, or the assembly is non-trivial. `yinyang` is the one missing lever.

Details: `unverified/salphaseion-strings-and-primes.md`, `telegram-intel.md`.

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

1. **Crack `matrixsumlist` over STR_A/STR_B.** This is the linchpin. STR_A's
   frequent digits are exactly the primes 2,3,5,7 (b,c,e,g), so the strongest
   untried lead is a **straddling-checkerboard / VIC** read (same family as Phase
   3.2) with 2,3,5,7 as prefix digits. Also: STR_A (message) + STR_B (keystream)
   under a non-additive combiner; the 7×13 / 13×7 shape of STR_A (`matrixsumlist`
   has 13 letters; 91 = 7×13). See `unverified/salphaseion-strings-and-primes.md`.
2. **`primes` = {2,3,5,7}** is confirmed; the open question is the *arrangement*
   ("too many combinations"). All 24 permutations of `2357` as a password slot
   are already ruled out, so it likely feeds the cipher in #1 rather than being a
   literal substring.
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
