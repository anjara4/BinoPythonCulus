from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen

import math
import pandas as pd
import time
from model.exercise import Exercise


class Infinite(Exercise):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right):
        super().__init__(selected_config, recording_label, pupil_labs, cam_left, cam_right)
        self.setWindowTitle("Infinite")

        self.timer_GUI = QTimer()
        self.timer_GUI.timeout.connect(self.__update)
        self.time_step_GUI = 0.12

        self.__current_time = 0

        self.__speed = 0.06
        self.set_size(30)
        self.__fixed_size = 55
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

        self.__x = self.get_display_width() / 2 - self.get_size()/2
        self.__y = self.get_display_height() / 2 - self.get_size()/2

        #These following parameters are used to scale the size of the infini object

        self.__original_width_px = 35 #pixel value of the infini object without scalling
        self.__original_height_px = 100 #pixel value of the infini object  without scalling

        self.__width_target_infini_cm = 10
        self.__height_target_infini_cm = 20

        self.__size_object_cm_from_config = 1
        self.set_ratio_pixel_cm()

        #1cm    -> 53px (from the ratio)
        #0.67cm -> 35px (original height of the infini) (0.67 = original_height_px / ratio)
        #0.67cm * β = target_height_cm (β is the scalling) 
        # β = (target_height_cm * ration) / original_height_px 
        self.__x_scaling_vertical = float(self._parameters.x_scaling_infini_vertical)
        self.__y_scaling_vertical = float(self._parameters.y_scaling_infini_vertical)

        self.__x_scaling_horizontal = float(self._parameters.x_scaling_infini_horizontal)
        self.__y_scaling_horizontal = float(self._parameters.y_scaling_infini_horizontal)

        #self.ellipses = []

        self.measures=[]

    def update_original_width_height_px(self):
        if self.__is_object_vertical:
            self.__original_width_px = 35
            self.__original_height_px = 100
        else:
            self.__original_width_px = 100
            self.__original_height_px = 35

    def set_size_object_cm_from_config(self):
        self.__size_object_cm_from_config = self.get_size_object_cm()

    def scale_x(self):
        self.__x_scaling = (self.get_ratio_pixel_cm() * self.__width_target_infini_cm) / self.__original_width_px

    def scale_y(self):
        self.__y_scaling = (self.get_ratio_pixel_cm() * self.__height_target_infini_cm) / self.__original_height_px

    def get_screen_calibration_value(self):
        return self.__screen_calibration_value

    def set_screen_calibration_value(self, value):
        self.__screen_calibration_value = value

    def set_width_target_infini_cm(self, value):
        self.__width_target_infini_cm = value

    def get_height_target_infini_cm(self):
        return self.__height_target_infini_cm

    def set_height_target_infini_cm(self, value):
        self.__height_target_infini_cm = value

    def get_y_scaler(self):
        return self.__y_scaler

    def set_y_scaler(self, value):
        self.__y_scaler = value

    def set_time_step(self, value):
        self.time_step_GUI = value * 0.1
        self.timer_GUI.start(self.time_step_GUI)

    def get_is_object_vertical(self):
        return self.__is_object_vertical

    def set_is_object_vertical(self, value):
        self.__is_object_vertical = value

    def set_nb_cycle_exo(self, value):
        self.__nb_cycle = value

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def __update_position(self):
        current_time = time.perf_counter() #for data saving
        
        self.__averageAngleSpeed = self.__two_pi * self.__speed / self.__coef_speed
        self.__averageAngleSpeed = self.__averageAngleSpeed * self.__coef_averageAngleSpeed

        delta = self.time_step_GUI * self.__averageAngleSpeed
        self.__currentAngle = self.__currentAngle + delta 

        correction_angle = delta * (0.28 * abs(math.cos(self.__currentAngle)) - 0.17);
        self.__currentAngle = self.__currentAngle + correction_angle

        if self.__currentAngle > self.__two_pi: 
            self.__currentAngle = 0

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
            self.__x = self.__x + self.get_display_width() / 2 

            self.__y = tmp 
            self.__y = self.__y * self.__y_scaling_vertical
            self.__y = self.__y + self.get_display_height() / 2 
        else:
            self.__x = tmp  
            self.__x = self.__x * self.__x_scaling_horizontal
            self.__x = self.__x + self.get_display_width() / 2 

            self.__y = cos * tmp 
            self.__y = self.__y * self.__y_scaling_horizontal 
            self.__y = self.__y + self.get_display_height() / 2 

        if self.get_is_recording():
            if self.get_start_time() is None:
                self.set_start_time(current_time)
            elapsed_time = current_time - self.get_start_time()

            self.get_csv_recorder().record(
                round(elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )

    def __update(self):
        self.__update_position()

        self.update()
    