from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.Qt import Qt
import math
from parameters import Parameters
from threading import Thread
import time
from csv_recorder import CSV_recorder

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Calibration(QWidget):
    closed = pyqtSignal()

    def __init__(self, size, connected_patient, folder_recording_name, file_recording_name):
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
        self.__calibration_on = True

        self.folder_recording_name = folder_recording_name
        self.file_recording_name = file_recording_name

        self.csv_recorder = CSV_recorder()
        self.csv_recorder.set_filename(self.folder_recording_name + "/" + self.file_recording_name + "position_calibration.csv")
        self.csv_recorder.set_header()

        self.__csv_recorder = None
        current_time = time.perf_counter()
        self.__start_time = current_time
        
        self.__position = [
            Point(self.__display_width/2 - self.__size/2, self.__display_height/2 - self.__size/2),  # Center
            Point(0, 0),  # Top-left corner
            Point(self.__display_width - self.__size, 0),  # Top-right corner
            Point(self.__display_width - self.__size, self.__display_height - self.__size),  # Bottom-right corner
            Point(0, self.__display_height - self.__size)  # Bottom-left corner
        ]


    def paintEvent(self, event):
        if self.__i < len(self.__position):
            painter = QPainter(self)
            parameters = Parameters()
            pixmap = QPixmap(parameters.image_calibration) 
            painter.drawPixmap(
                self.__position[self.__i].x, 
                self.__position[self.__i].y, 
                self.__size, 
                self.__size, pixmap)

    def __update(self):
        if self.__space_key_pressed == True and self.__i < len(self.__position):
            current_time = time.perf_counter()
            elapsed_time = current_time - self.__start_time
            self.csv_recorder.record(
                round(elapsed_time, 2),
                round(self.__position[self.__i].x, 2),
                round(self.__position[self.__i].y, 2)
                )

            self.__i = self.__i + 1
            self.__space_key_pressed = False
        elif self.__i >= len(self.__position):
            self.__calibration_on = False
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

