import uvc
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QThread
import numpy as np
import sys
import cv2

dev_list = uvc.device_list()
#print(dev_list.)
cap_world = uvc.Capture([ d for d in dev_list if d["name"]=="Pupil Cam1 ID2"][0]["uid"]) # Index world camera
#print('world', cap_world.avaible_modes)

class VideoThreadWorld(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        cap_world.frame_mode = (1280, 720, 30)
        while True:
            frame = cap_world.get_frame_robust()
            self.change_pixmap_signal.emit(frame.gray)

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Eye camera")
		self.display_width = 640
		self.display_height = 480
		# For the video recording
		self.image_world_label = QLabel(self)

		self.calib_box = QHBoxLayout()
		self.calib_box.addWidget(self.image_world_label)

		self.setLayout(self.calib_box)

		self.thread_world = VideoThreadWorld()
		self.thread_world.start()
		# connect its signal to the update_image slot
		#self.thread.change_pixmap_signal.connect(self.update_image)
		self.thread_world.change_pixmap_signal.connect(self.update_image_world)

	def update_image_world(self, frame):
		"""Updates the image_label with a new opencv image"""
		qt_img = self.convert_cv_qt_world(frame)
		self.image_world_label.setPixmap(qt_img)

        # time.sleep(1e-3)  # Slow down the program to allow the computation of centroids to be complete

	def convert_cv_qt_world(self, frame):
		"""Convert from an opencv image to QPixmap"""
		rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # The frame rgb_image is cropped to remove the housing of the camera
		h, w, ch = rgb_image.shape

		bytes_per_line = ch * w
		convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
		p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
		return QPixmap.fromImage(p)

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())