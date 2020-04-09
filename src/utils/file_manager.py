from src.utils.cryptography import encrypt_file, decrypt_file
from src.utils.auth import get_user_keys, get_user_public_key
from src.utils.ipfs import add_file, get_file
import os

def read_file(file_path):
    try:
        data = open(file_path, 'rb')
        message = data.read()
        data.close()
        return True, message
    except Exception as inst:
        return False, None

def write_file(file_path, message):
    try:
        data = open(file_path, 'wb')
        data.write(message)
        data.close()
        return True
    except Exception as inst:
        return False

def read_file_from_ipfs(file_hash, user_hash, user_password):
    response, status = get_file(file_hash)
    file_path = os.path.join(file_hash)
    keys = get_user_keys(user_hash, user_password)
    private_key = keys["ipfs-object"]["private-key"]
    status, message = read_file(file_path)
    decrypted_data = decrypt_file(message, private_key)
    os.remove(file_path)
    return decrypted_data

def write_file_to_ipfs(file, receiver_hash):
    receiver_public_key = get_user_public_key(receiver_hash)
    filename = file.filename
    file_path = os.path.join(filename)
    file.save(file_path)
    status, message = read_file(file_path)
    encrypted_data = encrypt_file(message, receiver_public_key)
    write_file(file_path, encrypted_data)
    response, status = add_file(file_path)
    os.remove(file_path)
    response["encrypted-data"] = str(encrypted_data)
    return response
