#ifndef OptaIO_h
#define OptaIO_h

#include "Arduino.h"

class OptaIO {
public:
  OptaIO();
  void setupPins();
  bool button(const char* state);
  bool input(int inputNumber, int state);
  void relay(int relayNumber, int state);

private:
  static const int relayPins[4];
  static const int ledPins[4];
  static const int inputPins[8];
};

#endif
