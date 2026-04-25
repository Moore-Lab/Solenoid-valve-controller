#include <Arduino.h>

#define VALVE_PIN 33
#define BAUD_RATE 115200

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(VALVE_PIN, OUTPUT);
  digitalWrite(VALVE_PIN, LOW);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "OPEN") {
      digitalWrite(VALVE_PIN, HIGH);
      Serial.println("OK:OPEN");
    } else if (cmd == "CLOSE") {
      digitalWrite(VALVE_PIN, LOW);
      Serial.println("OK:CLOSE");
    } else {
      Serial.println("ERR:UNKNOWN");
    }
  }
}
