import sys
import requests

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

    ip, api_key = "", ""
    for line in lines:
        if line.startswith('ip:'):
            ip = line.split(':')[1].strip()
        elif line.startswith('api:'):
            api_key = line.split(':')[1].strip()
    return ip, api_key

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
        print("Usage: python3 deconzAPIcall.py [state file identifier] [lamp_id] [color] [brightness] [fade-time(seconds)]")
        sys.exit(1)

    state_file_identifier, lamp_id, color, brightness, fade_time = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    ip, api_key = read_state_file(state_file_identifier)
    color_codes = read_color_codes('colours.txt')  # Assuming the color codes are stored in 'colours.txt'
    color_values = color_codes.get(color.upper())
    if not color_values:
        print("Invalid color name")
        sys.exit(1)
    
    response = make_api_call(ip, api_key, lamp_id, color_values, brightness, fade_time)
    print("Response:", response.text)
