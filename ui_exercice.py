from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget, QRadioButton
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap

from exercice import Infinite
from exercice import Saccade
from exercice import Fixation

from ui_customDialog import CustomDialog 
from recording import CSV_recorder
from recording import PupilLabs_recorder
from cam_video_world import CameraWorld
from cam_video_world import CameraLeft
from cam_video_world import CameraWrite
from ui_calibration import UI_calibration

import zmq
import sys
import time
import threading

class UI_main_excercice(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        self.ui_calibration = UI_calibration(self.__selected_config)

        # Create a sub-tab widget
        sub_tabs = QTabWidget()
        sub_tab1 = UI_saccade(self.__connected_patient, self.__selected_config, self.ui_calibration)
        sub_tab2 = UI_fixation(self.__connected_patient, self.__selected_config, self.ui_calibration)
        sub_tab3 = UI_infinite(self.__connected_patient, self.__selected_config, self.ui_calibration)
        sub_tabs.addTab(sub_tab1, "Saccade")
        sub_tabs.addTab(sub_tab2, "Fixation")
        sub_tabs.addTab(sub_tab3, "Infini")

        # Create a label and line edit for the common interface for Calibration
        
        layout_exo = QVBoxLayout()
        layout_exo.addWidget(sub_tabs)
        layout_exo.addLayout(self.ui_calibration.layout_calibration)
        
        cam_world = CameraWorld()
        cam_left = CameraLeft()
        cam_write = CameraWrite()

        layout_camera = QHBoxLayout()
        #layout_camera.addWidget(cam_world)
        layout_camera.addWidget(cam_left)
        layout_camera.addWidget(cam_write)

        layout = QHBoxLayout()
        layout.addLayout(layout_exo)
        layout.addLayout(layout_camera)
        
        self.setLayout(layout)

class UI_saccade(QWidget):
    def __init__(self, connected_patient, selected_config, calibration):
        super().__init__()
        self.saccade = None 
        self.pupilLabs_recorder = PupilLabs_recorder()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__calibration = calibration

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png')  

        label_color = QLabel("Select target color")
        self.combo_box_color = QComboBox()
        self.combo_box_color.setSizePolicy(size_policy)
        self.combo_box_color.setFixedWidth(300)
        self.combo_box_color.addItem("Black", QColor("black"))
        self.combo_box_color.addItem("Red", QColor("red"))
        self.combo_box_color.addItem("Blue", QColor("blue"))
        self.combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(self.combo_box_color)

        label_size = QLabel("Select target size (cm)")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(1)
        self.slider_size.setMaximum(10)
        self.slider_size.setSliderPosition(1)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_time_step = QLabel("Select time step (ms)")
        self.slider_time_step = QSlider(Qt.Horizontal, self)
        self.slider_time_step.setSizePolicy(size_policy)
        self.slider_time_step.setFixedWidth(285)
        self.slider_time_step.setMinimum(100)
        self.slider_time_step.setMaximum(5000)
        self.slider_time_step.setSliderPosition(1000)
        self.slider_time_step.valueChanged.connect(self.update_slider_time_step_value)
        self.label_slider_time_step_value = QLabel()
        self.label_slider_time_step_value.setSizePolicy(size_policy)
        self.label_slider_time_step_value.setFixedWidth(15)
        self.label_slider_time_step_value.setText(str(self.slider_time_step.value()))
        layout_time_step = QHBoxLayout()
        layout_time_step.addWidget(label_time_step)
        layout_time_step.addWidget(self.slider_time_step)
        layout_time_step.addWidget(self.label_slider_time_step_value)

        label_delta_horizontal = QLabel("Delta left / write (cm)")
        self.slider_delta_horizontal = QSlider(Qt.Horizontal, self)
        self.slider_delta_horizontal.setSizePolicy(size_policy)
        self.slider_delta_horizontal.setFixedWidth(300)
        self.slider_delta_horizontal.setMinimum(0)
        self.slider_delta_horizontal.setMaximum(50)
        self.slider_delta_horizontal.setSliderPosition(0)
        self.slider_delta_horizontal.valueChanged.connect(self.update_slider_delta_horizontal_value)
        self.label_slider_delta_horizontal_value = QLabel()
        self.label_slider_delta_horizontal_value.setSizePolicy(size_policy)
        self.label_slider_delta_horizontal_value.setFixedWidth(15)
        self.label_slider_delta_horizontal_value.setText(str(self.slider_delta_horizontal.value()))
        layout_delta_horizontal = QHBoxLayout()
        layout_delta_horizontal.addWidget(label_delta_horizontal)
        layout_delta_horizontal.addWidget(self.slider_delta_horizontal)
        layout_delta_horizontal.addWidget(self.label_slider_delta_horizontal_value)

        label_delta_vertical = QLabel("Delta top / bottom (cm)")
        self.slider_delta_vertical = QSlider(Qt.Horizontal, self)
        self.slider_delta_vertical.setSizePolicy(size_policy)
        self.slider_delta_vertical.setFixedWidth(300)
        self.slider_delta_vertical.setMinimum(0)
        self.slider_delta_vertical.setMaximum(50)
        self.slider_delta_vertical.setSliderPosition(20)
        self.slider_delta_vertical.valueChanged.connect(self.update_slider_delta_vertical_value)
        self.label_slider_delta_vertical_value = QLabel()
        self.label_slider_delta_vertical_value.setSizePolicy(size_policy)
        self.label_slider_delta_vertical_value.setFixedWidth(15)
        self.label_slider_delta_vertical_value.setText(str(self.slider_delta_vertical.value()))
        layout_delta_vertical = QHBoxLayout()
        layout_delta_vertical.addWidget(label_delta_vertical)
        layout_delta_vertical.addWidget(self.slider_delta_vertical)
        layout_delta_vertical.addWidget(self.label_slider_delta_vertical_value)

        label_auto_stop = QLabel("Automatic stop?")
        self.radio_bouton_true = QRadioButton("True", self)
        self.radio_bouton_false = QRadioButton("False", self)
        self.radio_bouton_false.setChecked(True)
        self.radio_bouton_false.toggled.connect(self.create_form_automatic_stop)
        layout_auto_stop = QHBoxLayout()
        layout_auto_stop.addWidget(label_auto_stop)
        layout_auto_stop.addWidget(self.radio_bouton_true)
        layout_auto_stop.addWidget(self.radio_bouton_false)

        label_nb_cycle = QLabel("Nb saccade cycle")
        self.slider_nb_cycle = QSlider(Qt.Horizontal, self)
        self.slider_nb_cycle.setSizePolicy(size_policy)
        self.slider_nb_cycle.setFixedWidth(285)
        self.slider_nb_cycle.setMinimum(1)
        self.slider_nb_cycle.setMaximum(50)
        self.slider_nb_cycle.setSliderPosition(10)
        self.slider_nb_cycle.setEnabled(False)
        self.slider_nb_cycle.valueChanged.connect(self.update_slider_nb_cycle_value)
        self.label_slider_nb_cycle_value = QLabel()
        self.label_slider_nb_cycle_value.setSizePolicy(size_policy)
        self.label_slider_nb_cycle_value.setFixedWidth(15)
        self.label_slider_nb_cycle_value.setText(str(self.slider_nb_cycle.value()))
        layout_nb_cycle = QHBoxLayout()
        layout_nb_cycle.addWidget(label_nb_cycle)
        layout_nb_cycle.addWidget(self.slider_nb_cycle)
        layout_nb_cycle.addWidget(self.label_slider_nb_cycle_value)

        button_run = QPushButton("Run Saccade")
        button_run.clicked.connect(self.button_call_run_saccade)

        button_run_record_target = QPushButton("Rec Target")
        button_run_record_target.clicked.connect(self.button_call_record_target)

        button_run_record_pupil = QPushButton("Rec Pupil")
        button_run_record_pupil.clicked.connect(self.button_call_record_pupil)

        button_run_all = QPushButton("Run All")
        button_run_all.clicked.connect(self.button_call_run_all)

        button_stop = QPushButton("Stop")
        button_stop.clicked.connect(self.button_call_stop)

        layout_button_run_record = QHBoxLayout()
        layout_button_run_record.addWidget(button_run)
        layout_button_run_record.addWidget(button_run_record_target)
        layout_button_run_record.addWidget(button_run_record_pupil)
        layout_button_run_record.addWidget(button_run_all)
        layout_button_run_record.addWidget(button_stop)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color) 
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_time_step)
        self.layout.addLayout(layout_delta_horizontal)
        self.layout.addLayout(layout_delta_vertical)
        self.layout.addLayout(layout_auto_stop)
        self.layout.addLayout(layout_nb_cycle)
        self.layout.addLayout(layout_button_run_record)
        self.layout.addWidget(self.recording_label)

        self.setLayout(self.layout)

    def create_form_automatic_stop(self):
        if self.radio_bouton_false.isChecked():
            self.slider_nb_cycle.setEnabled(False)
        else:
            self.slider_nb_cycle.setEnabled(True)

    def update_slider_nb_cycle_value(self):
        self.label_slider_nb_cycle_value.setText(str(self.slider_nb_cycle.value()))

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_time_step_value(self):
        self.label_slider_time_step_value.setText(str(self.slider_time_step.value()))

    def update_slider_delta_horizontal_value(self):
        self.label_slider_delta_horizontal_value.setText(str(self.slider_delta_horizontal.value()))

    def update_slider_delta_vertical_value(self):
        self.label_slider_delta_vertical_value.setText(str(self.slider_delta_vertical.value()))

    def button_call_run_all(self):
        self.button_call_run_saccade()
        self.button_call_record_target()
        self.button_call_record_pupil()

    def button_call_record_pupil(self):
        self.pupilLabs_recorder.start_record_pupilLab(self.__calibration.get_pupilLabs_status())

    def button_call_stop(self):
        self.pupilLabs_recorder.stop_record_pupilLab(self.__calibration.get_pupilLabs_status())
        self.recording_label.clear()
        if self.saccade != None:
            self.saccade.close()
            self.saccade = None

    def button_call_run_saccade(self):
        if self.__selected_config.get_name_config() != "None":
            self.saccade = Saccade()
            self.saccade.set_selected_config(self.__selected_config)
            self.saccade.set_ratio_pixel_cm()
            self.saccade.set_is_running(True)

            if self.radio_bouton_false.isChecked():
                self.saccade.set_nb_cycle(10000) #define a high number represinting an infinite value
            else:
                self.saccade.set_nb_cycle(self.slider_nb_cycle.value())
            
            self.saccade.set_size(self.slider_size.value())
            self.saccade.set_color(QColor(self.combo_box_color.currentData()))
            self.saccade.set_time_step(self.slider_time_step.value()) 
            self.saccade.set_delta_horizontal(self.slider_delta_horizontal.value()/2)
            self.saccade.set_delta_vertical(self.slider_delta_vertical.value()/2)
            
            screen = QDesktopWidget().screenGeometry(1)
            self.saccade.setGeometry(screen)
            #self.saccade.showMaximized()
            self.saccade.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

    def button_call_record_target(self):
        if self.saccade != None:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Saccade"))
                csv_recorder.set_header()

                self.saccade.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))

                self.saccade.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

class UI_fixation(QWidget):
    def __init__(self, connected_patient, selected_config, calibration):
        super().__init__()
        self.fixation = None
        self.pupilLabs_recorder = PupilLabs_recorder()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__calibration = calibration

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png') 

        label_color = QLabel("Select target color")
        self.combo_box_color = QComboBox()
        self.combo_box_color.setSizePolicy(size_policy)
        self.combo_box_color.setFixedWidth(300)
        self.combo_box_color.addItem("Black", QColor("black"))
        self.combo_box_color.addItem("Red", QColor("red"))
        self.combo_box_color.addItem("Blue", QColor("blue"))
        self.combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(self.combo_box_color)

        label_size = QLabel("Select target size (cm)")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(1)
        self.slider_size.setMaximum(10)
        self.slider_size.setSliderPosition(1)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_horizontal_position = QLabel("Select delta X from center (cm)")
        self.slider_horizontal_position = QSlider(Qt.Horizontal, self)
        self.slider_horizontal_position.setSizePolicy(size_policy)
        self.slider_horizontal_position.setFixedWidth(282)
        self.slider_horizontal_position.setMinimum(-20)
        self.slider_horizontal_position.setMaximum(20)
        self.slider_horizontal_position.setSliderPosition(0)
        self.slider_horizontal_position.valueChanged.connect(self.update_slider_horizontal_position_value)
        self.label_slider_horizontal_position_value = QLabel()
        self.label_slider_horizontal_position_value.setSizePolicy(size_policy)
        self.label_slider_horizontal_position_value.setFixedWidth(18)
        self.label_slider_horizontal_position_value.setText(str(self.slider_horizontal_position.value()))
        layout_horizontal_position = QHBoxLayout()
        layout_horizontal_position.addWidget(label_horizontal_position)
        layout_horizontal_position.addWidget(self.slider_horizontal_position)
        layout_horizontal_position.addWidget(self.label_slider_horizontal_position_value)

        label_vertical_position = QLabel("Select delta y from center (cm)")
        self.slider_vertical_position = QSlider(Qt.Horizontal, self)
        self.slider_vertical_position.setSizePolicy(size_policy)
        self.slider_vertical_position.setFixedWidth(282)
        self.slider_vertical_position.setMinimum(-20)
        self.slider_vertical_position.setMaximum(20)
        self.slider_vertical_position.setSliderPosition(0)
        self.slider_vertical_position.valueChanged.connect(self.update_slider_vertical_position_value)
        self.label_slider_vertical_position_value = QLabel()
        self.label_slider_vertical_position_value.setSizePolicy(size_policy)
        self.label_slider_vertical_position_value.setFixedWidth(18)
        self.label_slider_vertical_position_value.setText(str(self.slider_vertical_position.value()))
        layout_vertical_position = QHBoxLayout()
        layout_vertical_position.addWidget(label_vertical_position)
        layout_vertical_position.addWidget(self.slider_vertical_position)
        layout_vertical_position.addWidget(self.label_slider_vertical_position_value)

        button_run = QPushButton("Run Fixation")
        button_run.clicked.connect(self.button_call_run_fixation)

        button_record_target = QPushButton("Rec Target")
        button_record_target.clicked.connect(self.button_call_record_target)

        button_record_pupil = QPushButton("Rec Pupil")
        button_record_pupil.clicked.connect(self.button_call_record_pupil)

        button_run_all = QPushButton("Run All")
        button_run_all.clicked.connect(self.button_call_run_all)

        button_stop = QPushButton("Stop")
        button_stop.clicked.connect(self.button_call_stop)

        label_auto_stop = QLabel("Automatic stop?")
        self.radio_bouton_true = QRadioButton("True", self)
        self.radio_bouton_false = QRadioButton("False", self)
        self.radio_bouton_false.setChecked(True)
        self.radio_bouton_false.toggled.connect(self.create_form_automatic_stop)
        layout_auto_stop = QHBoxLayout()
        layout_auto_stop.addWidget(label_auto_stop)
        layout_auto_stop.addWidget(self.radio_bouton_true)
        layout_auto_stop.addWidget(self.radio_bouton_false)

        label_time_exo = QLabel("Time (s)")
        self.slider_time_exo = QSlider(Qt.Horizontal, self)
        self.slider_time_exo.setSizePolicy(size_policy)
        self.slider_time_exo.setFixedWidth(285)
        self.slider_time_exo.setMinimum(1)
        self.slider_time_exo.setMaximum(100)
        self.slider_time_exo.setSliderPosition(10)
        self.slider_time_exo.setEnabled(False)
        self.slider_time_exo.valueChanged.connect(self.update_slider_time_exo_value)
        self.label_slider_time_exo_value = QLabel()
        self.label_slider_time_exo_value.setSizePolicy(size_policy)
        self.label_slider_time_exo_value.setFixedWidth(15)
        self.label_slider_time_exo_value.setText(str(self.slider_time_exo.value()))
        layout_time_exo = QHBoxLayout()
        layout_time_exo.addWidget(label_time_exo)
        layout_time_exo.addWidget(self.slider_time_exo)
        layout_time_exo.addWidget(self.label_slider_time_exo_value)

        layout_button_run_record = QHBoxLayout()
        layout_button_run_record.addWidget(button_run)
        layout_button_run_record.addWidget(button_record_target)
        layout_button_run_record.addWidget(button_record_pupil)
        layout_button_run_record.addWidget(button_run_all)
        layout_button_run_record.addWidget(button_stop)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_horizontal_position)
        self.layout.addLayout(layout_vertical_position)
        self.layout.addLayout(layout_auto_stop)
        self.layout.addLayout(layout_time_exo)
        self.layout.addLayout(layout_button_run_record)
        self.layout.addWidget(self.recording_label)

        self.setLayout(self.layout)

    def create_form_automatic_stop(self):
        if self.radio_bouton_false.isChecked():
            self.slider_time_exo.setEnabled(False)
        else:
            self.slider_time_exo.setEnabled(True)

    def update_slider_time_exo_value(self):
        self.label_slider_time_exo_value.setText(str(self.slider_time_exo.value()))

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_vertical_position_value(self):
        self.label_slider_vertical_position_value.setText(str(self.slider_vertical_position.value()))

    def update_slider_horizontal_position_value(self):
        self.label_slider_horizontal_position_value.setText(str(self.slider_horizontal_position.value()))

    def button_call_run_all(self):
        self.button_call_run_fixation()
        self.button_call_record_target()
        self.button_call_record_pupil()

    def button_call_record_pupil(self):
        self.pupilLabs_recorder.start_record_pupilLab(self.__calibration.get_pupilLabs_status())

    def button_call_stop(self):
        self.pupilLabs_recorder.stop_record_pupilLab(self.__calibration.get_pupilLabs_status())
        self.recording_label.clear()
        if self.fixation != None:
            self.fixation.close()
            self.fixation = None

    def button_call_run_fixation(self):
        self.fixation = Fixation()
        if self.__selected_config.get_name_config() != "None":
            self.fixation.set_is_running(True)
            self.fixation.set_selected_config(self.__selected_config)
            self.fixation.set_color(QColor(self.combo_box_color.currentData()))
            self.fixation.set_ratio_pixel_cm()
            self.fixation.set_size(self.slider_size.value())
            self.fixation.set_horizontal_position(self.slider_horizontal_position.value())
            self.fixation.set_vertical_position(self.slider_vertical_position.value())

            if self.radio_bouton_false.isChecked():
                self.fixation.set_time_exo(10000) #define a high number represinting an infinite value
            else:
                self.fixation.set_time_exo(self.slider_time_exo.value())

            screen = QDesktopWidget().screenGeometry(1)
            self.fixation.setGeometry(screen)
            #self.fixation.showMaximized()
            self.fixation.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

    def button_call_record_target(self):
        if self.fixation != None:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Fixation"))
                csv_recorder.set_header()

                self.fixation.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))

                self.fixation.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

class UI_infinite(QWidget):
    def __init__(self, connected_patient, selected_config, calibration):
        super().__init__()
        self.__is_button_start_infinite_on = False
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__calibration = calibration
        self.infinite = None
        self.pupilLabs_recorder = PupilLabs_recorder()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png') 

        label_direction = QLabel("Select target direction")
        self.combo_box_direction = QComboBox()
        self.combo_box_direction.setSizePolicy(size_policy)
        self.combo_box_direction.setFixedWidth(300)
        self.combo_box_direction.addItem("Vertical")
        self.combo_box_direction.addItem("Horizontal")
        self.combo_box_direction.setCurrentIndex(0)
        layout_direction = QHBoxLayout()
        layout_direction.addWidget(label_direction)
        layout_direction.addWidget(self.combo_box_direction)

        label_color = QLabel("Select target color")
        self.combo_box_color = QComboBox()
        self.combo_box_color.setSizePolicy(size_policy)
        self.combo_box_color.setFixedWidth(300)
        self.combo_box_color.addItem("Black", QColor("black"))
        self.combo_box_color.addItem("Red", QColor("red"))
        self.combo_box_color.addItem("Blue", QColor("blue"))
        self.combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(self.combo_box_color)

        label_size = QLabel("Select target size (cm)")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(1)
        self.slider_size.setMaximum(10)
        self.slider_size.setSliderPosition(1)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_speed = QLabel("Select target speed")
        self.slider_speed = QSlider(Qt.Horizontal, self)
        self.slider_speed.setSizePolicy(size_policy)
        self.slider_speed.setFixedWidth(285)
        self.slider_speed.setMinimum(10)
        self.slider_speed.setMaximum(200)
        self.slider_speed.valueChanged.connect(self.update_slider_speed_value)
        self.label_slider_speed_value = QLabel()
        self.label_slider_speed_value.setSizePolicy(size_policy)
        self.label_slider_speed_value.setFixedWidth(15)
        self.label_slider_speed_value.setText(str(self.slider_speed.value()))
        layout_speed = QHBoxLayout()
        layout_speed.addWidget(label_speed)
        layout_speed.addWidget(self.slider_speed)
        layout_speed.addWidget(self.label_slider_speed_value)

        label_width_infini_cm = QLabel("Select width infini object (cm)")
        self.slider_width_infini_cm = QSlider(Qt.Horizontal, self)
        self.slider_width_infini_cm.setSizePolicy(size_policy)
        self.slider_width_infini_cm.setFixedWidth(285)
        self.slider_width_infini_cm.setMinimum(5)
        self.slider_width_infini_cm.setMaximum(40)
        self.slider_width_infini_cm.setSliderPosition(10)
        self.slider_width_infini_cm.valueChanged.connect(self.update_slider_width_infini_cm_value)
        self.label_slider_width_infini_cm_value = QLabel()
        self.label_slider_width_infini_cm_value.setSizePolicy(size_policy)
        self.label_slider_width_infini_cm_value.setFixedWidth(15)
        self.label_slider_width_infini_cm_value.setText(str(self.slider_width_infini_cm.value()))
        layout_width_infini_cm = QHBoxLayout()
        layout_width_infini_cm.addWidget(label_width_infini_cm)
        layout_width_infini_cm.addWidget(self.slider_width_infini_cm)
        layout_width_infini_cm.addWidget(self.label_slider_width_infini_cm_value)

        label_height_infini_cm = QLabel("Select height infini object (cm)")
        self.slider_height_infini_cm = QSlider(Qt.Horizontal, self)
        self.slider_height_infini_cm.setSizePolicy(size_policy)
        self.slider_height_infini_cm.setFixedWidth(285)
        self.slider_height_infini_cm.setMinimum(5)
        self.slider_height_infini_cm.setMaximum(30)
        self.slider_height_infini_cm.setSliderPosition(20)
        self.slider_height_infini_cm.valueChanged.connect(self.update_slider_height_infini_cm_value)
        self.label_slider_height_infini_cm_value = QLabel()
        self.label_slider_height_infini_cm_value.setSizePolicy(size_policy)
        self.label_slider_height_infini_cm_value.setFixedWidth(15)
        self.label_slider_height_infini_cm_value.setText(str(self.slider_height_infini_cm.value()))
        layout_height_infini_cm = QHBoxLayout()
        layout_height_infini_cm.addWidget(label_height_infini_cm)
        layout_height_infini_cm.addWidget(self.slider_height_infini_cm)
        layout_height_infini_cm.addWidget(self.label_slider_height_infini_cm_value)

        label_auto_stop = QLabel("Automatic stop?")
        self.radio_bouton_true = QRadioButton("True", self)
        self.radio_bouton_false = QRadioButton("False", self)
        self.radio_bouton_false.setChecked(True)
        self.radio_bouton_false.toggled.connect(self.create_form_automatic_stop)
        layout_auto_stop = QHBoxLayout()
        layout_auto_stop.addWidget(label_auto_stop)
        layout_auto_stop.addWidget(self.radio_bouton_true)
        layout_auto_stop.addWidget(self.radio_bouton_false)

        label_nb_cycle = QLabel("Nb saccade cycle")
        self.slider_nb_cycle = QSlider(Qt.Horizontal, self)
        self.slider_nb_cycle.setSizePolicy(size_policy)
        self.slider_nb_cycle.setFixedWidth(285)
        self.slider_nb_cycle.setMinimum(1)
        self.slider_nb_cycle.setMaximum(20)
        self.slider_nb_cycle.setSliderPosition(5)
        self.slider_nb_cycle.setEnabled(False)
        self.slider_nb_cycle.valueChanged.connect(self.update_slider_nb_cycle_value)
        self.label_slider_nb_cycle_value = QLabel()
        self.label_slider_nb_cycle_value.setSizePolicy(size_policy)
        self.label_slider_nb_cycle_value.setFixedWidth(15)
        self.label_slider_nb_cycle_value.setText(str(self.slider_nb_cycle.value()))
        layout_nb_cycle = QHBoxLayout()
        layout_nb_cycle.addWidget(label_nb_cycle)
        layout_nb_cycle.addWidget(self.slider_nb_cycle)
        layout_nb_cycle.addWidget(self.label_slider_nb_cycle_value)

        button_run = QPushButton("Run Infini")
        button_run.clicked.connect(self.button_call_run_infini)

        button_run_record_target = QPushButton("Rec Target")
        button_run_record_target.clicked.connect(self.button_call_record_target)

        button_run_record_pupil = QPushButton("Rec Pupil")
        button_run_record_pupil.clicked.connect(self.button_call_record_pupil)

        button_run_all = QPushButton("Run All")
        button_run_all.clicked.connect(self.button_call_run_all)

        button_stop = QPushButton("Stop")
        button_stop.clicked.connect(self.button_call_stop)

        layout_button_run_record = QHBoxLayout()
        layout_button_run_record.addWidget(button_run)
        layout_button_run_record.addWidget(button_run_record_target)
        layout_button_run_record.addWidget(button_run_record_pupil)
        layout_button_run_record.addWidget(button_run_all)
        layout_button_run_record.addWidget(button_stop)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_direction)
        self.layout.addLayout(layout_color) 
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_speed)
        self.layout.addLayout(layout_width_infini_cm)
        self.layout.addLayout(layout_height_infini_cm)
        self.layout.addLayout(layout_auto_stop)
        self.layout.addLayout(layout_nb_cycle)
        self.layout.addLayout(layout_button_run_record)
        self.layout.addWidget(self.recording_label)

        self.setLayout(self.layout)

    def create_form_automatic_stop(self):
        if self.radio_bouton_false.isChecked():
            self.slider_nb_cycle.setEnabled(False)
        else:
            self.slider_nb_cycle.setEnabled(True)

    def update_slider_nb_cycle_value(self):
        self.label_slider_nb_cycle_value.setText(str(self.slider_nb_cycle.value()))


    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_speed_value(self):
        self.label_slider_speed_value.setText(str(self.slider_speed.value()))

    def update_slider_width_infini_cm_value(self):
        self.label_slider_width_infini_cm_value.setText(str(self.slider_width_infini_cm.value()))

    def update_slider_height_infini_cm_value(self):
        self.label_slider_height_infini_cm_value.setText(str(self.slider_height_infini_cm.value()))

    def button_call_record_pupil(self):
        self.pupilLabs_recorder.start_record_pupilLab(self.__calibration.get_pupilLabs_status())

    def button_call_stop(self):
        self.pupilLabs_recorder.stop_record_pupilLab(self.__calibration.get_pupilLabs_status())
        self.recording_label.clear()
        if self.infinite != None:
            self.infinite.close()
            self.infinite = None

    def button_call_run_all(self):
        self.button_call_run_infini()
        self.button_call_record_pupil()
        self.button_call_record_target()

    def button_call_run_infini(self):
        if self.__selected_config.get_name_config() != "None":
            self.infinite = Infinite()

            if self.radio_bouton_false.isChecked():
                self.infinite.set_nb_cycle(10000) #define a high number represinting an infinite value
            else:
                self.infinite.set_nb_cycle(self.slider_nb_cycle.value())

            self.infinite.set_is_running(True)
            self.infinite.set_speed(self.slider_speed.value()/1000) #the slider only return integer value
            self.infinite.set_size(self.slider_size.value())
            self.infinite.set_color(QColor(self.combo_box_color.currentData()))
            self.infinite.set_is_object_vertical((self.combo_box_direction.currentIndex() == 0))#index==0 -> is_vertical=True
            self.infinite.set_width_target_infini_object_cm(self.slider_width_infini_cm.value())
            self.infinite.set_height_target_infini_object_cm(self.slider_height_infini_cm.value())
            self.infinite.set_selected_config(self.__selected_config)

            self.infinite.init_scenario()

            screen = QDesktopWidget().screenGeometry(1)
            self.infinite.setGeometry(screen)
            #self.infinite.showMaximized()
            self.infinite.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec() 

    def button_call_record_target(self):
        if self.infinite != None:
            if self.__connected_patient.get_codePatient() != "None":
                if (self.combo_box_direction.currentIndex() == 0):#index==0 -> is_vertical=True
                    exercice_name = "InfiniteV"
                else:
                    exercice_name = "InfiniteH"

                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), exercice_name))
                csv_recorder.set_header()

                self.infinite.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))
                
                self.infinite.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()    
        else: 
            dlg = CustomDialog(message="Start infini first")
            dlg.exec()

