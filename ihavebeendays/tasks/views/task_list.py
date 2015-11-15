from django.views.generic import ListView
from ihavebeendays.tasks.forms import TaskForm
from ihavebeendays.tasks.models import Task


class TaskListView(ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        qs = super(TaskListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user).finished()

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['task_started'] = self.model.objects.filter(user=self.request.user).unfinished()
        context['task_form'] = TaskForm()

        return context
