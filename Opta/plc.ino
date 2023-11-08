#include <OptaIO.h>
#include <SerialRelayControl.h>

OptaIO optaIO;
SerialRelayControl relayController(optaIO);

void setup() {
  optaIO.setupPins();
  relayController.begin(115200);
}

void loop() {
  relayController.update();
}
