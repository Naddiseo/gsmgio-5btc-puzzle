#!/usr/bin/env python3
"""
Phase-0 prime structure (verified reproduction of the community 'primes' lead).

The 14x14 colour matrix unravels (spiral: left,bottom,right,top) to binary.
white=0, black=1, and (per phase0) yellow=0, blue=1 -> 'gsmg.io/theseedisplanted'.
The yellow/blue squares are all 8 apart, i.e. at positions that are multiples of
8; dividing by 8 gives the integers 1..24, each assigned blue or yellow.

Verified prime artefacts (the 'reinserting the prime basics' lead):
  * matrix colour counts  0:86 1:86 blue:15 yellow:9  -> 8686159          (prime)
  * dbbi char-freq desc   b25 e18 f10 g10 c8 h8 i5 d4 a3 -> 2518101088543 (prime)
  * concatenation 86861592518101088543                                    (prime)
"""
from collections import Counter

GRID = ("00110b0010110y 11b1001110b011 1101110b001001 0110b000011101 0b1000110y0110 "
        "100110y010y011 100b1100010y00 b11000000010y0 00011b0111110b 11b111y0110001 "
        "1101000y011011 11110010b01100 0b0111010y0110 01b0110110b011").split()

def isprime(n):
    n=int(n)
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True

def matrix_prime():
    c=Counter("".join(GRID))
    return f"{c['0']}{c['1']}{c['b']}{c['y']}"

def dbbi_prime(dbbi):
    c=Counter(dbbi)
    desc=sorted(c.items(), key=lambda kv:(-kv[1],kv[0]))
    return "".join(str(v) for _,v in desc)

BLUE   = {1,2,3,4,6,7,8,11,12,13,14,16,17,20,23}   # positions/8 with blue
YELLOW = {5,9,10,15,18,19,21,22,24}                # positions/8 with yellow

if __name__=="__main__":
    mp=matrix_prime()
    dp=dbbi_prime("dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe")
    print("matrix prime", mp, isprime(mp))
    print("dbbi prime  ", dp, isprime(dp))
    print("combined    ", mp+dp, isprime(mp+dp))
    assert sorted(BLUE|YELLOW)==list(range(1,25))
    primes=[p for p in range(2,25) if isprime(p)]
    print("primes<=24:", primes)
    print("  blue primes  :", [p for p in primes if p in BLUE])
    print("  yellow primes:", [p for p in primes if p in YELLOW])
