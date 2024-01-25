import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import threading
from PyQt5.QtCore import pyqtSignal, Qt, QThread
import numpy as np
import cv2
import uvc

dev_list = uvc.device_list()
cap_world = uvc.Capture([ d for d in dev_list if d["name"]=="Pupil Cam1 ID2"][0]["uid"]) 

class MyThread(threading.Thread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        cap_world.frame_mode = (1280, 720, 30)
        while not self._stop_event.is_set():
            print("Thread is running")
            frame = cap_world.get_frame_robust()
            self.change_pixmap_signal.emit(frame.gray)

    def stop(self):
        self._stop_event.set()
        print("Thread stops")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.start_button = QPushButton("Start", self)
        self.start_button.move(50, 50)
        self.start_button.clicked.connect(self.start_thread)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.move(150, 50)
        self.stop_button.clicked.connect(self.stop_thread)

        self.thread = MyThread()

    def update_image_world(self, frame):
            qt_img = self.convert_cv_qt_world(frame)
            self.image_world_label.setPixmap(qt_img)

    def convert_cv_qt_world(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # The frame rgb_image is cropped to remove the housing of the camera
        h, w, ch = rgb_image.shape

        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def start_thread(self):
        self.thread.start()
        #MyThread().thread.change_pixmap_signal.connect(self.update_image_world)

    def stop_thread(self):
        self.thread.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
