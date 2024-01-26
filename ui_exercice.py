from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from exercice import Infinite
from exercice import Saccade
from exercice import Fixation

from ui_customDialog import CustomDialog 
from recording import CSV_recorder
from cam_video_world import CameraWorld
from ui_calibration import UI_calibration

class UI_main_excercice(QWidget):
    def __init__(self, connected_patient):
        super().__init__()

        # Create a sub-tab widget
        sub_tabs = QTabWidget()
        sub_tab1 = UI_saccade(connected_patient)
        sub_tab2 = UI_fixation(connected_patient)
        sub_tab3 = UI_infinite(connected_patient)
        sub_tabs.addTab(sub_tab1, "Saccade")
        sub_tabs.addTab(sub_tab2, "Fixation")
        sub_tabs.addTab(sub_tab3, "Infini")

        # Create a label and line edit for the common interface for Calibration
        self.ui_calibration = UI_calibration()

        layout_exo = QVBoxLayout()
        layout_exo.addWidget(sub_tabs)
        layout_exo.addWidget(self.ui_calibration.group_box_calibration)
        
        cam_world = CameraWorld()

        layout = QHBoxLayout()
        layout.addLayout(layout_exo)
        layout.addWidget(cam_world)
        
        self.setLayout(layout)

class UI_saccade(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__is_button_start_saccade_on = False
        self.saccade = Saccade()
        self.__connected_patient = connected_patient

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        slider_size = QSlider(Qt.Horizontal, self)
        slider_size.setSizePolicy(size_policy)
        slider_size.setFixedWidth(300)
        slider_size.setMinimum(0)
        slider_size.setMaximum(100)
        slider_size.setSliderPosition(50)
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        label_time_step = QLabel("Select time step")
        slider_time_step = QSlider(Qt.Horizontal, self)
        slider_time_step.setSizePolicy(size_policy)
        slider_time_step.setFixedWidth(300)
        slider_time_step.setMinimum(100)
        slider_time_step.setMaximum(5000)
        slider_time_step.setSliderPosition(1000)
        layout_time_step = QHBoxLayout()
        layout_time_step.addWidget(label_time_step)
        layout_time_step.addWidget(slider_time_step)

        label_delta_horizontal = QLabel("Delta horizontal")
        slider_delta_horizontal = QSlider(Qt.Horizontal, self)
        slider_delta_horizontal.setSizePolicy(size_policy)
        slider_delta_horizontal.setFixedWidth(300)
        slider_delta_horizontal.setMinimum(0)
        slider_delta_horizontal.setMaximum(1000)
        slider_delta_horizontal.setSliderPosition(0)
        layout_delta_horizontal = QHBoxLayout()
        layout_delta_horizontal.addWidget(label_delta_horizontal)
        layout_delta_horizontal.addWidget(slider_delta_horizontal)

        label_delta_vertical = QLabel("Delta vertical")
        slider_delta_vertical = QSlider(Qt.Horizontal, self)
        slider_delta_vertical.setSizePolicy(size_policy)
        slider_delta_vertical.setFixedWidth(300)
        slider_delta_vertical.setMinimum(0)
        slider_delta_vertical.setMaximum(1000)
        slider_delta_vertical.setSliderPosition(200)
        layout_delta_vertical = QHBoxLayout()
        layout_delta_vertical.addWidget(label_delta_vertical)
        layout_delta_vertical.addWidget(slider_delta_vertical)

        button_start_exercice_saccade = QPushButton("Start")
        button_start_exercice_saccade.clicked.connect(lambda: self.start_exercice_saccade(slider_size.value(), 
            QColor(combo_box_color.currentData()), 
            slider_time_step.value(), 
            slider_delta_horizontal.value(), 
            slider_delta_vertical.value()
            ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_time_step)
        self.layout.addLayout(layout_delta_horizontal)
        self.layout.addLayout(layout_delta_vertical)
        self.layout.addWidget(button_start_exercice_saccade)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def start_exercice_saccade(self, size, color, time_step, delta_horizontal, delta_vertical):
        self.saccade.set_is_running(True)
        self.saccade.set_size(size)
        self.saccade.set_color(color)
        self.saccade.set_time_step(time_step) 
        self.saccade.set_delta_horizontal(delta_horizontal)
        self.saccade.set_delta_vertical(delta_vertical)
        
        screen = QDesktopWidget().screenGeometry(1)
        self.saccade.setGeometry(screen)
        self.saccade.showMaximized()
        self.__is_button_start_saccade_on = True

    def start_recording(self):
        if self.__is_button_start_saccade_on:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Saccade"))

                self.saccade.set_csv_recorder(csv_recorder)
                self.saccade.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

    def stop_recording(self):
        self.saccade.set_is_recording(False)

class UI_fixation(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__is_button_start_fixation_on = False
        self.fixation = Fixation()
        self.__connected_patient = connected_patient

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        slider_size = QSlider(Qt.Horizontal, self)
        slider_size.setSizePolicy(size_policy)
        slider_size.setFixedWidth(300)
        slider_size.setMinimum(100)
        slider_size.setMaximum(1000)
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        label_horizontal_position = QLabel("Select horizontal position")
        slider_horizontal_position = QSlider(Qt.Horizontal, self)
        slider_horizontal_position.setSizePolicy(size_policy)
        slider_horizontal_position.setFixedWidth(300)
        slider_horizontal_position.setMinimum(0)
        slider_horizontal_position.setMaximum(1000)
        slider_horizontal_position.setSliderPosition(0)
        layout_horizontal_position = QHBoxLayout()
        layout_horizontal_position.addWidget(label_horizontal_position)
        layout_horizontal_position.addWidget(slider_horizontal_position)

        label_vertical_position = QLabel("Select vertical position")
        slider_vertical_position = QSlider(Qt.Horizontal, self)
        slider_vertical_position.setSizePolicy(size_policy)
        slider_vertical_position.setFixedWidth(300)
        slider_vertical_position.setMinimum(0)
        slider_vertical_position.setMaximum(1000)
        slider_vertical_position.setSliderPosition(0)
        layout_vertical_position = QHBoxLayout()
        layout_vertical_position.addWidget(label_vertical_position)
        layout_vertical_position.addWidget(slider_vertical_position)

        button_start_exercice_fixation = QPushButton("Start")
        button_start_exercice_fixation.clicked.connect(lambda: self.start_exercice_fixation(
            QColor(combo_box_color.currentData()),
            slider_size.value(),
            slider_horizontal_position.value(),
            slider_vertical_position.value()
            ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_horizontal_position)
        self.layout.addLayout(layout_vertical_position)
        self.layout.addWidget(button_start_exercice_fixation)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def start_exercice_fixation(self, color, size, horizontal_position, vertical_position):
        self.fixation.set_is_running(True)
        self.fixation.set_color(color)
        self.fixation.set_size(size)
        self.fixation.set_horizontal_position(horizontal_position)
        self.fixation.set_vertical_position(vertical_position)
        screen = QDesktopWidget().screenGeometry(1)
        self.fixation.setGeometry(screen)
        self.fixation.showMaximized()
        self.__is_button_start_fixation_on = True

    def start_recording(self):
        if self.__is_button_start_fixation_on:
            if self.__connected_patient.get_codePatient() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Fixation"))

                self.fixation.set_csv_recorder(csv_recorder)
                self.fixation.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

    def stop_recording(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("test")

class UI_infinite(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__is_button_start_infinite_on = False
        self.infinite = Infinite()
        self.__connected_patient = connected_patient

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_direction = QLabel("Select direction")
        self.combo_box_direction = QComboBox()
        self.combo_box_direction.setSizePolicy(size_policy)
        self.combo_box_direction.setFixedWidth(300)
        self.combo_box_direction.addItem("Vertical")
        self.combo_box_direction.addItem("Horizontal")
        self.combo_box_direction.setCurrentIndex(0)
        layout_direction = QHBoxLayout()
        layout_direction.addWidget(label_direction)
        layout_direction.addWidget(self.combo_box_direction)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        slider_size = QSlider(Qt.Horizontal, self)
        slider_size.setSizePolicy(size_policy)
        slider_size.setFixedWidth(300)
        slider_size.setMinimum(1)
        slider_size.setMaximum(100)
        slider_size.setSliderPosition(50)
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        label_speed = QLabel("Select speed")
        slider_speed = QSlider(Qt.Horizontal, self)
        slider_speed.setSizePolicy(size_policy)
        slider_speed.setFixedWidth(300)
        slider_speed.setMinimum(10)
        slider_speed.setMaximum(200)
        layout_speed = QHBoxLayout()
        layout_speed.addWidget(label_speed)
        layout_speed.addWidget(slider_speed)

        label_horizontal_scale = QLabel("Select horizontal scale")
        slider_horizontal_scale = QSlider(Qt.Horizontal, self)
        slider_horizontal_scale.setSizePolicy(size_policy)
        slider_horizontal_scale.setFixedWidth(300)
        slider_horizontal_scale.setMinimum(1)
        slider_horizontal_scale.setMaximum(40)
        slider_horizontal_scale.setSliderPosition(10)
        layout_horizontal_scale = QHBoxLayout()
        layout_horizontal_scale.addWidget(label_horizontal_scale)
        layout_horizontal_scale.addWidget(slider_horizontal_scale)

        label_vertical_scale = QLabel("Select vertical scale")
        slider_vertical_scale = QSlider(Qt.Horizontal, self)
        slider_vertical_scale.setSizePolicy(size_policy)
        slider_vertical_scale.setFixedWidth(300)
        slider_vertical_scale.setMinimum(1)
        slider_vertical_scale.setMaximum(40)
        slider_vertical_scale.setSliderPosition(10)
        layout_vertical_scale = QHBoxLayout()
        layout_vertical_scale.addWidget(label_vertical_scale)
        layout_vertical_scale.addWidget(slider_vertical_scale)

        button_start_exercice_infini = QPushButton("Start")
        button_start_exercice_infini.clicked.connect(lambda: self.start_exercice_infini(
            slider_speed.value(), 
            slider_size.value(), 
            QColor(combo_box_color.currentData()),
            (self.combo_box_direction.currentIndex() == 0),#index==0 -> is_vertical=True
            slider_horizontal_scale.value(),
            slider_vertical_scale.value(),
                ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_direction)
        self.layout.addLayout(layout_color) 
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_speed)
        self.layout.addLayout(layout_horizontal_scale)
        self.layout.addLayout(layout_vertical_scale)
        self.layout.addWidget(button_start_exercice_infini)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def start_exercice_infini(self, speed, size, color, is_vertical, horizontal_scale, vertical_scale):
        self.infinite.set_is_running(True)
        self.infinite.set_speed(speed/1000) #the slider only return integer value
        self.infinite.set_size(size)
        self.infinite.set_color(color)
        self.infinite.set_is_object_vertical(is_vertical)
        self.infinite.set_x_scaler(horizontal_scale)
        self.infinite.set_y_scaler(vertical_scale)
        screen = QDesktopWidget().screenGeometry(1)
        self.infinite.setGeometry(screen)
        self.infinite.showMaximized()
        self.__is_button_start_infinite_on = True

    def start_recording(self):
        if self.__is_button_start_infinite_on:
            if self.__connected_patient.get_codePatient() != "None":
                if (self.combo_box_direction.currentIndex() == 0):#index==0 -> is_vertical=True
                    exercice_name = "InfiniteV"
                else:
                    exercice_name = "InfiniteH"

                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), exercice_name))

                self.infinite.set_csv_recorder(csv_recorder)
                self.infinite.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient")
                dlg.exec()    
        else: 
            dlg = CustomDialog(message="Start infini first")
            dlg.exec()

    def stop_recording(self):
        self.infinite.set_is_recording(False)

