from PyQt5.QtWidgets import QVBoxLayout, QDialog, QDialogButtonBox, QLabel 
from PyQt5.QtCore import Qt

class CustomDialog(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Information")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.layout = QVBoxLayout()
        label_message = QLabel(message)
        self.layout.addWidget(label_message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)