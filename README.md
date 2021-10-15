# tibrahim-pelago-reddit
Pelago - Coding Challenge - Data Engineer

## Task Detail
1. Create a data schema in any database of your choice
2. Create any AWS service of your choice to read data from the API
3. Process and clean the data as required
4. Insert top 100 HOT posts into the database table(s) on an hourly schedule from any subreddit of your choice

### Breaking Down The Tasks
For now on, I'll skip the whole task because I don't really know what Reddit is. So, I'll add several additional task to truly understand the business context.
- [x] Create this [Github repo](https://github.com/taufiqibrahim/tibrahim-pelago-reddit) and start documentation
- [x] Learn about Reddit and sign up
- [x] Explore how to use [PRAW](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) API
- [x] Explore API response, get the data model/schema
- [ ] Quick explore on deployment infrastructure

## What is Reddit?
Based on Reddit Help page:
- Reddit is home to thousands of communities, endless conversation, and authentic human connection. Whether you're into breaking news, sports, TV fan theories, or a never-ending stream of the internet's cutest animals, there's a community on Reddit for you.
- Reddit is a large community made up of thousands of smaller communities. These smaller, sub-communities within Reddit are also known as __subreddits__ and are created and moderated by redditors like you.

So, I am going to get data from [r/aws](https://www.reddit.com/r/aws/) subreddit.

Before going further, I need to create Reddit account to access Reddit API. We will obtain and use Reddit Client ID & Client Secret. I follow the [First Steps Guide](https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to create them.

Go to my [app preferences](https://www.reddit.com/prefs/apps). Click the "Create app" or "Create another app" button. Fill out the form like so:

name: My Example App
App type: Choose the script option
description: You can leave this blank
about url: You can leave this blank
redirect url: http://www.example.com/unused/redirect/uri (We won't be using this as a redirect)

## Create AWS Lambda Security Group
- `ServerlessSG`

## Create Database
- AWS RDS Postgres `db.t3.micro`
- Allow inbound from `ServerlessSG` 

## Deployment
### AWS Lambda + Serverless Framework

Prerequisite:
```bash
# install serverless framework
npm install -g serverless

# install dependencies from package.json
npm install
```

Create AWS Lambda IAM role called `ServerlessLambdaExecutionRole` using `AWSLambdaBasicExecutionRole`. Copy and paste the ARN into `env.json`.

```bash
# set AWS_PROFILE
export AWS_PROFILE=personal
# validate configuration
serverless print --stage dev
# get deployment info
serverless info --stage dev
# deploy
serverless deploy --stage dev
```
