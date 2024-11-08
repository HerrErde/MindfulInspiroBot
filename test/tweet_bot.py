import os
import sys
import time
from datetime import datetime

import requests
import tweepy
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load environment variables from .env file
load_dotenv()
# load_dotenv("2.env")

# Load Twitter API keys and tokens from environment variables
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


input_image_path = "image.jpg"
output_image_path = "output_image.jpg"
font_path = "font.ttf"


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


client_v1 = get_twitter_conn_v1(
    consumer_key, consumer_secret, access_token, access_token_secret
)
client_v2 = get_twitter_conn_v2(
    consumer_key, consumer_secret, access_token, access_token_secret
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
                image_url = unsplash_url.format(image_value=image_value)
                return image_url, text
            else:
                print("Insufficient data received")
        elif response.status_code == 429:
            print(f"Rate limit exceeded.")
            time.sleep(60 * 5)
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")


def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded and saved as {filename}")
        else:
            print(f"Failed to download image: HTTP status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Image download failed: {e}")


def write_image_text(input_image_path, output_image_path, text, font_path):
    try:
        # Open the input image
        with Image.open(input_image_path) as image:
            # Initialize drawing context
            draw = ImageDraw.Draw(image)

            # Load the font
            font_size = 36
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text size using the loaded font
            text_width, text_height = draw.textsize(text, font=font)

            # Calculate text position to center it on the image
            image_width, image_height = image.size
            text_position = (
                (image_width - text_width) // 2,
                (image_height - text_height) // 2,
            )

            # Draw text on the image
            draw.text(text_position, text, font=font, fill="white")

            # Save the modified image
            image.save(output_image_path)

    except FileNotFoundError:
        print(f"Error: File not found: {input_image_path}")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    print("Twitter Bot Starts")
    while True:
        try:
            # Check if the current time is a full hour
            current_time = datetime.now().time()
            if current_time.minute == 59 and current_time.second > 50:
                image_url, text = fetch_inspirobot()
                if len(text) > 128:
                    print("Text is too long, fetching again...")
                    continue

                if image_url and text:
                    download_image(image_url, input_image_path)
                    write_image_text(
                        input_image_path, output_image_path, text, font_path
                    )
                    # Upload Media
                    media_path = output_image_path
                    media = client_v1.media_upload(filename=media_path)

                    # Send Tweet with Media
                    media_id = media.media_id
                    response = client_v2.create_tweet(text=text, media_ids=[media_id])

                    # Remove Images
                    os.remove(input_image_path)
                    os.remove(output_image_path)
                    print(
                        f"Tweet posted successfully! URL: https://twitter.com/user/status/{response.data['id']}"
                    )
                else:
                    print("Failed to fetch image URL and text.")
            else:
                # Sleep for 10 seconds before checking the time again
                print(f"Not yet time. {current_time.second}s")
            time.sleep(10)

        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(1)

        except Exception as ex:
            print(f"An error occurred: {ex}")
            # Sleep for a longer time before retrying on other unexpected errors
            time.sleep(60)
