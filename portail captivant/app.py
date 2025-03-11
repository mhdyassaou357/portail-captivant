from flask import Flask, render_template, request, redirect, url_for, session  
import json
from waitress import serve

app = Flask(__name__)
app.secret_key = 'ton_secret_key'  # Pour sécuriser les sessions

# Charger les utilisateurs depuis un fichier JSON
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            print("Utilisateurs chargés:", users)  # Debug
            return users
    except FileNotFoundError:
        print("Fichier users.json non trouvé")  # Debug
        return {}
    except json.JSONDecodeError:
        print("Erreur de lecture JSON")  # Debug
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
            return redirect(url_for('dashboard'))
        else:
            print("Échec de connexion: Nom d'utilisateur ou mot de passe incorrect")  # Debug
            return "Nom d'utilisateur ou mot de passe incorrect", 403

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('index'))

    if session['username'] != "yassaou":
        return "Accès interdit", 403

    new_username = request.form.get('new_username', '').strip()
    new_password = request.form.get('new_password', '').strip()

    if not new_username or not new_password:
        return "Nom d'utilisateur ou mot de passe vide", 400

    users = load_users()

    if new_username in users:
        return "L'utilisateur existe déjà", 400

    users[new_username] = new_password
    save_users(users)
    print(f"Nouvel utilisateur ajouté: {new_username}")  # Debug
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    print("Déconnexion réussie")  # Debug
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
