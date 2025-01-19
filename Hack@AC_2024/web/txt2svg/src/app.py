from flask import Flask, render_template, send_file, request
from generatesvg import image
from uuid import uuid4

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    text, font, size, x, y, comment = request.form['text'], request.form['font'], request.form['size'], request.form['x'], request.form['y'], request.form['comment']
    img = image(text, font, size, x, y, comment).generate_svg()

    filename = f"images/{uuid4()}.svg"
    with open(filename, 'w') as f:
        f.write(img.decode('utf-8'))
    f.close()

    return send_file(filename, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)