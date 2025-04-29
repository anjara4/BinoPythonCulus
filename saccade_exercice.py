from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer

import time

from model.exercise import Exercise

class Saccade(Exercise):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right, scenario): 
        super().__init__(selected_config, recording_label, pupil_labs, cam_left, cam_right)
        self.setWindowTitle("Saccade")

        self.__scenario = scenario
        self.scenario_path = self._parameters.scenario_path
        for i in [1,2,3,4]:
            if self.__scenario == i:
                self.scenar = self.read_scenario(self.scenario_path.replace('*',str(i)))

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step_GUI = 1000

        self.__duration_exo = 1000

        self.__nb_cycle = -1
        self.__cpt_cycle = 0

        self.__delta_hor = 50
        self.__delta_ver = 50

        self.__size_object_cm = 1
        
        self.__x_left_tmp = 0
        self.__y_left_tmp = 0

        self.__x_right_tmp = 0
        self.__y_right_tmp = 0
        
        self.__x = 0
        self.__y = 0

    def set_time_step_GUI(self, value):
        self.__time_step_GUI = value
        self.__timer.start(self.__time_step_GUI)

    def init_x_left_pos(self):
        self.__x_left_tmp = self.get_display_width() / 2 - self.get_delta_hor() - self.get_size()/2

    def init_y_left_pos(self):
        self.__y_left_tmp = self.get_display_height() / 2 - self.get_delta_ver() - self.get_size()/2

    def init_x_right_pos(self):
        self.__x_right_tmp = self.get_display_width() / 2 + self.get_delta_hor() - self.get_size()/2

    def init_y_right_pos(self):
        self.__y_right_tmp = self.get_display_height() / 2 + self.get_delta_ver() - self.get_size()/2

    def set_x(self):
        self.__x = self.__x_left_tmp

    def set_y(self):
        self.__y = self.__y_left_tmp

    def set_saccade_time(self, value):
        self.__saccade_time = value

    def get_delta_hor(self):
        return self.__delta_hor

    def set_delta_hor(self, value):
        self.__delta_hor = value

    def scale_delta_hor(self):
        self.__delta_hor = self.__delta_hor * self.get_ratio_pixel_cm() 

    def get_delta_ver(self):
        return self.__delta_ver

    def set_delta_ver(self, value):
        self.__delta_ver = value

    def scale_delta_ver(self):
        self.__delta_ver = self.__delta_ver * self.get_ratio_pixel_cm()

    def set_nb_cycle(self, value):
        self.__nb_cycle = value

    def set_duration_exo(self, value):
        self.__duration_exo = value

    def read_scenario(self, path):
        list = []
        with open(path) as f:
            for line in f:
                list.append(int(line))
            return list
    
    def translate_scenario_indexes_to_pixel_position(self, scenario):
        translated_scenario = []
        degree_of_amplitude = 5
        scaled_amplitude = degree_of_amplitude * self.get_ratio_pixel_cm() 
        for pos in scenario:
            if pos == 0 :
                translated_scenario.append((self.get_display_width() / 2 - self.get_size()/2, self.get_display_height() / 2 - self.get_size()/2))
            elif pos == 1:
                translated_scenario.append((self.get_display_width() / 2 + scaled_amplitude - self.get_size()/2 , self.get_display_height() / 2 - self.get_size()/2 ))
            elif pos == 2:
                translated_scenario.append((self.get_display_width() / 2 + scaled_amplitude - self.get_size()/2, self.get_display_height() / 2 + scaled_amplitude - self.get_size()/2))
            elif pos == 3:
                translated_scenario.append((self.get_display_width() / 2 - self.get_size()/2 , self.get_display_height() / 2 + scaled_amplitude - self.get_size()/2))
            elif pos == 4:
                translated_scenario.append((self.get_display_width() / 2 - scaled_amplitude - self.get_size()/2, self.get_display_height() / 2 + scaled_amplitude - self.get_size()/2))
            elif pos == 5:
                translated_scenario.append((self.get_display_width() / 2 - scaled_amplitude - self.get_size()/2 , self.get_display_height() / 2 - self.get_size()/2 ))
            elif pos == 6:
                translated_scenario.append((self.get_display_width() / 2 - scaled_amplitude - self.get_size()/2, self.get_display_height() / 2 - scaled_amplitude - self.get_size()/2))
            elif pos == 7:
                translated_scenario.append((self.get_display_width() / 2  - self.get_size()/2 , self.get_display_height() / 2 - scaled_amplitude - self.get_size()/2))
            elif pos == 8:
                translated_scenario.append((self.get_display_width() / 2 + scaled_amplitude - self.get_size()/2, self.get_display_height() / 2 - scaled_amplitude - self.get_size()/2))

        return translated_scenario
        
    def __update_position(self):
        current_time = time.perf_counter()
        if self.get_start_time() is None:
            self.set_start_time(current_time)
        elapsed_time = current_time - self.get_start_time()

        
        if self.__scenario == 0:
            if self.__x == self.__x_left_tmp and self.__y == self.__y_left_tmp:
                self.__x = self.__x_right_tmp
                self.__y = self.__y_right_tmp
            else:
                self.__x = self.__x_left_tmp
                self.__y = self.__y_left_tmp
            
        else :
            if self.__cpt_cycle < len(self.scenar):
                print(round(elapsed_time),self.__cpt_cycle)

                translated_scenario = self.translate_scenario_indexes_to_pixel_position(self.scenar)
                self.__x = translated_scenario [self.__cpt_cycle][0]
                self.__y = translated_scenario [self.__cpt_cycle][1]  
        
            
        if self.get_is_recording():
            self.get_csv_recorder().record(
                round(elapsed_time, 2),
                round(self.__x, 2),
                round(self.__y, 2)
            )
        if self.elapsed_time >= self.__duration_exo and self.__scenario == 0:
            self.stop_exo()
        if self.__scenario != 0:
            if self.__cpt_cycle >= len(self.scenar) :
                self.stop_exo()
        
        self.__cpt_cycle = self.__cpt_cycle + 1

    def __update(self):
        self.__update_position()
        """if self.__nb_cycle < self.__cpt_cycle: 
            self.stop_exo()"""

        self.update()

    def paintEvent(self, event):
        if self.get_is_running():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())