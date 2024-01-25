import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QMainWindow, QPushButton
import threading
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer
import numpy as np
import cv2
import uvc

class VideoThreadWorld(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.running = False
        self.paused = False

    def run(self):
        if self.cap is None:
            print("No capture object available.")
            return

        self.running = True
        self.cap.frame_mode = (1280, 720, 30)
        while self.running:
            if not self.paused:
                try:
                    frame = self.cap.get_frame_robust()
                    self.change_pixmap_signal.emit(frame.gray)
                except Exception as e:
                    print(f"Error capturing frame: {e}")
        self.cap.close()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eye camera")
        self.display_width = 640
        self.display_height = 480
        self.setFixedSize(self.display_width, self.display_height)
        self.image_world_label = QLabel(self)
        self.startButton = QPushButton('Start', self)
        self.stopButton = QPushButton('Stop', self)
        self.startButton.clicked.connect(self.start_video)
        self.stopButton.clicked.connect(self.stop_video)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_world_label)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.setLayout(self.layout)

        self.thread_world = None
        self.cap_world = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_camera)
        self.timer.start(5000)

    def check_camera(self):
        dev_list = uvc.device_list()
        if len(dev_list) <= 1:
            print("No UVC devices found. Please connect a camera.")
        else:
            if self.thread_world is None or not self.thread_world.isRunning():
                self.cap_world = uvc.Capture([d for d in dev_list if d["name"]=="Pupil Cam1 ID2"][0]["uid"])
                self.thread_world = VideoThreadWorld(self.cap_world)
                self.thread_world.change_pixmap_signal.connect(self.update_image_world)
                self.thread_world.start()

    def start_video(self):
        if self.thread_world is None:
            self.thread_world = VideoThreadWorld(self.cap_world)
            self.thread_world.change_pixmap_signal.connect(self.update_image_world)
            self.thread_world.start()
        else:
            self.thread_world.resume()

    def stop_video(self):
        if self.thread_world is not None:
            self.thread_world.pause()

    def closeEvent(self, event):
        self.thread_world.stop()
        event.accept()

    def update_image_world(self, frame):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt_world(frame)
        self.image_world_label.setPixmap(qt_img)

    def convert_cv_qt_world(self, frame):
        rgb_image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
