#include "SerialRelayControl.h"

SerialRelayControl::SerialRelayControl(OptaIO &optaIO) : optaIO(optaIO) {
  // Constructor (if needed)
}

void SerialRelayControl::begin(int baudRate) {
  Serial.begin(baudRate);
}

void SerialRelayControl::update() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command >= '1' && command <= '4') {
      int relayNumber = command - '0'; // Convert ASCII to integer (1 -> 1, 2 -> 2, ...)
      optaIO.relay(relayNumber, HIGH);
    } else if (command >= '5' && command <= '8') {
      int relayNumber = command - '4'; // Convert ASCII to integer (5 -> 1, 6 -> 2, ...)
      optaIO.relay(relayNumber, LOW);
    }
  }
}
