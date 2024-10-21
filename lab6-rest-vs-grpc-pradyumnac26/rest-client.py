#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import time
import sys
import base64
import random

def doRawImage(addr, debug=False):
    # prepare headers for http request
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    # send http request with image and receive response
    image_url = addr + '/api/rawimage'
    response = requests.post(image_url, data=img, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    # send http request with image and receive response
    add_url = addr + "/api/add/5/10"
    response = requests.post(add_url, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))

def doDotProduct(addr, debug=False):
    headers = {'content-type': 'application/json'}
    dot_product_url = addr + '/api/dotproduct'

    # Create two random lists of 100 floats between 0 and 1
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    payload = json.dumps({'a': a, 'b': b})

    # Send HTTP request with the payload and receive response
    response = requests.post(dot_product_url, data=payload, headers=headers)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

def doJsonImage(addr, debug=False):
    headers = {'content-type': 'application/json'}
    json_image_url = addr + '/api/jsonimage'

    # Read the image and encode it in base64
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as image_file:
        image_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the payload
    payload = json.dumps({'image': image_string})

    # Send HTTP request with the payload and receive response
    response = requests.post(json_image_url, data=payload, headers=headers)

    if debug:
        print("Response is", response)
        print(json.loads(response.text))

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, dotProduct or jsonImage")
    print(f"and <reps> is the integer number of repetitions for measurement")
    sys.exit(1)

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"http://{host}:5000"
print(f"Running {reps} reps against {addr}")

if cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(addr)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(addr, debug=True)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(addr, debug=True)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
