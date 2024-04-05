import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import time
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer
import numpy as np
import uvc
from parameters import Parameters

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, cap, position):
        super().__init__()
        parameters = Parameters()
        self.display_width = int(parameters.camera_display_width)
        self.display_height = int(parameters.camera_display_height)

        self.fps = int(parameters.fps)
        self.frame_size_height = int(parameters.frame_size_height)
        self.frame_size_weight = int(parameters.frame_size_weight)
        self.cap = cap

        self.position = position

        self.stop_thread_flag = False

    def run(self):
        try:
            self.cap.frame_mode = (self.frame_size_height, self.frame_size_weight, self.fps)
        except Exception as e:
            print(f"Error capturing frame from  " + self.position + "  camera: {e}")

        while not self.stop_thread_flag:
            try:
                frame = self.cap.get_frame_robust()
                self.change_pixmap_signal.emit(frame.gray)
            except Exception as e:
                print(f"Error capturing frame from  " + self.position + "  camera: {e}")
                break

class Camera(QWidget):
    def __init__(self, exposure_time, id_cam):
        super().__init__()
        self.exposure_time = exposure_time
        parameters = Parameters()
        self.display_width = int(parameters.camera_display_width)
        self.display_height = int(parameters.camera_display_height)
        self.setFixedSize(self.display_width, self.display_height)

        self.fps = int(parameters.fps)
        self.frame_size_height = int(parameters.frame_size_height)
        self.frame_size_weight = int(parameters.frame_size_weight)

        self.thread = None

        self.id_cam = id_cam

        self.position = ""
        if self.id_cam == 1:
            self.position = "left"
        else:
            self.position = "right"

        self.cap = self.get_cap_camera(self.id_cam) 
        if self.cap is not None:
            self.set_exposure_time_camera(self.cap, self.exposure_time)
            self.start_thread()

        self.video_is_running = False

        self.image = QLabel(self) # create the label that holds the image
        self.image.resize(self.display_width, self.display_height)

    def start_thread(self):
        self.cap = self.get_cap_camera(self.id_cam) 
        if self.cap is not None:
            self.set_exposure_time_camera(self.cap, self.exposure_time)
            if self.thread is not None:
                self.thread.stop_thread_flag = True
                self.thread = None
            self.thread = VideoThread(self.cap, self.position)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()        

    def set_exposure_time_camera(self, cap, exposure_time):
        controls_dict = dict([(c.display_name, c) for c in cap.controls])  
        controls_dict['Absolute Exposure Time'].value = exposure_time  # Manually control the value of exposure. 1~32.

    def get_cap_camera(self, id_cam):
        dev_list = uvc.device_list()
        try:
            return uvc.Capture([ d for d in dev_list if d["name"]=="Pupil Cam2 ID" + str(id_cam)][0]["uid"]) # Index eye camera
        except Exception as e:
            print(f"Failed to capture " + self.position + " camera: {e}")
            return None

    def get_cap(self):
        return self.cap

    def set_cap(self, value):
        self.cap = value

    @pyqtSlot(np.ndarray)
    def update_image(self, frame):
        frame_color = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        if self.video_is_running:
            self.video.write(frame_color.astype('uint8'))
            
        qt_img = self.convert_cv_qt(frame_color)
        self.image.setPixmap(qt_img)

    def convert_cv_qt(self, frame):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.id_cam == 0:
            rgb_image = cv2.flip(rgb_image, -1)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)

    def start_recording(self, file_name):
        if not(self.video_is_running):
            self.video_is_running = True
            self.codec = cv2.VideoWriter_fourcc(*"MJPG")  # Codec MJPG
            self.video = cv2.VideoWriter(
                file_name + ".avi", 
                self.codec, fps=self.fps, 
                frameSize=(self.frame_size_height, self.frame_size_weight))
         
    def stop_recording(self):
        if self.video_is_running:
            self.video_is_running = False
            # For the recording of the video
            self.video.release()

