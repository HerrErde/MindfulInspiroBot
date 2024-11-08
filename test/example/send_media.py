import os

import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("2.env")

# Load Twitter API keys and tokens from environment variables
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


def get_twitter_conn_v1(
    consumer_key, consumer_secret, access_token, access_token_secret
) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)


def get_twitter_conn_v2(
    consumer_key, consumer_secret, access_token, access_token_secret
) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client


client_v1 = get_twitter_conn_v1(
    consumer_key, consumer_secret, access_token, access_token_secret
)
client_v2 = get_twitter_conn_v2(
    consumer_key, consumer_secret, access_token, access_token_secret
)

media_path = "test.jpg"
media = client_v1.media_upload(filename=media_path)
media_id = media.media_id

client_v2.create_tweet(text="Tweet text", media_ids=[media_id])
