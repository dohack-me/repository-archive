import sqlite3
from flask import Flask, request
from PIL import Image
from PIL.ExifTags import TAGS
from uuid import uuid4

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <style>
    body {
        background-color: #f2f2f2;
        font-family: "Roboto", sans-serif;
    }
    h1 {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #1a263a;

    }
    input[type=file], input[type=submit] {
        font-family: "Roboto", sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #1a263a;
        border: none;
        border-bottom: 1px solid #1a263a;
        background-color: #f2f2f2;
        padding: 10px;
        margin: 10px;
    }

    .center {
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }
    .center2 {
        text-align: center;
    }
    </style>
    <div class="center">
    <div class="center2">
    <h1>Submit a Picture of a Fruit!</h1>
    <form action="/fruit" method="post" enctype = "multipart/form-data">
    <input type="file" id="myFile" name="filename"><br>
    <input type="submit">
    </form>
    </div>
    </div>
    """
@app.route('/fruit', methods=['POST'])
def fruit():
    file = request.files['filename']

    if file.mimetype == 'image/jpeg':

        filename = uuid4().hex + ".jpg"
        file.save("images/" + filename)

        #return the image data in string format
        img = Image.open("images/" + filename)
        exif_data = img._getexif()

        if exif_data:
            # return the Image Description
            #write exif_data into a dictionary
            exif_dict = {}

            for tag, value in exif_data.items():
                decoded = TAGS.get(tag, tag)
                exif_dict[decoded] = value

            if 'ImageDescription' in exif_dict:
                fruitname = exif_dict['ImageDescription']
                db = sqlite3.connect('database.db')
                cursor = db.cursor()
                statement = f"SELECT color FROM fruits WHERE name='{fruitname}';"
                cursor.execute(statement)
                return str(cursor.fetchall()[0][0])
            
            else:
                # if there is no image description
                return "Cannot Verify Your Picture is A Fruit. Please Add a Image Description to Your Picture."
        else:
            # if there is no exif data
            return "Cannot Verify Your Picture is A Fruit. Please Add a Metadata to Your Picture."
        
    elif file.mimetype == 'image/png':
        return "PNG is not allowed, Please Use JPG"
    else:
        return "File type not allowed"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)