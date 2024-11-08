from auth import mast_client


async def create_toot(text, image_path):
    if text is None or image_path is None:
        return

    print("Preparing toot...")
    try:
        media = mast_client.media_post(image_path)
        response = mast_client.status_post(text, media_ids=[media["id"]])
        print(f"New Toot! URL: https://botsin.space/@ca_dmv_bot/{response['id']}")
    except Exception as e:
        print(f"Failed to post image on Mastodon: {e}")
