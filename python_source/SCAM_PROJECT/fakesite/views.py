import socket
from django.http import HttpResponse
from ipware import get_client_ip
from .models import User
# from pynput.keyboard import Key, Controller


def index(request):
    # keyboard = Controller()
    pub_ip, is_routable = get_client_ip(request)
    priv_ip = request.META['REMOTE_ADDR']
    host_info = socket.gethostbyaddr(pub_ip)
    pc_name = host_info[0]  # name of the computer

    # save to database
    user = User.objects.get_or_create(
        pc_name=pc_name,
        pub_ip=pub_ip,
        priv_ip=priv_ip
    )

    # with keyboard.pressed(Key.ctrl):
    #     keyboard.press('w')
    #     keyboard.release('w')
    return HttpResponse("Something went wrong. Please try again later.")
