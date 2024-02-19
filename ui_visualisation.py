import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
import pandas as pd
import os

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
        layout = QtWidgets.QVBoxLayout(self)

        label_csv_selector = QLabel("Select a target csv file")
        self.line_edit_csv_selector = QLineEdit()
        self.button_browse = QPushButton("Browse")
        self.button_browse.clicked.connect(self.browse_files)
        self.button_plot = QPushButton("Plot")
        self.button_plot.clicked.connect(self.plot_csv)

        layout_csv_selector = QHBoxLayout()
        layout_csv_selector.addWidget(label_csv_selector)
        layout_csv_selector.addWidget(self.line_edit_csv_selector)
        layout_csv_selector.addWidget(self.button_browse)
        layout_csv_selector.addWidget(self.button_plot)
        
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        layout.addLayout(layout_csv_selector)
        layout.addWidget(self.sc)

    def ged_data(self, fileName):
        return pd.read_csv(fileName, sep=';')

    def browse_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*_Target.csv)", options=options)
        if fileName:
            self.line_edit_csv_selector.setText(fileName)

    def plot_csv(self):
        if not self.line_edit_csv_selector.text().strip():
            dlg = CustomDialog(message="Select a target csv file")
            dlg.exec() 
        else:
            self.sc.axes.clear()
            try:
                data = self.ged_data(os.path.basename(self.line_edit_csv_selector.text()))
                self.sc.axes.scatter(data['x'], data['y'])
                self.sc.draw()
            except Exception as e:
                print(f"An error occurred: {e}")
                dlg = CustomDialog(message="Error: " + str(e))
                dlg.exec()

