import itertools, hashlib
from itertools import permutations
from fastaes import parse, dec_full, pad_ok
from gsmg_toolkit import ALL_BLOBS
from btc import candidates_from_bytes, check_candidate

BLOBS={n:parse(b) for n,b in ALL_BLOBS.items()}

prime_sp=['','2357','2,3,5,7','primes','prime','23','235','7','seven','2','3','5']
prime_sp+=[''.join(p) for p in permutations('2357')]
prime_sp=list(dict.fromkeys(prime_sp))

SLOTS=[
 ['','9','nine','yellow','Yellow'],
 ['','15','fifteen','blue','Blue'],
 prime_sp,
 ['','matrixsumlist','MatrixSumList','matrix','sumlist'],
 ['','lastwordsbeforearchichoice'],
 ['','yinyang','YinYang','cosmicduality','CosmicDuality','duality','yin','yang'],
 ['','thispassword','thepassword','enter','password'],
]

def printable(pt):
    body=pt[:-pt[-1]] if pad_ok(pt) else pt
    return sum(1 for b in body if 32<=b<127)/max(1,len(body))

def test(P):
    for mode in ('hash','direct'):
        passph = hashlib.sha256(P.encode()).hexdigest() if mode=='hash' else P
        pb=passph.encode()
        for md in ('sha256','md5'):
            for name,(salt,ct) in BLOBS.items():
                pt=dec_full(salt,ct,pb,md)
                if not pad_ok(pt): continue
                # candidate! verify
                for k in candidates_from_bytes(pt):
                    kh=check_candidate(k)
                    if kh:
                        print(f"*** PRIZE *** P={P!r} mode={mode} md={md} blob={name} {kh}")
                        return True
                if printable(pt)>0.85:
                    print(f"printable P={P!r} mode={mode} md={md} blob={name}: {pt[:50]!r}")
    return False

n=0; found=False
for combo in itertools.product(*SLOTS):
    P=''.join(combo)
    if not P: continue
    n+=1
    if test(P): found=True
    if n%50000==0: print(f"...{n} tested")
print(f"DONE: {n} passwords tested across 3 blobs x2 modes x2 KDFs. prize={found}")
