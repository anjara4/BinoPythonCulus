from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget, QTableView, QHeaderView
from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel

import csv

from PyQt5.QtCore import pyqtSignal
from ui_customDialog import CustomDialog 
from csv_recorder import CSV_recorder
from datetime import datetime
import pandas as pd
from parameters import Parameters

class UI_main_patient(QWidget):
    def __init__(self, connected_patient):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__table_list_patient = QTableView()
     
        # Table will fit the screen horizontally
        self.__table_list_patient.horizontalHeader().setStretchLastSection(True)
        self.__table_list_patient.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        
        self.__table_list_patient.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        #self.__table_list_patient.verticalHeader().setVisible(False)
        #self.__table_list_patient.horizontalHeader().setVisible(False)
        self.__table_list_patient.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)


        parameters = Parameters()
        self.__data_patient = parameters.data_patient

        self.sub_tabs = QTabWidget()
        self.sub_tab_creation = Creation()
        self.sub_tab_connexion = Connexion(self.__table_list_patient)

        self.sub_tab_creation.createdPatientSignal.connect(self.connect_new_created_patient)
        
        self.sub_tab_data = Data()
        self.sub_tabs.addTab(self.sub_tab_creation, "Add Patient")
        self.sub_tabs.addTab(self.sub_tab_connexion, "List of Patients")
        #self.sub_tabs.addTab(self.sub_tab_data, "Data")

        self.sub_tab_connexion.bt_refresh.clicked.connect(self.refresh_patient)
        self.sub_tab_connexion.bt_connect.clicked.connect(self.connect_patient)
        self.sub_tab_connexion.bt_delete.clicked.connect(self.delete_patient)

        self.sub_tabs.currentChanged.connect(self.refresh_patient)

        self.sub_tabs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sub_tabs.setFixedWidth(600)
        
        lt = QHBoxLayout()
        lt.addStretch(1)
        lt.addWidget(self.sub_tabs)
        lt.addStretch(1)

        self.setLayout(lt)

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

    def connect_new_created_patient(self, code_new_patient):
        self.__connected_patient.set_codePatient(code_new_patient)

    def connect_patient(self):
        if self.check_if_row_is_selectioned(self.__table_list_patient.selectedIndexes()) and self.get_id_from_selected_row(index_code_patient=0)!='IdPatient':
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=0)
            self.__connected_patient.set_codePatient(code_patient_selected)
        elif self.get_id_from_selected_row(index_code_patient=0)=='IdPatient' :
            dlg = CustomDialog(message="Non-selectable row")
            dlg.exec()
        else:
            dlg = CustomDialog(message="Select a row before connecting")
            dlg.exec()

    def delete_patient(self):
        if self.check_if_row_is_selectioned(self.__table_list_patient.selectedIndexes()):
            code_patient_selected = self.get_id_from_selected_row(index_code_patient=0)
            if self.__connected_patient.get_codePatient() != code_patient_selected: 
                df = pd.read_csv(self.__data_patient, delimiter=';')
                df = df[df['IdPatient'] != code_patient_selected]
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

        lb_logged_in_as = QLabel("Connected patient: ")
        self.lb_logged_in_user = QLabel(self.__codePatient)
        self.lt_logged_in = QHBoxLayout()
        self.lt_logged_in.addWidget(lb_logged_in_as)
        self.lt_logged_in.addWidget(self.lb_logged_in_user)

    def set_codePatient(self, value):
        self.__codePatient = value
        self.lb_logged_in_user.setText(self.__codePatient)

    def get_codePatient(self):
        return self.__codePatient

class Creation(QWidget):
    createdPatientSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        #size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy = QSizePolicy()
        
        parameters = Parameters()
        self.__data_patient = parameters.data_patient

        self.lb_first_name = QLabel("*Enter ID patient:")
        self.le_first_name = QLineEdit()
        self.le_first_name.setSizePolicy(size_policy)
        self.le_first_name.setFixedWidth(300)
        lt_first_name = QHBoxLayout()
        lt_first_name.addWidget(self.lb_first_name)
        lt_first_name.addWidget(self.le_first_name)

        self.bt_save_patient = QPushButton("Save patient")
        self.bt_save_patient.clicked.connect(self.save_patient)

        self.lt = QVBoxLayout()
        self.lt.addLayout(lt_first_name)
        self.lt.addWidget(self.bt_save_patient)

        self.setLayout(self.lt)

    def save_patient_validator(self):
        if self.le_first_name.text() :
            return True
        else:
            return False

    def save_patient(self):
        if self.save_patient_validator():
            csv_recorder = CSV_recorder()
            csv_recorder.save_patient(self.__data_patient, 
                self.le_first_name.text(), 
                datetime.now().strftime('%d-%m-%Y'))
            
            dlg = CustomDialog(message="Patient saved in Data_conf/data_patient.csv")
            dlg.exec()

            self.createdPatientSignal.emit(self.le_first_name.text())
        else:
            dlg = CustomDialog(message="All the information are mandatory")
            dlg.exec()

class Connexion(QWidget):
    def __init__(self, table_list_patient):
        super().__init__()

        self.__table_list_patient = table_list_patient

        self.bt_refresh = QPushButton("Refresh")
        self.bt_connect = QPushButton("Connect")
        self.bt_delete = QPushButton("Delete")

        lt_vertical_bt = QHBoxLayout()
        lt_vertical_bt.addWidget(self.bt_refresh)
        lt_vertical_bt.addWidget(self.bt_connect)
        lt_vertical_bt.addWidget(self.bt_delete)

        #self.__table_list_patient.resizeColumnsToContents()

        lt_code_patient = QVBoxLayout()
        lt_code_patient.addLayout(lt_vertical_bt)
        lt_code_patient.addWidget(self.__table_list_patient)

        self.setLayout(lt_code_patient)

class CsvTableModel(QStandardItemModel):
    def __init__(self, data, parent=None):
        QStandardItemModel.__init__(self, parent)
        for line in data:
            self.appendRow([QStandardItem(item) for item in line])

class Data(QWidget):
    def __init__(self):
        super().__init__()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.lb_filter = QLabel("Select a filter")
        parameters = Parameters()
        self.__data_patient = parameters.data_patient
        
        self.cb_filter = QComboBox()
        self.cb_filter.setSizePolicy(size_policy)
        self.cb_filter.setFixedWidth(300)
        self.cb_filter.addItem("All", 0)
        self.cb_filter.addItem("Target", 1)
        self.load_patient_data()
        self.cb_filter.setCurrentIndex(0)
        
        self.bt_apply_filter = QPushButton("Apply")
        dir_path = '.'
        self.bt_apply_filter.clicked.connect(lambda: self.apply_filter(dir_path))

        lt_filter = QHBoxLayout()
        lt_filter.addWidget(self.lb_filter)
        lt_filter.addWidget(self.cb_filter)
        lt_filter.addWidget(self.bt_apply_filter)

        self.table = QTableView()

        #self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        lt = QVBoxLayout()
        lt.addLayout(lt_filter)
        lt.addWidget(self.table)        

        self.apply_filter(dir_path)

        self.setLayout(lt)

    def load_patient_data(self):
        with open(self.__data_patient, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            for row in reader:
                self.cb_filter.addItem(row[0])

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


        

