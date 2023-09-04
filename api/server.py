# the main file for the flask application
from flask import Flask, request
from utils import *

tmp_dir = 'tmp/'
    
app = Flask(__name__)

# read configuration settings from the config file to initialize the server
config = initialize()

# since this is merely a PoC for how the models can be used
# this server is ery simple with only a single handler for a single api method
@app.route('/upload', methods=['GET', 'POST'])
def upload_file_post():
    # call the revelant function to handle a GET request
    if request.method=='GET':
        return handle_get()
    # call the relevant function to handle a POST request
    if request.method=='POST':
        return handle_post(request, config)

# run the server if this is the file passed to the python interpreter
if __name__ == '__main__':
    app.run(debug=True)