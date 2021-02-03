import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap


class CartoonifyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_path = ""

        # main ui
        self.image_path_le = QLineEdit()
        self.upload_btn = QPushButton()
        self.upload_btn.setText("UPLOAD")
        self.cartoonify_btn = QPushButton()
        self.cartoonify_btn.setText("CARTOONIFY")

        self.setWindowTitle('Cartoonifier')
        self.setFixedSize(250, 120)

        self.c_widget = QWidget(self)
        self.setCentralWidget(self.c_widget)
        self.general_layout = QVBoxLayout()
        self.c_widget.setLayout(self.general_layout)
        self.open_main_ui()

    def open_main_ui(self):
        image_picker_layout = QHBoxLayout()
        image_picker_layout.addWidget(self.image_path_le)
        image_picker_layout.addWidget(self.upload_btn)

        self.general_layout.addLayout(image_picker_layout)
        self.general_layout.addWidget(self.cartoonify_btn)

    def open_cartoonified_dialog(self):
        cartoonified_dlg = CartoonifiedDialog(self)
        cartoonified_dlg.save_btn.clicked.connect(cartoonified_dlg.open_imagename_dlg)
        cartoonified_dlg.exec_()

    def open_image_filename_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open File",
                                                   "H:\\",
                                                   "Image files (*.jpg *.png *jpeg)",
                                                   options=QFileDialog.DontUseNativeDialog)
        self.image_path = file_path
        self.image_path_le.setText(os.path.basename(file_path))


class CartoonifiedDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CartoonifiedDialog, self).__init__(*args, **kwargs)
        # cartoonify dialog
        self.image_display = QLabel()
        self.default_image_pixmap = QPixmap('./icons/no_image.png')
        self.image_display.setPixmap(self.default_image_pixmap)
        self.save_btn = QPushButton()
        self.save_btn.setText("SAVE")

        layout = QVBoxLayout()
        layout.addWidget(self.image_display)
        layout.addWidget(self.save_btn)
        self.setWindowTitle("Dialog1")
        self.setLayout(layout)
        self.setFixedSize(self.default_image_pixmap.width(), self.default_image_pixmap.height())

    def open_imagename_dlg(self):
        set_filename_dlg = ImageNameDialog(self)
        set_filename_dlg.exec_()


class ImageNameDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ImageNameDialog, self).__init__(*args, **kwargs)

        self.image_name_le = QLineEdit()
        self.ok_btn = QPushButton()
        self.ok_btn.setText("OK")
        layout = QVBoxLayout()
        layout.addWidget(self.image_name_le)
        layout.addWidget(self.ok_btn)
        self.setLayout(layout)
        self.setWindowTitle("Set Image Filename")
        self.setFixedSize(250, 120)
