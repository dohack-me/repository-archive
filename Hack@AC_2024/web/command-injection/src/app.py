from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', stuff='')
    
    if request.method == 'POST':
        url = request.form['url']

        if "http://" not in url and "https://" not in url:
            stuff = "I know you tried to do something funny. Stop trying to hack me!\n file:// wont work!"
            return render_template('index.html', stuff=stuff)
        
        stuff = os.popen(f'curl {url}').read()
        return render_template('index.html', stuff=stuff)
    
@app.route('/guide')
def guide():
    return render_template('guide.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)