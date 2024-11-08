import re
from io import BytesIO

from auth import bsky_client


async def create_skeet(text, image_path, image_alt):
    if text is None or image_path is None:
        return

    print("Preparing skeet...")
    try:
        # Read the image file as bytes
        with open(image_path, "rb") as image_file:
            image_data = BytesIO(image_file.read())

        response = bsky_client.send_image(text, image_data, image_alt)

        # Extract the post ID from the uri
        post_id_match = re.search(r"/([^/]+)$", response["uri"])
        if post_id_match:
            post_id = post_id_match.group(1)
            print(
                f"New Skeet! URL: https://bsky.app/profile/inspiromindbot.bsky.social/post/{post_id}"
            )
        else:
            print("Post ID not found in the response.")
    except Exception as e:
        print(f"Failed to post image on Bluesky: {e}")
