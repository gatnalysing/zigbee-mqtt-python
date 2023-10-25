#include <Ethernet.h>
#include <PubSubClient.h>

byte mac[] = {0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45}; 
IPAddress ip(192, 168, 0, 201);  // Set the static IP address
IPAddress broker(192, 168, 0, 66);  // IP address of your MQTT broker

EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

const int ledPin = LED_D0;  // Use the same LED pin from the previous program

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  Ethernet.begin(mac, ip);

  mqttClient.setServer(broker, 1883);
  mqttClient.setCallback(callback);

  connectToMQTT();
}

void connectToMQTT() {
  while (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT...");
    if (mqttClient.connect("OptaPLC")) {
      Serial.println("Connected to MQTT Broker!");
      mqttClient.subscribe("LEDControl");
    } else {
      Serial.print("Failed to connect to MQTT, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Trying again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received [");
  Serial.print(topic);
  Serial.print("] ");

  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (message == "ON") {
    digitalWrite(ledPin, HIGH);
  } else if (message == "OFF") {
    digitalWrite(ledPin, LOW);
  }
}

void loop() {
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  mqttClient.loop();
}
