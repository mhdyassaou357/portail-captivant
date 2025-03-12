from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from waitress import serve

app = Flask(__name__)
app.secret_key = 'ton_secret_key'  # Pour sécuriser les sessions

# Charger les utilisateurs depuis un fichier JSON
def load_users():
    try:
        if not os.path.exists('users.json'):
            print("Fichier users.json introuvable.")  # Debug
            return {}
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            print("Utilisateurs chargés:", users)  # Debug
            return users
    except json.JSONDecodeError:
        print("Erreur de lecture du fichier users.json")  # Debug
        return {}

# Sauvegarder les utilisateurs dans un fichier JSON
def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))  # Redirection vers 'index'

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        print(f"Tentative de connexion: {username} / {password}")  # Debug

        users = load_users()
        
        if username in users and users[username] == password:
            session['username'] = username
            print("Connexion réussie!")  # Debug
            if username == "yassaou":
                return redirect(url_for('dashboard'))
            return redirect(url_for('success'))
        else:
            print("Échec de connexion: Nom d'utilisateur ou mot de passe incorrect")  # Debug
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.clear()
    print("Déconnexion réussie")  # Debug
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
