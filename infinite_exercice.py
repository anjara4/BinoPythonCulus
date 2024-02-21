from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math
import pandas as pd
import csv

from screen_calibration import Screen_calibration
from recording import PupilLabs_recorder
from parameters import Parameters


class Infinite(QWidget):
    def __init__(self, pupilLabs, recording_label):
        super().__init__()
        self.setWindowTitle("Infinite")

        self.__pupilLabs = pupilLabs
        self.__recording_label = recording_label

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 5
        self.__timer.start(self.__time_step)
        self.__current_time = self.__time_step

        self.__is_running = False

        self.__speed = 0.01
        self.__size = 50
        self.__color = Qt.red
        self.__is_object_vertical = True

        self.__averageAngleSpeed = 0
        self.__currentAngle = 0
        self.__x = self.__display_width / 2 - self.__size/2
        self.__y = self.__display_height / 2 - self.__size/2
        self.__index = 0

        self.__csv_recorder = None
        self.__is_recording = False

        self.__selected_config = None

        self.__nb_cycle = 5
        self.__cpt_cycle = 0

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
        self.__x_scaling = (self.__ratio_pixel_cm * self.__width_target_infini_cm) / self.__original_width_px
        self.__y_scaling = (self.__ratio_pixel_cm * self.__height_target_infini_cm) / self.__original_height_px

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

    def set_time_step(self, value):
        self.__time_step = value
        self.timer.setInterval(self.__time_step)

    def get_screen_calibration_value(self):
        return self.__screen_calibration_value

    def set_screen_calibration_value(self, value):
        self.__screen_calibration_value = value

    def get_size(self):
        return self.__size

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
        self.__is_recording = value

    def get_width_target_infini_object_cm(self):
        return self.__width_target_infini_object_cm

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

    def get_color(self):
        return self.__color

    def set_color(self, value):
        self.__color = value

    def get_speed(self):
        return self.__speed

    def set_speed(self, value):
        self.__speed = value

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def get_is_object_vertical(self):
        return self.__is_object_vertical

    def set_is_object_vertical(self, value):
        self.__is_object_vertical = value

    def get_nb_cycle(self):
        return self.__nb_cycle

    def set_nb_cycle(self, value):
        self.__nb_cycle = value

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.__size, self.__size)
            #for x, y in self.ellipses:
            #    painter.drawEllipse(x, y, self.get_size(), self.get_size())

    def __update(self):
        if self.get_is_running():
            diviser = math.pow(2, self.__index / 2)
            self.__averageAngleSpeed = 2 * math.pi * self.get_speed() / (5.24412 * self.get_size())
            self.__averageAngleSpeed = self.__averageAngleSpeed * (5.24412 / (1.24412 / diviser + 4))#// prendre en compte approximativement le scale.

            delta = self.__time_step * self.__averageAngleSpeed
            self.__currentAngle = self.__currentAngle + delta

            sin = math.sin(self.__currentAngle)
            cos = math.cos(self.__currentAngle)
            tmp = self.get_size() * sin / (1 + cos * cos)

            if self.get_is_object_vertical():
                self.__x = cos * (tmp / diviser) * self.__x_scaling 
                self.__x = self.__x + self.__display_width / 2 - self.__size/2

                self.__y = tmp * self.__y_scaling 
                self.__y = self.__y + self.__display_height / 2 - self.__size/2

                #self.ellipses.append((self.__x, self.__y))

                if abs(sin) < 0.009:#The threshold 0.009 is selected based on the sin data recorded 
                    if 5 * self.__nb_cycle + 5 >= self.__cpt_cycle:
                        self.__cpt_cycle = self.__cpt_cycle + 1
                    else:
                        self.__is_running = False
                        pupilLabs_recorder = PupilLabs_recorder()
                        pupilLabs_recorder.stop_record_pupilLab(self.__pupilLabs)
                        self.__recording_label.clear()
                        self.close()

                if self.get_is_recording():
                    self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
            else:
                self.__x = tmp * self.__x_scaling 
                self.__x = self.__x + self.__display_width / 2 - self.__size/2

                self.__y = cos * (tmp / diviser) * self.__y_scaling
                self.__y = self.__y + self.__display_height / 2 - self.__size/2

                if self.get_is_recording():
                    self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
            
            self.__current_time = self.__current_time + self.__time_step

        self.update()
