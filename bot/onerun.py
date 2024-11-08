import asyncio
import os
import sys
import time

import requests
from auth import unsplash_api_key
from cache import entry_exists, load_cache, save_cache
from download import download_image, fetch_inspirobot
from image import create
from network import create_skeet, create_tweet  # , create_toot

tmp_dir = ".tmp"
input_image_path = ".tmp/image.jpg"
output_image_path = ".tmp/output_image.jpg"
font_path = "assets/font.ttf"
font_size = 150
message_size = 100
minute = 59
second = 50
wait_time = 5
timezone = "Europe/Berlin"
enable_cache = False
CACHE_FILE = "assets/inspirobot_cache.json"

blocked_list = ["intestine", "breathing", "deep breath", "[", "repeat", ":"]


async def fetch_data():
    image_url, text, alt_description = await fetch_inspirobot(unsplash_api_key)
    if not image_url or not text:
        print("Failed to fetch image URL or text. Retrying...")
        return None, None, None

    print(
        f"Image URL: {image_url}, Text: {text.replace('\n', ' ')}, Alt Desc: {alt_description}"
    )

    if any(blocked_item in text for blocked_item in blocked_list):
        print("Blocked content found in text.")
        print("Fetching again...")
        return None, None, None

    if len(text) > message_size:
        print("Text is too long.")
        print("Fetching again...")
        return None, None, None

    print("Data fetched successfully.")
    return image_url, text, alt_description


async def create_image(image_url, text, output_image_path):
    if image_url is None or text is None:
        return

    print("Downloading image...")
    await download_image(image_url, input_image_path)
    print(f"Image downloaded to: {input_image_path}")

    print("Processing image...")
    create(input_image_path, output_image_path, text, font_path)
    print(f"New image saved at: {output_image_path}")


async def create_post(text, image_path, alt_text):
    if text is None or output_image_path is None:
        return

    mod_alt_text = f"{alt_text}, with the text '{text}'."

    await create_tweet(text, image_path, mod_alt_text)
    await create_skeet(text, image_path, mod_alt_text)
    # await create_toot(text, image_path,mod_alt_text)

    os.remove(input_image_path)
    os.remove(output_image_path)
    print("Temp images removed.")


async def main():
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    if os.path.exists(input_image_path):
        os.remove(input_image_path)
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    try:
        while True:
            image_url, text = (
                "https://images.unsplash.com/photo-1530937058026-7ab413e9ae19",
                "Together we can make the moon implode.",
            )
            image_url, text, alt_description = await fetch_data()

            if image_url and text:
                if enable_cache:
                    cached_data = load_cache(CACHE_FILE)
                    if entry_exists(cached_data, image_url, text):
                        print("Data already exists in cache. Fetching again...")
                        continue
                    else:
                        save_cache({"url": image_url, "text": text}, CACHE_FILE)

                await create_image(image_url, text, output_image_path)
                # create_post(text, output_image_path, alt_description)
                break
            else:
                print("Retrying data fetch...")
                time.sleep(1)  # Wait before retrying

    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(1)

    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        time.sleep(30)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(30)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())