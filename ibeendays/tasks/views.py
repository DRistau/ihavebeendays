from django.views.generic import CreateView, ListView
from ibeendays.tasks.models import Task


class TaskListView(ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        qs = super(TaskListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user).finished()


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'user']
    success_url = '/tasks/'

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['data']['user'] = self.request.user.pk

        return kwargs
