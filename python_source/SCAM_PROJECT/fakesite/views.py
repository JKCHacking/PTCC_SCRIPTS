import socket
from django.http import HttpResponse
from ipware import get_client_ip
from .models import User
# from pynput.keyboard import Key, Controller


def index(request):
    # keyboard = Controller()
    ip, is_routable = get_client_ip(request)
    host_info = socket.gethostbyaddr(ip)
    pc_name = host_info[0]  # name of the computer
    pc_name2 = request.META['REMOTE_HOST']
    pc_name3 = request.META['HTTP_HOST']
    print(ip)
    print(pc_name)
    print(pc_name2)
    print(pc_name3)
    # save to database
    user = User.objects.get_or_create(
        pc_name=pc_name,
        ip_add=ip
    )
    print(user)
    # with keyboard.pressed(Key.ctrl):
    #     keyboard.press('w')
    #     keyboard.release('w')
    return HttpResponse("Thank you for visiting.")
