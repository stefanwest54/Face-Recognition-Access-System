# RFID Computer Vision Access Control System (Man Trap)

Author: Stefan M. West  
Date: September 2025  

## Overview
This project combines hardware (Arduino + 5V 2mA 1 channel relay + RFIO-RC522 + electromagnetic lock + LEDs) with software (Python + DeepFace + OpenCV + Arduino) to create an RFID activated, computer vision–based access control system to simulate a modern mantrap.  

The system works as follows:
1. The Arduino monitors for RFID presence.  
2. When a card is detected, Arduino sends the UID to the PC over serial.  
3. DeepFace then checks .json file for UID, if approved the PC activates the webcam and runs facial recognition using ArcFace (DeepFace).
   If denied, PC sends `DENIED` over serial for LED indication 
5. If the face matches an enrolled user above the configured threshold, access is granted and the PC sends `APPROVED` back to the Arduino.  
6. The Arduino provides LED feedback while powering solenoid lock for entry.  

---

## Components
- Arduino board (Uno, Nano, or similar)
- 5V 2mA 1 channel relay
- breadboard
- jumper wires
- RFIO-RC522 RFID tag reader  
- 3 LEDs (red, green, blue) with resistors
- electromagnetic solenoid lock
- Webcam connected to PC (Can use integrated webcam) 
- Python environment with required libraries  

---

## Program 1: UID Interpreter and Access Control (Python)

**File:** `trappem.py`  

### Description
- Listens for `UID` messages from Arduino.
- Approves or denies input based on saved UID.
- If denied, PC sends `DENIED` to Arduino for LED fedback.
- If approved, PC opens the webcam and runs DeepFace facial recognition.  
- Compares embeddings against a JSON database of enrolled users.  
- Grants or denies access based on similarity threshold.  
- Sends `APPROVED` back to Arduino if access is granted.
- Arduino allows power flow to solenoid for a few moments if unlocking.

### Configuration
- `DB_PATH`: path to `face_db.json`  
- `COM_PORT`: serial port for Arduino (e.g., `COM5`)  
- `BAUD_RATE`: default `9600`  
- `GRANT_THRESHOLD`: similarity threshold (default `0.60`)

### Usage 
1.) Run:

        py trappem.py

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
- Accepts RFID UID for 2 factor authentication.
- Generates ArcFace embeddings for each user.  
- Averages embeddings across multiple images per user.  
- Saves normalized embeddings  and UID into `face_db.json`.  

### Usage
1. Create a folder inside `enroll/` with the new user’s name.  
2. Place one or more `.jpg` images of the user inside that folder.  
3. Run:

       py enroll.py
   
5. Input unique UID number for each saved user.
   
## License

This project is licensed under the MIT License. See the LICENSE file for details.
