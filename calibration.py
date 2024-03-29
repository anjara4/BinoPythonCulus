from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.Qt import Qt
import math
from parameters import Parameters

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Calibration(QWidget):
    closed = pyqtSignal()

    def __init__(self, size):
        super().__init__()
        self.setWindowTitle("Calibration")

        screen = QDesktopWidget().availableGeometry(1)#QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height()  

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step = 0.01
        self.__timer.start(self.__time_step)

        self.__i = 0

        self.__size = size
        self.__space_key_pressed = False
        
        self.__position = [
            Point(self.__display_width/2 - self.__size/2, self.__display_height/2 - self.__size/2),  # Center
            Point(self.__display_width - self.__size, 0),  # Top-right corner
            Point(self.__display_width - self.__size, self.__display_height - self.__size),  # Bottom-right corner
            Point(0, self.__display_height - self.__size),  # Bottom-left corner
            Point(0, 0)  # Top-left corner
]

    def paintEvent(self, event):
        if self.__i < len(self.__position):
            painter = QPainter(self)
            parameters = Parameters()
            pixmap = QPixmap(parameters.image_calibration) 
            painter.drawPixmap(self.__position[self.__i].x, self.__position[self.__i].y, self.__size, self.__size, pixmap)

    def __update(self):
        if self.__space_key_pressed == True and self.__i < len(self.__position):
            self.__i = self.__i + 1
            self.__space_key_pressed = False
        elif self.__i >= len(self.__position):
            self.close()
        self.update()

    def closeEvent(self, event):
        self.closed.emit()  # Emit the 'closed' signal
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.__space_key_pressed = True

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value


