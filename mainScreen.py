from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QDesktopWidget
import sys
from infiniteMove import InfiniteMove

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w = InfiniteMove()
        screen = QDesktopWidget().screenGeometry(1)
        self.w.setGeometry(screen)
        self.w.showMaximized()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
