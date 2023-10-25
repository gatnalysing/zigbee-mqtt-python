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
int relayMapping[numRelays] = {0, 1, 2, 3}; // User-friendly relay number to pin index mapping
int inputPins[8] = {A0, A1, A2, A3, A4, A5, A6, A7};

unsigned long lastReconnectAttempt = 0;
unsigned long reconnectInterval = 5000; // 5 seconds


void initializePinMappings() {
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    pinMode(ledPins[i], OUTPUT);
  }
  
  for (int i = 0; i < 8; i++) {
    pinMode(inputPins[i], INPUT);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Starting up...");

  initializePinMappings();
  
  Ethernet.begin(mac, ip);
  mqttClient.setServer(broker, 1883);
  mqttClient.setCallback(callback);
  connectToMQTT();
}

bool connectToMQTT() {
  if (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT...");
    if (mqttClient.connect("OptaPLC")) {
      Serial.println("Connected to MQTT Broker!");
      mqttClient.subscribe("RelayControl");
      return true;
    } else {
      Serial.print("Failed to connect to MQTT, rc=");
      Serial.println(mqttClient.state());
      return false;
    }
  }
  return true; // Already connected
}

void sendAck(String message) {
  mqttClient.publish("RelayControl/Ack", message.c_str());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received [");
  Serial.print(topic);
  Serial.print("] ");

  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  handleMQTTMessage(message);
}

void setRelayState(int relayNumber, bool state) {
  if (relayNumber >= 1 && relayNumber <= numRelays) {
    int pinIndex = relayMapping[relayNumber - 1]; // User-friendly relay number to pin index
    digitalWrite(relayPins[pinIndex], state);
    digitalWrite(ledPins[pinIndex], state);
    sendAck("Executed: " + String(relayNumber) + " to " + String(state));
  } else {
    Serial.println("Error: Invalid relay number");
    sendAck("Error: Invalid relay number");
  }
}

void handleMQTTMessage(String message) {
  // Assume message format is "ON X" or "OFF X"
  String command = message.substring(0, 3); // Extract ON or OFF, adjusted to 3 to include space
  String relay = message.substring(3);
  relay.trim(); // Remove leading/trailing white spaces
  
  bool state = command.startsWith("ON");
  
  if (relay == "A") {
    for (int i = 1; i <= numRelays; i++) { // Start from 1
      setRelayState(i, state);
    }
    sendAck("Executed: ALL to " + String(state));
  } else {
    int relayNumber = relay.toInt(); // Convert string to int
    if(relayNumber == 0 && relay != "0") {
      Serial.println("Error: Invalid relay identifier");
      sendAck("Error: Invalid relay identifier");
    } else {
      setRelayState(relayNumber, state);
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String serialCommand = Serial.readStringUntil('\n');
    serialCommand.trim();
    if (serialCommand.length() > 0) {
      Serial.println("Serial command received: " + serialCommand);
      handleSerialCommand(serialCommand);
    }
  }

  if (!mqttClient.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > reconnectInterval) {
      lastReconnectAttempt = now;
      if (connectToMQTT()) {
        lastReconnectAttempt = 0;
      }
    }
  } else {
    mqttClient.loop();
    handleInputs();
  }
}

void handleSerialCommand(String command) {
  if (command.startsWith("ON") || command.startsWith("OFF")) {
    handleMQTTMessage(command);
  } else {
    Serial.println("Error: Invalid serial command");
  }
}

void handleInputs() {
  static int lastInputStates[8];
  static bool firstRun = true;
  
  if (firstRun) {
    for (int i = 0; i < 8; i++) {
      lastInputStates[i] = digitalRead(inputPins[i]);
    }
    firstRun = false;
  }

  // High priority: If I1 (A0) or I2 (A1) is HIGH, set all relays HIGH
  if (digitalRead(inputPins[0]) == HIGH || digitalRead(inputPins[1]) == HIGH) { // Using inputPins array
    for (int i = 0; i < numRelays; i++) {
      setRelayState(i + 1, HIGH); // i + 1 to convert to user-friendly relay number
    }
    return; // Exit the function early
  }

  // Read all inputs and report to MQTT if there is any change
  for (int i = 0; i < 8; i++) {
    int currentState = digitalRead(inputPins[i]);
    if (currentState != lastInputStates[i]) {
      lastInputStates[i] = currentState;
      // Construct topic string, e.g., "InputState/0"
      char topic[15];
      sprintf(topic, "InputState/%d", i);
      // Send state to MQTT
      mqttClient.publish(topic, currentState == HIGH ? "1" : "0");
    }
  }
}
