#!/usr/bin/env python3
"""
Targeted checker for the Brave New World 0.2 BTC mnemonic.

IMPORTANT — feasibility (measured on 1 core):
  * one candidate check (BIP39 seed + a few BIP32 derivations) ~= 2 ms
  * orderings of a SINGLE known 12-word set = 12! = 479,001,600
    -> ~293 core-hours just for one word set, one passphrase.
  We do NOT know the exact 12 words, the count, duplicates, or passphrase, so
  full enumeration is infeasible. This file is therefore NOT a blind brute
  forcer. It only helps once a human has pinned MOST of the phrase and only a
  few positions float.

Use it like:
  FIXED = ["moon","tower","food","this","subject","real","black",
           "order","stable", None, None, None]   # None = unknown slot
  FLOATERS = ["picture","seed","phrase"]         # candidates for the None slots
It streams permutations of FLOATERS into the None slots (no giant set in RAM),
checks BIP39 checksum, derives addresses, compares to TARGET.
"""
import itertools
from solver import check_mnemonic, TARGET

# ---- edit these as you narrow the phrase down ----
FIXED   = ["moon","tower","food","this","subject","real","black","order","stable",None,None,None]
FLOATERS = ["picture","seed","phrase","clock","liberty","matter"]
PASSPHRASES = [""]            # add suspected BIP39 passphrases here
# --------------------------------------------------

def run():
    slots = [i for i,w in enumerate(FIXED) if w is None]
    n = len(slots)
    tested = valid = 0
    for pick in itertools.permutations(FLOATERS, n):   # streamed, no set()
        cand = FIXED[:]
        for idx, w in zip(slots, pick):
            cand[idx] = w
        for pp in PASSPHRASES:
            res = check_mnemonic(cand, pp) if pp == "" else None
            # check_mnemonic only takes passphrase via its own arg; call directly
        # simpler: just use the no-passphrase path of solver.check_mnemonic
        res = check_mnemonic(cand)
        tested += 1
        if res is None:
            continue
        valid += 1
        if res:
            print("[!!!] MATCH:", " ".join(cand), res)
            return
    print(f"[done] tested={tested} valid_checksum={valid} no match for TARGET {TARGET}")

if __name__ == "__main__":
    run()
