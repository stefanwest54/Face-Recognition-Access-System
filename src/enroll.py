## Author: Stefan M. West - ISU - 9/19/2025 7:19 P.M. ##
## Create new approved user in enroll folder.
## Add approved user's .jpg files to user folder.
## Run "python enroll.py" in powershell to write new
#   user to .JSON within same directory folder.
## User will then be recognized and categorized by model

import os, json, base64
import numpy as np
from deepface import DeepFace

ENROLL_DIR = "enroll"
DB_PATH = "face_db.json"

def np_to_b64(arr):
    return base64.b64encode(arr.astype(np.float32).tobytes()).decode("utf-8")

db = {}

## Adds pictures in new save file to path for deepFace
for person in os.listdir(ENROLL_DIR):
    person_dir = os.path.join(ENROLL_DIR, person)
    if not os.path.isdir(person_dir):
        continue

    embeddings = []
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        try:
            emb_obj = DeepFace.represent(img_path=img_path, model_name="ArcFace", enforce_detection=True)
            emb = np.array(emb_obj[0]["embedding"], dtype=np.float32)
            embeddings.append(emb)
        except Exception as e:
            print(f"Skipping {img_path}: {e}")

    if embeddings:
        mean_emb = np.mean(np.stack(embeddings), axis=0)
        mean_emb /= np.linalg.norm(mean_emb)
        db[person] = np_to_b64(mean_emb)

with open(DB_PATH, "w") as f:
    json.dump(db, f)

print(f"Saved {len(db)} identities to {DB_PATH}")
