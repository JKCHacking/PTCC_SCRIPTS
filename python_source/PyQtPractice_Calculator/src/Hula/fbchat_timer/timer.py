import fbchat
import fbchat.models as fb_models
import datetime
import json
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def get_cookies():
    cookie_path = "H:\\Desktop\\My Documents\\HulaAutomation\\session.json"
    with open(cookie_path) as f:
        data = json.load(f)
    return data


def timer():
    message = "Joshnee Kim Cunanan"
    scheduled_time_input = "5:00:00 PM"

    love_chat_id = "100000370955526"  # Love's id for testing
    love_thread_type = fbchat.ThreadType.USER

    family_chat_id = "1664712073847423"
    family_thread_type = fbchat.ThreadType.GROUP

    hula_chat_id = "3560959980690725"
    hula_thread_type = fbchat.ThreadType.GROUP

    chat_id = love_chat_id
    thread_type = love_thread_type

    now = datetime.datetime.now()
    scheduled_time_obj = datetime.datetime.strptime(scheduled_time_input, "%I:%M:%S %p")
    scheduled_time = now.replace(hour=scheduled_time_obj.hour,
                                 minute=scheduled_time_obj.minute,
                                 second=scheduled_time_obj.second)

    session_cookies = get_cookies()

    client = fbchat.Client("dummy_email@gmail.com", "dummy_password", session_cookies=session_cookies)
    if client.isLoggedIn():
        print("Login Successful: {}".format(client.uid))

    while True:
        if scheduled_time < datetime.datetime.now():
            client.send(fb_models.Message(text=message), thread_id=chat_id, thread_type=thread_type)
            print("\rMessage sent!")
            break
        else:
            current_time = datetime.datetime.now()
            remaining = scheduled_time - current_time
            time_remaining_string = strfdelta(remaining, "Time Remaining: %H:%M:%S")
            print("\r{}".format(time_remaining_string), end="", flush=True)


if __name__ == "__main__":
    timer()
