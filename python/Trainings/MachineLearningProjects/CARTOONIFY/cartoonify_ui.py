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
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


class CartoonifyUI(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def open_cartoonified_dialog(self, image_path):
        cartoonified_dlg = CartoonifiedDialog(self)
        cartoonified_dlg.temp_img_path = image_path
        pixmap = cartoonified_dlg.create_pixmap(image_path)
        cartoonified_dlg.image_display.setPixmap(pixmap)
        cartoonified_dlg.setFixedSize(pixmap.width(), pixmap.height())
        cartoonified_dlg.save_btn.clicked.connect(cartoonified_dlg.save_image)
        cartoonified_dlg.exec_()
        return cartoonified_dlg

    def open_image_filename_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open File",
                                                   "H:\\",
                                                   "Image files (*.jpg *.png *jpeg)",
                                                   options=QFileDialog.DontUseNativeDialog)
        self.image_path_le.setText(file_path)

    def messagebox(self, message, icon):
        msg = QMessageBox()
        if icon == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class CartoonifiedDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CartoonifiedDialog, self).__init__(*args, **kwargs)
        self.temp_img_path = ""
        # cartoonify dialog
        image_name_layout = QHBoxLayout()
        self.image_name_le = QLineEdit()
        self.image_name_label = QLabel()
        self.image_name_label.setText("Image Name:")
        image_name_layout.addWidget(self.image_name_label)
        image_name_layout.addWidget(self.image_name_le)

        self.image_display = QLabel()
        self.default_image_pixmap = QPixmap('icons/no_image.png')
        self.image_display.setPixmap(self.default_image_pixmap)
        self.save_btn = QPushButton()
        self.save_btn.setText("SAVE")

        layout = QVBoxLayout()
        layout.addWidget(self.image_display)
        layout.addLayout(image_name_layout)
        layout.addWidget(self.save_btn)
        self.setWindowTitle("Dialog1")
        self.setLayout(layout)
        self.setFixedSize(self.default_image_pixmap.width(), self.default_image_pixmap.height())

    def create_pixmap(self, image_path):
        return QPixmap(image_path)

    def save_image(self):
        user_filename = self.image_name_le.text()
        img_dir = os.path.dirname(self.temp_img_path)
        img_filename, img_ext = os.path.splitext(os.path.basename(self.temp_img_path))
        if user_filename:
            dst_img_path = os.path.join(img_dir, "{}{}".format(user_filename, img_ext))
            if os.path.exists(dst_img_path):
                os.remove(dst_img_path)
            os.rename(self.temp_img_path, dst_img_path)
            os.remove(self.temp_img_path)
            self.close()
        else:
            self.messagebox("Please input a filename!", "Warning")

    def messagebox(self, message, icon):
        msg = QMessageBox()
        if icon == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
