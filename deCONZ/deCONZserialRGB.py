import sys
import requests
import time
from log import log_action  # Import the log_action function

def read_color_codes(filename):
    color_codes = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().rstrip(',').split(': ')
            color_name = parts[0].strip()
            xy_values = parts[1].strip('{').strip('}').split(',')
            x = float(xy_values[0].split(':')[1])
            y = float(xy_values[1].split(':')[1])
            color_codes[color_name] = {"x": x, "y": y}
    return color_codes

def read_state_file(state_file_identifier):
    state_filename = state_file_identifier + "state.txt"
    with open(state_filename, 'r') as file:
        lines = file.readlines()

    ip, api_key, lamps = "", "", []
    lamp_id = None
    for line in lines:
        if line.startswith('ip:'):
            ip = line.split(':')[1].strip()
        elif line.startswith('api:'):
            api_key = line.split(':')[1].strip()
        elif line.startswith('  Lamp ID:'):
            lamp_id = line.split(':')[1].strip()
        elif 'Extended color light' in line and lamp_id:
            lamps.append(lamp_id)
            lamp_id = None
    return ip, api_key, lamps

def make_api_call(ip, api_key, lamp_id, color_values, brightness, fade_time):
    url = f"http://{ip}/api/{api_key}/lights/{lamp_id}/state"
    transitiontime = fade_time * 10  # Converting fade time from seconds to tenths of a second
    payload = {
        "xy": [color_values['x'], color_values['y']],
        "bri": brightness,
        "transitiontime": transitiontime
    }
    response = requests.put(url, json=payload)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Error: Incorrect number of arguments provided.")
        print("Usage: python3 deCONZserialRGB.py [state file identifier] [color] [brightness] [fade-time(seconds)] [sleep-time(seconds)]")
        sys.exit(1)

    state_file_identifier, color, brightness_str, fade_time_str, sleep_time_str = sys.argv[1:6]

    try:
        brightness = int(brightness_str)
        fade_time = int(fade_time_str)
        sleep_time = int(sleep_time_str)
    except ValueError:
        print("Error: Brightness, fade-time, and sleep-time must be integers.")
        sys.exit(1)

    ip, api_key, lamps = read_state_file(state_file_identifier)
    color_codes = read_color_codes('colours.txt')
    color_values = color_codes.get(color.upper())

    if not color_values:
        print(f"Invalid color name: {color}")
        sys.exit(1)

    for lamp_id in lamps:
        response = make_api_call(ip, api_key, lamp_id, color_values, brightness, fade_time)
        print(f"Lamp ID {lamp_id} Response:", response.text)

        # Log the action for each lamp
        action_description = f"Changed color to {color}, Brightness {brightness}, Fade time {fade_time}"
        log_action(state_file_identifier, lamp_id, action_description, response)

        time.sleep(sleep_time)
