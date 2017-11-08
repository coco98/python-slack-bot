from flask import Blueprint, jsonify, request
import json
import requests
import pprint
from .config import dataUrl, dataHeaders
import slackclient
import os

hasura_examples = Blueprint('hasura_examples', __name__)

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
sc = slackclient.SlackClient(SLACK_TOKEN)

@hasura_examples.route("/get_articles")
def articles():

    query = {
        'type': 'select',
        'args': {
            'table': 'article',
            'columns': [
                '*'
            ]
        }
    }
    print(json.dumps(query))
    print(dataUrl)

    response = requests.post( dataUrl, data = json.dumps(query), headers = dataHeaders)
    return jsonify(response.json())

@hasura_examples.route("/comment/<article_id>", methods=['POST'])
def add_comment(article_id):
    j = request.json

    comment = j.get("comment")
    
    query = {
        "type": "insert",
        "args": {
            "table": "comments",
            "objects": [
                {
                    "article_id": article_id,
                    "comment": comment
                }
            ]
        }
    }
    
    print("query:", json.dumps(query))
    print(dataUrl)
    
    response = requests.post( dataUrl, data = json.dumps(query), headers = dataHeaders)
    print(response.json())

    print("posting to slack")
    sc_msg = "New comment on article {} \"{}\"".format(article_id, comment[:50] + (comment[50:] and "..."))
    slack_post("#general", sc_msg)
    
    return jsonify(response.json())

def slack_post(channel, message):
    sc.api_call("chat.postMessage", channel=channel, text=message)
