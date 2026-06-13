#!/usr/bin/env python3
"""
Exhaustive n-gram password search over the FULL architect 'yourlife' monologue
(the complete cp1141/Beaufort-decoded version, longer than prior attempts),
plus the 2023-02-23 roadmap sentence and the two-doors 'last words'.

Forms per phrase: raw, nospace, sha256(hex/bin/upper). Both 96-byte blobs,
EVP_BytesToKey md5/sha256, AES-128/256.
"""
import base64, hashlib, sys
from Crypto.Cipher import AES

AES1="U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
AES2="QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
P1="U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z"
P2="gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4"
def bf(s): return s+"="*(-len(s)%4)
BLOBS={"salph":base64.b64decode(bf(AES1+AES2)),"p32":base64.b64decode(bf(P1+P2))}

def evp(pw,salt,kl,il,md):
    d=b"";p=b""
    while len(d)<kl+il:p=md(p+pw+salt).digest();d+=p
    return d[:kl],d[kl:kl+il]
def tryd(raw,pwb):
    salt,ct=raw[8:16],raw[16:];o=[]
    for kl in(32,16):
        for md in(hashlib.md5,hashlib.sha256):
            k,iv=evp(pwb,salt,kl,16,md);pt=AES.new(k,AES.MODE_CBC,iv).decrypt(ct);pad=pt[-1]
            if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad and all(32<=b<127 or b in(9,10,13) for b in pt[:-pad]):
                o.append((f"{md().name}{kl*8}",pt[:-pad].decode()))
    return o
def test(pw):
    pwb=pw.encode() if isinstance(pw,str) else pw
    for fb in (pwb,hashlib.sha256(pwb).hexdigest().encode(),hashlib.sha256(pwb).digest(),hashlib.sha256(pwb).hexdigest().upper().encode()):
        for bn,raw in BLOBS.items():
            r=tryd(raw,fb)
            if r:
                print(f"\n[!!! HIT] pw={pw!r} blob={bn} {r}")
                open("MATCH.txt","a").write(f"{pw!r} {bn} {r}\n")
                return True
    return False

YL='yourlifeisthesumofaremainderofanunbalancedequationinherenttotheprogrammingofthispuzzleyouaretheeventualityofananomalywhichdespitemysinceresteffortsihavebeenunabletoeliminatefromwhatisotherwiseaharmonyofmathematicalprecisionwhileitremainsaburdentosedulouslyavoidititisnotunexpectedandthusnotbeyondameasureofcontrolwhichhasledyouinexorablyhereyouyouhaventansweredmyquestionmequiterightinterestingthatwasquickerthantheotherspleaseifyoufindawaytocompletethelastpartofthepuzzletaketheprivatekeyyouveearneditbutpleasetakethistoheartthatwhatawisemanabovehintedatisworthhundredfourtyoftheinvestmentthatswhatusguysatgsmgaretryingtoaccomplishintheendpleasejusthelpusbuilditinsteadofjustwaistingyourlifetimebyhuntingforworthlesspricesandthrophieslikethisimsorrytotellyouthatyouvecomethisfarbutyoullneverfinishthelasttaskiexpectyoutosaybullshitwelldenialisthemostpredictableofallhumanresponsesbutrestassuredthiswillnotbethelasttimeihavedestroyedarestlesssoulandihavebecomeexceedinglyefficientatitthefunctionoftheyouisnowtoreturntothesourcecodesallowingatemporarydisseminationofthecodeyouhopefullycarryreinsertingtheprimebasicsafterwhichyouwillberequiredtoselectfromovertwentythreecipherssixteenencryptionsandorsevenintertwinedpasswordstofindtheactualprivatekeynotethatalsobruteforcingmightberequiredfailuretocomplywiththisprocesswillresultinacataclysmicsystemcrashkillingyourwillpowerwhichcoupledwiththeexterminationofyourwilltoliveandwillultimatelyresultintheextinctionoftheentirenessofyourselfselfgoodluckneverthelessireallyhopeyouretheoneciaobellao'

# split YL into pseudo-words at known boundaries is hard (no spaces); instead
# slide fixed-length windows AND use the spaced versions of the other texts.
ROADMAP="yellow blue primes matrix sumlist last words before archichoice yinyang we wont give away thepassword its in front of your eyes but youre not seeing it very last step is a true give away promised"
LW="the door to your right leads to the source and the salvation of zion the door to your left leads back to the matrix to her and to the end of your species the function of the one is now to return to the source"

def gen():
    seen=set()
    def emit(p):
        if p and p not in seen:
            seen.add(p); return True
        return False
    # YL fixed windows: every start, lengths 4..40
    for i in range(len(YL)):
        for L in range(4,41):
            if i+L>len(YL): break
            p=YL[i:i+L]
            if emit(p): yield p
    # spaced-text n-grams
    for txt in (ROADMAP,LW):
        w=txt.split()
        for i in range(len(w)):
            for n in range(1,13):
                if i+n>len(w): break
                ph=" ".join(w[i:i+n])
                if emit(ph): yield ph
                ph2=ph.replace(" ","")
                if emit(ph2): yield ph2

def main():
    t=0
    for p in gen():
        t+=1
        if test(p): print(f"SOLVED #{t}"); return
        if t%20000==0: print(f"... {t} tested", flush=True)
    print(f"[done] {t} tested, no hit.")

if __name__=="__main__":
    main()
