from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib import messages
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.models import Task


class TaskCreateView(CreateView):
    http_method_names = ['post']
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)

        messages.success(self.request, 'Task created!')

        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        return super(TaskCreateView, self).post(*args, **kwargs)
