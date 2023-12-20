# Manual Zigbee2MQTT Installation Guide

## Table of Contents
1. [Prepare Your System](#1-prepare-your-system)
2. [Remove Conflicting Services (deCONZ and Previous Z2M)](#2-remove-conflicting-services-deconz-and-previous-z2m)
3. [Install Mosquitto MQTT Broker](#3-install-mosquitto-mqtt-broker)
4. [Install Zigbee2MQTT](#4-install-zigbee2mqtt)
5. [Prepare Directory and Download Zigbee2MQTT](#5-prepare-directory-and-download-zigbee2mqtt)
6. [Install and Build Zigbee2MQTT](#6-install-and-build-zigbee2mqtt)
7. [Start Zigbee2MQTT for First Time](#7-start-zigbee2mqtt-for-first-time)
8. [Make Changes to Z2M's Configuration.yaml](#8-make-changes-to-z2ms-configurationyaml)
9. [Configure Z2M as a Service](#9-configure-z2m-as-a-service)
10. [Final Check](#10-final-check)

## 1. Prepare Your System
- Update and upgrade your system:
  ```bash
  sudo apt update
  sudo apt upgrade -y
  ```

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

## 5. Prepare Directory and Download Zigbee2MQTT
  ```bash
  sudo mkdir /opt/zigbee2mqtt
  sudo chown -R $USER: /opt/zigbee2mqtt
  git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
  ```
  
## 6. Install and Build Zigbee2MQTT
  ```bash
  cd /opt/zigbee2mqtt
  npm ci
  sudo npm install -g npm@10.2.5
  npm run build
  ```

## 7. Start Zigbee2MQTT for First Time
  ```bash
  npm start
  ```
- Let it set up configurations and wait for the success message:
  ```bash
  Zigbee2MQTT:info  2023-12-19 11:21:37: Zigbee2MQTT started!
  ```
- Press `Ctrl`+`C` to stop the process.

## 8. Make changes to z2m's configuration.yaml
  ```
  nano /opt/zigbee2mqtt/data/configuration.yaml
  ```
  ~~~
  #gateway identifier:
  #zg107
  homeassistant: false
  permit_join: false
  mqtt:
    base_topic: zigbee2mqtt
    server: 'mqtt://localhost'
  #enable webUI:
  frontend:
    port: 8080
  serial:
    port: /dev/ttyACM0
  ~~~

## 9. Configure Z2M as a Service
  ```bash
  sudo nano /etc/systemd/system/zigbee2mqtt.service
  ```
- Remember to add your username
  ```
  [Unit]
  Description=Zigbee2MQTT
  After=network.target
  
  [Service]
  ExecStart=/usr/bin/npm start
  WorkingDirectory=/opt/zigbee2mqtt
  StandardOutput=inherit
  StandardError=inherit
  Restart=always
  User=your-username-here
  
  [Install]
  WantedBy=multi-user.target
  ```
- Enable and start the service:
  ```bash
  sudo systemctl enable zigbee2mqtt
  sudo systemctl start zigbee2mqtt
  ```

## 10. Final Check
- Verify everything is working:
  ```
  systemctl status zigbee2mqtt
  ```
  and/or
  ```
  sudo journalctl -u zigbee2mqtt.service -f
  ```
