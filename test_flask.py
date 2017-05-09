from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
application = Flask(__name__)
CORS(application)
import io
import os
import random

import base64
import cv2
import numpy as np
from PIL import Image

scriptpath = os.path.dirname(os.path.realpath(__file__))

@application.route('/')
def index():
    return render_template('test_page.html')

def arrayIntoBase64String(imgArr):
    pil_img = Image.fromarray(imgArr)
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")

def getLines(grayImg, edges, lineRho, lineTheta, lineThreshold, lineMinLength, lineMaxGap):
    lines = cv2.HoughLinesP(edges, lineRho, lineTheta, lineThreshold, minLineLength=lineMinLength,maxLineGap=lineMaxGap)
    grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2RGB)

    if lines is None:
        return grayImg
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(grayImg,(x1,y1),(x2,y2),(0,255,0),2)

    return grayImg

def getCorners(grayImg, cornerBlockSize, cornerKSize, cornerK):
    grayImg = np.float32(grayImg)
    dst = cv2.cornerHarris(grayImg,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.
    grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2RGB)
    grayImg[dst>0.01*dst.max()]=[0,0,255]
    #Convert RGB grayscale and add one more zero column to each pixel
    zeros = np.zeros((grayImg.shape[0], grayImg.shape[1]))
    cornerImg = np.dstack((grayImg, zeros))
    cornerImg = np.uint8(cornerImg)
    return cornerImg

@application.route('/api/v1/featureprocessing',methods=['POST'])
def apiResponse():
    postData = request.get_json()

    imgData = postData['imgData']
    imgData = Image.open(io.BytesIO(base64.b64decode(imgData)))
    imgData = np.array(imgData)
    grayImg = cv2.cvtColor(imgData, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny( grayImg, 
        float(postData['edgeMinVal']), 
        float(postData['edgeMaxVal']) )

    edgeImgBase64 = arrayIntoBase64String(edges)
    lineImgBase64 = arrayIntoBase64String(getLines(grayImg, edges,
        float(postData['lineRho']),
        float(postData['lineTheta']),
        int(postData['lineThreshold']),
        float(postData['lineMinLength']),
        float(postData['lineMaxGap']) ))
    cornerImgBase64 = arrayIntoBase64String(getCorners(grayImg, 
        int(postData['cornerBlockSize']),
        int(postData['cornerKSize']),
        float(postData['cornerK']) ))

    return jsonify({'edgeImg': edgeImgBase64, 'lineImg': lineImgBase64, 'cornerImg': cornerImgBase64 })

if __name__ == "__main__":
    application.run(debug=True)




# im = Image.open('/Users/cloudlife/Desktop/train_32.jpg')
# im = np.array(im)
# grayImg = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# graycorners = getCorners(grayImg)

# print(graycorners.shape)

# zeroMatrix = np.zeros( (graycorners.shape[0], graycorners.shape[1]) )

# done = np.dstack((graycorners, zeroMatrix))
# print(done.shape)
# done = np.uint8(done)
# that = arrayIntoBase64String(done)