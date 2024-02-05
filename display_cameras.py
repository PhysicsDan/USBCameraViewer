import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton
from os import makedirs

class CameraViewer(QMainWindow):
    def __init__(self, num_cameras, save_dir):
        super(CameraViewer, self).__init__()

        self.num_cameras = num_cameras
        self.cap_list = [cv2.VideoCapture(i) for i in range(num_cameras)]
        self.save_dir = save_dir
        makedirs(self.save_dir, exist_ok=True)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.labels = [QLabel() for _ in range(self.num_cameras)]

        for label in self.labels:
            self.layout.addWidget(label)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_frames)
        self.update_timer.start(30)

        # Enable resizing
        self.setAttribute(Qt.WA_StyledBackground)

        # Set minimum size for the main window
        self.setMinimumSize(200, 200)

        # Add a button for saving images
        self.save_button = QPushButton("Save Images", self)
        self.save_button.clicked.connect(self.save_images)
        self.layout.addWidget(self.save_button)

    def update_frames(self):
        frames = [cap.read()[1] for cap in self.cap_list]

        for i, frame in enumerate(frames):
            if frame is not None:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                # Resize the image to fit the label while maintaining aspect ratio
                pixmap = pixmap.scaledToWidth(self.labels[i].width(), Qt.SmoothTransformation)

                self.labels[i].setPixmap(pixmap)

    def save_images(self):
        current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd_hh-mm-ss")

        for i, cap in enumerate(self.cap_list):
            ret, frame = cap.read()
            if ret:
                image_filename = f"{self.save_dir}/camera_{i + 1}_{current_datetime}.png"
                cv2.imwrite(image_filename, frame)
                print(f"Image from Camera {i + 1} saved as {image_filename}")

    def closeEvent(self, event):
        for cap in self.cap_list:
            cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    num_cameras = 1
    save_dir = "images/"
    main_window = CameraViewer(num_cameras, save_dir)
    main_window.setWindowTitle("Camera Viewer")
    main_window.setGeometry(100, 100, 800, 600)
    main_window.show()

    sys.exit(app.exec_())

