# Ultrasonic Activated Computer Vision Access Control System

Author: Stefan M. West  
Date: September 2025  

## Overview
This project combines hardware (Arduino + ultrasonic sensor + LEDs) with software (Python + DeepFace + OpenCV) to create a motion‑triggered, computer vision–based access control system.  

The system works as follows:
1. The Arduino monitors distance using an ultrasonic sensor.  
2. When motion is detected, the Arduino sends a `TRIGGER` message to the PC over serial.  
3. The PC activates the webcam and runs facial recognition using ArcFace (DeepFace).  
4. If the face matches an enrolled user above the configured threshold, access is granted and the PC sends `APPROVED` back to the Arduino.  
5. The Arduino provides LED feedback to indicate system state and access results.  

---

## Components
- Arduino board (Uno, Nano, or similar)  
- HC‑SR04 ultrasonic sensor  
- 3 LEDs (red, green, blue) with resistors  
- Webcam connected to PC  
- Python environment with required libraries  

---

## Program 1: Ultrasonic Activated Computer Vision Access Control (Python)

**File:** `usacvac.py`  

### Description
- Listens for `TRIGGER` messages from Arduino.  
- Opens the webcam and runs ArcFace facial recognition.  
- Compares embeddings against a JSON database of enrolled users.  
- Grants or denies access based on similarity threshold.  
- Sends `APPROVED` back to Arduino if access is granted.  

### Configuration
- `DB_PATH`: path to `face_db.json`  
- `COM_PORT`: serial port for Arduino (e.g., `COM5`)  
- `BAUD_RATE`: default `9600`  
- `GRANT_THRESHOLD`: similarity threshold (default `0.70`)

### Usage 
1.) Run:

        python usacvac.py

### Requirements
- Python 3.9+  
- OpenCV (`cv2`)  
- DeepFace  
- NumPy  
- PySerial  

---

## Program 2: Face Enrollment Utility (Python)

**File:** `enroll.py`  

### Description
- Enrolls new users by processing `.jpg` images in the `enroll/` directory.  
- Generates ArcFace embeddings for each user.  
- Averages embeddings across multiple images per user.  
- Saves normalized embeddings into `face_db.json`.  

### Usage
1. Create a folder inside `enroll/` with the new user’s name.  
2. Place one or more `.jpg` images of the user inside that folder.  
3. Run:

       python enroll.py

## License

This project is licensed under the MIT License. See the LICENSE file for details.
