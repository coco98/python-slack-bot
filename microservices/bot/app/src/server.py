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
        pass
    except Exception as e:
        print(e)
        raise
    return (sendChoice())

@app.route('/test', methods=['GET'])
def test():
    return "Running"

def sendChoice():
    choiceResponse = {
        "text": "Are you freaking serious you want to send this message?",
        "attachments": [
            {
                "text": "Please decide",
                "fallback": "You are unable to choose a game",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Are you really sure?",
                            "ok_text": "Yes",
                            "dismiss_text": "No"
                        }
                    }
                ]
            }
        ]
    }
    return choiceResponse