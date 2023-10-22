const int buttonPin = BTN_USER; // "USER" button
const int relayPin = D0;
const int ledPin = LED_D0;

bool isButtonHeld = false;
unsigned long buttonPressedTime = 0;
bool flashing = false;

void setup() {
  pinMode(relayPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // BTN_USER is active LOW
  digitalWrite(ledPin, HIGH);
  delay(1000);
}

bool state_change() {
  digitalWrite(relayPin, LOW);
  if (flashingDelay(5000)) return true;
  digitalWrite(relayPin, HIGH);
  if (flashingDelay(5000)) return true;
  return false;
}

bool flashingDelay(unsigned long duration) {
  unsigned long startTime = millis();
  while (millis() - startTime < duration) {
    if (flashing) {
      if ((millis() / 250) % 2 == 0) {
        digitalWrite(ledPin, HIGH);
      } else {
        digitalWrite(ledPin, LOW);
      }
    }
    if (digitalRead(buttonPin) == LOW) { // Button is pressed
      return true; // Interrupted
    }
    delay(1); // Short delay to avoid blocking
  }
  return false; // Completed without interruption
}

void loop() {
  int button_state = digitalRead(buttonPin);
  if (button_state == LOW) { // Button is pressed
    if (!isButtonHeld) {
      buttonPressedTime = millis();
      isButtonHeld = true;
    }
    unsigned long currentTime = millis();
    if (currentTime - buttonPressedTime >= 10000) {
      flashing = true; // Start flashing when button is held for 10 seconds
    }
    if (currentTime - buttonPressedTime > 20000) {
      isButtonHeld = false; // Reset if held for more than 20 seconds
      flashing = false; // Stop flashing
      digitalWrite(ledPin, HIGH);
    }
  } else { // Button is not pressed
    if (isButtonHeld) {
      unsigned long buttonReleasedTime = millis();
      if (buttonReleasedTime - buttonPressedTime >= 10000 && buttonReleasedTime - buttonPressedTime <= 20000) {
        if (state_change()) return;
        if (state_change()) return;
        if (state_change()) return;
        if (state_change()) return;
        flashingDelay(5000);
        state_change();
        digitalWrite(relayPin, LOW);
        delay(5000);
        digitalWrite(relayPin, HIGH);
        flashing = false; // Stop flashing after power cycling is completed
      }
      isButtonHeld = false; // Reset button hold state
    }
    if (!flashing) {
      digitalWrite(ledPin, HIGH);
      digitalWrite(relayPin, HIGH);
      delay(1000);
    }
  }
}
