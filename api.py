from flask import Flask, request, Response, jsonify, render_template, send_file
from hide_plate import hide_image_plate
import numpy as np
from PIL import Image
import cv2

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', title="home", username=None)

@app.route("/picture", methods=["POST"])
def post_image():
    file = request.files['image']
    image = Image.open(file.stream)
    # process the image
    hide_image_plate(image)
    # build a response dict to send back to client
    #return send_file('./images/image_hidden.jpg', mimetype="image/jpg")
    return jsonify({'msg': 'success', 'size': [image.width, image.height]})


# Run flask app
app.run(host="0.0.0.0", port=5000)