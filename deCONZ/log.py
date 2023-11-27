import csv
import sys
import requests
import datetime
import os

def read_gateway_details(identifier):
    with open('zgindex.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == identifier:
                return row['ip'], row['api'], row['description'], row['ds']
    return None, None, None, None

def api_call(ip, api_key, lamp_id):
    url = f"http://{ip}/api/{api_key}/lights/{lamp_id}"
    response = requests.get(url)
    return response

def log_action(gateway_id, lamp_id, action, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = 'success' if response.ok else 'fail'
    response_data = response.json() if response.ok else 'No Response'

    log_dir = os.path.join('logs', gateway_id)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    unique_id = response_data.get('uniqueid', 'UNKNOWN') if response.ok else 'UNKNOWN'
    unique_id = unique_id.replace(':', '-').replace('/', '-').replace('\\', '-')  # Replace illegal characters
    unique_id_parts = unique_id.split('-')
    formatted_unique_id = f"{lamp_id:03d}-{''.join(unique_id_parts[1:])}"

    log_filename = os.path.join(log_dir, f"{formatted_unique_id}.csv")

    file_exists = os.path.isfile(log_filename)
    with open(log_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Time', 'Action', 'Status', 'Response Data', 'Additional Info'])
        writer.writerow([timestamp, action, status, response_data, ''])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 log.py [gateway identifier] [lamp ID] [action taken]")
        sys.exit(1)

    gateway_id, lamp_id, action = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    ip, api_key, _, _ = read_gateway_details(gateway_id)
    if not ip or not api_key:
        print(f"Gateway {gateway_id} not found in zgindex.csv")
        sys.exit(1)

    response = api_call(ip, api_key, lamp_id)
    log_action(gateway_id, lamp_id, action, response)
