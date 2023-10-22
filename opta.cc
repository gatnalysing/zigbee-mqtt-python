int button_state = 0;  // Breyta til að lesa stöðu á rofa

void setup() {
  pinMode(D0, OUTPUT); // Arduino opta Relay 1
  pinMode(LED_D0, OUTPUT);  //Arduino opta LED 0
  delay(1000);
}

void state_change(){
  digitalWrite(LED_D0,LOW);
  digitalWrite(D0, LOW);
  delay(5000);
  digitalWrite(LED_D0, HIGH);
  digitalWrite(D0, HIGH);
  delay(5000);
}

void loop() {
  button_state = digitalRead(BTN_USER);  // BTN_USER er innbyggði rofinn
  if (button_state == LOW){
    delay(1500);
    state_change();
    state_change();
    state_change();
  // partur 2
    state_change();
    delay(5000);
  // partur 3
    state_change();
    digitalWrite(LED_D0,LOW);
    digitalWrite(D0, LOW);
    delay(5000);
    digitalWrite(LED_D0,HIGH);
    digitalWrite(D0, HIGH);
  }
  else {  
    digitalWrite(LED_D0,HIGH);
    digitalWrite(D0, HIGH);
    delay(1000);
  }
    
}
