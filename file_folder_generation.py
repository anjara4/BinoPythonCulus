from parameters import Parameters
from datetime import datetime
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class Generation():
    def folder_rec(self, foldername):
        try:
            os.mkdir(foldername)
        except OSError:
            print(f"Creation of the directory {foldername} failed")
        else:
            print(f"Successfully created the directory {foldername}")

    def filename_rec(self, exercice_name, code_patient, file_description):
        now = datetime.now()
        date = "Date" + now.strftime('%d-%m-%Y')
        time = "Time" + now.strftime("%H") + "-" + now.strftime("%M") + "-" + now.strftime("%S")
        filename = f"{exercice_name}_{code_patient}_{date}_{time}_{file_description}"
        return filename

    def write_into_text(self, folder_path, data):
        file = open(folder_path + "description.txt", 'w')
        file.write(data)
        file.close()

    def decription_rec(self, folder_path, exercice_name, code_patient, name_config, size, other):
        now = datetime.now()
        date = "Date creation: " + now.strftime('%d-%m-%Y')
        time = "Time creation: " + now.strftime("%H") + "-" + now.strftime("%M") + "-" + now.strftime("%S")
        exo = "Name exo: " + exercice_name
        config = "Name config: " + name_config
        patient = "Code patient: " + code_patient
        size_target = "Size target: " + str(size)

        self.write_into_text(
                            folder_path,
                            str(date) + "\n" + 
                            str(time) + "\n" +
                            str(exo) + "\n" +
                            str(config) + "\n" +
                            str(patient) + "\n" +
                            str(size_target) + "\n" +
                            str(other)
                            )

    def foldername_rec(self, exercice_name, code_patient):
        now = datetime.now()
        date = "Date" + now.strftime('%d-%m-%Y')
        time = "Time" + now.strftime("%H") + "-" + now.strftime("%M") + "-" + now.strftime("%S")

        parameters = Parameters()
        data_path = parameters.data_folder_path 

        filename = data_path + f"{exercice_name}_{code_patient}_{date}_{time}"
        self.folder_rec(data_path)
        self.folder_rec(filename)
        return filename
        