# 🎯 Virtual Keyboard and Mouse Using Hand Gestures

A Python-based project that uses computer vision to control a virtual keyboard and mouse through hand gestures using a webcam.

## 🚀 Features

- ✋ Real-time hand tracking using a webcam
- 🖱️ Mouse cursor movement using hand gestures
- ⌨️ Virtual keyboard with letters and numbers
- 🤏 Pinch gesture for selecting keys
- 🔠 Space, Backspace, and Enter keys
- 👁️ Live hand landmark detection

## 🛠️ Technologies Used

- Python 3.12
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## 💻 Requirements

- Windows computer
- Python 3.12
- Webcam
- Internet connection for installing the required libraries

## 📦 Installation

Install the required Python libraries using Command Prompt:

```bash
py -3.12 -m pip install mediapipe==0.10.21 opencv-contrib-python==4.11.0.86 numpy pyautogui
```

## ▶️ How to Run

1. Download or clone this repository.
2. Open Command Prompt inside the project folder.
3. Run the virtual keyboard:

```bash
py -3.12 virtual_keyboard.py
```

4. Move your index finger to control the cursor.
5. Bring your thumb and index finger together to select a key.
6. Press `Q` while a project window is active to exit.

## 📂 Project Files

| File | Description |
|---|---|
| `virtual_keyboard.py` | Main virtual keyboard and mouse application |
| `hand_tracking.py` | Hand detection and tracking application |

## 🔮 Future Improvements

- Improve gesture recognition accuracy
- Add more keyboard shortcuts
- Support typing directly into other applications
- Improve cursor movement and calibration

## 👨‍💻 Author

**Dhanush S**

---

⭐ If you find this project interesting, consider giving the repository a star!
