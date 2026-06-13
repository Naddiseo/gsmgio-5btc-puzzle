import base64,hashlib
from Crypto.Cipher import AES
AES1='U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z'
AES2='QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
def bf(s):return s+'='*(-len(s)%4)
COSMIC=''.join(open('cosmic_duality_blob.txt').read().split())
BLOBS={'salph':base64.b64decode(bf(AES1+AES2)),'cosmic':base64.b64decode(bf(COSMIC))}
def evp(pw,salt,kl,il,md):
    d=b'';p=b''
    while len(d)<kl+il:p=md(p+pw+salt).digest();d+=p
    return d[:kl],d[kl:kl+il]
def tryc(answer):
    pwb=hashlib.sha256(answer.encode()).hexdigest().encode()
    out=[]
    for bn,raw in BLOBS.items():
        salt,ct=raw[8:16],raw[16:]
        k,iv=evp(pwb,salt,32,16,hashlib.sha256)
        pt=AES.new(k,AES.MODE_CBC,iv).decrypt(ct);pad=pt[-1]
        if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad:
            body=pt[:-pad]
            pr=sum(1 for b in body if 32<=b<127 or b in(9,10,13))/max(1,len(body))
            if pr>=0.95 or body[:1] in (b'5',b'K',b'L') or body[:8]==b'Salted__':
                out.append((bn,pr,body))
    return out
n=0;hits=0
with open('/tmp/words_alpha.txt') as f:
    for line in f:
        w=line.strip()
        if not w: continue
        for variant in (w, w.capitalize(), w.upper()):
            n+=1
            r=tryc(variant)
            for bn,pr,body in r:
                hits+=1
                print(f'[HIT] {bn} answer={variant!r} pr={pr:.2f}: {body[:100]!r}',flush=True)
        if n%200000==0: print('...',n,flush=True)
print('done, tested',n,'hits',hits)
