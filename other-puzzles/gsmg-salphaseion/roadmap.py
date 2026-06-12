#!/usr/bin/env python3
"""
The SalPhaseIon page decodes into a self-describing ROADMAP. This reproduces
every cleanly-decodable embedded instruction label (verified).

Layout of the full SalPhaseIon character stream (single chars, space-separated):

  STR_A (dbbi, 91, a-i)            <- ciphertext, not yet cracked
  binary1  -> "matrixsumlist"       (a=0,b=1, 8-bit ASCII)
  STR_B (faed, 570, a-i)           -> bifid(dbifhceg) -> "btcseed"+90+z+472
  z
  base10 s1 -> "lastwordsbeforearchichoice"   (abcdefghio -> 1234567890, hex->ascii)
  z
  base10 s2 -> "thispassword"
  z
  "shabef"  -> "sha256"   (sha + b,e,f = sha + 2,5,6)
  "ourfirsthintisyourlastcommand"            <- AES password hint
  [AES blob]  (OpenSSL Salted__, 80-byte ciphertext)
  binary2  -> "enter"
  [AES blob cont.]
  "shabef" -> sha256 ; "anstoo" -> "ans too"

"our first hint" (per phase0 notebook) = "follow the white rabbit".
"""
import binascii, hashlib

def bits_to_ascii(ab):           # a=0 b=1
    b="".join('0' if c=='a' else '1' for c in ab if c in 'ab')
    return "".join(chr(int(b[i:i+8],2)) for i in range(0,len(b)-7,8))

def base10_to_ascii(s):          # abcdefghio -> 1234567890, then hex -> ascii
    d=s.translate(str.maketrans('abcdefghio','1234567890'))
    h=hex(int(d))[2:]
    if len(h)%2: h='0'+h
    return binascii.a2b_hex(h).decode()

def shabef():                    # 'shabef' wordplay -> sha256
    return "sha"+ "".join(str("abcdefghi".index(c)+1) for c in "bef")

ROADMAP = {
 "binary1": bits_to_ascii("abbabbababbaaaababbbabaaabbbaabaabbabaababbbbaaaabbbaabbabbbabababbabbababbabbaaabbabaababbbaabbabbbabaa"),
 "binary2": bits_to_ascii("abbaabababbabbbaabbbabaaabbaabababbbaaba"),  # 'enter'
 "s1":      base10_to_ascii("agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"),
 "s2":      base10_to_ascii("cfobfdhgdobdgooiigdocdaoofidh"),
 "shabef":  shabef(),
}

if __name__=="__main__":
    for k,v in ROADMAP.items():
        print(f"{k:8s} -> {v}")
    assert ROADMAP["binary1"]=="matrixsumlist"
    assert ROADMAP["binary2"]=="enter"
    assert ROADMAP["s1"]=="lastwordsbeforearchichoice"
    assert ROADMAP["s2"]=="thispassword"
    assert ROADMAP["shabef"]=="sha256"
    print("\nall roadmap decodings VERIFIED")
