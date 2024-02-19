from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QSizePolicy, QWidget, QRadioButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap

from fixation_exercice import Fixation

from ui_customDialog import CustomDialog
from recording import CSV_recorder
from recording import PupilLabs_recorder

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
        self.lb_rec_img = QLabel(self)
        self.lb_rec_img.setGeometry(10, 10, 50, 50)
        self.pp_rec = QPixmap('record_icon.png')

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

        lb_hor_pos = QLabel("Select delta X from center (cm)")
        self.sd_hor_pos = QSlider(Qt.Horizontal, self)
        self.sd_hor_pos.setSizePolicy(size_policy)
        self.sd_hor_pos.setFixedWidth(282)
        self.sd_hor_pos.setMinimum(-20)
        self.sd_hor_pos.setMaximum(20)
        self.sd_hor_pos.setSliderPosition(0)
        self.sd_hor_pos.valueChanged.connect(self.update_sd_hor_pos_value)
        self.lb_sd_hor_pos_value = QLabel()
        self.lb_sd_hor_pos_value.setSizePolicy(size_policy)
        self.lb_sd_hor_pos_value.setFixedWidth(18)
        self.lb_sd_hor_pos_value.setText(str(self.sd_hor_pos.value()))
        lt_hor_pos = QHBoxLayout()
        lt_hor_pos.addWidget(lb_hor_pos)
        lt_hor_pos.addWidget(self.sd_hor_pos)
        lt_hor_pos.addWidget(self.lb_sd_hor_pos_value)

        lb_ver_pos = QLabel("Select delta y from center (cm)")
        self.sd_ver_pos = QSlider(Qt.Horizontal, self)
        self.sd_ver_pos.setSizePolicy(size_policy)
        self.sd_ver_pos.setFixedWidth(282)
        self.sd_ver_pos.setMinimum(-20)
        self.sd_ver_pos.setMaximum(20)
        self.sd_ver_pos.setSliderPosition(0)
        self.sd_ver_pos.valueChanged.connect(self.update_sd_ver_pos_value)
        self.lb_sd_ver_pos_value = QLabel()
        self.lb_sd_ver_pos_value.setSizePolicy(size_policy)
        self.lb_sd_ver_pos_value.setFixedWidth(18)
        self.lb_sd_ver_pos_value.setText(str(self.sd_ver_pos.value()))
        lt_ver_pos = QHBoxLayout()
        lt_ver_pos.addWidget(lb_ver_pos)
        lt_ver_pos.addWidget(self.sd_ver_pos)
        lt_ver_pos.addWidget(self.lb_sd_ver_pos_value)

        bt_run = QPushButton("Run Fixation")
        bt_run.clicked.connect(self.bt_call_run_fixation)

        bt_record_target = QPushButton("Rec Target")
        bt_record_target.clicked.connect(self.bt_call_record_target)

        bt_record_pupil = QPushButton("Rec Pupil")
        bt_record_pupil.clicked.connect(self.bt_call_record_pupil)

        bt_run_all = QPushButton("Run All")
        bt_run_all.clicked.connect(self.bt_call_run_all)

        bt_stop = QPushButton("Stop")
        bt_stop.clicked.connect(self.bt_call_stop)

        lb_auto_stop = QLabel("Automatic stop?")
        self.rb_true = QRadioButton("True", self)
        self.rb_false = QRadioButton("False", self)
        self.rb_false.setChecked(True)
        self.rb_false.toggled.connect(self.create_form_automatic_stop)
        lt_auto_stop = QHBoxLayout()
        lt_auto_stop.addWidget(lb_auto_stop)
        lt_auto_stop.addWidget(self.rb_true)
        lt_auto_stop.addWidget(self.rb_false)

        lb_time_exo = QLabel("Duration (s)")
        self.sd_time_exo = QSlider(Qt.Horizontal, self)
        self.sd_time_exo.setSizePolicy(size_policy)
        self.sd_time_exo.setFixedWidth(285)
        self.sd_time_exo.setMinimum(1)
        self.sd_time_exo.setMaximum(100)
        self.sd_time_exo.setSliderPosition(10)
        self.sd_time_exo.setEnabled(False)
        self.sd_time_exo.valueChanged.connect(self.update_sd_time_exo_value)
        self.lb_sd_time_exo_value = QLabel()
        self.lb_sd_time_exo_value.setSizePolicy(size_policy)
        self.lb_sd_time_exo_value.setFixedWidth(15)
        self.lb_sd_time_exo_value.setText(str(self.sd_time_exo.value()))
        lt_time_exo = QHBoxLayout()
        lt_time_exo.addWidget(lb_time_exo)
        lt_time_exo.addWidget(self.sd_time_exo)
        lt_time_exo.addWidget(self.lb_sd_time_exo_value)

        lt_bt_run_record = QHBoxLayout()
        lt_bt_run_record.addWidget(bt_run)
        lt_bt_run_record.addWidget(bt_record_target)
        lt_bt_run_record.addWidget(bt_record_pupil)
        lt_bt_run_record.addWidget(bt_run_all)
        lt_bt_run_record.addWidget(bt_stop)

        self.lt = QVBoxLayout()
        self.lt.addLayout(lt_color)
        self.lt.addLayout(lt_size)
        self.lt.addLayout(lt_hor_pos)
        self.lt.addLayout(lt_ver_pos)
        self.lt.addLayout(lt_auto_stop)
        self.lt.addLayout(lt_time_exo)
        self.lt.addLayout(lt_bt_run_record)
        self.lt.addWidget(self.lb_rec_img)

        self.setLayout(self.lt)

    def create_form_automatic_stop(self):
        if self.rb_false.isChecked():
            self.sd_time_exo.setEnabled(False)
        else:
            self.sd_time_exo.setEnabled(True)

    def update_sd_time_exo_value(self):
        self.lb_sd_time_exo_value.setText(str(self.sd_time_exo.value()))

    def update_sd_size_value(self):
        self.lb_sd_size_value.setText(str(self.sd_size.value()))

    def update_sd_ver_pos_value(self):
        self.lb_sd_ver_pos_value.setText(str(self.sd_ver_pos.value()))

    def update_sd_hor_pos_value(self):
        self.lb_sd_hor_pos_value.setText(str(self.sd_hor_pos.value()))

    def bt_call_run_all(self):
        self.bt_call_run_fixation()
        self.bt_call_record_target()
        self.bt_call_record_pupil()

    def bt_call_record_pupil(self):
        self.pupilLabs_recorder.start_record_pupilLab(
            self.__calibration.get_pupilLabs().get_status())

    def bt_call_stop(self):
        self.pupilLabs_recorder.stop_record_pupilLab(
            self.__calibration.get_pupilLabs().get_status())
        self.lb_rec_img.clear()
        if self.fixation is not None:
            self.fixation.close()
            self.fixation = None

    def bt_call_run_fixation(self):
        self.fixation = Fixation(
            self.__calibration.get_pupilLabs().get_status(),
            self.lb_rec_img)
        if self.__selected_config.get_name_config() != "None":
            self.fixation.set_is_running(True)
            self.fixation.set_selected_config(self.__selected_config)
            self.fixation.set_color(QColor(self.cb_color.currentData()))
            self.fixation.set_ratio_pixel_cm()
            self.fixation.set_size(self.sd_size.value())
            self.fixation.set_hor_pos(self.sd_hor_pos.value())
            self.fixation.scale_hor_pos()
            self.fixation.set_ver_pos(self.sd_ver_pos.value())
            self.fixation.scale_ver_pos()

            if self.rb_false.isChecked():
                self.fixation.set_time_exo(10000)
                # define a high number represinting an infinite value
            else:
                self.fixation.set_time_exo(self.sd_time_exo.value())

            screen = QDesktopWidget().screenGeometry(1)
            self.fixation.setGeometry(screen)
            # self.fixation.showMaximized()
            self.fixation.showFullScreen()
        else:
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

    def bt_call_record_target(self):
        if self.fixation is not None:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(
                    csv_recorder.generate_filename(
                        self.__connected_patient.get_codePatient(),
                        "Fixation"))
                csv_recorder.set_header()

                self.fixation.set_csv_recorder(csv_recorder)

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))

                self.fixation.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()
