# Decoding the 2020-01-14 "Yellow / Blue have a number" hint

**Status:** structurally verified (reproducible from `puzzle.png`), interpretation
of *what the numbers mean for the final password* is still open.

Reproduce with: `python3 solver/gsmg_toolkit.py selftest`

## The hint

> Roses are White but often Red.
> **Yellow has a number and so does Blue.**
> Go back to the first puzzle piece without further ado.
> It might have shown you only one door, beware that the rabbits nest may contain a whole lot more.

## What the colours actually are

The phase-0 image is a **14×14 grid (196 squares)**. Read as a counter-clockwise,
outside-in spiral (top-left, going down first), with `white/yellow = 0` and
`black/blue = 1`, eight squares per byte, it yields the 24-byte string
`gsmg.io/theseedisplanted` (the bunny occupies the 4 centre squares, which fall
into the ignored 4-bit tail). This is fully reproduced in code, so the grid
extraction is trustworthy.

The new observation: **every yellow and every blue square sits on a position that
is an exact multiple of 8** — i.e. each coloured square is the *8th (least
significant) bit of a byte*. There are 24 bytes and exactly 24 coloured squares
(9 yellow + 15 blue), one per character.

The colour encodes that LSB:
- **Yellow = LSB 0** → the character's ASCII code is **even**
- **Blue = LSB 1** → the character's ASCII code is **odd**

| char | g | s | m | g | . | i | o | / | t | h | e | s | e | e | d | i | s | p | l | a | n | t | e | d |
|------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| colour | U | U | U | U | Y | U | U | U | Y | Y | U | U | U | U | Y | U | U | Y | Y | U | Y | Y | U | Y |

(U = blue, Y = yellow.)

## "Yellow has a number and so does Blue"

The most literal reading of the hint:

- **Yellow's number = 9** (count of even-ASCII characters)
- **Blue's number = 15** (count of odd-ASCII characters)

Other candidate "numbers" the same data gives, kept for completeness:

- Yellow-marked characters, in order: `.thdplntd`
- Blue-marked characters, in order: `gsmgio/eseeisae`
- Byte indices marked yellow: `5, 9, 10, 15, 18, 19, 21, 22, 24`
- Byte indices marked blue: `1, 2, 3, 4, 6, 7, 8, 11, 12, 13, 14, 16, 17, 20, 23`
- The 24-bit parity word (blue=1): `1111 0111 0011 1101 1001 0010`
  = `0xF73D92` = `16203666` (this is just the parities of the URL, so it carries
  no information beyond the URL itself).

## Why this matters

The 2023-02-23 official hint spells out the final-password recipe and it **begins
with these two tokens**:

> **yellow blue** primes matrix sumlist last words before archichoice yinyang
> we wont give away thepassword its in front of your eyes but youre not seeing it

So `yellow` and `blue` are the first two ingredients of the master password, and
this is the first concrete decoding of what those tokens resolve to. The leading
hypotheses to test are that they contribute `9`/`15`, `nine`/`fifteen`, or the
extracted letter-runs above.

## Open question

The colours are *redundant* with the URL (they only re-state each character's
parity). So either:
1. the intended payload really is just the two counts (9 and 15), or
2. "the rabbits nest may contain a whole lot more" points at a **different,
   non-binary re-reading** of the same grid (e.g. treating white/black/yellow/blue
   as four symbols / base-4), which has not yet produced anything legible.
