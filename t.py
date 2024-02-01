from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV File Selector")

        self.lineEdit = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.browse_files)

        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv)", options=options)
        if fileName:
            self.lineEdit.setText(fileName)
