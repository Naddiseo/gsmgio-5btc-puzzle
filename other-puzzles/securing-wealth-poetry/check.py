#!/usr/bin/env python3
"""
Checker for the "Brave New World" 0.2 BTC puzzle.

Given a candidate 12/24-word BIP39 mnemonic, validate the checksum and derive
common address types, comparing against the target.

Usage:
    python3 solver.py "word1 word2 ... word12"
    python3 solver.py            # runs a tiny demo over a candidate set

Deps: pip install mnemonic ecdsa base58
"""
import sys, hashlib, hmac, itertools
from mnemonic import Mnemonic
import ecdsa, base58

TARGET = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"
mnemo = Mnemonic("english")

def b58check(prefix, payload):
    data = prefix + payload
    chk = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return base58.b58encode(data + chk).decode()

def hash160(b):
    return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()

def priv_to_p2pkh(priv32, compressed=True):
    sk = ecdsa.SigningKey.from_string(priv32, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x(); y = vk.pubkey.point.y()
    if compressed:
        pub = (b"\x03" if y & 1 else b"\x02") + x.to_bytes(32, "big")
    else:
        pub = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    return b58check(b"\x00", hash160(pub))

# --- minimal BIP32 (master + hardened/normal derivation) ---
CURVE_N = ecdsa.SECP256k1.order

def bip32_master(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]  # key, chaincode

def ckd_priv(k, c, i):
    if i & 0x80000000:
        data = b"\x00" + k + i.to_bytes(4, "big")
    else:
        sk = ecdsa.SigningKey.from_string(k, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        x = vk.pubkey.point.x(); y = vk.pubkey.point.y()
        pub = (b"\x03" if y & 1 else b"\x02") + x.to_bytes(32, "big")
        data = pub + i.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    ki = (int.from_bytes(I[:32], "big") + int.from_bytes(k, "big")) % CURVE_N
    return ki.to_bytes(32, "big"), I[32:]

def derive(seed, path):
    k, c = bip32_master(seed)
    for i in path:
        k, c = ckd_priv(k, c, i)
    return k

H = 0x80000000
PATHS = {
    "m":                 [],
    "m/0":               [0],
    "m/0/0":             [0, 0],
    "m/0'/0'/0'":        [0|H, 0|H, 0|H],
    "m/0'/0/0":          [0|H, 0, 0],
    "m/44'/0'/0'/0/0":   [44|H, 0|H, 0|H, 0, 0],
    "m/44'/0'/0'/0/1":   [44|H, 0|H, 0|H, 0, 1],
    "m/49'/0'/0'/0/0":   [49|H, 0|H, 0|H, 0, 0],
    "m/84'/0'/0'/0/0":   [84|H, 0|H, 0|H, 0, 0],
}

def check_mnemonic(words, passphrase=""):
    phrase = " ".join(words)
    if not mnemo.check(phrase):
        return None
    seed = Mnemonic.to_seed(phrase, passphrase)
    hits = []
    for name, path in PATHS.items():
        priv = derive(seed, path)
        for comp in (True, False):
            if priv_to_p2pkh(priv, comp) == TARGET:
                hits.append((name, "comp" if comp else "uncomp"))
    return hits

if __name__ == "__main__":
    if len(sys.argv) > 1:
        words = sys.argv[1].split()
        res = check_mnemonic(words)
        if res is None:
            print("Invalid BIP39 checksum.")
        elif res:
            print("MATCH!", res)
        else:
            print("Valid mnemonic, but no derived address matched target.")
    else:
        print("Pass a 12/24-word mnemonic as a quoted argument.")
        print("Target:", TARGET)
