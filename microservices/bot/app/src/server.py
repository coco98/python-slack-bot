from src import app
from flask import jsonify, request
import requests
import json

@app.route("/")
def event():
    try:
        DATA = request.get_data()
        print ("===============================================================");
        print (DATA.decode());
        print ("===============================================================");
        output = json.loads(DATA.decode())
        print("Topic Recieved: " + output["topic"]);
        receivedToken = output["token"]
        receivedTeamId = output["team_id"]
        pass
    except Exception as e:
        print(e)
        raise
    return("OK")
