from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(name)

@app.route('/')
def hello_world():
    return render_template('hello.html') #COMM2

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        decrypted = f.decrypt(valeur_bytes)
        return f"Valeur décryptée : {decrypted.decode()}"
    except:
        return "Erreur : valeur non déchiffrable"

@app.route('/encrypt/', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()
        key = data['key'].encode()
        message = data['message'].encode()

        f = Fernet(key)
        encrypted_token = f.encrypt(message).decode()
        return jsonify({'encrypted_token': encrypted_token})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/generate-key/', methods=['GET'])
def generate_key():
    key = Fernet.generate_key().decode()
    return jsonify({'key': key})


if name == "main":
  app.run(debug=True)
