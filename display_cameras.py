# File: display_cameras.py
# Author: Daniel Molloy <https://github.com/PhysicsDan>
# Last Edited: 2024-02-05 23:43:43

import sys
from os import makedirs

import cv2
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CameraViewer(QMainWindow):
    def __init__(self, camera_streams: list, frame_time_ms: int, save_dir: str):
        """
        Main application window for viewing and saving frames from USB cameras.

        Parameters:
            - camera_streams (list): List of camera indices or stream sources.
            - frame_time_ms (int): Time in milliseconds between frame updates.
            - save_dir (str): Directory to save captured images.

        Attributes:
            - num_cameras (int): Number of cameras or streams.
            - camera_streams (list): List of camera indices or stream sources.
            - cap_list (list): List of OpenCV VideoCapture objects for each camera.
            - save_dir (str): Directory to save captured images.
            - central_widget (QWidget): Central widget of the main window.
            - layout (QVBoxLayout): Layout manager for widgets.
            - labels (list): List of QLabel widgets for displaying camera frames.
            - update_timer (QTimer): Timer for updating camera frames at regular intervals.
            - save_button (QPushButton): Button for saving images.
        """

        # Initialises the object with properties and methods from the QMainWindow parent class.
        # It ensures that the parent class's __init__ method is executed before the child class's
        # (__init__ of CameraViewer) to properly initialize the object with both classes' behavior and attributes.
        super(CameraViewer, self).__init__()

        # Number of cameras or streams
        self.num_cameras = len(camera_streams)

        # List of camera indices or stream sources
        self.camera_streams = camera_streams.copy()

        # List of OpenCV VideoCapture objects for each camera
        self.cap_list = [cv2.VideoCapture(i) for i in camera_streams]

        # Directory to save captured images
        self.save_dir = save_dir
        makedirs(self.save_dir, exist_ok=True)

        # Set up the main window and widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.labels = [QLabel() for _ in range(self.num_cameras)]
        for label in self.labels:
            self.layout.addWidget(label)

        # Set up the timer for updating frames at regular intervals
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_frames)
        self.update_timer.start(int(frame_time_ms))

        # Enable resizing
        self.setAttribute(Qt.WA_StyledBackground)

        # Set minimum size for the main window
        self.setMinimumSize(200, 200)

        # Add a button for saving images
        self.save_button = QPushButton("Save Images", self)
        self.save_button.clicked.connect(self.save_images)
        self.layout.addWidget(self.save_button)

    def update_frames(self):
        # Read frames from each camera and update the labels
        frames = [cap.read()[1] for cap in self.cap_list]

        for i, frame in enumerate(frames):
            if frame is not None:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(
                    rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(q_image)

                # Resize the image to fit the label while maintaining aspect ratio
                pixmap = pixmap.scaledToWidth(
                    self.labels[i].width(), Qt.SmoothTransformation
                )

                self.labels[i].setPixmap(pixmap)

    def save_images(self):
        # Save the current frame from each camera with a timestamped filename
        current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd_hh-mm-ss")

        for i, cap in enumerate(self.cap_list):
            ret, frame = cap.read()
            if ret:
                image_filename = f"{self.save_dir}/camera_{self.camera_streams[i]}_{current_datetime}.png"
                cv2.imwrite(image_filename, frame)
                print(
                    f"Image from Camera {self.camera_streams[i]} saved as {image_filename}"
                )

    def closeEvent(self, event):
        # Release camera objects when the application is closed
        for cap in self.cap_list:
            cap.release()
        event.accept()


if __name__ == "__main__":
    # Set up the PyQt application
    app = QApplication(sys.argv)

    # Specify camera streams, frame update time, and save directory
    camera_streams = [1, 2, 3, 4]
    frame_time_ms = 50
    save_dir = "images/"

    # Create and show the CameraViewer main window
    main_window = CameraViewer(camera_streams, frame_time_ms, save_dir)
    main_window.setWindowTitle("USB Camera Viewer")
    main_window.setGeometry(100, 100, 800, 600)
    main_window.show()

    # Start the PyQt application event loop
    sys.exit(app.exec_())
