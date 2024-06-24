from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

from ui_saccade_exercice import UI_saccade
from ui_fixation_exercice import UI_fixation
from ui_infinite_exercice import UI_infinite

from ui_customDialog import CustomDialog

from pupil_labs import Pupil_labs
from cam_video import Camera

class UI_main_excercice(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        self.__pupil_labs = Pupil_labs(self.__selected_config)

        self.__pupil_labs.stop_pupilLabs()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lb_exposure_time = QLabel("Select exposure time")
        #lb_exposure_time.setSizePolicy(size_policy)
        #lb_exposure_time.setFixedWidth(150)
        self.sd_exposure_time = QSlider(Qt.Horizontal, self)
        self.sd_exposure_time.setFixedWidth(285)
        self.sd_exposure_time.setMinimum(1)
        self.sd_exposure_time.setMaximum(32)
        self.sd_exposure_time.setSliderPosition(8)
        #self.sd_exposure_time.setSizePolicy(size_policy)
        #self.sd_exposure_time.setFixedWidth(150)
        self.sd_exposure_time.valueChanged.connect(self.update_sd_exposure_time_value)
        self.lb_sd_exposure_time_value = QLabel()
        self.lb_sd_exposure_time_value.setText(str(self.sd_exposure_time.value()))
        self.bt_apply_exposure_time = QPushButton("Apply")
        self.bt_apply_exposure_time.clicked.connect(self.set_exposure_time)

        lt_exposure_time = QHBoxLayout()
        lt_exposure_time.addWidget(self.lb_exposure_time)
        lt_exposure_time.addWidget(self.sd_exposure_time)
        lt_exposure_time.addWidget(self.lb_sd_exposure_time_value)
        lt_exposure_time.addWidget(self.bt_apply_exposure_time)

        self.__cam_left = Camera(self.sd_exposure_time.value(), 1)
        self.__cam_right = Camera(self.sd_exposure_time.value(), 0)

        self.lb_desc_cam_left = QLabel("Left Eye")
        self.lb_desc_cam_right = QLabel("Right Eye")

        lt_desc_cam_left = QHBoxLayout()
        lt_desc_cam_left.addStretch(1)
        lt_desc_cam_left.addWidget(self.lb_desc_cam_left)
        lt_desc_cam_left.addStretch(1)

        lt_desc_cam_right = QHBoxLayout()
        lt_desc_cam_right.addStretch(1)
        lt_desc_cam_right.addWidget(self.lb_desc_cam_right)
        lt_desc_cam_right.addStretch(1)

        lt_cam_left = QVBoxLayout()
        lt_cam_left.addWidget(self.__cam_left.image)
        lt_cam_left.addLayout(lt_desc_cam_left)

        lt_cam_right = QVBoxLayout()
        lt_cam_right.addWidget(self.__cam_right.image)
        lt_cam_right.addLayout(lt_desc_cam_right)

        lt_cam = QHBoxLayout()
        lt_cam.addLayout(lt_cam_left)
        lt_cam.addLayout(lt_cam_right)

        self.bt_refresh_camera = QPushButton("Refresh Camera")
        self.bt_refresh_camera.clicked.connect(self.refresh_camera_main)
        self.bt_refresh_camera.setSizePolicy(size_policy)
        self.bt_refresh_camera.setFixedWidth(150)

        lt_refresh_camera = QHBoxLayout()
        lt_refresh_camera.addStretch(1)
        lt_refresh_camera.addWidget(self.bt_refresh_camera)
        lt_refresh_camera.addStretch(1)

        lt_window_right = QVBoxLayout()
        lt_window_right.addLayout(lt_exposure_time)
        lt_window_right.addLayout(lt_refresh_camera)
        lt_window_right.addLayout(lt_cam)

        sub_tabs = QTabWidget()
        
        self.sub_tab_fixation = UI_fixation(
                            self.__connected_patient,
                            self.__selected_config,
                            self.__cam_left,
                            self.__cam_right,
                            self.__pupil_labs
                            )

        self.sub_tab_infinite = UI_infinite(
                            self.__connected_patient,
                            self.__selected_config,
                            self.__cam_left,
                            self.__cam_right,
                            self.__pupil_labs
                            )
        
        self.sub_tab_saccade = UI_saccade(
                            self.__connected_patient,
                            self.__selected_config,
                            self.__cam_left,
                            self.__cam_right,
                            self.__pupil_labs
                            )
        
        self.sub_tab_fixation.toggleSignal.connect(self.toggle_is_mode_pupil_fixation)
        self.sub_tab_infinite.toggleSignal.connect(self.toggle_is_mode_pupil_infinite)
        self.sub_tab_saccade.toggleSignal.connect(self.toggle_is_mode_pupil_saccade)

        sub_tabs.addTab(self.sub_tab_fixation, "Fixation")
        sub_tabs.addTab(self.sub_tab_infinite, "Infini")
        sub_tabs.addTab(self.sub_tab_saccade, "Saccade")


        lt_exo = QVBoxLayout()
        lt_exo.addWidget(sub_tabs)

        lt = QHBoxLayout()
        lt.addLayout(lt_exo)
        lt.addLayout(lt_window_right)

        self.toggle_is_mode(False)

        self.setLayout(lt)

    def toggle_is_mode(self, enabled):
        self.lb_exposure_time.setEnabled(enabled)
        self.sd_exposure_time.setEnabled(enabled)
        self.lb_sd_exposure_time_value.setEnabled(enabled)
        self.bt_apply_exposure_time.setEnabled(enabled)
        #self.__cam_left.image.setEnabled(enabled)
        #self.__cam_right.image.setEnabled(enabled)
        self.bt_refresh_camera.setEnabled(enabled)
        self.lb_desc_cam_left.setEnabled(enabled)
        self.lb_desc_cam_right.setEnabled(enabled)

        if enabled: 
            self.refresh_camera_main()

    def toggle_is_mode_pupil_saccade(self, enabled):
        self.toggle_is_mode(enabled)

    def toggle_is_mode_pupil_fixation(self, enabled):
        self.toggle_is_mode(enabled)

    def toggle_is_mode_pupil_infinite(self, enabled):
        self.toggle_is_mode(enabled)

    def refresh_camera_main(self):
        self.refresh_cam(self.__cam_left)
        self.refresh_cam(self.__cam_right)        

    def refresh_cam(self, cam):
        if cam is not None:
            cam.stop_recording()
            cam.start_thread()

            cap = cam.get_cap()
            if cap is not None:
                cam.set_exposure_time_camera(
                    cap,
                    self.sd_exposure_time.value()
                    )

    def set_exposure_time(self):
        if self.__cam_left is not None:
            self.__cam_left.set_exposure_time_camera(
                self.__cam_left.get_cap(), 
                self.sd_exposure_time.value()
                )

        if self.__cam_right is not None:
            self.__cam_right.set_exposure_time_camera(
                self.__cam_right.get_cap(),
                self.sd_exposure_time.value()
                )

    def update_sd_exposure_time_value(self):
        self.lb_sd_exposure_time_value.setText(
            str(self.sd_exposure_time.value()))
