#!/usr/bin/env python3
"""
Decoder for the "Securing Wealth in Poetry" 0.03 BTC puzzle (Trithemius, 2019).

The article describes three steganographic encodings and gives worked examples.
The GPS method is fully reverse-engineered and VERIFIED against the article's
own example:

    "U.S. Supreme Court 38.8906 N, 77.0044 W"
    -> 12 significant digits: 3,8,8,9,0,6,7,7,0,0,4,4
    -> position_k (1-based) = digit_k + 10*k
    -> 3,18,28,39,40,56,67,77,80,90,104,114   (matches the article exactly)

This module: tokenize the article, apply an index set, extract words, and
(via solver) check BIP39 validity + target address.
"""
import re

TARGET = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"

def gps_positions(digits):
    """digits: list/str of significant coordinate digits -> 1-based word positions."""
    ds = [int(c) for c in str(digits) if c.isdigit()]
    return [d + 10*k for k, d in enumerate(ds)]

def phone_positions(*numbers):
    """Story-&-phone method: concatenate the digit groups as positions (as given)."""
    out = []
    for n in numbers:
        out.extend(int(x) for x in re.findall(r"\d+", n))
    return out

def tokenize(text, mode="alpha"):
    """
    mode:
      'alpha'      -> runs of [A-Za-z'] (apostrophes kept inside words)
      'alpha_noap' -> runs of [A-Za-z] (apostrophes split words)
      'ws'         -> whitespace split, strip surrounding punctuation
    """
    if mode == "alpha":
        return re.findall(r"[A-Za-z']+", text)
    if mode == "alpha_noap":
        return re.findall(r"[A-Za-z]+", text)
    if mode == "ws":
        return [w.strip(".,;:!?()\"'—-").lower() for w in text.split() if w.strip(".,;:!?()\"'—-")]
    raise ValueError(mode)

def pick(words, positions, base=1):
    return [words[p-base] if 0 <= p-base < len(words) else f"<{p}?>" for p in positions]

def nth_letter_cipher(text, n):
    """Null cipher: take the n-th letter (1-based) of each word; skip short words."""
    out = []
    for w in re.findall(r"[A-Za-z]+", text):
        if len(w) >= n:
            out.append(w[n-1])
    return "".join(out)

if __name__ == "__main__":
    # self-test against the article's GPS example
    pos = gps_positions("388906770044")
    assert pos == [3,18,28,39,40,56,67,77,80,90,104,114], pos
    print("GPS rule self-test PASSED:", pos)
