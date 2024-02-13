from PyQt5.QtWidgets import QDesktopWidget, QWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt

from calibration import Calibration

from ui_customDialog import CustomDialog 

import subprocess

import pandas as pd

import zmq

class UI_calibration(QWidget):
    def __init__(self, selected_config):
        super().__init__()
        
        self.__pupilLabs_status = None

        self.__selected_config = selected_config

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_start_pupilLabs = QPushButton("Run Pupil")
        button_start_pupilLabs.clicked.connect(self.start_pupilLabs)

        button_start_lens = QPushButton("Run Lens")
        button_start_lens.clicked.connect(self.start_calibration_lens)

        layout_button_start = QHBoxLayout()
        layout_button_start.addWidget(button_start_pupilLabs)
        layout_button_start.addWidget(button_start_lens)

        label_size = QLabel("Select size calibration object")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(300)
        self.slider_size.setMaximum(1000)
        self.slider_size.setSliderPosition(300)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        button_start_calibration_pupilLabs = QPushButton("Calibration Pupil")
        button_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)

        button_start_calibration_lens = QPushButton("Calibration Lens")
        button_start_calibration_lens.clicked.connect(self.start_calibration_lens)

        layout_button_calibration = QHBoxLayout()
        layout_button_calibration.addWidget(button_start_calibration_pupilLabs)
        layout_button_calibration.addWidget(button_start_calibration_lens)

        self.layout_calibration = QVBoxLayout()
        self.layout_calibration.addLayout(layout_button_start)
        self.layout_calibration.addLayout(layout_size)
        self.layout_calibration.addLayout(layout_button_calibration)

    def get_pupilLabs_status(self):
        return self.__pupilLabs_status 

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

    def get_path_pupilLabs(self):
        df = pd.read_csv('data_configuration.csv', delimiter=';')
        
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]

        return filtered_df['PathPupilLabs'].values.item()

    def start_lens(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("start lens")

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

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

    def start_calibration_lens(self):
        screen = QDesktopWidget().screenGeometry(1)
        self.calibration = Calibration(self.slider_size.value())
        self.calibration.setGeometry(screen)
        #self.calibration.showMaximized()
        self.calibration.showFullScreen()

