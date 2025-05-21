from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Fichier hello.html requis dans /templates

# Génère une clé globale (utilisée dans /encrypt/<valeur> et /decrypt/<valeur>)
global_key = Fernet.generate_key()
global_f = Fernet(global_key)

@app.route('/encrypt/<string:valeur>', methods=['GET'])
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # str -> bytes
    token = global_f.encrypt(valeur_bytes)  # chiffrement
    return f"Valeur encryptée : {token.decode()}"  # bytes -> str

@app.route('/decrypt/<string:valeur>', methods=['GET'])
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        decrypted = global_f.decrypt(valeur_bytes)
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception:
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

if __name__ == "__main__":
    app.run(debug=True)
