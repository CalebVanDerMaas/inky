import os
from PIL import Image, ImageDraw, ImageOps
from inky.auto import auto
import calendar
import datetime
from fetch_gps import fetch_gps_data
import random
import time
from collections import deque


cal = calendar.Calendar()
now = datetime.datetime.now()
dates = cal.monthdatescalendar(now.year, now.month)

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

# Define the micro font character positions
microFontDict = {'a': (0, 0, 4, 4), 'b': (4, 0, 8, 4), 'c': (8, 0, 12, 4), 'd': (12, 0, 16, 4,), 'e':(16, 0, 20, 4), 'f': (20, 0, 24, 4), 'g': (24, 0, 28, 4), 'h': (28, 0, 32, 4), 'i': (32, 0, 36, 4), 'j': (36, 0, 40, 4), 'k': (40, 0, 44, 4), 'l': (44, 0, 48, 4), 'm': (48, 0, 52, 4), 'n':(52, 0, 56, 4), 'o':(56, 0, 60, 4), 'p': (60, 0, 64, 4), 'q': (64, 0, 68, 4), 'r': (68, 0, 72, 4), 's': (72, 0, 76, 4), 't': (76, 0, 80, 4), 'u': (80, 0, 84, 4), 'v': (84, 0, 88, 4), 'w': (88, 0, 92, 4), 'x':(92, 0, 96, 4), 'y': (96, 0, 100, 4), 'z':(100, 0, 104, 4), '1': (0, 4, 4, 8), '2': (4, 4, 8, 8), '3': (8, 4, 12, 8), '4': (12, 4, 16, 8), '5':(16, 4, 20, 8), '6': (20, 4, 24, 8), '7': (24, 4, 28, 8), '8': (28, 4, 32, 8), '9': (32, 4, 36, 8), '0': (36, 4, 40, 8), '\'': (40, 4, 44, 8), '\"': (44, 4, 48, 8), '^': (48, 4, 52, 8), '-':(52, 4, 56, 8), '=':(56, 4, 60, 8), '_': (60, 4, 64, 8), '+': (64, 4, 68, 8), '[': (68, 4, 72, 8), ']': (72, 4, 76, 8), '(': (76, 4, 80, 8), ')': (80, 4, 84, 8), '<': (84, 4, 88, 8), '>': (88, 4, 92, 8), '\\':(92, 4, 96, 8), '/': (96, 4, 100, 8), '|':(100, 4, 104, 8), '.':(104, 4, 108, 8), ',': (108, 4, 112, 8),':':(112, 4, 116, 8), ' ':(104, 0, 108, 4)}

def draw_text(input_string, start_pos):
    current_pos = start_pos
    for char in input_string.lower():
        if char in microFontDict:
            crop_region = microFontDict[char]
            char_image = micro_font_sprites.crop(crop_region)
            # Use the character image as a mask to paste white (0) onto the main image
            image.paste(0, current_pos, char_image)
        current_pos = (current_pos[0] + 4, current_pos[1])

random_number = random.randint(1, 3)
GPS_load_imgPath = "GPSLoad" + str(random_number) + ".png"

GPS_load_img = Image.open(f"resources/{GPS_load_imgPath}")

inky_display.set_image(GPS_load_img)
inky_display.show()

time.sleep(6)

gpt_data = None

for attempt in range(60):
    gps_data = fetch_gps_data()
    if gps_data:
        break
    else:
        print(f"Trying again")

if gps_data:
    lat, lon, timestamp = gps_data
    data_string = f"Lat:{lat:.6f},Lon:{lon:.6f},Time:{timestamp}"
else:
    data_string = f"Lat:N/A,Lon:N/A,Time:{now}"

# Open the file in read mode
with open('GPS_DATA.txt', 'r') as file:
    last_line = deque(file, maxlen=1)
    first_word = last_line[0].strip().split()[0]
    print(first_word)
    latest_number = int(first_word)

latest_number += 1 

output_string = str(latest_number) + " " + data_string
# Appending to a file
with open('GPS_DATA.txt', 'a') as file:
    file.write(output_string)

# Open the file in read mode
with open('GPS_DATA.txt', 'r') as file:
    lines = file.readlines()  # Read all lines into a list
    last_30_lines = deque(file, maxlen=30)

start_x = 1
start_y = 1

# Now you can work with last_30_lines
for line in last_30_lines:
    draw_text(line, (start_x, start_y))
    start_y +=4

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