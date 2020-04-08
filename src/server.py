from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_compress import Compress
from src.settings import URL, SERVER_PORT
from src.utils.ipfs import add_file, get_file, get_ipfs_config
from src.utils.auth import generate_keys, encrypt_file, decrypt_file
import os

app = Flask(__name__)
Compress(app)

@app.route('/generate-keys', methods=['GET'])
def generate():
    private_key, public_key = generate_keys()
    return jsonify({
        "private-key": str(private_key),
        "public-key": str(public_key)
    })

# add file to the IPFS network
@app.route('/add', methods=['POST'])
def add():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(filename)
    file.save(file_path)
    # open the message
    data = open(file_path, 'rb')
    message = data.read()
    data.close()
    # encrypt the data using the generated keys
    private_key, public_key = generate_keys()
    encrypted_data = encrypt_file(message, public_key)
    # write encrypted data
    data = open(file_path + '.encrypted', 'wb')
    data.write(encrypted_data)
    data.close()
    response, status = add_file(filename + '.encrypted')
    os.remove(file_path)
    os.remove(file_path + '.encrypted')
    response["private-key"] = str(private_key)
    response["encrypted-data"] = str(encrypted_data)
    if status:
        return jsonify({
            "success": True,
            "data": response,
            "message": 'Encrypted the data!'
        })
    else:
        return jsonify({
            "status": status,
            "file": filename, 
            "message": 'File Not Found!'
        })

# add file to the IPFS network
@app.route('/get', methods=['GET'])
def get():
    hash = request.json['hash']
    private_key = request.json['private-key']
    response, status = get_file(hash)
    filename = hash
    file_path = os.path.join(filename)
    data = open(file_path, 'rb')
    message = data.read()
    data.close()
    try: 
        decrypted_data = decrypt_file(message, private_key)
        os.remove(file_path)
        if status:
            return jsonify({
                "success": True,
                "data": str(decrypted_data),
                "message": 'Decrypted the data!'
            })
        else:
            return jsonify({
                "status": status,
                "message": 'File Not Found!'
            })
    except Exception as inst:
        os.remove(file_path)
        return jsonify({
            "status": False,
            "data": None,
            "message": str(inst)
        })

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
