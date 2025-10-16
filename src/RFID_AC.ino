//RFID activator for trappem.py
//Author: Stefan West

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 53
#define RST_PIN 49
MFRC522 mfrc522(SS_PIN, RST_PIN);

const int blueLED  = 3;
const int redLED   = 4;
const int greenLED = 5;
const int relay    = 2;


void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(relay, OUTPUT);

  digitalWrite(redLED, HIGH);
  digitalWrite(greenLED, LOW);
  digitalWrite(blueLED, LOW);
  digitalWrite(relay, LOW);

  Serial.println("[ACTION] ARDUINO READY");

}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    if (msg == "APPROVED") {
      unlockSequence();
    }
    else if (msg == "DENIED") {
      deniedSequence();
    }
    else if (msg == "UID_GOOD"){
      goodUID();
    }
  }
  
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;
  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println("[ACTION] Card Scanned...");
  Serial.println(content);
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

void unlockSequence() {
  digitalWrite(relay, HIGH);
  digitalWrite(redLED, LOW);
  for (int i = 0; i < 5; i++) {
    digitalWrite(blueLED, HIGH);
    delay(300);
    digitalWrite(blueLED, LOW);
    delay(300);
  }
  delay(1000);
  digitalWrite(relay, LOW);
  digitalWrite(redLED, HIGH);
}

void deniedSequence() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(redLED, LOW);
    delay(300);
    digitalWrite(redLED, HIGH);
    delay(300);
  }
}

void goodUID(){
  digitalWrite(redLED, LOW);
  for (int i = 0; i < 5; i++) {
    digitalWrite(greenLED, HIGH);
    delay(300);
    digitalWrite(greenLED, LOW);
    delay(300);
  }
  digitalWrite(redLED, HIGH);
}

