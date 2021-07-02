from comtypes import client


class AppCreator:
    def __init__(self, app_progid):
        try:
            self.app = client.GetActiveObject(app_progid, dynamic=True)
        except OSError:
            self.app = client.CreateObject(app_progid, dynamic=True)

    def get_app(self):
        return self.app
