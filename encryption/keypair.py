# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

pem_private_key = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.NoEncryption()
)

pem_public_key = private_key.public_key().public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)

private_encoded = pem_private_key.decode('utf-8')
public_encoded = pem_public_key.decode('utf-8')

print(private_encoded)
print(public_encoded)