from PIL import Image, ImageDraw, ImageFont


def textsize(text, font):
    im = Image.new(mode="RGB", size=(1, 1))  # Create a minimal image
    draw = ImageDraw.Draw(im)
    width, height = draw.textbbox((0, 0), text=text, font=font)[
        2:
    ]  # Get width and height
    return width, height


def wrap_text(text, font, max_width):
    """Wrap text to fit within a maximum width."""
    lines = []
    words = text.split()
    if not words:
        return lines

    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        width, _ = textsize(test_line, font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    return lines


def write_image_text(
    input_image_path,
    output_image_path,
    text,
    font_path,
    font_size,
    text_color=(255, 255, 255),
    max_width=None,  # Maximum width for text wrapping
):
    try:
        # Open the input image
        with Image.open(input_image_path) as image:
            # Initialize drawing context
            draw = ImageDraw.Draw(image)

            # Load the font
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text size for each line
            wrapped_lines = []
            if max_width is not None:
                wrapped_lines = wrap_text(text, font, max_width)
            else:
                wrapped_lines = text.split("\n")

            # Calculate total text height
            total_height = sum(textsize(line, font)[1] for line in wrapped_lines)

            # Calculate text position to center it on the image
            image_width, image_height = image.size
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

    except FileNotFoundError:
        print(f"Error: File not found: {input_image_path}")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


input_image_path = "image.jpg"
output_image_path = "output_image.jpg"
text = "Meditate on the ancient religious proverb: You shall not transport human nature on a ship of ivory."
font_path = "font.ttf"  # Path to your TrueType font file
font_size = 40
text_color = (255, 255, 255)  # White color for the text (RGB)
max_width = 1100  # Maximum width for text wrapping

# Call the function to write wrapped text on the image
write_image_text(
    input_image_path,
    output_image_path,
    text,
    font_path,
    font_size,
    text_color,
    max_width,
)
