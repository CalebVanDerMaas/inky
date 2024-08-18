import socket
import time
from datetime import datetime

# GPS2IP server details
SERVER_IP = "172.20.10.1"  # The IP address you provided
PORT = 11123  # Default port for GPS2IP, change if you've set a different port in the app

def parse_gprmc(gprmc_sentence):
    parts = gprmc_sentence.split(',')
    if len(parts) < 12 or parts[0] != '$GPRMC':
        return None

    time = parts[1][:2] + ':' + parts[1][2:4] + ':' + parts[1][4:6]
    status = parts[2]
    if status != 'A':
        return None  # 'V' means warning, data not valid

    lat = float(parts[3][:2]) + float(parts[3][2:]) / 60
    if parts[4] == 'S':
        lat = -lat

    lon = float(parts[5][:3]) + float(parts[5][3:]) / 60
    if parts[6] == 'W':
        lon = -lon

    date = '20' + parts[9][4:6] + '-' + parts[9][2:4] + '-' + parts[9][:2]
    timestamp = f"{date} {time}"

    return lat, lon, timestamp

def fetch_gps_data():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, PORT))
            s.settimeout(5)
            data = s.recv(1024).decode('ascii')
            for line in data.split('\n'):
                if line.startswith('$GPRMC'):
                    return parse_gprmc(line)
    except Exception as e:
        print(f"Error fetching GPS data: {e}")
    return None

def main():
    while True:
        gps_data = fetch_gps_data()
        if gps_data:
            lat, lon, timestamp = gps_data
            print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Timestamp: {timestamp}")
        else:
            print("Failed to fetch GPS data")
        
        time.sleep(5)  # Wait for 5 seconds before the next request

if __name__ == "__main__":
    main()