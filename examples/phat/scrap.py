import requests
import json
import time

# GPS2IP server details
SERVER_IP = "172.20.10.1"  # The IP address you provided
PORT = 11123  # Default port for GPS2IP, change if you've set a different port in the app
URL = f"http://{SERVER_IP}:{PORT}"

def fetch_gps_data():
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            data = json.loads(response.text)
            # latitude = data.get('latitude')
            # longitude = data.get('longitude')
            # timestamp = data.get('timestamp')
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching GPS data: {e}")
        return None

def main():
    while True:
        gps_data = fetch_gps_data()
        if gps_data:
            data = gps_data
            print(f"Data: " + data)
        else:
            print("Failed to fetch GPS data")
        
        time.sleep(5)  # Wait for 5 seconds before the next request

if __name__ == "__main__":
    main()