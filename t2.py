import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Radio Buttons")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        label = QLabel("Please select an option:", self)

        rb_true = QRadioButton("True", self)
        rb_true.toggled.connect(self.update_label)

        rb_false = QRadioButton("False", self)
        rb_false.toggled.connect(self.update_label)

        self.result_label = QLabel("", self)

        layout.addWidget(label)
        layout.addWidget(rb_true)
        layout.addWidget(rb_false)
        layout.addWidget(self.result_label)

        self.show()

    def update_label(self):
        rb = self.sender()
        if rb.isChecked():
            self.result_label.setText(f"You selected {rb.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())