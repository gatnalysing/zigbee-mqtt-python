import csv
import requests

# Function to make API call to Deconz for a specific gateway
def get_lamps(ip, api_key):
    url = f"http://{ip}/api/{api_key}/lights"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error accessing API for {ip}: {response.status_code}")
        return None
# Function to rename a lamp
def rename_lamp(ip, api_key, lamp_id, new_name):
    url = f"http://{ip}/api/{api_key}/lights/{lamp_id}"
    response = requests.put(url, json={"name": new_name})
    return response.ok

# Main script
def main():
    with open('zgindex.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lamps = get_lamps(row['ip'], row['api'])
            if lamps:
                should_rename = None
                for lamp_id, lamp in sorted(lamps.items(), key=lambda x: int(x[0])):
                    lamp_name = lamp.get('name')
                    expected_name = f"{row['ds']}-lampi{str(lamp_id).zfill(3)}"
                    if lamp_name != expected_name:
                        if should_rename is None:
                            user_input = input(f"Rename lamps in {row['name']} to match format {row['ds']}-lampiXXX? (y/n): ")
                            should_rename = user_input.lower() == 'y'
                        if should_rename:
                            rename_lamp(row['ip'], row['api'], lamp_id, expected_name)

                # After possible renaming, fetch updated lamp details
                updated_lamps = get_lamps(row['ip'], row['api'])
                # Create a more human-readable output file
                with open(f"{row['name']}.txt", mode='w') as txt_file:
                    txt_file.write(f"name: {row['name']}\n")
                    txt_file.write(f"description: {row['description']}\n")
                    txt_file.write(f"ds: {row['ds']}\n")
                    txt_file.write(f"ip: {row['ip']}\n")
                    txt_file.write(f"api: {row['api']}\n")
                    txt_file.write(f"api total: {len(lamps)}\n")
                    txt_file.write(f"count: {len(updated_lamps)}\n")
                    txt_file.write("devices: (\n")
                    for lamp_id, lamp in sorted(updated_lamps.items(), key=lambda x: int(x[0])):
                        txt_file.write(f"\t{lamp.get('name')}\n")
                    txt_file.write(")")

if __name__ == "__main__":
    main()
