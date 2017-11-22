from src import app
from flask import jsonify, request
import requests
import json
import os

token = os.environ['SLACK_TOKEN']

@app.route('/', methods=['POST'])
def event():
    try:
        data = request.form.to_dict()
        print(data)
        receivedToken = data["token"]
        print("Received Token: " + receivedToken)
        print("asdasdad Token: " + token)
        if (receivedToken==token):
            print("TOken Valid")
            receivedText= data["text"]
            id = storeText(receivedText, data["response_url"])
            sendChoice(id)
            return "Waiting for response"
        else:
            return "Invalid Token"
    except Exception as e:
        print(e)
        raise
    
    return "ok"

@app.route('/test', methods=['GET'])
def test():
    return "Running"

@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.form.to_dict()
    print (data)
    receivedToken = data["payload"]["token"]
    if (receivedToken == token):
        return "ok"
    return "ok"


def sendChoice(id):
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
                        "text": "Yep",
                        "type": "button",
                        "value": "yes",
                        "id": id
                    },
                    {
                        "name": "choice",
                        "text": "Nope",
                        "type": "button",
                        "value": "no",
                        "id": id
                    }
                ]
            }
        ]
    }
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", responseUrl, data=json.dumps(payload), headers=headers)
    print(response.text)
    return

def storeText(text, responseUrl):
    url = "http://data.hasura/v1/query"

    requestPayload = {
        "type": "insert",
        "args": {
            "table": "slack_messages",
            "objects": [
                {
                    "message": text,
                    "response_url": responseUrl
                }
            ],
            "returning": [
                "id"
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    print (resp.content)
    id = resp.content["returning"][0]["id"]
    return id
