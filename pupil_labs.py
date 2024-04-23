from PyQt5.QtWidgets import QDesktopWidget, QWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt

import pandas as pd

from ui_customDialog import CustomDialog 
from parameters import Parameters


import psutil
import time

import subprocess
import zmq, msgpack

class Pupil_labs(QWidget):
    def __init__(self, selected_config):
        super().__init__()

        self.__selected_config = selected_config
        self.__pupil_labs_status = None

    def get_path_pupilLabs(self):
        parameters = Parameters()
        df = pd.read_csv(parameters.data_configuration, delimiter=';')
        
        filtered_df = df[df['NameConf'] == self.__selected_config.get_name_config()]

        return filtered_df['PathPupilLabs'].values.item()

    def findProcessIdByName(self, processName):
        listOfProcessObjects = []
        #Iterate over the all the running process
        for proc in psutil.process_iter():
           try:
               pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
               # Check if process name contains the given name string.
               if processName.lower() in pinfo['name'].lower() :
                   listOfProcessObjects.append(pinfo)
           except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
               pass
        return listOfProcessObjects

    def stop_pupilLabs(self):
        listOfProcessIds = self.findProcessIdByName('pupil_capture')

        if len(listOfProcessIds) > 0:
           for elem in listOfProcessIds:
                processID = elem['pid']
                #processName = elem['name']
                #processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
                #print((processID ,processName,processCreationTime ))

                try:
                    process = psutil.Process(processID)
                    process.terminate()
                except Exception as e:
                    print(f"could not stop pupil labs")

        self.__pupil_labs_status = None

    def start_pupilLabs(self):
        if self.__selected_config.get_name_config() != "None":
            if self.__pupil_labs_status is None or self.__pupil_labs_status.poll() is not None:
                try:
                    self.__pupil_labs_status = subprocess.Popen([self.get_path_pupilLabs()])
                    dlg = CustomDialog(message="Pupil capture launched, it might tike a few seconds")
                    dlg.exec()
                except FileNotFoundError:
                     dlg = CustomDialog(message="Invalid path to PupilLabs executable")
                     dlg.exec()
            else:
                dlg = CustomDialog(message="Pupil capture already running")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Select a config")
            dlg.exec()

    def start_calibration(self):
        if self.__selected_config.get_name_config() != "None":
            if self.__pupil_labs_status == None:
                dlg = CustomDialog(message="PupilLab application not detected")
                dlg.exec() 
            elif self.__pupil_labs_status.poll() is None:
                pupil_remote = self.connect_pupil_network_api()
                pupil_remote.send_string('C')
                print(pupil_remote.recv_string())
            else:
                dlg = CustomDialog(message="Start pupil capture")
                dlg.exec()
        else:
            dlg = CustomDialog(message="Select a config")
            dlg.exec()

    def get_status(self):
        return self.__pupil_labs_status

    def send_recv_notification(self, pupil_remote, n):
        pupil_remote.send_string(f"notify.{n['subject']}", flags=zmq.SNDMORE)
        pupil_remote.send(msgpack.dumps(n))
        return pupil_remote.recv_string()

    def connect_pupil_network_api(self):
        ctx = zmq.Context()
        pupil_remote = zmq.Socket(ctx, zmq.REQ)
        parameters = Parameters()
        pupil_remote.connect('tcp://' + parameters.ip_adresse + ':' + parameters.port_number)
        return pupil_remote

    def start_record(self, folderName):
        if self.__pupil_labs_status == None:
            dlg = CustomDialog(message="PupilLab application not detected")
            dlg.exec() 
        elif self.__pupil_labs_status.poll() is None:
            pupil_remote = self.connect_pupil_network_api()
            pupil_remote.send_string('R ' + folderName)
            print(pupil_remote.recv_string())
        else:
            dlg = CustomDialog(message="PupilLab application not detected")
            dlg.exec() 

    def stop_record(self):
        try:
            pupil_remote = self.connect_pupil_network_api()
            pupil_remote.send_string('r')
            print(pupil_remote.recv_string())
        except Exception as e:
            print(f"could not stop the recording")
            
    def open_camera_eyes(self, position):
        pupil_remote = self.connect_pupil_network_api()

        n = {
            "subject": f"eye_process.should_start",
            "eye_id": position,
        }

        try:
            print(self.send_recv_notification(pupil_remote, n))
            time.sleep(5)
        except Exception as e:
            print(f"Error from opening camera" + str(position))

    def close_camera_eyes(self, position):
        pupil_remote = self.connect_pupil_network_api()

        n = {
            "subject": f"eye_process.should_stop",
            "eye_id": position,
        }

        try:
            print(self.send_recv_notification(pupil_remote, n))
            time.sleep(5)
        except Exception as e:
            print(f"Error from closing camera" + str(position))
