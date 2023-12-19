## Pairing Lamps to Zigbee2MQTT Gateway

1. Set Zigbee2MQTT gateway to pairing mode:
   ```
   mosquitto_pub -h 10.0.0.X -t 'zigbee2mqtt/bridge/request/permit_join' -m '{"value": true, "time": 3600}'
   ```
   
3. Reset lamps to their factory settings and enable pairing:
    
   - In 5 second intervals turn lamps off and on until they start flashing
   - Let the lamps flash about 10 times for about 10 seconds
   - Turn the lamps off and on again, twice more for 5 seconds

  Depiction of sequence as stated by Dresden:
     ![Factory Reset of Zigbee Lamp](https://raw.githubusercontent.com/gatnalysing/zigbee-mqtt-python/main/pictures/factoryresetlamp.jpeg)


4. Once in pairing mode lamps will hopefully join your zigbee network:
   - Check  [`webUI`](http://10.0.0.X:8080/) or configuration file for joined devices
   ```
   nano /opt/zigbee2mqtt/data/configuration.yaml
   ```
5. Once done cancel pairing on gateway:
   ```
   mosquitto_pub -h 10.0.0.X -t 'zigbee2mqtt/bridge/request/permit_join' -m '{"value": false}'
   ```
