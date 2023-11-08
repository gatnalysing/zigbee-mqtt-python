#include <OptaIO.h>
#include <SerialRelayControl.h>

OptaIO optaIO;
SerialRelayControl relayController(optaIO);

void setup() {
  optaIO.setupPins();
  relayController.begin(9600);
}

void loop() {
  relayController.update();
}
