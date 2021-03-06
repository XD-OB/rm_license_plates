from flask import Flask, request, Response
from hide_plate import hide_image_plate
import numpy as np
import jsonpickle
import cv2

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_home():
    return "<h1>Welcome<h1><br/><h2>This API is used to hide plates</h2>"

@app.route("/picture", methods=["POST"])
def post_image():
    # convert string of image data to uint8
    nparr = np.fromstring(request.data, np.uint8)
    # decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # process the image
    hide_image_plate(image)
    # build a response dict to send back to client
    response = {
        'message': 'image received. size={}x{}'.format(image.shape[1], image.shape[0])
    }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# Run flask app
app.run(host="0.0.0.0", port=5000)