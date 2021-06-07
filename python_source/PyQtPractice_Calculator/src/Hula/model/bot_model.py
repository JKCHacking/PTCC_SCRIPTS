import json
import fbchat


class BotModel:
    def __init__(self):
        self.session = None

    def create_session(self, email, password):
        session_cookies = self.__get_cookies()
        try:
            self.session = fbchat.Session.from_cookies(session_cookies)
        except fbchat.FacebookError as fb_err:
            print(str(fb_err))

    def get_session(self):
        return self.session

    def __get_cookies(self):
        cookie_path = "H:\\Desktop\\My Documents\\HulaAutomation\\session.json"
        with open(cookie_path) as f:
            data = json.load(f)
        return data