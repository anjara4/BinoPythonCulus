from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math
import pandas as pd
import csv

from screen_calibration import Screen_calibration
from parameters import Parameters

import time
from datetime import datetime

class Fixation(QWidget):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right):
        super().__init__()
        self.setWindowTitle("Fixation")

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__selected_config = selected_config
        self.__recording_label = recording_label
        self.__pupil_labs = pupil_labs
        self.__cam_left = cam_left
        self.__cam_right = cam_right 

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step_GUI = 0.01
        self.__timer.start(self.__time_step_GUI)

        self.__is_running = False

        self.__duration_exo = 1000

        screenCalibration = Screen_calibration()
        self.__size_screen_calibration_object_px = screenCalibration.get_size_object_px()

        self.__size = 50
        self.__color = Qt.red

        self.__hor_pos = 0
        self.__ver_pos = 0

        self.__size_object_cm = 1
        self.__ratio_pixel_cm = 1

        self.__x = self.__display_width / 2 - self.__size/2
        self.__y = self.__display_height / 2 - self.__size/2

        self.__csv_recorder = None
        self.__is_recording = False
        self.__start_time = None
        self.elapsed_time = 0

    def get_selected_config(self):
        return self.__selected_config

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_size_object_cm(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()
        
    def get_depth_from_config(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['Depth'].values.item()

    def degrees_to_cm(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        #return 2 * self.get_depth_from_config() * math.tan(angle_radians)
        return self.get_depth_from_config() * math.tan(angle_radians)

    def scale_hor_pos(self):
        self.__hor_pos = self.__hor_pos  * -self.__ratio_pixel_cm 

    def scale_ver_pos(self):
        self.__ver_pos = self.__ver_pos  * self.__ratio_pixel_cm

    def set_ratio_pixel_cm(self):
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.get_size_object_cm()

    def update_size_object_cm(self):
        self.__size_object_cm = self.get_size_object_cm()

    def get_csv_recorder(self):
        return self.__csv_recorder

    def get_csv_recorder(self, value):
        self.__csv_recorder = value

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value

    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def get_duration_exo(self):
        return self.__duration_exo

    def set_duration_exo(self, value):
        self.__duration_exo = value

    def get_color(self):
        return self.__color

    def set_color(self, value):
        self.__color = value

    def get_hor_pos(self):
        return self.__hor_pos

    def set_hor_pos(self, value):
        self.__hor_pos = value

    def get_ver_pos(self):
        return self.__ver_pos

    def set_ver_pos(self, value):
        self.__ver_pos = value

    def set_is_running(self, value):
        self.__is_running = value

    def set_is_recording(self, value):
        self.__start_time = None
        self.__is_recording = value

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def set_x(self):
        self.__x = self.__display_width / 2 - self.get_hor_pos() - self.__size/2

    def set_y(self):
        self.__y = self.__display_height / 2 - self.get_ver_pos() - self.__size/2

    def paintEvent(self, event):
        if self.__is_running:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def stop_exo(self):
        self.__is_running = False
        self.__is_recording = False

        if self.__cam_left is not None:
            self.__cam_left.stop_recording()
        if self.__cam_right is not None:
            self.__cam_right.stop_recording()

        if self.__pupil_labs.get_status() is not None:
            self.__pupil_labs.stop_record()
        self.__recording_label.clear()
        self.close()

    def __update(self):
        if self.__is_recording:
            current_time = time.perf_counter()
            if self.__start_time is None:
                self.__start_time = current_time
            self.elapsed_time = current_time - self.__start_time
            self.get_csv_recorder().record(
                round(self.elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )

        if self.elapsed_time >= self.__duration_exo:
            self.stop_exo()

        self.update()
        
