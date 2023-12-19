"""
This script automates the management of system reboots based on the 'zigbee2mqtt' service's behavior. 

When it detects that 'zigbee2mqtt' service's restart counter has reached 10, it initiates a system reboot. 

The script's behavior can be inhibited in the configuration file ('disable_reboot.conf')

'disable_reboot.conf' is automatically created on the first run

"""

import subprocess
import re
import time
import os
import configparser

script_dir = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(script_dir, 'disable_reboot.conf')

def create_default_config():
    if not os.path.exists(config_file_path):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        with open(config_file_path, 'w') as configfile:
            configfile.write("# Configuration for reboot script\n")
            configfile.write("# Set disable_reboot to False to enable automatic reboot\n")
            config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    disable_reboot_value = config['DEFAULT'].get('disable_reboot', 'True')
    return disable_reboot_value.lower() == 'false'

def tail_journalctl(service_name):
    process = subprocess.Popen(['journalctl', '-u', service_name, '-f'], stdout=subprocess.PIPE)
    restart_counter = 0
    while True:
        line = process.stdout.readline()
        if line:
            decoded_line = line.decode('utf-8').strip()
            if "Scheduled restart job, restart counter is at" in decoded_line:
                match = re.search(r'restart counter is at (\d+)', decoded_line)
                if match:
                    current_counter = int(match.group(1))
                    if current_counter != restart_counter:
                        restart_counter = current_counter
                        print(f"Restart counter is at {restart_counter}")
                        if restart_counter >= 10:
                            handle_reboot()

def handle_reboot():
    if read_config():
        countdown_for_reboot(60)  # 60 seconds countdown

def countdown_for_reboot(seconds):
    for i in range(seconds, 0, -1):
        if read_config():
            print(f"Rebooting in {i} seconds. Update '{config_file_path}' to abort.")
            time.sleep(1)
        else:
            print("Reboot aborted.")
            return
    subprocess.run(['sudo', 'reboot'], check=True)

def main():
    create_default_config()
    tail_journalctl('zigbee2mqtt')

if __name__ == "__main__":
    main()
