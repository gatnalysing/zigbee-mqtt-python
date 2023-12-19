# Manual Zigbee2MQTT Installation Guide

## Table of Contents
1. [Prepare Your System](#1-prepare-your-system)
2. [Remove Conflicting Services](#2-remove-conflicting-services-deconz-and-previous-z2m)
3. [Install Mosquitto MQTT Broker](#3-install-mosquitto-mqtt-broker)
4. [Install Zigbee2MQTT](#4-install-zigbee2mqtt)
5. [Final Check](#5-final-check)

## 1. Prepare Your System
- Update and upgrade your system:
  ```bash
  sudo apt update
  sudo apt upgrade -y

## 2. Remove Conflicting Services (deCONZ and Previous Z2M)
- If you have deCONZ installed:
  ```bash
  sudo systemctl stop deconz
  sudo systemctl disable deconz
  sudo systemctl stop deconz-gui
  sudo systemctl disable deconz-gui
  sudo apt remove deconz -y
  sudo rm /etc/apt/sources.list.d/deconz.list
  ```
- If you have an existing Zigbee2MQTT installation:
  ```bash
  sudo systemctl stop zigbee2mqtt
  sudo systemctl disable zigbee2mqtt
  sudo rm -rf /opt/zigbee2mqtt
  ```

## 3. Install Mosquitto MQTT Broker
- Install and start Mosquitto:
  ```bash
  sudo apt install -y mosquitto mosquitto-clients
  sudo systemctl enable mosquitto
  sudo systemctl start mosquitto
  ```
- Configure Mosquitto (optional but recommended):
  ```bash
  sudo nano /etc/mosquitto/mosquitto.conf
  ```
  Add:
  ```bash
  listener 1883
  allow_anonymous true
  ```
  Restart Mosquitto:
  ```bash
  sudo service mosquitto restart
  ```

## 4. Install Zigbee2MQTT
- Install Node.js and dependencies:
  ```bash
  sudo apt-get install -y ca-certificates curl gnupg
  sudo mkdir -p /etc/apt/keyrings
  sudo rm -f /etc/apt/keyrings/nodesource.gpg
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
  sudo apt-get update
  sudo apt-get install -y nodejs git
  ```
- Set up Zigbee2MQTT:
  ```bash
  sudo mkdir /opt/zigbee2mqtt
  sudo chown -R $USER: /opt/zigbee2mqtt
  git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
  cd /opt/zigbee2mqtt
  npm ci
  sudo npm install -g npm@10.2.5
  npm run build
  npm start
  ```
- Start Zigbee2MQTT for the first time and wait for success message:
  
  'Zigbee2MQTT started!'
  'Ctrl+C'
  
- Configure Z2M as a service:
  ```bash
  sudo nano /etc/systemd/system/zigbee2mqtt.service
  ```
  Add the service file content, replacing `User=user` with your username.
  Enable and start the service:
  ```bash
  sudo systemctl enable zigbee2mqtt
  sudo systemctl start zigbee2mqtt
  ```

## 5. Final Check
- Verify everything is working:
  ```bash
  systemctl status zigbee2mqtt
  sudo journalctl -u zigbee2mqtt.service -f
  ```
