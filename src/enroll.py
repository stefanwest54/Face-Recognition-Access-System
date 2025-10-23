import os, json, base64
import numpy as np
from deepface import DeepFace

ENROLL_DIR = "enroll"
DB_PATH = "face_db.json"

def np_to_b64(arr):
    return base64.b64encode(arr.astype(np.float32).tobytes()).decode("utf-8")

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

db = load_db()

# Process each person folder in ENROLL_DIR
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

        if person in db:
            db[person]["embedding"] = np_to_b64(mean_emb)
            if not db[person].get("rfid_uid"):
                rfid_uid = input(f"Swipe RFID tag for {person}: ")
                db[person]["rfid_uid"] = rfid_uid
        else:
            rfid_uid = input(f"Swipe RFID tag for {person}: ")
            db[person] = {
                "embedding": np_to_b64(mean_emb),
                "rfid_uid": rfid_uid
            }

        print(f"Enrolled/updated {person} with UID {db[person]['rfid_uid']}")

save_db(db)
print(f"Saved {len(db)} identities to {DB_PATH}")