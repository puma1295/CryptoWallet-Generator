import ecdsa, sha3, binascii, os, hashlib, base58
from ecdsa import SigningKey, SECP256k1

keccak = sha3.keccak_256()

priv = SigningKey.generate(curve=SECP256k1)
pub = priv.get_verifying_key().to_string()

keccak.update(pub)
address = keccak.hexdigest()[24:]

banner = ("#################################################\n"
          "## CRYPTOWALLET GENERATOR - By Polina Voronina ##\n"
          "#################################################")
print(banner+'\n')


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d

print('1) Bitcoin')
print('2) Ethereum\n')
choice = raw_input("What wallet would you like to generate? ")
print('')

def ether():
    print("ETH_ADDRESS: 0x" + address)
    print ("PRIVATE_KEY: " + binascii.hexlify(priv.to_string()))

# thanks to nykee-J from reddit for BTC code below.
def bitcoin():
    for n in range(1):
        priv_key = os.urandom(32)
        fullkey = '80' + binascii.hexlify(priv_key).decode()
        sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
        sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))
        sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
        hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
        publ_addr_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
        publ_addr_b = base58.b58encode(publ_addr_a + checksum)
        i = n + 1
        print("BTC_ADDRESS: ", str(i) + ": " + publ_addr_b.decode())
        print("PRIVATE_KEY: ", str(i) + ": " + WIF.decode())

if choice == '1':
    bitcoin()
    print('\n[+] DONE')
elif choice == '2':
    ether()
    print('\n[+] DONE')
else:
    print('\n[-] INVALID CHOICE')
