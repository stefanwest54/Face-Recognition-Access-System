const int trigPin = 6;
const int echoPin = 7;
const int blueLED = 11;
const int redLED  = 12;
const int greenLED = 13;
const int relay = 2;

const float triggerDistance = 10;  // cm
const float tolerance = 2;

bool triggered = false;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(relay, OUTPUT);

  Serial.begin(9600);  
  
  digitalWrite(redLED, HIGH);
  digitalWrite(greenLED, LOW);
  digitalWrite(blueLED, LOW);
  digitalWrite(relay, HIGH);
}

void loop() {
  float distance = getFilteredDistance();

  // Listen for PC messages
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "APPROVED") {
      digitalWrite(relay, LOW);
      for (int i = 0; i < 3; i++) {
        digitalWrite(blueLED, HIGH);
        delay(300);
        digitalWrite(blueLED, LOW);
        delay(300);
      }
      delay(1000);
      digitalWirte(relay, HIGH);
    }
  }

 // Ultrasonic trigger logic
  if (distance > 0 && abs(distance - triggerDistance) > tolerance) {
    if (!triggered) {
      triggered = true;
      digitalWrite(redLED, LOW);
      digitalWrite(greenLED, HIGH);
      Serial.println("TRIGGER");
      delay(1000);
      digitalWrite(redLED, HIGH);
      digitalWrite(greenLED, LOW);
      triggered = false;
    }
  }
  delay(100);
}

// Ultrasonic distance function
float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 20000);
  if (duration == 0) return -1;

  return duration * 0.0343 / 2;
}

// Averaging filter
float getFilteredDistance() {
  const int samples = 5;
  float sum = 0;
  int valid = 0;

  for (int i = 0; i < samples; i++) {
    float d = getDistance();
    if (d > 0) {
      sum += d;
      valid++;
    }
    delay(10);
  }

  if (valid == 0) return -1;
  return sum / valid;
}
