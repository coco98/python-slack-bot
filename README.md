# python-slack-bot

**This is slackbot you will have:**
![](https://media.giphy.com/media/26u8yqs5WE4bINd3W/giphy.gif)

This is a simple slackbot that responds to slash commands and uses message buttons. It allows users on a channel to post messages to the channel.

Features:

1. Receive command: `/anonbot here's a message for the channel sent from an anonymous team member`
2. Save the command data in the database (uses Hasura data APIs)
3. Ask the slack user to confirm if they want to post their message
4. If the user clicks on the confirm button, post the message to the channel as the bot so that everyone can see

Reasons why this is the best way to get started with a basic slackbot:

1. This is a small but perfect example of how to implement a bot that accepts commands
2. The bot asks users for their confirmation and is a good starting point for implementing interactive commands/messages/buttons in slackbots
3. Slack requires all bots to have API callbacks on HTTPS. This project can be deployed on a free Hasura cluster in one command which auto-generates certified free SSL certificates (LetsEncrypt FTW) :)

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
 command=/anonbot
 text=here's a message for the channel sent from an anonymous team member
 ```

As taken from: [https://api.slack.com/custom-integrations/slash-commands](https://api.slack.com/custom-integrations/slash-commands)

This callback will take the message text and save it in the database.
It will also reply to the user asking the user to confirm if the user wants to paste the to everyone in the current channel

#### 2. Interactive message callback request URL

```http
POST /confirm
Content-Type application/x-www-form-urlencoded

payload={..JSON payload describing whether the user confirmed to post the message...}
```

This is based on: [https://api.slack.com/docs/message-buttons](https://api.slack.com/docs/message-buttons)

### Deployment guide

- Quickstart the project from Hasura hub.
```
$ hasura quickstart coco98/python-slack-bot && cd python-slack-bot
```

- Create a [Slack app](https://api.slack.com/slack-apps). Name it whatever you want. Choose the workspace you want to run it in. 

![CreateApp](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/create_app.png)


- On creation, you will be taken to the app management page. Click on `slash commands` and create a command. Add the URL to be https://bot.cluster-name.hasura-app.io/echo . You can find your cluster name by running `$ hasura cluster status` from the project directory.

![AddCommand](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/add_command.png)

- Go to `interactive components` in the panel on the left and enable interactive component. Add the URL as https://bot.cluster-name.hasura-app.io/confirm . Leave the options load URL empty.

![AddInteractive](https://github.com/coco98/python-slack-bot/raw/master/readme-assets/add_interactive.png)

- Go to `Basic Information` in the left panel and click on `Add features and functionality -> Bots`. Add a bot user and name it whatever you like.

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

- Push these changes to your Hasura cluster.

```
$ git add .
$ git commit -m "First commit"
$ git push hasura master
```

You can test your app in your channels :D
