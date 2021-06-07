import sys
from PyQt5.QtWidgets import QApplication
from model.hula_bot import BotModel
from controller.login import LoginCtrl
from controller.hula_bot import BotCtrl
from view.hula_bot import BotUI
from view.login import LoginUI


def main():
    app = QApplication(sys.argv)

    bot_model = BotModel()
    bot_view = BotUI()
    bot_ctrl = BotCtrl(bot_view, bot_model)

    login_view = LoginUI()
    login_ctrl = LoginCtrl(login_view, bot_model, bot_ctrl)
    login_ctrl.init_UI()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
