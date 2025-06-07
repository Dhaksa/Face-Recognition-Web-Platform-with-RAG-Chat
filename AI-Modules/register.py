import cv2
import face_recognition
import sqlite3
import os
import time
import csv
from datetime import datetime

# === Setup Directories ===
os.makedirs("known_faces", exist_ok=True)

# === Setup DB ===
DB_PATH = "faces.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL,
    registered_at TEXT NOT NULL
)
''')
conn.commit()

# === Save to logs.csv ===
def save_log(name, action="Registered"):
    log_file = "logs.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(log_file)

    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Action", "Timestamp"])
        writer.writerow([name, action, timestamp])

# === Webcam Access ===
name = input("Enter your name for registration: ").strip()

video = cv2.VideoCapture(0)
print("📸 Opening camera. Please look directly into the webcam.")
time.sleep(3)

ret, frame = video.read()
video.release()

if not ret:
    print("❌ Failed to capture image.")
    conn.close()
    exit()

# === Face Detection & Encoding ===
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

if len(face_encodings) == 0:
    print("❌ No face detected. Try again.")
    conn.close()
    exit()

# Save first face found
encoding = face_encodings[0]
encoding_blob = encoding.tobytes()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# === Save to SQLite ===
cursor.execute("INSERT INTO users (name, encoding, registered_at) VALUES (?, ?, ?)",
               (name, encoding_blob, timestamp))
conn.commit()

# === Save captured photo ===
cv2.imwrite(f"known_faces/{name}.jpg", frame)

# === Save to logs.csv ===
save_log(name, "Registered")

# === Success Message ===
print(f"✅ Registered {name} at {timestamp}")
print("📝 Log entry added to logs.csv")

# Cleanup
conn.close()
cv2.destroyAllWindows()
