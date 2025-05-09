from flask import Flask, request, redirect, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect('chapitres.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chapitres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matiere TEXT,
            chapitre TEXT,
            auteur TEXT,
            date_ajout TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route: homepage - display form and chapter list
@app.route('/')
def index():
    conn = sqlite3.connect('chapitres.db')
    c = conn.cursor()
    c.execute('SELECT matiere, chapitre, auteur, date_ajout FROM chapitres ORDER BY id DESC')
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

# Route: form submission
@app.route('/add', methods=['POST'])
def add_chapitre():
    matiere = request.form['matiere']
    chapitre = request.form['chapitre']
    auteur = request.form['auteur']
    date_ajout = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('chapitres.db')
    c = conn.cursor()
    c.execute('INSERT INTO chapitres (matiere, chapitre, auteur, date_ajout) VALUES (?, ?, ?, ?)',
              (matiere, chapitre, auteur, date_ajout))
    conn.commit()
    conn.close()

    return redirect('/')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
