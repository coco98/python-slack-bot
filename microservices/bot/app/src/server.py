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

def sendChoice():
    url = "https://hooks.slack.com/services/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"
    choiceResponse = "{\n        \"text\": \"Are you freaking serious you want to send this message?\",\n        \"attachments\": [\n            {\n                \"text\": \"Please decide\",\n                \"fallback\": \"You are unable to choose a game\",\n                \"callback_id\": \"wopr_game\",\n                \"color\": \"#3AA3E3\",\n                \"attachment_type\": \"default\",\n                \"actions\": [\n                    {\n                        \"confirm\": {\n                            \"title\": \"Are you sure?\",\n                            \"text\": \"Are you really sure?\",\n                            \"ok_text\": \"Yes\",\n                            \"dismiss_text\": \"No\"\n                        }\n                    }\n                ]\n            }\n        ]\n    }"
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", url, data=choiceResponse, headers=headers)
    print(response.text)