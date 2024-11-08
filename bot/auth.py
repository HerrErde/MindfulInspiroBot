import os

import atproto
import tweepy
from dotenv import load_dotenv

# from mastodon import Mastodon

# Load environment variables from .env file
load_dotenv()

# Load Twitter API keys and tokens from environment variables
unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
mastdodon_access_token = os.getenv("MASTODON_ACCESS_TOKEN")
bsky_url = os.getenv("BLUESKY_URL")
bsky_handle = os.getenv("BLUESKY_HANDLE")
bsky_pass = os.getenv("BLUESKY_PASS")


# Authenticate to Twitter
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


# Authenticate to Bluesky
def get_bsky_client(bsky_handle, bsky_pass):

    bsky_client = atproto.Client(bsky_url)
    bsky_client.login(bsky_handle, bsky_pass)

    return bsky_client


""" # Authenticate to Mastodon
def get_mast_client(mastdodon_access_token):
    mastodon = Mastodon(access_token=mastdodon_access_token)

    return mastodon """


client_v1 = get_twitter_conn_v1(
    consumer_key, consumer_secret, access_token, access_token_secret
)
client_v2 = get_twitter_conn_v2(
    consumer_key, consumer_secret, access_token, access_token_secret
)

bsky_client = get_bsky_client(bsky_handle, bsky_pass)

""" mast_client = get_mast_client(mastdodon_access_token)
"""
