import csv

from parameters import Parameters

class CSV_recorder:
    def __init__(self):
        self.__filename = "keep.csv"

    def get_filename(self):
        return self.__filename

    def set_filename(self, value):
        self.__filename = value

    def set_header(self):
        with open(self.__filename, 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(["time", "x", "y"])

    def record(self, t, x, y):
        with open(self.__filename, 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([t, x, y])

    def save_patient(self, file_patient, first_name, name, sex, date_birth, code_patient, date_creation):
        with open(file_patient, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([first_name, name, sex, date_birth, code_patient, date_creation])

    def save_configuration(self, file_configuration, name_configuration, depth, screen_width, screen_height, width_target_infini_object_cm, path_pupilLabs, date_creation):
        with open(file_configuration, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([name_configuration, depth, screen_width, screen_height, width_target_infini_object_cm, path_pupilLabs, date_creation])
