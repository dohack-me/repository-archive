from dotenv import dotenv_values
config = dotenv_values(".env")

from flask import Flask, render_template, request, redirect
import sqlite3
import random, string
from bot import Bot

app = Flask(__name__)

blacklist = ['script','javascript','js','onerror','onload','onmouseover','onclick','src','(',')']

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS inputs (uid TEXT, data TEXT)")
con.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        return render_template('index.html')

    elif request.method == "POST":
      userinput = request.form['userinput']
      uid = "".join([random.choice(string.ascii_letters + string.digits) for n in range(25)])

      for trigger in blacklist:
          if trigger in userinput.lower():
              return render_template('return.html', data="The data you entered is dangerous and not allowed.")

      con = sqlite3.connect("database.db")
      cur = con.cursor()
      cur.execute("INSERT INTO inputs VALUES(?, ?)", (uid, userinput))
      con.commit()

      return redirect(f"/retrieve/{uid}")

@app.route('/report', methods=['GET','POST'])
def report():
    if request.method == "GET":
        return render_template('report/index.html')
    elif request.method == "POST":
        thread = Bot(f"http://localhost:{int(config['PORT'])}/retrieve/{request.form['uid']}")
        thread.start()
        return render_template("report/return.html", data=f"it visited this url: /retrieve/{request.form['uid']}")

@app.route('/retrieve/<uid>')
def retrieve(uid):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT data FROM inputs WHERE uid = ?", (uid,))
    data = str(cur.fetchall()[0][0])
    return render_template('return.html', data=data, uid=f"Retrieved with UID: {uid}")

app.run(port=int(config["PORT"]), host="0.0.0.0")