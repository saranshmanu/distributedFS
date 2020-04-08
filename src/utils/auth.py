from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# generate public_key and private_key for assymetric key encryption and decryption
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_key

# encrypt data using public_key
def encrypt_file(data, public_key):
    public_key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )
    encrypted_data = public_key.encrypt(
        data,
        get_padding()
    )
    return encrypted_data

# decrypt data using private_key
def decrypt_file(data, private_key):
    private_key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    decrypted_data = private_key.decrypt(
        data,
        get_padding()
    )
    return decrypted_data

# get padding algorithm for auth
def get_padding():
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
