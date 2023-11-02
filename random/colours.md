

**RED:**
```sh
#RED
mosquitto_pub -h 10.0.0.102 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.701, "y": 0.299}, "brightness": 255}'
```

**GREEN:**
```sh
#GREEN
mosquitto_pub -h 10.0.0.102 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.214, "y": 0.709}, "brightness": 255}'
```

**BLUE:**
```sh
#BLUE
mosquitto_pub -h 10.0.0.102 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.139, "y": 0.081}, "brightness": 255}'
```
