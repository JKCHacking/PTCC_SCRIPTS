import socket
from django.http import HttpResponse
from ipware import get_client_ip
from .models import User
from pywinauto.keyboard import send_keys


def index(request):
    ip, is_routable = get_client_ip(request)
    host_info = socket.gethostbyaddr(ip)
    pc_name = host_info[0]  # name of the computer
    print(ip)
    print(pc_name)
    # save to database
    user = User.objects.get_or_create(
        pc_name=pc_name,
        ip_add=ip
    )
    print(user)
    send_keys("^w")
    return HttpResponse("Thank you for visiting.")
