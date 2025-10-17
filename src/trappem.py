## RFID Activated Computer Vision Access Control
## Author: Stefan West 

import json, base64
import numpy as np
import cv2
from deepface import DeepFace
import serial

# CONFIG

users = {
    "D0 69 46 2B": "Jack",
    "A0 01 E8 2B": "Alice",
    "F6 63 15 25": "Mike",
}

DB_PATH = "face_db.json"
COM_PORT = 'COM5'
BAUD_RATE = 9600
GRANT_THRESHOLD = 0.60  # tune after testing

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
                print(f"[SERIAL] APPROVED PERSONELLE: {best_name}.")
                print("[ACTION] Unlocked And Closing Webcam.")
                print("[ACTION] Back To Listening...")
                ser.write(b"APPROVED\n")
                break

        except Exception:
            # No face detected or other error
            pass

        cv2.imshow("ArcFace Access Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[ACTION] Quitting Webcam.")
            print("[ACTION] Back To Listening...")
            break

    cap.release()
    cv2.destroyAllWindows()

# SERIAL LISTENER LOOP
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print("[ACTION] Program initializing...")
print("[ACTION] ARDUINO READY.")

while True:
    raw = ser.readline().decode(errors="ignore").strip()
    if not raw:
        continue
    
    parts = raw.split()
    if len(parts) == 4 and all(len(p) == 2 and all(c in "0123456789ABCDEF" for c in p.upper()) for p in parts):
        uid = raw

        if uid in users:
            name = users[uid]
            print("[SERIAL] APPROVED PERSONELLE: ", name)
            print("[ACTION] Opening webcam...")
            ser.write(b"UID_GOOD\n")
            run_face_recognition()
        else:
            print("[SERIAL] DENIED PERSONELLE: UNKNOWN UID")

            ser.write(b"DENIED\n")
