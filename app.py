from flask import Flask, request, Response, render_template, send_file, make_response, redirect, url_for
from replace_plate import replace_plate
from hide_plate import hide_plate
from tools import verify_file
from PIL import Image
from os import path
import numpy as np
import cv2

app = Flask(__name__)

## Config for the cache problem
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
## Only accept requests that are up to 1MB in size
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template('index.html', title="home", username=None)


@app.route("/api/hide", methods=["POST"])
def post_api_hide():
    file = request.files['image']
    # Verify the file
    error_json = verify_file(file, app.config['UPLOAD_EXTENSIONS'])
    if (error_json != None):
        return error_json
    # Open image
    image = Image.open(file.stream)
    # process the image
    hide_plate(image)
    # build a response dict to send back to client
    return send_file('static/results/result_hide.jpg', mimetype="image/jpg"), 200


@app.route("/api/replace", methods=["POST"])
def post_api_replace():
    file = request.files['image']
    # Verify the file
    error_json = verify_file(file, app.config['UPLOAD_EXTENSIONS'])
    if (error_json != None):
        return error_json
    # Open image
    image = Image.open(file.stream)
    # process the image
    replace_plate(image)
    # build a response dict to send back to client
    return send_file('static/results/result_replace.jpg', mimetype="image/jpg"), 200


@app.route("/result", methods=["POST"])
def post_hide():
    file = request.files['image']
    file_name = file.filename
    # Check if the file input was empty
    if (file_name == ''):
        print("No file!")
        return redirect(url_for('index'))
    # Check extension of the file
    file_ext = path.splitext(file_name)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        print("Wrong image extension!")
        return redirect(url_for('index'))
    # Open image
    image = Image.open(file.stream)
    # process the image
    hide_plate(image)
    replace_plate(image)
    # build a response dict to send back to client
    return render_template('result.html')


# Run flask app
app.run(host="0.0.0.0", port=5000)