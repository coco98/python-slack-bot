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
        if (receivedToken==token):
            receivedText= data["text"]
            id = storeText(receivedText, data["response_url"])
            sendChoice(id, data["response_url"])
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
    receivedToken = json.loads(data["payload"])["token"]
    if (receivedToken == token):
        return "ok"
    return "not ok"


def sendChoice(id, responseUrl):
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
        "Content-Type": "application/json",
        "X-Hasura-User-Id": "1",
        "X-Hasura-Role": "admin"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    id = respObj["returning"][0]["id"]
    print(id)
    return id

def fetchAndSend(id):
    url = "http://data.hasura/v1/query"

    requestPayload = {
        "type": "select",
        "args": {
            "table": "slack_messages",
            "columns": [
                "message",
                "response_url"
            ],
            "where": {
                "id": {
                    "$eq": "23"
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "X-Hasura-User-Id": "1",
        "X-Hasura-Role": "admin"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    message = respObj[0][""]
    responseUrl = respObj[0]["response_url"]
    print(id)
    return id