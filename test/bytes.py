from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont


def textsize(text, font):
    im = Image.new(mode="RGB", size=(1, 1))  # Create a minimal image
    draw = ImageDraw.Draw(im)
    width, height = draw.textbbox((0, 0), text=text, font=font)[
        2:
    ]  # Get width and height
    return width, height


def download_image_as_bytes(url):
    # Download the image and load it into BytesIO
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return BytesIO(response.content)


def modify_image(image_bytes, text, font_path, font_size):
    # Open the image from bytes
    with Image.open(image_bytes) as image:
        # Initialize drawing context
        draw = ImageDraw.Draw(image)

        # Load the font
        font = ImageFont.truetype(font_path, font_size)

        # Calculate text position to center it
        text_width, text_height = textsize(text, font=font)
        text_x = (image.width - text_width) // 2
        text_y = (image.height - text_height) // 2

        # Draw the text on the image
        draw.text((text_x, text_y), text, font=font, fill=(255, 0, 0))

        # Save the modified image to a new BytesIO object
        modified_image_bytes = BytesIO()
        image.save(modified_image_bytes, format="PNG")
        modified_image_bytes.seek(0)

        return modified_image_bytes


def save_modified_image(image_bytes, output_path):
    # Save the modified image bytes to a file
    with open(output_path, "wb") as f:
        f.write(image_bytes.getvalue())


# Usage example
url = "https://images.unsplash.com/photo-1445366526762-3646e5bf3beb"
font_path = "font.ttf"

# Download and modify the image
original_image_bytes = download_image_as_bytes(url)
modified_image_bytes = modify_image(
    original_image_bytes, "Hello, World!", font_path, 400
)

# Save only the modified image
save_modified_image(modified_image_bytes, "modified_image.png")
