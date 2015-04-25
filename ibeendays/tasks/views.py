from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from ibeendays.tasks.models import Task


class TaskListView(ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        qs = super(TaskListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)


@login_required
def app(request):
    return render(request, 'app.html',
                  context_instance=RequestContext(request))
