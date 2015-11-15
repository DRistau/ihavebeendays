from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django.contrib import messages
from ihavebeendays.tasks.forms import TaskResetForm
from ihavebeendays.tasks.models import Task


class TaskResetView(UpdateView):
    model = Task
    form_class = TaskResetForm
    template_name = 'tasks/task_reset_form.html'
    success_url = reverse_lazy('tasks')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.reset()
            messages.success(self.request, 'Task reseted!')

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 uuid=self.kwargs.get('uuid'))

    def get_queryset(self):
        qs = super(TaskResetView, self).get_queryset()
        return qs.filter(user=self.request.user).unfinished()
