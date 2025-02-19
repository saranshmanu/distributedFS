from cryptography.fernet import Fernet
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import BLAKE2s
from binascii import hexlify

# generate public_key and private_key for assymetric key encryption and decryption
def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    private_key = private_key.export_key().decode()
    public_key = public_key.export_key().decode()
    return private_key, public_key

# encrypt data using public_key
def encrypt_file(data, public_key):
    public_key = bytes(public_key, encoding='utf8')
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key=public_key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

# decrypt data using private_key
def decrypt_file(data, private_key):
    private_key = bytes(private_key, encoding='utf8')
    private_key = RSA.import_key(bytes(private_key))
    decrypt = PKCS1_OAEP.new(key=private_key)
    decrypted_data = decrypt.decrypt(data)
    return decrypted_data

def create_hash(text):
    h_obj = BLAKE2s.new(digest_bits=256)
    h_obj.update(text.encode())
    return h_obj.hexdigest()
 
# encrypt data using key
def encrypt_object(message):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted = cipher_suite.encrypt(message.encode())
    return encrypted.decode(), key.decode()

# decrypt data using key
def decrypt_object(message, key):
    cipher_suite = Fernet(key.encode())
    decrypted = cipher_suite.decrypt(message.encode())
    return decrypted.decode()
