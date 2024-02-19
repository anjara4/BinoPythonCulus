from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from ui_saccade_exercice import UI_saccade
from ui_fixation_exercice import UI_fixation
from ui_infinite_exercice import UI_infinite

from cam_video_world import CameraLeft
from cam_video_world import CameraWrite
from ui_calibration import UI_calibration

class UI_main_excercice(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        self.ui_calibration = UI_calibration(self.__selected_config)

        sub_tabs = QTabWidget()
        sub_tab1 = UI_saccade(
                            self.__connected_patient,
                            self.__selected_config,
                            self.ui_calibration
                            )

        sub_tab2 = UI_fixation(
                            self.__connected_patient,
                            self.__selected_config,
                            self.ui_calibration
                            )

        sub_tab3 = UI_infinite(
                            self.__connected_patient,
                            self.__selected_config,
                            self.ui_calibration
                            )

        sub_tabs.addTab(sub_tab1, "Saccade")
        sub_tabs.addTab(sub_tab2, "Fixation")
        sub_tabs.addTab(sub_tab3, "Infini")

        # Create a label and line edit for the common interface for Calibration
        layout_exo = QVBoxLayout()
        layout_exo.addWidget(sub_tabs)
        layout_exo.addLayout(self.ui_calibration.layout_calibration)

        cam_left = CameraLeft()
        cam_write = CameraWrite()

        layout_camera = QHBoxLayout()
        layout_camera.addWidget(cam_left)
        layout_camera.addWidget(cam_write)

        layout = QHBoxLayout()
        layout.addLayout(layout_exo)
        layout.addLayout(layout_camera)

        self.setLayout(layout)
