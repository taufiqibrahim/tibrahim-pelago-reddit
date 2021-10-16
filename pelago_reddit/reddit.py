import json
import praw
import psycopg2
import psycopg2.extras
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RedditIngestionConfig:
    reddit_client_id: str
    reddit_client_secret: str
    reddit_redirect_uri: str
    reddit_user_agent: str
    pg_host: str
    pg_port: int = 5432
    pg_database: str = 'postgres'
    pg_user: str = 'postgres'
    pg_password: str = 'postgres'


@dataclass
class RedditTopNHotPostIngestionConfig(RedditIngestionConfig):
    subreddit_name: str = 'aws'
    limit: int = 100


class RedditIngestion:

    def __init__(self, config: RedditIngestionConfig) -> None:
        self.config = config

    def _get_reddit_connection(self):
        self.reddit = praw.Reddit(
            client_id=self.config.reddit_client_id,
            client_secret=self.config.reddit_client_secret,
            redirect_uri=self.config.reddit_redirect_uri,
            user_agent=self.config.reddit_user_agent,
        )

    def _get_db_connection(self):
        connection = psycopg2.connect(
            host=self.config.pg_host,
            port=self.config.pg_port,
            database=self.config.pg_database,
            user=self.config.pg_user,
            password=self.config.pg_password,
        )
        connection.autocommit = True
        return connection


class RedditTopNHotPostIngestion(RedditIngestion):

    def __init__(self, config: RedditTopNHotPostIngestionConfig) -> None:
        self.config = config

    def get_data(self):
        data = list()
        self._get_reddit_connection()
        for submission in self.reddit.subreddit(self.config.subreddit_name).hot(limit=self.config.limit):
            data.append(submission)
        return data

    def clean(self, records: list):
        clean_records = [(
            r.id,
            r.title,
            i + 1,
            datetime.fromtimestamp(r.created),
            r.url,
            r.selftext,
            r.upvote_ratio,
            r.author.name,
            r.author_premium,
            r.over_18,
            json.dumps(r.treatment_tags),
            datetime.utcnow().replace(minute=0, second=0, microsecond=0), # schedule timestamp
        ) for i, r in enumerate(records)]

        return clean_records

    def write_to_db(self, records: list):
        insert_stmt = "INSERT INTO hot_posts (id, title, rank, created, url, selftext, upvote_ratio, author, author_premium, over_18, treatment_tags, _scheduled_ts) VALUES %s;"
        conn = self._get_db_connection()
        with conn.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, insert_stmt, records)

    def execute(self):
        data = self.get_data()
        clean = self.clean(data)
        self.write_to_db(clean)
