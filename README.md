
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
[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)


## [Zigbee2MQTT Setup](https://www.zigbee2mqtt.io/guide/installation/01_linux.html "zigbee2mqtt.io guide")
(https://www.zigbee2mqtt.io/guide/installation/01_linux.html)
### Installation

Update the package list and install dependencies:

```
sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
```

Add the NodeSource repository to your system:

```
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update && sudo apt-get install nodejs -y
```

Verify Node.js installation:

```
node --version
npm --version
```

Clone the Zigbee2MQTT repository and install it:

```
sudo mkdir /opt/zigbee2mqtt
sudo chown -R ${USER}: /opt/zigbee2mqtt
git clone --depth 1 https://github.com/Koenkk/zigbee
```
[Back to top](#raspberry-pi-recipe---zigbee2mqtt-flavour)
