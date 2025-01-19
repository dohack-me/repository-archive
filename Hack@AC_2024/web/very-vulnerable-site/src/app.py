from flask import Flask, render_template, render_template_string, redirect, url_for, make_response, request
from hashlib import sha256
import sqlite3
import jwt

app = Flask(__name__)
flag = open('flag.txt').read()
secret = 'secret'

@app.route('/')
def index(message=""):
    if request.args.get('message'):
        message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    phash = sha256(password.encode('utf-8')).hexdigest()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    ## Wait how do I use the question mark thing again?
    cur.execute(f"INSERT INTO users (username, password, admin) VALUES ('{username}', '{phash}', 0)")
    conn.commit()

    return redirect(url_for('index', message='Successfully registered!'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    phash = sha256(password.encode('utf-8')).hexdigest()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT admin FROM users WHERE username='{username}' AND password='{phash}'")
    res = cur.fetchone()
    if res:
        ## Not sure if I used a weak secret but meh...
        encoded_jwt = jwt.encode({'username': username, 'admin': res[0]}, secret, algorithm='HS256')
        resp = make_response(redirect(url_for('admin')))
        resp.set_cookie('jwt', encoded_jwt)
        return resp
    else:
       return redirect(url_for('index', message="Invalid username or password!"))
    
@app.route('/admin')
def admin():

    cookie = request.cookies.get('jwt')

    if cookie:

        try:
            decoded_jwt = jwt.decode(cookie, secret, algorithms=['HS256'])
            if decoded_jwt['admin'] == 1:
                return flag
            else:
                templatestring = f"""
                <h1>Hi {decoded_jwt['username']}, you are not an admin!</h1>
                """
                ## What is this - I don't know, I just accepted what copilot gave me lol
                return render_template_string(templatestring)
        except Exception as e:
            return redirect(url_for('index', message=f"Invalid JWT! Perhaps Altered?\n{e}"))
        
    else:
        return redirect(url_for('index', message="You are not logged in!"))
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)