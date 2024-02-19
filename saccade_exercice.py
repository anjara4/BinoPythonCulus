from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math
import pandas as pd
import csv

from screen_calibration import Screen_calibration
from recording import PupilLabs_recorder

class Saccade(QWidget):
    def __init__(self, pupilLabs, recording_label): 
        super().__init__()
        self.setWindowTitle("Saccade")

        self.__selected_config = None
        self.__pupilLabs = pupilLabs
        self.__recording_label = recording_label 

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        screenCalibration = Screen_calibration()
        self.__size_screen_calibration_object_px = screenCalibration.get_size_object_px()

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 1000
        self.__timer.start(self.__time_step)

        self.__delta_time = self.__time_step/1000
        self.__current_time = self.__delta_time

        self.__is_running = False
        self.__nb_cycle = -1
        self.__cpt_cycle = 0

        self.__size = 50
        self.__color = Qt.red
        self.__delta_hor = 50
        self.__delta_ver = 50
        self.__is_object_on_left = False

        self.__size_object_cm = 1
        self.__ratio_pixel_cm = 1
        
        self.__x = self.__display_width / 2 + self.get_delta_hor() - self.__size/2
        self.__y = self.__display_height / 2 + self.get_delta_ver() - self.__size/2

        self.__csv_recorder = None
        self.__is_recording = False

    def set_ratio_pixel_cm(self):
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.get_size_object_cm()

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_size_object_cm(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def set_time_step(self, value):
        self.__time_step = value
        self.__timer.setInterval(self.__time_step)

    def get_delta_hor(self):
        return self.__delta_hor

    def set_delta_hor(self, value):
        self.__delta_hor = value

    def scale_delta_hor(self):
        self.__delta_hor = self.__delta_hor * self.__ratio_pixel_cm 

    def get_delta_ver(self):
        return self.__delta_ver

    def set_delta_ver(self, value):
        self.__delta_ver = value

    def scale_delta_ver(self):
        self.__delta_ver = self.__delta_ver * self.__ratio_pixel_cm

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value
        self.scale_size()

    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def get_color(self):
        return self.__color

    def set_color(self, value):
        self.__color = value

    def get_is_recording(self):
        return self.__is_recording

    def set_is_recording(self, value):
        self.__is_recording = value

    def get_is_running(self):
        return self.__is_running

    def set_is_running(self, value):
        self.__is_running = value

    def get_nb_cycle(self):
        return self.__nb_cycle

    def set_nb_cycle(self, value):
        self.__nb_cycle = value

    def paintEvent(self, event):
        if self.__is_running:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def __update(self):
        x_left_tmp = self.__display_width / 2 - self.get_delta_hor() - self.__size/2
        y_left_tmp = self.__display_height / 2 - self.get_delta_ver() - self.__size/2

        x_right_tmp = self.__display_width / 2 + self.get_delta_hor() - self.__size/2
        y_right_tmp = self.__display_height / 2 + self.get_delta_ver() - self.__size/2

        if self.__nb_cycle > self.__cpt_cycle: 
            if self.__is_object_on_left:
                self.__x = x_right_tmp
                self.__y = y_right_tmp
                self.__is_object_on_left = False
            else:
                self.__x = x_left_tmp
                self.__y = y_left_tmp
                self.__is_object_on_left = True

            self.__cpt_cycle = self.__cpt_cycle + 1
        else:
            self.__is_running = False
            pupilLabs_recorder = PupilLabs_recorder()
            pupilLabs_recorder.stop_record_pupilLab(self.__pupilLabs)
            self.__recording_label.clear()
            self.close()

        if self.get_is_recording():
            self.__csv_recorder.record(self.__current_time, self.__x, self.__y)
        
        self.__current_time = self.__current_time + self.__time_step

        self.update()