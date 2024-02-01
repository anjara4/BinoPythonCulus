from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math
import pandas as pd


class Saccade(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saccade")

        self.__selected_config = None

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 1000
        self.__timer.start(self.__time_step)

        self.__delta_time = self.__time_step/1000
        self.__current_time = self.__delta_time

        self.__is_running = False

        self.__size = 50
        self.__color = Qt.red
        self.__delta_horizontal = 50
        self.__delta_vertical = 50
        self.__is_object_on_left = False
        self.__x = 0
        self.__y = 0

        self.__csv_recorder = None
        self.__is_recording = False

    def get_selected_config(self):
        return self.__selected_config

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_name_object(self):
        return self.__selected_config.get_name_config()

    def get_size_object(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        index_list = df.loc[df['SizeObject'] == self.get_name_object()].index.tolist()
        res = 1
        if index_list:
            res = index_list[0]
        return res

    def update_size_object(self):
        self.__size_object_cm = self.get_size_object()

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def set_time_step(self, value):
        self.__time_step = value
        self.__timer.setInterval(self.__time_step)

    def get_delta_horizontal(self):
        return self.__delta_horizontal

    def set_delta_horizontal(self, value):
        self.__delta_horizontal = value

    def get_delta_vertical(self):
        return self.__delta_horizontal

    def set_delta_vertical(self, value):
        self.__delta_vertical = value

    def get_delta_horizontal(self):
        return self.__delta_vertical

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value

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

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def __update(self):
        x_left_tmp = self.__display_width / 2 - self.get_delta_horizontal()
        y_left_tmp = self.__display_height / 2 - self.get_delta_vertical()

        x_right_tmp = self.__display_width / 2 + self.get_delta_horizontal()
        y_right_tmp = self.__display_height / 2 + self.get_delta_vertical()

        if self.__is_object_on_left:
            self.__x = x_right_tmp
            self.__y = y_right_tmp
            self.__is_object_on_left = False
        else:
            self.__x = x_left_tmp
            self.__y = y_left_tmp
            self.__is_object_on_left = True

        if self.get_is_recording():
            self.__csv_recorder.record(self.__current_time, self.__x, self.__y)
        
        self.__current_time = self.__current_time + self.__time_step

        self.update()

class Fixation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixation")

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__selected_config = None

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 10
        self.__timer.start(self.__time_step)

        self.__delta_time = 0
        self.__current_time = 0

        self.__is_running = False

        self.__size = 50
        self.__color = Qt.red

        self.__horizontal_position = 0
        self.__vertical_position = 0

        self.__x = 0
        self.__y = 0

        self.__csv_recorder = None
        self.__is_recording = False

    def get_selected_config(self):
        return self.__selected_config

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_name_object(self):
        return self.__selected_config.get_name_config()

    def get_size_object(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        index_list = df.loc[df['SizeObject'] == self.get_name_object()].index.tolist()
        res = 1
        if index_list:
            res = index_list[0]
        return res

    def update_size_object(self):
        self.__size_object_cm = self.get_size_object()

    def get_csv_recorder(self):
        return self.__csv_recorder

    def get_csv_recorder(self, value):
        self.__csv_recorder = value

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value

    def get_color(self):
        return self.__color

    def set_color(self, value):
        self.__color = value

    def get_horizontal_position(self):
        return self.__horizontal_position

    def set_horizontal_position(self, value):
        self.__horizontal_position = value

    def get_vertical_position(self):
        return self.__vertical_position

    def set_vertical_position(self, value):
        self.__vertical_position = value

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
        self.__x = self.__display_width / 2 - self.get_horizontal_position()
        self.__y = self.__display_height / 2 - self.get_vertical_position()

        if self.get_is_recording():
            self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
        
        self.__current_time = self.__current_time + self.__time_step

        self.update()

class Infinite(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infinite")

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 5
        self.__timer.start(self.__time_step)
        self.__current_time = self.__time_step

        self.__is_running = False

        self.__x_scaler = 1
        self.__y_scaler = 1
        self.__speed = 0.01
        self.__size = 50
        self.__color = Qt.red
        self.__is_object_vertical = True

        self.__averageAngleSpeed = 0
        self.__currentAngle = 0
        self.__x = 0 
        self.__y = 0 
        self.__index = 0

        self.__csv_recorder = None
        self.__is_recording = False

        self.__selected_config = None

        #These following parameters are used to scale the size of the infini object
        self.__original_width_px = 35 #pixel value of the infini object without scalling
        self.__original_height_px = 100 #pixel value of the infini object  without scalling

        self.__width_target_infini_object_cm = 10
        self.__heigth_target_infini_object_cm = 20

        self.__size_screen_calibration_object_px = 500 #This is the size of the object dranw during the screen calibration
        self.__size_object_cm = 10 #9.4cm is the value of the 500 pix drawn on the screen
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.__size_object_cm

        self.__x_scaling = (self.__ratio_pixel_cm * self.__width_target_infini_object_cm) / self.__original_width_px
        self.__y_scaling = (self.__ratio_pixel_cm * self.__heigth_target_infini_object_cm) / self.__original_height_px

        #self.ellipses = []

    def get_selected_config(self):
        return self.__selected_config

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_name_object(self):
        return self.__selected_config.get_name_config()

    def get_size_object(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        index_list = df.loc[df['SizeObject'] == self.get_name_object()].index.tolist()
        res = 1
        if index_list:
            res = index_list[0]
        return res

    def update_size_object(self):
        self.__size_object_cm = self.get_size_object()

    def update_x_scaling(self):
        self.__x_scaling = (self.__ratio_pixel_cm * self.__width_target_infini_object_cm) / self.__original_width_px

    def update_y_scaling(self):
        self.__y_scaling = (self.__ratio_pixel_cm * self.__heigth_target_infini_object_cm) / self.__original_height_px

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

    def set_width_target_infini_object_cm(self, value):
        self.__width_target_infini_object_cm = value

    def get_height_target_infini_object_cm(self):
        return self.__height_target_infini_object_cm

    def set_height_target_infini_object_cm(self, value):
        self.__height_target_infini_object_cm = value

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

    def cm2pix(self, distance_cm, size_object_px):
        return distance_cm * size_object_px 

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())
            #for x, y in self.ellipses:
            #    painter.drawEllipse(x, y, self.get_size(), self.get_size())

    def __update(self):
        diviser = math.pow(2, self.__index / 2)
        self.__averageAngleSpeed = 2 * math.pi * self.get_speed() / (5.24412 * self.get_size())
        self.__averageAngleSpeed = self.__averageAngleSpeed * (5.24412 / (1.24412 / diviser + 4))#// prendre en compte approximativement le scale.

        delta = self.__time_step * self.__averageAngleSpeed
        self.__currentAngle = self.__currentAngle + delta

        sin = math.sin(self.__currentAngle)
        cos = math.cos(self.__currentAngle)
        tmp = self.get_size() * sin / (1 + cos * cos)

        if self.get_is_object_vertical():
            self.__x = cos * (tmp / diviser) * self.__x_scaling #* self.scale_x #self.get_x_scaler()  
            self.__x = self.__x + self.__display_width / 2

            self.__y = tmp * self.__y_scaling #* self.get_y_scaler()
            self.__y = self.__y + self.__display_height / 2

            #self.ellipses.append((self.__x, self.__y))

            if self.get_is_recording():
                self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
        else:
            self.__x = tmp * self.scale_x #self.get_x_scaler()
            self.__x = self.__x + self.__display_width / 2

            self.__y = cos * (tmp / diviser) * self.get_y_scaler()
            self.__y = self.__y + self.__display_height / 2

            if self.get_is_recording():
                self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
        
        self.__current_time = self.__current_time + self.__time_step

        self.update()
