# Exploration log — approaches tried and ruled out

A running record so the same dead ends aren't repeated. Tooling lives in
`solver/`; every claim here is reproducible.

## The endgame, stated precisely

To decrypt the **Cosmic Duality** blob (the final payload) you need one password,
assembled (per the 2023-02-23 hint) from 7 components in order:

`yellow · blue · primes · matrixsumlist · lastwordsbeforearchichoice · yinyang · thepassword`

Resolved values:
- **yellow = 9, blue = 15** (grid LSB counts — reproducible)
- **primes = {2,3,5,7}** (2021-03-01 hint, explicit)
- **lastwordsbeforearchichoice**, **thispassword** — literal decoded strings

Still unknown (the whole ballgame):
- **matrixsumlist** — an operation on the two base-9 strings STR_A/STR_B
- **yinyang** — the Cosmic Duality value
- exact spelling/format of the assembled password

The speech confirms the shape: *"reinserting the prime basics … seven intertwined
passwords … bruteforcing might be required"* — and the recipe has exactly 7 slots.

## Ruled out (this and prior sessions)

| Approach | Tool | Result |
|----------|------|--------|
| Recipe-concatenation passwords, ~16k combos incl. all `2357` perms | `experiments.py`, `focused_sweep.py` | no prize, no printable |
| **In-process mega-sweep**, 372k passwords × 2 passphrase modes × 2 KDFs × 3 blobs | `big_sweep.py` | no prize key, no printable plaintext |
| STR_A/STR_B: 141 numeric/matrix/duality transforms | `strab_sweep.py` | no English, no key |
| STR_A/STR_B: VIC straddling checkerboard, prime prefixes, both digit maps, reversed | `checkerboard.py` | no English (convention validated on phase 3.2) |
| STR_A/STR_B: primality bitmask; "zero out" prime/nonprime digits/indices then decimal→hex→ascii; zero each single/pair of letters | inline | no ASCII |
| STR_A/STR_B: primality of decimal & base-9 integers | inline | not prime |
| Grid "second door": spiral cw/ccw, row/col-major, boustrophedon × 5 colour→bit maps × reversal × 8 offsets | inline | only the known `gsmg.io/theseedisplanted` |
| First-hint-derived passwords (9/15/2357 combos, roses poem, image text hash) | inline | no prize |

## Hints newly mined this session

- **2021-12-25**: "prime numbers … required" and *"some characters need to be
  'zeroed out'"*. Tested the obvious zeroing schemes on STR_A/STR_B — negative.
  Interpretation still open (may apply to assembly, not the strings).
- **2021-12-02 / 2020-08-02**: "There is another **DOOR**" — implies a second
  message in the first image. Simple re-readings of the grid don't reveal one.
- **2023-01-12**: "theory of everything … is a valid path."
- **2024-04-10**: "1357 blocks to go" (note the odd digits 1,3,5,7).

## Where the wall is

Every path funnels to **decoding STR_A/STR_B** (the `matrixsumlist` step). All
mechanical/brute approaches fail, which is consistent with it needing a *key* (an
alphabet/phrase) that hasn't been located in the puzzle, rather than a
transformation that can be searched. That key — or the analogous "fubcd-king…"
phrase that defined the Phase 3.2 alphabet — is the thing to hunt next.
