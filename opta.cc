#include <Ethernet.h>
#include <PubSubClient.h>

byte mac[] = {0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45};
IPAddress ip(192, 168, 0, 201);
IPAddress broker(192, 168, 0, 66);

EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

const int numRelays = 4;
int relayPins[numRelays] = {D0, D1, D2, D3};
int ledPins[numRelays] = {LED_D0, LED_D1, LED_D2, LED_D3};

void setup() {
  Serial.begin(115200);
  
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(relayPins[i], LOW);
    digitalWrite(ledPins[i], LOW);
  }
  
  Ethernet.begin(mac, ip);
  mqttClient.setServer(broker, 1883);
  mqttClient.setCallback(callback);
  connectToMQTT();
}

void connectToMQTT() {
  unsigned long startTime = millis();
  int connectionAttempts = 0;
  
  while (!mqttClient.connected()) {
    if (millis() - startTime > 5000) {
      Serial.println("Connecting to MQTT...");
      if (mqttClient.connect("OptaPLC")) {
        Serial.println("Connected to MQTT Broker!");
        mqttClient.subscribe("RelayControl");
      } else {
        Serial.print("Failed to connect to MQTT, rc=");
        Serial.print(mqttClient.state());
        Serial.println(" Trying again in 5 seconds");
        connectionAttempts++;
        if (connectionAttempts > 5) {
          Serial.println("Too many failed attempts, attempting to reset Ethernet and MQTT...");
          Ethernet.begin(mac, ip);
          mqttClient.setServer(broker, 1883);
          connectionAttempts = 0; // Reset the counter after attempting to reinitialize
        }
      }
      startTime = millis(); // Reset the timer
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

  if (message.startsWith("ON")) {
    int relayNum = message.substring(3).toInt();
    if (relayNum > 0 && relayNum <= numRelays) {
      digitalWrite(relayPins[relayNum - 1], HIGH);
      digitalWrite(ledPins[relayNum - 1], HIGH);
    } else if (relayNum == 0 || message.substring(3) == "A") {
      for (int i = 0; i < numRelays; i++) {
        digitalWrite(relayPins[i], HIGH);
        digitalWrite(ledPins[i], HIGH);
      }
    }
  } else if (message.startsWith("OFF")) {
    int relayNum = message.substring(4).toInt();
    if (relayNum > 0 && relayNum <= numRelays) {
      digitalWrite(relayPins[relayNum - 1], LOW);
      digitalWrite(ledPins[relayNum - 1], LOW);
    } else if (relayNum == 0 || message.substring(4) == "A") {
      for (int i = 0; i < numRelays; i++) {
        digitalWrite(relayPins[i], LOW);
        digitalWrite(ledPins[i], LOW);
      }
    }
  }
}

void loop() {
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  mqttClient.loop();
}
