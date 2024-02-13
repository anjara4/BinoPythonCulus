import csv
from datetime import datetime
import zmq

from ui_customDialog import CustomDialog 

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

    def generate_filename(self, code_patient, exercice_name):
        now = datetime.now()
        return code_patient + "_" + now.strftime('%d-%m-%Y') + "_" + now.strftime("%H") + "-" + now.strftime("%M") + "_" + exercice_name + "_Target.csv"

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

class PupilLabs_recorder:
    def __init__(self):
        self.ctx = zmq.Context()
        self.pupil_remote = zmq.Socket(self.ctx, zmq.REQ)

    def start_record_pupilLab(self, pupilLabStatus):
        if pupilLabStatus == None:
            dlg = CustomDialog(message="PupilLab application not detected")
            dlg.exec() 
        elif pupilLabStatus.poll() is None:
            self.pupil_remote.connect('tcp://127.0.0.1:50020')

            self.pupil_remote.send_string('R')
            print(self.pupil_remote.recv_string())
        else:
            dlg = CustomDialog(message="PupilLab application not detected")
            dlg.exec() 

    def stop_record_pupilLab(self, pupilLabStatus):
        if pupilLabStatus == None:
            return

        elif pupilLabStatus.poll() is None:
            self.pupil_remote.connect('tcp://127.0.0.1:50020')
            self.pupil_remote.send_string('r')
            print(self.pupil_remote.recv_string())