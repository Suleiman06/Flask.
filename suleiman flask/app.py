from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

# Database-fil
DATABASE = 'database.db'

# Funksjon for å koble til databasen
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Lukk databasetilkobling etter hver forespørsel
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Hovedside / Login-side
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return "Innlogging vellykket!"  # Kan byttes ut med en omdirigering til en annen side
        else:
            return "Feil brukernavn eller passord!"
    return render_template('login.html')

# Registrere ny bruker
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Brukernavn er allerede tatt!"
    return render_template('register.html')

# Vise alle brukere
@app.route('/view_users')
def view_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * username FROM users")
    users = cursor.fetchall()
    return render_template('view_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
