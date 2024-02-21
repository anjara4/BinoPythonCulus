class Parameters:
    def __init__(self):

        self.__paths = []

        with open('parameters.txt', 'r') as file:
            # Read each line in the file and store it in a list
            self.__paths = [line.strip().split('=')[1].strip() for line in file]

        self.image_calibration = self.__paths[0]
        self.image_recording = self.__paths[1]
        self.data_folder_path = self.__paths[2]
        self.data_patient = self.__paths[3]
        self.data_configuration = self.__paths[4]
        self.ip_adresse = self.__paths[5]
        self.port_number = self.__paths[6]
        self.size_object_screen_calibration = self.__paths[7]
        self.size_object_calibration_lens = self.__paths[8] 