from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QSizePolicy, QWidget, QRadioButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from datetime import datetime
import os

from saccade_exercice import Saccade
from parameters import Parameters

from ui_customDialog import CustomDialog
from recording import CSV_recorder
from recording import PupilLabs_recorder

class UI_saccade(QWidget):
    def __init__(self, connected_patient, selected_config, calibration):
        super().__init__()
        self.saccade = None
        self.pupilLabs_recorder = PupilLabs_recorder()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__calibration = calibration
        parameters = Parameters()
        self.__data_path = parameters.data_folder_path 

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.lb_rec_img = QLabel(self)
        self.lb_rec_img.setGeometry(10, 10, 50, 50)
        self.pp_rec = QPixmap(parameters.image_recording)

        lb_color = QLabel("Select target color")
        self.cb_color = QComboBox()
        self.cb_color.setSizePolicy(size_policy)
        self.cb_color.setFixedWidth(300)
        self.cb_color.addItem("Black", QColor("black"))
        self.cb_color.addItem("Red", QColor("red"))
        self.cb_color.addItem("Blue", QColor("blue"))
        self.cb_color.setCurrentIndex(0)
        lt_color = QHBoxLayout()
        lt_color.addWidget(lb_color)
        lt_color.addWidget(self.cb_color)

        lb_size = QLabel("Select target size (cm)")
        self.sd_size = QSlider(Qt.Horizontal, self)
        self.sd_size.setSizePolicy(size_policy)
        self.sd_size.setFixedWidth(285)
        self.sd_size.setMinimum(1)
        self.sd_size.setMaximum(10)
        self.sd_size.setSliderPosition(1)
        self.sd_size.valueChanged.connect(self.update_sd_size_value)
        self.lb_sd_size_value = QLabel()
        self.lb_sd_size_value.setSizePolicy(size_policy)
        self.lb_sd_size_value.setFixedWidth(15)
        self.lb_sd_size_value.setText(str(self.sd_size.value()))
        lt_size = QHBoxLayout()
        lt_size.addWidget(lb_size)
        lt_size.addWidget(self.sd_size)
        lt_size.addWidget(self.lb_sd_size_value)

        lb_time_step = QLabel("Select time step (ms)")
        self.sd_time_step = QSlider(Qt.Horizontal, self)
        self.sd_time_step.setSizePolicy(size_policy)
        self.sd_time_step.setFixedWidth(285)
        self.sd_time_step.setMinimum(100)
        self.sd_time_step.setMaximum(5000)
        self.sd_time_step.setSliderPosition(1000)
        self.sd_time_step.valueChanged.connect(self.update_sd_time_step_value)
        self.lb_sd_time_step_value = QLabel()
        self.lb_sd_time_step_value.setSizePolicy(size_policy)
        self.lb_sd_time_step_value.setFixedWidth(15)
        self.lb_sd_time_step_value.setText(str(self.sd_time_step.value()))
        lt_time_step = QHBoxLayout()
        lt_time_step.addWidget(lb_time_step)
        lt_time_step.addWidget(self.sd_time_step)
        lt_time_step.addWidget(self.lb_sd_time_step_value)

        lb_delta_hor = QLabel("Delta left / write (cm)")
        self.sd_delta_hor = QSlider(Qt.Horizontal, self)
        self.sd_delta_hor.setSizePolicy(size_policy)
        self.sd_delta_hor.setFixedWidth(300)
        self.sd_delta_hor.setMinimum(0)
        self.sd_delta_hor.setMaximum(50)
        self.sd_delta_hor.setSliderPosition(20)
        self.sd_delta_hor.valueChanged.connect(self.update_sd_delta_hor_value)
        self.lb_sd_delta_hor_value = QLabel()
        self.lb_sd_delta_hor_value.setSizePolicy(size_policy)
        self.lb_sd_delta_hor_value.setFixedWidth(15)
        self.lb_sd_delta_hor_value.setText(str(self.sd_delta_hor.value()))
        lt_delta_hor = QHBoxLayout()
        lt_delta_hor.addWidget(lb_delta_hor)
        lt_delta_hor.addWidget(self.sd_delta_hor)
        lt_delta_hor.addWidget(self.lb_sd_delta_hor_value)

        lb_delta_ver = QLabel("Delta top / bottom (cm)")
        self.sd_delta_ver = QSlider(Qt.Horizontal, self)
        self.sd_delta_ver.setSizePolicy(size_policy)
        self.sd_delta_ver.setFixedWidth(300)
        self.sd_delta_ver.setMinimum(0)
        self.sd_delta_ver.setMaximum(50)
        self.sd_delta_ver.setSliderPosition(0)
        self.sd_delta_ver.valueChanged.connect(self.update_sd_delta_ver_value)
        self.lb_sd_delta_ver_value = QLabel()
        self.lb_sd_delta_ver_value.setSizePolicy(size_policy)
        self.lb_sd_delta_ver_value.setFixedWidth(15)
        self.lb_sd_delta_ver_value.setText(str(self.sd_delta_ver.value()))
        lt_delta_ver = QHBoxLayout()
        lt_delta_ver.addWidget(lb_delta_ver)
        lt_delta_ver.addWidget(self.sd_delta_ver)
        lt_delta_ver.addWidget(self.lb_sd_delta_ver_value)

        lb_auto_stop = QLabel("Automatic stop?")
        self.rb_true = QRadioButton("True", self)
        self.rb_false = QRadioButton("False", self)
        self.rb_false.setChecked(True)
        self.rb_false.toggled.connect(self.create_form_automatic_stop)
        lt_auto_stop = QHBoxLayout()
        lt_auto_stop.addWidget(lb_auto_stop)
        lt_auto_stop.addWidget(self.rb_true)
        lt_auto_stop.addWidget(self.rb_false)

        lb_nb_cycle = QLabel("Nb saccade cycle")
        self.sd_nb_cycle = QSlider(Qt.Horizontal, self)
        self.sd_nb_cycle.setSizePolicy(size_policy)
        self.sd_nb_cycle.setFixedWidth(285)
        self.sd_nb_cycle.setMinimum(1)
        self.sd_nb_cycle.setMaximum(50)
        self.sd_nb_cycle.setSliderPosition(10)
        self.sd_nb_cycle.setEnabled(False)
        self.sd_nb_cycle.valueChanged.connect(self.update_sd_nb_cycle_value)
        self.lb_sd_nb_cycle_value = QLabel()
        self.lb_sd_nb_cycle_value.setSizePolicy(size_policy)
        self.lb_sd_nb_cycle_value.setFixedWidth(15)
        self.lb_sd_nb_cycle_value.setText(str(self.sd_nb_cycle.value()))
        lt_nb_cycle = QHBoxLayout()
        lt_nb_cycle.addWidget(lb_nb_cycle)
        lt_nb_cycle.addWidget(self.sd_nb_cycle)
        lt_nb_cycle.addWidget(self.lb_sd_nb_cycle_value)

        bt_run = QPushButton("Run Saccade")
        bt_run.clicked.connect(self.bt_call_run_saccade)

        bt_run_record_target = QPushButton("Rec Target")
        bt_run_record_target.clicked.connect(lambda: self.bt_call_record_target(
            self.generate_foldername_rec(
                "Saccade", 
                self.__connected_patient.get_codePatient()),
            self.generate_filename_rec(
                "Saccade", 
                self.__connected_patient.get_codePatient())
            ))

        bt_run_record_pupil = QPushButton("Rec Pupil")
        bt_run_record_pupil.clicked.connect(lambda: self.bt_call_record_pupil(
            self.generate_foldername_rec(
                "Saccade", 
                self.__connected_patient.get_codePatient())
            ))

        bt_run_all = QPushButton("Run All")
        bt_run_all.clicked.connect(self.bt_call_run_all)

        bt_stop = QPushButton("Stop")
        bt_stop.clicked.connect(self.bt_call_stop)

        lt_bt_run_record = QHBoxLayout()
        lt_bt_run_record.addWidget(bt_run)
        lt_bt_run_record.addWidget(bt_run_record_target)
        lt_bt_run_record.addWidget(bt_run_record_pupil)
        lt_bt_run_record.addWidget(bt_run_all)
        lt_bt_run_record.addWidget(bt_stop)

        self.lt = QVBoxLayout()
        self.lt.addLayout(lt_color)
        self.lt.addLayout(lt_size)
        self.lt.addLayout(lt_time_step)
        self.lt.addLayout(lt_delta_hor)
        self.lt.addLayout(lt_delta_ver)
        self.lt.addLayout(lt_auto_stop)
        self.lt.addLayout(lt_nb_cycle)
        self.lt.addLayout(lt_bt_run_record)
        self.lt.addWidget(self.lb_rec_img)

        self.setLayout(self.lt)

    def create_form_automatic_stop(self):
        if self.rb_false.isChecked():
            self.sd_nb_cycle.setEnabled(False)
        else:
            self.sd_nb_cycle.setEnabled(True)

    def update_sd_nb_cycle_value(self):
        self.lb_sd_nb_cycle_value.setText(str(self.sd_nb_cycle.value()))

    def update_sd_size_value(self):
        self.lb_sd_size_value.setText(str(self.sd_size.value()))

    def update_sd_time_step_value(self):
        self.lb_sd_time_step_value.setText(str(self.sd_time_step.value()))

    def update_sd_delta_hor_value(self):
        self.lb_sd_delta_hor_value.setText(str(self.sd_delta_hor.value()))

    def update_sd_delta_ver_value(self):
        self.lb_sd_delta_ver_value.setText(str(self.sd_delta_ver.value()))

    def bt_call_run_all(self):
        folder_recording_name = self.generate_foldername_rec(
            "Saccade", 
            self.__connected_patient.get_codePatient())

        file_recording_name = self.generate_filename_rec(
            "Saccade", 
            self.__connected_patient.get_codePatient())

        self.bt_call_run_saccade()
        
        self.bt_call_record_target(folder_recording_name, file_recording_name)
        self.bt_call_record_pupil(folder_recording_name)

    def bt_call_record_pupil(self):
        self.pupilLabs_recorder.start_record_pupilLab(
            self.__calibration.get_pupilLabs().get_status())

    def generate_folder_rec(self, foldername):
        try:
            os.mkdir(foldername)
        except OSError:
            print(f"Creation of the directory {foldername} failed")
        else:
            print(f"Successfully created the directory {foldername}")

    def generate_filename_rec(self, exercice_name, code_patient):
        now = datetime.now()
        date = now.strftime('%d-%m-%Y')
        time = now.strftime("%H") + "-" + now.strftime("%M")
        filename = f"{exercice_name}_{code_patient}_{date}_{time}_Target.csv"
        return filename

    def generate_foldername_rec(self, exercice_name, code_patient):
        now = datetime.now()
        date = now.strftime('%d-%m-%Y')
        time = now.strftime("%H") + "-" + now.strftime("%M")
        filename = self.__data_path + f"{exercice_name}_{code_patient}_{date}_{time}"
        self.generate_folder_rec(filename)
        return filename

    def bt_call_record_pupil(self, folder_recording_name): 
        self.pupilLabs_recorder.start_record_pupilLab(
            self.__calibration.get_pupilLabs().get_status(),
            folder_recording_name)


    def bt_call_stop(self):
        self.pupilLabs_recorder.stop_record_pupilLab(
            self.__calibration.get_pupilLabs().get_status())

        self.lb_rec_img.clear()
        if self.saccade is not None:
            self.saccade.close()
            self.saccade = None

    def bt_call_run_saccade(self):
        if self.__selected_config.get_name_config() != "None":
            self.saccade = Saccade(
                self.__calibration.get_pupilLabs().get_status(),
                self.lb_rec_img)
            self.saccade.set_selected_config(self.__selected_config)
            self.saccade.set_ratio_pixel_cm()
            self.saccade.set_is_running(True)

            if self.rb_false.isChecked():
                self.saccade.set_nb_cycle(10000)
                # define a high number represinting an infinite value
            else:
                self.saccade.set_nb_cycle(self.sd_nb_cycle.value())
            self.saccade.set_size(self.sd_size.value())
            self.saccade.set_color(QColor(self.cb_color.currentData()))
            self.saccade.set_time_step(self.sd_time_step.value())
            self.saccade.set_delta_hor(self.sd_delta_hor.value()/2)
            self.saccade.scale_delta_hor()
            self.saccade.set_delta_ver(self.sd_delta_ver.value()/2)
            self.saccade.scale_delta_ver()

            screen = QDesktopWidget().screenGeometry(1)
            self.saccade.setGeometry(screen)
            # self.saccade.showMaximized()
            self.saccade.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

    def bt_call_record_target(self, folder_recording_name, file_recording_name):
        if self.saccade is not None:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(folder_recording_name + "/" + file_recording_name)
                csv_recorder.set_header()

                self.saccade.set_csv_recorder(csv_recorder)

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))

                self.saccade.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Start saccade first")
            dlg.exec()
