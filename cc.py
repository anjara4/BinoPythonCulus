import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class Tab(QWidget):
    def __init__(self):
        super().__init__()
        label_code_patient = QLabel("Code patient")
        line_edit_code_patient = QLineEdit()
        line_edit_code_patient.setReadOnly(True)
        line_edit_code_patient.setStyleSheet("background-color: lightgray;")
        layout = QHBoxLayout()
        layout.addWidget(label_code_patient)
        layout.addWidget(line_edit_code_patient)
        self.setLayout(layout)

class SubTabPatient(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("This is a sub-tab for patient data.")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class TabPatient(Tab):
    def __init__(self):
        super().__init__()
        self.sub_tabs = QTabWidget()
        self.sub_tab1 = SubTabPatient()
        self.sub_tab2 = SubTabPatient()
        self.sub_tab3 = SubTabPatient()
        self.sub_tabs.addTab(self.sub_tab1, "Creation")
        self.sub_tabs.addTab(self.sub_tab2, "Connexion")
        self.sub_tabs.addTab(self.sub_tab3, "Data")
        
        layout = QVBoxLayout()
        layout.addWidget(self.sub_tabs)

        if self.layout() is not None:
            self.layout().deleteLater()
        self.setLayout(layout)

class Login(QWidget):
    def __init__(self):
        super().__init__()
        label_username = QLabel("Username")
        line_edit_username = QLineEdit()
        label_password = QLabel("Password")
        line_edit_password = QLineEdit()
        line_edit_password.setEchoMode(QLineEdit.Password)
        button_login = QPushButton("Login")
        layout = QVBoxLayout()
        layout.addWidget(label_username)
        layout.addWidget(line_edit_username)
        layout.addWidget(label_password)
        layout.addWidget(line_edit_password)
        layout.addWidget(button_login)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabs and Sub-Tabs Example")
        self.setGeometry(100, 100, 800, 600)

        tab_widget = QTabWidget()
        tab_widget.addTab(Tab(), "Tab 1")
        tab_widget.addTab(TabPatient(), "Tab 2")
        tab_widget.addTab(Login(), "Login")

        label_logged_in_as = QLabel("Logged in as: ")
        label_logged_in_user = QLabel("Guest")
        layout_logged_in = QHBoxLayout()
        layout_logged_in.addWidget(label_logged_in_as)
        layout_logged_in.addWidget(label_logged_in_user)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_logged_in)
        layout_main.addWidget(tab_widget)

        widget_main = QWidget()
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
