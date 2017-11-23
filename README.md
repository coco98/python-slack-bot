# python-slack-bot

![](https://media.giphy.com/media/26u8yqs5WE4bINd3W/giphy.gif)

This is a simple slackbot that responds to slash commands and uses message buttons.

This is the easiest and fastest way to deploy a slackbot because slack callbacks require
HTTPS URLs with valid SSL certificates, which Hasura generates automatically :)

Features:

1. Receive command
2. Insert command data in the database using the Hasura data APIs
3. Echo the same output as a message only the user can see, with a confirm message button
4. If the user clicks on the confirm button, display the message to the whole channel

You can make trivial modifications to the code to make the bot work as you wish.

This slack bot builds on top the following slack APIs:

1. [https://api.slack.com/custom-integrations/slash-commands](https://api.slack.com/custom-integrations/slash-commands)
2. [https://api.slack.com/interactive-messages](https://api.slack.com/interactive-messages)
3. [https://api.slack.com/methods/chat.postMessage](https://api.slack.com/methods/chat.postMessage)

### Callbacks

#### 1. slash command callback request URL
 ```http
 POST /echo
 Content-Type application/x-www-form-urlencoded

 token=gIkuvaNzQIHg97ATvDxqgjtO
 team_id=T0001
 team_domain=example
 channel_id=C2147483705
 channel_name=test
 user_id=U2147483697
 user_name=Steve
 command=/weather
 text=94070
 ```

As taken from: [https://api.slack.com/custom-integrations/slash-commands](https://api.slack.com/custom-integrations/slash-commands)

This callback will take the message text and save it in the database.
It will also reply to the user asking the user to confirm if the user wants to paste the to everyone in the current channel

#### 2. Interactive message callback request URL

```http
POST /confirm
Content-Type application/x-www-form-urlencoded

payload=
{
  "actions": [
    {
      "name": "recommend",
      "value": "recommend",
      "type": "button"
    }
  ],
  "callback_id": "comic_1234_xyz",
  "team": {
    "id": "T47563693",
    "domain": "watermelonsugar"
  },
  "channel": {
    "id": "C065W1189",
    "name": "forgotten-works"
  },
  "user": {
    "id": "U045VRZFT",
    "name": "brautigan"
  },
  "action_ts": "1458170917.164398",
  "message_ts": "1458170866.000004",
  "attachment_id": "1",
  "token": "xAB3yVzGS4BQ3O9FACTa8Ho4",
  "original_message": {"text":"New comic book alert!","attachments":[{"title":"The Further Adventures of Slackbot","fields":[{"title":"Volume","value":"1","short":true},{"title":"Issue","value":"3","short":true}],"author_name":"Stanford S. Strickland","author_icon":"https://api.slack.comhttps://a.slack-edge.com/bfaba/img/api/homepage_custom_integrations-2x.png","image_url":"http://i.imgur.com/OJkaVOI.jpg?1"},{"title":"Synopsis","text":"After @episod pushed exciting changes to a devious new branch back in Issue 1, Slackbot notifies @don about an unexpected deploy..."},{"fallback":"Would you recommend it to customers?","title":"Would you recommend it to customers?","callback_id":"comic_1234_xyz","color":"#3AA3E3","attachment_type":"default","actions":[{"name":"recommend","text":"Recommend","type":"button","value":"recommend"},{"name":"no","text":"No","type":"button","value":"bad"}]}]},
  "response_url": "https://hooks.slack.com/actions/T47563693/6204672533/x7ZLaiVMoECAW50Gw1ZYAXEM",
  "trigger_id": "13345224609.738474920.8088930838d88f008e0"
}
```

This structure is based on: [https://api.slack.com/docs/message-buttons](https://api.slack.com/docs/message-buttons)

### Guide to get it running

- Create a [Slack app](https://api.slack.com/slack-apps). Name it whatever you want. Choose the workspace you want to run it in. 

![CreateApp](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/create_app.png)


- On creation, you will be taken to the app management page. Click on `slash commands` and create a command. Add the URL to be https://bot.cluster-name.hasura-app.io. You can find your cluster name by running `$ hasura cluster status` from the project directory.

![AddCommand](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/add_command.png)


- Click on Bots and add a bot user. Name it whatever you like.

![AddBot](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/add_bot.png)


- Go to `OAuth and Permissions` in the panel on the left. Scroll down to scopes and add the following permission scope.

![Scope](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/scope.png)


- Scroll up and install the app to your workspace. Once it is installed, you will see a bot access token. Copy this token and add it to your secrets (since you do not want to expose the token explicitly in your code).

```
$ hasura secret update bot.access.token <bot_access_token>
```

- Go to `Basic Information` in the panel on the left. Scroll down to App credentials. Copy the 
*verification token*. Add this to your secrets as well

![app_creds](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/app_creds.png)


```
$ hasura secret update slack.token <verification_token>
```

