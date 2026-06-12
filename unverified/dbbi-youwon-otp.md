# dbbi decodes TWO ways — the "cosmic duality" of STR_A

Both SalPhaseIon strings now have verified decodes, and **dbbi (STR_A) plays a
dual role** (fitting the puzzle's "Cosmic Duality" theme):

## 1. dbbi as the Bifid KEY for faed  (verified — see bifid-breakthrough.md)
`dbbi`'s unique letters → `dbifhceg`; Bifid-decoding `faed` → `btcseed` + part1/part2.

## 2. dbbi as Vigenère/OTP CIPHERTEXT  (verified, reproducible)
**Key = the "INCASE…" string** (the Phase-3.2 VIC plaintext, also 91 chars — which
is why "dbbi and incase are both 91"):

```
cipher (dbbi):  dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe
key (incase):   INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
decrypt(c-k):   VOZIJBDTIQBRGVEOMZNBC YOUWON XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA
```

The plaintext contains **`YOUWON`** (P ≈ 3×10⁻⁷ by chance → almost certainly
intentional), splitting the 91 chars into:
- **`VOZIJBDTIQBRGVEOMZNBC`** (21 chars) — community reads as the "HALF" key
- **`YOUWON`** (6)
- **`XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA`** (64 chars)
  — the "BETTER HALF"; **64 = exactly the length of a hex private key**

### Status of the half/better-half strings
Not yet a direct key. Checked (oracle vs both addresses): base-26 → bytes (all
windows, mod the curve order N), pairs→bytes (×26, ×16), nibble-hex, sha256, and a
further Vigenère layer (keys: incase, betterhalf, youwon, …). No match yet — they
likely need one more decode/combination. **Caveat:** some community members think
YOUWON is an "infinite-monkey" coincidence; the 3e-7 probability argues otherwise.

## The "primes" recipe slot — community candidates (UNVERIFIED)
- **`8686159`** = the phase-0 grid colour frequency `0=86, 1=86, blue=15, yellow=9`
  → "8686159" (a prime). Note this also re-confirms **yellow=9, blue=15**.
- **`2518101088543`** = dbbi's letter frequency, greatest→least (a prime).
- Concatenated **`86861592518101088543`** is also prime.
The creator confirmed "prime number is very important"; plural "primes" is
explicit. What to *do* with them (where in the password) is still unknown.

## Recipe completeness check (2023-02-23 hint)
`yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang → thepassword`
| slot | value | status |
|------|-------|--------|
| yellow | 9 | ✓ |
| blue | 15 | ✓ |
| primes | 8686159 / 2518101088543 ? | candidate |
| matrixsumlist | 40585…878976 (grid as number) | ✓ |
| lastwordsbeforearchichoice | literal / two-door speech | ✓ |
| yinyang | Cosmic Duality blob | open |
| thepassword | — | the assembled result |

## Key-extraction attempts (loop iteration — all negative, oracle-checked)
- half/better strings → base-N (16/24/25/26/32/36), 26 Caesar shifts, pairs→bytes
  (×16/24/26/32), reversed, base-26 mod curve-order N → privkey. No address match.
- half/better as AES passwords (sha/direct/md5/sha256) on all 3 blobs. No.
- half/better as Vigenère keys over the yin-yang wide channel. No.
- part1/part2 bit-packed to 256 bits (wide=5b square-pos / alpha; narrow=2b; both
  orders; 4 bcde orderings; narrow-only channel ±reversed) → privkey. No.
- Recipe concat with primes∈{8686159, 2518101088543, 86861592518101088543, 2357}
  and yinyang∈{ISBN 9780705406963, yinyang, cosmicduality} → all 3 blobs. No.
- Wide-channel Bifid with long keys (incase, speech, lastwords, salvationofzion,
  the half/better strings themselves) and a 4-letter crib search for
  salvation/yinyang/youwon — no clean decode.

**Next-iteration ideas:** (a) the recipe may be 4 *sequential stages*, not a
concatenated password (X: "4 stages"); (b) "reinserting the prime basics" may mean
inserting 2,3,5,7 into a string at prime positions before hashing; (c) the
half/better and part1/part2 may pair up (two "halves" each).
