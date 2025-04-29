from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import pandas as pd

from model.exercise import Exercise
import time
from datetime import datetime

class Fixation(Exercise):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right, central_spot_size=0.0):
        super().__init__(selected_config, recording_label, pupil_labs, cam_left, cam_right)
        self.setWindowTitle("Fixation")

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step_GUI = 0.01
        self.__timer.start(self.__time_step_GUI)

        self.__duration_exo = 1000

        self.__hor_pos = 0
        self.__ver_pos = 0

        self.__size_object_cm = 1

        self.__x = self.get_display_width() / 2 - self.get_size()/2
        self.__y = self.get_display_height() / 2 - self.get_size()/2

        self.set_ratio_pixel_cm()
        self.__central_spot = self.degrees_to_cm(float(central_spot_size)) * self.get_ratio_pixel_cm()

    def scale_hor_pos(self):
        self.__hor_pos = self.__hor_pos  * -self.get_ratio_pixel_cm() 

    def scale_ver_pos(self):
        self.__ver_pos = self.__ver_pos  * self.get_ratio_pixel_cm()

    def update_size_object_cm(self):
        self.__size_object_cm = self.get_size_object_cm()

    def get_duration_exo(self):
        return self.__duration_exo

    def set_duration_exo(self, value):
        self.__duration_exo = value

    def get_hor_pos(self):
        return self.__hor_pos

    def set_hor_pos(self, value):
        self.__hor_pos = value

    def get_ver_pos(self):
        return self.__ver_pos

    def set_ver_pos(self, value):
        self.__ver_pos = value

    def set_x(self):
        self.__x = self.get_display_width() / 2 - self.get_hor_pos() - self.get_size()/2

    def set_y(self):
        self.__y = self.get_display_height() / 2 - self.get_ver_pos() - self.get_size()/2

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

            if self.__central_spot > 0:
                painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                painter.drawEllipse((self.get_display_width() / 2 - self.__central_spot/2), (self.get_display_height()/2 - self.__central_spot/2), self.__central_spot, self.__central_spot)


    def __update(self):
        if self.get_is_recording():
            current_time = time.perf_counter()
            if self.get_start_time() is None:
                self.set_start_time(current_time)
            self.elapsed_time = current_time - self.get_start_time()
            self.get_csv_recorder().record(
                round(self.elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )

        if self.elapsed_time >= self.__duration_exo:
            self.stop_exo()

        self.update()
        
