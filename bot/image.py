import os
import random
import re

from PIL import Image, ImageDraw, ImageFont, ImageStat


def get_rand_font(rand_font):
    font_dir = "assets/fonts"

    if rand_font:
        fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]
        if fonts:
            font_path = os.path.join(font_dir, random.choice(fonts))
        else:
            raise FileNotFoundError("No .ttf files found in the font directory.")
    else:
        font_path = os.path.join(font_dir, "font.ttf")
    print(f"Font Name: {os.path.splitext(os.path.basename(font_path))[0]}")
    return font_path


def compress(input_image_path, max_size_kb=970):
    # Load the image
    image = Image.open(input_image_path)

    # Start with high quality and gradually reduce if needed
    quality = 95
    while True:
        # Save with current quality
        image.save(input_image_path, format="JPEG", quality=quality)

        # Check the file size
        size_kb = os.path.getsize(input_image_path) / 1024  # Convert to KB

        # Stop if size is below target or quality is too low
        if size_kb <= max_size_kb or quality <= 20:
            break

        # Reduce quality incrementally to compress more
        quality -= 5

    print(f"Final size: {size_kb:.2f} KB, quality setting: {quality}")


def image_brightness(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Convert the image to grayscale
    img_gray = img.convert("L")

    # Calculate the brightness of the image
    stat = ImageStat.Stat(img_gray)
    brightness = stat.mean[0]

    # Determine text color based on brightness
    if brightness < 128:
        return (255, 255, 255)  # Use white text for dark backgrounds
    else:
        return (0, 0, 0)  # Use black text for bright backgrounds


def textsize(text, font):
    im = Image.new(mode="RGB", size=(1, 1))  # Create a minimal image
    draw = ImageDraw.Draw(im)
    width, height = draw.textbbox((0, 0), text=text, font=font)[2:]
    return width, height


def resize(input_image_path, output_image_path):
    with Image.open(input_image_path) as im:
        # Calculate the aspect ratio
        aspect_ratio = im.width / im.height

        # Resize the image while maintaining aspect ratio
        if aspect_ratio > 1234 / 694:
            new_width = int(694 * aspect_ratio)
            new_height = 694
        else:
            new_width = 1234
            new_height = int(1234 / aspect_ratio)

        resized_image = im.resize((new_width, new_height), Image.LANCZOS)

        # Center-crop the image to the specified dimensions
        left = (new_width - 1234) / 2
        top = (new_height - 694) / 2
        right = (new_width + 1234) / 2
        bottom = (new_height + 694) / 2
        cropped_image = resized_image.crop((left, top, right, bottom))

        # Save the resized and cropped image
        cropped_image.save(output_image_path)


def split_sentences(text):
    # Split text into sentences
    sentences = re.split(r"(?<=\.)\s+", text)
    return sentences


def wrap_text(text, font, image_width, first_ratio=0.85, other_ratio=0.75):
    """Wrap text to fit within a maximum width with the first line slightly longer than others."""
    # Split the text into sentences
    sentences = split_sentences(text)

    lines = []
    words = text.split()
    if not words:
        return lines

    if len(sentences) >= 2:
        for sentence in sentences:
            # Calculate the width of the entire sentence
            width, _ = textsize(sentence, font)

            # If the sentence width is within the image width, add it directly as a line
            if width <= image_width:
                lines.append(sentence)
            else:
                # Otherwise, apply word-wrapping within this sentence
                current_line = ""
                for word in sentence.split():
                    test_line = f"{current_line} {word}".strip()
                    line_width, _ = textsize(test_line, font)
                    if line_width <= image_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
    else:
        # Set max width for the first and other lines
        first_line_width = image_width * first_ratio
        other_lines_width = image_width * other_ratio

        current_line = words[0]
        is_first_line = True

        for word in words[1:]:
            test_line = current_line + " " + word
            width, _ = textsize(test_line, font)

            # Check if the line width exceeds the appropriate max width
            max_width = first_line_width if is_first_line else other_lines_width
            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
                is_first_line = False

        lines.append(current_line)
    return lines


def calc_max_font_size(text, font_path, image_width):
    """Calculate the maximum font size that fits the text within 75% of the given image width."""
    font_size = 1
    max_width = image_width * 0.75  # Set maximum width to 75% of the image width
    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_width, _ = textsize(text, font)
        if text_width > max_width:
            break
        font_size += 1
    return (
        font_size - 1
    )  # Return the last font size that fit within 75% of the image width


def create(
    input_image_path,
    output_image_path,
    text,
    rand_font,
):
    try:
        resize(input_image_path, output_image_path)
        text_color = image_brightness(input_image_path)
        font_path = get_rand_font(rand_font)

        # Open the input image
        with Image.open(input_image_path) as image:
            # Initialize drawing context
            draw = ImageDraw.Draw(image)

            image_width, image_height = image.size
            # Calculate the maximum font size for the given text and max width
            max_font_size = calc_max_font_size(text, font_path, image_width)

            # Increase font size by 2% if text is over 40 characters
            if len(text) > 40:
                max_font_size = int(max_font_size * 1.5)

            print(f"Font size: {max_font_size}")
            font = ImageFont.truetype(font_path, max_font_size)

            # Split text by newlines, wrapping each line individually
            lines = [wrap_text(line, font, image_width) for line in text.splitlines()]

            # Flatten the list to get a single list of wrapped lines
            wrapped_lines = [item for sublist in lines for item in sublist]

            # Calculate total text height for all wrapped lines
            total_height = sum(textsize(line, font)[1] for line in wrapped_lines)

            # Calculate text position to center it on the image
            text_y = (image_height - total_height) // 2

            # Draw each line of text on the image
            current_y = text_y
            for line in wrapped_lines:
                line_width, line_height = textsize(line, font)
                text_x = (image_width - line_width) // 2
                draw.text((text_x, current_y), line, font=font, fill=text_color)
                current_y += line_height

            # Save the modified image
            image.save(output_image_path)
            print("Text overlaid on image.")
            compress(output_image_path, 970)

    except FileNotFoundError:
        print(f"Error: File not found: {input_image_path}")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
