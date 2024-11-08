import requests


def fetch_inspirobot():
    unsplash_url = "https://source.unsplash.com/{image_value}/1600x900"
    api_url = "https://inspirobot.me/api?generateFlow=1"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()["data"]
            image_values = []
            texts = []
            for entry in data:
                if "image" in entry:
                    image_values.append(entry["image"])
                if "text" in entry:
                    texts.append(entry["text"])
            image_urls = [
                unsplash_url.format(image_value=value) for value in image_values
            ]
            return image_urls, texts
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")


# Example usage:
if __name__ == "__main__":
    image_urls, texts = fetch_inspirobot()
    if image_urls and texts:
        for i in range(len(image_urls)):
            print("Image URL:", image_urls[i])
            print("Text:", texts[i] if i < len(texts) else "No text available")
            print()  # Add a newline for better readability between entries
    else:
        print("Failed to fetch image URLs and texts.")
