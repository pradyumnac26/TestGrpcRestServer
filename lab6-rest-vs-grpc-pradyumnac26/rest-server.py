#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
#!/usr/bin/env python3

##
## Sample Flask REST server implementing methods
##

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
        # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# New dotproduct endpoint
@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        data = request.get_json()  # Get JSON data
        a = np.array(data['a'])  # Convert list 'a' to numpy array
        b = np.array(data['b'])  # Convert list 'b' to numpy array
        dot_product = np.dot(a, b)  # Calculate dot product
        response = {'dotproduct': dot_product}  # Create response dictionary
    except Exception as e:
        response = {'error': str(e)}  # Handle errors
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# New jsonimage endpoint
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        data = request.get_json()  # Get JSON data
        image_data = base64.b64decode(data['image'])  # Decode base64 image
        ioBuffer = io.BytesIO(image_data)  # Create a BytesIO buffer
        img = Image.open(ioBuffer)  # Open the image using PIL
        response = {
            'width': img.size[0],
            'height': img.size[1]
        }  # Create response with image dimensions
    except Exception as e:
        response = {'error': str(e)}  # Handle errors
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
