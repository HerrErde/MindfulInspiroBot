from PIL import Image, ImageDraw, ImageFont


def draw_text_with_box(image_path, output_path, text, position, font_size):
    # Open the image
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate the size of the text
    x1, y1, x2, y2 = font.getbbox(text)
    text_width, text_height = (x2 - x1, y2 - y1)
    x, y = position

    # Draw a white rectangle behind the text
    box_padding = 10  # Space around the text
    box_coords = (
        x - box_padding,
        y - box_padding,
        x + text_width + box_padding,
        y + text_height + box_padding,
    )
    draw.rectangle(box_coords, fill="white")

    # Draw the main text (black text)
    draw.text(position, text, font=font, fill="black")

    # Save the image
    image.save(output_path)


def draw_text_with_border(image_path, output_path, text, position, font_size):
    # Create a blank image
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create a bounding box for the text
    x, y = position
    # Draw the border (white text)
    border_offset = 5  # Adjust border thickness
    for offset in range(-border_offset, border_offset + 1):
        draw.text((x + offset, y), text, font=font, fill="white")
        draw.text((x, y + offset), text, font=font, fill="white")

    # Draw the main text (black text)
    draw.text(position, text, font=font, fill="black")

    # Save the image
    image.save(output_path)


# Example usage
image_path = "image.png"  # Replace with your image path
output_path = "output_image.png"  # Where to save the new image
text = "Hello, World!"
position = (50, 50)  # Position (x, y) to place the text
font_size = 36  # Size of the text

draw_text_with_border(image_path, output_path, text, position, font_size)
draw_text_with_box(image_path, output_path, text, position, font_size)
