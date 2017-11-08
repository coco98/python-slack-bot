import slackclient
import requests
import random
import os

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
sc = slackclient.SlackClient(SLACK_TOKEN)

app_url = "http://app.default"

if __name__ == "__main__":
    if not sc.rtm_connect():
        print("Couldn't connect to RTM stream")
        exit(1)
    while True:
        events = sc.rtm_read()
        for event in events:
            if event.get("type") == "message":
                print("--------------")
                print(event)
                text = event.get("text")
                if not text:
                    continue
                if "articlebot" in text:
                    # expected format: 'articlebot 12 interesting article'
                    s = text.split() 
                    article_id = s[1]
                    comment = " ".join(s[2:])
                    response = requests.post(app_url+"/comment/"+article_id, json={"comment":comment})
                    print(response.json())
                
                
