import base64
from src.utils.ipfs import add_json, get_json
from src.utils.cryptography import generate_keys, encrypt_object, decrypt_object

def create_user():
    private_key, public_key = generate_keys() # str object
    encrypted_private_key, password = encrypt_object(private_key) # byte object
    object = {
        "private-key": encrypted_private_key,
        "public-key": public_key
    }
    hash, status = add_json(object)
    return {
        "generated-password": password,
        "user-hash": hash,
        "ipfs-object": object
    }

def get_user_keys(hash, password):
    object, status = get_json(hash)
    public_key = object['public-key']
    encrypted_private_key = object['private-key']
    decrypted_private_key = decrypt_object(encrypted_private_key, password)
    object = {
        "private-key": decrypted_private_key,
        "public-key": public_key
    }
    return {
        "user-hash": hash,
        "ipfs-object": object
    }

def get_user_public_key(hash):
    object, status = get_json(hash)
    public_key = object['public-key']
    return public_key