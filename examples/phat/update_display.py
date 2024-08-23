import os
from PIL import Image, ImageDraw, ImageOps
from inky.auto import auto
import calendar
import datetime
from fetch_gps import fetch_gps_data
import random
import time
from collections import deque
from openai import OpenAI
from dotenv import load_dotenv
import requests
import subprocess


load_dotenv()
api_key = os.getenv('OPEN_API_KEY')

client = OpenAI(
    organization='org-S1Zw4T83HJpCOBs0Xt2ybEGT',
    project='proj_2zk2JdLG6inpTQANIaSVEGeK',
    api_key=api_key
)

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

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

def generate_micro_message():
    # Create user message for micro-message assistant
    client.beta.threads.messages.create(
        "thread_Y3yoH0mjloc75XRZoX26q5HR",
        role="user",
        content="Create a new micro message."
    )

    # Start the run
    run = client.beta.threads.runs.create(
        thread_id="thread_Y3yoH0mjloc75XRZoX26q5HR",
        assistant_id="asst_dkT1sDyjExP1WUJWBYrN1sFv"
    )

    run_id = run.id

    # Wait for completion with timeout
    timeout = 60  # 60 seconds timeout
    start_time = time.time()
    while True:
        run_status = check_run(run_id)
        if run_status == "completed":
            # Retrieve and return the generated message
            messages = client.beta.threads.messages.list(
                thread_id="thread_Y3yoH0mjloc75XRZoX26q5HR"
            )
            return messages.data[0].content[0].text.value
        elif run_status in ["failed", "cancelled", "expired"]:
            raise Exception(f"Run failed with status: {run_status}")
        elif time.time() - start_time > timeout:
            raise Exception("Timeout waiting for response")
        else:
            time.sleep(1)  # Wait for 1 second before checking again

# Check run status
def check_run(run_id):
    run_check = client.beta.threads.runs.retrieve(
        thread_id="thread_Y3yoH0mjloc75XRZoX26q5HR",
        run_id=run_id
    )
    return run_check.status

def try_connect_internet(attempts=60, delay=5):
    for _ in range(attempts):
        if check_internet_connection():
            return True
        time.sleep(delay)
    return False

def try_fetch_gps_data(attempts=60, delay=5):
    for _ in range(attempts):
        gps_data = fetch_gps_data()
        if gps_data:
            return gps_data
        time.sleep(delay)
    return None

def safe_shutdown():
    print("Shutting down safely...")
    os.system('sudo systemctl stop journal_entry.service')
    os.system('sudo shutdown')

random_number = random.randint(1, 3)
GPS_load_imgPath = "GPSLoad" + str(random_number) + ".png"

GPS_load_img = Image.open(f"resources/{GPS_load_imgPath}")

internet_load_img = Image.open(f"resources/ConnectingImage.png")

inky_display.set_image(internet_load_img)
inky_display.show()
time.sleep(10)

while True:
    internet_connected = try_connect_internet()

    if internet_connected:
        inky_display.set_image(GPS_load_img)
        inky_display.show()
        time.sleep(7)

        gps_data = try_fetch_gps_data()

        if gps_data:
            lat, lon, timestamp = gps_data
            data_string = f"Lat:{lat:.6f},Lon:{lon:.6f},Time:{timestamp}"
        else:
            data_string = f"Lat:N/A,Lon:N/A,Time:{time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    else:
        data_string = f"Lat:N/A,Lon:N/A,Time:{time.strftime('%Y-%m-%d %H:%M:%S')}"

    # Generate micro message
    try:
        micro_message = generate_micro_message()
        print(f"Generated micro message: {micro_message}")
    except Exception as e:
        print(f"Error generating micro message: {e}")
        micro_message = "No message this time..."

    clean_micro_message = micro_message.strip('"')
    final_micro_message = "\n" + clean_micro_message

    # Open the file in read mode to get the last index number
    with open('GPS_DATA.txt', 'r') as file:
        last_lines = deque(file, maxlen=2)
        index = last_lines[0].strip().split()[0]
        latest_number = int(index)

    latest_number += 1
    output_string = "\n" + str(latest_number) + " " + data_string

    # Append new data to the file
    with open('GPS_DATA.txt', 'a') as file:
        file.write(output_string)
        file.write(final_micro_message)

    # Display the last 30 lines
    with open('GPS_DATA.txt', 'r') as file:
        last_30_lines = deque(file, maxlen=30)

    start_x = 1
    start_y = 1

    for line in last_30_lines:
        draw_text(line, (start_x, start_y))
        start_y += 4

    draw.rectangle([0, 0, inky_display.WIDTH - 1, inky_display.HEIGHT - 1], outline=0)

    image.save("debug_output.png", "PNG")

    try:
        inky_display.set_image(image)
        inky_display.show()
        print("Image sent to display successfully.")
    except Exception as e:
        print(f"Error displaying image: {e}")

    print(f"Text started at position: ({start_x}, {start_y})")
    print("Debug image saved as 'debug_output.png'")

    safe_shutdown()
    time.sleep(10)
    break  # End the loop