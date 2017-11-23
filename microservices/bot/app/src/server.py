from src import app
from flask import jsonify, request
import requests
import json
import os

slackToken = os.environ['SLACK_TOKEN']
botAccessToken = os.environ['BOT_ACCESS_TOKEN']
hasuraDataUrl = "http://data.hasura/v1/query"
chatUrl = "https://slack.com/api/chat.postMessage"

@app.route('/', methods=['GET'])
def test():
    return "Slackbot is running"

@app.route('/echo', methods=['POST'])
def event():
    data = request.form.to_dict()
    print(data)
    receivedToken = data["token"]
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        id = storeMsgToDB(receivedMessage)
        sendConfirmation(id, receivedMessage, data["response_url"])
        return "Waiting for confirmation"
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
            message = fetchAndSend(data["callback_id"], channel)
            return ("Message Sent: " + str(message))
        else:
            return "Ok. Not sending. :confused:"

def sendConfirmation(id, message, responseUrl):
    payload = {
        "text": "Are you sure you want to send a message?",
        "attachments": [
            {
                "text": '"'+message+'"',
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

def storeMsgToDB(text):

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
    resp = requests.request("POST", hasuraDataUrl, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    id = respObj["returning"][0]["id"]
    return id

def fetchAndSend(id, channel):

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
    resp = requests.request("POST", hasuraDataUrl, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    message = respObj[0]["message"]
    return sendMessage(message, channel)

def sendMessage(message, channel):
    payload = {
        "token": botAccessToken,
        "text": message,
        "channel": channel
    }
    headers = {
        'content-type': "application/json",
        'Authorization': 'Bearer '+botAccessToken
    }

    response = requests.request("POST", chatUrl, data=json.dumps(payload), headers=headers)
    print(response.json())
    return message