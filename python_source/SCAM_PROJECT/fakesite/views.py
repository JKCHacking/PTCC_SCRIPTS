from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ipware import get_client_ip
from .models import User, Visitor
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request, username):
    pub_ip, is_routable = get_client_ip(request)

    Visitor.objects.get_or_create(
        username=username,
        pub_ip=pub_ip
    )

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the email from the form
            email = form.cleaned_data['email']
            # save to database
            User.objects.get_or_create(
                email=email
            )
            return HttpResponseRedirect('error/')
    else:
        form = LoginForm()

    return render(request, 'fake_login.html', {'form': form})


def fake_error(request, username):
    return HttpResponse('Servers are busy, please try again later.')
