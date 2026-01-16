import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def write(content):
    with open('python-encryption.csv', 'a') as f:
        f.write(str(content))
        f.write('\n')

def generate_key(input_key=None):
    if input_key:
        key = input_key
    else:
        key = AESGCM.generate_key(bit_length=256)

    aesgcm = AESGCM(key)

    return key, aesgcm

data = b"a secret message"
aad = b"authenticated but unencrypted data"

nonce = os.urandom(12)
print(nonce)
save, key = generate_key()

with open('hello.txt', 'rb') as f:
    data = f.read()
    ct = key.encrypt(nonce, data, aad)

# with open('z.key', 'wb') as f:
#     f.write(save)

# with open('hello.txt.bin', 'wb') as f:
    # f.write(ct)

with open('z.key', 'rb') as f:
    data = f.read()
    save, key = generate_key(data)

with open('hello.txt.bin', 'rb') as f:
    ct = f.read()
    zoo = b''
    result = key.decrypt(zoo, ct, aad)

print(result)