# from flask import Flask, jsonify, render_template, request
# from flask_cors import CORS, cross_origin
# app = Flask(__name__)
# CORS(app)
# import io
# import os
# import random


# FLASK_DEBUG = 'true'

# scriptpath = os.path.dirname(os.path.realpath(__file__))
# def readFile(filepath):
#     with io.open(filepath, 'r', encoding='utf8') as f:
#         content = f.read().splitlines()
#     return content


# @app.route('/')
# def index():
#     return render_template('test_page.html')

# @app.route('/api/v2/response',methods=['POST'])
# # @requires_auth
# def apiResponse():
#     postData = request.get_json()
#     entryValue = str(postData['entryValue'])

#     if entryValue[-1:]=='\n':
#         journalStarters = readFile( os.path.join(scriptpath, 'misc', 'journalstarters.txt') )
#         randomStarter = random.choice(journalStarters)

#         return jsonify({ 'response': randomStarter })

#     else:
#         continuations = readFile( os.path.join(scriptpath, 'misc', 'continuations.txt') )
#         randomContinuation = random.choice(continuations)

#         return jsonify({ 'response': randomContinuation })

# if __name__ == "__main__":
#     app.run()



# from celery import Celery

# app = Celery('tasks', broker='redis://localhost:6379/0')

# @app.task
# def add(x, y):
#     print(x+y)
#     return x + y

# add.delay(4, 4)

import schedule
import time
from twilio.rest import TwilioRestClient 

# put your own credentials here 
ACCOUNT_SID = "ACcd689b662aff4e16bc67ffb4dd91da76" 
AUTH_TOKEN = "395b44c03ed64ce0df0d3c352a1edf57" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

def job():
    print("I'm working...")
    client.messages.create(
        to="+19164022827", 
        from_="+15598887372", 
        body="""Hey leave a journal entry, at http://alphadev-dev.sn22bmaivu.us-west-1.elasticbeanstalk.com/ """, 
        media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg", 
    )

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)