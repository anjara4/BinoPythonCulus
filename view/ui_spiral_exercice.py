from spiral_exercise import Spiral
from view.ui_exercise import UI_exercise
from PyQt5.QtWidgets import QVBoxLayout, QRadioButton, QLabel, QSlider, QComboBox, QHBoxLayout, QPushButton, QDesktopWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal

class UI_spiral(UI_exercise):
    toggleSignal = pyqtSignal(bool)
    def __init__(self, connected_patient, selected_config, pupil_labs, cam_left, cam_right):
        super().__init__(connected_patient, selected_config, pupil_labs, cam_left, cam_right, "Spiral")
    
        #region Create label for spiral orientation
        lb_orientation = QLabel("Spiral orientation")
        self.cb_orientation = QComboBox()
        self.cb_orientation.setSizePolicy(self.size_policy)
        self.cb_orientation.setFixedWidth(300)
        self.cb_orientation.addItem("Counterclockwise")
        self.cb_orientation.addItem("Clockwise")
        self.cb_orientation.setCurrentIndex(0)
        self.lt_orientation = QHBoxLayout()
        self.lt_orientation.addWidget(lb_orientation)
        self.lt_orientation.addWidget(self.cb_orientation)
        self.lt_orientation.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create label for spiral distance between loops
        lb_dist_between_loops = QLabel("Distance between loops (°)")
        self.sd_dist_between_loops = QSlider(Qt.Horizontal)
        self.sd_dist_between_loops.setSizePolicy(self.size_policy)
        self.sd_dist_between_loops.setFixedWidth(250)
        self.sd_dist_between_loops.setMinimum(1)
        self.sd_dist_between_loops.setMaximum(5)
        self.sd_dist_between_loops.setValue(5)
        self.sd_dist_between_loops.valueChanged.connect(self.update_sd_dist_between_loops_value)
        self.lb_sd_dist_between_loops_value = QLabel()
        self.lb_sd_dist_between_loops_value.setText(str(self.sd_dist_between_loops.value()/10))
        self.lt_dist_between_loops = QHBoxLayout()
        self.lt_dist_between_loops.addWidget(lb_dist_between_loops)
        self.lt_dist_between_loops.addWidget(self.sd_dist_between_loops)
        self.lt_dist_between_loops.addWidget(self.lb_sd_dist_between_loops_value)
        self.lt_dist_between_loops.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create a QLabel for number of cycles
        lb_nb_cycle_exo = QLabel("Nb cycle")
        self.sd_nb_cycle_exo = QSlider(Qt.Horizontal, self)
        self.sd_nb_cycle_exo.setSizePolicy(self.size_policy)
        self.sd_nb_cycle_exo.setFixedWidth(260)
        self.sd_nb_cycle_exo.setMinimum(2)
        self.sd_nb_cycle_exo.setMaximum(5)
        self.sd_nb_cycle_exo.setValue(4)
        self.sd_nb_cycle_exo.setEnabled(True)
        self.sd_nb_cycle_exo.valueChanged.connect(self.update_sd_nb_cycle_exo_value)
        self.lb_sd_nb_cycle_exo_value = QLabel()
        self.lb_sd_nb_cycle_exo_value.setSizePolicy(self.size_policy)
        self.lb_sd_nb_cycle_exo_value.setFixedWidth(25)
        self.lb_sd_nb_cycle_exo_value.setText(str(self.sd_nb_cycle_exo.value()))
        self.lt_nb_cycle_exo = QHBoxLayout()
        self.lt_nb_cycle_exo.addWidget(lb_nb_cycle_exo)
        self.lt_nb_cycle_exo.addWidget(self.sd_nb_cycle_exo)
        self.lt_nb_cycle_exo.addWidget(self.lb_sd_nb_cycle_exo_value)
        self.lt_nb_cycle_exo.setContentsMargins(0, 0, 0, 8)
        #endregion

        #region Create a QLabel for automatic stop
        """
        self.lb_auto_stop = QLabel("Automatic stop")
        self.rb_true = QRadioButton("True", self)
        self.rb_false = QRadioButton("False", self)
        self.rb_true.setChecked(True)
        self.rb_false.toggled.connect(self.create_form_automatic_stop)
        self.lt_auto_stop = QHBoxLayout()
        self.lt_auto_stop.addWidget(self.lb_auto_stop)
        self.lt_auto_stop.addWidget(self.rb_true)
        self.lt_auto_stop.addWidget(self.rb_false)
        self.lt_auto_stop.setContentsMargins(0, 0, 0, 0)
        """
        #endregion

        #region Create label for spiral speed
        lb_speed = QLabel("Speed factor")
        self.sd_speed = QSlider(Qt.Horizontal)
        self.sd_speed.setSizePolicy(self.size_policy)
        self.sd_speed.setFixedWidth(250)
        self.sd_speed.setMinimum(1)
        self.sd_speed.setMaximum(20)
        self.sd_speed.setValue(10)
        self.sd_speed.setEnabled(True)
        self.lb_sd_speed_value = QLabel()   
        self.lb_sd_speed_value.setText(str(self.sd_speed.value()/10))
        self.lb_sd_speed_value.setSizePolicy(self.size_policy)
        self.lb_sd_speed_value.setFixedWidth(35)
        self.sd_speed.valueChanged.connect(self.update_sd_speed_value)
        self.lt_speed = QHBoxLayout()
        self.lt_speed.addWidget(lb_speed)
        self.lt_speed.addWidget(self.sd_speed)
        self.lt_speed.addWidget(self.lb_sd_speed_value)
        self.lt_speed.setContentsMargins(0, 0, 0, 0)
        #endregion

        self.lt_bt_rec = QHBoxLayout()
        self.lt_bt_rec.addWidget(self.bt_launch_exercise)
        self.lt_bt_rec.addWidget(self.bt_rec_target_pupil)
        self.lt_bt_rec.addWidget(self.bt_rec_target_lens)    

        self.lt = QVBoxLayout()
        self.lt.addLayout(self.lt_color)
        self.lt.addLayout(self.lt_size)
        self.lt.addLayout(self.lt_orientation)
        self.lt.addLayout(self.lt_speed)
        self.lt.addLayout(self.lt_dist_between_loops)
        self.lt.addLayout(self.lt_nb_cycle_exo)
        #self.lt.addLayout(self.lt_auto_stop)
        self.lt.addLayout(self.lt_mode)
        self.lt.addLayout(self.lt_bt_pupilLabs)
        self.lt.addLayout(self.lt_bt_rec)
        self.lt.addWidget(self.bt_stop)
        self.lt.addWidget(self.lb_rec_img)
        self.lt.addLayout(self.lt_bt_calibration)

        self.setLayout(self.lt)

    def create_form_automatic_stop(self):
        if self.rb_false.isChecked():
            self.sd_nb_cycle_exo.setEnabled(False)
        else:
            self.sd_nb_cycle_exo.setEnabled(True)

    def launch_exercise(self):
        self.stop_all()

        if self.check_condition_exo():
            self.set_exercise(Spiral(
                self.get_selected_config(),
                self.lb_rec_img,
                self.get_pupil_labs(),
                self.get_camera_left(),
                self.get_camera_right()
                ))
            
            self.get_exercise().set_x(self.get_exercise().get_x_init())
            self.get_exercise().set_y(self.get_exercise().get_y_init())
            self.get_exercise().set_nb_cycle_exo(self.sd_nb_cycle_exo.value())
            self.get_exercise().set_t()
            self.get_exercise().set_speed_factor(self.sd_speed.value()*100)

            """
            if self.rb_false.isChecked():
                self.get_exercise().set_nb_cycle_exo(1000)
                # define an high number represinting an infinite value
            else:
                self.get_exercise().set_nb_cycle_exo(self.sd_nb_cycle_exo.value())"""

            self.get_exercise().set_selected_config(self.get_selected_config())
            self.get_exercise().set_color(QColor(self.cb_color.currentData()))
            self.set_orientation()
            self.get_exercise().set_dist_between_loops(self.get_exercise().degrees_to_px(float(self.lb_sd_dist_between_loops_value.text())))
            self.get_exercise().set_ratio_pixel_cm()

            self.get_exercise().set_size(
                self.get_exercise().degrees_to_cm(
                    float(self.logMar_to_deg[self.lb_sd_size_value.text()])
                ) 
            )

            self.get_exercise().scale_size()  # based on ratio_pixel_cm

            screen = QDesktopWidget().screenGeometry(1)
            self.get_exercise().setGeometry(screen)
            # self.infinite.showMaximized()
            self.get_exercise().showFullScreen()
            self.get_exercise().set_is_running(True)
    
    def set_orientation(self):
        if self.cb_orientation.currentText() == "Clockwise":
            self.get_exercise().set_orientation(1)
        else:
            self.get_exercise().set_orientation(-1)

    def update_sd_nb_cycle_exo_value(self):
        self.lb_sd_nb_cycle_exo_value.setText(str(self.sd_nb_cycle_exo.value()))

    def update_sd_dist_between_loops_value(self):
        self.lb_sd_dist_between_loops_value.setText(str(self.sd_dist_between_loops.value()/10))

    def update_sd_speed_value(self): 
        self.lb_sd_speed_value.setText(str(self.sd_speed.value()/10))
