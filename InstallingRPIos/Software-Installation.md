
# Zigbee Gateway - Initial Software Installation

1. [WireGuard VPN](#wireguard-vpn)
2. [Mosquitto MQTT Broker](#mosquitto-mqtt-broker)
3. [Zigbee2MQTT Setup](#zigbee2mqtt-setup)

## [WireGuard VPN](https://wireguard.how/client/raspberry-pi-os/ "wireguard.how...")
(https://wireguard.how/client/raspberry-pi-os/)
### Installation

   - Install WireGuard:

      ```
      sudo apt install wireguard
      ```
### Server Configuration

   - Edit the WireGuard server configuration

      ```
      sudo nano /etc/wireguard/wg0.conf
      ```

   - Add the new client to your list of peers in the `wg0.conf` server file
   - Apply the new configuration
     
### Client Configuration

   - Edit the WireGuard client configuration:

      ```
      sudo nano /etc/wireguard/wg0.conf
      ```
   - Install `resolvconf`:
      ```
      sudo apt-get install resolvconf
      ```
   - Set WireGuard to start on boot:
      ```
      sudo systemctl enable wg-quick@wg0
      ```
   - Restart service:
      ```
      sudo systemctl restart wg-quick@wg0
      ```
   - Ping a VPN peer to test
     ```
     ping 10.0.0.1
     ```

[Back to top](#zigbee-gateway---initial-software-installation)


## Mosquitto MQTT Broker

### Installation

- Install Mosquitto and its client tools:
```
sudo apt install -y mosquitto mosquitto-clients
```

### Service Management

- Enable and start the Mosquitto service:
```
sudo systemctl enable mosquitto
```
```
sudo systemctl start mosquitto
```

- Configuration file:
```
sudo nano /etc/mosquitto/mosquitto.conf
```

- Add following lines at the end of file to manage access at fw:
```
listener 1883
allow_anonymous true
```

- Restart service for configurations to take:
```
sudo service mosquitto restart
```

[Back to top](#zigbee-gateway---initial-software-installation)


## [Zigbee2MQTT Setup](https://www.zigbee2mqtt.io/guide/installation/01_linux.html "zigbee2mqtt.io guide")
(https://www.zigbee2mqtt.io/guide/installation/01_linux.html)

### Installation

Install Node.js and dependencies:

```
sudo apt-get update
```
```
sudo apt-get install -y ca-certificates curl gnupg
```
```
sudo mkdir -p /etc/apt/keyrings
```
```
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
```
```
NODE_MAJOR=20
```
```
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
```
```
sudo apt-get update
```
```
sudo apt-get install -y nodejs
```
```
sudo apt-get install -y git
```
Verify the installations:

```
node --version
npm --version
```

Create a directory for Zigbee2MQTT and change its ownership to the current user:

```
sudo mkdir /opt/zigbee2mqtt
```
```
sudo chown -R $USER: /opt/zigbee2mqtt
```

Clone the Zigbee2MQTT repository:

```
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
```
```
cd /opt/zigbee2mqtt
```

Install the required packages:
```
npm ci
```

Build Zigbee2MQTT:
```
npm run build
```

### Running Zigbee2MQTT

To start Zigbee2MQTT for the first time and let it coomplete the initial build:
```
npm start
```
After "`Zigbee2MQTT started!`" message, exit gracefully with `Ctrl`+`C` ("`Stopped Zigbee2MQTT`")

### Running as a Daemon with systemctl

Create a new service file for Zigbee2MQTT:

```bash
sudo nano /etc/systemd/system/zigbee2mqtt.service
```

*Add the following content to the `zigbee2mqtt.service` file:*

```ini
[Unit]
Description=Zigbee2MQTT
After=network.target

[Service]
ExecStart=/usr/bin/npm start
WorkingDirectory=/opt/zigbee2mqtt
StandardOutput=inherit
StandardError=inherit
Restart=always
User=user

[Install]
WantedBy=multi-user.target
```
**Note:** Replace `User=user` with the appropriate username

Enable and start the Zigbee2MQTT service:
```
sudo systemctl enable zigbee2mqtt
```
```
sudo systemctl start zigbee2mqtt
```

Check the status of the service:
```
systemctl status zigbee2mqtt.service
```

[Back to top](#zigbee-gateway---initial-software-installation)
