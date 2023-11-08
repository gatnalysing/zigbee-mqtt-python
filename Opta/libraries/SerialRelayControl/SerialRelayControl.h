#ifndef SerialRelayControl_h
#define SerialRelayControl_h

#include "Arduino.h"
#include "OptaIO.h"

class SerialRelayControl {
public:
  SerialRelayControl(OptaIO &optaIO);
  void begin(int baudRate);
  void update();

private:
  OptaIO &optaIO;
};

#endif
