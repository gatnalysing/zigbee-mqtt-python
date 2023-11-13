
# Raspberry Pi Recipe - zigbee2MQTT flavour



1. [Initial Raspberry Pi OS Setup](#initial-raspberry-pi-os-setup)
2. [WireGuard VPN](#wireguard-vpn)
   - [Client Configuration](#client-configuration)
   - [Server Configuration](#server-configuration)
3. [Mosquitto MQTT Broker](#mosquitto-mqtt-broker)
4. [Zigbee2MQTT Setup](#zigbee2mqtt-setup)

## Initial Raspberry Pi OS Setup

- Network install onto SSD: Boot and hold `Shift`.
- Configure system:
  ```
  sudo passwd
  ```
  
  ```
  sudo raspi-config
  ```

- Set locales: UK, IS.
- Enable SSH.
- Change hostname
- apt update / upgrade

## [WireGuard VPN](https://wireguard.how/client/raspberry-pi-os/ "wireguard.how...")
(https://wireguard.how/client/raspberry-pi-os/)
### Installation

   - Install WireGuard:

      ```
      sudo apt install wireguard
      ```
   - Install `resolvconf`:
      ```
      sudo apt-get install resolvconf
      ```
      _(I'm unsure why this step is needed)_
     
### Client Configuration

   - Edit the WireGuard client configuration:

      ```
      sudo nano /etc/wireguard/wg0.conf
      ```

      ```ini
      [Interface]
      Address = X.X.X.X/24
      PrivateKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
      DNS = X.X.X.X # This resolved issues for me
      
      [Peer]
      PublicKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
      Endpoint = # 123.0.0.123:123 # Use IP of your VPN server and port
      AllowedIPs = 0.0.0.0/0 # This is open, restric yours as needed
      PersistentKeepalive = 25 # This resolved issues for me
      ```
   - Set WireGuard to start on boot:
      
      ```
      sudo systemctl enable wg-quick@wg0
      sudo systemctl restart wg-quick@wg0
      ```

### Server Configuration

   - Edit the WireGuard server configuration

      ```
      sudo nano /etc/wireguard/wg0.conf
      ```

   - Add the new client to your list of peers in the `wg0.conf` server file
   - Apply the new configuration

[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)


## Mosquitto MQTT Broker

### Installation

Install Mosquitto and its client tools:

```
sudo apt install -y mosquitto mosquitto-clients
```

### Service Management

Enable and start the Mosquitto service:

```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
Configuration file:

```
sudo nano /etc/mosquitto/mosquitto.conf
```

```
pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

#add these lines:
listener 1883
allow_anonymous true
```
_IMO it's best to restrict access at the fw instead of here_


```
sudo service mosquitto restart
# for mosquitto.conf changes to take effect
```

[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)


## [Zigbee2MQTT Setup](https://www.zigbee2mqtt.io/guide/installation/01_linux.html "zigbee2mqtt.io guide")
(https://www.zigbee2mqtt.io/guide/installation/01_linux.html)

### Installation

Install Node.js and dependencies:

```
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update
sudo apt-get install -y nodejs
```

```
sudo apt-get install -y nodejs git make g++ gcc
```
```
sudo apt-get install -y npm
```

Verify the installations:

```
node --version
npm --version
```

Create a directory for Zigbee2MQTT and change its ownership to the current user:

```bash
sudo mkdir /opt/zigbee2mqtt
sudo chown -R $USER: /opt/zigbee2mqtt
```

Clone the Zigbee2MQTT repository:

```bash
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
cd /opt/zigbee2mqtt
```

Install the required packages:

```bash
npm ci
```

Build Zigbee2MQTT:

```bash
npm run build
```

### Running Zigbee2MQTT

To start Zigbee2MQTT for the first time and let it coomplete the initial build

```bash
cd /opt/zigbee2mqtt
npm start
```
Once it's up and running with a `Zigbee2MQTT started!` message, press `Ctrl`+`C` and wait for it to exit gracefully with a `Stopped Zigbee2MQTT` message at the end.

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
User=pi

[Install]
WantedBy=multi-user.target
```
**Note:** Replace `User=pi` with the appropriate username if you are not using the default 'pi' user.

Enable and start the Zigbee2MQTT service:

```bash
sudo systemctl enable zigbee2mqtt
sudo systemctl start zigbee2mqtt
```

Check the status of the service:

```bash
systemctl status zigbee2mqtt.service
```



[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)
