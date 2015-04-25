from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template import RequestContext


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('app'))

    return render(request, 'home.html',
                  context_instance=RequestContext(request))
