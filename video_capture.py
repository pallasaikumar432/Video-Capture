import cv2
import threading
import tkinter as tk
from tkinter import messagebox

class VideoRecorder:
    def __init__(self, output_file="recorded_video.mp4", camera_index=0, duration=10):
        self.output_file = output_file
        self.camera_index = camera_index
        self.duration = duration
        self.recording = False
        self.thread = None

    def start_recording(self):
        self.recording = True
        self.thread = threading.Thread(target=self.record_video)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.thread is not None:
            self.thread.join()

    def record_video(self):
        # Open the camera
        cap = cv2.VideoCapture(self.camera_index)

        # Check if the camera opened successfully
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera")
            return

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.output_file, fourcc, 20.0, (640, 480))

        start_time = cv2.getTickCount() / cv2.getTickFrequency()
        while self.recording:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret:
                # Write the frame into the output file
                out.write(frame)

                # Display the resulting frame
                cv2.imshow('frame', frame)

                # Check if recording duration exceeded
                current_time = cv2.getTickCount() / cv2.getTickFrequency()
                if (current_time - start_time) >= self.duration:
                    break

                # Press 'q' to stop recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything when done
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Info", f"Video recorded and saved as '{self.output_file}'")

def start_recording():
    recorder.start_recording()

def stop_recording():
    recorder.stop_recording()

# Create a Tkinter window
root = tk.Tk()
root.title("Video Recorder")

# Create a VideoRecorder object
recorder = VideoRecorder()

# Create Start and Stop buttons
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
