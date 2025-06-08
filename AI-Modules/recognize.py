import face_recognition
import cv2
import os
import numpy as np
import datetime
import csv

# === Load known face encodings and names ===
def load_known_faces(known_dir="known_faces"):
    known_encodings = []
    known_names = []
    for filename in os.listdir(known_dir):
        if filename.endswith(('.jpg', '.png')):
            path = os.path.join(known_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

# === Log login/logout info to CSV ===
def log_event(name, event_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_exists = os.path.isfile("logs.csv")

    with open("logs.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["Name", "Event", "Timestamp"])  # header
        writer.writerow([name, event_type, timestamp])
    print(f"{event_type} recorded for {name} at {timestamp}")

# === Track currently logged-in users ===
active_users = {}

print(" Webcam started. Press 'q' to quit.")
known_encodings, known_names = load_known_faces()

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print(" Failed to capture video.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        name = "Not Registered"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

        if best_match_index is not None and matches[best_match_index]:
            name = known_names[best_match_index]

            # Log Login if not already active
            if name not in active_users:
                active_users[name] = datetime.datetime.now()
                log_event(name, "Login")
        else:
            print(" Unregistered user detected. Please register!")

        # Draw bounding box and label
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

    # Show video stream
    cv2.imshow("Face Recognition", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# === Log logout for all active users ===
for name in active_users.keys():
    log_event(name, "Logout")

video_capture.release()
cv2.destroyAllWindows()
