import time
from fetch_gps import fetch_gps_data
import socket
import time
from datetime import datetime
from update_display import draw_text

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
    draw_text(output_string, (2,2))