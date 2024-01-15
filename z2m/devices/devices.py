"""
Zigbee Device List Extractor

This script establishes an SSH connection to a remote Zigbee2MQTT server and retrieves a list of paired Zigbee devices.
The list is then saved as a CSV file in a structured directory format.

Usage: python3 devices.py user@IP_ADDRESS
"""

import paramiko
import yaml
import csv
import sys
import os

def get_paired_devices(ssh_client, file_path):
    with ssh_client.open_sftp() as sftp:
        with sftp.open(file_path) as file:
            data = yaml.safe_load(file)
            return data.get('devices', {}).keys()

def save_to_csv(devices, ip, base_directory):
    gateway_dir = f"zg{ip.split('.')[-1]}"
    directory = os.path.join(base_directory, gateway_dir)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, gateway_dir + ".csv")
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Device'])
        for device in devices:
            writer.writerow([device])

def main(user_at_ip):
    parts = user_at_ip.split('@')
    if len(parts) == 2:
        username, ip = parts
    else:
        username = os.getenv('USER')
        ip = parts[0]

    local_username = os.getenv('USER')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, username=username, key_filename=f'/home/{local_username}/.ssh/id_rsa')

    devices = get_paired_devices(ssh_client, '/opt/zigbee2mqtt/data/configuration.yaml')

    base_directory = 'data'
    save_to_csv(devices, ip, base_directory)
    
    ssh_client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 devices.py user@IP_ADDRESS or python3 devices.py IP_ADDRESS")
        sys.exit(1)

    main(sys.argv[1])

