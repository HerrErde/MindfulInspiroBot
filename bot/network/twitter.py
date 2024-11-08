from auth import client_v1, client_v2


async def create_tweet(text, image_path, alt_text):
    if text is None or image_path is None:
        return

    print("Preparing tweet...")
    try:
        try:
            client_v1.get_me()
            print("Authentication successful!")
        except tweepy.TweepyException as e:
            print("Authentication failed:", e)
            return

        media = client_v1.media_upload(filename=image_path)
        media_id = media.media_id
        if alt_text:
            client_v1.create_media_metadata(media_id, alt_text)

        print("Uploading media to Twitter...")
        response = client_v2.create_tweet(text=text, media_ids=[media_id])
        print(f"New Tweet! URL: https://twitter.com/user/status/{response.data['id']}")
    except Exception as e:
        print(f"Failed to post image on Twitter: {e}")
        return
