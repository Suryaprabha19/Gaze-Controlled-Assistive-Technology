# 👁️ Eye Tracking Virtual Keyboard with Blink Selection

This project implements a virtual keyboard interface that allows users to control directional keys (`Front`, `Reverse`, `Left`, `Right`) using **eye tracking** and **blink detection**. It utilizes a standard webcam and is particularly helpful for accessibility applications or hands-free control systems.

---

## 🔍 Features

- ✅ Real-time **eye tracking** using facial landmarks
- ✅ Detects **double blinks** to trigger key selection
- ✅ Displays a 4-key **virtual keyboard layout** on the screen
- ✅ Uses average eye position to map gaze to a key
- ✅ Simple and lightweight – runs on most computers with a webcam

---
📊 How Blink Detection Works
- EAR (Eye Aspect Ratio) is used to monitor blinks.
- When EAR falls below a threshold (eyes closed), a blink is detected.
- Two consecutive blinks confirm a key press.

---
🧠 How Gaze Detection Works
- Calculates the average position of the left and right eye.
- Matches this position to predefined regions on screen (keys).
- The key under your gaze is marked for selection.

---

## 📦 Requirements

Ensure you have the following installed:

- Python 3.6 or above
- OpenCV
- dlib
- numpy

This project uses shape_predictor_68_face_landmarks.dat from dlib.
- Download the file from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
- Extract the .bz2 file and place the .dat file in the root directory of the project.

---

## 📥 Installation
- Install Required Packages
```bash
pip install opencv-python dlib numpy

