import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.drawing_canvas = QtWidgets.QLabel()
        self.output_panel = QtWidgets.QLabel()
        self.output_panel.setFixedSize(400, 400)
        canvas = QtGui.QPixmap(400, 400)
        canvas.fill(QtGui.QColor("white"))
        self.drawing_canvas.setPixmap(canvas)
        self.general_layout = QtWidgets.QHBoxLayout()
        self.general_layout.addWidget(self.drawing_canvas)
        self.general_layout.addWidget(self.output_panel)
        self.c_widget = QtWidgets.QWidget(self)
        self.c_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.c_widget)

        # enable mouse tracking.
        self.drawing_canvas.setMouseTracking(True)
        self.setMouseTracking(True)

        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, event) -> None:
        if self.last_x is None:
            return
        painter = QtGui.QPainter(self.drawing_canvas.pixmap())
        painter.drawLine(self.last_x, self.last_y, event.x(), event.y())
        painter.end()
        self.update()
        self.last_x = event.x()
        self.last_y = event.y()

    def mousePressEvent(self, event):
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseReleaseEvent(self, event):
        self.last_x = None
        self.last_y = None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec_()
