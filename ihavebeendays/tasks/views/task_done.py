from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django.contrib import messages
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.models import Task


class TaskDoneView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.done()

        messages.success(self.request, 'Task done!')

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 uuid=self.kwargs.get('uuid'))

    def get_queryset(self):
        qs = super(TaskDoneView, self).get_queryset()
        return qs.filter(user=self.request.user).unfinished()
