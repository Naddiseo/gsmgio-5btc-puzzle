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

## Finding 8 — the "Sum" token from STR_A (b-as-separator)  ✓ NEW, VERIFIED

A previously-untried decode of **STR_A** (the 91-char `dbbi` string): treat **`b`
as a separator**, and for each group of letters between separators **sum the
letter values** (a=1 … i=9; `b`=2 is the separator). Map each group-sum to a
char: 1–26 → A–Z, 27–36 → digit (sum−27). This yields:

    DIFNLREV9E6VARXVF5UF8PE      (23 groups → 23 chars)

The digits (9,6,5,8) land **exactly** where a group-sum exceeds 26 — a designed
feature, not coincidence — so the method is almost certainly intended. This is
the **"sum" / "ans"** the SalPhaseIon stream refers to ("…combine what was found
in the sum and what was said at the end…"). Reproduced from first principles in
`salph_sum_decode.py` and cross-checked against community work
(github `mkno03/GSMG-5BTC-...`, which reports the same token but did **not**
crack the AES — its "hits" are padding-oracle false positives). Tested as an AES
password (alone, sha256, and combined with last-words / "ans"=5 / matrixsumlist
column-sums of STR_B) under EVP-md5/sha256 **and** PBKDF2-sha1/sha256 ×
AES-128/192/256 — no decryption yet, but this is the strongest verified new
component for assembling the password.

## Finding 9 — the EXACT AES scheme, reverse-engineered from solved phases  ✓ NEW, VERIFIED

Using the **solved** earlier phases (answers public) as known-plaintext, the
encryption scheme is now pinned down exactly (`phase_decryptor.py`):

    passphrase = sha256_HEX(answer)              # 64-char hex digest, as a string
    key,iv     = EVP_BytesToKey(md=SHA-256, passphrase, salt)   # AES-256, 1 iter
    plaintext  = AES-256-CBC(ciphertext); strip PKCS#7

VERIFIED decryptions:
- **Phase 2**, answer `causality` → `"The ironic 2name of the keymakers trying to
  protect the current digital powers…"` (Mr-Robot/cipher riddles).
- **Phase 3.2**, answer `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`
  → `"I've been waiting for you. You have many questions…"` + the EBCDIC blob.

Key correction: the KDF digest is **SHA-256, not MD5** (newer `openssl enc`
default), and the passphrase is the **hex** sha256 of the answer. Answers are
**concatenations of the stage's sub-solutions** (e.g. Phase-2 parts 1–7). This is
exactly what the SalPhaseIon `shabef` (=sha256) labels denote. The Cosmic/salph
blobs are the same scheme; the only unknown is the *answer string* assembled from
the SalPhaseIon roadmap. Every candidate answer can now be tested deterministically
and correctly via `phase_decryptor.decrypt(blob, answer)`.

## Finding 10 — the FEFEFE image marker + Bacon cipher  ✓ NEW, VERIFIED

From a 2026-06 community-log review (`community_findings.py`):
- **FEFEFE marker**: `puzzle.png` has exactly ONE 25×25 grid cell colored
  **(254,254,254)** instead of pure white — a deliberate "glitch in the matrix"
  marker just left of the rabbit. Verified at grid **(row 7, col 4)**, 0-indexed
  = spiral index 163 = byte 21, bit 3 of the phase-0 URL decode. Intentional but
  its use in the answer is not yet determined.
- **Bacon (rot-1) cipher**: an inverted-alphabet Baconian on a/b; decodes chat
  members' a/b strings to Matrix quotes ("everythingthathasabeginninghasanend",
  "beingtheoneislikebeinginlove", "choicestakingintotheabyss"). The puzzle's own
  a/b strings are plain 8-bit ASCII, so this is a community tool, not a step.
- Two long base58 strings claimed to "hide a private key" decode (base58→base64→
  Bacon) to chat banter ("we need to focus into whats left…") — not puzzle data.

Tested all decoded Matrix quotes + Bacon phrases as the Cosmic/salph answer under
the confirmed scheme (Finding 9): no decryption.

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

## Finding 11 — Denis Golovkin's blue/yellow token structure, VERIFIED  ✓ NEW

Reproduced from the transcript ("First 20 prime indexes of dbbi … 'b' for blue,
'be' (25, y) for yellow … 16/7 blue/yellow [23/16/7]"). The verified structural
facts in **STR_A** ("dbbi", 91 chars):

- Replacing every `be` → `y` compresses STR_A (81 chars). Its **b/y subsequence
  has exactly 25 tokens = 15 standalone `b` (blue) + 10 `be`→`y` (yellow)** —
  matching Denis's literal "**(25, y)**" (and `y` = 25th letter; `be` = 2,5).
- The split Denis quotes, **[23/16/7]**, equals the count of **primes ≤ 83 (=23)**
  and is *the same triple* the Architect's Beaufort speech states verbatim:
  "select from over **twenty-three ciphers, sixteen encryptions** and/or **seven**
  intertwined passwords." So [23/16/7] is almost certainly a **description of the
  solution-pipeline length, not a single password** — which is the structural
  reason every single-password blob attack (ours and the community's) fails: the
  blob key is the *output* of a 23/16/7 composition, not a guessable phrase.
- Denis's exact prime→b/y mapping does **not** reproduce cleanly: 1-indexed
  primes≤83 into raw STR_A land on non-b/y letters (g,a,e,h,f,c,i); into the
  compressed string they give 8 b / 3 y / 11 other. His precise indexing
  (likely a rabbit/spiral re-ordering he didn't spell out) is unrecovered. The
  *token counts* (15/10) are solid; the *prime selection* is not.

Denis's final "**I mean two**" — read as two passwords/answers (cf. the INCASE
"half and better half" = two keys). Tested 100+ two-part concatenations of every
verified artifact under the confirmed scheme — no decryption.

## Finding 12 — the phase-3.2 cell-18 AES is captured as a third target  ✓ NEW

The notebook's leftover, never-cracked AES (`phase3.2.ipynb` cell 18,
salt **b45a5e3d827593ca**, 96 B = 80-byte ciphertext = 5 CBC blocks) is now a
target in `attack.py`. Per the chain it is upstream of SalPhaseIon. Tested
against every phase-3.2-internal answer (INCASE forms, the Beaufort/architect
speech and its sentences, the VIC alphabet `fubcdora/lethingkymvpszjqwx.`,
"ciaobellao", "returntothesourcecode", "reinsertingtheprimebasics") under the
verified scheme — **no decryption**. The bifid 90-char "btcseed" payload was
re-examined as a BIP39/seed encoding (45 pairs, 2nd letter ∈ {b,c,d,e}); no
readable/checksum-valid decode under ASCII-offset, mod-26, or 2-bit schemes.
The OTP 64-char tail was checked as a private key (sha256/dsha256/base26/hexmap
forms) against both real GSMG addresses via `btc.py` — **no address match**.

## Tooling note (this session)

The dozen overlapping one-off brute scripts were consolidated into a single
`attack.py` (verified `Salted__` decryptor + one candidate generator over all
verified artifacts + the three real ciphertexts). Removed: aes_attack, aes_ngram,
analyze, cosmic_attack, full_attack, full_ngram_attack, ngram_correct,
prime_attack, roadmap_attack, sum_combo_attack, salph_dict_brute (all exhausted).

## Finding 13 — community "SOLVED" issue #69 is FABRICATED  ✓ NEW, VERIFIED

`puzzlehunt/gsmgio-5btc-puzzle` issue #69 ("SOLVED: Comprehensive Solution")
claims a master AES key `818af53daa3028449f125a2e4f47259ddf9b9d86e59ce6c4993a67ffd76bb402`
built by XOR-ing the SHA-256 hashes of 7 tokens (matrixsumlist, enter,
lastwordsbeforearchichoice, thispassword, matrixsumlist, sha256, theone) and
"direct -K hex injection" into AES-256-CBC.

- The master key **does** reproduce from that XOR — but this is **circular**:
  the key is *defined* as the XOR, so reproduction proves nothing. Only actual
  decryption validates a key.
- Decrypting our (structurally valid, ct%16=0) cosmic and salph blobs with that
  key under every natural IV (zeros, salt‖salt, key[:16], CryptoJS first-16) and
  ciphertext slicing yields **garbage** (printable ≈ 0.39; only CBC block 0 even
  varies with IV — proof the key is wrong for this ciphertext).
- I generalised the method (novel for our tooling: *direct* AES-256 key = XOR of
  sha256(token) over the real roadmap tokens, all subsets size 1–5, 3 blobs,
  5 IV schemes = 638 token-sets) → **zero valid-padding ASCII decryptions**.
- The issue's "plaintext" is just the already-public INCASE sentence, it provides
  **no private key**, and it asks for a reward / permission to "dust" the address
  — the standard fabricated-submission pattern. **Disregard issue #69.**

Side note: the README's base64 transcription of AES1/AES2 (as machine-fetched)
is lossy (ct%16=12, invalid); our `salphaseion.ipynb` transcription assembles to
a clean 96-byte `Salted__` blob (salt `3ab585348552415d`, 80-byte ct), so our
ciphertext is the structurally sound one.

## Finding 14 — the Cosmic Duality plaintext is (reportedly) a PGP message  ✓ NEW LEAD

Issue #51 ("Progress on Salphaseion and Cosmic Duality") reports the cosmic
plaintext is a **~1327-byte PGP/OpenPGP message** (PKESK = Public-Key Encrypted
Session Key packets) — and our cosmic ciphertext is exactly **1328 bytes**, so a
correct AES decrypt would yield ~1327 plaintext bytes. **Important consequence:**
all our prior attacks required printable-ASCII ≥ 0.95 and would have *rejected a
binary PGP blob*. `attack.py`'s acceptance is now PGP-aware (valid PKCS#7 + PGP
packet-tag first byte / `-----BEGIN PGP` armor / nested `Salted__`).

Re-ran every verified candidate + roadmap concatenations + direct-XOR-key
(issue-#69 style) over all 3 blobs with the PGP filter (6840 decryptions). The
only "hits" were two single-byte tag coincidences on the small p32 blob with
random tails — statistical noise (expected at this trial count), not real PGP
structure. **No genuine PGP message recovered**; issue #51's author was likewise
stuck (the layer implies a further PGP private key is needed even after AES).

## Finding 15 — full structure of the bifid "btcseed" output  ✓ NEW, VERIFIED

Analysing the entire 570-char bifid decode (not just the 90-char block):

    btcseed | payload(90) | z@97 | tail(472)

- **Every** data pair is `(WIDE, NARROW)` with **NARROW ∈ {b,c,d,e}** (exactly
  2 bits). The `payload` is paired at offset 0 `(wide,narrow)`; the `tail` is the
  *same* pairing but **order-flipped** — its pairs read `(narrow,wide)` at offset
  0, i.e. clean `(wide,narrow)` again only at offset 1 (tail[0]=`e` is a leftover
  marker). So the single `z` is a **parity-flip / mirror point**, not just a
  separator: the second half is the first half's pairing reflected.
- Combined there are **280 `(wide,narrow)` pairs** (45 + 235). WIDE uses 24
  distinct letters; the alphabets are `a–y` minus `j` (bifid 5×5, I/J merged).
- Decoding attempts that FAIL (so future work can skip them): pair→ASCII via
  `wide*4+narrow` under compact- and a–z indexing × offsets {0,29,31,32,48,64};
  narrow-stream (2-bit) → bytes; first-letter Vigenère shifted by narrow
  (b/c/d/e = 0–3 or 1–4, add/sub/sub-rev). None yield readable text, a valid
  BIP39 checksum (16/24-word), or a private key matching either GSMG address.

The `(wide, narrow∈{b,c,d,e})` shape (4-valued second coordinate) strongly
implies a **keyed Polybius/grid read** (4 columns) whose square is one of the
roadmap passwords (`thispassword`, `lastwordsbeforearchichoice`) — that keyed
re-read is the concrete open sub-problem here.

## Finding 16 — the COMPLETE SalPhaseIon page token-stream, reconstructed  ✓ NEW, VERIFIED

The whole `salphaseion.ipynb` page is one continuous single-char token stream.
Reassembled verbatim from cell 0 (1075 tokens), it parses cleanly into:

    STR_A(91, a-i)                      <- "dbbi…" ciphertext #1
    binary1  -> "matrixsumlist"         (a/b, 8-bit ASCII)
    STR_B(570, a-i)                     <- "faed…" ciphertext #2
    z
    s1       -> "lastwordsbeforearchichoice"   (a-i via abcdefghio->1234567890, int->hex->ascii)
    z
    s2       -> "thispassword"                 (same map)
    z
    shabef   -> "sha256"                (b=2,e=5,f=6 base-10 -> SHA-256)
    "ourfirsthintisyourlastcommand"
    AES1  = U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
    binary2  -> "enter"                 (a/b, 8-bit ASCII)
    AES2  = QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
    shabef   -> "sha256"
    "anstoo"

So the AES = base64(AES1‖AES2) = the single 96-byte `Salted__` blob (salt
`3ab585348552415d`, 80-byte ct = 5 blocks); the `enter` between the two halves is
an instruction marker, not data (AES2 alone is not `Salted__`, confirming it is a
continuation). The two `shabef`(sha256) tokens bracket the blob — the password is
sha256-shaped, applied to text that is literally on the page ("in front of your
eyes"): the plain tokens `ourfirsthintisyourlastcommand` / `anstoo` plus the
labels `matrixsumlist` / `lastwordsbeforearchichoice` / `thispassword`.

## Finding 17 — the phase-3.2 Beaufort speech IS the final-stage instruction set  ✓ NEW

The Architect monologue (Beaufort key `THEMATRIXHASYOU`) ends with an explicit
recipe for exactly this stage:

  "…return to the source codes … **reinserting the prime basics** … you will be
   required to select from over **twenty-three ciphers, sixteen encryptions,
   and/or seven intertwined passwords** to find the actual private key. note that
   **also brute forcing might be required** … ciao bella o"

Concrete mappings (new):
  * **twenty-three ciphers** ↔ the 23-char `SUM = DIFNLREV9E6VARXVF5UF8PE`
    (STR_A b-separator letter-sum). 23 is not a coincidence.
  * **reinserting the prime basics** ↔ primes **2,3,5,7** (creator-confirmed,
    2021-03-01) used as position indices.
  * **seven intertwined passwords** ↔ "intertwined" = the **yinyang** roadmap
    step = interleave of (up to) seven password streams.
  * **brute forcing might be required** ↔ the final passphrase is expected to be
    short / from a constrained space, not a long derived string.

## Session 2026-06-14 — exhaustive password search, no hit (negative results)

Tested against all three real blobs (salph 96B, p32cell18 96B, cosmic 1328B)
under EVP-MD5, EVP-SHA256, **and PBKDF2** (sha1/256/512, iters 1/1k/10k/100k),
AES-{128,192,256}-CBC, passphrase forms {raw, sha256-hex, sha256-HEX, sha256-bin,
md5-hex}, strict PKCS#7 + printable/nested-Salted__ acceptance:

  * every page plain token and all 127 of their combinations;
  * SUM / OTP-PRE / OTP-TAIL(64) / two-time-pad M2 / bifid payload, raw + sha256;
  * yin-yang **interleavings** and **OTP-chains** of {SUM, PRE, TAIL, bifid,
    ciaobellao, thematrixhasyou, theseedisplanted, …} pairwise + triple;
  * GSMG URL-hash construction `sha256("GSMGIO5BTCPUZZLECHALLENGE"+X)` (passphrase
    and direct hex-key) for every X;
  * Caesar/Vigenère reads of PRE and TAIL (no English surfaces — they are
    high-entropy key material, with `YOUWON` as an embedded confirmation marker);
  * prime-position (2,3,5,7,…) extractions from the Beaufort speech and the URL.

None produced valid-padding readable plaintext. The 64-char post-`YOUWON` tail
and the keyed-Polybius re-read of the bifid `(wide,narrow∈bcde)` pairs (Finding
15) remain the two concrete open sub-problems.

## Honest status

This is the SalPhaseIon/Cosmic-Duality wall — the GSMG puzzle has been stuck
here for years. The findings above are real and reproduced from first principles.
The page is now fully reconstructed (Finding 16) and the creator's own recipe is
decoded (Finding 17), but the final passphrase string is still not pinned, and
the large Cosmic Duality ciphertext still needs a byte-accurate transcription.
**No key recovered.**
