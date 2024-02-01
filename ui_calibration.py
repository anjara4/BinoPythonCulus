from PyQt5.QtWidgets import QDesktopWidget, QWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt

from calibration import Calibration

class UI_calibration(QWidget):
    def __init__(self):
        super().__init__()
        
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label_size = QLabel("Select size")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(300)
        self.slider_size.setMaximum(400)
        self.slider_size.setSliderPosition(100)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        self.button_start_calibration_pupilLabs = QPushButton("Pupil")
        self.button_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)

        self.button_start_calibration_lens = QPushButton("Lens")
        self.button_start_calibration_lens.clicked.connect(lambda: self.start_calibration_lens(self.slider_size.value()))

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.button_start_calibration_pupilLabs)
        layout_button.addWidget(self.button_start_calibration_lens)
        
        layout_calibration = QVBoxLayout()
        layout_calibration.addLayout(layout_size)
        layout_calibration.addLayout(layout_button)

        self.group_box_calibration = QGroupBox("Calibration")
        self.group_box_calibration.setLayout(layout_calibration)

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def start_calibration_pupilLabs(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("pupilLabs")

    def start_calibration_lens(self, size):
        screen = QDesktopWidget().screenGeometry(1)
        self.calibration = Calibration(size)
        self.calibration.setGeometry(screen)
        self.calibration.showMaximized()

