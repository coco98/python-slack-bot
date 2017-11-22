from src import app
from flask import jsonify, request
import requests
import json

@app.route('/', methods=['POST'])
def event():
    try:
        data = request.form

        print ("===============================================================");
        print (request.json)
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
    print ("================")
    print (data)
    print ("================")
    return "ok"

def sendChoice():
    url = "https://hooks.slack.com/services/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"
    payload = {
        "text": "Are you sure you want to send a message?",
        "attachments": [
            {
                "text": "Please decide",
                "fallback": "You are indecisive",
                "callback_id": "message_confirmation",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "choice",
                        "text": "Nope",
                        "type": "button",
                        "value": "no"
                    },
                    {
                        "name": "choice",
                        "text": "Yep",
                        "type": "button",
                        "value": "yes"
                    }
                ]
            }
        ]
    }
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)