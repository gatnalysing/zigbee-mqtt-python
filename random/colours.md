RED
mosquitto_pub -h 10.0.0.101 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.701, "y": 0.299}}'

GREEN
mosquitto_pub -h 10.0.0.101 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.214, "y": 0.709}}'

BLUE
mosquitto_pub -h 10.0.0.101 -t zigbee2mqtt/MyLight/set -m '{"color": {"x": 0.139, "y": 0.081}}'

