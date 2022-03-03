import sys
from gui import Application


def main():
    app = Application(sys.argv)
    app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
