# Reykjavík Street Lamp Project

---

13.02.2024 - Progress update:

**Done:**
- [x] mqtt_pub.py
- [x] mqtt_sub.py
- [x] parse_dev.py
- [x] parse_gw.py
- [x] query_device.py
- [x] device_manager.py
- [x] RGB.py

... more --> [github.com/davidjrb/zgmanager](https://github.com/gatnalysing/zgmanager) 

---

![Street Lights](https://raw.githubusercontent.com/gatnalysing/zigbee-mqtt-python/main/pictures/streetlights.png)


This project marks Reykjavík's step towards smart city integration, beginning with ZigBee-enabled street lamps. It's a foundational step for broader smart initiatives.

## The Plan

We use Flask for ZigBee gateway APIs and Django for our management interface. The project features a real-time interactive map at reykjavik.gatnalysing.is, created with Leaflet and JavaScript, for monitoring and controlling the lamps.

![map in browser](https://github.com/gatnalysing/zigbee-mqtt-python/blob/main/pictures/browsermap.png)

We aim to transition from deCONZ to Zigbee2mqtt, supporting open-source and community-driven development. We're also exploring Python tools like Prometheus and mqtt2prometheus for better logging and monitoring.

While ZigBee may not be the city-wide choice for street light control, it offers insights for Reykjavík's smart-city goals. The project opens possibilities for environmental and traffic sensors, location services, and more.

![aurora](https://github.com/gatnalysing/zigbee-mqtt-python/blob/main/pictures/aurora.png)

Another goal is to integrate [Reykjavík Energy](https://or.is)'s DSMR energy monitoring hardware into our platform. As they are set to offer such services next year, real-time energy data will aid in diagnosing malfunctions earlier. We also plan to make some of this data public on the city's official online map, which could be informative for residents.

## Stay Tuned

We're setting up hardware and learning. Our focus is on foundational work. Community engagement will expand as we progress. Follow our updates here. We'll enhance collaboration and input channels as we become more proficient with Git.

Regards,
The City Lights Team of Reykjavik
