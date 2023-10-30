#include "Arduino.h"
#include "OptaIO.h"

OptaIO::OptaIO() {
  // Constructor (if needed)
}

void OptaIO::setupPins() {
  pinMode(BTN_USER, INPUT);
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    pinMode(ledPins[i], OUTPUT);
  }
  for (int i = 0; i < 8; i++) {
    pinMode(inputPins[i], INPUT);
  }
}

bool OptaIO::button(const char* state) {
  int buttonState = digitalRead(BTN_USER);
  if (strcmp(state, "pressed") == 0) {
    return buttonState == LOW;
  } else if (strcmp(state, "released") == 0) {
    return buttonState == HIGH;
  } else {
    return false; // Unknown state
  }
}

bool OptaIO::input(int inputNumber, int state) {
  if (inputNumber >= 1 && inputNumber <= 8) {
    return digitalRead(inputPins[inputNumber - 1]) == state;
  } else {
    // Handle invalid input number
    return false;
  }
}

void OptaIO::relay(int relayNumber, int state) {
  if (relayNumber >= 1 && relayNumber <= 4) {
    digitalWrite(relayPins[relayNumber - 1], state);
    digitalWrite(ledPins[relayNumber - 1], state);
  } else {
    // Handle invalid relay number
  }
}

const int OptaIO::relayPins[4] = {D0, D1, D2, D3};
const int OptaIO::ledPins[4] = {LED_D0, LED_D1, LED_D2, LED_D3};
const int OptaIO::inputPins[8] = {A0, A1, A2, A3, A4, A5, A6, A7};
