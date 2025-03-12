from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import math
import pandas as pd

import time

from parameters import Parameters
from screen_calibration import Screen_calibration
from pupil_labs import Pupil_labs

class Saccade(QWidget):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right, scenario): 
        super().__init__()
        self.setWindowTitle("Saccade")

        self.__selected_config = selected_config
        self.__recording_label = recording_label 
        self.__pupil_labs = pupil_labs
        self.__cam_left = cam_left
        self.__cam_right = cam_right 
        self.__scenario = scenario

        parameters = Parameters()
        self.scenario_path = parameters.scenario_path
        for i in [1,2,3,4]:
            if self.__scenario == i:
                self.scenar = self.read_scenario(self.scenario_path.replace('*',str(i)))
      
        screen_count = QDesktopWidget().screenCount()
        if screen_count > 1:
            screen = QDesktopWidget().screenGeometry(1)
        else :
            screen = QDesktopWidget().screenGeometry(0)        
        self.__display_width = screen.width() 
        self.__display_height = screen.height() 

        screenCalibration = Screen_calibration()
        self.__size_screen_calibration_object_px = screenCalibration.get_size_object_px()

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__time_step_GUI = 1000

        self.__is_running = False

        self.__duration_exo = 1000

        self.__nb_cycle = -1
        self.__cpt_cycle = 0

        self.__size = 50
        self.__color = Qt.red
        self.__delta_hor = 50
        self.__delta_ver = 50

        self.__size_object_cm = 1
        self.__ratio_pixel_cm = 1

        self.__x_left_tmp = 0
        self.__y_left_tmp = 0

        self.__x_right_tmp = 0
        self.__y_right_tmp = 0
        
        self.__x = 0
        self.__y = 0

        self.__csv_recorder = None
        self.__is_recording = False
        self.__start_time = None
        self.elapsed_time = 0

    def set_time_step_GUI(self, value):
        self.__time_step_GUI = value
        self.__timer.start(self.__time_step_GUI)

    def init_x_left_pos(self):
        self.__x_left_tmp = self.__display_width / 2 - self.get_delta_hor() - self.__size/2

    def init_y_left_pos(self):
        self.__y_left_tmp = self.__display_height / 2 - self.get_delta_ver() - self.__size/2

    def init_x_right_pos(self):
        self.__x_right_tmp = self.__display_width / 2 + self.get_delta_hor() - self.__size/2

    def init_y_right_pos(self):
        self.__y_right_tmp = self.__display_height / 2 + self.get_delta_ver() - self.__size/2

    def set_x(self):
        self.__x = self.__x_left_tmp

    def set_y(self):
        self.__y = self.__y_left_tmp

    def set_ratio_pixel_cm(self):
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.get_size_object_cm()

    def set_selected_config(self, value):
        self.__selected_config = value

    def get_size_object_cm(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()
        
    def get_depth_from_config(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['Depth'].values.item()

    def degrees_to_cm(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        return self.get_depth_from_config() * math.tan(angle_radians)

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def set_saccade_time(self, value):
        self.__saccade_time = value

    def get_delta_hor(self):
        return self.__delta_hor

    def set_delta_hor(self, value):
        self.__delta_hor = value

    def scale_delta_hor(self):
        self.__delta_hor = self.__delta_hor * self.__ratio_pixel_cm 

    def get_delta_ver(self):
        return self.__delta_ver

    def set_delta_ver(self, value):
        self.__delta_ver = value

    def scale_delta_ver(self):
        self.__delta_ver = self.__delta_ver * self.__ratio_pixel_cm

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size = value

    def get_is_recording(self):
        return self.__is_recording

    def set_is_recording(self, value):
        self.__start_time = None
        self.__is_recording = value

    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def get_color(self):
        return self.__color

    def set_color(self, value):
        self.__color = value

    def set_is_running(self, value):
        self.__is_running = value

    def set_nb_cycle(self, value):
        self.__nb_cycle = value

    def set_duration_exo(self, value):
        self.__duration_exo = value

    def paintEvent(self, event):
        if self.__is_running:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.get_color(), Qt.SolidPattern))
            painter.drawEllipse(self.__x, self.__y, self.get_size(), self.get_size())

    def stop_exo(self):
        self.__is_running = False
        self.__is_recording = False

        if self.__cam_left is not None:
            self.__cam_left.stop_recording()
        if self.__cam_right is not None:
            self.__cam_right.stop_recording()

        if self.__pupil_labs.get_status() is not None:
            self.__pupil_labs.stop_record()
        self.__recording_label.clear()
        self.close()

    def read_scenario(self, path):
        list = []
        with open(path) as f:
            for line in f:
                list.append(int(line))
            return list
    
    def translate_scenario_indexes_to_pixel_position(self, scenario):
        translated_scenario = []
        degree_of_amplitude = 5
        scaled_amplitude = degree_of_amplitude * self.__ratio_pixel_cm 
        for pos in scenario:
            if pos == 0 :
                translated_scenario.append((self.__display_width / 2 - self.__size/2, self.__display_height / 2 - self.__size/2))
            elif pos == 1:
                translated_scenario.append((self.__display_width / 2 + scaled_amplitude - self.__size/2 , self.__display_height / 2 - self.__size/2 ))
            elif pos == 2:
                translated_scenario.append(((self.__display_width / 2 - self.__size/2) + scaled_amplitude *math.cos(math.degrees(45)), (self.__display_height / 2 - self.__size/2) + scaled_amplitude *math.sin(math.degrees(45))))
            elif pos == 3:
                translated_scenario.append((self.__display_width / 2 - self.__size/2 , self.__display_height / 2 + scaled_amplitude - self.__size/2))
            elif pos == 4:
                translated_scenario.append(((self.__display_width / 2 - self.__size/2) - scaled_amplitude*math.cos(math.degrees(45)) , (self.__display_height / 2 - self.__size/2) + scaled_amplitude *math.sin(math.degrees(45))))
            elif pos == 5:
                translated_scenario.append((self.__display_width / 2 - scaled_amplitude - self.__size/2 , self.__display_height / 2 - self.__size/2 ))
            elif pos == 6:
                translated_scenario.append(((self.__display_width / 2 - self.__size/2) - scaled_amplitude *math.cos(math.degrees(45)), (self.__display_height / 2 - self.__size/2)- scaled_amplitude *math.sin(math.degrees(45))))
            elif pos == 7:
                translated_scenario.append((self.__display_width / 2  - self.__size/2 , self.__display_height / 2 - scaled_amplitude - self.__size/2))
            elif pos == 8:
                translated_scenario.append(((self.__display_width / 2 - self.__size/2) + scaled_amplitude *math.cos(math.degrees(45)), (self.__display_height / 2 - self.__size/2) - scaled_amplitude*math.sin(math.degrees(45))))

        return translated_scenario
        
    def __update_position(self):
        current_time = time.perf_counter()
        if self.__start_time is None:
            self.__start_time = current_time
        elapsed_time = current_time - self.__start_time

        
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
        
            
        if self.__is_recording:
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
        
        
