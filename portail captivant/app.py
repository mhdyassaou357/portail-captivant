from flask import Flask, render_template, request, redirect, url_for, session
import json
from waitress import serve

app = Flask(__name__)
app.secret_key = 'ton_secret_key'  # Pour sécuriser les sessions

# Charger les utilisateurs depuis un fichier JSON
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Sauvegarder les utilisateurs dans un fichier JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users and users[username] == password:  # Comparaison directe des mots de passe
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 403

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session['username'] != "yassaou":
        return "Accès interdit", 403  # Seul l'admin peut ajouter un utilisateur

    new_username = request.form['new_username']
    new_password = request.form['new_password']

    users = load_users()

    if new_username in users:
        return "L'utilisateur existe déjà", 400

    users[new_username] = new_password  # Enregistrer le mot de passe en clair
    save_users(users)

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
