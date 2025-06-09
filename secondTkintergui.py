import cv2
import threading
import pyttsx3
import time
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)
tts_lock = threading.Lock()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Detection control variables
running = False
paused = False
last_spoken_time = 0
speak_interval = 2  # seconds

# Start detection
def start_detection(event=None):
    global running, paused, last_spoken_time
    running = True
    paused = False
    status_var.set("Status: Running")
    cap = cv2.VideoCapture(0)

    def loop():
        global last_spoken_time

        if not running:
            cap.release()
            return

        if paused:
            lbl_video.after(10, loop)
            return

        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera")
            return

        results = model(frame, show=False)
        detected_labels = set()

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                label = box.cls[0]
                class_name = model.names[int(label)]

                if confidence > 0.5:
                    detected_labels.add(class_name)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        current_time = time.time()
        if detected_labels and current_time - last_spoken_time >= speak_interval:
            threading.Thread(target=speak_detected_objects, args=(detected_labels,)).start()
            last_spoken_time = current_time

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, loop)

    loop()

# Speak labels
def speak_detected_objects(labels):
    if not labels:
        return
    with tts_lock:
        label_list = list(labels)
        if len(label_list) == 1:
            sentence = f"Detected {label_list[0]}"
        else:
            sentence = "Detected " + ", ".join(label_list[:-1]) + f", and {label_list[-1]}"
        engine.say(sentence)
        engine.runAndWait()

# Stop
def stop_detection():
    global running
    running = False
    status_var.set("Status: Stopped")
    lbl_video.config(image='')

# Pause
def pause_detection(event=None):
    global paused
    paused = True
    status_var.set("Status: Paused")

# Resume
def resume_detection(event=None):
    global paused
    paused = False
    status_var.set("Status: Running")

# Exit app
def exit_app(event=None):
    stop_detection()
    root.destroy()

# --------------------- UI ---------------------
root = tk.Tk()
root.title("YOLOv8 Object Detection with TTS")
root.geometry("900x700")
root.configure(bg="#1e1e2f")

# Fonts and styles
font_style = ("Segoe UI", 12)
btn_style = {"font": font_style, "padx": 10, "pady": 5, "bd": 0, "width": 15}

# Video label
lbl_video = tk.Label(root, bg="#1e1e2f")
lbl_video.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

btn_start = tk.Button(btn_frame, text="▶ Start", command=start_detection, bg="#27ae60", fg="white", **btn_style)
btn_start.grid(row=0, column=0, padx=10)

btn_pause = tk.Button(btn_frame, text="⏸ Pause (P)", command=pause_detection, bg="#f39c12", fg="white", **btn_style)
btn_pause.grid(row=0, column=1, padx=10)

btn_resume = tk.Button(btn_frame, text="🔄 Resume (R)", command=resume_detection, bg="#2980b9", fg="white", **btn_style)
btn_resume.grid(row=0, column=2, padx=10)

btn_stop = tk.Button(btn_frame, text="❌ Exit (Q)", command=exit_app, bg="#c0392b", fg="white", **btn_style)
btn_stop.grid(row=0, column=3, padx=10)

# Status
status_var = tk.StringVar()
status_var.set("Status: Not Started")
lbl_status = tk.Label(root, textvariable=status_var, fg="white", bg="#1e1e2f", font=("Segoe UI", 14, "bold"))
lbl_status.pack(pady=10)

# Keyboard bindings
root.bind('p', pause_detection)
root.bind('r', resume_detection)
root.bind('q', exit_app)
root.bind('s', start_detection)


root.mainloop()
