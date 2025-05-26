import cv2
import tkinter as tk
from tkinter import messagebox
from threading import Thread

running = False  # Global flag

def motion_tracking():
    global running
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam")
        return

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while running:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Motion Tracker", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(10) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    running = False

def start_tracking():
    global running
    if not running:
        running = True
        Thread(target=motion_tracking).start()
    else:
        messagebox.showinfo("Info", "Motion tracking is already running.")

def stop_tracking():
    global running
    running = False

# GUI setup
root = tk.Tk()
root.title("Visual Tracking System")
root.geometry("300x150")

label = tk.Label(root, text="Motion Detection & Tracking", font=("Arial", 14))
label.pack(pady=10)

start_btn = tk.Button(root, text="Start Tracking", command=start_tracking)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop Tracking", command=stop_tracking)
stop_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.destroy)
exit_btn.pack(pady=5)

root.mainloop()


