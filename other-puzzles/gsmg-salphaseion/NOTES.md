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

## Honest status

This is the SalPhaseIon/Cosmic-Duality wall — the GSMG puzzle has been stuck
here for years. The two findings above are real and now reproduced from first
principles with clean tooling, but converting them into a working key requires
the next conceptual step (prime-indexed "last words" → yinyang/salvation), which
is not yet pinned down. No key recovered.
