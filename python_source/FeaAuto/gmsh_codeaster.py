import sys
import gmsh
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox


class GUI(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.width_label = QLabel("Width:")
        self.height_label = QLabel("Height:")
        self.thickness_label = QLabel("Thickness:")
        self.e_modulus_label = QLabel("Elastic Modulus:")
        self.pressure_label = QLabel("Pressure:")

        self.width_edit = QLineEdit()
        self.height_edit = QLineEdit()
        self.thickness_edit = QLineEdit()
        self.e_modulus_edit = QLineEdit()
        self.pressure_edit = QLineEdit()

        self.width_edit.setFixedHeight(22)
        self.height_edit.setFixedHeight(22)
        self.thickness_edit.setFixedHeight(22)
        self.e_modulus_edit.setFixedHeight(22)
        self.pressure_edit.setFixedHeight(22)

        # set double validator to each line edit
        validator = QDoubleValidator()
        self.width_edit.setValidator(validator)
        self.height_edit.setValidator(validator)
        self.thickness_edit.setValidator(validator)
        self.e_modulus_edit.setValidator(validator)
        self.pressure_edit.setValidator(validator)

        self.run_button = QPushButton("RUN")
        button_css = """
                    QPushButton{
                        border-radius:5px;
                        border:1px solid black;
                        border-style: outset;
                        background-color:#00FF00;
                    }
                    QPushButton:pressed {
                        background-color:#757575;
                    }
                """
        self.run_button.setStyleSheet(button_css)
        self.run_button.setFixedHeight(30)
        self.run_button.setFixedWidth(75)

        self.general_layout = QVBoxLayout()
        self.c_widget = QWidget()
        self.c_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.c_widget)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PLATE FEA")
        self.setFixedSize(250, 250)

        input_layout = QFormLayout()
        input_layout.setVerticalSpacing(15)
        input_layout.addRow(self.width_label, self.width_edit)
        input_layout.addRow(self.height_label, self.height_edit)
        input_layout.addRow(self.thickness_label, self.thickness_edit)
        input_layout.addRow(self.e_modulus_label, self.e_modulus_edit)
        input_layout.addRow(self.pressure_label, self.pressure_edit)

        self.general_layout.addLayout(input_layout)
        self.general_layout.addWidget(self.run_button, alignment=QtCore.Qt.AlignCenter)

    def display_message_box(self, message, level="info"):
        msg = QMessageBox()
        if level == "info":
            msg.setIcon(QMessageBox.Information)
        elif level == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif level == "error":
            msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()

    def run_simulation(self):
        width_plate = self.check_input(self.view.width_edit)
        height_plate = self.check_input(self.view.height_edit)
        thick_plate = self.check_input(self.view.thickness_edit)
        e_modulus = self.check_input(self.view.e_modulus_edit)
        pressure = self.check_input(self.view.pressure_edit)

        if width_plate and height_plate and thick_plate and e_modulus and pressure:
            # generate mesh
            self.model.generate_mesh(width_plate, height_plate, thick_plate)
            # prepare comm file
            # prepare export file
            # run code aster

    def connect_signals(self):
        self.view.run_button.clicked.connect(self.run_simulation)

    def check_input(self, line_edit):
        try:
            val = int(line_edit.text())
        except ValueError:
            val = 0

        if val <= 0:
            color = QColor(250, 160, 160)
            palette = QPalette()
            palette.setColor(QPalette.Base, color)
            line_edit.setPalette(palette)
        else:
            color = QColor(255, 255, 255)
            palette = QPalette()
            palette.setColor(QPalette.Base, color)
            line_edit.setPalette(palette)
        return val


class Model:
    def generate_mesh(self, w, h, t):
        lc = 1e-2
        # create the points of the plate
        p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
        p2 = gmsh.model.geo.addPoint(w, 0, 0, lc)
        p3 = gmsh.model.geo.addPoint(w, h, 0, lc)
        p4 = gmsh.model.geo.addPoint(0, h, 0, lc)
        p5 = gmsh.model.geo.addPoint(0, 0, t, lc)
        p6 = gmsh.model.geo.addPoint(w, 0, t, lc)
        p7 = gmsh.model.geo.addPoint(w, h, t, lc)
        p8 = gmsh.model.geo.addPoint(0, h, t, lc)

        # create the lines of the plate
        l1 = gmsh.model.geo.addLine(p1, p2)
        l2 = gmsh.model.geo.addLine(p2, p3)
        l3 = gmsh.model.geo.addLine(p3, p4)
        l4 = gmsh.model.geo.addLine(p4, p1)
        l5 = gmsh.model.geo.addLine(p5, p6)
        l6 = gmsh.model.geo.addLine(p6, p7)
        l7 = gmsh.model.geo.addLine(p7, p8)
        l8 = gmsh.model.geo.addLine(p8, p5)
        l9 = gmsh.model.geo.addLine(p1, p5)
        l10 = gmsh.model.geo.addLine(p6, p2)
        l11 = gmsh.model.geo.addLine(p7, p3)
        l12 = gmsh.model.geo.addLine(p4, p8)

        # create curve loops
        cl1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
        cl2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
        cl3 = gmsh.model.geo.addCurveLoop([l9, l5, l10, -l1])
        cl4 = gmsh.model.geo.addCurveLoop([l11, l3, l12, -l7])
        cl5 = gmsh.model.geo.addCurveLoop([l12, l8, -l9, -l4])
        cl6 = gmsh.model.geo.addCurveLoop([l10, l2, -l11, -l6])

        # create surface
        s1 = gmsh.model.geo.addPlaneSurface([cl1])
        s2 = gmsh.model.geo.addPlaneSurface([cl2])
        s3 = gmsh.model.geo.addPlaneSurface([cl3])
        s4 = gmsh.model.geo.addPlaneSurface([cl4])
        s5 = gmsh.model.geo.addPlaneSurface([cl5])
        s6 = gmsh.model.geo.addPlaneSurface([cl6])

        # create surface loop
        plate_loop = gmsh.model.geo.addSurfaceLoop([s1, s2, s3, s4, s5, s6])
        plate = gmsh.model.geo.addVolume([plate_loop])

        # create the groups
        gmsh.model.addPhysicalGroup(2, [s1], name="TOP_FACE")
        gmsh.model.addPhysicalGroup(2, [s2], name="BOT_FACE")
        gmsh.model.addPhysicalGroup(2, [s3], name="FRONT_FACE")
        gmsh.model.addPhysicalGroup(2, [s4], name="BACK_FACE")
        gmsh.model.addPhysicalGroup(2, [s5], name="LEFT_FACE")
        gmsh.model.addPhysicalGroup(2, [s6], name="RIGHT_FACE")

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)
        if "-nopopup" not in sys.argv:
            gmsh.fltk.run()
        gmsh.finalize()

    def run_code_aster(self):
        pass

    def display_result(self):
        pass


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self.model = Model()
        self.view = GUI()
        self.controller = Controller(self.model, self.view)

    def show(self):
        self.view.show()


def main():
    app = Application(sys.argv)
    app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
