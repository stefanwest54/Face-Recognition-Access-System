import json, base64
import numpy as np
import cv2
from deepface import DeepFace
import serial

DB_PATH = "face_db.json"
COM_PORT = 'COM5'
BAUD_RATE = 9600
GRANT_THRESHOLD = 0.60  # tune after testing

def b64_to_np(s):
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def verify_user(expected_name):
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

            db = load_db()
            best_name, best_score = "Unknown", -1.0
            for name, data in db.items():
                ref_emb = b64_to_np(data["embedding"])
                score = cosine_similarity(emb, ref_emb)
                if score > best_score:
                    best_score, best_name = score, name

            is_granted = best_score >= GRANT_THRESHOLD
            color = (0, 255, 0) if is_granted else (0, 0, 255)
            label = f"{best_name if is_granted else 'Denied'} | sim={best_score:.2f}"

            cv2.putText(frame, label, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if is_granted and best_name == expected_name:
                print(f"[SERIAL] APPROVED PERSONNEL: {best_name}")
                print("[ACTION] Unlocking and closing webcam.")
                print("[ACTION] Back to listening...")
                ser.write(b"APPROVED\n")
                cap.release()
                cv2.destroyAllWindows()
                return  

        except Exception:
            # No face detected or other error
            pass

        cv2.imshow("ArcFace Access Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[ACTION] Quitting Webcam.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return 

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print("[ACTION] Program initializing...")
print("[ACTION] Listening for RFID...")

while True:
    raw = ser.readline().decode(errors="ignore").strip()
    if not raw:
        continue

    parts = raw.split()
    if len(parts) == 4 and all(len(p) == 2 and all(c in "0123456789ABCDEF" for c in p.upper()) for p in parts):
        uid = raw
        db = load_db()

        matched_user = None
        for name, data in db.items():
            if isinstance(data, dict) and data.get("rfid_uid") == uid:
                matched_user = name
                break

        if matched_user:
            print(f"[SERIAL] APPROVED UID: {uid} belongs to {matched_user}")
            print("[ACTION] Opening webcam...")
            ser.write(b"UID_GOOD\n")
            verify_user(matched_user)  
            
        else:
            print(f"[SERIAL] DENIED PERSONNEL: UNKNOWN UID {uid}")
            ser.write(b"DENIED\n")
