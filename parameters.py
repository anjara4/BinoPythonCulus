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
        self.x_scaling_infini_vertical = self.__paths[9]
        self.y_scaling_infini_vertical = self.__paths[10]
        self.x_scaling_infini_horizontal = self.__paths[11]
        self.y_scaling_infini_horizontal = self.__paths[12] 
        self.fps = self.__paths[13]
        self.frame_size_height = self.__paths[14]
        self.frame_size_weight = self.__paths[15]
        self.camera_display_width = self.__paths[16]
        self.camera_display_height = self.__paths[17]
        self.logMar_to_deg_data = {}
        with open(self.__paths[18]) as f:
            for line in f:
                (key, val) = line.split(";")
                self.logMar_to_deg_data[key] = val
        self.scenario_path = self.__paths[19]
        self.default_config_name = self.__paths[20]
        self.default_patient_name = self.__paths[21]