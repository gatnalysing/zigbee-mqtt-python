
```
sudo systemctl disable zigbee2mqtt
sudo systemctl stop zigbee2mqtt
sudo gpasswd -a $USER dialout
wget -O - http://phoscon.de/apt/deconz.pub.key | \
           sudo apt-key add -
sudo sh -c "echo 'deb http://phoscon.de/apt/deconz \
            $(lsb_release -cs) main' > \
            /etc/apt/sources.list.d/deconz.list"
sudo apt update
sudo apt upgrade -y
sudo apt install deconz -y
sudo systemctl enable deconz
sudo systemctl disable deconz-gui
sudo systemctl stop deconz-gui
sudo systemctl start deconz
```
