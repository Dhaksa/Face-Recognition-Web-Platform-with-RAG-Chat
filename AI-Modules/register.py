import cv2
import face_recognition
import sqlite3
import os
import time
import csv
import sys
from datetime import datetime

# === Get name from command-line ===
if len(sys.argv) < 2:
    print("Name not provided. Exiting.")
    sys.exit(1)

name = sys.argv[1].strip()

# === Setup directories ===
os.makedirs("known_faces", exist_ok=True)

# === Setup DB ===
DB_PATH = "faces.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
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

# === Webcam loop ===
print(f"Registering user: {name}")
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Could not open webcam.")
    conn.close()
    sys.exit(1)

print("Adjust your face in front of the webcam...")

frame = None
encoding = None

while True:
    ret, frame = video.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Draw rectangles for visualization
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Register Face - Press Q to Cancel", frame)

    if len(face_encodings) > 0:
        encoding = face_encodings[0]
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(" Cancelled by user.")
        conn.close()
        video.release()
        cv2.destroyAllWindows()
        sys.exit(1)

video.release()
cv2.destroyAllWindows()

# === Save to DB ===
encoding_blob = encoding.tobytes()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("INSERT INTO users (name, encoding, registered_at) VALUES (?, ?, ?)",
               (name, encoding_blob, timestamp))
conn.commit()

# === Save image and logs ===
cv2.imwrite(f"known_faces/{name}.jpg", frame)
save_log(name, "Registered")

print(f"Registered {name} at {timestamp}")
print("Log entry added to logs.csv")
conn.close()
