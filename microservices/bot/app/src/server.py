from src import app
from flask import jsonify, request
import requests
import json

@app.route('/', methods=['POST'])
def event():
    try:
        DATA = request.get_data()

        print ("===============================================================");
        print request
        print ("===============================================================");
        print (DATA)
        print ("===============================================================");
        print (DATA.decode());
        print ("===============================================================");
        output = json.loads(DATA.decode())
        print (output)
        print ("===============================================================");
        print("Topic Recieved: " + output["topic"]);
        receivedToken = output["token"]
        receivedTeamId = output["team_id"]
        pass
    except Exception as e:
        print(e)
        raise
    return("OK")

@app.route('/test', methods=['GET'])
def test():
    return "Running"
