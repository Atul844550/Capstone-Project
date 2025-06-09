The application opens your webcam, detects objects in front of it using YOLOv8, and speaks the names of the objects it sees aloud through your computer speakers.
Object Detection and Voice Interaction Desktop App for Visually Impaired

Key Functionalities:
Feature	                          Description
Real-time Detection---	Captures video feed from your webcam and detects multiple objects instantly.
YOLOv8 Integration---	Uses the YOLOv8n.pt model from Ultralytics for accurate and fast detection.
Text-to-Speech (TTS)---	Announces the names of the objects that are detected, using pyttsx3.
Custom GUI (Tkinter)---	Provides Start, Pause, Resume, and Exit buttons in a clean dark-themed UI.
Keyboard Shortcuts---	Press S to start, P to pause, R to resume, and Q to quit.
Multithreading--	Uses threads to run TTS and camera loop simultaneously for smooth experience.

Ideal Use Cases:

Helping visually impaired users understand their surroundings.
Demonstrating real-time AI applications using YOLO.
Building a foundation for intelligent camera systems.
Academic or research use in computer vision projects.


 Possible Extensions:
 
Add object tracking.
Save logs of detected objects.
Add support for multiple languages in TTS.
Build a mobile version (Android with CameraX + TFLite).
Turn into an installer-based Windows .exe app.

Requirements:

opencv-python
ultralytics
pyttsx3
Pillow

