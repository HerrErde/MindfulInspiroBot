import os

import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Twitter API keys and tokens from environment variables
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate to Twitter

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)


# Example: Post media a tweet
"""
media_path = "photo-1491378630646-3440efa57c3b.jpg"
media = client.media_upload(filename=media_path)
media_id = media.media_id
response = client.create_tweet(text="Tweet text", media_ids=[media_id])
"""

# Example: Post a tweet
response = client.create_tweet(text="Hello, World!")
print(f"https://twitter.com/user/status/{response.data['id']}")

print("Tweet posted successfully!")
