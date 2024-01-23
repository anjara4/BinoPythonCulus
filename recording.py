import csv
from datetime import datetime

class CSV_recorder:
    def __init__(self):
        self.__filename = "keep.csv"

    def record(self, t, x, y):
        with open(self.__filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([t, x, y])

    def generate_filename(self, code_patient, exercice_name):
        now = datetime.now()
        return code_patient + "_" + now.strftime('%d-%m-%Y') + "_" + now.strftime("%H") + "-" + now.strftime("%M") + "_" + exercice_name + ".csv"

    def get_filename(self):
        return self.__filename

    def set_filename(self, value):
        self.__filename = value