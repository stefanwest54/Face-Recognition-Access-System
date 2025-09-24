## Author: Stefan M. West - ISU - 9/22/2025 1:47 P.M. ##
## Image input, processing and classification. Also will break
#   if approved user is detected. 

import json, base64
import numpy as np
import cv2
from deepface import DeepFace

## Catches images and breaks them down into detectable parts
DB_PATH = "face_db.json"

def b64_to_np(s):
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

with open(DB_PATH, "r") as f:
    raw_db = json.load(f)
DB = {name: b64_to_np(emb) for name, emb in raw_db.items()}

## Opens webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("[ACTION] Cannot open camera.")

GRANT_THRESHOLD = 0.70  # tune this after testing

while True:
    ret, frame = cap.read()
    if not ret:
        break

## detect + align + embed in one call
    try:
        emb_obj = DeepFace.represent(img_path=frame, model_name="ArcFace", enforce_detection=False)
        emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)

        best_name, best_score = "Unknown", -1.0
        for name, ref_emb in DB.items():
            score = cosine_similarity(emb, ref_emb)
            if score > best_score:
                best_score, best_name = score, name

        is_granted = best_score >= GRANT_THRESHOLD
        color = (0, 255, 0) if is_granted else (0, 0, 255)
        label = f"{best_name if is_granted else 'Denied'} | sim={best_score:.2f}"

        cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if is_granted:
            print("[SERIAL] APPROVED USER: " + best_name + " >")
            print("[ACTION] Unlocked And Closing Webcam >")
            print("[ACTION] Back To Listening...")
            break
        
    except Exception as e:
        # No face detected or other error
        pass


    cv2.imshow("ArcFace Access Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[ACTION] Quitting Webcam >")
        print("[ACTION] Back To Listening...")
        break

cap.release()
cv2.destroyAllWindows()
