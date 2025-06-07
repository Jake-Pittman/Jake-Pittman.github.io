import cv2
import time
from ultralytics import YOLO
import face_recognition
import numpy as np
import os

# Configuration for connecting to the GANZ NVR
# These can be overridden via environment variables for convenience.
NVR_USERNAME = os.environ.get("NVR_USERNAME", "jakepittman2")
NVR_PASSWORD = os.environ.get("NVR_PASSWORD", "Yellar22")
NVR_HOST = os.environ.get("NVR_HOST", "192.168.1.100")
NVR_PORT = os.environ.get("NVR_PORT", "554")
NVR_PATH = os.environ.get("NVR_PATH", "ch1")

# Build the RTSP URL from the pieces above
RTSP_URL = f"rtsp://{NVR_USERNAME}:{NVR_PASSWORD}@{NVR_HOST}:{NVR_PORT}/{NVR_PATH}"
FACE_TOLERANCE = 0.5

# Load YOLOv8n model for object detection
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

# Attempt to open the RTSP stream and reconnect if needed
def open_stream(url: str) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(url)
    while not cap.isOpened():
        print("❌ Failed to connect to RTSP stream. Retrying in 2s…")
        time.sleep(2)
        cap.release()
        cap = cv2.VideoCapture(url)
    return cap

cap = open_stream(RTSP_URL)

print("\u2705 Connected. Press Ctrl+C or 'q' to stop.")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("\u26A0\uFE0F Stream disconnected, retrying in 2s…")
            time.sleep(2)
            cap.release()
            cap = open_stream(RTSP_URL)
            continue

        # Run YOLO inference
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

        cv2.imshow("NVR Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("\n\uD83D\uDD34 Stopped by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
