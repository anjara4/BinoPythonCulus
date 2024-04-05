from PyQt5.QtWidgets import QDesktopWidget, QSlider, QPushButton, QButtonGroup
from PyQt5.QtWidgets import QSizePolicy, QWidget, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap

from infinite_exercice import Infinite
from parameters import Parameters
from file_folder_generation import Generation
from calibration import Calibration

from ui_customDialog import CustomDialog
from csv_recorder import CSV_recorder
from PyQt5.QtCore import pyqtSignal

class UI_infinite(QWidget):
    toggleSignal = pyqtSignal(bool)

    def __init__(self, connected_patient, selected_config, cam_left, cam_right, pupil_labs):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__cam_left = cam_left
        self.__cam_right = cam_right
        self.__pupil_labs = pupil_labs

        self.__infinite = None
        self.file_folder_gen = Generation()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.lb_rec_img = QLabel(self)
        self.lb_rec_img.setGeometry(10, 10, 50, 50)
        parameters = Parameters()
        self.pp_rec = QPixmap(parameters.image_recording)

        lb_mode = QLabel("Mode?")
        self.rb_mode_pupil = QRadioButton("Pupil", self)
        self.rb_mode_lens = QRadioButton("Lens", self)
        self.rb_mode_pupil.setChecked(False)
        self.rb_mode_lens.setChecked(False)

        self.rb_group_mode = QButtonGroup()
        self.rb_group_mode.addButton(self.rb_mode_pupil)
        self.rb_group_mode.addButton(self.rb_mode_lens)
        self.rb_group_mode.setExclusive(False)

        self.rb_mode_pupil.toggled.connect(self.mode_pupil)
        self.rb_mode_lens.toggled.connect(self.mode_lens)
        lt_mode = QHBoxLayout()
        lt_mode.addWidget(lb_mode)
        lt_mode.addWidget(self.rb_mode_pupil)
        lt_mode.addWidget(self.rb_mode_lens)

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

        lb_size = QLabel("Select target size (°)")
        self.sd_size = QSlider(Qt.Horizontal, self)
        self.sd_size.setSizePolicy(size_policy)
        self.sd_size.setFixedWidth(272)
        self.sd_size.setMinimum(3)
        self.sd_size.setMaximum(7)
        self.sd_size.setSliderPosition(5)
        self.sd_size.valueChanged.connect(self.update_sd_size_value)
        self.lb_sd_size_value = QLabel()
        self.lb_sd_size_value.setSizePolicy(size_policy)
        self.lb_sd_size_value.setFixedWidth(20)
        self.lb_sd_size_value.setText(str(self.sd_size.value()/10))
        lt_size = QHBoxLayout()
        lt_size.addWidget(lb_size)
        lt_size.addWidget(self.sd_size)
        lt_size.addWidget(self.lb_sd_size_value)

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

        lb_time_step = QLabel("Select time step (ms)")
        self.sd_time_step = QSlider(Qt.Horizontal, self)
        self.sd_time_step.setSizePolicy(size_policy)
        self.sd_time_step.setFixedWidth(268)
        self.sd_time_step.setMinimum(2)
        self.sd_time_step.setMaximum(15)
        self.sd_time_step.setSliderPosition(5)
        self.sd_time_step.valueChanged.connect(self.update_sd_time_step_value)
        self.lb_sd_time_step_value = QLabel()
        self.lb_sd_time_step_value.setSizePolicy(size_policy)
        self.lb_sd_time_step_value.setFixedWidth(24)
        self.lb_sd_time_step_value.setText(str(self.sd_time_step.value()*0.1))
        lt_time_step = QHBoxLayout()
        lt_time_step.addWidget(lb_time_step)
        lt_time_step.addWidget(self.sd_time_step)
        lt_time_step.addWidget(self.lb_sd_time_step_value)

        lb_auto_stop = QLabel("Automatic stop?")
        self.rb_true = QRadioButton("True", self)
        self.rb_false = QRadioButton("False", self)
        self.rb_false.setChecked(True)
        self.rb_false.toggled.connect(self.create_form_automatic_stop)
        lt_auto_stop = QHBoxLayout()
        lt_auto_stop.addWidget(lb_auto_stop)
        lt_auto_stop.addWidget(self.rb_true)
        lt_auto_stop.addWidget(self.rb_false)

        lb_nb_cycle_exo = QLabel("Nb infini cycle")
        self.sd_nb_cycle_exo = QSlider(Qt.Horizontal, self)
        self.sd_nb_cycle_exo.setSizePolicy(size_policy)
        self.sd_nb_cycle_exo.setFixedWidth(272)
        self.sd_nb_cycle_exo.setMinimum(1)
        self.sd_nb_cycle_exo.setMaximum(50)
        self.sd_nb_cycle_exo.setSliderPosition(10)
        self.sd_nb_cycle_exo.setEnabled(False)
        self.sd_nb_cycle_exo.valueChanged.connect(self.update_sd_nb_cycle_exo_value)
        self.lb_sd_nb_cycle_exo_value = QLabel()
        self.lb_sd_nb_cycle_exo_value.setSizePolicy(size_policy)
        self.lb_sd_nb_cycle_exo_value.setFixedWidth(15)
        self.lb_sd_nb_cycle_exo_value.setText(str(self.sd_nb_cycle_exo.value()))
        lt_nb_cycle_exo = QHBoxLayout()
        lt_nb_cycle_exo.addWidget(lb_nb_cycle_exo)
        lt_nb_cycle_exo.addWidget(self.sd_nb_cycle_exo)
        lt_nb_cycle_exo.addWidget(self.lb_sd_nb_cycle_exo_value)

        bt_start_pupilLabs = QPushButton("Run Pupil Capture")
        bt_start_pupilLabs.clicked.connect(self.start_pupilLabs)

        self.bt_start_calibration_pupilLabs = QPushButton("Calibration Pupil")
        self.bt_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)

        self.bt_start_calibration_lens = QPushButton("Calibration Lens")
        self.bt_start_calibration_lens.clicked.connect(self.start_calibration_lens)

        lt_bt_calibration = QHBoxLayout()
        lt_bt_calibration.addWidget(self.bt_start_calibration_pupilLabs)
        lt_bt_calibration.addWidget(self.bt_start_calibration_lens)

        self.bt_launch_infinite = QPushButton("Run Infini")
        self.bt_launch_infinite.clicked.connect(self.launch_infini)

        self.bt_rec_target = QPushButton("Rec Target")
        self.bt_rec_target.clicked.connect(lambda: self.rec_target(
            self.file_folder_gen.foldername_rec(
                self.get_exercice_name(), 
                self.__connected_patient.get_codePatient()),
            self.file_folder_gen.filename_rec(
                self.get_exercice_name(), 
                self.__connected_patient.get_codePatient(),
                "Target.csv"
                )
            )
        )

        self.bt_rec_pupil = QPushButton("Rec Pupil")
        self.bt_rec_pupil.clicked.connect(lambda: self.rec_pupil(
            self.file_folder_gen.foldername_rec(
                "Infini_Pupil", 
                self.__connected_patient.get_codePatient())
            )
        )

        self.bt_rec_lens = QPushButton("Rec Lens")
        self.bt_rec_lens.clicked.connect(lambda: self.rec_lens(
            self.file_folder_gen.foldername_rec(
                "Infini_Lens", 
                self.__connected_patient.get_codePatient()),
            self.file_folder_gen.filename_rec(
                "Infini_Lens", 
                self.__connected_patient.get_codePatient(),
                ""
                )
            )
        )

        self.bt_rec_target_pupil = QPushButton("Run Target/Pupil")
        self.bt_rec_target_pupil.clicked.connect(self.rec_target_pupil)

        self.bt_rec_target_lens = QPushButton("Run Target/Lens")
        self.bt_rec_target_lens.clicked.connect(self.rec_target_lens)

        bt_stop = QPushButton("Stop")
        bt_stop.clicked.connect(self.stop_all)

        lt_bt_rec = QHBoxLayout()
        lt_bt_rec.addWidget(self.bt_rec_target)
        lt_bt_rec.addWidget(self.bt_rec_pupil)
        lt_bt_rec.addWidget(self.bt_rec_target_pupil)
        lt_bt_rec.addWidget(self.bt_rec_lens)
        lt_bt_rec.addWidget(self.bt_rec_target_lens)        

        self.lt = QVBoxLayout()
        self.lt.addLayout(lt_color)
        self.lt.addLayout(lt_size)
        self.lt.addLayout(lt_direction)
        self.lt.addLayout(lt_time_step)
        self.lt.addLayout(lt_auto_stop)
        self.lt.addLayout(lt_nb_cycle_exo)
        self.lt.addWidget(bt_start_pupilLabs)
        self.lt.addWidget(self.bt_launch_infinite)
        self.lt.addLayout(lt_mode)
        self.lt.addLayout(lt_bt_rec)
        self.lt.addWidget(bt_stop)
        self.lt.addWidget(self.lb_rec_img)
        self.lt.addLayout(lt_bt_calibration)

        self.setLayout(self.lt)

    def start_pupilLabs(self):
        self.__pupil_labs.start_pupilLabs()

    def rec_video_calib_lens(self, cam, folder_recording_name, file_recording_name, position): 
        if cam is not None:
            cam.start_recording(
                folder_recording_name + "/" +
                file_recording_name + "_" + position)
        else:
            dlg = CustomDialog(message="Camera " + position + " Not available")
            dlg.exec()

    def start_calibration_pupilLabs(self):
        self.__pupil_labs.start_calibration()

    def calibration_window_closed(self):
        dlg = CustomDialog(message="Calibration done")
        dlg.exec() 
        self.bt_start_calibration_lens.setEnabled(True)
        self.__calibration.closed.disconnect(self.calibration_window_closed)  # Disconnect the signal
        
        if self.__cam_left is not None:
            self.__cam_left.stop_recording()
        
        if self.__cam_right is not None:
            self.__cam_right.stop_recording()

    def start_calibration_lens(self):
        if self.check_condition_all():
            if self.rb_mode_lens.isChecked():
                self.bt_start_calibration_lens.setEnabled(False)

                folder_recording_name = self.file_folder_gen.foldername_rec(
                        "Calibration_Lens", 
                        self.__connected_patient.get_codePatient())

                file_recording_name = self.file_folder_gen.filename_rec(
                        "Calibration_Lens", 
                        self.__connected_patient.get_codePatient(),
                        "")

                self.rec_video_calib_lens(self.__cam_left, folder_recording_name, file_recording_name, "left")
                self.rec_video_calib_lens(self.__cam_right, folder_recording_name, file_recording_name, "right")

                screen = QDesktopWidget().screenGeometry(1)
                parameters = Parameters()
                self.__calibration = Calibration(
                    int(parameters.size_object_calibration_lens),
                    self.__connected_patient.get_codePatient(),
                    folder_recording_name,
                    file_recording_name
                    )
                self.__calibration.closed.connect(self.calibration_window_closed)
                self.__calibration.setGeometry(screen)
                self.__calibration.showFullScreen()
            else: 
                dlg = CustomDialog(message="Check mode lens and refresh the camera")
                dlg.exec() 

    def check_condition_pupil(self):
        if self.__selected_config.get_name_config() != "None":
            is_ok_selected_config = True
        else:
            is_ok_selected_config = False
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

        if self.__connected_patient.get_codePatient() != "None":
            is_ok_connected_patient = True
        else:
            is_ok_connected_patient = False
            dlg = CustomDialog(message="Connect to a patient")
            dlg.exec()

        if self.__pupil_labs.get_status() is None:
            is_pupil_labs_on = False
            dlg = CustomDialog(message="Launch Pupil Labs")
            dlg.exec()
        else:
            is_pupil_labs_on = True

        return is_ok_selected_config and is_ok_connected_patient and is_pupil_labs_on

    def mode_pupil(self):
        if self.check_condition_pupil():
            if self.__pupil_labs.get_status() is None:
                self.rb_mode_pupil.setChecked(False)
                dlg = CustomDialog(message="PupilLab application not detected")
                dlg.exec() 
            else:
                if self.rb_mode_pupil.isChecked():
                    self.__pupil_labs.open_camera_eyes(0)
                    self.__pupil_labs.open_camera_eyes(1)

                    self.rb_mode_pupil.setChecked(True)
                    self.rb_mode_lens.setChecked(False)

                    self.bt_rec_pupil.setEnabled(True)
                    self.bt_rec_target_pupil.setEnabled(True)
                    self.bt_start_calibration_pupilLabs.setEnabled(True)

                    self.bt_rec_lens.setEnabled(False)
                    self.bt_rec_target_lens.setEnabled(False)
                    self.bt_start_calibration_lens.setEnabled(False)    

                    self.toggleSignal.emit(False)           
        else: 
            self.rb_mode_pupil.setChecked(False)

    def mode_lens(self):
        if self.check_condition_exo():
            if self.rb_mode_lens.isChecked():
                if self.__pupil_labs.get_status() is not None:
                    self.__pupil_labs.close_camera_eyes(0)
                    self.__pupil_labs.close_camera_eyes(1)

                dlg = CustomDialog(message="Mode lens activated \n Refresh the camera if it is frozen")
                dlg.exec()

                self.rb_mode_lens.setChecked(True)
                self.rb_mode_pupil.setChecked(False)

                self.bt_rec_lens.setEnabled(True)
                self.bt_rec_target_lens.setEnabled(True)
                self.bt_start_calibration_lens.setEnabled(True)
                    
                self.bt_rec_pupil.setEnabled(False)
                self.bt_rec_target_pupil.setEnabled(False)
                self.bt_start_calibration_pupilLabs.setEnabled(False)

                self.toggleSignal.emit(True)

                self.refresh_camera
        else: 
            self.rb_mode_lens.setChecked(False)

    def refresh_camera(self):
        self.refresh_camera_left()
        self.refresh_camera_right()        

    def refresh_camera_left(self):
        if self.__cam_left is not None:
            self.__cam_left.stop_recording()
            self.__cam_left.start_thread()

    def refresh_camera_right(self):
        if self.__cam_right is not None:
            self.__cam_right.stop_recording()
            self.__cam_right.start_thread()

    def get_exercice_name(self):
        if (self.cb_direction.currentIndex() == 0): # index==0 -> is_vertical=True
            return "InfiniteV_Target"
        else:
            return "InfiniteH_Target"

    def create_form_automatic_stop(self):
        if self.rb_false.isChecked():
            self.sd_nb_cycle_exo.setEnabled(False)
        else:
            self.sd_nb_cycle_exo.setEnabled(True)

    def update_sd_nb_cycle_exo_value(self):
        self.lb_sd_nb_cycle_exo_value.setText(str(self.sd_nb_cycle_exo.value()))

    def update_sd_size_value(self):
        self.lb_sd_size_value.setText(str(self.sd_size.value()/10))

    def update_sd_time_step_value(self):
        self.lb_sd_time_step_value.setText(str(self.sd_time_step.value()*0.1))

    def update_sd_wt_degree_value(self):
        self.lb_sd_wt_degree_value.setText(str(self.sd_wt_degree.value()))

    def update_sd_ht_degree_value(self):
        self.lb_sd_ht_degree_value.setText(str(self.sd_ht_degree.value()))

    def rec_pupil(self, folder_recording_name): 
        if self.check_condition_all():
            if self.__pupil_labs.get_status() is not None:
                self.__pupil_labs.start_record(folder_recording_name)

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))
            else:
                dlg = CustomDialog(message="Pupil Capture not detected")
                dlg.exec()

    def rec_target(self, folder_recording_name, file_recording_name):
        if self.__infinite is not None:
            if self.__connected_patient.get_codePatient() != "None":

                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(folder_recording_name + "/" + file_recording_name)
                csv_recorder.set_header()

                self.__infinite.set_csv_recorder(csv_recorder)

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))

                self.__infinite.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connect to a patient")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Start infini first")
            dlg.exec()

    def rec_lens(self, folder_recording_name, file_recording_name): 
        if self.check_condition_all():
            if self.__pupil_labs.get_status() is not None:
                self.__pupil_labs.close_camera_eyes(0)
                self.__pupil_labs.close_camera_eyes(1)

            if self.__cam_left is not None:
                self.__cam_left.start_recording(
                    folder_recording_name + "/" +
                    file_recording_name + "_left")

            if self.__cam_right is not None:
                self.__cam_right.start_recording(
                    folder_recording_name + "/" +
                    file_recording_name + "_right")

            self.lb_rec_img.setPixmap(
                self.pp_rec.scaled(
                    self.lb_rec_img.width(),
                    self.lb_rec_img.height(),
                    Qt.KeepAspectRatio))

    def rec_target_pupil(self):
        if self.check_condition_all():
            folder_recording_name = self.file_folder_gen.foldername_rec(
                "Infini_Pupil", 
                self.__connected_patient.get_codePatient())

            file_recording_name = self.file_folder_gen.filename_rec(
                "Infini_Pupil", 
                self.__connected_patient.get_codePatient(),
                "Target.csv")

            self.launch_infini()
            
            self.rec_target(folder_recording_name, file_recording_name)
            self.rec_pupil(folder_recording_name)

    def rec_target_lens(self):
        if self.check_condition_all():
            folder_recording_name = self.file_folder_gen.foldername_rec(
                "Infini_Lens", 
                self.__connected_patient.get_codePatient())

            file_recording_name = self.file_folder_gen.filename_rec(
                "Infini_Lens", 
                self.__connected_patient.get_codePatient(),
                "")

            self.launch_infini()
            
            self.rec_target(folder_recording_name, file_recording_name + "Target.csv")
            self.rec_lens(folder_recording_name, file_recording_name)

    def stop_all(self):
        if self.__pupil_labs.get_status() is not None:
            self.__pupil_labs.stop_record()

        self.lb_rec_img.clear()

        if self.__infinite is not None:
            self.__infinite.set_is_recording(False)
            self.__infinite.stop_exo()
            self.__infinite = None

        if self.__cam_left is not None:
            self.__cam_left.stop_recording()

        if self.__cam_right is not None:
            self.__cam_right.stop_recording()

    def check_condition_all(self):
        if self.__selected_config.get_name_config() != "None":
            is_ok_selected_config = True
        else:
            is_ok_selected_config = False
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

        if self.__connected_patient.get_codePatient() != "None":
            is_ok_connected_patient = True
        else:
            is_ok_connected_patient = False
            dlg = CustomDialog(message="Connect to a patient")
            dlg.exec()

        if self.rb_mode_lens.isChecked() or self.rb_mode_pupil.isChecked(): 
            is_ok_mode = True
        else:
            is_ok_mode = False
            dlg = CustomDialog(message="Select a mode")
            dlg.exec()

        return is_ok_selected_config and is_ok_connected_patient and is_ok_mode

    def check_condition_exo(self):
        if self.__selected_config.get_name_config() != "None":
            is_ok_selected_config = True
        else:
            is_ok_selected_config = False
            dlg = CustomDialog(message="Apply a config")
            dlg.exec()

        if self.__connected_patient.get_codePatient() != "None":
            is_ok_connected_patient = True
        else:
            is_ok_connected_patient = False
            dlg = CustomDialog(message="Connect to a patient")
            dlg.exec()

        return is_ok_selected_config and is_ok_connected_patient

    def launch_infini(self):
        self.stop_all()
        if self.check_condition_exo():
            self.__infinite = Infinite(
                self.__selected_config,
                self.lb_rec_img,
                self.__pupil_labs
                )

            if self.rb_false.isChecked():
                self.__infinite.set_nb_cycle_exo(1000)
                # define an high number represinting an infinite value
            else:
                self.__infinite.set_nb_cycle_exo(self.sd_nb_cycle_exo.value())

            self.__infinite.set_selected_config(self.__selected_config)
            self.__infinite.set_time_step(float(self.sd_time_step.value()))
            self.__infinite.set_color(QColor(self.cb_color.currentData()))
            self.__infinite.set_is_object_vertical(
                (self.cb_direction.currentIndex() == 1))
            # Based on if the object is displayed vertically or horizontally
            self.__infinite.update_original_width_height_px()
            self.__infinite.set_size_object_cm_from_config()
            self.__infinite.set_ratio_pixel_cm()
            self.__infinite.set_size(
                self.__infinite.degrees_to_cm(
                    float(self.lb_sd_size_value.text()
                    )
                ) 
            )
            self.__infinite.scale_size()  # based on ratio_pixel_cm

            screen = QDesktopWidget().screenGeometry(1)
            self.__infinite.setGeometry(screen)
            # self.infinite.showMaximized()
            self.__infinite.showFullScreen()
            self.__infinite.set_is_running(True)
