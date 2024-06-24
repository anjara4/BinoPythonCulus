import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy, QWidget, QSlider, QTabWidget, QRadioButton, QSizePolicy
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import numpy as np

import os

#import matplotlib.pyplot as plt
from scipy.stats import zscore

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QWidget
from PyQt5.QtCore import Qt

from ui_customDialog import CustomDialog 

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class UI_main_visualisation(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UI_main_visualisation, self).__init__(parent)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        lb_csv_selector_target = QLabel("Select a target csv file")
        self.le_csv_selector_target = QLineEdit()
        self.bt_browse_target = QPushButton("Browse")
        self.bt_browse_target.clicked.connect(lambda: self.browse_files(
            "CSV Files (*_Target.csv)",
            self.le_csv_selector_target
            ))

        lt_target = QHBoxLayout()
        lt_target.addWidget(lb_csv_selector_target)
        lt_target.addWidget(self.le_csv_selector_target)
        lt_target.addWidget(self.bt_browse_target)

        lb_csv_selector_eye = QLabel("Select an eye csv file")
        self.le_csv_selector_eye = QLineEdit()
        self.bt_browse_eye = QPushButton("Browse")
        self.bt_browse_eye.clicked.connect(lambda: self.browse_files(
            "CSV Files (*.csv)",
            self.le_csv_selector_eye
            ))
        
        lt_eye = QHBoxLayout()
        lt_eye.addWidget(lb_csv_selector_eye)
        lt_eye.addWidget(self.le_csv_selector_eye)
        lt_eye.addWidget(self.bt_browse_eye)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.setSizePolicy(size_policy)
        self.sc.setFixedWidth(1200)

        size_rb = 90
        self.rb_target = QRadioButton("Target", self)
        self.rb_target.setSizePolicy(size_policy)
        self.rb_target.setFixedWidth(size_rb)
        
        self.rb_eye = QRadioButton("Eye", self)
        self.rb_eye.setSizePolicy(size_policy)
        self.rb_eye.setFixedWidth(size_rb)

        lb_threshold = QLabel("Threshold \n Outliers")
        lb_threshold.setWordWrap(True)
        self.sd_threshold = QSlider(Qt.Horizontal, self)
        self.sd_threshold.setSizePolicy(size_policy)
        self.sd_threshold.setFixedWidth(size_rb)
        self.sd_threshold.setMinimum(1)
        self.sd_threshold.setMaximum(10)
        self.sd_threshold.setSliderPosition(2)
        self.sd_threshold.valueChanged.connect(self.update_sd_threshold_value)
        self.lb_sd_threshold_value = QLabel()
        self.lb_sd_threshold_value.setSizePolicy(size_policy)
        self.lb_sd_threshold_value.setFixedWidth(15)
        self.lb_sd_threshold_value.setText(str(self.sd_threshold.value()))
        self.lt_threshold = QHBoxLayout()
        self.lt_threshold.addWidget(lb_threshold)
        self.lt_threshold.addWidget(self.sd_threshold)
        self.lt_threshold.addWidget(self.lb_sd_threshold_value)

        lb_scaler = QLabel("Scaler \n Target")
        lb_scaler.setWordWrap(True)
        self.sd_scaler = QSlider(Qt.Horizontal, self)
        self.sd_scaler.setSizePolicy(size_policy)
        self.sd_scaler.setFixedWidth(size_rb)
        self.sd_scaler.setMinimum(5)
        self.sd_scaler.setMaximum(10)
        self.sd_scaler.setSliderPosition(8)
        self.sd_scaler.valueChanged.connect(self.update_sd_scaler_value)
        self.lb_sd_scaler_value = QLabel()
        self.lb_sd_scaler_value.setSizePolicy(size_policy)
        self.lb_sd_scaler_value.setFixedWidth(20)
        self.lb_sd_scaler_value.setText("0.8")
        #self.lb_sd_scaler_value.setText(str(self.sd_scaler.value()))
        self.lt_scaler = QHBoxLayout()
        self.lt_scaler.addWidget(lb_scaler)
        self.lt_scaler.addWidget(self.sd_scaler)
        self.lt_scaler.addWidget(self.lb_sd_scaler_value)

        self.rb_filtered_eye = QRadioButton("Filtered Eye", self)
        self.rb_filtered_eye.setSizePolicy(size_policy)
        self.rb_filtered_eye.setFixedWidth(size_rb)
        
        self.rb_all = QRadioButton("All", self)
        self.rb_all.setSizePolicy(size_policy)
        self.rb_all.setFixedWidth(size_rb)

        self.rb_none = QRadioButton("None", self)
        self.rb_none.setSizePolicy(size_policy)
        self.rb_none.setFixedWidth(size_rb)
        self.rb_none.setChecked(True)

        self.rb_target.toggled.connect(lambda: self.plot_csv(
            self.get_data(self.le_csv_selector_target.text(), True),
            'red'
            ))

        self.rb_eye.toggled.connect(lambda: self.plot_csv(
            self.get_data(self.le_csv_selector_eye.text(), False),
            'blue'
            ))

        self.rb_filtered_eye.toggled.connect(self.plot_filtered_eye_csv)

        self.rb_all.toggled.connect(self.plot_all)

        self.rb_none.toggled.connect(self.clear_canvas)

        lt_rb = QVBoxLayout()
        lt_rb.addWidget(self.rb_target)
        lt_rb.addWidget(self.rb_eye)
        lt_rb.addLayout(self.lt_threshold)
        lt_rb.addLayout(self.lt_scaler)
        lt_rb.addWidget(self.rb_filtered_eye)
        lt_rb.addWidget(self.rb_all)
        lt_rb.addWidget(self.rb_none)

        lt_plot = QHBoxLayout()
        lt_plot.addWidget(self.sc)
        lt_plot.addLayout(lt_rb)

        lt = QtWidgets.QVBoxLayout(self)
        lt.addLayout(lt_target)
        lt.addLayout(lt_eye)
        lt.addLayout(lt_plot)

    def update_sd_scaler_value(self):
        self.lb_sd_scaler_value.setText(str(self.sd_scaler.value()/10))
        
        if self.rb_all.isChecked():
            self.plot_all()

    def update_sd_threshold_value(self):
        self.lb_sd_threshold_value.setText(str(self.sd_threshold.value()))
        if self.rb_filtered_eye.isChecked():
            self.plot_filtered_eye_csv()    

        if self.rb_all.isChecked():
            self.plot_all()

    def plot_filtered_eye_csv(self):
        if self.validator():
            data = self.get_data(self.le_csv_selector_eye.text(), False)
            filtered_data = self.remove_noise_data(data, self.sd_threshold.value())
            self.plot_csv(filtered_data, 'blue')

    def clear_canvas(self):
        self.sc.axes.clear()
        self.sc.draw()

    def get_data(self, fileName, is_data_target):
        if is_data_target:
            data = pd.read_csv(fileName, sep=';')
            data = data[['x', 'y']]
        else:
            data = pd.read_csv(fileName, sep=',')
            data = data[['norm_pos_x', 'norm_pos_y']]
            data.rename(columns={'norm_pos_x': 'x', 'norm_pos_y': 'y'}, inplace=True)
        return data

    def remove_noise_data(self, data, threshold):
        data['z_x'] = zscore(data['x'])
        data['z_y'] = zscore(data['y'])

        return data[(data['z_x'].abs() < threshold) & (data['z_y'].abs() < threshold)]

    def normalize_data(self, data):
        scaler = MinMaxScaler()
        data[['x', 'y']] = scaler.fit_transform(data[['x', 'y']])
        return data

    def scale_data(self, data, scale):
        data[['x', 'y']] = data[['x', 'y']].mul(scale)
        return data

    def centralize_origin(self, data):
        min_x = data['x'].min()
        max_x = data['x'].max()

        min_y = data['y'].min()
        max_y = data['y'].max()

        data['x'] = data['x'] - ((max_x - min_x) / 2)
        data['y'] = data['y'] - ((max_y - min_y) / 2)
        return data

    def browse_files(self, filter_condition, le_output):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", filter_condition, options=options)
        if fileName:
            le_output.setText(fileName)

    def validator(self):
        if self.le_csv_selector_target.text() == "" or self.le_csv_selector_eye.text() == "":
            return False
        else: 
            return True

    def plot_all(self):
        if self.validator():
            d_target = self.get_data(self.le_csv_selector_target.text(), True)
            d_target = self.normalize_data(d_target)
            d_target = self.centralize_origin(d_target)
            d_target = self.scale_data(d_target, self.sd_scaler.value()/10)

            d_eye = self.get_data(self.le_csv_selector_eye.text(), False) 
            d_eye = self.remove_noise_data(d_eye, self.sd_threshold.value())
            d_eye = self.normalize_data(d_eye)
            d_eye = self.centralize_origin(d_eye)

            self.sc.axes.clear()
            try:
                self.sc.axes.scatter(d_target['x'], d_target['y'], c='red')
                
                self.sc.axes.scatter(d_eye['x'], d_eye['y'], c='blue')
                
                self.sc.draw()
            except Exception as e:
                print(f"An error occurred: {e}")
                dlg = CustomDialog(message="Error: " + str(e))
                dlg.exec()

    def plot_csv(self, data, color):
        self.sc.axes.clear()
        try:
            self.sc.axes.scatter(data['x'], data['y'], c=color)
            self.sc.draw()
        except Exception as e:
            print(f"An error occurred: {e}")
            dlg = CustomDialog(message="Error: " + str(e))
            dlg.exec()

