import os
import subprocess
import sys
import getpass

def check_wg0_conf_exists():
    return os.path.exists('/etc/wireguard/wg0.conf')

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process

def install_wireguard():
    print("Installing WireGuard...")
    os.system('sudo apt install wireguard')
    print("WireGuard installed.")

def configure_wireguard():
    print("Configuring WireGuard...")
    os.system('sudo apt-get install resolvconf')
    os.system('sudo systemctl enable wg-quick@wg0')
    os.system('sudo systemctl restart wg-quick@wg0')
    print("WireGuard configured.")

def install_mosquitto():
    print("Installing Mosquitto MQTT Broker...")
    os.system('sudo apt install -y mosquitto mosquitto-clients')
    os.system('sudo systemctl enable mosquitto')
    os.system('sudo systemctl start mosquitto')
    print("Mosquitto MQTT Broker installed.")

def install_zigbee2mqtt():
    print("Installing Zigbee2MQTT...")
    os.system('sudo apt-get update')
    os.system('sudo apt-get install -y ca-certificates curl gnupg')
    os.system('sudo mkdir -p /etc/apt/keyrings')
    os.system('curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg')
    os.system('echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install -y nodejs')
    os.system('sudo apt-get install -y git')
    os.system('sudo mkdir /opt/zigbee2mqtt')
    os.system('sudo chown -R $USER: /opt/zigbee2mqtt')
    os.system('git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt')
    os.chdir('/opt/zigbee2mqtt')
    os.system('npm ci')
    os.system('npm run build')
    print("Zigbee2MQTT installed.")

def start_zigbee2mqtt():
    print("Starting Zigbee2MQTT...")
    process = run_command('npm start')
    for line in iter(process.stdout.readline, b''):
        print(line.decode(), end='')
        if "Zigbee2MQTT started!" in line.decode():
            process.terminate()
            break
    print("Zigbee2MQTT started and stopped as intended.")

def setup_zigbee2mqtt_service():
    username = getpass.getuser()
    service_content = f"""
[Unit]
Description=Zigbee2MQTT
After=network.target

[Service]
ExecStart=/usr/bin/npm start
WorkingDirectory=/opt/zigbee2mqtt
StandardOutput=inherit
StandardError=inherit
Restart=always
User={username}

[Install]
WantedBy=multi-user.target
"""
    with open('/etc/systemd/system/zigbee2mqtt.service', 'w') as service_file:
        service_file.write(service_content)
    os.system('sudo systemctl enable zigbee2mqtt')
    os.system('sudo systemctl start zigbee2mqtt')
    print("Zigbee2MQTT service configured with the current user.")


if __name__ == '__main__':
    if not check_wg0_conf_exists():
        print("wg0.conf file not found. Please ensure it exists before running this script.")
        sys.exit(1)

    install_wireguard()
    configure_wireguard()
    install_mosquitto()
    install_zigbee2mqtt()
    start_zigbee2mqtt()
    setup_zigbee2mqtt_service()

    print("Installation and configuration complete.")
