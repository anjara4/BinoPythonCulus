from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QDesktopWidget

import math
import pandas as pd

from parameters import Parameters
from screen_calibration import Screen_calibration

class Exercise(QWidget):
    def __init__(self, selected_config, recording_label, pupil_labs, cam_left, cam_right):
        super().__init__()

        self._parameters = Parameters()

        self.__selected_config = selected_config
        self.__recording_label = recording_label
        self.__pupil_labs = pupil_labs
        self.__cam_left = cam_left
        self.__cam_right = cam_right 

        screenCalibration = Screen_calibration()
        self.__size_screen_calibration_object_px = screenCalibration.get_size_object_px()

        screen_count = QDesktopWidget().screenCount()
        if screen_count > 1:
            screen = QDesktopWidget().screenGeometry(1)
        else :
            screen = QDesktopWidget().screenGeometry(0)
        self.__display_width = screen.width() 
        self.__display_height = screen.height()  
      
        
        self.__is_running = False
        self.__csv_recorder = None
        self.__is_recording = False
        self.__start_time = None
        self.elapsed_time = 0

        self.__size = 50
        self.__color = Qt.red
        self.__ratio_pixel_cm = 1
        self.__nb_cycle = 1000

    def set_nb_cycle(self, value):
        self.__nb_cycle = value

    def get_nb_cycle(self):
        return self.__nb_cycle
        
    def set_color(self, value):
        self.__color = value

    def get_color(self):
        return self.__color
        
    def set_csv_recorder(self, value):
        self.__csv_recorder = value

    def get_csv_recorder(self):
        return self.__csv_recorder

    def set_is_recording(self, value):
        self.__start_time = None
        self.__is_recording = value

    def get_is_recording(self):
        return self.__is_recording

    def set_is_running(self, value):
        self.__is_running = value
    
    def get_is_running(self):
        return self.__is_running
    
    def set_ratio_pixel_cm(self):
        self.__ratio_pixel_cm = self.__size_screen_calibration_object_px / self.get_size_object_cm()

    def get_ratio_pixel_cm(self):
        return self.__ratio_pixel_cm
    
    def set_selected_config(self, value):
        self.__selected_config = value
    
    def get_selected_config(self):
        return self.__selected_config
    
    def get_name_object(self):
        return self.__selected_config.get_name_config()
    
    def set_nb_cycle_exo(self, value):
        self.__nb_cycle = value
    
    def get_nb_cycle_exo(self):
        return self.__nb_cycle
    
    def set_size(self, value):
        self.__size = value

    def get_size(self):
        return self.__size
    
    def scale_size(self):
        self.__size = self.__size * self.__ratio_pixel_cm

    def set_start_time(self, value):
        self.__start_time = value

    def get_start_time(self):
        return self.__start_time
    
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

    def degrees_to_cm(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        return self.get_depth_from_config() * math.tan(angle_radians)
    
    def degrees_to_px(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        return self.get_depth_from_config() * math.tan(angle_radians) * self.get_ratio_pixel_cm()
    
    def get_display_width(self):
        return self.__display_width
    
    def get_display_height(self):
        return self.__display_height
    
    def get_depth_from_config(self):
        df = pd.read_csv(self._parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['Depth'].values.item()
    
    def get_size_object_cm(self):
        df = pd.read_csv(self._parameters.data_configuration, delimiter=';')
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]
        return filtered_df['SizeObject'].values.item()    