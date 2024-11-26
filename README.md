# Hand-Tracking-Mouse-Control
This project allows users to control the mouse pointer and simulate clicks using hand gestures. The system uses a webcam to capture hand movements and the MediaPipe library to detect hand landmarks. The project integrates the OpenCV and autopy libraries to translate hand gestures into mouse actions.

## Project Overview
The project consists of two main components:

1. AiMouse.py: A Python script that captures webcam feed, detects hand gestures, and simulates mouse movements and clicks using the detected gestures.
2. HandTrackingModule2.py: A custom module that uses MediaPipe's hand tracking model to detect hand landmarks and determine gestures like finger up/down or pinch, enabling mouse control.

### Key Features
1. Mouse Movement: Control the mouse pointer by moving the index finger.
2. Mouse Click: Simulate a mouse click by pinching the index and middle fingers.
3. Gesture Detection: Detect multiple gestures, including finger positions and distances between fingers.

### Technology Used
1. Python: The primary programming language used.
2. OpenCV: Used for real-time video capture and image processing.
3. MediaPipe: Used for hand landmark detection and gesture recognition.
4. autopy: Used to control the mouse pointer.
5. NumPy: For numerical operations.

## Installation Instructions

### Prerequisites
Before running the project, ensure the following Python libraries are installed:

1. OpenCV for computer vision tasks.
pip install opencv-python

2. MediaPipe for hand landmark detection.
pip install mediapipe

3. autopy for mouse control.
pip install autopy

### How It Works
1. Hand Tracking: The system uses MediaPipe to detect the position of hand landmarks in the camera feed. These landmarks correspond to key points on the hand, such as the tips of the fingers, which are used to determine the state of the hand.

2. Mouse Control:
a. Moving the Mouse: The system tracks the position of the index finger and maps its movement to the screen coordinates using interpolation.
b. Clicking: When both the index and middle fingers are detected to be close to each other, a click event is triggered.

3. Smooth Movement: To reduce jitter in mouse movement, the script uses a smoothing technique to make the cursor movement more fluid.
