import cv2
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from modules import camera

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(0)  # Abre la cámara (0 es la cámara predeterminada)

        self.canvas = tk.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        self.update()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            #self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(camera.recognize_with_interface()))
            print(self.photo)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = CameraApp(root, "Camera App")
    root.mainloop()
