from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QRadioButton,QPushButton, QButtonGroup, QLabel, QDesktopWidget, QSizePolicy, QHBoxLayout, QComboBox, QSlider
from PyQt5.QtGui import QPixmap, QColor
from model.calibration import Calibration
from model.file_folder_generation import Generation
from parameters import Parameters
from view.ui_customDialog import CustomDialog
from model.csv_recorder import CSV_recorder
import os

class UI_exercise(QWidget):
    def __init__(self, connected_patient, selected_config, cam_left, cam_right, pupil_labs, exercise_name=None):
        super().__init__()
        self.parameters = Parameters()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.__pupil_labs = pupil_labs
        self.__cam_left = cam_left
        self.__cam_right = cam_right

        self.__exercise = None
        self.__exercise_name = exercise_name

        self.logMar_to_deg = self.parameters.logMar_to_deg_data
        self.file_folder_gen = Generation()

        self.size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #region Create a QLabel to display the recording status
        self.lb_rec_img = QLabel(self)
        self.lb_rec_img.setGeometry(10, 10, 50, 50)
        self.pp_rec = QPixmap(self.parameters.image_recording)

        self.lb_mode = QLabel("Mode")
        self.rb_mode_test = QRadioButton("Test", self)
        self.rb_mode_pupil = QRadioButton("Pupil", self)
        self.rb_mode_lens = QRadioButton("Lens", self)

        self.rb_mode_pupil.setChecked(False)
        self.rb_mode_lens.setChecked(False)
        self.rb_mode_test.setChecked(True)

        self.rb_group_mode = QButtonGroup()
        self.rb_group_mode.addButton(self.rb_mode_test)
        self.rb_group_mode.addButton(self.rb_mode_pupil)
        self.rb_group_mode.addButton(self.rb_mode_lens)
        self.rb_group_mode.setExclusive(True)

        self.rb_mode_test.toggled.connect(self.mode_test)
        self.rb_mode_pupil.toggled.connect(self.mode_pupil)
        self.rb_mode_lens.toggled.connect(self.mode_lens)

        self.lt_mode = QHBoxLayout()
        self.lt_mode.addWidget(self.lb_mode)
        self.lt_mode.addWidget(self.rb_mode_test)
        self.lt_mode.addWidget(self.rb_mode_pupil)
        self.lt_mode.addWidget(self.rb_mode_lens)
        self.lt_mode.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create a QLabel for Target color
        self.lb_color = QLabel("Select target color")
        self.cb_color = QComboBox()
        self.cb_color.setSizePolicy(self.size_policy)
        self.cb_color.setFixedWidth(300)
        self.cb_color.addItem("Black", QColor("black"))
        self.cb_color.addItem("Red", QColor("red"))
        self.cb_color.addItem("Blue", QColor("blue"))
        self.cb_color.setCurrentIndex(0)
        self.lt_color = QHBoxLayout()
        self.lt_color.addWidget(self.lb_color)
        self.lt_color.addWidget(self.cb_color)
        self.lt_color.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create a QLabel for Target size
        self.lb_size = QLabel("Select target size (logMar)")
        self.sd_size = QSlider(Qt.Horizontal, self)
        self.sd_size.setSizePolicy(self.size_policy)
        self.sd_size.setFixedWidth(255)
        self.sd_size.setMinimum(0)
        self.sd_size.setMaximum(13)
        self.sd_size.setSliderPosition(8)
        self.sd_size.valueChanged.connect(self.update_sd_size_value)
        self.lb_sd_size_value = QLabel()
        self.lb_sd_size_value.setSizePolicy(self.size_policy)
        self.lb_sd_size_value.setFixedWidth(30)
        self.lb_sd_size_value.setText(str(self.sd_size.value()/10))
        self.lt_size = QHBoxLayout()
        self.lt_size.addWidget(self.lb_size)
        self.lt_size.addWidget(self.sd_size)
        self.lt_size.addWidget(self.lb_sd_size_value)
        self.lt_size.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create Labels for lunching pupil labs and lens
        self.bt_start_pupilLabs = QPushButton("Start Pupil Capture")
        self.bt_start_pupilLabs.clicked.connect(self.start_pupilLabs)
        self.bt_start_pupilLabs.setEnabled(False)

        self.lt_bt_pupilLabs = QHBoxLayout()
        self.lt_bt_pupilLabs.addWidget(self.bt_start_pupilLabs)

        self.bt_start_calibration_pupilLabs = QPushButton("Calibration Pupil")
        self.bt_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)
        self.bt_start_calibration_pupilLabs.setEnabled(False)

        self.bt_start_calibration_lens = QPushButton("Calibration Lens")
        self.bt_start_calibration_lens.clicked.connect(self.start_calibration_lens)
        self.bt_start_calibration_lens.setEnabled(False)

        self.lt_bt_calibration = QHBoxLayout()
        self.lt_bt_calibration.addWidget(self.bt_start_calibration_pupilLabs)
        self.lt_bt_calibration.addWidget(self.bt_start_calibration_lens)
    
        self.bt_launch_exercise = QPushButton(f"Run {self.__exercise_name}")
        self.bt_launch_exercise.clicked.connect(self.launch_exercise)

        self.bt_rec_target_pupil = QPushButton(f"Run {self.__exercise_name}/Pupil")
        self.bt_rec_target_pupil.clicked.connect(self.rec_target_pupil)
        self.bt_rec_target_pupil.setEnabled(False)

        self.bt_rec_target_lens = QPushButton(f"Run {self.__exercise_name}/Lens")
        self.bt_rec_target_lens.clicked.connect(self.rec_target_lens)
        self.bt_rec_target_lens.setEnabled(False)

        self.bt_stop = QPushButton("Stop Run")
        self.bt_stop.clicked.connect(self.stop_all)           
        #endregion

    def calibration_window_closed(self):
        dlg = CustomDialog(message="Calibration done")
        dlg.exec() 
        self.bt_start_calibration_lens.setEnabled(True)
        self.__calibration.closed.disconnect(self.calibration_window_closed)  # Disconnect the signal
        
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
    
    def get_camera_left(self):
        return self.__cam_left
    
    def get_camera_right(self):
        return self.__cam_right
    
    def get_connected_patient(self):
        return self.__connected_patient

    def get_exercise(self):
        return self.__exercise

    def get_pupil_labs(self):
        return self.__pupil_labs
    
    def get_selected_config(self):
        return self.__selected_config

    def launch_exercise(self):
        pass

    def mode_lens(self):
        self.bt_launch_exercise.setEnabled(False)

        self.bt_start_pupilLabs.setEnabled(False)

        self.bt_rec_target_lens.setEnabled(True)
        self.bt_start_calibration_lens.setEnabled(True)
                    
        self.bt_rec_target_pupil.setEnabled(False)
        self.bt_start_calibration_pupilLabs.setEnabled(False)

        self.__pupil_labs.stop_pupilLabs()

        self.toggleSignal.emit(True)

        if self.rb_mode_lens.isChecked():
            dlg = CustomDialog(message="Refresh the camera if it is frozen")
            dlg.exec()
    
    def mode_pupil(self):
        self.bt_launch_exercise.setEnabled(False)

        self.bt_start_pupilLabs.setEnabled(True)

        self.bt_rec_target_pupil.setEnabled(True)
        self.bt_start_calibration_pupilLabs.setEnabled(True)

        self.bt_rec_target_lens.setEnabled(False)
        self.bt_start_calibration_lens.setEnabled(False)   

        if self.rb_mode_pupil.isChecked():
            dlg = CustomDialog(message="Do not forget to click on Start Pupil Capture")
            dlg.exec()

        self.toggleSignal.emit(False)  
    
    def mode_test(self):
        self.bt_launch_exercise.setEnabled(True)

        self.bt_start_pupilLabs.setEnabled(False)

        self.bt_rec_target_pupil.setEnabled(False)
        self.bt_start_calibration_pupilLabs.setEnabled(False)

        self.bt_rec_target_lens.setEnabled(False)
        self.bt_start_calibration_lens.setEnabled(False)   

        self.toggleSignal.emit(True) 

    def rec_description_text(self, type_exo, folder_recording_name, file_recording_name):
        self.file_folder_gen.decription_rec(
            folder_recording_name + "/",
            type_exo, 
            self.__connected_patient.get_codePatient(), 
            self.__selected_config.get_name_config(),
            self.sd_size.value()/10,
            ""
            )
        
    def rec_lens(self, folder_recording_name, file_recording_name): 
        if self.check_condition_all():
            self.__pupil_labs.stop_pupilLabs()

            self.rec_video_cam(folder_recording_name, file_recording_name)
            self.rec_description_text(f"{self.__exercise_name}_Lens", folder_recording_name, file_recording_name)

            self.lb_rec_img.setPixmap(
                self.pp_rec.scaled(
                    self.lb_rec_img.width(),
                    self.lb_rec_img.height(),
                    Qt.KeepAspectRatio))

    def rec_pupil(self, folder_recording_name, file_recording_name):
        if self.check_condition_all():
            if self.__pupil_labs.get_status() is not None:
                self.__pupil_labs.start_record(folder_recording_name)

                self.file_folder_gen.decription_rec(
                    folder_recording_name + "/",
                    f"{self.__exercise_name}_Pupil", 
                    self.__connected_patient.get_codePatient(), 
                    self.__selected_config.get_name_config(),
                    self.sd_size.value()/10,
                    ""
                    )

                self.rec_description_text(f"{self.__exercise_name}_Pupil", folder_recording_name, file_recording_name)
                self.rec_video_cam(os.getcwd(), "0000") #Fake recording for processing time purpose

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))
            else:
                dlg = CustomDialog(message="Pupil Capture not detected")
                dlg.exec()

    def rec_target(self, folder_recording_name, file_recording_name, is_clicked):
        if self.__exercise is not None:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(folder_recording_name + "/" + file_recording_name)
                csv_recorder.set_header()

                self.__exercise.set_csv_recorder(csv_recorder)

                self.file_folder_gen.decription_rec(
                    folder_recording_name + "/",
                    f"{self.__exercise_name}_Target", 
                    self.__connected_patient.get_codePatient(), 
                    self.__selected_config.get_name_config(),
                    self.sd_size.value()/10,
                    ""
                    )

                self.lb_rec_img.setPixmap(
                    self.pp_rec.scaled(
                        self.lb_rec_img.width(),
                        self.lb_rec_img.height(),
                        Qt.KeepAspectRatio))

                self.rec_description_text(f"{self.__exercise_name}_Target", folder_recording_name, file_recording_name)

                if is_clicked:
                    self.rec_video_cam(os.getcwd(), "0000") #Fake recording for processing time purpose

                self.__exercise.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connect to a patient")
                dlg.exec()
        else:
            dlg = CustomDialog(message=f"Start {self.__exercise_name} first")
            dlg.exec()

    def rec_target_lens(self):
        if self.check_condition_all():
            folder_recording_name = self.file_folder_gen.foldername_rec(
                f"{self.__exercise_name}_Lens", 
                self.__connected_patient.get_codePatient())

            file_recording_name = self.file_folder_gen.filename_rec(
                f"{self.__exercise_name}_Lens", 
                self.__connected_patient.get_codePatient(),
                "")

            self.launch_exercise()
            
            self.rec_target(folder_recording_name, file_recording_name + "Target.csv", False)
            self.rec_lens(folder_recording_name, file_recording_name)

    def rec_target_pupil(self):
        if self.check_condition_all():
            folder_recording_name = self.file_folder_gen.foldername_rec(
                f"{self.__exercise_name}_Pupil", 
                self.__connected_patient.get_codePatient())

            file_recording_name = self.file_folder_gen.filename_rec(
                f"{self.__exercise_name}_Pupil", 
                self.__connected_patient.get_codePatient(),
                "Target.csv")

            self.launch_exercise()
            
            self.rec_target(folder_recording_name, file_recording_name, False)
            self.rec_pupil(folder_recording_name, file_recording_name)

    def rec_video_calib_lens(self, cam, folder_recording_name, file_recording_name, position): 
        if cam is not None:
            cam.start_recording(
                folder_recording_name + "/" +
                file_recording_name + "_" + position)
        else:
            dlg = CustomDialog(message="Camera " + position + " Not available")
            dlg.exec()

    def rec_video_cam(self, folder_recording_name, file_recording_name):
        if self.__cam_left is not None:
            self.__cam_left.start_recording(
                folder_recording_name + "/" +
                file_recording_name  + "_left"
                )

        if self.__cam_right is not None:
            self.__cam_right.start_recording(
                folder_recording_name + "/" +
                file_recording_name  + "_right"
                )

    def set_exercise_name(self, name):
        self.__exercise_name = name

    def set_exercise(self, exercise):
        self.__exercise = exercise
    
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
    
    def start_calibration_pupilLabs(self):
        self.__pupil_labs.start_calibration()
        
    def start_pupilLabs(self):
        self.__pupil_labs.start_pupilLabs()

        self.__pupil_labs.open_camera_eyes(0)
        self.__pupil_labs.open_camera_eyes(1)

    def stop_all(self):
        if self.__pupil_labs.get_status() is not None:
            self.__pupil_labs.stop_record()
            
        self.lb_rec_img.clear()

        if self.__exercise is not None:
            self.__exercise.set_is_recording(False)
            self.__exercise.stop_exo()
            self.__exercise = None

        if self.__cam_left is not None:
            self.__cam_left.stop_recording()

        if self.__cam_right is not None:
            self.__cam_right.stop_recording()

    def stop_pupilLabs(self):
        self.__pupil_labs.stop_pupilLabs()

    def update_sd_size_value(self):
        self.lb_sd_size_value.setText(str(self.sd_size.value()/10))
    
    