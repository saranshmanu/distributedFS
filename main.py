from flask import Flask, redirect, url_for, request, render_template, after_this_request
from flask_compress import Compress
from src.settings import URL, SERVER_PORT
from dotenv import load_dotenv

app = Flask(__name__)
Compress(app)

dotenv_path = '.env'
load_dotenv(dotenv_path)

@app.route('/')
def render():
    return 'hello'

@app.errorhandler(404)
def page_not_found(e):
    return 'NOT FOUND', 404

host = URL
port = SERVER_PORT

if __name__ == '__main__':
    print(host, port)
    app.run(debug=True, host=host, port=port)

