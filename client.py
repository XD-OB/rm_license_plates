from __future__ import print_function
import requests
import json
import cv2

addr = 'http://localhost:5000'
url = addr + '/picture'

# prepare headers for http request
content_type = 'multipart/form-data'
headers = {'content-type': content_type}

image = {'image': open('./images/souad.jpg', 'rb')}
# send http request with image and receive response
response = requests.post(url, files=image, headers=headers)