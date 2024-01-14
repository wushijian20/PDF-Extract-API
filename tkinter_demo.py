import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import threading

def choose_video():
    global cap
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.avi *.mp4")])
    if file_path:
        cap = cv2.VideoCapture(file_path)
        play_video()

def play_video():
    global cap, canvas, photo

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)

            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            root.after(int(1000 / 30), play_video)  # 30 FPS
        else:
            cap.release()

# Create main window
root = tk.Tk()
root.title("Video Player")

# Create canvas for video playback
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Button to choose a video file
choose_btn = tk.Button(root, text="Choose Video", command=choose_video)
choose_btn.pack()

# Initialize video capture object
cap = None

# Start the GUI
root.mainloop()
