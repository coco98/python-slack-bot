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
    return("OK")

@app.route('/test', methods=['GET'])
def test():
    return "Running"
