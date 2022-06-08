import sys
import os
import gmsh
import subprocess
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox


AS_RUN = "C:/Users/{}/Local Settings/code_aster/V2021/bin/as_run.bat".format(os.getlogin())
SRC_PATH = ""
if getattr(sys, "frozen", False):
    SRC_PATH = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    SRC_PATH = os.path.dirname(os.path.realpath(__file__))


def except_hook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press enter to exit...")


sys.excepthook = except_hook


class GUI(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.width_label = QLabel("Width:")
        self.height_label = QLabel("Height:")
        self.thickness_label = QLabel("Thickness:")
        self.e_modulus_label = QLabel("Elastic Modulus:")
        self.pressure_label = QLabel("Pressure:")
        self.size_label = QLabel("Size:")

        self.width_edit = QLineEdit()
        self.height_edit = QLineEdit()
        self.thickness_edit = QLineEdit()
        self.e_modulus_edit = QLineEdit()
        self.pressure_edit = QLineEdit()
        self.size_edit = QLineEdit()

        self.width_edit.setFixedHeight(22)
        self.height_edit.setFixedHeight(22)
        self.thickness_edit.setFixedHeight(22)
        self.e_modulus_edit.setFixedHeight(22)
        self.pressure_edit.setFixedHeight(22)
        self.size_edit.setFixedHeight(22)

        # set double validator to each line edit
        validator = QDoubleValidator()
        self.width_edit.setValidator(validator)
        self.height_edit.setValidator(validator)
        self.thickness_edit.setValidator(validator)
        self.e_modulus_edit.setValidator(validator)
        self.pressure_edit.setValidator(validator)
        self.size_edit.setValidator(validator)

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
        # self.setFixedSize(250, 300)

        dimension_form = QFormLayout()
        dimension_form.setVerticalSpacing(15)
        dimension_form.addRow(self.width_label, self.width_edit)
        dimension_form.addRow(self.height_label, self.height_edit)
        dimension_form.addRow(self.thickness_label, self.thickness_edit)

        mesh_form = QFormLayout()
        mesh_form.addRow(self.size_label, self.size_edit)

        solver_form = QFormLayout()
        solver_form.setVerticalSpacing(15)
        solver_form.addRow(self.e_modulus_label, self.e_modulus_edit)
        solver_form.addRow(self.pressure_label, self.pressure_edit)

        dimension_group = QGroupBox("DIMENSION")
        dimension_group.setLayout(dimension_form)
        mesh_group = QGroupBox("MESH")
        mesh_group.setLayout(mesh_form)
        solver_group = QGroupBox("SOLVER")
        solver_group.setLayout(solver_form)

        self.general_layout.addWidget(dimension_group)
        self.general_layout.addWidget(mesh_group)
        self.general_layout.addWidget(solver_group)
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
        size = self.view.size_edit.text()
        try:
            size = float(size)
        except ValueError:
            size = 0
            self.view.size_edit.setText("0")

        if width_plate and height_plate and thick_plate and e_modulus and pressure:
            # generate mesh
            self.model.generate_mesh(width_plate, height_plate, thick_plate, size)
            # run code aster
            res = self.model.run_code_aster(e_modulus, pressure)
            if res == -1:
                print("Errored has occured, Please check logs.")
            else:
                # display the output in the GMSH Display.
                self.model.display_result()

    def connect_signals(self):
        self.view.run_button.clicked.connect(self.run_simulation)

    def check_input(self, line_edit):
        try:
            val = float(line_edit.text())
        except ValueError:
            val = 0

        if val <= 0:
            color = QColor(250, 160, 160)  # red
            palette = QPalette()
            palette.setColor(QPalette.Base, color)
            line_edit.setPalette(palette)
        else:
            color = QColor(255, 255, 255)  # white
            palette = QPalette()
            palette.setColor(QPalette.Base, color)
            line_edit.setPalette(palette)
        return val


class Model:
    def generate_mesh(self, w, h, t, size):
        gmsh.initialize(sys.argv)
        gmsh.model.add("MESH_PLATE")
        # create the points of the plate
        p1 = gmsh.model.geo.addPoint(0, 0, 0, size)
        p2 = gmsh.model.geo.addPoint(w, 0, 0, size)
        p3 = gmsh.model.geo.addPoint(w, h, 0, size)
        p4 = gmsh.model.geo.addPoint(0, h, 0, size)
        p5 = gmsh.model.geo.addPoint(0, 0, t, size)
        p6 = gmsh.model.geo.addPoint(w, 0, t, size)
        p7 = gmsh.model.geo.addPoint(w, h, t, size)
        p8 = gmsh.model.geo.addPoint(0, h, t, size)

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
        gmsh.model.addPhysicalGroup(2, [s1], name="BOT_F")
        gmsh.model.addPhysicalGroup(2, [s2], name="TOP_F")
        gmsh.model.addPhysicalGroup(2, [s3], name="FRONT_F")
        gmsh.model.addPhysicalGroup(2, [s4], name="BACK_F")
        gmsh.model.addPhysicalGroup(2, [s5], name="LEFT_F")
        gmsh.model.addPhysicalGroup(2, [s6], name="RIGHT_F")
        gmsh.model.addPhysicalGroup(3, [plate], name="PLATE_V")

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)
        gmsh.write("plate.unv")

    def run_code_aster(self, e_mod, pres):
        self.generate_comm(e_mod, pres)
        self.generate_export()
        # run the code_aster
        res = self.run_command([AS_RUN, "export.export"])
        return res

    def generate_comm(self, e_mod, pres):
        # generate the command file
        with open("command.txt", mode="r") as comm_template:
            contents = comm_template.read()
        contents = contents.format(elastic_modulus=e_mod, pressure=pres)
        with open("command.comm", mode="w") as comm_file:
            comm_file.write(contents)

    def generate_export(self):
        # generate the export file
        with open("export.txt", mode="r") as export_template:
            contents = export_template.read()
        contents = contents.format(work_dir=SRC_PATH)
        with open("export.export", mode="w") as export_file:
            export_file.write(contents)

    def run_command(self, command):
        test_file = "test.log"
        ret = 1
        with open(test_file, "wb") as f:
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                for c in iter(lambda: process.stdout.read(1), b""):
                    sys.stdout.buffer.write(c)
                    f.write(c)
            except FileNotFoundError:
                print("Cannot find Code_Aster v15 Windows Installation")
                f.write(b"Cannot find Code_Aster v15 Windows Installation")
                ret = -1
        return ret

    def display_result(self):
        gmsh.open("plate.msh")
        if "nopopup" not in sys.argv:
            gmsh.fltk.run()
        gmsh.finalize()


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
