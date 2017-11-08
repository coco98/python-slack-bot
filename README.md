# python-slack-bot

This project demos a Slack bot on Hasura. It has been forked from the `hello-python-flask` project.


## Introduction

This quickstart project comes with the following by default:
1. A basic hasura project
2. Three tables `article`, `author` and `comments` with some dummy data
3. A Flask app having the endpoints: `/get_articles` to fetch a list of articles, and `/comment` to comment on an article and post the new comment to a Slack channel
4. A Slack bot which can post a new comment to the `comments` table when invoked using a message on Slack

## Description

A detailed description of the base project and its usage is available in the Readme of the `hello-python-flask` project.

This project adds a `comments` table and two Slack bots to the base project.

The `comment` table essentiallly maps comments to articles. There is also a flask endpoint `/comment/<article_id>` to which a comment can be POSTed.

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

2. An article can be commented upon by summoning the bot with the article ID and the comment. For example: `articlebot 12 Interesting article` will post a comment for article number 12 saying "Interesting article". This bot uses the Real Time Event feed from Slack to watch for comments and take action if a set of conditions are met.

## Usage

Make sure you insert the Slack API Token in the `env` section in `k8s.yaml` in each of `app` and `slack-bot`. Deploy the project using the standard `git push` method.
