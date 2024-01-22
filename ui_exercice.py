from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from exercice import Infinite
from recording import Object_recorder

class UI_main_excercice(QWidget):
    def __init__(self):
        super().__init__()

        # Create a sub-tab widget
        sub_tabs = QTabWidget()
        sub_tab1 = UI_saccade()
        sub_tab2 = UI_fixation()
        sub_tab3 = UI_infinite()
        sub_tabs.addTab(sub_tab1, "Saccade")
        sub_tabs.addTab(sub_tab2, "Fixation")
        sub_tabs.addTab(sub_tab3, "Infini")

        # Create a label and line edit for the common interface
        self.button_start_calibration_pupilLabs = QPushButton("Pupil")
        self.button_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)

        self.button_start_calibration_lens = QPushButton("Lens")
        self.button_start_calibration_lens.clicked.connect(self.start_calibration_lens)

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_calibration = QHBoxLayout()
        layout_calibration.addWidget(self.button_start_calibration_pupilLabs)
        layout_calibration.addWidget(self.button_start_calibration_lens)
        group_box_calibration = QGroupBox("Calibration")
        group_box_calibration.setLayout(layout_calibration)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording)

        # Create a layout for the common interface
        layout = QVBoxLayout()
        # Add the sub-tab widget to the layout
        layout.addWidget(sub_tabs)
        layout.addWidget(group_box_calibration)
        layout.addWidget(group_box_recording)
        

        # Set the layout for the tab
        self.setLayout(layout)

    def start_calibration_pupilLabs(self):
        text = self.line_edit.text()
        print(f"Text submitted: {text}")

    def start_calibration_lens(self):
        text = self.line_edit.text()
        print(f"Text submitted: {text}")

    def start_recording(self):
        recorder = Object_recorder('positions.csv')
        recorder.record_position(10, 20)
        recorder.record_position(30, 40)

    def stop_recording(self):
        text = self.line_edit.text()
        print(f"Text submitted: {text}")

class UI_saccade(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_object = QLabel("Select object")
        combo_box_object = QComboBox()
        combo_box_object.setSizePolicy(size_policy)
        combo_box_object.setFixedWidth(300)
        combo_box_object.addItem("Circle")
        combo_box_object.addItem("Square")
        combo_box_object.setCurrentIndex(0)
        layout_object = QHBoxLayout()
        layout_object.addWidget(label_object)
        layout_object.addWidget(combo_box_object)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Red")
        combo_box_color.addItem("Blue")
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
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        label_delta_horizontal = QLabel("Delta horizontal")
        slider_delta_horizontal = QSlider(Qt.Horizontal, self)
        slider_delta_horizontal.setSizePolicy(size_policy)
        slider_delta_horizontal.setFixedWidth(300)
        slider_delta_horizontal.setMinimum(0)
        slider_delta_horizontal.setMaximum(100)
        slider_delta_horizontal.setSliderPosition(50)
        layout_delta_horizontal = QHBoxLayout()
        layout_delta_horizontal.addWidget(label_delta_horizontal)
        layout_delta_horizontal.addWidget(slider_delta_horizontal)

        label_delta_vertical = QLabel("Delta vertical")
        slider_delta_vertical = QSlider(Qt.Horizontal, self)
        slider_delta_vertical.setSizePolicy(size_policy)
        slider_delta_vertical.setFixedWidth(300)
        slider_delta_vertical.setMinimum(0)
        slider_delta_vertical.setMaximum(100)
        slider_delta_vertical.setSliderPosition(50)
        layout_delta_vertical = QHBoxLayout()
        layout_delta_vertical.addWidget(label_delta_vertical)
        layout_delta_vertical.addWidget(slider_delta_vertical)

        button_start_exercice_saccade = QPushButton("Start")
        button_start_exercice_saccade.clicked.connect(self.start_exercice_saccade)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_object)
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_delta_horizontal)
        self.layout.addLayout(layout_delta_vertical)
        self.layout.addWidget(button_start_exercice_saccade)

        self.setLayout(self.layout)

    def start_exercice_saccade(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("text")


class UI_fixation(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_object = QLabel("Select object")
        combo_box_object = QComboBox()
        combo_box_object.setSizePolicy(size_policy)
        combo_box_object.setFixedWidth(300)
        combo_box_object.addItem("Circle")
        combo_box_object.addItem("Square")
        combo_box_object.setCurrentIndex(0)
        layout_object = QHBoxLayout()
        layout_object.addWidget(label_object)
        layout_object.addWidget(combo_box_object)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Red")
        combo_box_color.addItem("Blue")
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
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        label_horizontal_position = QLabel("Select horizontal position")
        slider_horizontal_position = QSlider(Qt.Horizontal, self)
        slider_horizontal_position.setSizePolicy(size_policy)
        slider_horizontal_position.setFixedWidth(300)
        slider_horizontal_position.setMinimum(0)
        slider_horizontal_position.setMaximum(100)
        slider_horizontal_position.setSliderPosition(50)
        layout_horizontal_position = QHBoxLayout()
        layout_horizontal_position.addWidget(label_horizontal_position)
        layout_horizontal_position.addWidget(slider_horizontal_position)

        label_vertical_position = QLabel("Select vertical position")
        slider_vertical_position = QSlider(Qt.Horizontal, self)
        slider_vertical_position.setSizePolicy(size_policy)
        slider_vertical_position.setFixedWidth(300)
        slider_vertical_position.setMinimum(0)
        slider_vertical_position.setMaximum(100)
        slider_vertical_position.setSliderPosition(50)
        layout_vertical_position = QHBoxLayout()
        layout_vertical_position.addWidget(label_vertical_position)
        layout_vertical_position.addWidget(slider_vertical_position)

        button_start_exercice_fixation = QPushButton("Start")
        button_start_exercice_fixation.clicked.connect(self.start_exercice_fixation)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_object)
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_horizontal_position)
        self.layout.addLayout(layout_vertical_position)
        self.layout.addWidget(button_start_exercice_fixation)

        self.setLayout(self.layout)

    def start_exercice_fixation(self):
        text = self.line_edit.text()
        print(f"Text submitted: {text}")

class UI_infinite(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_direction = QLabel("Select direction")
        combo_box_direction = QComboBox()
        combo_box_direction.setSizePolicy(size_policy)
        combo_box_direction.setFixedWidth(300)
        combo_box_direction.addItem("Vertical")
        combo_box_direction.addItem("Horizontal")
        combo_box_direction.setCurrentIndex(0)
        layout_direction = QHBoxLayout()
        layout_direction.addWidget(label_direction)
        layout_direction.addWidget(combo_box_direction)

        label_object = QLabel("Select object")
        combo_box_object = QComboBox()
        combo_box_object.setSizePolicy(size_policy)
        combo_box_object.setFixedWidth(300)
        combo_box_object.addItem("Circle")
        combo_box_object.addItem("Square")
        combo_box_object.setCurrentIndex(0)
        layout_object = QHBoxLayout()
        layout_object.addWidget(label_object)
        layout_object.addWidget(combo_box_object)

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
            (combo_box_direction.currentIndex() == 0),#index==0 -> is_vertical=True
            slider_horizontal_scale.value(),
            slider_vertical_scale.value(),
                ))

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_direction)
        self.layout.addLayout(layout_object)
        self.layout.addLayout(layout_color) 
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_speed)
        self.layout.addLayout(layout_horizontal_scale)
        self.layout.addLayout(layout_vertical_scale)
        self.layout.addWidget(button_start_exercice_infini)

        self.setLayout(self.layout)

    def start_exercice_infini(self, speed, size, color, is_vertical, horizontal_scale, vertical_scale):
        self.infinite = Infinite()
        self.infinite.object_speed = speed/1000 #the slider only return integer value
        self.infinite.object_size = size
        self.infinite.object_color = color
        self.infinite.object_is_vertical = is_vertical
        self.infinite.x_scaler_position = horizontal_scale
        self.infinite.y_scaler_position = vertical_scale
        screen = QDesktopWidget().screenGeometry(1)
        self.infinite.setGeometry(screen)
        self.infinite.showMaximized()

