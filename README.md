# python-slack-bot

This project demos a Slack bot on Hasura. It adds a Slack functionality to the `hello-python-flask` project.


## Description

This project is built upon the `hello-python-flask` quickstart project.

A detailed description of the base project and its usage is available in its README.

This project adds a `comments` table and two Slack API uses to the base project.

The `comments` table essentiallly maps comments to articles. There is also a Flask endpoint `/comment/<article_id>` to which a comment can be POSTed.
Along with inserting the comment into the database, it also posts the comment to a Slack channel.

There are two Slack bots (i.e. Slack API uses):

1. Whenever the `/comment/<article_id>` endpoint is called with the article ID and the comment, the data is inserted into the `comments` table and the new comment is also posted to a Slack channel. For example, to post a comment for `article_id` 12:

    ```http

    POST /comment/12
    Content-Type application/json

    {
      "comment" : "Interesting article"
    }

    ```
    A message will be posted to the channel defined in the code.

    This bot uses a simple Slack API call to post the  message.


2. An article can be commented upon by summoning the bot with the article ID and the comment.

   For example: `articlebot 12 Interesting article` will post a comment for article number 12 saying "Interesting article".

   This bot uses the Real Time Event feed from Slack to watch for messages that invoke it and parse and insert the comment into the database.

The project has 2 custom microservices:

1. The `app` microservice which is the Flask app from the base project and has been extended to serve the `/comment` endpoint.

2. The `slack-bot` microservice which watches the Real Time Events feed from Slack and responds to any message that invokes it. This microservice is not exposed to the outside world, i.e. there is no route corresponding to it in `conf/routes.yaml`.

## Usage

Make sure you insert the Slack API Token in the `env` section in `k8s.yaml` in each of `app` and `slack-bot`. Deploy the project using the standard `git push` method.
