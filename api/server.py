from flask import Flask, request
from utils import *

tmp_dir = 'tmp/'
    

app = Flask(__name__)

config = initialize()


@app.route('/upload', methods=['GET', 'POST'])
def upload_file_post():
    if request.method=='GET':
        return handle_get()
    if request.method=='POST':
        return handle_post(request, config)

if __name__ == '__main__':
    app.run(debug=True)