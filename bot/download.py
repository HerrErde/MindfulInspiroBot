import json
import sys

import aiohttp


async def fetch_inspirobot(unsplash_api_key):
    unsplash_api = "https://api.unsplash.com/photos/{image_id}?client_id={access_key}"
    url = "https://inspirobot.me/api?generateFlow=1"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = (await response.json())["data"]

                if len(data) >= 2:
                    text = data[1].get("text", None).replace("’", "'")
                    image_id = data[0]["image"]

                    # Fetch image metadata from Unsplash
                    image_data_url = unsplash_api.format(
                        image_id=image_id, access_key=unsplash_api_key
                    )
                    async with session.get(image_data_url) as unsplash_response:
                        unsplash_response.raise_for_status()
                        unsplash_data = await unsplash_response.json()

                        image_url = unsplash_data["urls"]["raw"]
                        alt_description = unsplash_data.get("alt_description", None)
                        image_width = unsplash_data["width"]
                        image_height = unsplash_data["height"]

                        # Check dimensions and rate limit
                        limit = unsplash_response.headers.get("X-Ratelimit-Limit")
                        remaining = unsplash_response.headers.get(
                            "X-Ratelimit-Remaining"
                        )
                        print(f"Ratelimit Limit: {remaining}/{limit}")

                        if image_width <= image_height:
                            print(f"Insufficient Size: {image_width}x{image_height}")
                            return None, None, None
                        else:
                            return image_url, text, alt_description
                else:
                    print("Insufficient data received from InspiroBot")
        except aiohttp.ClientError as e:
            print(f"Request to InspiroBot failed: {e}")
        except (KeyError, IndexError) as e:
            print(f"Error parsing InspiroBot response: {e}")
        except KeyboardInterrupt:
            print("Exiting.")
            sys.exit(1)

    return None, None, None


async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(await response.read())
                return True
        except aiohttp.ClientError as e:
            print(f"Image download failed: {e}")
            return False
