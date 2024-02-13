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

class VideoThreadWrite(QThread):
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
        self.cap.frame_mode = (192, 192, 30)
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

class VideoThreadLeft(QThread):
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
        self.cap.frame_mode = (192, 192, 30)
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

class CameraWorld(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("World camera")
        self.display_width = 320
        self.display_height = 240
        self.setFixedSize(self.display_width, self.display_height)
        
        self.image_world_label = QLabel(self)

        layout = QHBoxLayout()
        layout.addWidget(self.image_world_label)
        
        self.setLayout(layout)

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

class CameraWrite(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Write camera")
        self.display_width = 400
        self.display_height = 300
        self.setFixedSize(self.display_width, self.display_height)
        
        self.image_write_label = QLabel(self)

        layout = QHBoxLayout()
        layout.addWidget(self.image_write_label)
        
        self.setLayout(layout)

        self.thread_write = None

        self.cap_write = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_camera)
        self.timer.start(5000)

    def check_camera(self):
        dev_list = uvc.device_list()
        if len(dev_list) <= 1:
            print("No UVC devices found. Please connect a camera.")
        else:
            if self.thread_write is None or not self.thread_write.isRunning():
                self.cap_write = uvc.Capture([d for d in dev_list if d["name"]=="Pupil Cam2 ID0"][0]["uid"])

                self.thread_write = VideoThreadWrite(self.cap_write)

                self.thread_write.change_pixmap_signal.connect(self.update_image_write)
                
                self.thread_write.start()

    def start_video(self):
        if self.thread_write is None:
            self.thread_write = VideoThreadLeft(self.cap_write)
            self.thread_write.change_pixmap_signal.connect(self.update_image_write)
            self.thread_write.start()
        else:
            self.thread_write.resume()

    def stop_video(self):
        if self.thread_write is not None:
            self.thread_write.pause()

    def closeEvent(self, event):
        self.thread_write.stop()
        event.accept()

    def update_image_write(self, frame):
        qt_img = self.convert_cv_qt_write(frame)
        self.image_write_label.setPixmap(qt_img)

    def convert_cv_qt_write(self, frame):
        rgb_image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class CameraLeft(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Left camera")
        self.display_width = 400
        self.display_height = 300
        self.setFixedSize(self.display_width, self.display_height)
        
        self.image_left_label = QLabel(self)

        layout = QHBoxLayout()
        layout.addWidget(self.image_left_label)
        
        self.setLayout(layout)

        self.thread_left = None

        self.cap_left = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_camera)
        self.timer.start(5000)

    def check_camera(self):
        dev_list = uvc.device_list()
        if len(dev_list) <= 1:
            print("No UVC devices found. Please connect a camera.")
        else:
            if self.thread_left is None or not self.thread_left.isRunning():
                self.cap_left = uvc.Capture([d for d in dev_list if d["name"]=="Pupil Cam2 ID1"][0]["uid"])

                self.thread_left = VideoThreadLeft(self.cap_left)

                self.thread_left.change_pixmap_signal.connect(self.update_image_left)
                
                self.thread_left.start()

    def start_video(self):
        if self.thread_left is None:
            self.thread_left = VideoThreadLeft(self.cap_left)
            self.thread_left.change_pixmap_signal.connect(self.update_image_left)
            self.thread_left.start()
        else:
            self.thread_left.resume()

    def stop_video(self):
        if self.thread_left is not None:
            self.thread_left.pause()

    def closeEvent(self, event):
        self.thread_left.stop()
        event.accept()

    def update_image_left(self, frame):
        qt_img = self.convert_cv_qt_left(frame)
        self.image_left_label.setPixmap(qt_img)

    def convert_cv_qt_left(self, frame):
        rgb_image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)