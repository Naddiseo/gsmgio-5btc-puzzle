#!/usr/bin/env python3
"""
Unified password attack against ALL THREE OpenSSL/CryptoJS blobs, now including
the byte-accurate large 'Cosmic Duality' ciphertext (cosmic_duality_blob.txt).

Candidate sources: roadmap labels & 2023-02-23 sentence, full architect
'yourlife' windows, two-doors 'last words', matrixsumlist outputs, yellow/blue
prime char-picks over the phase-0 URL, keyword roundup, prime numbers, page URL
hash. Forms: raw / sha256{hex,bin,HEX} / md5hex. KDF: EVP_BytesToKey
{md5,sha256} x AES-{128,256}.
"""
import base64, hashlib, os
from Crypto.Cipher import AES

AES1="U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2="QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P1="U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P2="gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"
def bf(s): return s+"="*(-len(s)%4)
HERE=os.path.dirname(os.path.abspath(__file__))
COSMIC="".join(open(os.path.join(HERE,"cosmic_duality_blob.txt")).read().split())
BLOBS={
 "salph":  base64.b64decode(bf(AES1+AES2)),
 "p32":    base64.b64decode(bf(P1+P2)),
 "cosmic": base64.b64decode(bf(COSMIC)),
}

def evp(pw,salt,kl,il,md):
    d=b"";p=b""
    while len(d)<kl+il:p=md(p+pw+salt).digest();d+=p
    return d[:kl],d[kl:kl+il]
def tryd(raw,pwb):
    salt,ct=raw[8:16],raw[16:];o=[]
    for kl in(32,16):
        for md in(hashlib.md5,hashlib.sha256):
            k,iv=evp(pwb,salt,kl,16,md)
            pt=AES.new(k,AES.MODE_CBC,iv).decrypt(ct);pad=pt[-1]
            if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad and all(32<=b<127 or b in(9,10,13) for b in pt[:-pad]):
                o.append((f"{md().name}{kl*8}",pt[:-pad]))
    return o
def test(pw,label):
    pwb=pw.encode() if isinstance(pw,str) else pw
    forms=[(pwb,"raw"),
           (hashlib.sha256(pwb).hexdigest().encode(),"shahex"),
           (hashlib.sha256(pwb).digest(),"shabin"),
           (hashlib.sha256(pwb).hexdigest().upper().encode(),"shaHEX"),
           (hashlib.md5(pwb).hexdigest().encode(),"md5hex")]
    for fb,fn in forms:
        for bn,raw in BLOBS.items():
            for kdf,pt in tryd(raw,fb):
                print(f"\n[!!! HIT] {label!r} form={fn} blob={bn} {kdf}")
                print(f"  PT[:200]={pt[:200]!r}")
                open(os.path.join(HERE,"MATCH.txt"),"a").write(f"{label!r} {fn} {bn} {kdf}\n{pt!r}\n\n")
                return True
    return False

def primes_upto(n): return [p for p in range(2,n+1) if all(p%i for i in range(2,int(p**.5)+1))]
URL="gsmg.io/theseedisplanted"; SEED="theseedisplanted"
BLUE_ORD=[1,2,3,4,6,7,8,11,12,13,14,16,17,20,23]; YELLOW_ORD=[5,9,10,15,18,19,21,22,24]
P24=primes_upto(24); BP=[p for p in P24 if p in BLUE_ORD]; YP=[p for p in P24 if p in YELLOW_ORD]
def pick(s,idxs,off=1): return "".join(s[i-off] for i in idxs if 0<=i-off<len(s))
ROADMAP=("yellow blue primes matrix sumlist last words before archichoice yinyang we wont give away "
         "thepassword its in front of your eyes but youre not seeing it very last step is a true give away promised")
LW=("the door to your right leads to the source and the salvation of zion the door to your left leads back "
    "to the matrix to her and to the end of your species the function of the one is now to return to the source")
YL='yourlifeisthesumofaremainderofanunbalancedequationinherenttotheprogrammingofthispuzzleyouaretheeventualityofananomalywhichdespitemysinceresteffortsihavebeenunabletoeliminatefromwhatisotherwiseaharmonyofmathematicalprecisionwhileitremainsaburdentosedulouslyavoidititisnotunexpectedandthusnotbeyondameasureofcontrolwhichhasledyouinexorablyhereyouyouhaventansweredmyquestionmequiterightinterestingthatwasquickerthantheotherspleaseifyoufindawaytocompletethelastpartofthepuzzletaketheprivatekeyyouveearneditbutpleasetakethistoheartthatwhatawisemanabovehintedatisworthhundredfourtyoftheinvestmentthatswhatusguysatgsmgaretryingtoaccomplishintheendpleasejusthelpusbuilditinsteadofjustwaistingyourlifetimebyhuntingforworthlesspricesandthrophieslikethisimsorrytotellyouthatyouvecomethisfarbutyoullneverfinishthelasttaskiexpectyoutosaybullshitwelldenialisthemostpredictableofallhumanresponsesbutrestassuredthiswillnotbethelasttimeihavedestroyedarestlesssoulandihavebecomeexceedinglyefficientatitthefunctionoftheyouisnowtoreturntothesourcecodesallowingatemporarydisseminationofthecodeyouhopefullycarryreinsertingtheprimebasicsafterwhichyouwillberequiredtoselectfromovertwentythreecipherssixteenencryptionsandorsevenintertwinedpasswordstofindtheactualprivatekeynotethatalsobruteforcingmightberequiredfailuretocomplywiththisprocesswillresultinacataclysmicsystemcrashkillingyourwillpowerwhichcoupledwiththeexterminationofyourwilltoliveandwillultimatelyresultintheextinctionoftheentirenessofyourselfselfgoodluckneverthelessireallyhopeyouretheoneciaobellao'
RS=[6,10,8,7,6,6,5,4,9,9,7,8,7,9]; CS=[8,10,8,10,8,7,3,6,7,5,9,6,6,8]
URLHASH="89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"

def gen():
    seen=set()
    def emit(p):
        if not p: return
        k=p if isinstance(p,str) else p.decode('latin1')
        if k not in seen: seen.add(k); return p
    out=[]
    def add(p):
        r=emit(p)
        if r is not None: out.append(r)
    # keywords / labels / titles
    for kw in ["yinyang","yingyang","cosmicduality","CosmicDuality","SalPhaseIon","salphaseion",
               "thepassword","thispassword","matrixsumlist","lastwordsbeforearchichoice",
               "yellowblueprimes","salvation","salvationofzion","thesalvationofzion",
               "returntothesource","followthewhiterabbit","thematrixhasyou","reinserttheprimebasics",
               "reinsertingtheprimebasics","theprimebasics","enter","anstoo","ourfirsthintisyourlastcommand",
               URL,SEED,URLHASH,URLHASH.upper(),"theseedisplanted","gsmgio5btcpuzzlechallenge",
               "GSMGIO5BTCPUZZLECHALLENGE"]:
        add(kw)
    # prime numbers
    for pn in ["8686159","2518101088543","86861592518101088543"]:
        add(pn)
    # yellow/blue prime picks
    for nm,s in [("url",URL),("seed",SEED)]:
        for off in (0,1):
            for idxs in (BP,YP,sorted(BP+YP),BLUE_ORD,YELLOW_ORD):
                add(pick(s,idxs,off))
    # matrixsumlist
    for lst in (RS,CS,RS+CS,CS+RS):
        for sep in ("",",", " ","-"): add(sep.join(map(str,lst)))
        add(bytes(lst))
    # YL windows
    for i in range(len(YL)):
        for L in range(4,41):
            if i+L>len(YL): break
            add(YL[i:i+L])
    # spaced ngrams
    for txt in (ROADMAP,LW):
        w=txt.split()
        for i in range(len(w)):
            for n in range(1,13):
                if i+n>len(w): break
                ph=" ".join(w[i:i+n]); add(ph); add(ph.replace(" ",""))
    return out

def main():
    print("blobs:")
    for n,r in BLOBS.items(): print(f"  {n}: salt={r[8:16].hex()} ct={len(r)-16} blocks={(len(r)-16)//16}")
    c=gen(); print(f"{len(c)} unique candidates")
    for i,pw in enumerate(c):
        lbl=(pw if isinstance(pw,str) else pw.decode('latin1'))[:24]
        if test(pw,lbl): print(f"SOLVED #{i}"); return
        if i%10000==0 and i: print(f"... {i}", flush=True)
    print("[done] no hit.")

if __name__=="__main__": main()
