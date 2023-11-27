import sys

# Set this to False if you don't want console output
consoleprintout = True

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

def parse_state_file(state_filename, color, brightness, fade_time, color_codes):
    with open(state_filename, 'r') as file:
        lines = file.readlines()

    api_calls = []
    ip, api_key = "", ""
    for line in lines:
        if line.startswith('ip:'):
            ip = line.split(':')[1].strip()
        elif line.startswith('api:'):
            api_key = line.split(':')[1].strip()
        elif line.startswith('  Lamp ID:'):
            lamp_id = line.split(':')[1].strip()
            color_values = color_codes.get(color.upper())
            if not color_values:
                raise ValueError("Invalid color name")
            transitiontime = fade_time * 10  # Converting fade time from seconds to tenths of a second
            #print("Fade time:", fade_time)
            #print("Transitiontime time:", transitiontime)
            api_call = f"curl -X PUT http://{ip}/api/{api_key}/lights/{lamp_id}/state -d '{{\"xy\": [{color_values['x']}, {color_values['y']}], \"bri\": {brightness}, \"transitiontime\": {transitiontime}}}'"
            api_calls.append(api_call)

    return api_calls

def write_to_file(api_calls, filename='api_calls.txt'):
    with open(filename, 'w') as file:
        for call in api_calls:
            file.write(call + '\n')

def generate_api_calls(state_filename, color, brightness, fade_time, color_codes_filename="colours.txt"):
    color_codes = read_color_codes(color_codes_filename)
    api_calls = parse_state_file(state_filename, color, brightness, fade_time, color_codes)
    write_to_file(api_calls)
    return api_calls

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 apibuilder.py [state file identifier] [color] [brightness] [fade-time(seconds)]")
        sys.exit(1)

    state_file_identifier, color, brightness, fade_time = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    state_filename = state_file_identifier + "state.txt"  # Append 'state.txt' to the file identifier
    api_calls = generate_api_calls(state_filename, color, brightness, fade_time)

    if consoleprintout:
        for call in api_calls:
            print(call)
