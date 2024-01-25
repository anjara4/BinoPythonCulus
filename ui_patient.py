from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget, QTableView
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem

import csv
import sys

from ui_exercice import UI_infinite
from ui_exercice import UI_fixation
from ui_exercice import UI_saccade
from ui_customDialog import CustomDialog 

from recording import CSV_recorder

from datetime import datetime

import pandas as pd

class UI_connected_patient(QWidget):
    def __init__(self):
        super().__init__()
        self.__codePatient = "None"

        label_logged_in_as = QLabel("Connected patient: ")
        self.label_logged_in_user = QLabel(self.__codePatient)
        self.layout_logged_in = QHBoxLayout()
        self.layout_logged_in.addWidget(label_logged_in_as)
        self.layout_logged_in.addWidget(self.label_logged_in_user)

    def set_codePatient(self, value):
        self.__codePatient = value
        self.label_logged_in_user.setText(self.__codePatient)

    def get_codePatient(self):
        return self.__codePatient

class UI_main_patient(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.sub_tabs = QTabWidget()
        self.sub_tab1 = Creation()
        self.sub_tab2 = Connexion(connected_patient)
        self.sub_tab3 = Data()
        self.sub_tabs.addTab(self.sub_tab1, "Creation")
        self.sub_tabs.addTab(self.sub_tab2, "Connexion")
        self.sub_tabs.addTab(self.sub_tab3, "Data")

        self.sub_tabs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sub_tabs.setFixedWidth(500)
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.sub_tabs)
        layout.addStretch(1)

        self.setLayout(layout)

class Creation(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.label_first_name = QLabel("Enter first name")
        self.line_edit_first_name = QLineEdit()
        self.line_edit_first_name.textChanged.connect(self.generate_code_patient)
        self.line_edit_first_name.setSizePolicy(size_policy)
        self.line_edit_first_name.setFixedWidth(300)
        layout_first_name = QHBoxLayout()
        layout_first_name.addWidget(self.label_first_name)
        layout_first_name.addWidget(self.line_edit_first_name)

        self.label_name = QLabel("Enter name")
        self.line_edit_name = QLineEdit()
        self.line_edit_name.textChanged.connect(self.generate_code_patient)
        self.line_edit_name.setSizePolicy(size_policy)
        self.line_edit_name.setFixedWidth(300)
        layout_name = QHBoxLayout()
        layout_name.addWidget(self.label_name)
        layout_name.addWidget(self.line_edit_name)

        self.label_date_of_birth = QLabel("Select date of birth")
        self.date_edit_date_of_birth = QDateEdit()
        self.date_edit_date_of_birth.dateChanged.connect(self.generate_code_patient)
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
        self.combo_box_sex.addItem("M", 0)
        self.combo_box_sex.addItem("F", 1)
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

    def generate_code_patient(self):
        if len(self.line_edit_first_name.text()[:2]) >= 2 and len(self.line_edit_first_name.text()[:2]) >= 2:
            self.line_edit_code_patient.setText(
            self.line_edit_first_name.text()[:2] + 
            self.line_edit_name.text()[:2] + 
            self.date_edit_date_of_birth.text()[-2:]
            )

    def save_patient(self):
        csv_recorder = CSV_recorder()
        csv_recorder.save_patient("data_patient.csv", 
            self.line_edit_first_name.text(), 
            self.line_edit_name.text(), 
            self.combo_box_sex.currentText(),
            self.date_edit_date_of_birth.text(), 
            self.line_edit_code_patient.text(),
            datetime.now().strftime('%d-%m-%Y'))

class Connexion(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__connected_patient = connected_patient

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.clicked.connect(self.connect_refresh)

        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.connect_patient)

        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.connect_delete)

        layout_vertical_button = QHBoxLayout()
        layout_vertical_button.addWidget(self.button_refresh)
        layout_vertical_button.addWidget(self.button_connect)
        layout_vertical_button.addWidget(self.button_delete)

        self.table = QTableView()
        self.connect_refresh()

        #self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        layout_code_patient = QVBoxLayout()
        layout_code_patient.addLayout(layout_vertical_button)
        layout_code_patient.addWidget(self.table)

        self.setLayout(layout_code_patient)

    def connect_refresh(self):
        self.model = self.get_model_data()
        self.table.setModel(self.model)

    def get_model_data(self):
        model = QStandardItemModel()
        with open('data_patient.csv', 'r') as file:
            for row in csv.reader(file, delimiter=';'):
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)
        return model

    def get_id_from_selected_row(self, index_code_patient):
        indexes = self.table.selectedIndexes()
        for index in indexes:
            row = index.row()
            column = index_code_patient #index.column()
            value = self.model.data(self.model.index(row, column))
            #print(f"({row}, {column} = {value}")
            return value

    def check_if_row_is_selectioned(self, indexes):
        return True if indexes else False

    def connect_patient(self):
        if self.check_if_row_is_selectioned(self.table.selectedIndexes()):
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=4)
            self.__connected_patient.set_codePatient(code_patient_selected)
        else:
            dlg = CustomDialog(message="Select a row before connecting")
            dlg.exec()

    def connect_delete(self):
        if self.check_if_row_is_selectioned(self.table.selectedIndexes()):
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=4)
            df = pd.read_csv('data_patient.csv', delimiter=';')
            df = df[df['CodePatient'] != code_patient_selected]
            df.to_csv('data_patient.csv', index=False, sep=';')
            dlg = CustomDialog(message="patient deleted" + str(code_patient_selected))
            dlg.exec()
            self.connect_refresh()#To refresh the dataview
        else:
            dlg = CustomDialog(message="Select a row before deleting")
            dlg.exec()

class Data(QWidget):
    def __init__(self):
        super().__init__()

        

