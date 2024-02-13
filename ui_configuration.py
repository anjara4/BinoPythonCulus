from PyQt5.QtWidgets import QWidget, QTabWidget, QTableView, QDesktopWidget, QFileDialog
from PyQt5.QtWidgets import QSizePolicy, QDateEdit, QLabel, QGroupBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QLocale


from ui_customDialog import CustomDialog 
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem

from recording import CSV_recorder

from datetime import datetime

from configuration import Screen_calibration

import csv

import pandas as pd

class UI_main_configuration(QWidget):
    def __init__(self, selected_config):
        super().__init__()

        self.__selected_config = selected_config

        self.sub_tabs = QTabWidget()
        self.sub_tab1 = Creation()
        self.sub_tab2 = Select_config(self.__selected_config)
        self.sub_tabs.addTab(self.sub_tab1, "Creation")
        self.sub_tabs.addTab(self.sub_tab2, "SelectConfig")

        self.sub_tabs.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sub_tabs.setFixedWidth(800)
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.sub_tabs)
        layout.addStretch(1)

        self.setLayout(layout)

class Creation(QWidget):
    def __init__(self):
        super().__init__()

        self.screen_calibration = None

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_name_config = QLabel("*Name config:")
        self.line_edit_name_config = QLineEdit()
        self.line_edit_name_config.setSizePolicy(size_policy)
        self.line_edit_name_config.setFixedWidth(300)
        layout_name_config = QHBoxLayout()
        layout_name_config.addWidget(label_name_config)
        layout_name_config.addWidget(self.line_edit_name_config)

        label_depth = QLabel("*Depth (cm):")
        self.line_edit_depth = QLineEdit()
        self.line_edit_depth.setSizePolicy(size_policy)
        self.line_edit_depth.setFixedWidth(300)
        self.line_edit_depth.setValidator(QIntValidator())
        layout_depth = QHBoxLayout()
        layout_depth.addWidget(label_depth)
        layout_depth.addWidget(self.line_edit_depth)

        label_screen_width = QLabel("*Screen width (cm):")
        self.line_edit_screen_width = QLineEdit()
        self.line_edit_screen_width.setSizePolicy(size_policy)
        self.line_edit_screen_width.setFixedWidth(300)
        self.line_edit_screen_width.setValidator(QIntValidator())
        layout_screen_width = QHBoxLayout()
        layout_screen_width.addWidget(label_screen_width)
        layout_screen_width.addWidget(self.line_edit_screen_width)

        label_screen_height = QLabel("*Screen height (cm):")
        self.line_edit_screen_height = QLineEdit()
        self.line_edit_screen_height.setSizePolicy(size_policy)
        self.line_edit_screen_height.setFixedWidth(300)
        self.line_edit_screen_height.setValidator(QIntValidator())
        layout_screen_height = QHBoxLayout()
        layout_screen_height.addWidget(label_screen_height)
        layout_screen_height.addWidget(self.line_edit_screen_height)

        self.button_start_screen_calibration = QPushButton("Show Object")
        self.button_start_screen_calibration.clicked.connect(self.start_screen_calibration)
        self.button_stop_screen_calibration = QPushButton("Quit Object")
        self.button_stop_screen_calibration.clicked.connect(self.stop_screen_calibration)
        layout_button_screen_calibration = QHBoxLayout()
        layout_button_screen_calibration.addWidget(self.button_start_screen_calibration)
        layout_button_screen_calibration.addWidget(self.button_stop_screen_calibration)

        validator = QDoubleValidator()
        validator.setLocale(QLocale(QLocale.C))
        label_size_object_cm = QLabel("*Write object width (cm):")
        self.line_edit_size_object_cm = QLineEdit()
        self.line_edit_size_object_cm.setSizePolicy(size_policy)
        self.line_edit_size_object_cm.setFixedWidth(300)
        self.line_edit_size_object_cm.setValidator(validator)
        layout_size_object_cm = QHBoxLayout()
        layout_size_object_cm.addWidget(label_size_object_cm)
        layout_size_object_cm.addWidget(self.line_edit_size_object_cm)

        layout_screen_calibration = QVBoxLayout()
        layout_screen_calibration.addLayout(layout_button_screen_calibration)
        layout_screen_calibration.addLayout(layout_size_object_cm)

        group_box_screen_calibration = QGroupBox("Screen calibration")
        group_box_screen_calibration.setLayout(layout_screen_calibration)

        label_exe_selector = QLabel("*Select the path to PupilLabs")
        self.line_edit_exe_selector = QLineEdit()
        button_browse = QPushButton("Browse")
        button_browse.clicked.connect(self.browse_files)

        layout_exe_selector = QHBoxLayout()
        layout_exe_selector.addWidget(label_exe_selector)
        layout_exe_selector.addWidget(self.line_edit_exe_selector)
        layout_exe_selector.addWidget(button_browse)

        self.button_save_configuration = QPushButton("Save configuration")
        self.button_save_configuration.clicked.connect(self.save_configuration)
        
        layout = QVBoxLayout()
        layout.addLayout(layout_name_config)
        layout.addLayout(layout_depth)
        layout.addLayout(layout_screen_width)
        layout.addLayout(layout_screen_height)
        layout.addWidget(group_box_screen_calibration)
        layout.addLayout(layout_exe_selector)
        layout.addWidget(self.button_save_configuration)

        self.setLayout(layout)

    def browse_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "pupil_capture.exe", options=options)
        if fileName:
            self.line_edit_exe_selector.setText(fileName)

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
        if self.line_edit_name_config.text() and self.line_edit_depth.text() and self.line_edit_screen_width.text() and self.line_edit_screen_height.text() and self.line_edit_size_object_cm.text() and self.line_edit_exe_selector.text():
            return True
        else:
            return False

    def save_configuration(self):
        if self.save_configuration_validator():
            csv_recorder = CSV_recorder()
            csv_recorder.save_configuration("data_configuration.csv",
                self.line_edit_name_config.text(),
                self.line_edit_depth.text(),
                self.line_edit_screen_width.text(),
                self.line_edit_screen_height.text(),
                self.line_edit_size_object_cm.text(),
                self.line_edit_exe_selector.text(),
                datetime.now().strftime('%d-%m-%Y'))
            dlg = CustomDialog(message="Configuration saved in data_configuration.csv")
            dlg.exec()
        else:
            dlg = CustomDialog(message="All the information are mandatory")
            dlg.exec()

class Selected_config(QWidget):
    def __init__(self):
        super().__init__()
        self.__name_config = "None"

        label_name_config = QLabel("config name:")
        self.label_config_selected_value = QLabel(self.__name_config)
        self.layout_name_config = QHBoxLayout()
        self.layout_name_config.addWidget(label_name_config)
        self.layout_name_config.addWidget(self.label_config_selected_value)

    def set_name_config(self, value):
        self.__name_config = value
        self.label_config_selected_value.setText(value)

    def get_name_config(self):
        return self.__name_config

class Select_config(QWidget):
    def __init__(self, selected_config):
        super().__init__()
        self.__selected_config = selected_config

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.clicked.connect(self.connect_refresh)

        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.connect_config)

        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.connect_delete)

        layout_vertical_button = QHBoxLayout()
        layout_vertical_button.addWidget(self.button_refresh)
        layout_vertical_button.addWidget(self.button_connect)
        layout_vertical_button.addWidget(self.button_delete)

        self.table = QTableView()
        self.connect_refresh()

        self.table.resizeColumnsToContents()

        #Selected Config

        layout = QVBoxLayout()
        layout.addLayout(layout_vertical_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def connect_refresh(self):
        self.model = self.get_model_data()
        self.table.setModel(self.model)

    def get_model_data(self):
        model = QStandardItemModel()
        with open('data_configuration.csv', 'r') as file:
            for row in csv.reader(file, delimiter=';'):
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)
        return model

    def get_id_from_selected_row(self, nameConf):
        indexes = self.table.selectedIndexes()
        for index in indexes:
            row = index.row()
            column = nameConf #index.column()
            value = self.model.data(self.model.index(row, column))
            #print(f"({row}, {column} = {value}")
            return value

    def check_if_row_is_selectioned(self, indexes):
        return True if indexes else False

    def connect_config(self):
        if self.check_if_row_is_selectioned(self.table.selectedIndexes()):
            nameConf_selected = self.get_id_from_selected_row(nameConf=0)
            screen_calibration_value_selected = self.get_id_from_selected_row(nameConf=0)

            self.__selected_config.set_name_config(nameConf_selected)
        else:
            dlg = CustomDialog(message="Select a row before connecting")
            dlg.exec()

    def connect_delete(self):
        if self.check_if_row_is_selectioned(self.table.selectedIndexes()):
            nameConf_selected = self.get_id_from_selected_row(nameConf=0)
            df = pd.read_csv('data_configuration.csv', delimiter=';')
            df = df[df['NameConf'] != nameConf_selected]
            df.to_csv('data_configuration.csv', index=False, sep=';')
            dlg = CustomDialog(message="configuration deleted" + str(nameConf_selected))
            dlg.exec()
            self.connect_refresh()#To refresh the dataview
        else:
            dlg = CustomDialog(message="Select a row before deleting")
            dlg.exec()