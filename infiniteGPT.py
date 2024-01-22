from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QWidget
import sys

class Eight(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the center of the figure and its size
        center = QPointF(self.width() / 2, self.height() / 2)
        size = min(self.width(), self.height()) / 2 - 10

        # Create a rectangle that bounds the figure
        rect = QRectF(center.x() - size, center.y() - size / 2, size * 2, size)

        # Create a path that follows the shape of the figure
        path = QPainterPath()
        path.moveTo(rect.left(), rect.top() + rect.height() / 4)
        path.cubicTo(rect.left(), rect.top() - rect.height() / 4,
                     rect.left() + rect.width(), rect.top() - rect.height() / 4,
                     rect.left() + rect.width(), rect.top() + rect.height() / 4)
        path.cubicTo(rect.left() + rect.width(), rect.top() + rect.height() / 2 + rect.height() / 4,
                     rect.left(), rect.top() + rect.height() / 2 + rect.height() / 4,
                     rect.left(), rect.top() + rect.height() / 4)

        # Draw a line that follows the path
        painter.drawPath(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    eight = Eight()
    eight.show()
    sys.exit(app.exec_())