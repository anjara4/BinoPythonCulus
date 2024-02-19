from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math
import pandas as pd
import csv

from screen_calibration import Screen_calibration
from recording import PupilLabs_recorder

class Fixation(QWidget):
    def __init__(self, pupilLabs, recording_label):
        super().__init__()
        self.setWindowTitle("Fixation")

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__selected_config = None
        self.__pupilLabs = pupilLabs
        self.__recording_label = recording_label

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 0.01
        self.__timer.start(self.__time_step)

        self.__delta_time = 0
        self.__current_time = 0

        self.__is_running = False

        self.__time_exo = False

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

    def get_selected_config(self):
        return self.__selected_config

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_size_object_cm(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()

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
        self.scale_size()

    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def get_time_exo(self):
        return self.__time_exo

    def set_time_exo(self, value):
        self.__time_exo = value

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

    def get_is_running(self):
        return self.__is_running

    def set_is_running(self, value):
        self.__is_running = value

    def get_is_recording(self):
        return self.__is_recording

    def set_is_recording(self, value):
        self.__is_recording = value

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def __update(self):
        if self.__current_time < self.__time_exo:
            self.__x = self.__display_width / 2 - self.get_hor_pos() - self.__size/2
            self.__y = self.__display_height / 2 - self.get_ver_pos() - self.__size/2

            if self.get_is_recording():
                self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
            
            self.__current_time = self.__current_time + self.__time_step
        else:
            self.close()
            pupilLabs_recorder = PupilLabs_recorder()
            pupilLabs_recorder.stop_record_pupilLab(self.__pupilLabs)
            self.__recording_label.clear()
        self.update()
