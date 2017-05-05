from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
import io
import os
import random

import base64
import cv2
import numpy as np
from PIL import Image

scriptpath = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def index():
    return render_template('test_page.html')

@app.route('/api/v1/featureprocessing',methods=['POST'])
def apiResponse():
    postData = request.get_json()
    imgData = postData['imgData']

    imgData = Image.open(io.BytesIO(base64.b64decode(imgData)))
    imgData = np.array(imgData)

    gray = cv2.cvtColor(imgData, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny( gray, 5, 25)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)

    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(imgData,(x1,y1),(x2,y2),(0,255,0),2)

    pil_img = Image.fromarray(imgData)
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    newImageString = base64.b64encode(buff.getvalue()).decode("utf-8")

    return jsonify({ 'response': newImageString })

if __name__ == "__main__":
    app.run(debug=True)


