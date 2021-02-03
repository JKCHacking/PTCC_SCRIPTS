import sys
from PyQt5.QtWidgets import QApplication
from cartoonify import Cartoonify
from cartoonify_ui import CartoonifyUI
from controller import Controller


class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.model = Cartoonify
        self.view = CartoonifyUI()
        self.view.show()
        self.controller = Controller(self.model, self.view)


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
