from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Calibration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration")

        screen = QDesktopWidget().screenGeometry(1)
        self.__size = 50
        self.__display_width = screen.width() - 2 * self.__size
        self.__display_height = screen.height() - 2 * self.__size

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 5000
        self.__timer.start(self.__time_step)

        self.__is_running = False

        self.__i = 0

        self.__position = [
                        Point(self.__display_width/2, self.__display_height/2), 
                        Point(0, 0), 
                        Point(self.__display_width, 0),
                        Point(self.__display_width, self.__display_height),
                        Point(0, self.__display_height)
                        ]

    def paintEvent(self, event):
        if self.get_is_running() and self.__i < len(self.__position):
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            painter.drawEllipse(self.__position[self.__i].x, self.__position[self.__i].y, self.__size, self.__size)

    def __update(self):
        if self.get_is_running():
            if self.__i < len(self.__position):
                self.update()
                self.__i = self.__i + 1
            else:
                self.set_is_running(False)
                self.close()

    def get_is_running(self):
        return self.__is_running

    def set_is_running(self, value):
        self.__is_running = value

