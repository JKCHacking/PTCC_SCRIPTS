import sys
from PyQt5.QtWidgets import QApplication
from model.bot_model import BotModel
from model.hula_model import HulaModel
from controller.login_controller import LoginCtrl
from controller.bot_controller import BotCtrl
from controller.hula_controller import HulaController
from view.bot_ui import BotUI
from view.login_ui import LoginUI
from view.hula_ui import HulaUI


def main():
    app = QApplication(sys.argv)

    bot_model = BotModel()
    bot_view = BotUI()
    bot_ctrl = BotCtrl(bot_view, bot_model)

    login_view = LoginUI()
    login_ctrl = LoginCtrl(login_view, bot_model, bot_ctrl)

    hula_model = HulaModel()
    hula_ui = HulaUI()
    hula_controller = HulaController(hula_ui, hula_model, login_ctrl)
    hula_controller.connect_bot_signal(bot_ctrl.message_received)
    hula_controller.init_UI()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
