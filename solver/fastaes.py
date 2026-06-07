"""Fast in-process OpenSSL-compatible AES decrypt (EVP_BytesToKey)."""
import base64, hashlib
from Crypto.Cipher import AES

def evp(password: bytes, salt: bytes, md='sha256', klen=32, ilen=16):
    d=b''; prev=b''; h=lambda x: hashlib.new(md,x).digest()
    while len(d)<klen+ilen:
        prev=h(prev+password+salt); d+=prev
    return d[:klen], d[klen:klen+ilen]

def parse(blob_b64):
    raw=base64.b64decode(blob_b64); assert raw[:8]==b'Salted__'
    return raw[8:16], raw[16:]

def dec_full(salt, ct, password, md='sha256'):
    if isinstance(password,str): password=password.encode()
    k,iv=evp(password,salt,md); 
    return AES.new(k,AES.MODE_CBC,iv).decrypt(ct)

def pad_ok(pt):
    p=pt[-1]
    return 1<=p<=16 and pt[-p:]==bytes([p])*p

if __name__=='__main__':
    # validate vs known phase3.2
    blob=open('../phase3-assets/phase3.2-aes.txt').read()
    salt,ct=parse(blob)
    pw=hashlib.sha256("jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple".encode()).hexdigest()
    pt=dec_full(salt,ct,pw)
    print("validate:",pt[:40])
