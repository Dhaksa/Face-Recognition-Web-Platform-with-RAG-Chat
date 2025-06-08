import face_recognition
import cv2
import os
import numpy as np
import datetime
import csv
import sys

# === Path Setup ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../server"))
KNOWN_DIR = os.path.join(BASE_DIR, "known_faces")
LOGS_CSV = os.path.join(BASE_DIR, "logs.csv")

event_type = sys.argv[1] if len(sys.argv) > 1 else "Login"

def load_known_faces(known_dir):
    known_encodings, known_names = [], []
    for filename in os.listdir(known_dir):
        if filename.endswith(('.jpg', '.png')):
            image = face_recognition.load_image_file(os.path.join(known_dir, filename))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

def log_event(name, event_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(LOGS_CSV)
    with open(LOGS_CSV, "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Event", "Timestamp"])
        writer.writerow([name, event_type, timestamp])
    print(f"{event_type} recorded for {name} at {timestamp}")

# === Load Faces ===
known_encodings, known_names = load_known_faces(KNOWN_DIR)

cap = cv2.VideoCapture(0)
print(f"Press 'q' to finish {event_type.lower()}")

logged_names = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
        name = "Not Registered"

        distances = face_recognition.face_distance(known_encodings, encoding)
        best_match = np.argmin(distances) if len(distances) > 0 else None

        if best_match is not None and matches[best_match]:
            name = known_names[best_match]

            # ✅ Log only once per session
            if name not in logged_names:
                log_event(name, event_type)
                logged_names.add(name)

        # Draw face box
        top *= 4; right *= 4; bottom *= 4; left *= 4
        # Draw bounding box in blue
        box_color = (255, 100, 0)  # light blue
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

        # Draw name background
        label_font = cv2.FONT_HERSHEY_DUPLEX
        text = name
        (text_width, text_height), _ = cv2.getTextSize(text, label_font, 0.8, 2)
        cv2.rectangle(frame, (left, bottom + 5), (left + text_width + 10, bottom + text_height + 15), box_color, cv2.FILLED)

        # Draw name text
        cv2.putText(frame, text, (left + 5, bottom + text_height + 10), label_font, 0.8, (255, 255, 255), 2)

        

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
