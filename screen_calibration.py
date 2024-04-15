from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer
import math

from parameters import Parameters

class Screen_calibration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Calibration")

        self.timer = QTimer()
        # Set the timer to trigger after 60000 milliseconds (1 minute)
        self.timer.setInterval(60000)
        # Connect the timer's timeout signal to the close function
        self.timer.timeout.connect(self.close)
        # Start the timer
        self.timer.start()

        screen = QDesktopWidget().availableGeometry(1)#QDesktopWidget().screenGeometry(1)
        self.__display_width = screen.width() 
        self.__display_height = screen.height()  

        parameters = Parameters()
        self.__size = int(parameters.size_object_screen_calibration)

    def get_size_object_px(self):
        return self.__size

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(self.__display_width/2 - self.__size/2, 
                    self.__display_height/2 - self.__size/2, 
                    self.__size, self.__size)

