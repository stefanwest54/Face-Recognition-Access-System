## Ultrasonic Activated Computer Vision Access Control
## Author: Stefan West 9/29/2025 7:43 p.m. CST

import json, base64
import numpy as np
import cv2
from deepface import DeepFace
import serial

# CONFIG

DB_PATH = "face_db.json"
COM_PORT = 'COM5'
BAUD_RATE = 9600
GRANT_THRESHOLD = 0.70  # tune after testing

# HELPERS

def b64_to_np(s):
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

# Load face embeddings DB

with open(DB_PATH, "r") as f:
    raw_db = json.load(f)
DB = {name: b64_to_np(emb) for name, emb in raw_db.items()}

# FACE RECOGNITION FUNCTION

def run_face_recognition():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise RuntimeError("[ACTION] Cannot open camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            emb_obj = DeepFace.represent(
                img_path=frame,
                model_name="ArcFace",
                enforce_detection=False
            )
            emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)

            best_name, best_score = "Unknown", -1.0
            for name, ref_emb in DB.items():
                score = cosine_similarity(emb, ref_emb)
                if score > best_score:
                    best_score, best_name = score, name

            is_granted = best_score >= GRANT_THRESHOLD
            color = (0, 255, 0) if is_granted else (0, 0, 255)
            label = f"{best_name if is_granted else 'Denied'} | sim={best_score:.2f}"

            cv2.putText(frame, label, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if is_granted:
                print(f"[SERIAL] APPROVED USER: {best_name} >")
                print("[ACTION] Unlocked And Closing Webcam >")
                print("[ACTION] Back To Listening...")
                ser.write(b"APPROVED\n")
                break

        except Exception:
            # No face detected or other error
            pass

        cv2.imshow("ArcFace Access Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[ACTION] Quitting Webcam >")
            print("[ACTION] Back To Listening...")
            break

    cap.release()
    cv2.destroyAllWindows()

# SERIAL LISTENER LOOP

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print("[ACTION] Listening For TRIGGER...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(f"[SERIAL] {line} >")
        if line == "TRIGGER":
            print("[ACTION] Opening webcam...")
            run_face_recognition()
