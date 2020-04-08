from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_compress import Compress
from src.settings import URL, SERVER_PORT
from src.utils.ipfs import add_file, get_ipfs_config
import os

app = Flask(__name__)
Compress(app)

# add file to the IPFS network
@app.route('/add', methods=['POST'])
def add():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(filename)
    file.save(file_path)
    response, status = add_file(filename)
    os.remove(file_path)
    if status:
        return jsonify(response)
    else:
        return jsonify({
            "status": status,
            "file": filename, 
            "message": 'File Not Found!'
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
