# Home Face Security

This repository contains a script for connecting to a GANZ NVR, running YOLOv8 object detection, and labeling known residents versus unknown persons.

## Configuration

The script reads connection details from environment variables so credentials don't need to be edited directly in the code.

```
NVR_USERNAME - Username for the NVR (default: jakepittman2)
NVR_PASSWORD - Password for the NVR (default: Yellar22)
NVR_HOST     - NVR IP or hostname (default: 192.168.1.100)
NVR_PORT     - RTSP port (default: 554)
NVR_PATH     - Stream path (default: ch1)
```

Place images of residents in `/Users/jake.pittman/Desktop/residents` named `<Name>.jpg` or `<Name>.png` and run:

```bash
python nvr_face_recognition.py
```

Press `q` or Ctrl+C to stop the stream.

## Testing with a webcam

You can try the detection logic using your computer's webcam instead of an NVR. Place resident images in `/Users/jake.pittman/Desktop/residents` and run:

```bash
python webcam_face_recognition.py
```

A window titled `Webcam` will appear. Press `q` or Ctrl+C to stop.
