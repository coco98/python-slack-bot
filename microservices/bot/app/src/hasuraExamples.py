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

@hasura_examples.route('/echo', methods=['POST'])
def echo():
    message = request.json.get('message')

    #Insert into the database
    query = {
        'type': 'insert',
        'args': {
            'table': 'comments',
            'objects': [
                {
                    'article_id': article_id,
                    'comment': comment
                }
            ]
        }
    }

    # response = requests.post( dataUrl, data = json.dumps(query), headers = dataHeaders)
    # print(response.json())

    print('replying to command')
    sc_msg = 'New comment on article {} \'{}\''.format(article_id, comment[:50] + (comment[50:] and '...'))
    slack_post('#general', sc_msg)

    return jsonify(response.json())

def slack_post(channel, message):
    sc.api_call('chat.postMessage', channel=channel, text=message)
