import codecs
import hashlib
import base58
import ecdsa

def pk_to_hash_unc_p2pkh(priv_key): 
    private_key_bytes = codecs.decode(priv_key, 'hex')
        # Get ECDSA public key (paired to given private key)
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
        # Add bitcoin byte '04' that denote UNCOMPRESSED public key
    bitcoin_byte = b'04'
    public_key = bitcoin_byte + key_hex
        # Compute the hash: public key bytes -> sha256 -> RIPEMD160
    public_key_bytes = codecs.decode(public_key, 'hex')
            # Run SHA256 for the public key
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
            # Run ripemd160 for the SHA256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Return RIPEMD160 hash
    return ripemd160_bpk_hex

    # Logic is same, but the public key is COMPRESSED: 
    # used only 32 bytes of the public key with "bitcoin code" set to
    # '03' or '02' based on the sign of the other unused 32 bytes
def pk_to_hash_c_p2pkh(priv_key):
    private_key_bytes = codecs.decode(priv_key, 'hex')

    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    
    if key_bytes[-1] & 1:
        bitcoin_byte = b'03'
    else:
        bitcoin_byte = b'02'
            
    key_bytes =  key_bytes[0:32]    
    key_hex = codecs.encode(key_bytes, 'hex')

    public_key = bitcoin_byte + key_hex

    public_key_bytes = codecs.decode(public_key, 'hex')
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')  

    return ripemd160_bpk_hex

def rp160hash_to_p2pkhAddress(rp160hash):
            # Add network byte
    network_byte = b'00'
    network_bitcoin_public_key = network_byte + rp160hash
    network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
            # Double SHA256 to get checksum
    sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
    sha256_nbpk_digest = sha256_nbpk.digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_nbpk_digest = sha256_2_nbpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    checksum = sha256_2_hex[:8]
            # Concatenate public key and checksum to get the address
    address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
    #address = BTC_operations.base58(address_hex)
    address = base58.b58encode(bytes(bytearray.fromhex(address_hex))).decode('utf-8')
    
    return address

file_names = ['keys.txt','keys_Plus.txt','keys_minus.txt','keys_multiply.txt','keys_noLine.txt',]

for Ifn in range(0, len(file_names)):
    try:
        print(f'Check keys from: {file_names[Ifn]} ...........\n')
        with open(file_names[Ifn]) as fp:
            while True:
                key = fp.readline()  
                if not key:
                    break      
         
                pk = key.rstrip('\n')   
                address_c   = rp160hash_to_p2pkhAddress(pk_to_hash_c_p2pkh(pk))
                if address_c == '1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7':
                    print(f'{address_c}: {pk} | compressed')
                address_unc = rp160hash_to_p2pkhAddress(pk_to_hash_unc_p2pkh(pk))
                if address_unc == '1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7':
                    print(f'{address_unc}: {pk} | UNcompressed')
    except Exception as ex:
        print(ex)
    finally:
        print(f'......keys from: {file_names[Ifn]} ...........CHECKED\n')

