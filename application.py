# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import datetime
import string
import traceback
import requests
import copy
import io
import re
import base64
from functools import wraps

import flask
from flask import request, Response, send_file, render_template, make_response, flash
from flask import session, redirect, send_from_directory, jsonify, _request_ctx_stack
from flask import Flask
from flask_cors import CORS, cross_origin
from werkzeug.local import LocalProxy

import cv2
import numpy as np
from PIL import Image

# Getting server filepath
scriptpath = os.path.dirname(os.path.realpath(__file__))

# Default config vals
FLASK_DEBUG = 'false' if os.environ.get('FLASK_DEBUG') is None else os.environ.get('FLASK_DEBUG')

# Create the Flask app
application = flask.Flask(__name__)
application.secret_key = '@thisworks'
CORS(application)

# Load config values specified above
application.config.from_object(__name__)

# Load configuration vals from a file
application.config.from_envvar('APP_CONFIG', silent=True)

# Only enable Flask debugging if an env var is set to true
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

def arrayIntoBase64String(imgArr):
    pil_img = Image.fromarray(imgArr)
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")

def getLines(grayImg, edges, lineRho, lineTheta, lineThreshold, lineMinLength, lineMaxGap):
    lines = cv2.HoughLinesP(edges, lineRho, lineTheta, lineThreshold, minLineLength=lineMinLength,maxLineGap=lineMaxGap)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(grayImg,(x1,y1),(x2,y2),(0,255,0),2)

    return grayImg

def getCorners(grayImg, cornerBlockSize, cornerKSize, cornerK):
    grayImg = np.float32(grayImg)
    dst = cv2.cornerHarris(grayImg, cornerBlockSize, cornerKSize, cornerK)
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
    grayImg2 = copy.copy(grayImg)

    edges = cv2.Canny( grayImg, 
        float(postData['edgeMinVal']), 
        float(postData['edgeMaxVal']) )

    edgeImgBase64 = arrayIntoBase64String(edges)
    lineImgBase64 = arrayIntoBase64String(getLines(grayImg, edges,
        float(postData['lineRho']),
        float(postData['lineTheta']),
        int(float(postData['lineThreshold'])),
        float(postData['lineMinLength']),
        float(postData['lineMaxGap']) ))
    cornerImgBase64 = arrayIntoBase64String(getCorners(grayImg2, 
        int(float(postData['cornerBlockSize'])),
        int(float(postData['cornerKSize'])),
        float(postData['cornerK']) ))

    return jsonify({'edgeImg': edgeImgBase64, 'lineImg': lineImgBase64, 'cornerImg': cornerImgBase64 })


# App stuff
if __name__ == '__main__':
    application.debug = os.environ['FLASK_DEBUG'] == 'true'
    application.run(host='0.0.0.0', port=int(5000))
