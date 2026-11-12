#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("ESP32-C3 dziala");
}

void loop() {
    Serial.println("Test");
    delay(2000);
}