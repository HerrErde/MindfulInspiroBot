import json


def load_cache(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from cache file: {e}")
        return []


def save_cache(data, CACHE_FILE):
    try:
        # Load existing cache or empty list if file doesn't exist
        cached_data = load_cache(CACHE_FILE)

        # Append new data to the cache list
        cached_data.append(data)

        # Write updated cache data back to the file
        with open(CACHE_FILE, "w") as f:
            json.dump(cached_data, f, indent=2)

        print("Cache updated successfully.")
    except IOError as e:
        print(f"Failed to write cache data to file: {e}")


# Function to check if an entry already exists in the cache
def entry_exists(cached_data, image_url, text):
    for entry in cached_data:
        if isinstance(entry, dict) and "url" in entry and "text" in entry:
            if entry["url"] == image_url or entry["text"] == text:
                return True
    return False
