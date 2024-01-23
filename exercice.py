from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math

class Saccade(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saccade Move")

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
        self.setWindowTitle("Infinite Move")

        screen = QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 5
        self.__timer.start(self.__time_step)
        self.__current_time = self.__time_step

        self.__is_running = False

        self.__x_scaler = 10
        self.__y_scaler = 10
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

    def set_time_step(self, value):
        self.__time_step = value
        self.timer.setInterval(self.__time_step)

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

    def get_x_scaler(self):
        return self.__x_scaler

    def set_x_scaler(self, value):
        self.__x_scaler = value

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

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

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
            self.__x = cos * (tmp / diviser) * self.get_x_scaler()
            self.__x = self.__x + self.__display_width / 2

            self.__y = tmp * self.get_y_scaler()
            self.__y = self.__y + self.__display_height / 2

            if self.get_is_recording():
                self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
        else:
            self.__x = tmp * self.get_x_scaler()
            self.__x = self.__x + self.__display_width / 2

            self.__y = cos * (tmp / diviser) * self.get_y_scaler()
            self.__y = self.__y + self.__display_height / 2

            if self.get_is_recording():
                self.get_csv_recorder().record(self.__current_time, self.__x, self.__y)
        
        self.__current_time = self.__current_time + self.__time_step

        self.update()
