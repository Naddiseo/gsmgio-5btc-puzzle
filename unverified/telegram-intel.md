# Intel from the creator's Telegram + community chat (2019–2023)

Findings extracted from Jrk Bgrt's (the creator's) messages and the public group
chat. Cross-checked against the data here; **none of this is a solve** — the
puzzle is confirmed still open ("Did anyone find yingyang? I don't think so").

## Confirmed by the creator

- **"Once you hit a 'ying yang', you'll be able to solve it the same day."**
  / *"when yingyang is reached, 2 hours max."* → the **yin-yang is the single
  remaining unlock**; everything after it is the "true give-away" final step.
- **Prime part**: *"You are at the prime part already???"*, *"At least prime
  number is very important."*, and (2021-12-25) *"some characters need to be
  'zeroed out'."*
- **Breaking SalPhaseIon "should give the feeling of the phase's name."**
- The two addresses = **two private keys** = "half and better half" =
  **Architect (father) + Oracle (mother)** of the Matrix.
- *"There may indeed a piece be found outside the main puzzle"* (the second door /
  SalPhaseIon, reached by hashing the cover-image text).

## Verified against our data

### `matrix` = the phase-0 grid as a number  ✅ reproduced
A community member posted *"you will have sumlist … 405857343294124796905203
38541901772425587069158131163878976 … in the first phase, four zeros were omitted
from the matrix."*

`solver/matrix_value.py` reproduces this **exactly**: read the 14×14 grid as a
196-bit number (W/Y=0, K/U=1) in the URL spiral, **zero the 4 centre (bunny)
squares** ("four zeros omitted"). So the `matrix` in `matrixsumlist` resolves to:

```
40585734329412479690520338541901772425587069158131163878976
```

(Tested in the recipe password — necessary but not sufficient: `yinyang` and
`thepassword` values are still unknown, so assemblies still fail.)

### STR_A: 'b' sits at prime positions  ✅ verified
In `dbbibfbh ccbeg…`, the letter **`b` is at positions 2,3,5,7,11** — the first
five primes — then the pattern breaks at 13. Community odds estimate ≈ 9 in
3.18×10¹¹ for the first 12 chars. Also: 8 of 10 gaps between `be` occurrences are
prime. This is the concrete signature of the "prime part" / "reinsert the prime
basics", but **how to exploit it to decode STR_A is still unknown** (removing the
b's, octal-mapping the remaining 8 symbols, etc. all give garbage).

## Community approaches already tried (all failed)

substitution 1-9 / 0-8 / primes; ROT; XOR; Caesar; double-hashing the whole
puzzle; matrix sum × multiply as a password; decrypting Cosmic Duality with the
SalPhaseIon result, with reversed blobs, with hashed answers. "I have zero ideas
on how to approach dbbi" is the common sentiment — STR_A/STR_B remain the wall.

## Additional clues worth chasing (from the chat)

- **"SalPhaseIon" = "salvation"** ("phase" inserted into salvation). The creator:
  *"Breaking salphation should give the feeling of the phase's name."* This maps
  to the Architect's **right door** — "the source and the **salvation** of Zion".
  So `lastwordsbeforearchichoice` and SalPhaseIon both point at the two-door /
  Source speech.
- **"CIAO BELLA O" → Bellaso / Chaocipher?** The Beaufort-decoded speech ends
  "…ciao bella o" (reverse of the song "o bella ciao"). Community: maybe a hint
  at the **Bellaso cipher** (a Vigenère precursor) or **Chaocipher**, or simply a
  "reverse" marker (cf. the 2023-02-23 reversed-binary hint).
- **dbbi/faed may be recipe slots 6 & 7 themselves** ("unless dbbib is the 6th
  and faed is the 7th, or them combined is the 6th") — i.e. possibly used
  directly rather than decoded to ASCII.
- The chain is believed to be: decode dbbi/faed → complete SalPhaseIon → hash →
  the SalPhaseIon AES "might lead back to the 3.2.2 AES" → … → Cosmic Duality →
  reward. An (unverified) GitHub-issue comment claims decrypting Cosmic Duality
  "using the result of SalPhaseIon" yielded "a long sentence like a lyric."

## Tested from these clues — all negative

matrix number / row-sum list / col-sum list in the recipe; blob-as-password
duality; letters→nth-prime; zeroing prime positions/values; inserting zeros at
prime positions; Bellaso-style and 8-symbol reductions of STR_A/STR_B. The
`dbbi`/`faed` decode and the `yinyang` value remain the universal wall.

## Open, highest-value question

**What is `yinyang` as a concrete value/operation?** The creator calls it "a very
specific hint" and the single unlock. It references the Cosmic Duality book
(yin-yang of two galaxies) and the two halves (Architect/Oracle). Resolving it is
the documented "2-hours-from-solved" step.
