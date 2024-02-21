from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget, QTableView
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel

import csv
import sys
import glob
import os

from ui_customDialog import CustomDialog 
from recording import CSV_recorder
from datetime import datetime
import pandas as pd
from parameters import Parameters

class UI_main_patient(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__table_list_patient = QTableView()
        parameters = Parameters()
        self.__data_patient = parameters.data_patient

        self.sub_tabs = QTabWidget()
        self.sub_tab_creation = Creation()
        self.sub_tab_connexion = Connexion(self.__table_list_patient)
        self.sub_tab_data = Data()
        self.sub_tabs.addTab(self.sub_tab_creation, "Creation")
        self.sub_tabs.addTab(self.sub_tab_connexion, "Connexion")
        #self.sub_tabs.addTab(self.sub_tab_data, "Data")

        self.sub_tab_connexion.button_refresh.clicked.connect(self.refresh_patient)
        self.sub_tab_connexion.button_connect.clicked.connect(self.connect_patient)
        self.sub_tab_connexion.button_delete.clicked.connect(self.delete_patient)

        self.sub_tabs.currentChanged.connect(self.refresh_patient)

        self.sub_tabs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sub_tabs.setFixedWidth(600)
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.sub_tabs)
        layout.addStretch(1)

        self.setLayout(layout)

    def refresh_patient(self):
        model = self.get_model_data()
        self.__table_list_patient.setModel(model)

    def get_model_data(self):
        model = QStandardItemModel()
        with open(self.__data_patient, 'r') as file:
            for row in csv.reader(file, delimiter=';'):
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)
        return model

    def get_id_from_selected_row(self, index_code_patient):
        indexes = self.__table_list_patient.selectedIndexes()
        model = self.get_model_data()
        for index in indexes:
            row = index.row()
            column = index_code_patient #index.column()
            value = model.data(model.index(row, column))
            #print(f"({row}, {column} = {value}")
            return value

    def check_if_row_is_selectioned(self, indexes):
        return True if indexes else False

    def connect_patient(self):
        if self.check_if_row_is_selectioned(self.__table_list_patient.selectedIndexes()):
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=4)
            self.__connected_patient.set_codePatient(code_patient_selected)
        else:
            dlg = CustomDialog(message="Select a row before connecting")
            dlg.exec()

    def delete_patient(self):
        if self.check_if_row_is_selectioned(self.__table_list_patient.selectedIndexes()):
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=4)
            if self.__connected_patient.get_codePatient() != code_patient_selected: 
                df = pd.read_csv(self.__data_patient, delimiter=';')
                df = df[df['CodePatient'] != code_patient_selected]
                df.to_csv(self.__data_patient, index=False, sep=';')
                dlg = CustomDialog(message="Patient deleted: " + str(code_patient_selected))
                dlg.exec()
                self.refresh_patient()#To refresh the dataview
            else:
                dlg = CustomDialog(message="Impossible to delete a connected patient: " + str(code_patient_selected))
                dlg.exec()
        else:
            dlg = CustomDialog(message="Select a row before deleting")
            dlg.exec()

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

class Creation(QWidget):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.label_first_name = QLabel("*Enter first name")
        self.line_edit_first_name = QLineEdit()
        self.line_edit_first_name.textChanged.connect(self.generate_code_patient)
        self.line_edit_first_name.setSizePolicy(size_policy)
        self.line_edit_first_name.setFixedWidth(300)
        layout_first_name = QHBoxLayout()
        layout_first_name.addWidget(self.label_first_name)
        layout_first_name.addWidget(self.line_edit_first_name)

        self.label_name = QLabel("*Enter name")
        self.line_edit_name = QLineEdit()
        self.line_edit_name.textChanged.connect(self.generate_code_patient)
        self.line_edit_name.setSizePolicy(size_policy)
        self.line_edit_name.setFixedWidth(300)
        layout_name = QHBoxLayout()
        layout_name.addWidget(self.label_name)
        layout_name.addWidget(self.line_edit_name)

        self.label_date_of_birth = QLabel("*Select date of birth")
        self.date_edit_date_of_birth = QDateEdit()
        self.date_edit_date_of_birth.dateChanged.connect(self.generate_code_patient)
        self.date_edit_date_of_birth.setSizePolicy(size_policy)
        self.date_edit_date_of_birth.setFixedWidth(300)
        self.date_edit_date_of_birth.setDisplayFormat("dd-MM-yyyy")
        self.date_edit_date_of_birth.setCalendarPopup(True)
        layout_date_of_birth = QHBoxLayout()
        layout_date_of_birth.addWidget(self.label_date_of_birth)
        layout_date_of_birth.addWidget(self.date_edit_date_of_birth)

        self.label_sex = QLabel("*Select sex")
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
    def save_patient_validator(self):
        if self.line_edit_first_name.text() and self.line_edit_name.text() and  self.line_edit_code_patient.text():
            return True
        else:
            return False

    def save_patient(self):
        if self.save_patient_validator():
            csv_recorder = CSV_recorder()
            csv_recorder.save_patient(self.__data_patient, 
                self.line_edit_first_name.text(), 
                self.line_edit_name.text(), 
                self.combo_box_sex.currentText(),
                self.date_edit_date_of_birth.text(), 
                self.line_edit_code_patient.text(),
                datetime.now().strftime('%d-%m-%Y'))
            dlg = CustomDialog(message="Patient saved in Data_conf/data_patient.csv")
            dlg.exec()
        else:
            dlg = CustomDialog(message="All the information are mandatory")
            dlg.exec()

class Connexion(QWidget):
    def __init__(self, table_list_patient):
        super().__init__()
        self.__table_list_patient = table_list_patient

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.button_refresh = QPushButton("Refresh")
        self.button_connect = QPushButton("Connect")
        self.button_delete = QPushButton("Delete")

        layout_vertical_button = QHBoxLayout()
        layout_vertical_button.addWidget(self.button_refresh)
        layout_vertical_button.addWidget(self.button_connect)
        layout_vertical_button.addWidget(self.button_delete)

        #self.table.resizeRowsToContents()
        self.__table_list_patient.resizeColumnsToContents()

        layout_code_patient = QVBoxLayout()
        layout_code_patient.addLayout(layout_vertical_button)
        layout_code_patient.addWidget(self.__table_list_patient)

        self.setLayout(layout_code_patient)

class CsvTableModel(QStandardItemModel):
    def __init__(self, data, parent=None):
        QStandardItemModel.__init__(self, parent)
        for line in data:
            self.appendRow([QStandardItem(item) for item in line])

class Data(QWidget):
    def __init__(self):
        super().__init__()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.label_filter = QLabel("Select a filter")
        parameters = Parameters()
        self.__data_patient = parameters.data_patient
        
        self.combo_box_filter = QComboBox()
        self.combo_box_filter.setSizePolicy(size_policy)
        self.combo_box_filter.setFixedWidth(300)
        self.combo_box_filter.addItem("All", 0)
        self.combo_box_filter.addItem("Target", 1)
        self.load_patient_data()
        self.combo_box_filter.setCurrentIndex(0)
        
        self.button_apply_filter = QPushButton("Apply")
        dir_path = '.'
        self.button_apply_filter.clicked.connect(lambda: self.apply_filter(dir_path))

        layout_filter = QHBoxLayout()
        layout_filter.addWidget(self.label_filter)
        layout_filter.addWidget(self.combo_box_filter)
        layout_filter.addWidget(self.button_apply_filter)

        self.table = QTableView()

        #self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addLayout(layout_filter)
        layout.addWidget(self.table)        

        self.apply_filter(dir_path)

        self.setLayout(layout)

    def load_patient_data(self):
        with open(self.__data_patient, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                self.combo_box_filter.addItem(row[4])

    def apply_filter(self, dir_path):
        #files = glob.glob(os.path.join(dir_path, '*.csv')) #'*MaSu*.csv'
        #model = CsvTableModel(files)

        model = self.get_model_data('*')
        self.table.setModel(model)
        self.table.setRootIndex(model.index(dir_path))

    def get_model_data(self, select):
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        model.setNameFilters([select + '.csv'])
        model.setNameFilterDisables(False)
        return model


        

