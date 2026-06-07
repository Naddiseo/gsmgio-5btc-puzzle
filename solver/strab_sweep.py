"""Exhaustive-ish transformation sweep of the two unsolved SalPhaseIon base-9
strings (STR_A, STR_B), under the 'matrixsumlist' instruction and a duality lens.

Every produced candidate is (a) scored for English and (b) tried as an AES
password against all three blobs, with results run through the address oracle.
"""
import binascii, hashlib
from gsmg_toolkit import SALPH_STR_A, SALPH_STR_B, ALL_BLOBS, try_password, looks_like_plaintext
from btc import candidates_from_bytes, check_candidate

WORDS = set("""the be to of and a in that have it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us prime primes matrix sum list yellow blue enter password key private bitcoin satoshi cipher half better source code answer correct congratulations seed planted matrixsumlist""".split())

def eng(s):
    s=s.lower()
    return sum(1 for w in WORDS if len(w)>=3 and w in s)

def printable_ratio(s):
    return sum(1 for c in s if 32<=ord(c)<127)/max(1,len(s))

CANDS={}  # text -> source label
def add(label,s):
    if s and isinstance(s,str):
        CANDS.setdefault(s,label)

def digits(S,base1=True):
    off=1 if base1 else 0
    return [ord(c)-ord('a')+off for c in S]

def to_ascii_from_int(num):
    h=hex(num)[2:]
    if len(h)%2:h='0'+h
    try:return binascii.unhexlify(h).decode('latin-1')
    except:return None

def transforms(S,label):
    n=len(S)
    for b1 in (True,False):
        d=digits(S,b1); tag=f'{label}{"1" if b1 else "0"}'
        # decimal -> hex -> ascii
        add(f'{tag}-decint', to_ascii_from_int(int(''.join(str(x) for x in d))) if all(0<=x<=9 for x in d) else None)
        # base9 -> bytes
        num=0
        for x in d: num=num*9+(x if not b1 else x-1)  # base9 needs 0-8
        add(f'{tag}-base9', to_ascii_from_int(num) if num else None)
        # pairs decimal -> ascii
        for o in (0,1):
            ds=d[o:]
            add(f'{tag}-pair{o}', ''.join(chr(ds[i]*10+ds[i+1]) for i in range(0,len(ds)-1,2) if 32<=ds[i]*10+ds[i+1]<127))
        # cumulative sum mod26 -> letters
        c=0;out=[]
        for x in d: c=(c+x)%26; out.append(chr(c%26+97))
        add(f'{tag}-cumsum', ''.join(out))
        # consecutive diff mod26
        add(f'{tag}-diff', ''.join(chr((d[i+1]-d[i])%26+97) for i in range(len(d)-1)))
        # matrix sums (all divisors)
        for rows in [r for r in range(2,n) if n%r==0]:
            cols=n//rows
            M=[d[i*cols:(i+1)*cols] for i in range(rows)]
            rowsum=[sum(r) for r in M]
            colsum=[sum(M[r][c] for r in range(rows)) for c in range(cols)]
            for nm,sm in (('rs',rowsum),('cs',colsum)):
                add(f'{tag}-{rows}x{cols}-{nm}-z26', ''.join(chr((v-1)%26+97) for v in sm))
                if all(32<=v<127 for v in sm):
                    add(f'{tag}-{rows}x{cols}-{nm}-asc', ''.join(chr(v) for v in sm))
            # transposition: read matrix column-major -> digits -> decint
            colmajor=[M[r][c] for c in range(cols) for r in range(rows)]
            add(f'{tag}-{rows}x{cols}-transp-decint', to_ascii_from_int(int(''.join(str(x) for x in colmajor))) if all(0<=x<=9 for x in colmajor) else None)

def duality(A,B):
    """Combine the two halves: align B against repeated A and combine mod 9/10."""
    da=digits(A,True); db=digits(B,True)
    # repeat A over B
    for mod,name in ((9,'m9'),(10,'m10')):
        for op,opn in ((lambda x,y:(x+y)%mod,'add'),(lambda x,y:(x-y)%mod,'sub'),(lambda x,y:(y-x)%mod,'rsub')):
            comb=[op(da[i%len(da)],db[i]) for i in range(len(db))]
            # decode combined as decint
            add(f'AB-{name}-{opn}-decint', to_ascii_from_int(int(''.join(str(x%10) for x in comb))) if comb else None)
            # as letters
            add(f'AB-{name}-{opn}-z26', ''.join(chr(x%26+97) for x in comb))

transforms(SALPH_STR_A,'A')
transforms(SALPH_STR_B,'B')
duality(SALPH_STR_A,SALPH_STR_B)

print(f"generated {len(CANDS)} candidate strings")
# English-looking
print("\n== English-scored (score>=3 or short+printable) ==")
shown=0
for s,lab in sorted(CANDS.items(), key=lambda kv:-eng(kv[0])):
    sc=eng(s)
    if sc>=3 and printable_ratio(s)>0.8:
        print(f"  [{lab}] score={sc} {s[:90]!r}"); shown+=1
        if shown>20: break
if not shown: print("  (none scored >=3)")

# AES oracle: try every candidate as a password against all blobs
print("\n== AES/oracle check of all candidates ==")
hits=0
for s,lab in CANDS.items():
    for blob_name,blob in ALL_BLOBS.items():
        for md in ('sha256','md5'):
            pt=try_password(blob,s,md=md)
            if pt is None: continue
            kh=None
            for k in candidates_from_bytes(pt):
                kh=check_candidate(k)
                if kh: break
            if kh:
                print(f"  *** PRIZE KEY *** [{lab}] pw={s!r} blob={blob_name} -> {kh}"); hits+=1
            elif looks_like_plaintext(pt):
                print(f"  printable [{lab}] pw={s!r} blob={blob_name}/{md} -> {pt[:50]!r}"); hits+=1
print(f"oracle hits: {hits}")
