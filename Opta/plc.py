__all__ = ["publish_message"]

import paho.mqtt.client as mqtt
import sys

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def publish_message(message):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("10.0.0.101", 1883, 60)

    client.loop_start()
    
    result = client.publish("RelayControl", payload=message, qos=0, retain=False)
    status = result.rc
    if status == 0:
        print(f"Send `{message}` to topic `RelayControl`")
    else:
        print("Failed to send message to topic `RelayControl`")
    
    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        action = sys.argv[1].upper()
        relay_num = sys.argv[2].upper()  # Convert to uppercase to handle 'A' or 'a'
        
        if action in ["ON", "OFF"] and (relay_num.isdigit() or relay_num == 'A'):
            message = f"{action} {relay_num}"
            publish_message(message)
        else:
            print("Invalid arguments. Please use ON/OFF and a relay number or 'A' for all.")
    else:
        print("Not enough arguments provided. Please run the script with ON/OFF and a relay number or 'A' for all.")
