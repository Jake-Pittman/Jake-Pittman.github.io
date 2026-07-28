import cv2
import time
from ultralytics import YOLO
import face_recognition
import numpy as np
import os

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# Preload face encodings for all residents
resident_encodings = []
resident_names = []
# Directory containing reference images for known residents
# Update this path if your photos are stored elsewhere
residents_dir = "/Users/jake.pittman/Desktop/residents"
if os.path.isdir(residents_dir):
    for filename in os.listdir(residents_dir):
        if not filename.lower().endswith((".jpg", ".png")):
            continue
        name = os.path.splitext(filename)[0]
        img_path = os.path.join(residents_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encs = face_recognition.face_encodings(image)
        if encs:
            resident_encodings.append(encs[0])
            resident_names.append(name)
else:
    print(f"No Residents directory found at {residents_dir}")

FACE_TOLERANCE = 0.5

# Open the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Unable to access the webcam")

print("\u2705 Webcam connected. Press 'q' to quit.")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("\u26A0\uFE0F Frame capture failed, retrying...")
            time.sleep(0.5)
            continue

        # Run YOLOv8 inference
        results = model(frame)[0]
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls = box.cpu().numpy().astype(int)
            if cls == 16:  # Dog class
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Dog", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif cls == 0:  # Person class
                face_crop = frame[y1:y2, x1:x2]
                face_encs = face_recognition.face_encodings(face_crop)
                if face_encs:
                    matches = face_recognition.compare_faces(
                        resident_encodings, face_encs[0], tolerance=FACE_TOLERANCE
                    )
                    if any(matches):
                        idx = matches.index(True)
                        name = resident_names[idx]
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, f"Resident: {name}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("\n\uD83D\uDD34 Stopped by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
