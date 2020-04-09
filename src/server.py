from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_compress import Compress
from src.settings import URL, SERVER_PORT
from src.utils.ipfs import add_file, get_file, get_ipfs_config
from src.utils.cryptography import generate_keys, encrypt_file, decrypt_file
from src.utils.file_manager import read_file, write_file
from src.utils.auth import create_user, get_user_keys, get_user_public_key

import os

app = Flask(__name__)
Compress(app)


def create_response(error, data, message):
    return {
        "success": not(error),
        "message": message,
        "data": data
    }


@app.route('/generate-keys', methods=['GET'])
def generate():
    private_key, public_key = generate_keys()
    return jsonify({
        "private-key": str(private_key),
        "public-key": str(public_key)
    })

@app.route('/create-user', methods=['GET'])
def create():
    try:
        response = create_user()
        return jsonify(create_response(False, response, 'Successfully Created User!'))
    except Exception as inst:
        return jsonify(create_response(True, None, str(inst)))

@app.route('/get-user-keys', methods=['GET'])
def get_keys():
    try:
        hash = request.json['hash']
        password = request.json['password']
        response = get_user_keys(hash, password)
        return jsonify(create_response(False, response, 'Successfully Fetched User Keys from the IPFS network!'))
    except Exception as inst:
        return jsonify(create_response(True, None, str(inst)))

# add file to the IPFS network
@app.route('/add', methods=['POST'])
def add():
    file = request.files['file']
    receiver_hash = request.form['receiver-hash']
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
    if status:
        return jsonify(create_response(False, response, 'Encrypted the data!'))
    else:
        return jsonify(create_response(True, {"file": file_path}, 'File Not Found!'))

# add file to the IPFS network
@app.route('/get', methods=['GET'])
def get():
    file_hash = request.json['file-hash']
    user_hash = request.json['user-hash']
    user_password = request.json['user-password']
    response, status = get_file(file_hash)
    file_path = os.path.join(file_hash)
    try:
        keys = get_user_keys(user_hash, user_password)
        private_key = keys["ipfs-object"]["private-key"]
        status, message = read_file(file_path)
        decrypted_data = decrypt_file(message, private_key)
        os.remove(file_path)
        return jsonify(create_response(False, str(decrypted_data), 'Decrypted the data!'))
    except Exception as inst:
        os.remove(file_path)
        return jsonify(create_response(True, None, 'Error while fetching the data!'))

# get config of IPFS network
@app.route('/config', methods=['GET'])
def config():
    return jsonify(get_ipfs_config())

# 404 path not found error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "code": 404,
        "message": 'Not Found!'
    })

# 405 method not found error handling
@app.errorhandler(405)
def page_not_found(e):
    return jsonify({
        "code": 405,
        "message": 'Method not allowed!'
    })


host = URL
port = SERVER_PORT


def server_init():
    app.run(debug=True, host=host, port=port)
