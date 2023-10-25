import paho.mqtt.client as mqtt
import time
import random

# MQTT configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "zigbee2mqtt/MyLight/set"

# Establishes the connection to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # Randomly pick a color from the xy space
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        brightness = random.randint(100, 255)
        
        color_payload = f'{{"color": {{"x": {x}, "y": {y}}}, "brightness": {brightness}, "transition": 7}}'
        client.publish(TOPIC, color_payload)
        
        # Wait for the transition to complete plus some extra time for effect
        time.sleep(9)
        
except KeyboardInterrupt:
    print("\nScript stopped by user")
finally:
    client.loop_stop()
    client.disconnect()
