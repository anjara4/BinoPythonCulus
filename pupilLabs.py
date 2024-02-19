from PyQt5.QtWidgets import QDesktopWidget, QWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt

import pandas as pd

from ui_customDialog import CustomDialog 

import subprocess
import zmq

class PupilLabs(QWidget):
    def __init__(self, selected_config):
        super().__init__()

        self.__selected_config = selected_config
        self.__pupilLabs_status = None

    def get_path_pupilLabs(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]

        return filtered_df['PathPupilLabs'].values.item()

    def start_pupilLabs(self):
        if self.__selected_config.get_name_config() != "None":
            if self.__pupilLabs_status is None or self.__pupilLabs_status.poll() is not None:
                try:
                    self.__pupilLabs_status = subprocess.Popen([self.get_path_pupilLabs()])
                    dlg = CustomDialog(message="Pupil capture launched, it might tike a few seconds")
                    dlg.exec()
                except FileNotFoundError:
                    dlg = CustomDialog(message="Invalid path to PupilLabs executable")
                    dlg.exec()
            else:
                dlg = CustomDialog(message="Pupil capture already running")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Select a config")
            dlg.exec()

    def start_calibration_pupilLabs(self):
        if self.__pupilLabs_status == None:
            dlg = CustomDialog(message="PupilLab application not detected")
            dlg.exec() 
        elif self.__pupilLabs_status.poll() is None:
            ctx = zmq.Context()
            pupil_remote = zmq.Socket(ctx, zmq.REQ)
            pupil_remote.connect('tcp://127.0.0.1:50020')

            pupil_remote.send_string('C')
            print(pupil_remote.recv_string())
        else:
            dlg = CustomDialog(message="Start pupil capture")
            dlg.exec()

    def get_status(self):
        return self.__pupilLabs_status

