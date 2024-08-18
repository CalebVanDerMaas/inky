import time
from fetch_gps import fetch_gps_data
import socket
import time
from datetime import datetime
from update_display import draw_text
from PIL import Image, ImageDraw, ImageOps
from inky.auto import auto
import os
import calendar
import datetime

# Set up the display
inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.BLACK)

# Create a new palette image
image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
image.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

# Fill the image with black (index 1 in our palette)
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, inky_display.WIDTH, inky_display.HEIGHT), fill=1)

# Load the font sprites
PATH = os.path.dirname(__file__)
micro_font_sprites = Image.open(os.path.join(PATH, "resources/microFontTemplate.png")).convert("1")
micro_font_sprites = ImageOps.invert(micro_font_sprites)  # Invert the font sprites

for attempt in range(1, 61):
    try:
        gps_data = fetch_gps_data()
    except Exception as e:
        print(f'attempt #{attempt} failed: {e}')
        if attempt < retries:
            print("Retrying in 5 seconds...")
            time.sleep(5)
        else:
            print("Max retries reached")

if gps_data: 
    lat, lon, time = gps_data
    output_string = f'lat: {lat}, lon: {lon}, time: {time}'
    print('outputstring: '+ output_string)
    draw_text(output_string, (2,2))
    # Draw debug information
    draw.rectangle([0, 0, inky_display.WIDTH - 1, inky_display.HEIGHT - 1], outline=0)

    # Save the result image for debugging
    image.save("debug_output.png", "PNG")

    try:
        # Display the image
        inky_display.set_image(image)
        inky_display.show()
        print("Image sent to display successfully.")
    except Exception as e:
        print(f"Error displaying image: {e}")

    print(f"Text started at position: ({start_x}, {start_y})")
    print("Debug image saved as 'debug_output.png'")