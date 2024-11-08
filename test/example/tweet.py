import os
import time

import requests
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


def fetch_inspirobot():
    unsplash_url = "https://source.unsplash.com/{image_value}/1600x900"
    url = "https://inspirobot.me/api?generateFlow=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["data"]
            if len(data) >= 2:
                image_value = data[0]["image"]
                text = data[1].get("text", "No text available")
                return f"https://source.unsplash.com/{image_value}/1600x900", text
            else:
                print("Insufficient data received")
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    while True:
        image_url, text = fetch_inspirobot()
        if len(text) > 128:
            print("Text is too long, fetching again...")
            continue

        if image_url and text:
            response = client.create_tweet(text=text)
            print(
                f"Tweet posted successfully! URL: https://twitter.com/user/status/{response.data['id']}"
            )
        else:
            print("Failed to fetch image URL and text.")

        # Sleep for an hour before the next iteration
        time.sleep(3600)  # 3600 seconds = 1 hour
