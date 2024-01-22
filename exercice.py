from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math

class Infinite(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infinite Move")

        screen = QDesktopWidget().screenGeometry(1)
        self.display_width = screen.width() 
        self.display_height = screen.height() 

        self.timer = QTimer()
        self.timer.timeout.connect(self.__update_object)
        self.__time_step = 5
        self.timer.start(self.__time_step)

        self.x_scaler_position = 10
        self.y_scaler_position = 10
        self.object_speed = 0.01
        self.object_size = 50
        self.object_color = Qt.red
        self.object_is_vertical = True

        self.__averageAngleSpeed = 0
        self.__currentAngle = 0
        self.__x_position_object = 0 
        self.__y_position_object = 0 
        self.__index = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(self.object_color, Qt.SolidPattern))
        painter.drawEllipse(self.__x_position_object, self.__y_position_object, self.object_size, self.object_size)

    def get_position_object(self):
        return (self.__x_position_object, self.__y_position_object)

    def __update_object(self):
        diviser = math.pow(2, self.__index / 2)
        self.__averageAngleSpeed = 2 * math.pi * self.object_speed / (5.24412 * self.object_size)
        self.__averageAngleSpeed = self.__averageAngleSpeed * (5.24412 / (1.24412 / diviser + 4))#// prendre en compte approximativement le scale.

        delta = self.__time_step * self.__averageAngleSpeed;
        self.__currentAngle = self.__currentAngle + delta;

        sin = math.sin(self.__currentAngle);
        cos = math.cos(self.__currentAngle);
        tmp = self.object_size * sin / (1 + cos * cos);

        if self.object_is_vertical:
            self.__x_position_object = cos * (tmp / diviser) * self.x_scaler_position
            self.__x_position_object = self.__x_position_object + self.display_width / 2

            self.__y_position_object = tmp * self.y_scaler_position
            self.__y_position_object = self.__y_position_object + self.display_height / 2
        else:
            self.__x_position_object = tmp * self.x_scaler_position
            self.__x_position_object = self.__x_position_object + self.display_width / 2

            self.__y_position_object = cos * (tmp / diviser) * self.y_scaler_position
            self.__y_position_object = self.__y_position_object + self.display_height / 2
        
        self.update()

