from django.conf import settings
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout


def home(request):
    return render(request, 'home.html',
                  context_instance=RequestContext(request))


def login(request):
    return render(request, 'login.html',
                  context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)

    return redirect(settings.LOGOUT_REDIRECT_URL)
