# Motion-Triggered Face Recognition Access System

This project integrates an Arduino-based ultrasonic motion detector with a Python face recognition pipeline. The Arduino monitors distance changes and signals events to Python scripts, which then trigger a webcam for real-time face verification using DeepFace with the ArcFace model. If the detected face matches an enrolled user above a defined confidence threshold, access is granted.

## Project Structure
project-root/ ├── motion_detection.ino                      # Arduino sketch: ultrasonic sensor and LED 
indicators ├── motion_trigger.py                            # Python: listens to Arduino serial output and 
launches recognition ├── enroll.py                          # Python: enrolls user images into a 
face embedding database ├── realtime_access.py              # Python: performs real-time face 
recognition via webcam ├── enroll/                          # Directory containing subfolders of 
user images │   ├── Alice/ │   └── Bob/ └── face_db.json    # Generated face embedding database


## Hardware Requirements

- Arduino Uno/Nano (or compatible board)
- HC-SR04 ultrasonic sensor
  - Trig → Pin 6
  - Echo → Pin 7
- LEDs for status feedback
  - Red LED → Pin 12 (idle)
  - Green LED → Pin 13 (trigger detected)

## Software Requirements

- Arduino IDE to upload `motion_detection.ino`
- Python 3.8 or higher
- Python libraries:
    deepFace cmd install: "pip install deepface opencv-python numpy pyserial"


## Setup and Usage

1. **Upload Arduino Code**  
 Open `motion_detection.ino` in the Arduino IDE, select the correct board and port, and upload. The Arduino will monitor distance and print "TRIGGER" over serial when motion is detected.

2. **Enroll Users**  
 Place user images in subfolders under `enroll/`, one folder per user. For example:
    enroll/ ├── Alice/ │   ├── alice1.jpg │   └── alice2.jpg └── Bob/ ├── bob1.jpg └── bob2.jpg
Run:
    cmd: 'python enroll.py'

This generates `face_db.json` containing embeddings for each user.

3. **Run Motion Trigger Listener**  
Start the Python listener that waits for Arduino serial output:
    cmd: 'python motion_trigger.py'

Adjust the serial port in the script if necessary. When "TRIGGER" is received, it launches `realtime_access.py`.

4. **Real-Time Face Recognition**  
`realtime_access.py` opens the webcam and compares detected faces against the enrolled database.  
- Default threshold: 0.70  
- If a match is found above threshold, access is granted.  
- Otherwise, access is denied.  
Press `q` to quit the webcam manually.

## File Descriptions

- `motion_detection.ino`: Arduino sketch that reads the ultrasonic sensor, toggles LEDs, and sends "TRIGGER" over serial.
- `motion_trigger.py`: Python script that listens to Arduino serial output and launches `realtime_access.py`.
- `enroll.py`: Builds a face embedding database (`face_db.json`) from images in `enroll/` using DeepFace with ArcFace.
- `realtime_access.py`: Opens the webcam, extracts embeddings, compares against the database, and grants or denies access.

## Testing

1. Place an object within x cm of the ultrasonic sensor.                # This can be tuned within Arduino code
2. Arduino should switch LEDs (red to green) and print "TRIGGER".  
3. Python listener should detect "TRIGGER" and open the webcam.  
4. Present an enrolled face:  
- If recognized, "APPROVED USER" is displayed and access is granted.  
- If not recognized, "Denied" is displayed.

## Troubleshooting

- If the serial port is incorrect, update `COM_PORT` in `motion_trigger.py`.
- If the camera is not found, ensure the webcam is connected and accessible by OpenCV.
- If recognition accuracy is low, add more images per user and re-run `enroll.py`. Adjust the threshold as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
