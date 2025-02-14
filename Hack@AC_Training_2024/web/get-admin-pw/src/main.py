import sqlite3
from flask import Flask, request

conn = sqlite3.connect('example.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT);')
cur.execute('INSERT INTO user (name, password) VALUES (?, ?)', ('admin', 'hackac'))
conn.commit()

def login(username, password):
    statement = f"SELECT * FROM user WHERE name='{username}' AND password='{password}'"

    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    cur.execute(statement, )
    
    return cur.fetchone() is not None

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Try to get admin password - username:admin pw:???? (impossible)</h1>
      <form action="/login" method="post">
        <input name="username" type="text" />
        <input name="password" type="text" />
        <input type="submit" />
      </form>
    """

@app.route('/login', methods=['POST'])
def goIn():
    username = request.form['username']
    password = request.form['password']
    if login(username, password):
        return "Noted with thanks!"
    return "Invalid username or password"
    
app.run(host='0.0.0.0', port=5050)