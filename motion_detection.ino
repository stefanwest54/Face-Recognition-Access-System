// Pin assignments
const int trigPin = 6;
const int echoPin = 7;
const int redLED  = 12;
const int greenLED = 13;
const int blueLED = 11; //

// Trigger parameters (in cm)
const float triggerDistance = 5; // Distance when door is closed
const float tolerance = 1;     // Allowed variation before triggering

// State tracking
bool triggered = false;

void setup() {
  // Initialization for pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // Start serial: higher bit rate
  Serial.begin(115200);

  // Start idle: red ON, green OFF
  digitalWrite(redLED, HIGH);
  digitalWrite(greenLED, LOW);
  digitalWrite(blueLED, LOW); //
}

void loop() {
  float distance = getDistance();
  // Normal trigger logic
  if (abs(distance - triggerDistance) > tolerance) {
    if (!triggered) {
      triggered = true;
      digitalWrite(redLED, LOW);
      digitalWrite(greenLED, HIGH);
      // Word motion_trigger.py is looking for
      Serial.println("TRIGGER"); 
      delay(1000);
      digitalWrite(redLED, HIGH);
      digitalWrite(greenLED, LOW);
    }
    else{
      triggered = false;
    }
    if (Serial.available() > 0) {
      String msg = Serial.readStringUntil('\n');
      msg.trim(); // Remove any extra spaces or newlines
      if (msg == "UNLOCKED") {
        digitalWrite(blueLED, HIGH); // Turn LED  
        Serial.println("Door Unlocked!");
      }
    }
  }
}

// --- Ultrasonic distance function ---
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.0343 / 2; // cm
  return distance;
}
