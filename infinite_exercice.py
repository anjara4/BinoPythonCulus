from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QPointF
import pyautogui
import math
import pandas as pd
import csv
from PyQt5.QtGui import QColor

import time
from datetime import datetime

from screen_calibration import Screen_calibration
from parameters import Parameters


class Infinite(QWidget):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right):
        super().__init__()
        self.setWindowTitle("Infinite")

        self.__selected_config = selected_config
        self.__recording_label = recording_label
        self.__pupil_labs = pupil_labs
        self.__cam_left = cam_left
        self.__cam_right = cam_right 

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height()  

        self.timer_GUI = QTimer()
        self.timer_GUI.timeout.connect(self.__update)
        self.time_step_GUI = 0.12

        self.__current_time = 0

        self.__is_running = False

        self.__speed = 0.06
        self.__size = 30
        self.__fixed_size = 55
        self.__color = Qt.red
        self.__is_object_vertical = True

        self.__averageAngleSpeed = 0
        self.__currentAngle = 0
        self.__nb_cycle = 1000
        self.__current_cycle = 1
        self.__diviser = 1 

        self.__two_pi = 2 * math.pi
        self.__index = 0
        self.__coef_speed = 5.24412 * self.__fixed_size / 2
        self.__coef_averageAngleSpeed = 5.24412 / (1.24412 / self.__diviser + 4)

        self.__x = self.__display_width / 2 - self.__size/2
        self.__y = self.__display_height / 2 - self.__size/2

        self.__csv_recorder = None
        self.__is_recording = False
        self.__start_time = None

        #These following parameters are used to scale the size of the infini object

        self.__original_width_px = 35 #pixel value of the infini object without scalling
        self.__original_height_px = 100 #pixel value of the infini object  without scalling

        self.__width_target_infini_cm = 10
        self.__height_target_infini_cm = 20

        screenCalibration = Screen_calibration()
        self.__size_object_cm_from_config = 1
        self.__size_screen_calibration_object_px = screenCalibration.get_size_object_px() #This is the size of the object dranw during the screen calibration
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.__size_object_cm_from_config

        #1cm    -> 53px (from the ratio)
        #0.67cm -> 35px (original height of the infini) (0.67 = original_height_px / ratio)
        #0.67cm * β = target_height_cm (β is the scalling) 
        # β = (target_height_cm * ration) / original_height_px 
        parameters = Parameters()
        self.__x_scaling_vertical = float(parameters.x_scaling_infini_vertical)
        self.__y_scaling_vertical = float(parameters.y_scaling_infini_vertical)

        self.__x_scaling_horizontal = float(parameters.x_scaling_infini_horizontal)
        self.__y_scaling_horizontal = float(parameters.y_scaling_infini_horizontal)

        #self.ellipses = []

    def update_original_width_height_px(self):
        if self.__is_object_vertical:
            self.__original_width_px = 35
            self.__original_height_px = 100
        else:
            self.__original_width_px = 100
            self.__original_height_px = 35

    def set_selected_config(self, value):
        self.__selected_config = value

    def set_size_object_cm_from_config(self):
        self.__size_object_cm_from_config = self.get_size_object_cm_from_config()

    def get_size_object_cm_from_config(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()

    def get_name_object(self):
        return self.__selected_config.get_name_config()

    def set_ratio_pixel_cm(self):
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.__size_object_cm_from_config

    def scale_x(self):
        self.__x_scaling = (self.__ratio_pixel_cm * self.__width_target_infini_cm) / self.__original_width_px

    def scale_y(self):
        self.__y_scaling = (self.__ratio_pixel_cm * self.__height_target_infini_cm) / self.__original_height_px

    def get_screen_calibration_value(self):
        return self.__screen_calibration_value

    def set_screen_calibration_value(self, value):
        self.__screen_calibration_value = value

    def set_size(self, value):
        self.__size = value

    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def get_is_running(self):
        return self.__is_running

    def set_is_running(self, value):
        self.__is_running = value

    def get_is_recording(self):
        return self.__is_recording

    def set_is_recording(self, value):
        self.__start_time = None
        self.__is_recording = value

    def get_width_target_infini_object_cm(self):
        return self.__width_target_infini_object_cm

    def set_width_target_infini_cm(self, value):
        self.__width_target_infini_cm = value

    def get_height_target_infini_cm(self):
        return self.__height_target_infini_cm

    def get_depth_from_config(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['Depth'].values.item()

    def degrees_to_cm(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        return self.get_depth_from_config() * math.tan(angle_radians) 

    def set_height_target_infini_cm(self, value):
        self.__height_target_infini_cm = value

    def get_y_scaler(self):
        return self.__y_scaler

    def set_y_scaler(self, value):
        self.__y_scaler = value

    def set_color(self, value):
        self.__color = value

    def set_time_step(self, value):
        self.time_step_GUI = value * 0.1
        self.timer_GUI.start(self.time_step_GUI)

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def get_is_object_vertical(self):
        return self.__is_object_vertical

    def set_is_object_vertical(self, value):
        self.__is_object_vertical = value

    def set_nb_cycle_exo(self, value):
        self.__nb_cycle = value

    def paintEvent(self, event):
        if self.__is_running:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.__color, Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.__size, self.__size)

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

    def __update_position(self):
        current_time = time.perf_counter() #for data saving
        
        self.__averageAngleSpeed = self.__two_pi * self.__speed / self.__coef_speed
        self.__averageAngleSpeed = self.__averageAngleSpeed * self.__coef_averageAngleSpeed

        delta = self.time_step_GUI * self.__averageAngleSpeed
        self.__currentAngle = self.__currentAngle + delta 

        correction_angle = delta * (0.28 * abs(math.cos(self.__currentAngle)) - 0.17);
        self.__currentAngle = self.__currentAngle + correction_angle

        if self.__currentAngle > self.__two_pi: 
            self.__currentAngle = 0;

            if self.__current_cycle < self.__nb_cycle:
                self.__current_cycle = self.__current_cycle + 1
            else:
                self.stop_exo()

        sin = math.sin(self.__currentAngle) 
        cos = math.cos(self.__currentAngle) 
        #tmp = self.__size * sin / (1 + cos * cos)
        tmp = self.__fixed_size * sin / (1 + cos * cos) #self.__fixed_size is a define size

        if self.get_is_object_vertical():
            self.__x = cos * tmp 
            self.__x = self.__x * self.__x_scaling_vertical
            self.__x = self.__x + self.__display_width / 2 

            self.__y = tmp 
            self.__y = self.__y * self.__y_scaling_vertical
            self.__y = self.__y + self.__display_height / 2 
        else:
            self.__x = tmp  
            self.__x = self.__x * self.__x_scaling_horizontal
            self.__x = self.__x + self.__display_width / 2 

            self.__y = cos * tmp 
            self.__y = self.__y * self.__y_scaling_horizontal 
            self.__y = self.__y + self.__display_height / 2 

        if self.__is_recording:
            if self.__start_time is None:
                self.__start_time = current_time
            elapsed_time = current_time - self.__start_time

            self.get_csv_recorder().record(
                round(elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )

    def __update(self):
        self.__update_position()

        self.update()
        

