import csv
import requests

def fetch_lamp_states(ip, api_key):
    url = f"http://{ip}/api/{api_key}/lights"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error accessing API for {ip}: {response.status_code}")
        return None

def main():
    with open('zgindex.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lamp_states = fetch_lamp_states(row['ip'], row['api'])
            if lamp_states:
                with open(f"{row['name']}state.txt", mode='w') as state_file:
                    state_file.write(f"name: {row['name']}\n")
                    state_file.write(f"description: {row['description']}\n")
                    state_file.write(f"ds: {row['ds']}\n")
                    state_file.write(f"ip: {row['ip']}\n")
                    state_file.write(f"api: {row['api']}\n")
                    state_file.write("Lamps:\n")
                    for lamp_id, lamp_details in sorted(lamp_states.items(), key=lambda x: int(x[0])):
                        state_file.write(f"  Lamp ID: {lamp_id}\n")
                        state_file.write(f"    Name: {lamp_details.get('name')}\n")
                        state_file.write(f"    Type: {lamp_details.get('type')}\n")
                        state_file.write(f"    State: {lamp_details.get('state')}\n")
                        state_file.write("\n")

if __name__ == "__main__":
    main()
