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
    
    result = client.publish("LEDControl", payload=message, qos=0, retain=False)
    status = result.rc
    if status == 0:
        print(f"Send `{message}` to topic `LEDControl`")
    else:
        print("Failed to send message to topic `LEDControl`")
    
    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1].upper()
        if message in ["ON", "OFF"]:
            publish_message(message)
        else:
            print("Invalid argument. Please enter ON or OFF.")
    else:
        print("No argument provided. Please run the script with ON or OFF argument.")
