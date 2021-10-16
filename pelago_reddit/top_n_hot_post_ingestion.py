import os
from pelago_reddit.reddit import RedditTopNHotPostIngestion, RedditTopNHotPostIngestionConfig


def main(event, context):
    config = RedditTopNHotPostIngestionConfig(
        reddit_client_id=os.environ['REDDIT_CLIENT_ID'],
        reddit_client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        reddit_redirect_uri=os.environ['REDDIT_REDIRECT_URI'],
        reddit_user_agent=os.environ['REDDIT_USER_AGENT'],
        pg_host=os.environ['PG_HOST'],
        pg_port=int(os.environ['PG_PORT']),
        pg_database=os.environ['PG_DATABASE'],
        pg_user=os.environ['PG_USER'],
        pg_password=os.environ['PG_PASSWORD'],
        subreddit_name=os.environ['SUBREDDIT_NAME'],
        limit=int(os.environ['LIMIT']),
    )
    ri = RedditTopNHotPostIngestion(config=config)
    ri.execute()
