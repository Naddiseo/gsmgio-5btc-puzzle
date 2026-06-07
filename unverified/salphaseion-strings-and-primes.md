# SalPhaseIon base-9 strings + the "primes" slot — analysis & negative results

**Status:** unsolved. Records what STR_A / STR_B are, the confirmed value of the
`primes` recipe slot, and the approaches already ruled out.

## The two strings (the real bottleneck)

Both are sequences over the 9 symbols `a–i`, flanking the decoded instruction
`matrixsumlist`:

```
… STR_A (91) …  [binary → "matrixsumlist"]  … STR_B (570) …  z…z…z  "our first hint is your last command"
```

- **STR_A** — 91 chars, **skewed** distribution → looks like a *message*:
  `b=25 e=18 f=10 g=10 c=8 h=8 i=5 d=4 a=3`
- **STR_B** — 570 chars, roughly **uniform** → looks like *keystream/ciphertext*.

Constants: `SALPH_STR_A`, `SALPH_STR_B` in `solver/gsmg_toolkit.py`.

## Confirmed: `primes` = {2, 3, 5, 7}

From the 2021-03-01 Telegram hint (`hints/2021-03-01-primes.png`):

> "just say which **primes 2,3,5,7** we need use"
> Jrk: "You are at the **prime part** already???"
> "there are too many combinations :("
> Jrk: "Oh wait, shouldn't have said that. That might have been a hint"

And 2023-01-09 (`hints/2023-01-09-prime-number.png`):
> "At least prime number is very important to get any further."

So the `primes` slot is built from the single-digit primes **2, 3, 5, 7**, and the
difficulty is *which arrangement/subset* ("too many combinations").

### Suggestive overlap with STR_A
Mapping `a..i = 1..9`, the prime digits are `b=2, c=3, e=5, g=7`. These are
**exactly the most frequent symbols in STR_A** (b,e,g,c). The non-prime digits
(a=1,d=4,f=6,h=8,i=9) are the rare ones. This strongly suggests STR_A is meant to
be read through a prime/non-prime lens — e.g. a straddling-checkerboard (as used
in the Phase 3.2 VIC cipher) where 2,3,5,7 act as prefix digits, or where
prime-valued digits are data and the rest are separators. **Not yet cracked.**

The speech (Phase 3.2) reinforces this: *"reinserting the prime basics … select
from over twentythree ciphers sixteen encryptions and or **seven** intertwined
passwords"* — and the 2023-02-23 recipe has exactly **7** components
(yellow, blue, primes, matrixsumlist, lastwordsbeforearchichoice, yinyang,
thepassword) = the "seven intertwined passwords".

## Approaches ruled out (all in `solver/`)

- **141 transformations** of STR_A/STR_B (`strab_sweep.py`): base-9 → bytes,
  decimal → hex → ascii, digit-pairs → ascii, cumulative sum, consecutive diff,
  matrix row/col sums and column-major transposition for every divisor, and
  duality combinations (STR_A repeated as a key over STR_B, ±mod 9/10). No
  English; none works as an AES password (oracle-checked against both addresses).
- **Primality**: neither string is prime as a decimal or base-9 integer.
- **~16,000 password concatenations** of the recipe slots — including all 24
  permutations of `2357` and yellow=9 / blue=15 / yinyang / matrixsumlist /
  lastwords / thispassword variants — oracle-verified against all three blobs.
  No prize key, no printable plaintext. (`experiments.py`, `focused_sweep.py`.)

## Most promising untried directions

1. **Straddling checkerboard / VIC on STR_A** using 2,3,5,7 as prefix digits
   (same cipher family as Phase 3.2; the alphabet may be one already derived,
   e.g. `fubcdora/lethingkymvpszjqwx.`).
2. STR_A as message + STR_B as a running key under a **non-additive** combiner
   (the yin-yang/duality framing: the two strings are the two halves).
3. STR_A digits as **indices into the Architect speech** (the "in front of your
   eyes" text) — needs the right grouping/offset.
