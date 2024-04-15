from PyQt5.QtWidgets import QWidget, QTabWidget, QTableView, QDesktopWidget, QFileDialog
from PyQt5.QtWidgets import QSizePolicy, QDateEdit, QLabel, QGroupBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QLocale

import csv
import pandas as pd

from PyQt5.QtCore import pyqtSignal

from ui_customDialog import CustomDialog 
from csv_recorder import CSV_recorder
from datetime import datetime
from screen_calibration import Screen_calibration
from parameters import Parameters

class UI_main_configuration(QWidget):
    def __init__(self, selected_config):
        super().__init__()

        self.__selected_config = selected_config
        self.__table_list_config = QTableView()
        self.__table_list_config.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        self.__model_data_config = QStandardItemModel()

        parameters = Parameters()
        self.__data_configuration = parameters.data_configuration

        self.sub_tabs = QTabWidget()
        self.sub_tab_creation = Creation()
        self.sub_select_config = Select_config(self.__selected_config, self.__table_list_config)
        self.sub_tabs.addTab(self.sub_tab_creation, "Creation")
        self.sub_tabs.addTab(self.sub_select_config, "SelectConfig")

        self.sub_tab_creation.createdConfigSignal.connect(self.connect_new_created_config)

        self.sub_tabs.currentChanged.connect(self.refresh_config)

        self.sub_tabs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sub_tabs.setFixedWidth(800)

        self.sub_select_config.bt_refresh.clicked.connect(self.refresh_config)
        self.sub_select_config.bt_connect.clicked.connect(self.connect_config)
        self.sub_select_config.bt_delete.clicked.connect(self.delete_config)
        
        lt = QHBoxLayout()
        lt.addStretch(1)
        lt.addWidget(self.sub_tabs)
        lt.addStretch(1)

        self.setLayout(lt)

    def refresh_config(self):
        model = self.get_model_data()
        self.__table_list_config.setModel(model)

    def get_model_data(self):
        model = QStandardItemModel()
        with open(self.__data_configuration, 'r') as file:
            for row in csv.reader(file, delimiter=';'):
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)
        return model

    def get_id_from_selected_row(self, nameConf):
        indexes = self.__table_list_config.selectedIndexes()
        model = self.get_model_data()
        for index in indexes:
            row = index.row()
            column = nameConf #index.column()
            value = model.data(model.index(row, column))
            #print(f"({row}, {column} = {value}")
            return value

    def check_if_row_is_selectioned(self, indexes):
        return True if indexes else False

    def connect_new_created_config(self, name_config):
        self.__selected_config.set_name_config(name_config)

    def connect_config(self):
        if self.check_if_row_is_selectioned(self.__table_list_config.selectedIndexes()):
            nameConf_selected = self.get_id_from_selected_row(nameConf=0)
            screen_calibration_value_selected = self.get_id_from_selected_row(nameConf=0)

            self.__selected_config.set_name_config(nameConf_selected)
        else:
            dlg = CustomDialog(message="Select a row before connecting")
            dlg.exec()

    def delete_config(self):
        if self.check_if_row_is_selectioned(self.__table_list_config.selectedIndexes()):
            nameConf_selected = self.get_id_from_selected_row(nameConf=0)
            if self.__selected_config.get_name_config() != nameConf_selected: 
                df = pd.read_csv(self.__data_configuration, delimiter=';')
                df = df[df['NameConf'] != nameConf_selected]
                df.to_csv(self.__data_configuration, index=False, sep=';')
                dlg = CustomDialog(message="configuration deleted" + str(nameConf_selected))
                dlg.exec()
                self.refresh_config()#To refresh the dataview
            else:
                dlg = CustomDialog(message="Impossible to delete a connected config: " + str(nameConf_selected))
                dlg.exec()
        else:
            dlg = CustomDialog(message="Select a row before deleting")
            dlg.exec()

class Creation(QWidget):
    createdConfigSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.screen_calibration = None
        parameters = Parameters()
        self.__data_configuration = parameters.data_configuration

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        lb_name_config = QLabel("*Name config:")
        self.le_name_config = QLineEdit()
        self.le_name_config.setSizePolicy(size_policy)
        self.le_name_config.setFixedWidth(300)
        lt_name_config = QHBoxLayout()
        lt_name_config.addWidget(lb_name_config)
        lt_name_config.addWidget(self.le_name_config)

        lb_depth = QLabel("*Depth (cm):")
        self.le_depth = QLineEdit()
        self.le_depth.setSizePolicy(size_policy)
        self.le_depth.setFixedWidth(300)
        self.le_depth.setValidator(QIntValidator())
        lt_depth = QHBoxLayout()
        lt_depth.addWidget(lb_depth)
        lt_depth.addWidget(self.le_depth)

        lb_screen_width = QLabel("*Screen width (cm):")
        self.le_screen_width = QLineEdit()
        self.le_screen_width.setSizePolicy(size_policy)
        self.le_screen_width.setFixedWidth(300)
        self.le_screen_width.setValidator(QIntValidator())
        lt_screen_width = QHBoxLayout()
        lt_screen_width.addWidget(lb_screen_width)
        lt_screen_width.addWidget(self.le_screen_width)

        lb_screen_height = QLabel("*Screen height (cm):")
        self.le_screen_height = QLineEdit()
        self.le_screen_height.setSizePolicy(size_policy)
        self.le_screen_height.setFixedWidth(300)
        self.le_screen_height.setValidator(QIntValidator())
        lt_screen_height = QHBoxLayout()
        lt_screen_height.addWidget(lb_screen_height)
        lt_screen_height.addWidget(self.le_screen_height)

        self.bt_start_screen_calibration = QPushButton("Show Object")
        self.bt_start_screen_calibration.clicked.connect(self.start_screen_calibration)
        self.bt_stop_screen_calibration = QPushButton("Quit Object")
        self.bt_stop_screen_calibration.clicked.connect(self.stop_screen_calibration)
        lt_bt_screen_calibration = QHBoxLayout()
        lt_bt_screen_calibration.addWidget(self.bt_start_screen_calibration)
        lt_bt_screen_calibration.addWidget(self.bt_stop_screen_calibration)

        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.C))
        lb_size_object_cm = QLabel("*Write object width (cm):")
        self.le_size_object_cm = QLineEdit()
        self.le_size_object_cm.setSizePolicy(size_policy)
        self.le_size_object_cm.setFixedWidth(300)
        self.le_size_object_cm.setValidator(validator)
        lt_size_object_cm = QHBoxLayout()
        lt_size_object_cm.addWidget(lb_size_object_cm)
        lt_size_object_cm.addWidget(self.le_size_object_cm)

        lt_screen_calibration = QVBoxLayout()
        lt_screen_calibration.addLayout(lt_bt_screen_calibration)
        lt_screen_calibration.addLayout(lt_size_object_cm)

        group_box_screen_calibration = QGroupBox("Screen calibration")
        group_box_screen_calibration.setLayout(lt_screen_calibration)

        lb_exe_selector = QLabel("*Select the path to PupilLabs")
        self.le_exe_selector = QLineEdit()
        bt_browse = QPushButton("Browse")
        bt_browse.clicked.connect(self.browse_files)

        lt_exe_selector = QHBoxLayout()
        lt_exe_selector.addWidget(lb_exe_selector)
        lt_exe_selector.addWidget(self.le_exe_selector)
        lt_exe_selector.addWidget(bt_browse)

        self.bt_save_configuration = QPushButton("Save configuration")
        self.bt_save_configuration.clicked.connect(self.save_configuration)
        
        lt = QVBoxLayout()
        lt.addLayout(lt_name_config)
        lt.addLayout(lt_depth)
        lt.addLayout(lt_screen_width)
        lt.addLayout(lt_screen_height)
        lt.addWidget(group_box_screen_calibration)
        lt.addLayout(lt_exe_selector)
        lt.addWidget(self.bt_save_configuration)

        self.setLayout(lt)

    def browse_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "pupil_capture.exe", options=options)
        if fileName:
            self.le_exe_selector.setText(fileName)

    def start_screen_calibration(self):
        screen = QDesktopWidget().screenGeometry(1)
        self.screen_calibration = Screen_calibration()
        self.screen_calibration.setGeometry(screen)
        self.screen_calibration.showMaximized()

    def stop_screen_calibration(self):
        if self.screen_calibration != None:
            self.screen_calibration.close()
            self.screen_calibration = None

    def save_configuration_validator(self):
        if self.le_name_config.text() and self.le_depth.text() and self.le_screen_width.text() and self.le_screen_height.text() and self.le_size_object_cm.text() and self.le_exe_selector.text():
            return True
        else:
            return False

    def save_configuration(self):
        if self.save_configuration_validator():
            csv_recorder = CSV_recorder()
            csv_recorder.save_configuration(self.__data_configuration,
                self.le_name_config.text(),
                self.le_depth.text(),
                self.le_screen_width.text(),
                self.le_screen_height.text(),
                self.le_size_object_cm.text(),
                self.le_exe_selector.text(),
                datetime.now().strftime('%d-%m-%Y'))
            dlg = CustomDialog(message="Configuration saved in data_conf/data_configuration.csv")
            dlg.exec()

            self.createdConfigSignal.emit(self.le_name_config.text())
        else:
            dlg = CustomDialog(message="All the information are mandatory")
            dlg.exec()

class Selected_config(QWidget):
    def __init__(self):
        super().__init__()
        self.__name_config = "None"

        lb_name_config = QLabel("config name:")
        self.lb_config_selected_value = QLabel(self.__name_config)
        self.lt_name_config = QHBoxLayout()
        self.lt_name_config.addWidget(lb_name_config)
        self.lt_name_config.addWidget(self.lb_config_selected_value)

    def set_name_config(self, value):
        self.__name_config = value
        self.lb_config_selected_value.setText(value)

    def get_name_config(self):
        return self.__name_config

class Select_config(QWidget):
    def __init__(self, selected_config, table_list_config):
        super().__init__()
        self.__selected_config = selected_config
        self.__table_list_config = table_list_config

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.bt_refresh = QPushButton("Refresh")
        self.bt_connect = QPushButton("Connect")
        self.bt_delete = QPushButton("Delete")

        lt_vertical_bt = QHBoxLayout()
        lt_vertical_bt.addWidget(self.bt_refresh)
        lt_vertical_bt.addWidget(self.bt_connect)
        lt_vertical_bt.addWidget(self.bt_delete)

        self.__table_list_config.resizeColumnsToContents()

        lt = QVBoxLayout()
        lt.addLayout(lt_vertical_bt)
        lt.addWidget(self.__table_list_config)

        self.setLayout(lt)