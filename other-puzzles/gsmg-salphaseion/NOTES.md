# GSMG.IO 5 BTC Puzzle — SalPhaseIon / Cosmic Duality stage (UNSOLVED)

The main `Bahs` repo documents the GSMG.IO puzzle solved through **Phase 3.2**
(the EBCDIC→Beaufort→VIC chain yielding the "INCASE…" key). This folder works
the **next open frontier**: the two SalPhaseIon ciphertext strings, reproduced
and verified against the community Telegram transcript.

**Official addresses (only two known):**
- `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` — main puzzle / final prize.
- `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` — where **half the funds moved during the
  halving**.

## Are "btcseed" / "YOUWON" real signal, or paranoia?  (honest take)

Under a random-output null model:
- **btcseed** at the exact start of the bifid output (7 letters, 25-letter
  alphabet) ≈ **1 in 6.1 billion**.
- **YOUWON** appearing anywhere in the 91-char OTP output (6 letters) ≈
  **1 in 3.6 million**.

Why this is more than cherry-picking: **neither key was brute-forced.** The
bifid keyword `dbifhceg` is the *dedup-first-appearance rule applied to `dbbi`
itself* (d,b,b,i,b,f,b,h,c,c,b,e,g → dbifhceg) — derived from the string's own
structure, not chosen to spell "btcseed". The OTP key `INCASE…` is the
independently-verified Phase-3.2 output. So both tokens come from *forced*,
single applications, which is what makes them hard to dismiss.

The steelman **for** skepticism (valid): if the community collectively tried
many (cipher, key, operation, alphabet) combinations and kept the one run that
happened to spell a word, the effective trial count inflates and the "surprise"
shrinks — the garden-of-forking-paths problem. btcseed survives this far better
(rule-derived key, astronomically rare); YOUWON is weaker (a Vigenère/OTP `c−k`
was one of a few natural operations to try).

**Bottom line:** they are most likely intentional *markers/labels* confirming
direction — but they are NOT payload. We have decoded **two signposts and zero
treasure**: the 90-char block, the 472-char tail, and especially the 21- and
64-char OTP segments remain fully opaque, and **no key or seed has been
recovered**. So "are we just chasing btcseed?" is a fair worry: the markers tell
us *where*, not *what*.

---
Prize address (final): `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`.

## Canonical inputs

- **STR_A "dbbi"** — 91 chars, alphabet a–i.
- **STR_B "faed"** — 570 chars, alphabet a–i (recovered from the CyberChef
  bifid-input base64 in the transcript).
- **Key "INCASE…"** (from Phase 3.2):
  `INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE`

## Finding 1 — bifid(STR_B) → btcseed  ✓ REPRODUCED

`bifid_decode(faed, key="dbifhceg")` (5×5 square, I/J merged; the keyword is the
de-duplicated prefix of `dbbi…`) yields:

    btcseed
    deoemckeadhbschdkbdcsdkdvbxcpcochcrdicibqeebddbcndsbdcpdgcpdncncsescgddclenbmcuducqcacdeld   (90)
    z                                                                                            (single separator)
    elcmefdfesdodwck…dpciel                                                                       (472)

The single `z` is the only one in 570 chars (it falls where the two halves share
their one common letter), strongly implying it's an intentional separator. The
90-char block splits into **45 pairs whose 2nd letter is always ∈ {b,c,d,e}**;
1st letters never use c/f/j/t/w/y/z — a deliberately structured encoding (the
"btcseed" label suggests it encodes a 12-word seed / key material).

## Finding 2 — OTP(STR_A) → YOUWON  ✓ REPRODUCED  (the breakthrough)

`(dbbi − INCASE) mod 26`, with A=0, over all 91 chars:

    VOZIJBDTIQBRGVEOMZNBC  YOUWON  XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA
    |------ 21 chars -----|       |--------------------------- 64 chars ---------------------------|

`YOUWON` appears at index 21, followed by **exactly 64 characters** — the count
of hex chars in a 256-bit Bitcoin private key (Sycorax's observation). This is
the single strongest legible result anyone has pulled from `dbbi`.

## What has been tested here (all negative)

- SHA256 / double-SHA256 of {after-64, before-21, YOUWON+after, full OTP, the
  bifid blocks, INCASE, the raw strings} as a private key → **no** GSMG address.
- The 64-char tail as base-26 → 256-bit int → privkey → **no** match.
- Second-layer bifid / OTP / Vigenère on the 21- and 64-char segments →
  noise (and `after+INCASE` just reconstructs `dbbi`, i.e. self-inverse, not new
  information).

So the 64-char tail is **not** a private key under any direct/obvious encoding;
it almost certainly needs the puzzle's next intended step.

## Finding 3 — the SalPhaseIon page is a self-describing ROADMAP  ✓ NEW, VERIFIED

The full SalPhaseIon character stream (from `salphaseion.ipynb`) is not just the
two a–i ciphertexts. Decoding its other embedded segments (all reproduced in
`roadmap.py`) yields the puzzle's own instruction labels:

| segment | encoding | decodes to |
|---|---|---|
| binary1 (a/b) | a=0,b=1, 8-bit ASCII | **`matrixsumlist`** |
| binary2 (a/b) | a=0,b=1, 8-bit ASCII | **`enter`** |
| base-10 s1 | `abcdefghio`→`1234567890`, hex→ascii | **`lastwordsbeforearchichoice`** |
| base-10 s2 | same | **`thispassword`** |
| `shabef` | `sha`+letter-index(b,e,f)=`sha`+2,5,6 | **`sha256`** |

So the page literally lays out the procedure:
`STR_A` → (matrix-sum-list) … `STR_B`=btcseed … **last words before the
architect's choice** … **this password** … **sha256** of *"our first hint is
your last command"* … **[AES blob]** … **enter** … **[AES blob]** … sha256
*"ans too"*.

Per `phase0.ipynb`, **"our first hint" = "follow the white rabbit"** (Matrix).

## Finding 4 — the AES blob is real and correctly assembled  ✓ NEW

The two base64 chunks join (with the literal `z`) into one OpenSSL blob:

    base64( "Salted__" + salt(3ab585348552415d) + 80-byte ciphertext )

96 bytes total, ciphertext = 5 AES-CBC blocks — a well-formed `openssl enc`
output (my decryptor is round-trip-verified against the `openssl` CLI). The
password is one of the architect's "seven intertwined passwords"; tried so far
(via EVP_BytesToKey md5/sha256, AES-128/256, raw + sha256-hex + sha256-raw
forms): the roadmap labels, Matrix quotes, "follow the white rabbit" variants,
btcseed/youwon — **no valid-padding decryption yet**. `aes_attack.py` extends.

## AES password search — exhaustive negatives (this session)

The combined blob (80-byte ct) is consistent with a **64-hex-char private key +
16-byte PKCS#7 pad**. Attacked with strict-ASCII / valid-padding filtering:
- ~38,700 contiguous word n-grams (len 1–13) of the architect speech + the
  canonical Matrix two-doors monologue, each raw / no-space / sha256(hex,raw).
- All decoded puzzle strings (btcseed payload, bifid tail, OTP/YOUWON segments,
  STR_A, STR_B, INCASE, roadmap labels) × KDFs {EVP_BytesToKey-md5,
  -sha256, PBKDF2-sha256/sha512 @ 1/1000/10000} × AES-128/256.
- Both blob assemblies (combined 80-byte ct, and AES1-alone 32-byte ct).

**No valid decryption.** (Decryptor round-trip-verified vs the `openssl` CLI, so
negatives are real.) The password is one of the architect's "seven intertwined
passwords"; the community has not cracked it either.

## The connected lead (strongest direction)

Three roadmap/transcript threads point at one mechanism:
- roadmap label **`lastwordsbeforearchichoice`**,
- the architect's instruction **"reinserting the prime basics"**, and
- the transcript claim that **prime indexes over "last words" extract ~30–31
  bytes containing "ying yang" and "salvation."**

The architect's literal *last words before the choice* are the Matrix Reloaded
**two-doors speech**: *"…leads to the source and the **salvation** of Zion … the
door to your left … the Matrix…"* — and the two doors ARE the **yin-yang /
cosmic duality** (the next phase). So the intended step is almost certainly a
*specific* prime-indexed selection over that speech, yielding the cosmic-duality
key material. Plain prime-indexing (all primes, 0/1-based, with/without spaces)
does NOT cleanly surface salvation/yingyang — the exact word-set + prime scheme
is still unknown (this is the live frontier).

## Tooling added
- `roadmap.py` — verified decode of all embedded instruction labels.
- `aes_attack.py`, `aes_ngram.py` — OpenSSL-blob decryptors + n-gram password
  search (round-trip-checked vs `openssl`).

## Open leads (from the transcript — the next intended step)

- "**yellow blue primes**" — an unsolved sub-clue gating progress.
- "next phase is **yinyang** = **cosmic duality**."
- A user (Denis Golovkin) claims applying **specific prime indexes to specific
  last words** extracts ~30–31 bytes containing "**ying yang**" and
  "**salvation**" — i.e. a *prime-indexed selection over "last words"*, not a
  direct decode of the 64-char tail.
- The "INCASE" message ("keys belong to **half and better half**") implies **two**
  keys — possibly STR_A and STR_B (or part-0 / part-1) are the two halves.
- AES blobs (`U2FsdGVkX1…` = OpenSSL `Salted__`) appear later in the chain; the
  transcript hints the answers are SHA256'd ("sha256 our first hint is your last
  command", "sha256 ans too") to derive keys.

## Tooling (verified)

- `gsmg_toolkit.py` — canonical strings + `bifid_decode`, `otp`; self-tests both
  findings (`btcseed…`, `YOUWON`).
- `btc.py` — privkey→P2PKH (comp/uncomp) via coincurve; `check_priv` compares to
  the known GSMG addresses. Sanity-checked against privkey=1.
- `analyze.py` — the hypothesis battery (re-run to extend with new ideas).

## Finding 5 — there are TWO AES blobs; "Cosmic Duality" is the large, untranscribed one  ✓ NEW

The SalPhaseIon page image (`salphaseion-assets/SalPhaselonCosmicDuality.png`)
has **two** sections, and they are different ciphertexts:

1. **"SalPhaseIon"** heading → the a–i character block. This is what
   `salphaseion.ipynb` transcribed. Spelled out *inside* this a–i stream (char by
   char, with the rest of the roadmap labels) is the **small 96-byte** OpenSSL
   blob `U2FsdGVkX186tYU0…d9z QvX0…N/jJ` (salt `3ab585348552415d`). This is the
   blob all prior tooling here attacks.

2. **"Cosmic Duality"** heading → a **separate, much larger** base64 block
   beginning `U2FsdGVkX18tP2//gbcl…` (≈13 lines × 64 = 832 b64 chars ≈ 624 bytes
   = `Salted__` + 8-salt + ciphertext). **This blob was never captured as text in
   this repo** — the notebook stops at the small embedded blob. The byte-accurate
   transcription is now in **`cosmic_duality_blob.txt`** (28 lines × 64 = 1792
   base64 chars = 1344 bytes; salt `2d3f6fe06dc950e6`; **83 AES-CBC blocks**;
   structurally a valid `openssl enc` / CryptoJS `Salted__` blob).

Implication: the small "SalPhaseIon" blob and the large "Cosmic Duality" blob are
plausibly a **two-stage lock** — decrypting the small one likely yields the
password (or instruction) for the large final-treasure blob. The roadmap labels
that bracket the small blob ("sha256 / our first hint is your last command /
[blob] / enter / [blob] / sha256 ans too") describe how to open it.

## Finding 6 — authoritative matrix/spiral geometry  ✓ NEW

Re-ran the phase-0 spiral unwrap tracking every cell. The **24 coloured cells sit
exactly at spiral positions 8, 16, 24, … 192** — i.e. each is the **LSB (8th bit)
of one of the 24 bytes** that spell `gsmg.io/theseedisplanted`. Therefore:

- **blue = LSB 1 = odd-ASCII char**, at URL char positions
  {1,2,3,4,6,7,8,11,12,13,14,16,17,20,23};
- **yellow = LSB 0 = even-ASCII char**, at {5,9,10,15,18,19,21,22,24}.

So "Yellow has a number and so does Blue" (2020-01-14 poem) literally means the
yellow/blue cells tag the parity of each URL character. "yellow blue primes"
(2023-02-23) selects the **prime-positioned** ones: blue-prime positions
{2,3,7,11,13,17,23} → chars `s m o e e s e`; yellow-prime {5,19} → `. l`.
Matrix row sums = [6,10,8,7,6,6,5,4,9,9,7,8,7,9], col sums =
[8,10,8,10,8,7,3,6,7,5,9,6,6,8] (both total 101). None of these, in any tested
encoding, opens either blob.

## Finding 7 — the full roadmap (decoded 2023-02-23 official hint)  ✓

The official "reverse binary string" hint decodes to the ordered pipeline:

> yellow blue primes · matrix sumlist · last words before archichoice · yinyang ·
> "we wont give away thepassword **its in front of your eyes but youre not seeing
> it** · very last step is a true give away"

Read as: the password is **visible on the page** and is *constructed* by walking
these steps (not brute-forced). The "ying yang / cosmic duality" is the two-doors
choice; 2023-08-06 hint: *"once you hit a ying yang you'll solve it the same
day."* The exact per-step operations remain the open frontier.

## Exhaustive negative password searches (this session, correct 96-byte blobs)

All against both blobs, EVP_BytesToKey {md5,sha256} × AES-{128,256}, password
forms {raw, sha256-hex, sha256-bin, sha256-HEX, md5-hex}:

- 90k n-gram forms of the architect speech + Matrix monologue (`ngram_correct.py`).
- 3.3k structured candidates (`full_attack.py`); 1.5k roadmap candidates
  (`roadmap_attack.py`); 57k full-`yourlife` windows + roadmap n-grams
  (`full_ngram_attack.py`).
- The 2021-05-06 entry recipe `sha256("GSMGIO5BTCPUZZLECHALLENGE"+address)` and
  variants; the page URL hash; visible titles; matrixsumlist outputs under
  y/b ∈ {(0,1),(5,2),(9,15),(2,3),(5,7),…}; yellow/blue prime char picks over the
  URL/seed; the full architect monologue and every sentence-boundary phrase.

**No valid-padding ASCII decryption.** Decryptor is round-trip-verified vs the
`openssl`/CryptoJS `Salted__` format, so the negatives are real.

## Honest status

This is the SalPhaseIon/Cosmic-Duality wall — the GSMG puzzle has been stuck
here for years. The findings above are real and reproduced from first principles,
but the password derivation (the ordered roadmap pipeline ending in
yinyang/"in front of your eyes") is not yet pinned to a concrete string, and the
large Cosmic Duality ciphertext still needs a byte-accurate transcription. No key
recovered.
