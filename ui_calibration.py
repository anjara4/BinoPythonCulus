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
        slider_size = QSlider(Qt.Horizontal, self)
        slider_size.setSizePolicy(size_policy)
        slider_size.setFixedWidth(300)
        slider_size.setMinimum(100)
        slider_size.setMaximum(400)
        slider_size.setSliderPosition(100)
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(slider_size)

        self.button_start_calibration_pupilLabs = QPushButton("Pupil")
        self.button_start_calibration_pupilLabs.clicked.connect(self.start_calibration_pupilLabs)

        self.button_start_calibration_lens = QPushButton("Lens")
        self.button_start_calibration_lens.clicked.connect(lambda: self.start_calibration_lens(slider_size.value()))

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.button_start_calibration_pupilLabs)
        layout_button.addWidget(self.button_start_calibration_lens)
        
        layout_calibration = QVBoxLayout()
        layout_calibration.addLayout(layout_size)
        layout_calibration.addLayout(layout_button)

        self.group_box_calibration = QGroupBox("Calibration")
        self.group_box_calibration.setLayout(layout_calibration)

    def start_calibration_pupilLabs(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("pupilLabs")

    def start_calibration_lens(self, size):
        screen = QDesktopWidget().screenGeometry(1)
        self.calibration = Calibration()
        self.calibration.set_size(size)
        self.calibration.setGeometry(screen)
        self.calibration.showMaximized()

