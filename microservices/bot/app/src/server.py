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
    print ("================")
    print (data)
    print ("================")
    return ok

def sendChoice():
    url = "https://hooks.slack.com/services/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"
    payload = {
        "text": "Would you like to play a game?",
        "attachments": [
            {
                "text": "Choose a game to play",
                "fallback": "You are unable to choose a game",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "game",
                        "text": "Chess",
                        "type": "button",
                        "value": "chess"
                    },
                    {
                        "name": "game",
                        "text": "Falken's Maze",
                        "type": "button",
                        "value": "maze"
                    },
                    {
                        "name": "game",
                        "text": "Thermonuclear War",
                        "style": "danger",
                        "type": "button",
                        "value": "war",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Wouldn't you prefer a good game of chess?",
                            "ok_text": "Yes",
                            "dismiss_text": "No"
                        }
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