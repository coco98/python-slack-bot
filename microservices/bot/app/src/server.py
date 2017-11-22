from src import app
from flask import jsonify, request
import requests
import json

@app.route('/', methods=['POST'])
def event():
    try:
        data = request.form
        print ("===============================================================");
        print (data)
        print ("===============================================================")
        receivedToken = data["token"]
        receivedTeamId = data["team_id"]
        sendChoice()

    except Exception as e:
        print(e)
        raise
    return "OK"

@app.route('/test', methods=['GET'])
def test():
    return "Running"

@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.form
    print (data)
    return something

def sendChoice():
    url = "https://hooks.slack.com/services/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"
    payload = {"text":"yo sup?"}
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)