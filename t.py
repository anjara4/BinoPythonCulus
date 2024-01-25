from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from cam_video_world import CameraWorld


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        # Create a label and line edit for the common interface
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start_video)

        self.button_stop = QPushButton("Stop")
        self.button_stop.clicked.connect(self.stopt_video)

        layout = QHBoxLayout()
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_stop)
        
        self.cam_world = CameraWorld()

        layout_all = QHBoxLayout()
        # Add the sub-tab widget to the layout
        layout_all.addLayout(layout)
        layout_all.addWidget(self.cam_world)
        
        widget_main = QWidget()
        widget_main.setLayout(layout_all)

        #self.setLayout(layout_all)
    
        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(widget_main)

        self.resize(600, 400)

    def start_video(self):
        self.cam_world.start_thread()
        

    def stopt_video(self):
        #text = self.line_edit.text()
        #print(f"Text submitted: {text}")
        print("test")

app = QApplication([])
w = MainWindow()
w.show()
app.exec()

