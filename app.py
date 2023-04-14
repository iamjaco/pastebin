from flask import Flask, render_template, request, redirect, url_for, abort
from flask_bootstrap import Bootstrap
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
Bootstrap(app)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('pastebin.db')
    except Error as e:
        print(e)

    return conn

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pastes (id INTEGER PRIMARY KEY, content TEXT NOT NULL)")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pastes(content) VALUES (?)", (content,))
        conn.commit()
        paste_id = cursor.lastrowid
        conn.close()
        return redirect(url_for('paste', paste_id=paste_id))

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM pastes")
    pastes = cursor.fetchall()
    conn.close()

    return render_template('index.html', pastes=pastes)

    
@app.route('/paste/<int:paste_id>')
def paste(paste_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM pastes WHERE id=?", (paste_id,))
    content = cursor.fetchone()
    conn.close()

    if content:
        return render_template('paste.html', content=content[0], paste_id=paste_id)
    else:
        abort(404)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)