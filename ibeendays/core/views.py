from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('app'))

    return render(request, 'home.html',
                  context_instance=RequestContext(request))


@login_required
def app(request):
    return render(request, 'app.html',
                  context_instance=RequestContext(request))


def login(request):
    return render(request, 'login.html',
                  context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)

    return redirect(settings.LOGOUT_REDIRECT_URL)
