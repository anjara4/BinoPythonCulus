from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui_exercice import UI_infinite
from ui_exercice import UI_fixation
from ui_exercice import UI_saccade

class UI_main_patient(QWidget):
    def __init__(self):
        super().__init__()
        self.sub_tabs = QTabWidget()
        self.sub_tab1 = UI_save_patient()
        self.sub_tab2 = UI_save_patient()
        self.sub_tab3 = UI_save_patient()
        self.sub_tabs.addTab(self.sub_tab1, "Creation")
        self.sub_tabs.addTab(self.sub_tab2, "Connexion")
        self.sub_tabs.addTab(self.sub_tab3, "Data")
        
        layout = QVBoxLayout()
        layout.addWidget(self.sub_tabs)

        self.setLayout(layout)

class UI_save_patient(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.label_first_name = QLabel("Enter first name")
        self.line_edit_first_name = QLineEdit()
        self.line_edit_first_name.setSizePolicy(size_policy)
        self.line_edit_first_name.setFixedWidth(300)
        layout_first_name = QHBoxLayout()
        layout_first_name.addWidget(self.label_first_name)
        layout_first_name.addWidget(self.line_edit_first_name)

        self.label_name = QLabel("Enter name")
        self.line_edit_name = QLineEdit()
        self.line_edit_name.setSizePolicy(size_policy)
        self.line_edit_name.setFixedWidth(300)
        layout_name = QHBoxLayout()
        layout_name.addWidget(self.label_name)
        layout_name.addWidget(self.line_edit_name)

        self.label_date_of_birth = QLabel("Select date of birth")
        self.date_edit_date_of_birth = QDateEdit()
        self.date_edit_date_of_birth.setSizePolicy(size_policy)
        self.date_edit_date_of_birth.setFixedWidth(300)
        self.date_edit_date_of_birth.setDisplayFormat("dd-MM-yyyy")
        self.date_edit_date_of_birth.setCalendarPopup(True)
        layout_date_of_birth = QHBoxLayout()
        layout_date_of_birth.addWidget(self.label_date_of_birth)
        layout_date_of_birth.addWidget(self.date_edit_date_of_birth)

        self.label_sex = QLabel("Select sex")
        self.combo_box_sex = QComboBox()
        self.combo_box_sex.setSizePolicy(size_policy)
        self.combo_box_sex.setFixedWidth(300)
        self.combo_box_sex.addItem("M")
        self.combo_box_sex.addItem("F")
        self.combo_box_sex.setCurrentIndex(0)
        layout_sex = QHBoxLayout()
        layout_sex.addWidget(self.label_sex)
        layout_sex.addWidget(self.combo_box_sex)

        self.label_code_patient = QLabel("Code patient (generate)")
        self.line_edit_code_patient = QLineEdit()
        self.line_edit_code_patient.setSizePolicy(size_policy)
        self.line_edit_code_patient.setFixedWidth(300)
        self.line_edit_code_patient.setReadOnly(True)
        self.line_edit_code_patient.setStyleSheet("background-color: lightgray;")
        layout_code_patient = QHBoxLayout()
        layout_code_patient.addWidget(self.label_code_patient)
        layout_code_patient.addWidget(self.line_edit_code_patient)

        self.button_save_patient = QPushButton("Save patient")
        self.button_save_patient.clicked.connect(self.save_patient)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_first_name)
        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_date_of_birth)
        self.layout.addLayout(layout_sex)
        self.layout.addLayout(layout_code_patient)
        self.layout.addWidget(self.button_save_patient)

        self.setLayout(self.layout)

    def save_patient(self):
        text = self.line_edit.text()
        print(f"Text submitted: {text}")


class TabPatient(QWidget):
    def __init__(self):
        super().__init__()
        self.sub_tabs = QTabWidget()
        self.sub_tab1 = UI_patient()
        self.sub_tab2 = UI_patient()
        self.sub_tab3 = UI_patient()
        self.sub_tabs.addTab(self.sub_tab1, "Creation")
        self.sub_tabs.addTab(self.sub_tab2, "Connexion")
        self.sub_tabs.addTab(self.sub_tab3, "Data")
        
        layout = QVBoxLayout()
        layout.addWidget(self.sub_tabs)

        self.setLayout(layout)
        

