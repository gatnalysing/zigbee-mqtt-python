### Step 1: Insert ConBee II USB Adapter

1. **Plug in the ConBee II USB Adapter:**
   ```plaintext
   Insert the ConBee II USB adapter into an available USB port on the Raspberry Pi.
   ```

---

### Step 2: Install deCONZ (Optional)

*deCONZ is a software that provides a graphical interface for Zigbee networks, and it supports ConBee. If you prefer to use deCONZ alongside Zigbee2MQTT, follow these steps. If not, skip to Step 3.*

2. **Install deCONZ:**
   ```sh
   sudo apt update
   sudo apt install -y deconz
   ```

3. **Enable and Start deCONZ Service:**
   ```sh
   sudo systemctl enable deconz
   sudo systemctl start deconz
   ```

   Access the deCONZ web interface on the default port 80.

---

### Step 3: Configure Zigbee2MQTT for ConBee II

4. **Edit Zigbee2MQTT Configuration File:**
   ```sh
   sudo nano /opt/zigbee2mqtt/data/configuration.yaml
   ```

   Add or modify the following lines to set the serial port for ConBee II (replace `/dev/ttyACM0` with your actual device path if different):
   ```yaml
   serial:
     port: /dev/ttyACM0
   ```

5. **Restart Zigbee2MQTT:**
   ```sh
   sudo systemctl restart zigbee2mqtt
   ```

---

### Step 4: Pair the Test Lamp

6. **Enable Pairing Mode in Zigbee2MQTT:**
   - Publish a message to enable pairing:
     ```sh
     mosquitto_pub -h 10.0.0.101 -t 'zigbee2mqtt/bridge/request/permit_join' -m '{"value":true}'
     ```

7. **Reset Your Lamp and Wait for It to Pair:**
   - Follow the manufacturer’s instructions to reset the lamp and put it in pairing mode.
   - Monitor Zigbee2MQTT logs:
     ```sh
     sudo journalctl -u zigbee2mqtt -f
     ```

---

### Step 5: Test the Lamp

8. **Send a Test Command to the Lamp:**
   - Change the lamp's color:
     ```sh
     mosquitto_pub -h 10.0.0.101 -t 'zigbee2mqtt/MyLight/set' -m '{"color": {"x": 0.701, "y": 0.299}}'
     ```

   - Replace `MyLight` with the lamp’s friendly name.

---

### Step 6: Ensure Backward Compatibility

9. **Check and Update Existing Script:**
   - Make sure the script points to the correct IP and topic.
