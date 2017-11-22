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
    req = request.form.to_dict()
    data = json.loads(req["payload"])
    print("===============================")
    print (data)
    print("===============================")
    receivedToken = data["token"]
    if (receivedToken == token):
        if (data["actions"][len(data["actions"])-1]["value"]):
            fetchAndSend(data["actions"][len(data["actions"])-1]["value"])
        else:
            return "Ok :confused:"
        


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
                        "value": id
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
                    "$eq": id
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
    print (message)
    print (responseUrl)
    sendMessage(message, responseUrl)

def sendMessage(message, responseUrl):
    payload = {
        "text": message
    }
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", responseUrl, data=json.dumps(payload), headers=headers)
    print(response.text)
    return