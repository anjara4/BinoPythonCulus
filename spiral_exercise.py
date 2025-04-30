from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen
from model.exercise import Exercise
import time
import numpy as np

class Spiral(Exercise):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right):
        super().__init__(selected_config, recording_label, pupil_labs, cam_left, cam_right)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step_GUI = 0.005
        self.__timer.start(self.__time_step_GUI)

        self.__speed_factor = 1000
        
        self.__step = 0

        self.__orientation = 1  # 1 for clockwise, -1 for counterclockwise

        self.__size_object_cm = 1

        self.__dist_between_loops = 50
        

        self.__x_init, self.__y_init = self.get_display_width() / 2 - self.get_size()/2, self.get_display_height() / 2 - self.get_size()/2
        self.__x = self.__x_init
        self.__y = self.__y_init
        self._t = np.linspace(0, 6 * np.pi, 1000)

        self.set_ratio_pixel_cm()

    def set_x(self, value):
        self.__x = value

    def get_x(self):
        return self.__x
    
    def get_x_init(self):
        return self.__x_init
    
    def set_y(self, value):
        self.__y = value

    def get_y(self):
        return self.__y
    
    def get_y_init(self):
        return self.__y_init
    
    def set_t(self):
        self.__t = np.linspace(0, self.get_nb_cycle() * 2 * np.pi, self.__speed_factor*self.get_nb_cycle())

    def set_orientation(self, value):
        self.__orientation = value

    def set_dist_between_loops(self, value):
        self.__dist_between_loops = value

    def get_dist_between_loops(self):
        return self.__dist_between_loops
    
    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())
    
    def get_turns_completed(self, current_time):
        # Calculate the number of turns completed based on the current time
        turns = (self.__orientation * current_time) / (2 * np.pi)
        return int(abs(turns))

    def set_speed_factor(self, value):
        self.__speed_factor = value

    def __update_position(self):
        current_time = time.perf_counter()
        #self.__current_time += self.__time_step_GUI

        self.__x = self.__x_init + self.__dist_between_loops * self.__t[self.__step] * np.cos(self.__orientation * self.__t[self.__step])
        self.__y = self.__y_init + self.__dist_between_loops * self.__t[self.__step] * np.sin(self.__orientation * self.__t[self.__step])

        if self.get_is_recording():
            if self.get_start_time() is None:
                self.set_start_time(current_time)
            elapsed_time = current_time - self.get_start_time()

            self.get_csv_recorder().record(
                round(elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )
        #print(self.get_turns_completed(), self.get_nb_cycle_exo())
        #if self.get_turns_completed(current_time)==self.get_nb_cycle_exo():
        if self.__step >= len(self.__t) - 1:
            self.stop_exo()
            self.__step = 0
        self.__step += 1

    def __update(self):
        self.__update_position()
        self.update()