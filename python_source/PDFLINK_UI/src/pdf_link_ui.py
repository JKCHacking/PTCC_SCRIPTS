import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFileDialog


class PDFLinkUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.setWindowTitle('PDF Linker')
        self.setFixedSize(500, 135)

        self.c_widget = QWidget(self)
        self.setCentralWidget(self.c_widget)
        self.general_layout = QVBoxLayout()
        self.c_widget.setLayout(self.general_layout)

        self.create_ui()

    def create_ui(self):
        # initializing widgets
        keyword_line_edit = QLineEdit()
        keyword_line_edit.setObjectName("keyword_le")

        page_line_edit = QLineEdit()
        page_line_edit.setObjectName("page_le")

        pdf_file_line_edit = QLineEdit()
        pdf_file_line_edit.setObjectName('pdf_file_le')
        pdf_file_line_edit.setReadOnly(True)

        browse_button = QPushButton()
        browse_button.setObjectName("browse_btn")
        browse_button.setText("Browse")

        file_picker_layout = QHBoxLayout()
        file_picker_layout.addWidget(pdf_file_line_edit)
        file_picker_layout.addWidget(browse_button)

        form_layout = QFormLayout()
        form_layout.addRow('Keyword:', keyword_line_edit)
        form_layout.addRow('Page:', page_line_edit)
        form_layout.addRow('PDF File', file_picker_layout)
        self.general_layout.addLayout(form_layout)
        self.buttons["Browse"] = browse_button

        # initializing ok and cancel buttons
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        ok_button = buttons.accepted
        cancel_button = buttons.rejected
        self.general_layout.addWidget(buttons)
        self.buttons["Ok"] = ok_button
        self.buttons["Cancel"] = cancel_button

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open File",
                                                   "H:\Desktop",
                                                   "*.pdf",
                                                   options=QFileDialog.DontUseNativeDialog)

        # accessing the QlineEdit of File picker
        widget = self.get_widget_by_name(self.general_layout, "pdf_file_le")
        widget.setText(os.path.basename(file_path))

    def get_widget_by_name(self, layout, widget_name):
        print("getting widget {} on layout {}".format(widget_name, layout))
        root_layout = layout
        widget = self.find_widget_in_layout(root_layout, widget_name)
        if not widget:
            for layout in self.visit(root_layout):
                widget = self.find_widget_in_layout(layout, widget_name)
                if widget:
                    break
            if not widget:
                print("Failed to find widget: {}".format(widget_name))
        return widget

    # going to apply visitor design pattern
    def visit(self, tree):
        """
            Example:
                layout
                    sublayout1
                        sublayout11
                        widget11
                        widget12
                    sublayout2
                        sublayout21
                        sublayout22
                        widget21
                    widget1
                    widget2
        """
        visited = set()
        not_visited = set()
        if tree.children():
            not_visited.update(tree.children())

        while not_visited:
            item = not_visited.pop()
            if item in visited:
                continue
            visited.add(item)
            yield item
            if item.children():
                not_visited.update(item.children())

    def find_widget_in_layout(self, layout, widget_name):
        widget = None
        count = layout.count()
        while count >= 0:
            layout_item = layout.itemAt(count)
            if layout_item:
                temp_widget = layout_item.widget()
                if temp_widget and temp_widget.objectName() == widget_name:
                    widget = temp_widget
                    break
            count -= 1
        return widget
