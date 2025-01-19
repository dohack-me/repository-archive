from flask import Flask, request, send_from_directory
import re
import tarfile

from io import BytesIO
import os
import base64



app = Flask(__name__)



@app.route('/')
def index():
    # eg image url accepted: https://images.unsplash.com/photo-1707920266055-3c74a15fb947?q=80&w=2574&auto=format&fit=crop
    return 'welcome to my quote-image tagger! I use this to tag the nice stuffs and quotes that i collect with an image that i think suits it! All my images only come from unsplash as its the best free image site! Give it a try!'


@app.route('/download', methods=['GET'])
def download():
    _regex = re.compile(r'[a-zA-Z0-9]+')
    file = request.args.get('file')
    if not _regex.fullmatch(file):
        return 'Invalid file name'

    else:
        return send_from_directory('signed_files', f'{file}.tar')

@app.route('/sign', methods=['GET'])
def sign():
    file_to_sign = request.args.get('file')
    filename = request.args.get('filename')   
    url = base64.b64decode(request.args.get('url'))
    _regex = re.compile(r'[a-zA-Z0-9]+')


    if not _regex.fullmatch(file_to_sign) or not _regex.fullmatch(filename):
        return 'Invalid file name'
    else:
        try:

            with open(f'stuffs/{file_to_sign}.txt', 'r') as f:
                contents = f.read()
            with tarfile.open(f"signed_files/{filename}.tar", "w") as tf:
                byteobj = BytesIO(b'Quote tagger generated output: ' + contents.encode() + b' url: ' + url + b'')
                tarinfo = tarfile.TarInfo(f'{file_to_sign}.txt')
                tarinfo.size = len(byteobj.getbuffer())
                tf.addfile(tarinfo, fileobj = byteobj)
            
            # check if the tarfile contains an unsplash url...im loyal to this service!
            with tarfile.open(f"signed_files/{filename}.tar", "r") as tf:
                member = tf.extractfile(f'{file_to_sign}.txt')
                contents = member.read().decode()
                _filter = re.compile(r'(https|http)+:\/\/(?:[^\/]+\.)*images\.unsplash\.com\/photo([-|[a-z0-9A-Z])+\?(.*=.*)+')
                if not _filter.search(contents):
                    os.remove(f"signed_files/{filename}.tar")
                    return 'Invalid url! I told you to only use unsplash >:('
                else:
                    # prevent thiefs from accessing my flag
                    _filter = re.compile(r'ACSI{.*}')
                    if _filter.search(contents):
                        os.remove(f"signed_files/{filename}.tar")
                        return 'I told you NOT to steal my precious flag!'
            return 'File signed successfully'

        except:
            return 'Something went wrong :('

if __name__ == '__main__':
    app.run()