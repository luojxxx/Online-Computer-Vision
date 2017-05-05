# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import datetime
import string
import traceback
import requests
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

@application.route('/api/v1/featureprocessing',methods=['POST'])
def apiResponse():

    return jsonify({ 'response': 'we good' })



# App stuff
if __name__ == '__main__':
    application.debug = os.environ['FLASK_DEBUG'] == 'true'
    application.run(host='0.0.0.0', port=int(5000))