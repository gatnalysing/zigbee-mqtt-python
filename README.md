
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
  ```bash
  sudo raspi-config
Set locales: UK, IS.
Enable SSH.
Change hostname


## [WireGuard VPN](https://wireguard.how/client/raspberry-pi-os/ "wireguard.how...")
(https://wireguard.how/client/raspberry-pi-os/)
### Installation

Install WireGuard:

```
sudo apt install wireguard
```

### Client Configuration

Edit the WireGuard client configuration:

```bash
sudo nano /etc/wireguard/wg0.conf
```

Your `wg0.conf` should resemble the following:

```ini
[Interface]
Address = 10.0.0.103/24
PrivateKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
DNS = 8.8.8.8

[Peer]
PublicKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
Endpoint = XXX.XXX.XXX.XX:XXXXX
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

If needed, install `resolvconf`:

```
sudo apt-get install resolvconf
```

You might need to reboot for the changes to take effect:

```
sudo reboot
```

Set WireGuard to start on boot:

```
sudo systemctl enable wg-quick@wg0
sudo systemctl restart wg-quick@wg0
```
[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)

### Server Configuration

Edit the WireGuard server configuration:

```
sudo nano /etc/wireguard/wg0.conf
```

Add your client to the list of `Peers`:

```ini
[Interface]
Address = 10.0.0.1/32
ListenPort = 51820
PrivateKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp0s25 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp0s25 -j MASQUERADE

[Peer]
# client1
PublicKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
AllowedIPs = 10.0.0.x/32

# Additional peers can be added similarly
```

Apply the configuration:

```
sudo wg syncconf wg0 <(sudo wg-quick strip wg0)
```

After making changes to the configuration, a reboot is recommended:

```
sudo reboot
```
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

Check the service status:

```
sudo systemctl status mosquitto
```

View the default configuration file:

```
cat /etc/mosquitto/mosquitto.conf
```

For testing it can be useful to open access by uncommenting:
```
pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

listener 1883
#allow_anonymous true
```
Remember to comment again and restart after changes:

```
sudo service mosquitto restart
```

[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)


## [Zigbee2MQTT Setup](https://www.zigbee2mqtt.io/guide/installation/01_linux.html "zigbee2mqtt.io guide")
(https://www.zigbee2mqtt.io/guide/installation/01_linux.html)

### Determine Adapter Location

First, check the location of your Zigbee adapter:

```bash
ls -l /dev/ttyACM0
```

Or if you have multiple adapters, find the specific one by ID:

```bash
ls -l /dev/serial/by-id
```

### Installation

Install Node.js and other dependencies:

```bash
sudo curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs git make g++ gcc
```

Verify the installation:

```bash
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

### Configuring Zigbee2MQTT

Copy the example configuration file and edit it as needed:

```bash
cp /opt/zigbee2mqtt/data/configuration.example.yaml /opt/zigbee2mqtt/data/configuration.yaml
nano /opt/zigbee2mqtt/data/configuration.yaml
```

### Running Zigbee2MQTT

To start Zigbee2MQTT:

```bash
cd /opt/zigbee2mqtt
npm start
```

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

Enable and start the Zigbee2MQTT service:

```bash
sudo systemctl enable zigbee2mqtt
sudo systemctl start zigbee2mqtt
```

Check the status of the service:

```bash
systemctl status zigbee2mqtt.service
```

**Note:** Replace `User=pi` with the appropriate username if you are not using the default 'pi' user.


Please ensure that the username and paths are correct for your specific setup, and adjust the Node.js version in the curl command if needed.



[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)
