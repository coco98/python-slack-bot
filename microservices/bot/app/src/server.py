from src import app
from flask import jsonify, request
import requests
import json
import os

slackToken = os.environ['SLACK_TOKEN']
botAccessToken = os.environ['BOT_ACCESS_TOKEN']

@app.route('/test', methods=['GET'])
def test():
    return "Slackbot is running"

@app.route('/', methods=['POST'])
def event():
    data = request.form.to_dict()
    print(data)
    receivedToken = data["token"]
    if (receivedToken==slackToken):
        receivedText= data["text"]
        id = storeMsgToDB(receivedText)
        sendConfirmation(id, data["response_url"])
        return "Waiting for response"
    else:
        return "Invalid Token"

@app.route('/confirm', methods=['POST'])
def confirm():
    req = request.form.to_dict()
    data = json.loads(req["payload"])
    print (data)
    receivedToken = data["token"]
    channel = data["channel"]["id"]
    if (receivedToken == slackToken):
        if (data["actions"][0]["value"] == "yes"):
            fetchAndSend(data["callback_id"], channel)
            return "Message Sent"
        else:
            return "Ok. Not sending. :confused:"

def sendConfirmation(id, responseUrl):
    payload = {
        "text": "Are you sure you want to send a message?",
        "attachments": [
            {
                "text": "Please decide",
                "fallback": "You are indecisive",
                "callback_id": id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "yes",
                        "text": "Yep",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "no",
                        "text": "Nope",
                        "type": "button",
                        "value": "no"
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

def storeMsgToDB(text, responseUrl):
    url = "http://data.hasura/v1/query"

    requestPayload = {
        "type": "insert",
        "args": {
            "table": "slack_messages",
            "objects": [
                {
                    "message": text,
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
    return id

def fetchAndSend(id, channel):
    url = "http://data.hasura/v1/query"

    requestPayload = {
        "type": "select",
        "args": {
            "table": "slack_messages",
            "columns": [
                "message",
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
    message = respObj[0]["message"]
    sendMessage(message, channel)

def sendMessage(message, channel):
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "token": botAccessToken,
        "text": message,
        "channel": channel
    }
    headers = {
        'content-type': "application/json",
        'Authorization': 'Bearer '+botAccessToken
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.json())