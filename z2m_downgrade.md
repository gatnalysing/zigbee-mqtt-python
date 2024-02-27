There have been a lot of problems since upgrade from z2m version 1.33.0

Things have been rough for deconz as well during this time. Not sure what's happenning.

I also noticed a faulty installation of mqtt on a couple of the nodes, so adding that here: 


First things first:
```
sudo apt update
sudo apt upgrade -y
```

```
sudo reboot -y
```

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

## Zigbee2MQTT

### Downgrade to 1.33.0

~~~bash
mkdir ~/Downloads
cd ~/Downloads
wget https://github.com/Koenkk/zigbee2mqtt/archive/refs/tags/1.33.0.tar.gz
~~~


~~~bash
sudo systemctl stop zigbee2mqtt
sudo mv /opt/zigbee2mqtt /opt/zigbee2mqtt_backup
sudo rm -rf /opt/zigbee2mqtt
sudo mkdir /opt/zigbee2mqtt
sudo chown -R $USER: /opt/zigbee2mqtt
sudo tar -zxvf 1.33.0.tar.gz -C /opt/zigbee2mqtt --strip-components=1
~~~


~~~bash
cd /opt/zigbee2mqtt
npm ci
~~~


~~~bash
npm run build
~~~


~~~bash
npm start
~~~

After "`Zigbee2MQTT started!`" message, exit gracefully with `Ctrl`+`C` ("`Stopped Zigbee2MQTT`")

edit conf:

```
nano /opt/zigbee2mqtt/data/configuration.yaml
```

and add:

```
frontend:
  port: 8080 # Port for the web interface
  host: 0.0.0.0 # Optional, default is 0.0.0.0 which allows access from any IP address.
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
other good commands to know:

```
journalctl -u zigbee2mqtt.service -f
```

```
sudo systemctl restart zigbee2mqtt
```

