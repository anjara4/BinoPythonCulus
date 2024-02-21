from PyQt5.QtWidgets import QDesktopWidget, QSlider, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QWidget, QRadioButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from datetime import datetime
import os

from infinite_exercice import Infinite
from parameters import Parameters

from ui_customDialog import CustomDialog
from recording import CSV_recorder
from recording import PupilLabs_recorder

class UI_infinite(QWidget):
    def __init__(self, connected_patient, selected_config, calibration):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__calibration = calibration
        self.infinite = None
        self.pupilLabs_recorder = PupilLabs_recorder()
        parameters = Parameters()
        self.__data_path = parameters.data_folder_path 

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.lb_rec_img = QLabel(self)
        self.lb_rec_img.setGeometry(10, 10, 50, 50)
        self.pp_rec = QPixmap(parameters.image_recording)

        lb_direction = QLabel("Select target direction")
        self.cb_direction = QComboBox()
        self.cb_direction.setSizePolicy(size_policy)
        self.cb_direction.setFixedWidth(300)
        self.cb_direction.addItem("Horizontal")
        self.cb_direction.addItem("Vertical")
        self.cb_direction.setCurrentIndex(0)
        lt_direction = QHBoxLayout()
        lt_direction.addWidget(lb_direction)
        lt_direction.addWidget(self.cb_direction)

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

        lb_speed = QLabel("Select target speed")
        self.sd_speed = QSlider(Qt.Horizontal, self)
        self.sd_speed.setSizePolicy(size_policy)
        self.sd_speed.setFixedWidth(285)
        self.sd_speed.setMinimum(10)
        self.sd_speed.setMaximum(200)
        self.sd_speed.valueChanged.connect(self.update_sd_speed_value)
        self.lb_sd_speed_value = QLabel()
        self.lb_sd_speed_value.setSizePolicy(size_policy)
        self.lb_sd_speed_value.setFixedWidth(15)
        self.lb_sd_speed_value.setText(str(self.sd_speed.value()))
        lt_speed = QHBoxLayout()
        lt_speed.addWidget(lb_speed)
        lt_speed.addWidget(self.sd_speed)
        lt_speed.addWidget(self.lb_sd_speed_value)

        lb_wt_cm = QLabel("Select width infini object (cm)")
        self.sd_wt_cm = QSlider(Qt.Horizontal, self)
        self.sd_wt_cm.setSizePolicy(size_policy)
        self.sd_wt_cm.setFixedWidth(285)
        self.sd_wt_cm.setMinimum(5)
        self.sd_wt_cm.setMaximum(40)
        self.sd_wt_cm.setSliderPosition(10)
        self.sd_wt_cm.valueChanged.connect(self.update_sd_wt_cm_value)
        self.lb_sd_wt_cm_value = QLabel()
        self.lb_sd_wt_cm_value.setSizePolicy(size_policy)
        self.lb_sd_wt_cm_value.setFixedWidth(15)
        self.lb_sd_wt_cm_value.setText(str(self.sd_wt_cm.value()))
        lt_wt_cm = QHBoxLayout()
        lt_wt_cm.addWidget(lb_wt_cm)
        lt_wt_cm.addWidget(self.sd_wt_cm)
        lt_wt_cm.addWidget(self.lb_sd_wt_cm_value)

        lb_ht_cm = QLabel("Select height infini object (cm)")
        self.sd_ht_cm = QSlider(Qt.Horizontal, self)
        self.sd_ht_cm.setSizePolicy(size_policy)
        self.sd_ht_cm.setFixedWidth(285)
        self.sd_ht_cm.setMinimum(5)
        self.sd_ht_cm.setMaximum(30)
        self.sd_ht_cm.setSliderPosition(20)
        self.sd_ht_cm.valueChanged.connect(self.update_sd_ht_cm_value)
        self.lb_sd_ht_cm_value = QLabel()
        self.lb_sd_ht_cm_value.setSizePolicy(size_policy)
        self.lb_sd_ht_cm_value.setFixedWidth(15)
        self.lb_sd_ht_cm_value.setText(str(self.sd_ht_cm.value()))
        lt_ht_cm = QHBoxLayout()
        lt_ht_cm.addWidget(lb_ht_cm)
        lt_ht_cm.addWidget(self.sd_ht_cm)
        lt_ht_cm.addWidget(self.lb_sd_ht_cm_value)

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
        self.sd_nb_cycle.setMaximum(20)
        self.sd_nb_cycle.setSliderPosition(5)
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

        bt_run = QPushButton("Run Infini")
        bt_run.clicked.connect(self.bt_call_run_infini)

        bt_run_record_target = QPushButton("Rec Target")
        bt_run_record_target.clicked.connect(lambda: self.bt_call_record_target(
            self.generate_foldername_rec(
                self.get_exercice_name(), 
                self.__connected_patient.get_codePatient()),
            self.generate_filename_rec(
                self.get_exercice_name(), 
                self.__connected_patient.get_codePatient())
            ))

        bt_run_record_pupil = QPushButton("Rec Pupil")
        bt_run_record_pupil.clicked.connect(lambda: self.bt_call_record_pupil(
            self.generate_foldername_rec(
                "Fixation", 
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
        self.lt.addLayout(lt_direction)
        self.lt.addLayout(lt_color)
        self.lt.addLayout(lt_size)
        self.lt.addLayout(lt_speed)
        self.lt.addLayout(lt_wt_cm)
        self.lt.addLayout(lt_ht_cm)
        self.lt.addLayout(lt_auto_stop)
        self.lt.addLayout(lt_nb_cycle)
        self.lt.addLayout(lt_bt_run_record)
        self.lt.addWidget(self.lb_rec_img)

        self.setLayout(self.lt)

    def get_exercice_name(self):
        if (self.cb_direction.currentIndex() == 0):
            # index==0 -> is_vertical=True
            return "InfiniteV"
        else:
            return "InfiniteH"

    def create_form_automatic_stop(self):
        if self.rb_false.isChecked():
            self.sd_nb_cycle.setEnabled(False)
        else:
            self.sd_nb_cycle.setEnabled(True)

    def update_sd_nb_cycle_value(self):
        self.lb_sd_nb_cycle_value.setText(str(self.sd_nb_cycle.value()))

    def update_sd_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_sd_speed_value(self):
        self.lb_sd_speed_value.setText(str(self.sd_speed.value()))

    def update_sd_wt_cm_value(self):
        self.lb_sd_wt_cm_value.setText(str(self.sd_wt_cm.value()))

    def update_sd_ht_cm_value(self):
        self.lb_sd_ht_cm_value.setText(str(self.sd_ht_cm.value()))

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
        if self.infinite is not None:
            self.infinite.close()
            self.infinite = None

    def bt_call_run_all(self):
        folder_recording_name = self.generate_foldername_rec(
            "Fixation", 
            self.__connected_patient.get_codePatient())

        file_recording_name = self.generate_filename_rec(
            "Fixation", 
            self.__connected_patient.get_codePatient())

        self.bt_call_run_infini()
        
        self.bt_call_record_target(folder_recording_name, file_recording_name)
        self.bt_call_record_pupil(folder_recording_name)

    def bt_call_run_infini(self):
        if self.__selected_config.get_name_config() != "None":
            self.infinite = Infinite(
                self.__calibration.get_pupilLabs().get_status(),
                self.lb_rec_img)

            if self.rb_false.isChecked():
                self.infinite.set_nb_cycle(10000)
                # define a high number represinting an infinite value
            else:
                self.infinite.set_nb_cycle(self.sd_nb_cycle.value())

            self.infinite.set_selected_config(self.__selected_config)
            self.infinite.set_speed(self.sd_speed.value()/1000)
            self.infinite.set_color(QColor(self.cb_color.currentData()))
            self.infinite.set_is_object_vertical(
                (self.cb_direction.currentIndex() == 1))
            # Based on if the object is displayed vertically or horizontally
            self.infinite.update_original_width_height_px()
            self.infinite.set_size_object_cm_from_config()
            self.infinite.set_ratio_pixel_cm()
            self.infinite.set_size(self.sd_size.value())
            self.infinite.scale_size()  # based on ratio_pixel_cm
            self.infinite.set_width_target_infini_cm(self.sd_wt_cm.value())
            self.infinite.set_height_target_infini_cm(self.sd_ht_cm.value())
            # based on ratio_pixel_cm and width_target_infini_object_cm
            self.infinite.scale_x()
            # based on ratio_pixel_cm and width_target_infini_object_cm
            self.infinite.scale_y()
            self.infinite.set_is_running(True)

            screen = QDesktopWidget().screenGeometry(1)
            self.infinite.setGeometry(screen)
            # self.infinite.showMaximized()
            self.infinite.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

    def bt_call_record_target(self, folder_recording_name, file_recording_name):
        if self.infinite is not None:
            if self.__connected_patient.get_codePatient() != "None":

                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(folder_recording_name + "/" + file_recording_name)
                csv_recorder.set_header()

                self.infinite.set_csv_recorder(csv_recorder)

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))

                self.infinite.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Start infini first")
            dlg.exec()
