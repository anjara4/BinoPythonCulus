from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui_exercice import UI_main_excercice
from ui_patient import UI_main_patient
from ui_patient import UI_connected_patient
from ui_configuration import UI_main_configuration
from ui_visualisation import UI_main_visualisation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binoculus")

        connected_patient = UI_connected_patient()

        # Create a tab widget
        tabs = QTabWidget()
        tab1 = UI_main_patient(connected_patient)
        tab2 = UI_main_configuration()
        tab3 = UI_main_excercice(connected_patient)
        tab4 = UI_main_visualisation()
        tabs.addTab(tab1, "Patient")
        tabs.addTab(tab2, "Configuration")
        tabs.addTab(tab3, "Exercice")
        tabs.addTab(tab4, "Visualisation")

        layout_main = QVBoxLayout()
        layout_main.addLayout(connected_patient.layout_logged_in)
        layout_main.addWidget(tabs)

        widget_main = QWidget()
        widget_main.setLayout(layout_main)
    
        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(widget_main)

        self.resize(600, 400)

app = QApplication([])
w = MainWindow()
w.show()
app.exec()
