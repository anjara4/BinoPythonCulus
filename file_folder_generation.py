from parameters import Parameters
from datetime import datetime
import os

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
        date = now.strftime('%d-%m-%Y')
        time = now.strftime("%H") + "-" + now.strftime("%M")
        filename = f"{exercice_name}_{code_patient}_{date}_{time}_{file_description}"
        return filename

    def foldername_rec(self, exercice_name, code_patient):
        now = datetime.now()
        date = now.strftime('%d-%m-%Y')
        time = now.strftime("%H") + "-" + now.strftime("%M")

        parameters = Parameters()
        data_path = parameters.data_folder_path 

        filename = data_path + f"{exercice_name}_{code_patient}_{date}_{time}"
        self.folder_rec(data_path)
        self.folder_rec(filename)
        return filename
        