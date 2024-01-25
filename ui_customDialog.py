from PyQt5.QtWidgets import QVBoxLayout, QDialog, QDialogButtonBox, QLabel 

class CustomDialog(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Information!")

        QBtn = QDialogButtonBox.Ok #| QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        label_message = QLabel(message)
        self.layout.addWidget(label_message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)