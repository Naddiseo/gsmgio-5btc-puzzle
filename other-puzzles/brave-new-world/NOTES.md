# "Brave New World" — 0.2 BTC Puzzle (UNSOLVED)

A BIP39 seed passphrase is hidden in the artwork. Whoever reconstructs the
mnemonic controls the wallet.

## Target

- **Address:** `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ` (P2PKH, legacy)
- **Balance:** ~0.201 BTC
- **Start date:** 2020-05-10
- **Status:** UNSOLVED (community has worked it since 2020)
- Image analyzed here: 1600×1200 re-render, no metadata, LSB ~0.5
  (so no usable pixel steganography on *this* copy — the original PNG/source
  would be needed to test stego properly).

## Theme

George Floyd / BLM / "I can't breathe" (05.25.20), COVID masks, 2020 US
election (Trump vs Pence/Biden 11.03.20), Aldous Huxley's *Brave New World*,
Illuminati / Great-Seal imagery. The big "BRAVE NEW WORLD" lettering is built
from micro-text of the **Bitcoin whitepaper** (flavor, not seed words).

## Confirmed hidden text (verified by zooming the image)

| Location | Text | BIP39? |
|---|---|---|
| Red clock hand (behind seal) | **MOON** | yes |
| Gray clock hand | **TOWER** | yes |
| Yellow cursive over chart line (top) | "Order and Stability" | order=yes, stable=yes (stability no) |
| Statue base (Forensically) | "Only **real** Bitcoin" → "Only Bitcoin" | real=yes |
| Floyd chest / Statue neck | "Breathe" | **no** (closest: breeze) |
| Space Needle | "Food" | yes |
| Repeated graffiti | "This" | yes |
| Statue (underlined) | "Subject" | yes |
| BLM / Latin pun | "Black" | yes |
| Statue scroll | `1865 - 202...?` (13th Amendment → ?) | — |

## Ciphers / mottos (decoded)

- **Great Seal (mirror-flipped in image):**
  - Top: `RERUM COGNOSCERE CAUSAS` ("to know the causes of things" — Virgil)
  - Mid: `FIAT IUSTITIA ET PEREAT MUNDUS` ("let justice be done though the world perish")
  - Bottom: `UBI BENE IBI PATRIA` ("where it is well, there is home")
- **Bottom-strip Latin:** `Esse quam videri` ("to be rather than to seem") and
  `... quam niger es, sic dixit caccabus ollae` = **"the pot calling the kettle black"** → reinforces **black**.
- **Runes** (per published hints; multiple alphabets, numbered 1–5):
  1. (top-left) Russian: "I hope that many bitcoins will be sent here"
  2. (bottom-left) Russian: "Сумма двух чисел" = "sum of two numbers"
  3. (above Trump) **Bill Cipher** (Gravity Falls) = "Tuesday"
  4. (long, right edge) Russian: "Here are encrypted bitcoins for a rainy day number X"
  5. ...
  The runes appear to give *instructions/red herrings*, not raw seed words.

## BIP39-valid candidate words gathered so far

`black, brave, breeze(?), clock, day, find, first, flag, food, hope, liberty,
life, matter, moon, more, number, one, only, order, peace, phrase, picture,
police, real, seed, stable, subject, this, tower, two, welcome, world`

(Not all are seed words — many are thematic text. A real BIP39 mnemonic is
12/15/18/21/24 words **in a specific order with a checksum**.)

## Honest assessment

This is a hard, long-unsolved puzzle. The hard part is not *finding* words —
it's knowing **which** ~12 of them, in **what order**. Blind brute force is
infeasible: even a known 12-word set has 12! ≈ 4.8×10⁸ orderings, and the word
set itself is ambiguous. Progress requires the puzzle's own ordering signal
(the rune instructions, the numbers 1–5, the "sum of two numbers", "number X",
the `1865-202?` date) to pin down sequence.

## Feasibility verdict (measured)

- One candidate check (BIP39 seed + a few BIP32 derivations) ≈ **2 ms / core**.
- Orderings of a *single known* 12-word set = 12! = 479,001,600 ≈ **293
  core-hours**. We don't know the exact set, word count, duplicates, or
  passphrase, so blind enumeration is **infeasible** — this is the same wall
  the community has hit for 6 years. `bruteforce.py` is therefore a *targeted*
  checker (fill in fixed words, float only a few unknown slots), not a cracker.
- Confirmed: of 120 orderings of the best current guess, 6 passed the BIP39
  checksum, **none** derived to the target address. So our current word/order
  guess is wrong — as expected.

## Brute-force expected-value verdict (why we stopped)

`fastsearch.py` is correct and fast (coincurve/libsecp256k1, cross-checked
against the documented test-vector address `1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA`).
Measured throughput ~7.5k orderings/sec/core under load. A single *fully known*
12-word set's 12! orderings ≈ **4-8 h wall** on 4 cores (most cost is the
PBKDF2 seed derivation on the ~1/16 checksum-valid orderings, across 6 paths).

But the prior per guessed set is tiny: pool ≈ 15 plausible words, only 9 are
visually confirmed, so 12-word subsets = C(15,12)=455 *if the pool even
contains all true words*. 455 × ~6 h ≈ 100+ days, with no guarantee. So blind
enumeration over guessed sets is **not viable**. The tooling's real role is a
**confirmer**: the instant a human pins the exact word set + clue-derived order,
`fastsearch.py`/`solver.py` verify it in seconds. Also note: the title is
"BRAVE **NEW** WORLD" and "new" is not a BIP39 word — evidence the title words
were chosen for theme, not as seed words.

## What the runes actually contribute (already published)

The runic blocks decode (per community) to *meta-instructions*, NOT new seed
words: "sum of two numbers", "Tuesday", "number X for a rainy day", "I hope
many bitcoins are sent here". Re-decoding them won't yield words — they hint at
**ordering / indices**. The bottleneck is reading the artist's intended order.

## Next steps

1. Decode runes 1–5 precisely (find the exact rune font / substitution).
2. Treat numeric clues (`sum of two numbers`, `number X`, `1865-202?`,
   `Tuesday`) as **word positions / indices**, not seed words.
3. Lock the confirmed words (moon, tower, food, this, subject, real, black,
   order/stable) and use index clues to order them.
4. If a clean 12-word candidate emerges, `solver.py` checks BIP39 checksum and
   derives the address (m/44'/0'/0'/0/0 and legacy m/0/0).
